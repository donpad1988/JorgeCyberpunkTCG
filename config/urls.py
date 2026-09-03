"""Root URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core import views as core_views
from apps.core.sitemaps import (
    ArticleSitemap,
    CardSitemap,
    DeckSitemap,
    StaticViewSitemap,
    VideoSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "articles": ArticleSitemap,
    "videos": VideoSitemap,
    "cards": CardSitemap,
    "decks": DeckSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("cuenta/", include("apps.accounts.urls")),
    path("", include("apps.decks.urls")),
    path("", include("apps.content.urls")),
    path("", include("apps.videos.urls")),
    path("", include("apps.cards.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
