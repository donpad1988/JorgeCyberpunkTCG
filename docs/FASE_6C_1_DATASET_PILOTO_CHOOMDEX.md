# Fase 6C.1 — Dataset piloto verificado de Choomdex

## Alcance y estado

Este documento prepara exactamente un Set y cuatro Cards para una carga **manual** posterior en Django Admin. No crea registros, fixtures, seeds, comandos, migraciones ni cambios de código; `db.sqlite3` permanece intacta. La comprobación externa se realizó el 2026-09-01 exclusivamente contra las fichas del sitio oficial Cyberpunk TCG. El catálogo permanece vacío hasta que una persona introduzca y revise estos datos en Admin.

Cada ficha seleccionada cubre uno de los cuatro `CardType` disponibles en el MVP: `LEGEND`, `UNIT`, `PROGRAM` y `GEAR`.

## Compatibilidad con el modelo actual

`Set` admite `name`, `slug`, `description`, `is_active`, `source_name`, `source_url`, `verified_at` y `verification_notes`. `Card` admite los campos del piloto y se relaciona con `Set` mediante `ForeignKey(..., on_delete=PROTECT)`.

| Campo | Tipo actual | Compatibilidad del piloto |
|---|---|---|
| `collector_number` | `CharField(max_length=60, blank=True)` | Compatible; conserva `078`, `095` y `103` sin perder ceros iniciales. |
| `cost`, `ram`, `power` | `PositiveIntegerField(null=True, blank=True)` | Compatibles con los enteros propuestos y con `VACÍO`. |
| `source_url` | `URLField(blank=True)` | Compatible con las URLs HTTPS oficiales. |
| `verified_at` | `DateTimeField(null=True, blank=True)` | Introducir en Admin la fecha y hora reales de la carga/verificación manual; no prellenar una fecha ficticia. |
| `rules_text` | `TextField(blank=True)` | Dejar `VACÍO` para este piloto. |

Al guardar un registro sin slug, `save()` usa `slugify(name)`; Admin también precompleta el campo. Los slugs propuestos son `welcome-to-night-city-retail`, `judy-alvarez-braindance-maestro`, `field-operator`, `take-control` y `sandevistan`. Deben conservarse salvo colisión real en una futura carga manual.

## Set piloto

La referencia de producto/Set para las cuatro entradas es **Welcome to Night City — Retail**. El modelo aún no distingue una identidad lógica de carta de una impresión concreta: el valor identifica la impresión de referencia, no modela todos los printings.

| Campo | Valor | Fuente | Observación |
|---|---|---|---|
| `name` | Welcome to Night City — Retail | Fichas oficiales de las cuatro cartas | Set de referencia común. |
| `slug` | welcome-to-night-city-retail | Derivado por Django Admin | Propuesta; se genera si se deja vacío. |
| `description` | VACÍO | — | No inventar descripción. |
| `is_active` | Sí | Decisión de publicación manual | Necesario para que Cards `PUBLISHED` sean públicas. |
| `source_name` | Cyberpunk TCG — Official Card Database | Sitio oficial | Fuente Nivel A. |
| `source_url` | https://cyberpunktcg.com/cards/judy-a-lvarez-braindance-maestro | Ficha oficial | Una ficha oficial que confirma el Set; las cuatro lo confirman. |
| `verified_at` | INTRODUCIR fecha/hora real de carga manual | Admin | No usar una fecha documentada como si fuese la carga. |
| `verification_notes` | Set contrastado en las cuatro fichas oficiales del piloto; el modelo no representa printings. | Fichas oficiales | No cargar code, release date ni card count. |

## Cards piloto

### Judy Álvarez — Braindance Maestro

