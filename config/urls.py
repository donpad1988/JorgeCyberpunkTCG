"""Root URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuenta/", include("apps.accounts.urls")),
    path("", include("apps.decks.urls")),
    path("", include("apps.content.urls")),
    path("", include("apps.videos.urls")),
    path("", include("apps.cards.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
