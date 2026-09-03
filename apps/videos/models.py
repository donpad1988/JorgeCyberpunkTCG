from django.db import models
from django.utils.text import slugify
from apps.content.models import Article
from apps.decks.models import Deck

class Video(models.Model):
    title=models.CharField(max_length=220); slug=models.SlugField(unique=True,blank=True)
    youtube_url=models.URLField(); youtube_video_id=models.CharField(max_length=50); summary=models.TextField()
    published_at=models.DateTimeField(null=True,blank=True); is_active=models.BooleanField(default=True)
    related_articles=models.ManyToManyField(Article,blank=True,related_name="videos")
    related_decks=models.ManyToManyField(Deck,blank=True,related_name="related_videos")
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=("-published_at","-created_at")
    def __str__(self): return self.title
    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("videos:detail", kwargs={"slug": self.slug})
