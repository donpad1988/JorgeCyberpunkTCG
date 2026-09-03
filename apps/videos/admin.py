from django.contrib import admin
from .models import Video
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display=("title","youtube_video_id","is_active","published_at","updated_at")
    list_filter=("is_active","published_at"); search_fields=("title","summary","youtube_video_id","youtube_url")
    prepopulated_fields={"slug":("title",)}; filter_horizontal=("related_articles","related_decks")
