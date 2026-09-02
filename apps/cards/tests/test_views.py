from django.test import TestCase
from django.urls import reverse

from apps.cards.models import Card, CardPrinting, Set


class CardsViewTests(TestCase):
    printing_fields = {
        "collector_number",
        "cost",
        "ram",
        "power",
        "printing_label",
        "source_name",
        "source_url",
        "verified_at",
        "verification_notes",
    }

    def create_card(
        self,
        name,
        *,
        card_set=None,
        card_type=Card.CardType.LEGEND,
        status=Card.Status.PUBLISHED,
        primary=True,
        **kwargs,
    ):
        printed = {key: kwargs.pop(key) for key in tuple(kwargs) if key in self.printing_fields}
        card = Card.objects.create(name=name, card_type=card_type, status=status, **kwargs)
        CardPrinting.objects.create(
            card=card,
            set=card_set or self.active_set,
            is_primary=primary,
            **printed,
        )
        return card

    def setUp(self):
        self.active_set = Set.objects.create(name="Active Set")
        self.other_set = Set.objects.create(name="Other Set")
        self.inactive_set = Set.objects.create(name="Inactive Set", is_active=False)

    def test_catalog_returns_ok_and_shows_empty_state(self):
        response = self.client.get(reverse("cards:catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Base táctica preparada.")

    def test_catalog_only_shows_public_cards(self):
        published = self.create_card("Published card")
        draft = self.create_card("Draft card", status=Card.Status.DRAFT)
        reviewed = self.create_card("Reviewed card", status=Card.Status.REVIEWED)
        inactive = self.create_card("Inactive set card", card_set=self.inactive_set)
        no_primary = self.create_card("No primary card", primary=False)

        response = self.client.get(reverse("cards:catalog"))

        self.assertContains(response, published.name)
        self.assertNotContains(response, draft.name)
        self.assertNotContains(response, reviewed.name)
        self.assertNotContains(response, inactive.name)
        self.assertNotContains(response, no_primary.name)

    def test_public_card_detail_is_available_and_non_public_cards_are_hidden(self):
        published = self.create_card("Published detail")
        draft = self.create_card("Draft detail", status=Card.Status.DRAFT)
        reviewed = self.create_card("Reviewed detail", status=Card.Status.REVIEWED)
        inactive = self.create_card("Inactive detail", card_set=self.inactive_set)

        self.assertEqual(self.client.get(reverse("cards:detail", args=[published.slug])).status_code, 200)
        self.assertEqual(self.client.get(reverse("cards:detail", args=[draft.slug])).status_code, 404)
        self.assertEqual(self.client.get(reverse("cards:detail", args=[reviewed.slug])).status_code, 404)
        self.assertEqual(self.client.get(reverse("cards:detail", args=[inactive.slug])).status_code, 404)
        self.assertEqual(self.client.get(reverse("cards:detail", args=["missing-card"])).status_code, 404)

    def test_search_finds_name_and_primary_collector_number_without_leaking_private_cards(self):
        named = self.create_card("Chrome Runner", collector_number="C-001")
        numbered = self.create_card("Silent Card", collector_number="R-404")
        draft = self.create_card("Draft Chrome", status=Card.Status.DRAFT, collector_number="D-001")
        reviewed = self.create_card("Reviewed Chrome", status=Card.Status.REVIEWED)
        inactive = self.create_card("Inactive Chrome", card_set=self.inactive_set)

        name_response = self.client.get(reverse("cards:catalog"), {"q": "chrome"})
        number_response = self.client.get(reverse("cards:catalog"), {"q": "R-404"})
        empty_response = self.client.get(reverse("cards:catalog"), {"q": "not-found"})

        self.assertContains(name_response, named.name)
        self.assertNotContains(name_response, draft.name)
        self.assertNotContains(name_response, reviewed.name)
        self.assertNotContains(name_response, inactive.name)
        self.assertContains(number_response, numbered.name)
        self.assertContains(empty_response, "Base táctica preparada.")

    def test_search_finds_a_secondary_printing_but_catalog_renders_primary_data(self):
        card = self.create_card("Multi-print card", collector_number="P-001", cost=1)
        CardPrinting.objects.create(
            card=card,
            set=self.other_set,
            collector_number="S-999",
            cost=9,
            is_primary=False,
        )

        response = self.client.get(reverse("cards:catalog"), {"q": "S-999"})

        self.assertContains(response, card.name)
        self.assertContains(response, "#P-001")
        self.assertNotContains(response, "#S-999")

    def test_catalog_filters_by_printing_set_and_card_type(self):
        target = self.create_card("Legend target", card_type=Card.CardType.LEGEND)
        other_set_card = self.create_card(
            "Other set target", card_set=self.other_set, card_type=Card.CardType.LEGEND
        )
        other_type = self.create_card("Unit target", card_type=Card.CardType.UNIT)

        set_response = self.client.get(reverse("cards:catalog"), {"set": self.active_set.slug})
        type_response = self.client.get(reverse("cards:catalog"), {"type": Card.CardType.LEGEND})
        combined_response = self.client.get(
            reverse("cards:catalog"),
            {"q": "target", "set": self.active_set.slug, "type": Card.CardType.LEGEND},
        )

        self.assertContains(set_response, target.name)
        self.assertNotContains(set_response, other_set_card.name)
        self.assertContains(type_response, target.name)
        self.assertNotContains(type_response, other_type.name)
        self.assertContains(combined_response, target.name)
        self.assertNotContains(combined_response, other_set_card.name)
        self.assertNotContains(combined_response, other_type.name)

    def test_catalog_supports_every_card_type_and_invalid_types_are_safe(self):
        cards = {card_type: self.create_card(f"{card_type} card", card_type=card_type) for card_type in Card.CardType.values}

        for card_type, card in cards.items():
            with self.subTest(card_type=card_type):
                response = self.client.get(reverse("cards:catalog"), {"type": card_type})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, card.name)
        self.assertEqual(self.client.get(reverse("cards:catalog"), {"type": "INVALID"}).status_code, 200)

    def test_set_filter_does_not_reveal_inactive_set_cards(self):
        hidden = self.create_card("Inactive filtered card", card_set=self.inactive_set)

        response = self.client.get(reverse("cards:catalog"), {"set": self.inactive_set.slug})

        self.assertNotContains(response, hidden.name)

    def test_catalog_paginates_logical_cards_at_twenty_four_per_page_and_preserves_filters(self):
        for index in range(25):
            self.create_card(f"Catalog card {index:02}", collector_number=f"C-{index:02}")

        first_page = self.client.get(reverse("cards:catalog"), {"q": "Catalog", "type": "LEGEND"})
        second_page = self.client.get(
            reverse("cards:catalog"), {"q": "Catalog", "type": "LEGEND", "page": 2}
        )

        self.assertEqual(first_page.context["page_obj"].paginator.per_page, 24)
        self.assertEqual(first_page.context["page_obj"].paginator.num_pages, 2)
        self.assertContains(second_page, "Catalog card 24")
        self.assertContains(first_page, "q=Catalog&amp;set=&amp;type=LEGEND&amp;page=2")

    def test_catalog_renders_primary_tactical_attributes_and_detail_link(self):
        card = self.create_card(
            "Tactical unit",
            card_type=Card.CardType.UNIT,
            collector_number="078",
            cost=3,
            ram=2,
            power=2,
        )

        response = self.client.get(reverse("cards:catalog"))

        self.assertContains(response, "UNIT")
        self.assertContains(response, card.name)
        self.assertContains(response, self.active_set.name)
        self.assertContains(response, "#078")
        self.assertContains(response, "COST")
        self.assertContains(response, "RAM")
        self.assertContains(response, "POWER")
        self.assertContains(response, reverse("cards:detail", args=[card.slug]))

    def test_catalog_omits_empty_primary_attributes(self):
        self.create_card("Minimal legend", collector_number="", cost=None, ram=None, power=None)

        response = self.client.get(reverse("cards:catalog"))

        self.assertNotContains(response, "COLLECTOR</dt><dd>#")
        self.assertNotContains(response, "COST</dt><dd>")
        self.assertNotContains(response, "RAM</dt><dd>")
        self.assertNotContains(response, "POWER</dt><dd>")

    def test_catalog_prefetches_primary_printings_without_per_card_queries(self):
        for index in range(3):
            self.create_card(f"Prefetched card {index}", collector_number=f"P-{index}")

        with self.assertNumQueries(4):
            response = self.client.get(reverse("cards:catalog"))

        self.assertEqual(response.status_code, 200)

    def test_detail_renders_primary_tactical_data_and_safe_printing_source_link(self):
        card = self.create_card(
            "Verified program",
            card_type=Card.CardType.PROGRAM,
            collector_number="103",
            cost=2,
            ram=2,
            power=None,
            source_name="Official Database",
            source_url="https://example.com/card/verified-program",
            rules_text="",
        )

        response = self.client.get(reverse("cards:detail", args=[card.slug]))

        self.assertContains(response, "CHOOMDEX // CARD FILE")
        self.assertContains(response, "PROGRAM")
        self.assertContains(response, "#103")
        self.assertContains(response, "COST")
        self.assertContains(response, "RAM")
        self.assertNotContains(response, "POWER</dt><dd>")
        self.assertNotContains(response, "Rules text")
        self.assertContains(
            response,
            'href="https://example.com/card/verified-program" target="_blank" rel="noopener noreferrer"',
        )
