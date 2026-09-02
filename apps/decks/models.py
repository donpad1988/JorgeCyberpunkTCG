from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from apps.cards.models import Card


class Deck(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="decks")
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "name")
        constraints = [
            models.UniqueConstraint(fields=("owner", "slug"), name="decks_unique_owner_slug"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DeckLegend(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="legends")
    card = models.ForeignKey(Card, on_delete=models.PROTECT, related_name="deck_legend_entries")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("deck", "card"), name="decks_unique_legend_per_deck"),
        ]

    def __str__(self):
        return f"{self.deck}: {self.card}"

    def clean(self):
        super().clean()
        if self.card_id and self.card.card_type != Card.CardType.LEGEND:
            raise ValidationError({"card": "Solo una Card LEGEND puede ocupar una plaza de Legend."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class DeckEntry(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="entries")
    card = models.ForeignKey(Card, on_delete=models.PROTECT, related_name="deck_entries")
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("deck", "card"), name="decks_unique_entry_per_deck"),
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name="decks_entry_quantity_positive"),
        ]

    def __str__(self):
        return f"{self.deck}: {self.quantity} × {self.card}"

    def clean(self):
        super().clean()
        errors = {}
        if self.card_id and self.card.card_type == Card.CardType.LEGEND:
            errors["card"] = "Las Legends no forman parte del mazo principal."
        if self.quantity is not None and self.quantity > 3:
            errors["quantity"] = "Una Card lógica no puede superar tres copias en el mazo principal."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
