from django.db import migrations


PRINTED_FIELDS = (
    "set_id",
    "collector_number",
    "cost",
    "ram",
    "power",
    "printing_label",
    "source_name",
    "source_url",
    "verified_at",
    "verification_notes",
)


def create_initial_printings(apps, schema_editor):
    Card = apps.get_model("cards", "Card")
    CardPrinting = apps.get_model("cards", "CardPrinting")

    for card in Card.objects.all().iterator():
        primary_printings = list(CardPrinting.objects.filter(card_id=card.pk, is_primary=True))
        if len(primary_printings) > 1:
            raise RuntimeError(f"Card {card.pk} tiene más de una printing primaria.")

        values = {
            "card_id": card.pk,
            "set_id": card.set_id,
            "collector_number": card.collector_number,
            "cost": card.cost,
            "ram": card.ram,
            "power": card.power,
            "printing_label": "",
            "is_primary": True,
            "source_name": card.source_name,
            "source_url": card.source_url,
            "verified_at": card.verified_at,
            "verification_notes": card.verification_notes,
        }
        if primary_printings:
            primary = primary_printings[0]
            if any(getattr(primary, field) != values[field] for field in PRINTED_FIELDS):
                raise RuntimeError(f"La printing primaria de Card {card.pk} no coincide con los datos heredados.")
            continue
        CardPrinting.objects.create(**values)


def restore_legacy_card_fields(apps, schema_editor):
    Card = apps.get_model("cards", "Card")
    CardPrinting = apps.get_model("cards", "CardPrinting")

    for card in Card.objects.all().iterator():
        printings = list(CardPrinting.objects.filter(card_id=card.pk))
        primaries = [printing for printing in printings if printing.is_primary]
        if len(printings) != 1 or len(primaries) != 1:
            raise RuntimeError(
                f"No es seguro revertir Card {card.pk}: se requiere exactamente una printing primaria."
            )
        primary = primaries[0]
        card.set_id = primary.set_id
        card.collector_number = primary.collector_number
        card.cost = primary.cost
        card.ram = primary.ram
        card.power = primary.power
        card.save(update_fields=("set", "collector_number", "cost", "ram", "power"))
        primary.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0002_cardprinting_expand"),
    ]

    operations = [
        migrations.RunPython(create_initial_printings, restore_legacy_card_fields),
    ]
