from dataclasses import dataclass

from apps.cards.models import Card
from django.db import transaction
from django.db.models import Sum

from .models import DeckEntry, DeckLegend


RAM_NOT_EVALUATED = "NOT_EVALUATED"


def is_card_eligible(card):
    return Card.objects.public().filter(pk=card.pk).exists()


@dataclass(frozen=True)
class DeckValidationResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    summary: dict


class DeckValidationService:
    def __init__(self, deck):
        self.deck = deck

    def validate(self):
        legends = list(self.deck.legends.select_related("card"))
        entries = list(self.deck.entries.select_related("card"))
        card_ids = {legend.card_id for legend in legends} | {entry.card_id for entry in entries}
        eligible_card_ids = set(
            Card.objects.public().filter(pk__in=card_ids).values_list("pk", flat=True)
        )
        errors = []
        warnings = []
        legend_count = len(legends)
        main_count = sum(entry.quantity for entry in entries)

        if legend_count != 3:
            errors.append("Selecciona exactamente 3 Legends únicas.")
        for legend in legends:
            if legend.card.card_type != Card.CardType.LEGEND:
                errors.append(f"{legend.card.name} no es una Legend válida.")
            elif legend.card_id not in eligible_card_ids:
                warnings.append(f"{legend.card.name} ya no está disponible para nuevas selecciones.")

        if main_count < 40:
            errors.append("El mazo principal necesita al menos 40 cartas.")
        if main_count > 50:
            errors.append("El mazo principal no puede superar 50 cartas.")
        for entry in entries:
            if entry.card.card_type == Card.CardType.LEGEND:
                errors.append(f"{entry.card.name} no puede formar parte del mazo principal.")
            if entry.quantity > 3:
                errors.append(f"{entry.card.name} supera el límite de tres copias.")
            if entry.card_id not in eligible_card_ids:
                warnings.append(f"{entry.card.name} ya no está disponible para nuevas selecciones.")

        summary = {
            "legend_count": legend_count,
            "main_count": main_count,
            "ram_status": RAM_NOT_EVALUATED,
        }
        return DeckValidationResult(
            valid=not errors,
            errors=tuple(dict.fromkeys(errors)),
            warnings=tuple(dict.fromkeys(warnings)),
            summary=summary,
        )


class DeckCompositionError(Exception):
    pass


class DeckCompositionService:
    def __init__(self, deck):
        self.deck = deck

    def _eligible_card(self, card_id):
        try:
            card = Card.objects.get(pk=card_id)
        except Card.DoesNotExist as exc:
            raise DeckCompositionError("La carta solicitada no existe.") from exc
        if not is_card_eligible(card):
            raise DeckCompositionError("Esta carta ya no está disponible para nuevas selecciones.")
        return card

    @transaction.atomic
    def add_legend(self, card_id):
        card = self._eligible_card(card_id)
        if card.card_type != Card.CardType.LEGEND:
            raise DeckCompositionError("Solo una Legend puede ocupar esta sección.")
        legends = DeckLegend.objects.select_for_update().filter(deck=self.deck)
        if legends.filter(card=card).exists():
            raise DeckCompositionError("Esta Legend ya está seleccionada.")
        if legends.count() >= 3:
            raise DeckCompositionError("Ya seleccionaste 3 Legends.")
        DeckLegend.objects.create(deck=self.deck, card=card)

    @transaction.atomic
    def remove_legend(self, legend_id):
        try:
            DeckLegend.objects.select_for_update().get(pk=legend_id, deck=self.deck).delete()
        except DeckLegend.DoesNotExist as exc:
            raise DeckCompositionError("La Legend no pertenece a este mazo.") from exc

    @transaction.atomic
    def add_main_card(self, card_id):
        card = self._eligible_card(card_id)
        if card.card_type == Card.CardType.LEGEND:
            raise DeckCompositionError("Las Legends no forman parte del mazo principal.")
        entries = DeckEntry.objects.select_for_update().filter(deck=self.deck)
        main_count = entries.aggregate(total=Sum("quantity"))["total"] or 0
        if main_count >= 50:
            raise DeckCompositionError("El MAIN ya alcanzó 50 cartas.")
        entry = entries.filter(card=card).first()
        if entry is None:
            DeckEntry.objects.create(deck=self.deck, card=card, quantity=1)
            return
        if entry.quantity >= 3:
            raise DeckCompositionError("Esta carta ya tiene 3 copias.")
        entry.quantity += 1
        entry.save(update_fields=("quantity",))

    @transaction.atomic
    def decrement_main_card(self, entry_id):
        try:
            entry = DeckEntry.objects.select_for_update().get(pk=entry_id, deck=self.deck)
        except DeckEntry.DoesNotExist as exc:
            raise DeckCompositionError("La entrada no pertenece a este mazo.") from exc
        if entry.quantity == 1:
            entry.delete()
            return
        entry.quantity -= 1
        entry.save(update_fields=("quantity",))

    @transaction.atomic
    def remove_main_card(self, entry_id):
        deleted, _ = DeckEntry.objects.filter(pk=entry_id, deck=self.deck).delete()
        if not deleted:
            raise DeckCompositionError("La entrada no pertenece a este mazo.")
