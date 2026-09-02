from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from apps.cards.models import Card, CardPrinting, Set


class CardModelsTests(TestCase):
    def create_card(self, name, *, card_type=Card.CardType.LEGEND, status=Card.Status.PUBLISHED):
        return Card.objects.create(name=name, card_type=card_type, status=status)

    def create_printing(self, card, card_set, *, primary=True, **kwargs):
        return CardPrinting.objects.create(card=card, set=card_set, is_primary=primary, **kwargs)

    def test_strings_and_slugs_are_generated_once(self):
        card_set = Set.objects.create(name="Core Set")
        card = self.create_card("Neon Legend")
        printing = self.create_printing(card, card_set, collector_number="001")

        self.assertEqual(str(card_set), "Core Set")
        self.assertEqual(str(card), "Neon Legend")
        self.assertEqual(str(printing), "Neon Legend — Core Set #001")
        self.assertEqual(card_set.slug, "core-set")
        self.assertEqual(card.slug, "neon-legend")

        card_set.name = "Renamed Set"
        card.name = "Renamed Card"
        card_set.save()
        card.save()
        self.assertEqual(card_set.slug, "core-set")
        self.assertEqual(card.slug, "neon-legend")

    def test_slugs_are_unique_for_sets_and_cards(self):
        card_set = Set.objects.create(name="Unique Set")
        self.create_card("Unique Card", card_type=Card.CardType.GEAR)

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Set.objects.create(name="Another set", slug=card_set.slug)
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Card.objects.create(
                    name="Another card", slug="unique-card", card_type=Card.CardType.GEAR
                )

    def test_card_type_and_status_choices_include_the_mvp_values(self):
        self.assertEqual(set(Card.CardType.values), {"LEGEND", "UNIT", "PROGRAM", "GEAR"})
        self.assertEqual(set(Card.Status.values), {"DRAFT", "REVIEWED", "PUBLISHED"})

    def test_printing_links_card_and_set_and_protects_its_set(self):
        card_set = Set.objects.create(name="Protected Set")
        card = self.create_card("Protected Card", card_type=Card.CardType.UNIT)
        printing = self.create_printing(card, card_set)

        self.assertEqual(list(card.printings.all()), [printing])
        self.assertEqual(list(card_set.printings.all()), [printing])
        with self.assertRaises(ProtectedError):
            card_set.delete()

    def test_card_deletion_cascades_to_its_printings(self):
        card_set = Set.objects.create(name="Cascade Set")
        card = self.create_card("Cascade Card")
        printing = self.create_printing(card, card_set)

        card.delete()

        self.assertFalse(CardPrinting.objects.filter(pk=printing.pk).exists())

    def test_public_queryset_requires_published_card_active_set_and_primary_printing(self):
        active_set = Set.objects.create(name="Active Set")
        inactive_set = Set.objects.create(name="Inactive Set", is_active=False)
        published = self.create_card("Published")
        draft = self.create_card("Draft", status=Card.Status.DRAFT)
        reviewed = self.create_card("Reviewed", status=Card.Status.REVIEWED)
        inactive = self.create_card("Inactive")
        no_primary = self.create_card("No primary")
        self.create_printing(published, active_set)
        self.create_printing(draft, active_set)
        self.create_printing(reviewed, active_set)
        self.create_printing(inactive, inactive_set)
        self.create_printing(no_primary, active_set, primary=False)

        self.assertEqual(list(Card.objects.public()), [published])

    def test_only_one_primary_printing_is_allowed_per_card(self):
        card_set = Set.objects.create(name="Primary Set")
        card = self.create_card("Primary Card")
        self.create_printing(card, card_set, collector_number="001")

        with self.assertRaises(ValidationError):
            self.create_printing(card, card_set, collector_number="002")

    def test_same_collector_number_is_allowed_for_different_cards(self):
        card_set = Set.objects.create(name="Shared Number Set")
        first = self.create_card("First")
        second = self.create_card("Second")
        self.create_printing(first, card_set, collector_number="001")
        self.create_printing(second, card_set, collector_number="001")

        self.assertEqual(CardPrinting.objects.filter(collector_number="001").count(), 2)

    def test_printing_keeps_its_own_provenance(self):
        card_set = Set.objects.create(name="Provenance Set")
        card = self.create_card("Provenance Card")
        printing = self.create_printing(
            card,
            card_set,
            source_name="Official Database",
            source_url="https://example.com/card/provenance",
            verification_notes="Manual verification",
        )

        self.assertEqual(printing.source_name, "Official Database")
        self.assertEqual(printing.source_url, "https://example.com/card/provenance")
        self.assertEqual(printing.verification_notes, "Manual verification")
