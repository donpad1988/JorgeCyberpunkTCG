from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from apps.cards.models import Card


class DeckQuerySet(models.QuerySet):
    def public_current(self):
        return self.filter(is_public=True, editorial_status=Deck.EditorialStatus.PUBLISHED)

    def public_archive(self):
        return self.filter(is_public=True, editorial_status=Deck.EditorialStatus.ARCHIVED)


class Deck(models.Model):
    class EditorialStatus(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        PUBLISHED = "PUBLISHED", "Publicado"
        ARCHIVED = "ARCHIVED", "Archivado"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="decks")
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    editorial_status = models.CharField(max_length=10, choices=EditorialStatus.choices, default=EditorialStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DeckQuerySet.as_manager()

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
        DeckEditorialProfile.objects.get_or_create(deck=self)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("decks:deck_detail", kwargs={"username": self.owner.username, "slug": self.slug})


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
        if self.card_id and self.card.card_type != Card.CardType.LEGEND:    # type: ignore
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
        if self.card_id and self.card.card_type == Card.CardType.LEGEND:    # type: ignore
            errors["card"] = "Las Legends no forman parte del mazo principal."
        if self.quantity is not None and self.quantity > 3:
            errors["quantity"] = "Una Card lógica no puede superar tres copias en el mazo principal."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class DeckEditorialProfile(models.Model):
    """Contenido editorial propio que acompaña, sin alterar, la composición."""

    deck = models.OneToOneField(Deck, on_delete=models.CASCADE, related_name="editorial_profile")
    archetype = models.CharField(max_length=160, blank=True)
    short_summary = models.CharField(max_length=320, blank=True)
    strategy_overview = models.TextField(blank=True)
    game_plan = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Editorial: {self.deck}"


class DeckKeyCard(models.Model):
    profile = models.ForeignKey(DeckEditorialProfile, on_delete=models.CASCADE, related_name="key_cards")
    card = models.ForeignKey(Card, on_delete=models.PROTECT, related_name="deck_key_card_entries")
    editorial_note = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "card__name")
        constraints = [
            models.UniqueConstraint(fields=("profile", "card"), name="decks_unique_key_card_per_profile"),
        ]

    def __str__(self):
        return f"{self.profile.deck}: {self.card}"

    def clean(self):
        super().clean()
        if self.profile_id and self.card_id:    # type: ignore
            deck = self.profile.deck
            is_in_deck = deck.legends.filter(card_id=self.card_id).exists() or deck.entries.filter(card_id=self.card_id).exists()   # type: ignore
            if not is_in_deck:
                raise ValidationError({"card": "La carta clave debe formar parte de la composición del mazo."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
