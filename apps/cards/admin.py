from django.contrib import admin
from .models import Card,Set
@admin.register(Set)
class SetAdmin(admin.ModelAdmin): list_display=("name","is_active","verified_at"); list_filter=("is_active",); search_fields=("name","slug"); prepopulated_fields={"slug":("name",)}
@admin.register(Card)
class CardAdmin(admin.ModelAdmin): list_display=("name","card_type","set","status","collector_number"); list_filter=("status","card_type","set"); search_fields=("name","collector_number"); prepopulated_fields={"slug":("name",)}
