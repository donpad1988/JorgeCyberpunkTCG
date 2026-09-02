from django.contrib.auth import get_user_model

from apps.cards.models import Card, CardPrinting, Set
from apps.decks.models import Deck, DeckEntry, DeckLegend


class DeckTestMixin:
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="owner", password="safe-pass")
        self.other_owner = get_user_model().objects.create_user(username="other", password="safe-pass")
        self.card_set = Set.objects.create(name="Deck Test Set")

    def create_deck(self, name="My deck", owner=None, **kwargs):
        return Deck.objects.create(owner=owner or self.owner, name=name, **kwargs)

    def create_card(self, name, *, card_type=Card.CardType.UNIT, status=Card.Status.PUBLISHED):
        card = Card.objects.create(name=name, card_type=card_type, status=status)
        CardPrinting.objects.create(card=card, set=self.card_set, is_primary=True)
        return card

    def add_legend(self, deck, card):
        return DeckLegend.objects.create(deck=deck, card=card)

    def add_entry(self, deck, card, quantity=1):
        return DeckEntry.objects.create(deck=deck, card=card, quantity=quantity)

    def make_structurally_valid_deck(self):
        deck = self.create_deck("Valid deck")
        for index in range(3):
            self.add_legend(deck, self.create_card(f"Legend {index}", card_type=Card.CardType.LEGEND))
        for index in range(14):
            self.add_entry(deck, self.create_card(f"Main card {index}"), 3 if index < 12 else 2)
        return deck
