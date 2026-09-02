# Fase 7B — Fundación técnica del Deck Builder

## Alcance realizado

Se creó `apps.decks` como base de dominio sin vistas, rutas, templates, CSS, JavaScript ni UI pública. No se añadieron Cards, CardPrintings, importadores, scraping, imágenes, dependencias ni reglas RAM.

La app depende de `apps.cards`; Choomdex no depende de Decks y no se modificó su arquitectura.

## Modelos y relaciones

| Modelo | Responsabilidad | Relaciones y restricciones |
|---|---|---|
| `Deck` | Mazo persistido de un usuario | `owner` con `CASCADE`; nombre, slug, descripción opcional, `is_public=False`, timestamps; único `(owner, slug)` |
| `DeckLegend` | Una Legend fuera del MAIN | `deck` con `CASCADE`, `card` con `PROTECT`; único `(deck, card)`; CardType debe ser `LEGEND` |
| `DeckEntry` | Una Card lógica y su cantidad MAIN | `deck` con `CASCADE`, `card` con `PROTECT`; único `(deck, card)`; cantidad 1–3 y constraint DB positiva |

Las relaciones se dirigen exclusivamente a `Card`, nunca a `CardPrinting`. Dos printings no pueden alterar el límite de copias ni identidad de una carta. `DeckLegend` separado asegura que Legends no forman parte del conteo MAIN.

El slug se genera predeciblemente desde el nombre si está vacío. Puede repetirse entre usuarios, no dentro del mismo owner; no se añade sufijo ni se sobrescribe un slug existente de forma silenciosa.

No existe ningún campo persistido de validez (`is_valid`, RAM, estado de validación): el resultado se recalcula.

## Integridad y servicio

Las validaciones de modelo protegen también al Admin y a escrituras de servidor:

- una DeckLegend sólo admite una Card LEGEND;
- un DeckEntry no admite Legends;
- la cantidad MAIN debe estar entre 1 y 3;
- la base mantiene unicidad por deck+Card y evita cantidades no positivas.

Un borrador puede tener 0, 1 o 2 Legends y cualquier tamaño MAIN: la composición se persiste, aunque no sea estructuralmente válida. Reglas agregadas —exactamente tres Legends, MAIN 40–50 y resumen— viven en `DeckValidationService`.

El servicio devuelve `DeckValidationResult(valid, errors, warnings, summary)`. `valid` significa **validez estructural evaluada**, no legalidad completa del juego. El resumen contiene `legend_count`, `main_count` y `ram_status="NOT_EVALUATED"`.

RAM no se implementó: el modelo actual sólo dispone de valores impresos de CardPrinting y no contiene una fuente de reglas actuales, colores ni tratamiento de multicolor verificados. No hay algoritmo, colores hardcoded ni módulo RAM. Una Card histórica despublicada se conserva en el mazo y se informa como warning; el helper de elegibilidad para nuevas selecciones exige Card publicada con printing primaria y Set activo.

## Admin, rendimiento y seguridad futura

Deck, DeckLegend y DeckEntry están registrados en Admin. Deck incluye inlines de Legends y Entries. La validación de modelo sigue activa en ese camino.

El servicio carga Legends y Entries con `select_related("card")` y evalúa elegibilidad en una única consulta por conjunto de Cards; no consulta CardPrinting por cada entrada. Las operaciones compuestas de futuras fases deberán usar `transaction.atomic()`.

No se implementa CRUD todavía. La futura 7C deberá usar `login_required`, comprobación de owner, POST para mutaciones, CSRF y rechazo de IDs/cantidades no autorizados enviados por cliente.

## Migración y datos existentes

`apps/decks/migrations/0001_initial.py` crea sólo los modelos y constraints de Decks, con dependencias correctas hacia el usuario configurable y `cards.0004`. Se revisó antes de aplicar.

Tras `migrate`: Cards=4, CardPrintings=4, Decks=0, DeckEntries=0 y DeckLegends=0. El backup histórico permanece ignorado y sin modificación.

## Pruebas y cierre

Las pruebas de `apps.decks` cubren slug/owner/privacidad, cascadas, `PROTECT`, validación de tipos y cantidades, unicidad, drafts, 0–4 Legends, MAIN 39/40/50/51, copias, elegibilidad, warning histórico, RAM no evaluado, Admin y ausencia de N+1 en el servicio.

Próxima fase propuesta: **7C — CRUD y seguridad**, sin iniciar automáticamente. El gate RAM continúa abierto para una fase posterior con fuente y modelo de reglas actuales autorizados.
