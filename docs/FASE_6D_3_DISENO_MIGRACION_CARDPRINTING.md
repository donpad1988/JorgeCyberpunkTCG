# Fase 6D.3 — Diseño de migración controlada Card → CardPrinting

## Estado inicial y decisiones vinculantes

Preflight del 2026-09-02: directorio `D:\01.Proyectos_Web\JorgeCyberpunkTCG`, HEAD `5e39495`, Git limpio, `check` OK, `makemigrations --check` sin cambios y 37 tests OK. Consulta Django de sólo lectura: 1 Set, **Welcome to Night City — Retail**, y 4 Cards `PUBLISHED`:

| Card | Slug | Collector | Cost | RAM | Power | Set |
|---|---|---|---:|---:|---:|---|
| Field Operator | field-operator | 078 | 3 | 2 | 2 | Welcome to Night City — Retail |
| Judy Álvarez — Braindance Maestro | judy-alvarez-braindance-maestro | 108 | VACÍO | 2 | VACÍO | Welcome to Night City — Retail |
| Sandevistan | sandevistan | 095 | 3 | 3 | 2 | Welcome to Night City — Retail |
| Take Control | take-control | 103 | 2 | 2 | VACÍO | Welcome to Night City — Retail |

Se mantienen como baseline vinculante: Card es identidad lógica/editorial; CardPrinting es impresión verificable; Set conserva etiqueta oficial literal; el catálogo lista una Card lógica; Card.slug mantiene la URL principal; Deck Builder futuro refiere Card; mercado futuro refiere CardPrinting; importación masiva continúa **NO-GO**. La relación es `Card 1—N CardPrinting N—1 Set`, coherente con 6D.1/6D.2.

Los siete gates de 6D.1 quedan incorporados sin reinterpretación: identidad/nombres/errata, contexto de collector/labels, Set frente a producto/release/canal, atributos impresos frente a reglas actuales/copyright, URLs, impacto en consumidores y migración reversible del piloto. Tras 6D.2, los gates 1, 2 y 4–7 están **CERRADOS CON CONDICIONES**; el gate 3 permanece **ABIERTO**. Este diseño no intenta cerrar el gate 3.

## Contratos futuros mínimos

### Card

Card conserva solamente la responsabilidad lógica/editorial: `name`, `slug`, `card_type`, `status`, `source_name`, `source_url`, `verified_at`, `verification_notes`, `created_at` y `updated_at`. `status` sigue siendo el workflow principal `DRAFT/REVIEWED/PUBLISHED`. La provenance existente permanece como evidencia de identidad/ficha lógica y no se elimina.

Card abandona `set`, `collector_number`, `cost`, `ram` y `power`: son valores observados de la impresión inicial. `rules_text` se conserva temporalmente en Card, marcado deprecado desde el punto de vista de dominio, porque los cuatro pilotos están vacíos y la evidencia de errata impide afirmar que sea texto vigente o impreso. No se mueve a `printed_rules_text` ni se elimina en 6D.4; su destino se decide en una futura política de contenido/reglas.

### CardPrinting

Contrato mínimo inicial: `card`, `set`, `collector_number`, `cost`, `ram`, `power`, `is_primary`, `printing_label`, `source_name`, `source_url`, `verified_at`, `verification_notes`, `created_at` y `updated_at`.

- `card` y `set`: relaciones obligatorias; el Set actual se conserva literal y no se renombra.
- `collector_number`: texto opcional; mantiene ceros y prefijos.
- `cost`, `ram`, `power`: enteros positivos opcionales, como valores impresos conocidos.
- `printing_label`: `CharField` flexible y opcional (`blank=True`, no enum, no required). Para el piloto migrado queda vacío: “Retail” ya está dentro del nombre literal del Set y separarlo inventaría una taxonomía.
- `is_primary`: booleano con valor inicial verdadero para la única impresión migrada. No hay status editorial propio en la primera versión; se pospone hasta que una Card tenga printings con ciclos de verificación independientes.
- provenance: se copia desde Card a la printing inicial y se conserva también en Card. La nota de migración debe dejar claro que la URL oficial actual identifica la ficha lógica que enumera la impresión, no un ID oficial de printing.

