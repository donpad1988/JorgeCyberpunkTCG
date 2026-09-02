from django.contrib import admin
from django.test import TestCase

from apps.decks.admin import DeckEntryInline, DeckLegendInline
from apps.decks.models import Deck, DeckEntry, DeckLegend


class DeckAdminTests(TestCase):
    def test_deck_models_are_registered_and_deck_uses_inlines(self):
        self.assertIn(Deck, admin.site._registry)
        self.assertIn(DeckLegend, admin.site._registry)
        self.assertIn(DeckEntry, admin.site._registry)
        self.assertIn(DeckLegendInline, admin.site._registry[Deck].inlines)
        self.assertIn(DeckEntryInline, admin.site._registry[Deck].inlines)
