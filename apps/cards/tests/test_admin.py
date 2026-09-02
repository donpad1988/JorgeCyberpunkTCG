from django.contrib import admin
from django.test import TestCase

from apps.cards.admin import CardPrintingInline
from apps.cards.models import Card, CardPrinting, Set


class CardsAdminTests(TestCase):
    def test_set_card_and_card_printing_are_registered_in_admin(self):
        self.assertIn(Set, admin.site._registry)
        self.assertIn(Card, admin.site._registry)
        self.assertIn(CardPrinting, admin.site._registry)

    def test_card_admin_edits_printings_inline(self):
        card_admin = admin.site._registry[Card]

        self.assertIn(CardPrintingInline, card_admin.inlines)
