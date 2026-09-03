from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.content.models import Article, ContentCategory
from apps.decks.models import Deck
from apps.videos.models import Video

class VideoTests(TestCase):
    def setUp(self):
        user=get_user_model().objects.create_user(username="video-editor",password="test-password-2026")
        category=ContentCategory.objects.create(name="Temporal",slug="temporal")
        self.article=Article.objects.create(title="Artículo publicado",article_type="GUIDE",category=category,author=user,summary="Resumen",body="Cuerpo",status="PUBLISHED",published_at=timezone.now())
        self.video=Video.objects.create(title="Video temporal",youtube_url="https://www.youtube.com/watch?v=test-id",youtube_video_id="test-id",summary="Resumen de video",published_at=timezone.now())

    def test_active_video_is_public_and_uses_safe_id_embed(self):
        self.video.related_articles.add(self.article)
        response=self.client.get(reverse("videos:detail",args=[self.video.slug]))
        self.assertContains(response,"youtube-nocookie.com/embed/test-id")
        self.assertContains(response,self.article.title)
        self.assertContains(self.client.get(reverse("videos:list")),self.video.title)
        self.assertEqual(self.video.slug,"video-temporal")

    def test_inactive_video_is_hidden_and_empty_catalog_is_supported(self):
        self.video.is_active=False; self.video.save()
        self.assertEqual(self.client.get(reverse("videos:detail",args=[self.video.slug])).status_code,404)
        self.assertContains(self.client.get(reverse("videos:list")),"Transmisiones pendientes")

    def create_deck(self,name,*,is_public=True):
        deck=Deck.objects.create(owner=self.article.author,name=name,is_public=is_public,editorial_status="PUBLISHED" if is_public else "DRAFT")
        deck.editorial_profile.archetype="Control"
        deck.editorial_profile.short_summary=f"Resumen de {name}."
        deck.editorial_profile.save()
        return deck

    def test_optional_many_to_many_allows_multiple_videos_and_decks_without_deletion(self):
        first=self.create_deck("Primer mazo")
        second=self.create_deck("Segundo mazo")
        follow_up=Video.objects.create(title="Actualización",youtube_url="https://www.youtube.com/watch?v=follow-up",youtube_video_id="follow-up",summary="Actualización editorial")

        self.video.related_decks.add(first,second)
        follow_up.related_decks.add(first)
        self.assertEqual(self.video.related_decks.count(),2)
        self.assertEqual(first.related_videos.count(),2)
        self.video.related_decks.remove(second)
        self.assertTrue(Deck.objects.filter(pk=second.pk).exists())
        self.assertTrue(Video.objects.filter(pk=self.video.pk).exists())

    def test_video_detail_never_exposes_a_private_related_deck(self):
        public=self.create_deck("Mazo público")
        private=self.create_deck("Mazo privado",is_public=False)
        self.video.related_decks.add(public,private)

        response=self.client.get(self.video.get_absolute_url())

        self.assertContains(response,public.name)
        self.assertContains(response,public.get_absolute_url())
        self.assertNotContains(response,private.name)
        self.assertNotContains(response,private.get_absolute_url())
        self.assertNotContains(response,private.editorial_profile.short_summary)

    def test_public_deck_detail_shows_only_active_related_videos(self):
        deck=self.create_deck("Mazo conectado")
        inactive=Video.objects.create(title="Video inactivo",youtube_url="https://www.youtube.com/watch?v=inactive",youtube_video_id="inactive",summary="No visible",is_active=False)
        self.video.related_decks.add(deck)
        inactive.related_decks.add(deck)

        response=self.client.get(deck.get_absolute_url())

        self.assertContains(response,"Transmisión relacionada")
        self.assertContains(response,self.video.title)
        self.assertContains(response,self.video.get_absolute_url())
        self.assertNotContains(response,inactive.title)
        self.assertNotContains(response,inactive.get_absolute_url())

    def test_details_without_public_relationships_keep_sections_absent_and_urls_canonical(self):
        deck=self.create_deck("Sin video")

        self.assertEqual(deck.get_absolute_url(),reverse("decks:deck_detail",args=[deck.owner.username,deck.slug]))
        self.assertEqual(self.video.get_absolute_url(),reverse("videos:detail",args=[self.video.slug]))
        self.assertNotContains(self.client.get(deck.get_absolute_url()),"Transmisión relacionada")
        self.assertNotContains(self.client.get(self.video.get_absolute_url()),"MAZOS RELACIONADOS")
