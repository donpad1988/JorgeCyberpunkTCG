from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ContentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "categoría editorial"
        verbose_name_plural = "categorías editoriales"

    def __str__(self):
        return self.name


class ArticleQuerySet(models.QuerySet):
    def publicly_visible(self):
        return self.filter(status=Article.Status.PUBLISHED, published_at__lte=timezone.now())


class Article(models.Model):
    class ArticleType(models.TextChoices):
        GUIDE = "GUIDE", "Guía"
        STRATEGY = "STRATEGY", "Estrategia"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        PUBLISHED = "PUBLISHED", "Publicado"

    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    article_type = models.CharField(max_length=10, choices=ArticleType.choices)
    category = models.ForeignKey(ContentCategory, on_delete=models.PROTECT, related_name="articles")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="articles")
    summary = models.TextField()
    body = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ("-published_at", "-created_at")
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
