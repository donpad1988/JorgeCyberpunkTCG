from django.shortcuts import get_object_or_404, render

from .models import Article


def article_list(request, article_type):
    articles = Article.objects.publicly_visible().filter(article_type=article_type).select_related("category", "author")
    return render(request, "content/article_list.html", {"articles": articles, "article_type": article_type})


def article_detail(request, article_type, slug):
    article = get_object_or_404(Article.objects.publicly_visible().select_related("category", "author"), article_type=article_type, slug=slug)
    return render(request, "content/article_detail.html", {"article": article})


def guide_list(request):
    return article_list(request, Article.ArticleType.GUIDE)


def strategy_list(request):
    return article_list(request, Article.ArticleType.STRATEGY)


def guide_detail(request, slug):
    return article_detail(request, Article.ArticleType.GUIDE, slug)


def strategy_detail(request, slug):
    return article_detail(request, Article.ArticleType.STRATEGY, slug)