No entran en 6D.4 `rarity`, ilustrador, imágenes, `rules_text` nuevo, idiomas, variantes, enums de labels, ID oficial ni restricciones de negocio de unicidad.

## Traslado de campos y resultado piloto

| Origen actual | Destino | Nullability destino | Valor piloto | Orden de migración | Riesgo |
|---|---|---|---|---|---|
| `Card.set` | `CardPrinting.set` | Obligatorio | Set literal existente | Crear campo → copiar | Taxonomía Set aún abierta; no renombrar. |
| `Card.collector_number` | `CardPrinting.collector_number` | Opcional | 078, 108, 095, 103 | Copiar textual | No asumir unicidad. |
| `Card.cost` | `CardPrinting.cost` | Opcional | 3, vacío, 3, 2 | Copiar | Es valor impreso, no valor vigente. |
| `Card.ram` | `CardPrinting.ram` | Opcional | 2, 2, 3, 2 | Copiar | No inferir invariancia entre printings. |
| `Card.power` | `CardPrinting.power` | Opcional | 2, vacío, 2, vacío | Copiar | Aplicabilidad depende de tipo. |

| Card lógica después de 6D.4 | Slug preservado | Printing inicial | Set | Collector | Cost | RAM | Power |
|---|---|---|---|---|---:|---:|---:|
| Field Operator | field-operator | una, primaria | Welcome to Night City — Retail | 078 | 3 | 2 | 2 |
| Judy Álvarez — Braindance Maestro | judy-alvarez-braindance-maestro | una, primaria | Welcome to Night City — Retail | 108 | VACÍO | 2 | VACÍO |
| Sandevistan | sandevistan | una, primaria | Welcome to Night City — Retail | 095 | 3 | 3 | 2 |
| Take Control | take-control | una, primaria | Welcome to Night City — Retail | 103 | 2 | 2 | VACÍO |

## Printing primaria, identidad y status

Se recomienda **`CardPrinting.is_primary`**. Evita el ciclo de FK que introduciría `Card.primary_printing`, permite crear la estructura y datos en orden natural y mantiene la primary junto a los datos que describe. En 6D.4 la integridad “una primary por Card publicada” se valida mediante data migration, Admin, servicio y tests; no se añade aún una restricción única parcial porque no existe necesidad de introducir complejidad adicional en el piloto. Cuando haya múltiples printings, la edición de primary debe ser transaccional y dejar siempre una printing utilizable antes de retirar la anterior.

La PK interna de Django basta para CardPrinting inicialmente. Para detectar candidatos se podrá comparar Card resuelta + Set literal + collector textual + `printing_label`, pero no se declara clave de negocio única ni `official_printing_id`: ambos siguen sin evidencia suficiente. CardPrinting no necesita slug en 6D.4 porque carece de consumidor/URL pública propia.

## Estrategia expand → migrate → validate → switch → contract

Se recomiendan **tres migraciones conceptuales**, partiendo de `apps.cards.0001_initial`:

1. `0002_cardprinting_expand`: schema. Crea CardPrinting y sus relaciones/campos; mantiene todos los campos actuales de Card.
2. `0003_migrate_cards_to_initial_printings`: data migration con `apps.get_model()`. Para cada Card crea exactamente una printing primaria, transfiere los cinco valores impresos y copia provenance; no cambia name, slug, status ni borra campos antiguos.
3. `0004_cardprinting_contract`: sólo tras una entrega completa de consumidores y validación prolongada. Retira de Card `set`, `collector_number`, `cost`, `ram` y `power`. `rules_text` no se contracta en esta etapa.

La migración de datos usa `apps.get_model()` y el histórico de modelos, no importaciones directas de `models.py`. Debe ser defensiva: antes de crear, buscar exactamente una printing marcada primaria asociada a la Card. Si no existe, crearla; si existe y sus valores coinciden, no duplicar; si existe pero hay divergencia o más de una candidata, abortar con error de revisión. No se establece una unique constraint no respaldada por evidencia oficial.

