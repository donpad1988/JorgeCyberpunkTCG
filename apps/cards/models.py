from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
class Set(models.Model):
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    source_name = models.CharField(max_length=160, blank=True)
    source_url = models.URLField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CardQuerySet(models.QuerySet):
    def public(self):
        return self.filter(
            status=Card.Status.PUBLISHED,
            printings__is_primary=True,
            printings__set__is_active=True,
        ).distinct()


class Card(models.Model):
    class CardType(models.TextChoices):
        LEGEND = "LEGEND", "Legend"
        UNIT = "UNIT", "Unit"
        PROGRAM = "PROGRAM", "Program"
        GEAR = "GEAR", "Gear"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        REVIEWED = "REVIEWED", "Revisado"
        PUBLISHED = "PUBLISHED", "Publicado"

    name = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    card_type = models.CharField(max_length=10, choices=CardType.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    rules_text = models.TextField(blank=True)
    source_name = models.CharField(max_length=160, blank=True)
    source_url = models.URLField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CardQuerySet.as_manager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("cards:detail", kwargs={"slug": self.slug})



class CardPrinting(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="printings")
    set = models.ForeignKey(Set, on_delete=models.PROTECT, related_name="printings")
    collector_number = models.CharField(max_length=60, blank=True)
    cost = models.PositiveIntegerField(null=True, blank=True)
    ram = models.PositiveIntegerField(null=True, blank=True)
    power = models.PositiveIntegerField(null=True, blank=True)
    printing_label = models.CharField(max_length=160, blank=True)
    is_primary = models.BooleanField(default=False)
    source_name = models.CharField(max_length=160, blank=True)
    source_url = models.URLField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("card__name", "set__name", "collector_number")

    def __str__(self):
        collector = f" #{self.collector_number}" if self.collector_number else ""
        return f"{self.card} — {self.set}{collector}"

    def clean(self):
        super().clean()
        if self.is_primary and self.card_id and CardPrinting.objects.filter(
            card_id=self.card_id,
            is_primary=True,
        ).exclude(pk=self.pk).exists():
            raise ValidationError({"is_primary": "Cada Card puede tener una sola printing primaria."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
