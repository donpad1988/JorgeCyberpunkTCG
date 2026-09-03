from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.cards.models import Card
from apps.content.models import Article
from apps.decks.models import Deck
from apps.videos.models import Video


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            "core:home",
            "content:guide_list",
            "content:strategy_list",
            "videos:list",
            "cards:catalog",
            "decks:public_decks",
        ]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    def items(self):
        return Article.objects.publicly_visible()

    def lastmod(self, obj):
        return obj.updated_at


class VideoSitemap(Sitemap):
    def items(self):
        return Video.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class CardSitemap(Sitemap):
    def items(self):
        return Card.objects.public()

    def lastmod(self, obj):
        return obj.updated_at


class DeckSitemap(Sitemap):
    def items(self):
        return Deck.objects.public_current()

    def lastmod(self, obj):
        return obj.updated_at