La validación posterior debe comprobar: número de Cards sin cambios; una printing primaria por cada Card piloto; mismos Set, collector, cost, RAM, power y provenance; slugs/URLs intactos; y cero CardPrintings huérfanas. La migración Django se aplica normalmente una vez, pero estas condiciones hacen segura la re-ejecución controlada del código o una reparación previa al contract.

## Reversibilidad, backup y punto de no retorno

Antes de 6D.4 es obligatorio crear y verificar un backup local con la convención `db.sqlite3.backup_pre_cardprinting_YYYYMMDD_HHMMSS`, fuera de Git, más checksum y registro de la ruta. Este diseño no crea ese backup.

El reverse de `0003` sólo es seguro mientras cada Card tenga una única printing primaria creada por la migración y no existan ediciones posteriores divergentes: repuebla campos antiguos desde esa printing, mantiene Card/name/slug/status y elimina únicamente la printing creada por la transformación. Si hay varias printings o cambios manuales, el reverse debe fallar y exigir restaurar backup; no elegir una por orden. El punto de no retorno es `0004_cardprinting_contract` o cualquier creación/edición posterior de múltiples printings sin snapshot reversible.

| Incidente | Respuesta / rollback |
|---|---|
| Fallo al crear schema | Revertir `0002`; confirmar que no hay tablas/relaciones parciales. |
| Fallo durante data migration | La transacción debe abortar; revisar conteos y restaurar backup si hay duda. |
| Datos incorrectos antes de contract | Corregir sólo tras comparar con backup; reverse lógico sólo si no hay ambigüedad. |
| Error tras cambiar views | Revertir código consumidor primero; mantener estructura expandida hasta validar. |
| Error después de contract | No confiar en reverse automático; restaurar backup y aplicar plan de recuperación probado. |

## Consumidores futuros

`Card.objects.public()` debe seguir filtrar `Card.status=PUBLISHED` y requerir mediante `Exists` al menos una CardPrinting primaria/utilizable, sin N+1. El catálogo consulta Cards lógicas, usa `Exists` para búsqueda/filtro de printings y `Prefetch` filtrado hacia la primary con `select_related('set')`; no une libremente la relación 1:N para renderizar cada tarjeta. El detalle conserva `/choomdex/<slug>/`, carga una Card y su primary; futuras printings se muestran como listado/selector secundario.

La búsqueda por nombre permanece en Card. La búsqueda por collector pasa por CardPrinting; se necesita `distinct()` o, preferiblemente, `Exists` para evitar duplicar Cards. Filtro Set: Card con una printing del Set, también sin duplicados. Filtro Type: directo sobre `Card.card_type`. La paginación continúa siendo de 24 Cards lógicas y debe aplicarse después de ordenar/deduplicar el queryset.

Para Admin se recomienda `CardAdmin` con `CardPrinting` como `TabularInline`, `extra=0`, edición clara de la primary y provenance. Es la opción más simple para el volumen editorial inicial; un admin separado puede añadirse sólo si el número de printings exige búsquedas/filtros masivos.

Deck Builder podrá relacionar `DeckEntry → Card` sin conocer CardPrinting; una elección estética puede ser opcional después. MarketObservation podrá referir CardPrinting sin introducir precio en Card. Si hay autorización futura de imágenes, el asset pertenece normalmente a CardPrinting; hasta entonces se mantienen placeholders y enlaces externos “Fuente oficial” con `target="_blank"` y `rel="noopener noreferrer"`.

## Plan de pruebas de 6D.4

- **Modelo:** Card con varias CardPrintings; FK Card y Set; `PROTECT` según diseño; campos impresos fuera de Card; primary única por regla de servicio; provenance copiada.
- **Migración:** fixture temporal anterior con una Card; resultado una Card + una primary, mismos valores; reverse correcto sólo en caso no ambiguo; aborta en datos inconsistentes.
- **Visibilidad:** DRAFT/REVIEWED no públicas; PUBLISHED pública sólo con primary utilizable; varias printings no duplican Card.
- **Búsqueda/filtros/paginación:** name y collector; filtros combinados Set/Type; sin duplicados; querystring de página preservado; 24 Cards lógicas por página.
- **URLs/UI:** cada slug actual sigue resolviendo; detalle recibe primary; no se exige slug de printing.
- **Regresión:** Admin inline, fuente segura, catálogo, detalle y toda la suite existente.

