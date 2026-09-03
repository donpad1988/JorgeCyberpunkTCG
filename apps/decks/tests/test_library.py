from django.test import TestCase
from django.urls import reverse

from apps.cards.models import Card
from apps.videos.models import Video

from .helpers import DeckTestMixin


class TacticalDeckLibraryTests(DeckTestMixin, TestCase):
    def create_public_deck(self, name, *, status="PUBLISHED", archetype="", summary=""):
        deck = self.create_deck(name, is_public=True, editorial_status=status)
        deck.editorial_profile.archetype = archetype
        deck.editorial_profile.short_summary = summary
        deck.editorial_profile.save()
        return deck

    def test_empty_library_is_intentional_and_hides_the_pilot_draft(self):
        pilot = self.create_deck("Mazo Privado Prueba")

        response = self.client.get(reverse("decks:public_decks"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ARCHIVO TÁCTICO EN PREPARACIÓN")
        self.assertContains(response, reverse("content:guide_list"))
        self.assertContains(response, reverse("videos:list"))
        self.assertNotContains(response, pilot.name)

    def test_library_searches_published_metadata_and_keeps_drafts_and_private_hidden(self):
        by_name = self.create_public_deck("Control nocturno")
        by_archetype = self.create_public_deck("Sin nombre", archetype="Tempo táctico")
        by_summary = self.create_public_deck("Resumen", summary="Plan de infiltración.")
        draft = self.create_public_deck("Draft visible por error", status="DRAFT", summary="infiltración")
        private = self.create_deck("Private infiltration", editorial_status="PUBLISHED")

        self.assertContains(self.client.get(reverse("decks:public_decks"), {"q": "control"}), by_name.name)
        self.assertContains(self.client.get(reverse("decks:public_decks"), {"q": "tempo"}), by_archetype.name)
        response = self.client.get(reverse("decks:public_decks"), {"q": "infiltración"})
        self.assertContains(response, by_summary.name)
        self.assertNotContains(response, draft.name)
        self.assertNotContains(response, private.name)
        no_results = self.client.get(reverse("decks:public_decks"), {"q": "no-existe"})
        self.assertContains(no_results, "No encontramos mazos para esta búsqueda.")
        self.assertContains(no_results, reverse("decks:public_decks"))

    def test_card_shows_real_composition_counts_active_video_and_detail_navigation(self):
        deck = self.create_public_deck("Composición real")
        legends = [self.create_card(f"Legend {index}", card_type=Card.CardType.LEGEND) for index in range(3)]
        for legend in legends:
            self.add_legend(deck, legend)
        for index, quantity in enumerate((3, 2, 1)):
            self.add_entry(deck, self.create_card(f"Main {index}"), quantity)
        active = Video.objects.create(title="Video activo", youtube_url="https://www.youtube.com/watch?v=active", youtube_video_id="active", summary="Resumen")
        inactive = Video.objects.create(title="Video inactivo", youtube_url="https://www.youtube.com/watch?v=inactive", youtube_video_id="inactive", summary="Resumen", is_active=False)
        active.related_decks.add(deck)
        inactive.related_decks.add(deck)

        library = self.client.get(reverse("decks:public_decks"))
        self.assertContains(library, "Legends</dt><dd>3")
        self.assertContains(library, "MAIN</dt><dd>6")
        self.assertContains(library, "Video disponible")
        detail = self.client.get(deck.get_absolute_url())
        self.assertContains(detail, reverse("decks:public_decks"))
        self.assertContains(detail, reverse("cards:detail", args=[legends[0].slug]))
        self.assertContains(detail, active.get_absolute_url())
        self.assertNotContains(library, inactive.title)

    def test_archived_public_deck_is_secondary_and_anonymous_can_open_it(self):
        current = self.create_public_deck("Actual")
        archived = self.create_public_deck("Histórico", status="ARCHIVED")
        private_archive = self.create_deck("Archivo privado", editorial_status="ARCHIVED")

        library = self.client.get(reverse("decks:public_decks"))
        self.assertContains(library, current.name)
        self.assertContains(library, "Archivo histórico")
        self.assertContains(library, archived.name)
        self.assertNotContains(library, private_archive.name)
        self.assertEqual(self.client.get(archived.get_absolute_url()).status_code, 200)
        self.assertContains(self.client.get(archived.get_absolute_url()), "Archivo táctico")

    def test_search_is_hidden_when_library_has_no_published_public_decks(self):
        response = self.client.get(reverse("decks:public_decks"))

        self.assertNotContains(response, 'id="deck-library-search"')
        self.assertContains(response, "ARCHIVO TÁCTICO EN PREPARACIÓN")

    def test_draft_public_does_not_enable_search(self):
        self.create_public_deck("Draft", status="DRAFT")

        response = self.client.get(reverse("decks:public_decks"))

        self.assertNotContains(response, 'id="deck-library-search"')

    def test_private_published_does_not_enable_search(self):
        self.create_deck("Private", editorial_status="PUBLISHED")

        response = self.client.get(reverse("decks:public_decks"))

        self.assertNotContains(response, 'id="deck-library-search"')

    def test_archived_public_does_not_enable_search(self):
        self.create_public_deck("Archived", status="ARCHIVED")

        response = self.client.get(reverse("decks:public_decks"))

        self.assertNotContains(response, 'id="deck-library-search"')
        self.assertContains(response, "Archivo histórico")

    def test_published_public_enables_search_and_no_results_keeps_one_clear_action(self):
        deck = self.create_public_deck("Searchable")

        response = self.client.get(reverse("decks:public_decks"), {"q": "missing"})

        self.assertContains(response, 'id="deck-library-search"')
        self.assertContains(response, 'for="deck-search"')
        self.assertContains(response, "BÚSQUEDA SIN RESULTADOS")
        self.assertContains(response, "Limpiar búsqueda", count=1)
        self.assertNotContains(response, deck.name)
