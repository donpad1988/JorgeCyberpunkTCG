from django.contrib import admin

from .models import Deck, DeckEditorialProfile, DeckEntry, DeckKeyCard, DeckLegend


class DeckLegendInline(admin.TabularInline):
    model = DeckLegend
    extra = 0


class DeckEntryInline(admin.TabularInline):
    model = DeckEntry
    extra = 0


class DeckEditorialProfileInline(admin.StackedInline):
    model = DeckEditorialProfile
    extra = 0
    max_num = 1


class DeckKeyCardInline(admin.TabularInline):
    model = DeckKeyCard
    extra = 0


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_public", "created_at", "updated_at")
    list_filter = ("is_public",)
    search_fields = ("name", "slug", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (DeckEditorialProfileInline, DeckLegendInline, DeckEntryInline)


@admin.register(DeckLegend)
class DeckLegendAdmin(admin.ModelAdmin):
    list_display = ("deck", "card")
    search_fields = ("deck__name", "card__name")


@admin.register(DeckEntry)
class DeckEntryAdmin(admin.ModelAdmin):
    list_display = ("deck", "card", "quantity")
    search_fields = ("deck__name", "card__name")


@admin.register(DeckEditorialProfile)
class DeckEditorialProfileAdmin(admin.ModelAdmin):
    list_display = ("deck", "archetype", "updated_at")
    search_fields = ("deck__name", "archetype", "short_summary")
    inlines = (DeckKeyCardInline,)


@admin.register(DeckKeyCard)
class DeckKeyCardAdmin(admin.ModelAdmin):
    list_display = ("profile", "card", "display_order")
    search_fields = ("profile__deck__name", "card__name")