## Política de fuentes, scraping e ingesta

JorgeCyberpunkTCG no dependerá de scraping de la web oficial. La importación masiva sigue **NO-GO**: no se crearán bots/crawlers ni se redistribuirá masivamente contenido oficial sin autorización. Se prioriza contenido propio —artículos, análisis tácticos, videos, reseñas y herramientas— y las fichas enlazan a la fuente oficial. Una API oficial, dataset autorizado, licencia o permiso expreso permitirían reevaluar el caso; no se implementa fetch remoto ni hotlink de imágenes.

La terminología de roadmap será **“INGESTA CONTROLADA DE DATOS CHOOMDEX — SUSPENDIDA HASTA DISPONER DE FUENTE AUTORIZADA”**, no “importador automático”. Choomdex complementa la base oficial, no intenta reemplazarla.

## Plan ejecutable de 6D.4

| Paso | Archivos / acción | Riesgo | Check | Rollback |
|---|---|---|---|---|
| 0. Backup/preflight | Backup, checksum, status, checks, snapshot SELECT. | Backup inexistente/inválido. | Restore de prueba y 37+ tests. | No iniciar. |
| 1. Expand schema | `models.py`, migración `0002`. | Relación/campos mal definidos. | `makemigrations`, `migrate`, model tests. | Revertir `0002`. |
| 2. Data migration | `0003` con `apps.get_model()`. | Duplicado o pérdida. | Conteos y tabla piloto. | Reverse sólo no ambiguo; si no, backup. |
| 3. Validación | Queries de correspondencia, script de sólo lectura temporal o tests. | Falsa equivalencia. | 1:1, slugs, provenance. | Detener antes de switch. |
| 4. Switch consumers | views, templates, CSS si necesita datos primary. | N+1/duplicados/URLs. | Catalog/detail/search/filter tests. | Revertir código, conservar expand. |
| 5. Admin | admin y pruebas. | Edición de dos primary. | Inline y reglas de primary. | Revertir admin. |
| 6. Tests | modelos, migración, visibilidad, búsqueda, URLs. | Cobertura insuficiente. | Suite completa. | No contractar. |
| 7. Contract schema | `0004` tras periodo validado. | Pérdida irreversible. | Backups y regresión completa. | Restaurar backup. |
| 8. Regresión completa | `check`, migraciones, tests. | Regresión transversal. | Todos OK. | Revertir release/backup. |
| 9. Manual Choomdex | Catálogo, cuatro detalles, búsqueda/filtros. | Diferencia con datos reales. | URLs/primary correctas. | No publicar contract. |
| 10. Git/commit | Diff limitado y commit separado. | Alcance mezclado. | Git limpio. | Revertir commit antes de push. |

## Checklist GO para ejecutar 6D.4

- [x] Backup obligatorio definido.
- [x] Contratos Card y CardPrinting definidos.
- [x] Estrategia `is_primary` definida.
- [x] Traslado de campos y `rules_text` temporal resueltos.
- [x] Data migration, reverse y rollback diseñados.
- [x] URLs, búsqueda, filtros, Admin y tests diseñados.
- [x] Importación masiva sigue NO-GO; scraping descartado; no hay dependencia de imágenes oficiales.
- [ ] Backup real creado/verificado justo antes de ejecutar.
- [ ] Implementación de schema/data migration revisada y tests escritos.
- [ ] Validación del gate Set/product/release/canal aceptada como abierta, sin normalización en 6D.4.

**Decisión: GO CON CONDICIONES** para ejecutar la futura 6D.4. No es autorización para importación masiva ni para resolver taxonomías abiertas durante la migración.
