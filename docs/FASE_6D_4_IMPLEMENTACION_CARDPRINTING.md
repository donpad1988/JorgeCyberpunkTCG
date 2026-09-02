# Fase 6D.4 — Implementación controlada de CardPrinting

## Alcance ejecutado

Se implementó la separación entre la identidad lógica `Card` y la impresión verificable `CardPrinting`, sin ampliar el dominio. La relación final es `Card 1:N CardPrinting` y `Set 1:N CardPrinting`.

`Card` conserva `name`, `slug`, `card_type`, `status`, `rules_text`, la provenance de identidad (`source_name`, `source_url`, `verified_at`, `verification_notes`) y timestamps. Los cinco atributos que describen una impresión (`set`, `collector_number`, `cost`, `ram`, `power`) se retiraron de `Card` y viven exclusivamente en `CardPrinting`.

`CardPrinting` contiene la Card, el Set, esos atributos impresos, `printing_label` opcional, `is_primary`, provenance de la impresión y timestamps. El piloto conserva `printing_label=""`: no se inventa una taxonomía a partir de “Retail”, que sigue formando parte del nombre literal del Set.

No se añadieron importadores, scraping, llamadas API, imágenes, hotlinks, textos de reglas nuevos, rareza, ilustrador, keywords, facciones, subtipos, precios, mazos ni nuevas Cards.

## Seguridad previa y migraciones

Antes de ejecutar se verificó `db.sqlite3.backup_pre_cardprinting_20260902_1431`: existe, tenía el mismo tamaño inicial que `db.sqlite3` (208896 bytes) y su SHA-256 fue idéntico antes y después de migrar. Se añadió únicamente `db.sqlite3.backup_*` a `.gitignore`, para que esa copia local no pueda entrar accidentalmente en Git. El backup no fue modificado, renombrado ni incluido en el commit.

Las migraciones son deliberadamente separadas:

1. `0002_cardprinting_expand` crea `CardPrinting` sin quitar campos de `Card`.
2. `0003_migrate_cards_to_initial_printings` usa `apps.get_model()` histórico. Para cada Card crea una sola printing primaria, copia Set, atributos impresos y provenance; aborta ante más de una primaria o una primaria preexistente divergente.
3. `0004_cardprinting_contract` elimina sólo `set`, `collector_number`, `cost`, `ram` y `power` de `Card`.

El reverse de la migración de datos sólo permite volver atrás cuando cada Card tiene exactamente una printing primaria; si hay ambigüedad falla explícitamente. Después de `0004`, la recuperación segura ante un problema de datos sigue siendo restaurar el backup verificado, no seleccionar una printing arbitrariamente.

## Resultado del piloto

La base local final contiene 4 Cards y 4 CardPrintings. Cada Card tiene exactamente una primaria, el Set literal `Welcome to Night City — Retail`, slugs sin cambios y provenance copiada.

| Card | Slug | Collector | Cost | RAM | Power | Label |
|---|---|---:|---:|---:|---:|---|
| Field Operator | `field-operator` | 078 | 3 | 2 | 2 | vacío |
| Judy Álvarez — Braindance Maestro | `judy-alvarez-braindance-maestro` | 108 | vacío | 2 | vacío | vacío |
| Sandevistan | `sandevistan` | 095 | 3 | 3 | 2 | vacío |
| Take Control | `take-control` | 103 | 2 | 2 | vacío | vacío |

## Aplicación y administración

`Card.objects.public()` sólo devuelve Cards `PUBLISHED` con una printing primaria cuyo Set está activo. El catálogo sigue siendo de Cards lógicas, a 24 por página; busca por nombre o collector de cualquier printing, filtra por Set a través de printing y por tipo en Card, y aplica `distinct()` antes de paginar.

Las vistas hacen un `Prefetch` limitado a la printing primaria con su Set, por lo que catálogo y detalle renderizan los datos de esa printing sin una consulta por Card. La URL principal no cambia: `/choomdex/<slug>/`. No existe URL ni selector público por printing en esta fase.

El admin de Card incorpora `CardPrintingInline`; el modelo también tiene su lista de administración para búsqueda y revisión. La validación de modelo impide guardar más de una primary para una misma Card. No se declaró una restricción compleja de base de datos porque el piloto no tiene evidencia suficiente para una política adicional; la migración, el modelo, admin y tests cubren el invariante actual.

## Pruebas y verificación

La suite de `apps.cards` cubre modelo, cascada/PROTECT, primary, provenance, admin, migración histórica, visibilidad, búsqueda, Set/tipo, paginación, URLs, representación de la primary y ausencia de N+1. La prueba de migración parte de `0001_initial`, crea una Card histórica y verifica su transformación en `0003`.

Checks requeridos al cierre:

- `manage.py check`: OK.
- `manage.py makemigrations --check`: sin cambios.
- `manage.py test apps.cards -v 2`: 25 tests OK.
- `manage.py test`: se ejecuta como verificación final de regresión.

## Límites que permanecen

El gate de taxonomía Set/producto/release/canal sigue abierto: no se renombró ni normalizó el Set. `rules_text` permanece en Card sin mover ni enriquecer. La ingesta controlada sigue suspendida hasta disponer de fuente autorizada; no se implementó automatización de datos.
