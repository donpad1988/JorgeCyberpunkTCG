from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.decks.models import Deck, DeckEditorialProfile, DeckKeyCard

from .helpers import DeckTestMixin


class DeckEditorialModelTests(DeckTestMixin, TestCase):
    def test_each_deck_gets_one_optional_editorial_profile_and_it_cascades(self):
        deck = self.create_deck("Editorial")
        profile = deck.editorial_profile

        self.assertEqual(profile.deck, deck)
        self.assertEqual(DeckEditorialProfile.objects.filter(deck=deck).count(), 1)
        deck.delete()
        self.assertFalse(DeckEditorialProfile.objects.filter(pk=profile.pk).exists())

    def test_key_card_must_belong_to_the_deck_and_is_unique(self):
        deck = self.create_deck("Key cards")
        included = self.create_card("Included")
        excluded = self.create_card("Excluded")
        self.add_entry(deck, included)
        profile = deck.editorial_profile

        key_card = DeckKeyCard(profile=profile, card=included, editorial_note="Rol propio.", display_order=2)
        key_card.full_clean()
        key_card.save()
        with self.assertRaises(ValidationError):
            DeckKeyCard(profile=profile, card=excluded).full_clean()
        with self.assertRaises(ValidationError):
            DeckKeyCard(profile=profile, card=included).full_clean()


class DeckEditorialViewTests(DeckTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.deck = self.create_deck("Tactical file", is_public=True)
        self.legend = self.create_card("Legend", card_type="LEGEND")
        self.main = self.create_card("Main")
        self.add_legend(self.deck, self.legend)
        self.add_entry(self.deck, self.main, 2)
        profile = self.deck.editorial_profile
        profile.archetype = "Control táctico"
        profile.short_summary = "Resumen editorial propio."
        profile.strategy_overview = "Estrategia editorial propia."
        profile.game_plan = "Plan flexible propio."
        profile.strengths = "Fortaleza propia."
        profile.weaknesses = "Debilidad propia."
        profile.save()
        DeckKeyCard.objects.create(profile=profile, card=self.main, editorial_note="Carta clave propia.", display_order=1)

    def urls(self, deck=None):
        deck = deck or self.deck
        kwargs = {"username": deck.owner.username, "slug": deck.slug}
        return {
            "detail": reverse("decks:deck_detail", kwargs=kwargs),
            "editorial": reverse("decks:deck_editorial_update", kwargs=kwargs),
        }

    def editorial_payload(self):
        return {
            "archetype": "Tempo",
            "short_summary": "Un resumen original actualizado.",
            "strategy_overview": "Una estrategia original.",
            "game_plan": "Un plan único y flexible.",
            "strengths": "Una fortaleza.",
            "weaknesses": "Una debilidad.",
            "key_cards-TOTAL_FORMS": "1",
            "key_cards-INITIAL_FORMS": "1",
            "key_cards-MIN_NUM_FORMS": "0",
            "key_cards-MAX_NUM_FORMS": "1000",
            "key_cards-0-id": str(self.deck.editorial_profile.key_cards.get().pk),
            "key_cards-0-card": str(self.main.pk),
            "key_cards-0-editorial_note": "Nueva explicación propia.",
            "key_cards-0-display_order": "3",
            "owner": str(self.other_owner.pk),
            "entries": "999",
        }

    def test_public_tactical_file_is_read_only_and_links_public_cards(self):
        response = self.client.get(self.urls()["detail"])

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TACTICAL DECK FILE")
        self.assertContains(response, "Resumen editorial propio.")
        self.assertContains(response, "2 × Main")
        self.assertContains(response, reverse("cards:detail", args=[self.legend.slug]))
        self.assertContains(response, reverse("cards:detail", args=[self.main.slug]))
        self.assertNotContains(response, "Editar contenido")

    def test_private_deck_and_editorial_are_owner_only(self):
        self.deck.is_public = False
        self.deck.save()
        self.assertEqual(self.client.get(self.urls()["detail"]).status_code, 404)
        self.assertRedirects(self.client.get(self.urls()["editorial"]), f"/cuenta/login/?next={self.urls()['editorial']}")
        self.client.force_login(self.other_owner)
        self.assertEqual(self.client.get(self.urls()["detail"]).status_code, 404)
        self.assertEqual(self.client.get(self.urls()["editorial"]).status_code, 404)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.urls()["detail"]).status_code, 200)

    def test_owner_can_update_editorial_without_changing_owner_or_composition(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.urls()["editorial"], self.editorial_payload())
        self.deck.refresh_from_db()
        profile = self.deck.editorial_profile

        self.assertRedirects(response, self.urls()["detail"])
        self.assertEqual(self.deck.owner, self.owner)
        self.assertEqual(self.deck.entries.get().quantity, 2)
        self.assertEqual(profile.short_summary, "Un resumen original actualizado.")
        self.assertEqual(profile.key_cards.get().editorial_note, "Nueva explicación propia.")

    def test_public_library_shows_editorial_summary_only_for_public_decks(self):
        private = self.create_deck("Hidden", owner=self.other_owner)
        private.editorial_profile.short_summary = "No visible"
        private.editorial_profile.save()

        response = self.client.get(reverse("decks:public_decks"))

        self.assertContains(response, 'id="published-decks-title"')
        self.assertContains(response, "Resumen editorial propio.")
        self.assertNotContains(response, private.name)
