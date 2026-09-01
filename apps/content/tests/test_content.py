from datetime import timedelta

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.content.models import Article, ContentCategory


class EditorialContentTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(username="editor", password="Secure-pass-2026!")
        self.category = ContentCategory.objects.create(name="Pruebas editoriales", slug="pruebas-editoriales")

    def article(self, title, article_type=Article.ArticleType.GUIDE, status=Article.Status.PUBLISHED, published_at=None, **kwargs):
        values = {"title": title, "article_type": article_type, "category": self.category, "author": self.author, "summary": "Resumen editorial de prueba.", "body": "Contenido temporal para pruebas.", "status": status, "published_at": published_at if published_at is not None else timezone.now()}
        values.update(kwargs)
        return Article.objects.create(**values)

    def test_models_generate_initial_slug_without_changing_an_existing_slug(self):
        article = self.article("Gestión táctica de prueba")
        self.assertEqual(article.slug, "gestion-tactica-de-prueba")
        article.title = "Título actualizado"
        article.save()
        self.assertEqual(article.slug, "gestion-tactica-de-prueba")
        self.assertEqual(str(self.category), "Pruebas editoriales")

    def test_public_lists_separate_types_and_hide_unavailable_articles(self):
        guide = self.article("Guía publicada")
        strategy = self.article("Estrategia publicada", Article.ArticleType.STRATEGY)
        draft = self.article("Borrador", status=Article.Status.DRAFT)
        future = self.article("Futura", published_at=timezone.now() + timedelta(days=1))
        undated = Article.objects.create(title="Sin fecha", article_type=Article.ArticleType.GUIDE, category=self.category, author=self.author, summary="Sin fecha.", body="Sin fecha.", status=Article.Status.PUBLISHED, published_at=None)

        guide_response = self.client.get(reverse("content:guide_list"))
        strategy_response = self.client.get(reverse("content:strategy_list"))
        self.assertContains(guide_response, guide.title)
        self.assertNotContains(guide_response, strategy.title)
        self.assertContains(strategy_response, strategy.title)
        for article in (draft, future, undated):
            self.assertNotContains(guide_response, article.title)
            self.assertEqual(self.client.get(reverse("content:guide_detail", args=[article.slug])).status_code, 404)

    def test_public_detail_uses_real_seo_data_and_escapes_body_html(self):
        article = self.article("Archivo seguro", body="<script>alert('x')</script>")
        response = self.client.get(reverse("content:guide_detail", args=[article.slug]))

        self.assertContains(response, article.title)
        self.assertContains(response, article.summary)
        self.assertContains(response, "&lt;script&gt;alert")
        self.assertNotContains(response, "<script>alert('x')</script>", html=True)
        self.assertContains(response, f"<title>{article.title} | Jorge CyberpunkTCG</title>", html=True)

    def test_navigation_home_and_admin_are_integrated(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, f'href="{reverse("content:guide_list")}"')
        self.assertContains(response, f'href="{reverse("content:strategy_list")}"')
        self.assertNotContains(response, "Guías <small>Próximamente")
        self.assertNotContains(response, "Estrategias <small>Próximamente")
        self.assertContains(response, "Choomdex <small>Próximamente")
        self.assertIn(Article, admin.site._registry)
        self.assertIn(ContentCategory, admin.site._registry)