| Campo | Valor | Fuente | Observación |
|---|---|---|---|
| `name` | Judy Álvarez — Braindance Maestro | [Ficha oficial](https://cyberpunktcg.com/cards/judy-a-lvarez-braindance-maestro) | Nombre oficial. |
| `slug` | judy-alvarez-braindance-maestro | Derivado por Django Admin | Propuesta. |
| `set` | Welcome to Night City — Retail | Ficha oficial | Usar el Set piloto. |
| `card_type` | LEGEND | Ficha oficial | Tipo canónico del MVP. |
| `collector_number` | 108 | Ficha oficial | Texto compatible con `CharField`. |
| `cost` | VACÍO | — | Deliberadamente no cargado. |
| `ram` | 2 | Ficha oficial | Entero positivo. |
| `power` | VACÍO | — | Deliberadamente no cargado. |
| `rules_text` | VACÍO | — | Política conservadora: no reproducir reglas. |
| `status` | PUBLISHED | Decisión editorial del piloto | Visible sólo si el Set está activo. |
| `source_name` | Cyberpunk TCG — Official Card Database | Sitio oficial | Fuente Nivel A. |
| `source_url` | https://cyberpunktcg.com/cards/judy-a-lvarez-braindance-maestro | Ficha oficial | URL de procedencia. |
| `verified_at` | INTRODUCIR fecha/hora real de carga manual | Admin | No prellenar. |
| `verification_notes` | Datos estructurados contrastados con ficha oficial; rules text y arte no se reproducen en este piloto. | Ficha oficial | Nota breve de procedencia. |

### Field Operator

| Campo | Valor | Fuente | Observación |
|---|---|---|---|
| `name` | Field Operator | [Ficha oficial](https://cyberpunktcg.com/cards/field-operator) | Nombre oficial. |
| `slug` | field-operator | Derivado por Django Admin | Propuesta. |
| `set` | Welcome to Night City — Retail | Ficha oficial | Usar el Set piloto. |
| `card_type` | UNIT | Ficha oficial | Tipo canónico del MVP. |
| `collector_number` | 078 | Ficha oficial | Conservar el cero inicial. |
| `cost` | 3 | Ficha oficial | Entero positivo. |
| `ram` | 2 | Ficha oficial | Entero positivo. |
| `power` | 2 | Ficha oficial | Entero positivo. |
| `rules_text` | VACÍO | — | Política conservadora: no reproducir reglas. |
| `status` | PUBLISHED | Decisión editorial del piloto | Visible sólo si el Set está activo. |
| `source_name` | Cyberpunk TCG — Official Card Database | Sitio oficial | Fuente Nivel A. |
| `source_url` | https://cyberpunktcg.com/cards/field-operator | Ficha oficial | URL de procedencia. |
| `verified_at` | INTRODUCIR fecha/hora real de carga manual | Admin | No prellenar. |
| `verification_notes` | Datos estructurados contrastados con ficha oficial; rules text y arte no se reproducen en este piloto. | Ficha oficial | Nota breve de procedencia. |

### Take Control

| Campo | Valor | Fuente | Observación |
|---|---|---|---|
| `name` | Take Control | [Ficha oficial](https://cyberpunktcg.com/cards/take-control) | Nombre oficial. |
| `slug` | take-control | Derivado por Django Admin | Propuesta. |
| `set` | Welcome to Night City — Retail | Ficha oficial | Usar el Set piloto. |
| `card_type` | PROGRAM | Ficha oficial | Tipo canónico del MVP. |
| `collector_number` | 103 | Ficha oficial | Texto compatible con `CharField`. |
| `cost` | 2 | Ficha oficial | Entero positivo. |
| `ram` | 2 | Ficha oficial | Entero positivo. |
| `power` | VACÍO | — | Deliberadamente no cargado. |
| `rules_text` | VACÍO | — | Política conservadora: no reproducir reglas. |
| `status` | PUBLISHED | Decisión editorial del piloto | Visible sólo si el Set está activo. |
| `source_name` | Cyberpunk TCG — Official Card Database | Sitio oficial | Fuente Nivel A. |
| `source_url` | https://cyberpunktcg.com/cards/take-control | Ficha oficial | URL de procedencia. |
| `verified_at` | INTRODUCIR fecha/hora real de carga manual | Admin | No prellenar. |
| `verification_notes` | Datos estructurados contrastados con ficha oficial; rules text y arte no se reproducen en este piloto. | Ficha oficial | Nota breve de procedencia. |

### Sandevistan

| Campo | Valor | Fuente | Observación |
|---|---|---|---|
| `name` | Sandevistan | [Ficha oficial](https://cyberpunktcg.com/cards/sandevistan) | Nombre oficial. |
| `slug` | sandevistan | Derivado por Django Admin | Propuesta. |
| `set` | Welcome to Night City — Retail | Ficha oficial | Usar el Set piloto. |
| `card_type` | GEAR | Ficha oficial | Tipo canónico del MVP. |
| `collector_number` | 095 | Ficha oficial | Conservar el cero inicial. |
| `cost` | 3 | Ficha oficial | Entero positivo. |
| `ram` | 3 | Ficha oficial | Entero positivo. |
| `power` | 2 | Ficha oficial | Entero positivo. |
| `rules_text` | VACÍO | — | Política conservadora: no reproducir reglas. |
| `status` | PUBLISHED | Decisión editorial del piloto | Visible sólo si el Set está activo. |
| `source_name` | Cyberpunk TCG — Official Card Database | Sitio oficial | Fuente Nivel A. |
| `source_url` | https://cyberpunktcg.com/cards/sandevistan | Ficha oficial | URL de procedencia. |
| `verified_at` | INTRODUCIR fecha/hora real de carga manual | Admin | No prellenar. |
| `verification_notes` | Datos estructurados contrastados con ficha oficial; rules text y arte no se reproducen en este piloto. | Ficha oficial | Nota breve de procedencia. |

## Decisiones de datos y límite arquitectónico

`rules_text` queda vacío: las fichas oficiales contienen reglas, pero no se copian a documentación ni a la base de datos de este piloto. No se descargan imágenes, no se guardan URLs de imagen y no se hace hotlink; Choomdex continúa con placeholders propios. La fuente oficial también muestra rareza, pero `rarity` sigue fuera del modelo y no se carga.

Las fichas oficiales muestran múltiples printings: Judy Álvarez — Braindance Maestro (4), Field Operator (5), Take Control (2) y Sandevistan (4). Esto aporta evidencia oficial de que una identidad de carta puede tener varias impresiones. `CardPrinting` permanece **POSPUESTO EN 6B**, con necesidad futura respaldada por evidencia oficial. Antes de un catálogo masivo debe reevaluarse `Card` frente a `CardPrinting`; este piloto deliberadamente pequeño evita introducir deuda de datos bajo el modelo simplificado.

## Orden de carga manual

1. Crear el Set piloto en Django Admin.
2. Guardar el Set y comprobar que está activo.
3. Crear Judy Álvarez — Braindance Maestro.
4. Crear Field Operator.
5. Crear Take Control.
6. Crear Sandevistan.
7. Verificar `/choomdex/`.
8. Probar los filtros `LEGEND`, `UNIT`, `PROGRAM` y `GEAR`.
9. Buscar `Judy`, `Field Operator`, `Take Control` y `Sandevistan`.
10. Abrir cada detalle y confirmar procedencia, valores y visibilidad pública.

La carga manual no forma parte de esta fase. La Fase 6C.2 no se ejecuta.
