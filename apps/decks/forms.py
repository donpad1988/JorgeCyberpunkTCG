from django import forms
from django.db import models
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils.text import slugify

from apps.cards.models import Card

from .models import Deck, DeckEditorialProfile, DeckKeyCard


class DeckMetadataForm(forms.ModelForm):
    editorial_status = forms.ChoiceField(choices=Deck.EditorialStatus.choices, required=False)

    class Meta:
        model = Deck
        fields = ("name", "description", "is_public", "editorial_status")

    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not self.instance.pk:
            slug = slugify(name)
            if Deck.objects.filter(owner=self.owner, slug=slug).exists():
                raise forms.ValidationError("Ya tienes un mazo con este nombre.")
        return name

    def clean_editorial_status(self):
        status = self.cleaned_data["editorial_status"]
        if status:
            return status
        if self.instance.pk:
            return self.instance.editorial_status
        return Deck.EditorialStatus.DRAFT


class CardActionForm(forms.Form):
    card_id = forms.IntegerField(min_value=1)


class EntryActionForm(forms.Form):
    entry_id = forms.IntegerField(min_value=1)


class DeckEditorialForm(forms.ModelForm):
    class Meta:
        model = DeckEditorialProfile
        fields = ("archetype", "short_summary", "strategy_overview", "game_plan", "strengths", "weaknesses")
        widgets = {
            "strategy_overview": forms.Textarea(attrs={"rows": 5}),
            "game_plan": forms.Textarea(attrs={"rows": 5}),
            "strengths": forms.Textarea(attrs={"rows": 4}),
            "weaknesses": forms.Textarea(attrs={"rows": 4}),
        }


class DeckKeyCardForm(forms.ModelForm):
    class Meta:
        model = DeckKeyCard
        fields = ("card", "editorial_note", "display_order")
        widgets = {"editorial_note": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, deck, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["card"].queryset = Card.objects.filter(
            models.Q(deck_legend_entries__deck=deck) | models.Q(deck_entries__deck=deck)
        ).distinct()


class BaseDeckKeyCardFormSet(BaseInlineFormSet):
    def __init__(self, *args, deck, **kwargs):
        self.deck = deck
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["deck"] = self.deck
        return kwargs


DeckKeyCardFormSet = inlineformset_factory(
    DeckEditorialProfile,
    DeckKeyCard,
    form=DeckKeyCardForm,
    formset=BaseDeckKeyCardFormSet,
    extra=1,
    can_delete=True,
)
