from django.contrib import admin
from django.test import TestCase

from apps.cards.models import Card, Set


class CardsAdminTests(TestCase):
    def test_set_and_card_are_registered_in_admin(self):
        self.assertIn(Set, admin.site._registry)
        self.assertIn(Card, admin.site._registry)
