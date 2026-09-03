from django import forms
from django.utils.text import slugify

from .models import Deck


class DeckMetadataForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ("name", "description", "is_public")

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
