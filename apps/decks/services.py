from dataclasses import dataclass

from apps.cards.models import Card


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
