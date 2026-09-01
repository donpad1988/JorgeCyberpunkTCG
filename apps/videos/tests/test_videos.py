from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.content.models import Article, ContentCategory
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
