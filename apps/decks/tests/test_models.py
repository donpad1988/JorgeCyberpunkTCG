from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from apps.cards.models import Card
from apps.decks.models import Deck, DeckEntry, DeckLegend

from .helpers import DeckTestMixin


class DeckModelTests(DeckTestMixin, TestCase):
    def test_deck_owner_privacy_and_slug(self):
        deck = self.create_deck("Mi primer mazo")

        self.assertEqual(deck.owner, self.owner)
        self.assertFalse(deck.is_public)
        self.assertEqual(deck.slug, "mi-primer-mazo")

    def test_slug_is_unique_per_owner_but_reusable_by_another_owner(self):
        self.create_deck("Mazo", slug="compartido")
        other = self.create_deck("Mazo", owner=self.other_owner, slug="compartido")

        self.assertEqual(other.slug, "compartido")
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Deck.objects.create(owner=self.owner, name="Otro", slug="compartido")

    def test_owner_and_deck_deletion_cascade_to_composition(self):
        deck = self.create_deck()
        legend = self.create_card("Legend", card_type=Card.CardType.LEGEND)
        main = self.create_card("Main")
        deck_legend = self.add_legend(deck, legend)
        entry = self.add_entry(deck, main)

        deck.delete()

        self.assertFalse(DeckLegend.objects.filter(pk=deck_legend.pk).exists())
        self.assertFalse(DeckEntry.objects.filter(pk=entry.pk).exists())

    def test_deck_has_no_persisted_validation_fields(self):
        deck = self.create_deck()
        self.assertEqual(str(deck), "My deck")
        for field_name in ("is_valid", "validation_status", "ram_valid"):
            with self.assertRaises(FieldDoesNotExist):
                Deck._meta.get_field(field_name)

    def test_deck_legend_requires_a_legend_card_and_is_unique_per_deck(self):
        deck = self.create_deck()
        legend = self.create_card("Legend", card_type=Card.CardType.LEGEND)
        non_legend = self.create_card("Unit")
        self.add_legend(deck, legend)

        with self.assertRaises(ValidationError):
            self.add_legend(deck, non_legend)
        with self.assertRaises(ValidationError):
            self.add_legend(deck, legend)

    def test_same_legend_can_be_used_by_a_different_deck(self):
        legend = self.create_card("Shared legend", card_type=Card.CardType.LEGEND)
        self.add_legend(self.create_deck(), legend)
        self.add_legend(self.create_deck("Other deck", owner=self.other_owner), legend)

        self.assertEqual(DeckLegend.objects.filter(card=legend).count(), 2)

    def test_deck_entry_rejects_legends_and_invalid_quantities(self):
        deck = self.create_deck()
        legend = self.create_card("Legend", card_type=Card.CardType.LEGEND)
        card = self.create_card("Unit")

        with self.assertRaises(ValidationError):
            self.add_entry(deck, legend)
        for quantity in (0, -1, 4):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValidationError):
                    self.add_entry(deck, card, quantity)

    def test_deck_entry_accepts_one_to_three_and_is_unique_per_deck(self):
        deck = self.create_deck()
        for quantity in (1, 2, 3):
            card = self.create_card(f"Unit {quantity}")
            self.assertEqual(self.add_entry(deck, card, quantity).quantity, quantity)
        card = self.create_card("Duplicate")
        self.add_entry(deck, card)

        with self.assertRaises(ValidationError):
            self.add_entry(deck, card)

    def test_card_references_are_protected(self):
        deck = self.create_deck()
        legend = self.create_card("Legend protected", card_type=Card.CardType.LEGEND)
        main = self.create_card("Main protected")
        self.add_legend(deck, legend)
        self.add_entry(deck, main)

        with self.assertRaises(ProtectedError):
            legend.delete()
        with self.assertRaises(ProtectedError):
            main.delete()
