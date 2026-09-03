from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404,render
from apps.decks.models import Deck
from .models import Video
def video_list(request): return render(request,"videos/video_list.html",{"videos":Video.objects.filter(is_active=True).prefetch_related("related_articles")})
def video_detail(request,slug):
    public_decks=Deck.objects.filter(is_public=True,editorial_status__in=(Deck.EditorialStatus.PUBLISHED,Deck.EditorialStatus.ARCHIVED)).select_related("owner","editorial_profile").annotate(
        legend_count=Count("legends",distinct=True),main_count=Count("entries",distinct=True)
    )
    video=get_object_or_404(Video.objects.filter(is_active=True).prefetch_related("related_articles",Prefetch("related_decks",queryset=public_decks,to_attr="public_related_decks")),slug=slug)
    return render(request,"videos/video_detail.html",{"video":video,"articles":video.related_articles.publicly_visible(),"decks":video.public_related_decks})
