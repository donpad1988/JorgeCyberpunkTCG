from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, render

from .models import Card, CardPrinting, Set


def with_primary_printing(queryset):
    return queryset.prefetch_related(
        Prefetch(
            "printings",
            queryset=CardPrinting.objects.filter(is_primary=True).select_related("set"),
            to_attr="primary_printings",
        )
    )


def add_primary_printings(cards):
    for card in cards:
        card.primary_printing = card.primary_printings[0]
    return cards


def catalog(request):
    queryset = Card.objects.public()
    query = request.GET.get("q", "").strip()
    set_slug = request.GET.get("set", "")
    card_type = request.GET.get("type", "")

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(printings__collector_number__icontains=query)
        )
    if set_slug:
        queryset = queryset.filter(printings__set__slug=set_slug)
    if card_type in Card.CardType.values:
        queryset = queryset.filter(card_type=card_type)

    queryset = with_primary_printing(queryset.distinct())
    page_obj = Paginator(queryset, 24).get_page(request.GET.get("page"))
    add_primary_printings(page_obj)
    sets = Set.objects.filter(
        is_active=True,
        printings__is_primary=True,
        printings__card__status=Card.Status.PUBLISHED,
    ).distinct()
    return render(
        request,
        "cards/catalog.html",
        {
            "page_obj": page_obj,
            "sets": sets,
            "q": query,
            "set_slug": set_slug,
            "card_type": card_type,
            "types": Card.CardType.choices,
        },
    )


def detail(request, slug):
    card = get_object_or_404(with_primary_printing(Card.objects.public()), slug=slug)
    card.primary_printing = card.primary_printings[0]
    return render(request, "cards/detail.html", {"card": card})
