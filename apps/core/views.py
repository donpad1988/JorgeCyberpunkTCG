from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


def home(request):
    """Render the public tactical cyberdeck landing page."""
    return render(request, "core/home.html")


def robots_txt(request):
    """Serve dynamic text/plain robots.txt with sitemap reference."""
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /cuenta/\n"
        "Disallow: /mazos/*/editar/\n"
        "Disallow: /mazos/*/editorial/\n"
        "Disallow: /mazos/*/construir/\n"
        "Disallow: /mazos/*/eliminar/\n"
        "\n"
        f"Sitemap: {sitemap_url}\n"
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def health_check(request):
    """Serve cheap system status health check for production monitoring."""
    from django.http import JsonResponse

    response = JsonResponse({"status": "healthy"})
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response
