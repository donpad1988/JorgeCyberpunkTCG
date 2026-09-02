from django.contrib import admin

from .models import Card, CardPrinting, Set


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "verified_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CardPrintingInline(admin.TabularInline):
    model = CardPrinting
    extra = 0
    fields = (
        "set",
        "collector_number",
        "cost",
        "ram",
        "power",
        "printing_label",
        "is_primary",
        "source_name",
        "source_url",
        "verified_at",
        "verification_notes",
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "card_type", "status")
    list_filter = ("status", "card_type")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CardPrintingInline,)


@admin.register(CardPrinting)
class CardPrintingAdmin(admin.ModelAdmin):
    list_display = ("card", "set", "collector_number", "is_primary")
    list_filter = ("is_primary", "set")
    search_fields = ("card__name", "collector_number", "printing_label")
