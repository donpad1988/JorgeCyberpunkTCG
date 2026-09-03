from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DeckMetadataForm
from .models import Deck
from .services import DeckValidationService


def get_visible_deck_or_404(request, username, slug):
    deck = get_object_or_404(
        Deck.objects.select_related("owner").prefetch_related("legends__card", "entries__card"),
        owner__username=username,
        slug=slug,
    )
    if deck.owner_id != getattr(request.user, "id", None) and not deck.is_public:
        raise Http404
    return deck


def get_owned_deck_or_404(request, username, slug):
    return get_object_or_404(
        Deck.objects.select_related("owner"),
        owner=request.user,
        owner__username=username,
        slug=slug,
    )


@login_required
def my_decks(request):
    decks = Deck.objects.filter(owner=request.user).order_by("-updated_at", "name")
    return render(request, "decks/deck_list.html", {"decks": decks})


def public_decks(request):
    decks = Deck.objects.filter(is_public=True).select_related("owner").order_by("-updated_at", "name")
    return render(request, "decks/public_deck_list.html", {"decks": decks})


@login_required
def deck_create(request):
    form = DeckMetadataForm(request.POST or None, owner=request.user)
    if request.method == "POST" and form.is_valid():
        deck = form.save(commit=False)
        deck.owner = request.user
        deck.save()
        return redirect("decks:deck_detail", username=deck.owner.username, slug=deck.slug)
    return render(request, "decks/deck_form.html", {"form": form, "heading": "Crear mazo"})


def deck_detail(request, username, slug):
    deck = get_visible_deck_or_404(request, username, slug)
    validation = DeckValidationService(deck).validate()
    return render(request, "decks/deck_detail.html", {"deck": deck, "validation": validation})


@login_required
def deck_update(request, username, slug):
    deck = get_owned_deck_or_404(request, username, slug)
    form = DeckMetadataForm(request.POST or None, instance=deck, owner=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("decks:deck_detail", username=deck.owner.username, slug=deck.slug)
    return render(request, "decks/deck_form.html", {"form": form, "deck": deck, "heading": "Editar mazo"})


@login_required
def deck_delete(request, username, slug):
    deck = get_owned_deck_or_404(request, username, slug)
    if request.method == "POST":
        deck.delete()
        return redirect("decks:my_decks")
    return render(request, "decks/deck_confirm_delete.html", {"deck": deck})
