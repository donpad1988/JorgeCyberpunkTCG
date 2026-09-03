from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, transaction
from django.core.paginator import Paginator
from django.db.models import Count, Exists, IntegerField, OuterRef, Prefetch, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.cards.models import Card, Set
from apps.videos.models import Video

from .forms import CardActionForm, DeckEditorialForm, DeckKeyCardFormSet, DeckMetadataForm, EntryActionForm
from .models import Deck, DeckEditorialProfile, DeckEntry
from .services import DeckCompositionError, DeckCompositionService, DeckValidationService


def get_visible_deck_or_404(request, username, slug):
    deck = get_object_or_404(
        Deck.objects.select_related("owner", "editorial_profile").prefetch_related(
            "legends__card", "entries__card", "editorial_profile__key_cards__card",
            Prefetch("related_videos", queryset=Video.objects.filter(is_active=True), to_attr="public_related_videos"),
        ),
        owner__username=username,
        slug=slug,
    )
    is_owner = deck.owner_id == getattr(request.user, "id", None)
    is_publicly_accessible = deck.is_public and deck.editorial_status in (
        Deck.EditorialStatus.PUBLISHED,
        Deck.EditorialStatus.ARCHIVED,
    )
    if not is_owner and not is_publicly_accessible:
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
    query = request.GET.get("q", "").strip()
    main_totals = DeckEntry.objects.filter(deck=OuterRef("pk")).values("deck").annotate(total=Sum("quantity")).values("total")
    active_videos = Video.objects.filter(is_active=True, related_decks=OuterRef("pk"))
    annotations = {
        "legend_count": Count("legends", distinct=True),
        "main_count": Coalesce(Subquery(main_totals, output_field=IntegerField()), Value(0)),
        "has_active_video": Exists(active_videos),
    }
    base_query = Deck.objects.select_related("owner", "editorial_profile").annotate(**annotations)
    decks = base_query.public_current()
    if query:
        decks = decks.filter(
            models.Q(name__icontains=query)
            | models.Q(editorial_profile__archetype__icontains=query)
            | models.Q(editorial_profile__short_summary__icontains=query)
        )
    decks = decks.order_by("-updated_at", "name")
    page_obj = Paginator(decks, 12).get_page(request.GET.get("page"))
    archived_decks = base_query.public_archive().order_by("-updated_at", "name")
    return render(
        request,
        "decks/public_deck_list.html",
        {"decks": page_obj, "page_obj": page_obj, "archived_decks": archived_decks, "q": query},
    )


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
    legends = sorted(deck.legends.all(), key=lambda legend: legend.card.name.lower())
    entries = sorted(deck.entries.all(), key=lambda entry: (entry.card.card_type, entry.card.name.lower()))
    cards = [legend.card for legend in legends] + [entry.card for entry in entries]
    public_card_ids = set(Card.objects.public().filter(pk__in=[card.pk for card in cards]).values_list("pk", flat=True))
    return render(
        request,
        "decks/deck_detail.html",
        {"deck": deck, "validation": validation, "public_card_ids": public_card_ids, "legends": legends, "entries": entries, "videos": deck.public_related_videos},
    )


@login_required
def deck_builder(request, username, slug):
    deck = get_owned_deck_or_404(request, username, slug)
    query = request.GET.get("q", "").strip()
    card_type = request.GET.get("type", "")
    set_slug = request.GET.get("set", "")
    cards = Card.objects.public().exclude(card_type=Card.CardType.LEGEND)
    if query:
        cards = cards.filter(name__icontains=query)
    if card_type in Card.CardType.values and card_type != Card.CardType.LEGEND:
        cards = cards.filter(card_type=card_type)
    if set_slug:
        cards = cards.filter(printings__is_primary=True, printings__set__slug=set_slug)
    cards = cards.distinct()
    sets = Set.objects.filter(
        is_active=True,
        printings__is_primary=True,
        printings__card__status=Card.Status.PUBLISHED,
    ).distinct()
    legends = Card.objects.public().filter(card_type=Card.CardType.LEGEND)
    validation = DeckValidationService(deck).validate()
    return render(
        request,
        "decks/deck_builder.html",
        {
            "deck": deck,
            "validation": validation,
            "available_legends": legends,
            "available_cards": cards,
            "sets": sets,
            "q": query,
            "card_type": card_type,
            "set_slug": set_slug,
            "types": Card.CardType.choices,
        },
    )


def _composition_action(request, username, slug, form_class, method, success_message):
    if request.method != "POST":
        raise Http404
    deck = get_owned_deck_or_404(request, username, slug)
    form = form_class(request.POST)
    if not form.is_valid():
        messages.error(request, "La acción recibida no es válida.")
        return redirect("decks:deck_builder", username=deck.owner.username, slug=deck.slug)
    try:
        getattr(DeckCompositionService(deck), method)(*form.cleaned_data.values())
    except DeckCompositionError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, success_message)
    return redirect("decks:deck_builder", username=deck.owner.username, slug=deck.slug)


@login_required
def legend_add(request, username, slug):
    return _composition_action(request, username, slug, CardActionForm, "add_legend", "Legend añadida.")


@login_required
def legend_remove(request, username, slug):
    return _composition_action(request, username, slug, EntryActionForm, "remove_legend", "Legend retirada.")


@login_required
def main_add(request, username, slug):
    return _composition_action(request, username, slug, CardActionForm, "add_main_card", "Carta añadida al MAIN.")


@login_required
def main_decrement(request, username, slug):
    return _composition_action(request, username, slug, EntryActionForm, "decrement_main_card", "Cantidad del MAIN actualizada.")


@login_required
def main_remove(request, username, slug):
    return _composition_action(request, username, slug, EntryActionForm, "remove_main_card", "Carta retirada del MAIN.")


@login_required
def deck_update(request, username, slug):
    deck = get_owned_deck_or_404(request, username, slug)
    form = DeckMetadataForm(request.POST or None, instance=deck, owner=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("decks:deck_detail", username=deck.owner.username, slug=deck.slug)
    return render(request, "decks/deck_form.html", {"form": form, "deck": deck, "heading": "Editar mazo"})


@login_required
def deck_editorial_update(request, username, slug):
    deck = get_owned_deck_or_404(request, username, slug)
    profile, _ = DeckEditorialProfile.objects.get_or_create(deck=deck)
    form = DeckEditorialForm(request.POST or None, instance=profile)
    formset = DeckKeyCardFormSet(request.POST or None, instance=profile, deck=deck)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            form.save()
            formset.save()
        return redirect("decks:deck_detail", username=deck.owner.username, slug=deck.slug)
    return render(request, "decks/deck_editorial_form.html", {"deck": deck, "form": form, "formset": formset})


@login_required
def deck_delete(request, username, slug):
    deck = get_owned_deck_or_404(request, username, slug)
    if request.method == "POST":
        deck.delete()
        return redirect("decks:my_decks")
    return render(request, "decks/deck_confirm_delete.html", {"deck": deck})
