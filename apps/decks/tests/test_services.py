from django.test import TestCase

from apps.cards.models import Card, CardPrinting
from apps.decks.services import DeckValidationService, RAM_NOT_EVALUATED, is_card_eligible

from .helpers import DeckTestMixin


class DeckValidationServiceTests(DeckTestMixin, TestCase):
    def test_draft_with_zero_one_or_two_legends_is_invalid_but_persistible(self):
        deck = self.create_deck()
        for count in range(3):
            with self.subTest(count=count):
                result = DeckValidationService(deck).validate()
                self.assertFalse(result.valid)
                if count < 2:
                    self.add_legend(deck, self.create_card(f"Legend {count}", card_type=Card.CardType.LEGEND))

    def test_three_legends_and_main_of_forty_are_structurally_valid(self):
        deck = self.make_structurally_valid_deck()

        result = DeckValidationService(deck).validate()

        self.assertTrue(result.valid)
        self.assertEqual(result.summary["legend_count"], 3)
        self.assertEqual(result.summary["main_count"], 40)
        self.assertEqual(result.summary["ram_status"], RAM_NOT_EVALUATED)

    def test_four_legends_is_invalid(self):
        deck = self.make_structurally_valid_deck()
        self.add_legend(deck, self.create_card("Fourth legend", card_type=Card.CardType.LEGEND))

        self.assertFalse(DeckValidationService(deck).validate().valid)

    def test_main_count_boundaries_use_sum_of_quantities(self):
        deck = self.make_structurally_valid_deck()
        entry = deck.entries.first()
        entry.quantity = 2
        entry.save()
        self.assertFalse(DeckValidationService(deck).validate().valid)

        entry.quantity = 3
        entry.save()
        extra = self.create_card("Extra main")
        self.add_entry(deck, extra, 3)
        self.add_entry(deck, self.create_card("Extra two"), 3)
        self.add_entry(deck, self.create_card("Extra three"), 3)
        self.add_entry(deck, self.create_card("Extra four"), 1)
        self.assertEqual(DeckValidationService(deck).validate().summary["main_count"], 50)
        self.assertTrue(DeckValidationService(deck).validate().valid)
        self.add_entry(deck, self.create_card("Too many"), 1)
        self.assertFalse(DeckValidationService(deck).validate().valid)

    def test_ram_is_explicitly_not_evaluated(self):
        result = DeckValidationService(self.make_structurally_valid_deck()).validate()

        self.assertEqual(result.summary["ram_status"], "NOT_EVALUATED")
        self.assertNotIn("ram_valid", result.summary)

    def test_eligibility_requires_published_card_primary_printing_and_active_set(self):
        published = self.create_card("Published")
        draft = self.create_card("Draft", status=Card.Status.DRAFT)
        reviewed = self.create_card("Reviewed", status=Card.Status.REVIEWED)
        no_primary = self.create_card("No primary")
        no_primary.printings.update(is_primary=False)
        inactive = self.create_card("Inactive set")
        inactive_set = self.card_set.__class__.objects.create(name="Inactive deck test set", is_active=False)
        inactive.printings.update(set=inactive_set)

        self.assertTrue(is_card_eligible(published))
        self.assertFalse(is_card_eligible(draft))
        self.assertFalse(is_card_eligible(reviewed))
        self.assertFalse(is_card_eligible(no_primary))
        self.assertFalse(is_card_eligible(inactive))

    def test_historical_unpublished_card_is_warning_not_structural_error(self):
        deck = self.make_structurally_valid_deck()
        historical_card = deck.entries.first().card
        Card.objects.filter(pk=historical_card.pk).update(status=Card.Status.DRAFT)

        result = DeckValidationService(deck).validate()

        self.assertTrue(result.valid)
        self.assertTrue(result.warnings)

    def test_validation_loads_composition_without_per_entry_queries(self):
        deck = self.make_structurally_valid_deck()

        with self.assertNumQueries(3):
            result = DeckValidationService(deck).validate()

        self.assertTrue(result.valid)
