from django.contrib import admin

from .models import Deck, DeckEntry, DeckLegend


class DeckLegendInline(admin.TabularInline):
    model = DeckLegend
    extra = 0


class DeckEntryInline(admin.TabularInline):
    model = DeckEntry
    extra = 0


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_public", "created_at", "updated_at")
    list_filter = ("is_public",)
    search_fields = ("name", "slug", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (DeckLegendInline, DeckEntryInline)


@admin.register(DeckLegend)
class DeckLegendAdmin(admin.ModelAdmin):
    list_display = ("deck", "card")
    search_fields = ("deck__name", "card__name")


@admin.register(DeckEntry)
class DeckEntryAdmin(admin.ModelAdmin):
    list_display = ("deck", "card", "quantity")
    search_fields = ("deck__name", "card__name")
