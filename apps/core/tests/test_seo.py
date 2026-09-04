from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.cards.models import Card, CardPrinting, Set
from apps.content.models import Article, ContentCategory
from apps.decks.models import Deck
from apps.videos.models import Video

User = get_user_model()


class SeoDiscoveryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="seo_owner", password="password123")
        self.category = ContentCategory.objects.create(name="Estrategia General", slug="estrategia-general")

        from django.utils import timezone

        # Articles
        self.published_article = Article.objects.create(
            title="Guía Táctica Piloto",
            article_type=Article.ArticleType.GUIDE,
            category=self.category,
            author=self.user,
            summary="Resumen de guía",
            body="Cuerpo de guía",
            status=Article.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        self.draft_article = Article.objects.create(
            title="Borrador de Estrategia",
            article_type=Article.ArticleType.STRATEGY,
            category=self.category,
            author=self.user,
            summary="Resumen borrador",
            body="Cuerpo borrador",
            status=Article.Status.DRAFT,
        )

        # Videos
        self.active_video = Video.objects.create(
            title="Video Activo",
            youtube_url="https://www.youtube.com/watch?v=active123",
            youtube_video_id="active123",
            summary="Resumen video activo",
            is_active=True,
        )
        self.inactive_video = Video.objects.create(
            title="Video Inactivo",
            youtube_url="https://www.youtube.com/watch?v=inactive123",
            youtube_video_id="inactive123",
            summary="Resumen video inactivo",
            is_active=False,
        )

        # Cards
        self.set_item = Set.objects.create(name="Core Set", is_active=True)
        self.public_card = Card.objects.create(
            name="Carta Pública",
            card_type=Card.CardType.UNIT,
            status=Card.Status.PUBLISHED,
        )
        CardPrinting.objects.create(card=self.public_card, set=self.set_item, is_primary=True, collector_number="001")

        self.draft_card = Card.objects.create(
            name="Carta Borrador",
            card_type=Card.CardType.PROGRAM,
            status=Card.Status.DRAFT,
        )
        CardPrinting.objects.create(card=self.draft_card, set=self.set_item, is_primary=True, collector_number="002")

        # Decks
        self.published_public_deck = Deck.objects.create(
            owner=self.user,
            name="Mazo Público Publicado",
            is_public=True,
            editorial_status=Deck.EditorialStatus.PUBLISHED,
        )
        self.draft_deck = Deck.objects.create(
            owner=self.user,
            name="Mazo Borrador",
            is_public=False,
            editorial_status=Deck.EditorialStatus.DRAFT,
        )
        self.published_private_deck = Deck.objects.create(
            owner=self.user,
            name="Mazo Privado Publicado",
            is_public=False,
            editorial_status=Deck.EditorialStatus.PUBLISHED,
        )
        self.archived_deck = Deck.objects.create(
            owner=self.user,
            name="Mazo Archivados",
            is_public=True,
            editorial_status=Deck.EditorialStatus.ARCHIVED,
        )

    def test_sitemap_xml_returns_200_and_xml_content_type(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("xml" in response["Content-Type"])

    def test_sitemap_includes_public_landings_and_public_entities(self):
        response = self.client.get(reverse("sitemap"))
        content = response.content.decode("utf-8")

        # Landings
        self.assertIn(reverse("core:home"), content)
        self.assertIn(reverse("content:guide_list"), content)
        self.assertIn(reverse("content:strategy_list"), content)
        self.assertIn(reverse("videos:list"), content)
        self.assertIn(reverse("cards:catalog"), content)
        self.assertIn(reverse("decks:public_decks"), content)
        self.assertIn(reverse("core:privacy"), content)
        self.assertIn(reverse("core:terms"), content)


        # Public entities
        self.assertIn(self.published_article.get_absolute_url(), content)
        self.assertIn(self.active_video.get_absolute_url(), content)
        self.assertIn(self.public_card.get_absolute_url(), content)
        self.assertIn(self.published_public_deck.get_absolute_url(), content)

    def test_sitemap_excludes_drafts_private_archived_builder_editors_and_auth(self):
        response = self.client.get(reverse("sitemap"))
        content = response.content.decode("utf-8")

        # Exclusions
        self.assertNotIn(self.draft_article.slug, content)
        self.assertNotIn(self.inactive_video.slug, content)
        self.assertNotIn(self.draft_card.slug, content)
        self.assertNotIn(self.draft_deck.slug, content)
        self.assertNotIn(self.published_private_deck.slug, content)
        self.assertNotIn(self.archived_deck.slug, content)

        # Auth & management routes excluded
        self.assertNotIn("/cuenta/login/", content)
        self.assertNotIn("/cuenta/registro/", content)
        self.assertNotIn("/admin/", content)
        self.assertNotIn("/construir/", content)
        self.assertNotIn("/editorial/", content)
        self.assertNotIn("/editar/", content)

    def test_robots_txt_returns_200_text_plain_and_dynamic_sitemap_directive(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")

        content = response.content.decode("utf-8")
        self.assertIn("User-agent: *", content)
        self.assertIn("Disallow: /admin/", content)
        self.assertIn("Disallow: /cuenta/", content)
        self.assertIn("Sitemap: http://testserver/sitemap.xml", content)

    def test_canonical_urls_and_query_string_stripping(self):
        # Catalog with search query string returns canonical link pointing to base catalog URL
        response = self.client.get(reverse("cards:catalog") + "?q=solos&type=UNIT&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<link rel="canonical" href="http://testserver/choomdex/">')

        # Public deck list with search query string returns clean canonical link
        pub_response = self.client.get(reverse("decks:public_decks") + "?q=control")
        self.assertEqual(pub_response.status_code, 200)
        self.assertContains(pub_response, '<link rel="canonical" href="http://testserver/mazos/publicos/">')

    def test_meta_robots_noindex_on_private_and_archived_pages(self):
        # Login page has noindex
        login_res = self.client.get(reverse("accounts:login"))
        self.assertContains(login_res, '<meta name="robots" content="noindex, nofollow">')

        # Archived deck detail has noindex
        archived_res = self.client.get(self.archived_deck.get_absolute_url())
        self.assertContains(archived_res, '<meta name="robots" content="noindex, nofollow">')

        # Owner preview of draft deck has noindex
        self.client.force_login(self.user)
        draft_res = self.client.get(self.draft_deck.get_absolute_url())
        self.assertContains(draft_res, '<meta name="robots" content="noindex, nofollow">')
