from django.shortcuts import get_object_or_404,render
from .models import Video
def video_list(request): return render(request,"videos/video_list.html",{"videos":Video.objects.filter(is_active=True).prefetch_related("related_articles")})
def video_detail(request,slug):
    video=get_object_or_404(Video.objects.filter(is_active=True).prefetch_related("related_articles"),slug=slug)
    return render(request,"videos/video_detail.html",{"video":video,"articles":video.related_articles.publicly_visible()})
