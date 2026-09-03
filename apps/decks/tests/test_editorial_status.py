from django.test import TestCase
from django.urls import reverse

from apps.videos.models import Video

from .helpers import DeckTestMixin


class DeckEditorialStatusTests(DeckTestMixin, TestCase):
    def urls(self, deck):
        return {
            "detail": deck.get_absolute_url(),
            "update": reverse("decks:deck_update", args=[deck.owner.username, deck.slug]),
        }

    def test_default_is_safe_draft_and_preserves_editorial_profile_and_composition(self):
        deck = self.create_deck("Pilot draft")
        card = self.create_card("Pilot main")
        self.add_entry(deck, card, 2)

        self.assertEqual(deck.editorial_status, "DRAFT")
        self.assertEqual(deck.editorial_profile.deck, deck)
        self.assertEqual(deck.entries.get().quantity, 2)

    def test_public_library_and_detail_apply_editorial_status_matrix(self):
        published = self.create_deck("Published", is_public=True)
        published_private = self.create_deck("Published private", is_public=False, editorial_status="PUBLISHED")
        draft_public = self.create_deck("Draft public", is_public=True, editorial_status="DRAFT")
        archived_public = self.create_deck("Archived public", is_public=True, editorial_status="ARCHIVED")
        archived_private = self.create_deck("Archived private", is_public=False, editorial_status="ARCHIVED")

        library = self.client.get(reverse("decks:public_decks"))
        self.assertContains(library, published.name)
        self.assertContains(library, archived_public.name)
        self.assertContains(library, "Archivo histórico")
        for deck in (published_private, draft_public, archived_private):
            self.assertNotContains(library, deck.name)
            self.assertEqual(self.client.get(deck.get_absolute_url()).status_code, 404)
        archived_response = self.client.get(archived_public.get_absolute_url())
        self.assertContains(archived_response, "Archivo táctico")
        self.assertContains(archived_response, 'name="robots" content="noindex, nofollow"')

    def test_owner_can_transition_status_but_another_user_cannot(self):
        deck = self.create_deck("Workflow")
        self.client.force_login(self.owner)
        response = self.client.post(self.urls(deck)["update"], {"name": deck.name, "description": "", "is_public": "on", "editorial_status": "PUBLISHED"})
        deck.refresh_from_db()
        self.assertRedirects(response, self.urls(deck)["detail"])
        self.assertEqual(deck.editorial_status, "PUBLISHED")
        self.client.force_login(self.other_owner)
        self.assertEqual(self.client.post(self.urls(deck)["update"], {"name": "Hijacked", "editorial_status": "ARCHIVED"}).status_code, 404)

    def test_video_relation_excludes_drafts_but_keeps_public_archive_context(self):
        published = self.create_deck("Current", is_public=True)
        archived = self.create_deck("Historic", is_public=True, editorial_status="ARCHIVED")
        draft = self.create_deck("Unreleased", is_public=True, editorial_status="DRAFT")
        private = self.create_deck("Private", is_public=False, editorial_status="PUBLISHED")
        video = Video.objects.create(title="Editorial video", youtube_url="https://www.youtube.com/watch?v=editorial", youtube_video_id="editorial", summary="Resumen")
        video.related_decks.add(published, archived, draft, private)

        response = self.client.get(video.get_absolute_url())
        self.assertContains(response, published.name)
        self.assertContains(response, archived.name)
        self.assertContains(response, "Archivo histórico")
        self.assertNotContains(response, draft.name)
        self.assertNotContains(response, private.name)
