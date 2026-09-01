from django.shortcuts import render


def home(request):
    """Minimal health page; visual work belongs to Phase 2."""
    return render(request, "core/home.html")
