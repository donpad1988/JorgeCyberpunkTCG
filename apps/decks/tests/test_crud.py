from django.test import Client, TestCase
from django.urls import reverse

from apps.decks.models import Deck

from .helpers import DeckTestMixin


class DeckCrudSecurityTests(DeckTestMixin, TestCase):
    def urls(self, deck):
        kwargs = {"username": deck.owner.username, "slug": deck.slug}
        return {
            "detail": reverse("decks:deck_detail", kwargs=kwargs),
            "update": reverse("decks:deck_update", kwargs=kwargs),
            "delete": reverse("decks:deck_delete", kwargs=kwargs),
        }

    def test_my_decks_requires_login_and_only_lists_the_owner_decks(self):
        own = self.create_deck("Own")
        other = self.create_deck("Other", owner=self.other_owner)

        self.assertRedirects(self.client.get(reverse("decks:my_decks")), "/cuenta/login/?next=/mazos/")
        self.client.force_login(self.owner)
        response = self.client.get(reverse("decks:my_decks"))

        self.assertContains(response, own.name)
        self.assertNotContains(response, other.name)

    def test_public_list_exposes_only_public_decks(self):
        public = self.create_deck("Public", owner=self.other_owner, is_public=True)
        private = self.create_deck("Private", owner=self.other_owner)

        response = self.client.get(reverse("decks:public_decks"))

        self.assertContains(response, public.name)
        self.assertNotContains(response, private.name)

    def test_authenticated_create_sets_request_user_and_private_default(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("decks:deck_create"),
            {"name": "Mi primer mazo", "description": "Nota", "owner": self.other_owner.pk},
        )
        deck = Deck.objects.get(name="Mi primer mazo")

        self.assertRedirects(response, reverse("decks:deck_detail", args=[self.owner.username, deck.slug]))
        self.assertEqual(deck.owner, self.owner)
        self.assertFalse(deck.is_public)
        self.assertEqual(deck.slug, "mi-primer-mazo")

    def test_create_requires_login_and_rejects_same_owner_slug_collision(self):
        self.create_deck("Existing")
        self.assertRedirects(self.client.get(reverse("decks:deck_create")), "/cuenta/login/?next=/mazos/crear/")
        self.client.force_login(self.owner)

        response = self.client.post(reverse("decks:deck_create"), {"name": "Existing"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya tienes un mazo con este nombre.")
        self.assertEqual(Deck.objects.filter(owner=self.owner).count(), 1)

    def test_private_detail_is_hidden_from_other_users_and_anonymous(self):
        deck = self.create_deck("Private")
        url = self.urls(deck)["detail"]

        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.other_owner)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_public_detail_is_visible_to_everyone_but_not_editable_by_others(self):
        deck = self.create_deck("Public", is_public=True)
        urls = self.urls(deck)

        self.assertEqual(self.client.get(urls["detail"]).status_code, 200)
        self.client.force_login(self.other_owner)
        self.assertEqual(self.client.get(urls["detail"]).status_code, 200)
        self.assertEqual(self.client.get(urls["update"]).status_code, 404)
        self.assertEqual(self.client.post(urls["delete"]).status_code, 404)
        self.assertTrue(Deck.objects.filter(pk=deck.pk).exists())

    def test_owner_can_update_metadata_without_owner_or_slug_manipulation(self):
        deck = self.create_deck("Original", is_public=False)
        original_slug = deck.slug
        self.client.force_login(self.owner)

        response = self.client.post(
            self.urls(deck)["update"],
            {"name": "Renamed", "description": "Updated", "is_public": "on", "owner": self.other_owner.pk, "slug": "other"},
        )
        deck.refresh_from_db()

        self.assertRedirects(response, self.urls(deck)["detail"])
        self.assertEqual(deck.owner, self.owner)
        self.assertEqual(deck.slug, original_slug)
        self.assertEqual(deck.name, "Renamed")
        self.assertTrue(deck.is_public)

    def test_update_requires_owner_and_does_not_change_composition(self):
        deck = self.create_deck("Deck")
        self.add_entry(deck, self.create_card("Main"))
        self.client.force_login(self.other_owner)

        response = self.client.post(self.urls(deck)["update"], {"name": "Hijacked"})

        self.assertEqual(response.status_code, 404)
        deck.refresh_from_db()
        self.assertEqual(deck.name, "Deck")
        self.assertEqual(deck.entries.count(), 1)

    def test_delete_requires_owner_and_post(self):
        deck = self.create_deck("Delete")
        urls = self.urls(deck)
        self.client.force_login(self.owner)

        self.assertEqual(self.client.get(urls["delete"]).status_code, 200)
        self.assertTrue(Deck.objects.filter(pk=deck.pk).exists())
        self.assertEqual(self.client.post(urls["delete"]).status_code, 302)
        self.assertFalse(Deck.objects.filter(pk=deck.pk).exists())

    def test_delete_requires_login_and_owner(self):
        deck = self.create_deck("Protected delete")
        url = self.urls(deck)["delete"]
        self.assertRedirects(self.client.get(url), f"/cuenta/login/?next={url}")
        self.client.force_login(self.other_owner)
        self.assertEqual(self.client.post(url).status_code, 404)

    def test_mutating_forms_keep_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)

        response = client.post(reverse("decks:deck_create"), {"name": "CSRF deck"})

        self.assertEqual(response.status_code, 403)

    def test_detail_shows_read_only_composition_and_partial_validation(self):
        deck = self.create_deck("Read only")
        legend = self.create_card("Legend", card_type="LEGEND")
        main = self.create_card("Main")
        self.add_legend(deck, legend)
        self.add_entry(deck, main, 2)

        self.client.force_login(self.owner)
        response = self.client.get(self.urls(deck)["detail"])

        self.assertContains(response, "Legend")
        self.assertContains(response, "2 × Main")
        self.assertContains(response, "NOT_EVALUATED")
        self.assertNotContains(response, "Añadir carta")

    def test_navbar_links_mazos_without_pending_label_for_all_session_states(self):
        anonymous = self.client.get(reverse("decks:public_decks"))
        self.assertContains(anonymous, reverse("decks:public_decks"))
        self.assertNotContains(anonymous, "Mazos <small>Próximamente</small>", html=False)

        self.client.force_login(self.owner)
        authenticated = self.client.get(reverse("decks:my_decks"))
        self.assertContains(authenticated, reverse("decks:my_decks"))
        self.assertNotContains(authenticated, "Mazos <small>Próximamente</small>", html=False)
