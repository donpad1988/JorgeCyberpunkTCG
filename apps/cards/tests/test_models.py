from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from apps.cards.models import Card, Set


class CardModelsTests(TestCase):
    def test_strings_and_slugs_are_generated_once(self):
        card_set = Set.objects.create(name="Core Set")
        card = Card.objects.create(
            name="Neon Legend",
            set=card_set,
            card_type=Card.CardType.LEGEND,
        )

        self.assertEqual(str(card_set), "Core Set")
        self.assertEqual(str(card), "Neon Legend")
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
        Card.objects.create(name="Unique Card", set=card_set, card_type=Card.CardType.GEAR)

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Set.objects.create(name="Another set", slug=card_set.slug)
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Card.objects.create(
                    name="Another card",
                    slug="unique-card",
                    set=card_set,
                    card_type=Card.CardType.GEAR,
                )

    def test_card_type_and_status_choices_include_the_mvp_values(self):
        self.assertEqual(
            set(Card.CardType.values),
            {"LEGEND", "UNIT", "PROGRAM", "GEAR"},
        )
        self.assertEqual(
            set(Card.Status.values),
            {"DRAFT", "REVIEWED", "PUBLISHED"},
        )

    def test_card_belongs_to_set_and_protects_its_set(self):
        card_set = Set.objects.create(name="Protected Set")
        card = Card.objects.create(name="Protected Card", set=card_set, card_type=Card.CardType.UNIT)

        self.assertEqual(card.set, card_set)
        self.assertEqual(list(card_set.cards.all()), [card])
        with self.assertRaises(ProtectedError):
            card_set.delete()

    def test_public_queryset_only_returns_published_cards_in_active_sets(self):
        active_set = Set.objects.create(name="Active Set")
        inactive_set = Set.objects.create(name="Inactive Set", is_active=False)
        published = Card.objects.create(
            name="Published", set=active_set, card_type=Card.CardType.LEGEND, status=Card.Status.PUBLISHED
        )
        draft = Card.objects.create(
            name="Draft", set=active_set, card_type=Card.CardType.UNIT, status=Card.Status.DRAFT
        )
        reviewed = Card.objects.create(
            name="Reviewed", set=active_set, card_type=Card.CardType.PROGRAM, status=Card.Status.REVIEWED
        )
        inactive = Card.objects.create(
            name="Inactive", set=inactive_set, card_type=Card.CardType.GEAR, status=Card.Status.PUBLISHED
        )

        self.assertEqual(list(Card.objects.public()), [published])
        self.assertNotIn(draft, Card.objects.public())
        self.assertNotIn(reviewed, Card.objects.public())
        self.assertNotIn(inactive, Card.objects.public())
