from django.test import Client, TestCase
from django.urls import reverse

from apps.cards.models import Card, Set
from apps.decks.models import DeckEntry, DeckLegend

from .helpers import DeckTestMixin


class DeckBuilderTests(DeckTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.deck = self.create_deck("Builder")

    def url(self, name, deck=None):
        deck = deck or self.deck
        return reverse(name, args=[deck.owner.username, deck.slug])

    def post(self, name, payload, deck=None):
        return self.client.post(self.url(name, deck), payload)

    def test_builder_is_owner_only_even_for_public_decks(self):
        self.assertRedirects(self.client.get(self.url("decks:deck_builder")), f"/cuenta/login/?next={self.url('decks:deck_builder')}")
        self.deck.is_public = True
        self.deck.editorial_status = "PUBLISHED"
        self.deck.save()
        self.client.force_login(self.other_owner)
        self.assertEqual(self.client.get(self.url("decks:deck_builder")).status_code, 404)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.url("decks:deck_builder")).status_code, 200)

    def test_owner_can_add_and_remove_legend_but_not_duplicate_or_fourth(self):
        legends = [self.create_card(f"Legend {index}", card_type=Card.CardType.LEGEND) for index in range(4)]
        self.client.force_login(self.owner)
        self.post("decks:legend_add", {"card_id": legends[0].pk})
        self.post("decks:legend_add", {"card_id": legends[0].pk})
        self.assertEqual(DeckLegend.objects.filter(deck=self.deck).count(), 1)
        self.post("decks:legend_add", {"card_id": legends[1].pk})
        self.post("decks:legend_add", {"card_id": legends[2].pk})
        self.post("decks:legend_add", {"card_id": legends[3].pk})
        self.assertEqual(DeckLegend.objects.filter(deck=self.deck).count(), 3)
        legend_id = DeckLegend.objects.get(deck=self.deck, card=legends[0]).pk
        self.post("decks:legend_remove", {"entry_id": legend_id})
        self.assertEqual(DeckLegend.objects.filter(deck=self.deck).count(), 2)

    def test_non_legend_and_ineligible_card_are_rejected_as_legends(self):
        unit = self.create_card("Unit")
        draft_legend = self.create_card("Draft legend", card_type=Card.CardType.LEGEND, status=Card.Status.DRAFT)
        self.client.force_login(self.owner)
        self.post("decks:legend_add", {"card_id": unit.pk})
        self.post("decks:legend_add", {"card_id": draft_legend.pk})

        self.assertFalse(DeckLegend.objects.filter(deck=self.deck).exists())

    def test_main_add_increment_decrement_and_remove_follow_server_limits(self):
        card = self.create_card("Main")
        self.client.force_login(self.owner)
        for _ in range(3):
            self.post("decks:main_add", {"card_id": card.pk})
        entry = DeckEntry.objects.get(deck=self.deck, card=card)
        self.assertEqual(entry.quantity, 3)
        self.post("decks:main_add", {"card_id": card.pk})
        entry.refresh_from_db()
        self.assertEqual(entry.quantity, 3)
        self.post("decks:main_decrement", {"entry_id": entry.pk})
        entry.refresh_from_db()
        self.assertEqual(entry.quantity, 2)
        self.post("decks:main_decrement", {"entry_id": entry.pk})
        entry.refresh_from_db()
        self.assertEqual(entry.quantity, 1)
        self.post("decks:main_decrement", {"entry_id": entry.pk})
        self.assertFalse(DeckEntry.objects.filter(pk=entry.pk).exists())

    def test_main_rejects_legend_ineligible_and_unknown_card_ids(self):
        legend = self.create_card("Legend", card_type=Card.CardType.LEGEND)
        draft = self.create_card("Draft", status=Card.Status.DRAFT)
        self.client.force_login(self.owner)
        for card_id in (legend.pk, draft.pk, 999999):
            self.post("decks:main_add", {"card_id": card_id})

        self.assertFalse(DeckEntry.objects.filter(deck=self.deck).exists())

    def test_main_limit_of_fifty_blocks_direct_post(self):
        for index in range(17):
            quantity = 2 if index == 16 else 3
            self.add_entry(self.deck, self.create_card(f"Main {index}"), quantity)
        candidate = self.create_card("Candidate")
        self.client.force_login(self.owner)

        self.post("decks:main_add", {"card_id": candidate.pk})

        self.assertFalse(DeckEntry.objects.filter(deck=self.deck, card=candidate).exists())
        self.assertEqual(sum(entry.quantity for entry in self.deck.entries.all()), 50)

    def test_historical_unpublished_entry_stays_visible_but_cannot_increment(self):
        card = self.create_card("Historical")
        entry = self.add_entry(self.deck, card, 2)
        Card.objects.filter(pk=card.pk).update(status=Card.Status.DRAFT)
        self.client.force_login(self.owner)

        response = self.post("decks:main_add", {"card_id": card.pk})
        entry.refresh_from_db()
        self.assertEqual(entry.quantity, 2)
        self.assertContains(self.client.get(self.url("decks:deck_builder")), "ya no está disponible")
        self.post("decks:main_decrement", {"entry_id": entry.pk})
        entry.refresh_from_db()
        self.assertEqual(entry.quantity, 1)
        self.post("decks:main_remove", {"entry_id": entry.pk})
        self.assertFalse(DeckEntry.objects.filter(pk=entry.pk).exists())

    def test_entry_id_attack_cannot_modify_another_deck_entry(self):
        other_deck = self.create_deck("Other", owner=self.other_owner)
        other_entry = self.add_entry(other_deck, self.create_card("Other main"))
        self.client.force_login(self.owner)

        response = self.post("decks:main_remove", {"entry_id": other_entry.pk})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(DeckEntry.objects.filter(pk=other_entry.pk).exists())

    def test_mutation_get_does_not_modify_and_other_owner_gets_404(self):
        card = self.create_card("Main")
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.url("decks:main_add")).status_code, 404)
        self.assertFalse(DeckEntry.objects.filter(deck=self.deck).exists())
        self.client.force_login(self.other_owner)
        self.assertEqual(self.post("decks:main_add", {"card_id": card.pk}).status_code, 404)

    def test_builder_search_and_cardtype_filter_exclude_legends_and_ineligible_cards(self):
        named = self.create_card("Chrome Unit", card_type=Card.CardType.UNIT)
        program = self.create_card("Chrome Program", card_type=Card.CardType.PROGRAM)
        self.create_card("Chrome Legend", card_type=Card.CardType.LEGEND)
        self.create_card("Chrome Draft", status=Card.Status.DRAFT)
        self.client.force_login(self.owner)

        response = self.client.get(self.url("decks:deck_builder"), {"q": "Chrome", "type": "UNIT"})

        self.assertContains(response, named.name)
        self.assertNotContains(response, program.name)
        self.assertEqual(list(response.context["available_cards"]), [named])

    def test_set_filter_uses_primary_printing_without_duplicate_cards(self):
        other_set = Set.objects.create(name="Other Set")
        card = self.create_card("Set card")
        card.printings.update(set=other_set)
        self.client.force_login(self.owner)

        response = self.client.get(self.url("decks:deck_builder"), {"set": other_set.slug})

        self.assertContains(response, card.name, count=1)

    def test_detail_exposes_builder_only_to_owner(self):
        self.client.force_login(self.owner)
        self.assertContains(self.client.get(self.url("decks:deck_detail")), "Construir mazo")
        self.deck.is_public = True
        self.deck.editorial_status = "PUBLISHED"
        self.deck.save()
        self.client.force_login(self.other_owner)
        self.assertNotContains(self.client.get(self.url("decks:deck_detail")), "Construir mazo")

    def test_all_composition_endpoints_require_owner_and_csrf(self):
        legend = self.create_card("Legend", card_type=Card.CardType.LEGEND)
        entry = self.add_entry(self.deck, self.create_card("Main"))
        deck_legend = self.add_legend(self.deck, legend)
        self.client.force_login(self.other_owner)
        actions = (
            ("decks:legend_add", {"card_id": legend.pk}),
            ("decks:legend_remove", {"entry_id": deck_legend.pk}),
            ("decks:main_add", {"card_id": entry.card_id}),
            ("decks:main_decrement", {"entry_id": entry.pk}),
            ("decks:main_remove", {"entry_id": entry.pk}),
        )
        for name, payload in actions:
            with self.subTest(name=name):
                self.assertEqual(self.post(name, payload).status_code, 404)

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)
        response = csrf_client.post(self.url("decks:main_add"), {"card_id": entry.card_id})
        self.assertEqual(response.status_code, 403)
