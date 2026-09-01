from django.shortcuts import render


def home(request):
    """Render the public tactical cyberdeck landing page."""
    return render(request, "core/home.html")
