# Fase 6D.1 — Arquitectura Card vs CardPrinting

## Decisión y evidencia

La recomendación es **GO CON CONDICIONES** para una futura Fase 6D.4 de `CardPrinting`. La evidencia Nivel A muestra que una misma carta visible tiene múltiples printings: Judy Álvarez — Braindance Maestro (4), Field Operator (5), Take Control (2) y Sandevistan (4). Las fichas también asocian a cada printing un Set, número, rareza e ilustrador concretos. [Judy](https://cyberpunktcg.com/cards/judy-a-lvarez-braindance-maestro), [Field Operator](https://cyberpunktcg.com/cards/field-operator), [Take Control](https://cyberpunktcg.com/cards/take-control) y [Sandevistan](https://cyberpunktcg.com/cards/sandevistan) son la evidencia de esta decisión.

No se implementa ningún modelo, migración, URL, dato ni script en esta fase.

## Definiciones propuestas

- **Card:** identidad lógica y editorial de juego que Choomdex muestra una vez, independientemente de cuántas impresiones verificadas tenga. No se presupone un ID lógico oficial: el identificador local será estable y la equivalencia se decidirá editorialmente con evidencia.
- **CardPrinting:** una aparición concreta y verificable de esa identidad en un Set/producto publicado. Es el lugar de los valores impresos y de la procedencia específica.
- **Set:** agrupación oficial que la fuente presenta como producto o edición para una impresión. Por ahora debe conservar su etiqueta oficial literal, por ejemplo “Welcome to Night City — Retail”; no se infiere aún una taxonomía separada de release, canal o producto padre.

La palabra “misma” Card no puede depender sólo del nombre. La propuesta inicial de identidad es una resolución editorial basada en nombre canónico, CardType y evidencia de identidad de juego/reglas; un cambio de nombre visible, reglas o atributos requiere revisión, no una regla automática ni una restricción única. Un futuro ID oficial, si se verifica, podría ser una clave de conciliación, no se inventa ahora.

## Matriz de responsabilidades

| Campo | Card | CardPrinting | Set | Futuro / estado | Justificación |
|---|---|---|---|---|---|
| `name` | Canónico editorial | Posible nombre impreso/localizado | — | PENDIENTE | La ficha actual muestra título, pero no confirma invariancia entre idiomas o versiones. |
| `slug` | Sí, URL lógica estable | Posible slug secundario | Sí | POSIBLE | Mantiene SEO de la identidad; no fijar URL de printing aún. |
| `set` | — | Sí | Entidad propia | CONFIRMADO | La misma Card aparece en más de un Set/producto. |
| `card_type` | Sí, salvo evidencia de cambio | Copia histórica sólo si hiciera falta | — | CONFIRMADO | Tipo identifica la carta en las fichas; no hay evidencia del piloto de cambio por printing. |
| `status` | Sí, estado editorial público | Opcional, estado de verificación de impresión | — | CONFIRMADO/POSIBLE | No confundir `DRAFT/REVIEWED/PUBLISHED` con estado oficial del producto. |
| `collector_number` | — | Sí, texto | — | CONFIRMADO | Depende del Set y conserva ceros/formato; no imponer unicidad global. |
| `cost`, `ram`, `power` | Valor actual sólo si se verifica política | Valor impreso | — | POSIBLE | El piloto sólo prueba valores impresos; errata/versiones pueden diferenciarlos. |
| `rules_text` | Texto actual/oracle, si se aprueba | Texto impreso, si se aprueba | — | PENDIENTE | Separar reglas vigentes, impresas y errata; se mantiene política conservadora de copyright. |
| `source_name`, `source_url`, `verified_at`, `verification_notes` | Identidad/errata | Claim de printing | Datos de Set | CONFIRMADO | La procedencia vive donde vive el hecho; puede coexistir en los tres niveles. |
| `created_at`, `updated_at` | Sí | Sí | Sí | CONFIRMADO | Auditoría local de cada registro, no fecha oficial. |
| rarity | — | Sí | — | CONFIRMADO | La fuente la muestra por ficha/printing; no se implementa. |
| artist / illustrator | — | Sí | — | CONFIRMADO | Puede variar con alternate art; no se implementa. |
| image / art reference | — | Sí, si licencia lo permite | — | POSIBLE | Arquitectónicamente pertenece a la impresión; derechos son una decisión independiente. |
| variant / finish / foil | — | Campo simple o hija sólo si hay varios valores verificables | — | PENDIENTE | No sobre-modelar antes de ver datos oficiales estructurados. |
| printing label | — | Sí, o relación al Set literal | Sí, etiqueta oficial | PENDIENTE | Retail/Beta/Starter/Demo/Pre-Release pueden mezclar producto, distribución y variante. |
| language | — | Sí | — | PENDIENTE | La impresión puede cambiar idioma y título visible. |
| release date | — | Posible disponibilidad de impresión | Posible fecha de Set/release | PENDIENTE | Requiere definición oficial del nivel al que aplica. |
| promo / beta / retail / starter deck / pre-release | — | Posible clasificación | Posible etiqueta del Set | PENDIENTE | Registrar literal primero; taxonomía sólo con fuente suficiente. |
| alternate art / full art | — | Sí | — | POSIBLE | Es una propiedad de representación de una impresión/variante. |
| keywords, subtypes, traits, factions, colors | Identidad/reglas actuales si se normalizan | Snapshot impreso sólo si es necesario | — | PENDIENTE | Vocabulario oficial y política de versionado aún no están cerrados. |
| RAM/color identity | Card, si es regla actual | Snapshot impreso si difiere | — | PENDIENTE | La guía asocia RAM a Legends; falta decidir tratamiento de cambios. |
| rules text version / errata | Referencia a regla vigente futura | Versión impresa | — | PENDIENTE | Mejor entidad/versionado de reglas si se vuelve necesario. |
| oracle/current rules text | Sí, o futura `RulesRevision` | — | — | PENDIENTE | No cargar ni reproducir texto hasta resolver licencia y política. |
| precio / mercado | — | Referencia de observación | — | FUTURO | `MarketObservation` debe depender además de condición, moneda, región y fecha. |

## Análisis de campos clave

**CardType.** Debe residir en Card por defecto: es parte de la identidad de juego observada en las fichas. CardPrinting sólo conserva un snapshot si una futura fuente demuestra cambios o necesita reconstrucción histórica.

**Cost, RAM y Power.** Los datos del piloto son valores impresos y por tanto pertenecen inicialmente a CardPrinting. No debe suponerse que son eternamente idénticos entre reimpresiones o errata. Si se requiere un valor para juego actual, será un campo de Card respaldado por una política de reglas vigente, o preferiblemente una futura revisión de reglas; no se debe sobrescribir el valor impreso.

**Rules text.** `CardPrinting.printed_rules_text` y una regla vigente de Card son conceptos distintos. Una futura `RulesRevision` sólo se justifica si errata/oracle requieren historia y fuentes. No se copia texto oficial en esta fase.

**Set y collector number.** `Card.set` debe migrar conceptualmente a `CardPrinting.set`. `collector_number` pertenece claramente a CardPrinting, permanece textual y su unicidad, si se verifica, será como máximo dentro del contexto de Set y una clasificación de printing; no se implementa ninguna restricción aún.

**Rarity, illustrator e imágenes.** Rareza e ilustrador son propiedades de CardPrinting. Una imagen también lo sería técnicamente porque puede variar por arte o acabado; eso no concede permiso de reutilización, hotlink ni almacenamiento. La licencia se decide de forma separada.

**Variantes y etiquetas.** `Variant`, finish, foil, promo y alternate art no ameritan entidad propia por ahora. La opción mínima futura es un campo de CardPrinting documentado con valores oficiales; una entidad hija sólo se evaluará si una misma impresión tiene múltiples combinaciones comercialmente distintas. Las etiquetas Retail, Beta, Starter Deck, Demo Deck y Pre-Release deben conservarse literalmente hasta verificar si representan Set, producto, canal, etapa o una combinación.

**Status y procedencia.** `DRAFT`, `REVIEWED` y `PUBLISHED` son workflow editorial local de Card y controlan el catálogo público. CardPrinting podría tener un estado de verificación independiente para permitir que una Card esté publicada con una printing primaria aprobada mientras otras siguen internas. Cada claim impreso (número, artista, rareza, imagen) debe tener procedencia en CardPrinting; hechos de Set en Set; identidad, errata o regla vigente en Card o su futura revisión.

## Catálogo, detalle, URLs y consumidores futuros

El catálogo público debe listar **una Card lógica por entrada** con una printing primaria verificada que aporte sus datos tácticos. Así evita duplicados, preserva búsqueda por nombre y favorece el futuro Deck Builder. La ficha de Card conserva `/choomdex/<slug>/`, presenta la información vigente/primaria y en el futuro lista o permite seleccionar printings; una URL anidada de impresión es posible, no está decidida ni se necesita para el MVP.

Un deck debe referenciar Card lógica para que dos copias con arte o printing distinto no alteren la identidad de juego. Una elección de colección/cosmética podría enlazar a CardPrinting por separado si el producto la necesita. El mercado debe referirse a CardPrinting y, previsiblemente, a una futura observación que incluya variante, condición, moneda, región, fecha y fuente; nunca a un precio único de Card.

## Migración conceptual del piloto y retrocompatibilidad

Para los cuatro registros piloto —Judy Álvarez — Braindance Maestro, Field Operator, Take Control y Sandevistan— una futura migración debe: (1) crear una Card lógica por identidad editorial revisada; (2) crear una CardPrinting por cada registro actual y enlazarla al Set ya registrado; (3) mover número, atributos impresos, procedencia de la ficha y cualquier texto impreso hacia CardPrinting; (4) conservar en Card el slug histórico y el estado editorial; (5) registrar la procedencia de la transformación; y (6) marcar la printing como primaria sólo tras revisión.

La URL actual de detalle debe seguir resolviendo a la Card lógica. La migración no debe reutilizar el slug para una printing ni crear redirects hasta contar con una estrategia de URL, pruebas de compatibilidad y un plan de reversión. Con sólo una printing por Card piloto, la experiencia actual puede preservarse sin ambigüedad.

## Modelo conceptual mínimo

```text
Set 1 ── * CardPrinting * ── 1 Card
                         └── (futuro) MarketObservation
Card ── (futuro, sólo si hace falta) RulesRevision
```

| Entidad | Responsabilidad | Relaciones / restricciones conceptuales | Pospuesto explícitamente |
|---|---|---|---|
| Set | Etiqueta y evidencia del producto/edición oficial. | Un Set tiene muchas CardPrintings; conservar nombre oficial literal. | Release padre, canal y taxonomía de productos. |
| Card | Identidad lógica, slug público, CardType y workflow editorial. | Una Card tiene una o más CardPrintings; una primaria publicada para catálogo cuando exista. | ID oficial, reglas/oracle versionadas, taxonomías de juego. |
| CardPrinting | Hecho impreso verificable en un Set. | Pertenece a una Card y un Set; número textual, valores impresos y provenance específica. | Variant hija, imágenes, rareza, artista, idioma y restricciones de unicidad hasta verificarlos. |

## Matriz de confianza

| Concepto | Evidencia | Confianza | Decisión |
|---|---|---|---|
| Una Card tiene múltiples printings. | Las cuatro fichas oficiales enumeran 2–5 printings. | ALTA | Introducir CardPrinting en fase futura, no ahora. |
| Número, Set, rareza e ilustrador son datos de printing. | Cada ficha los presenta junto a una printing concreta y hay múltiples printings. | ALTA | Situarlos en CardPrinting. |
| CardType es identidad lógica estable. | Tipos canónicos oficiales y sin cambio observado en piloto. | MEDIA | Mantener en Card, snapshot opcional si se necesita historia. |
| Cost/RAM/Power son invariantes entre printings. | Un piloto pequeño no prueba invariancia ni errata. | BAJA | Guardar primero como printed values; no derivar valor actual. |
| Retail/Beta/Starter/Demo/Pre-Release son una sola taxonomía. | Las etiquetas oficiales combinan varios términos. | BAJA | Conservar literal en Set/printing y posponer normalización. |
| Nombre visible es identidad suficiente. | No hay ID lógico oficial ni evidencia de localizaciones/versiones. | BAJA | Resolver identidad editorialmente; no imponer unicidad. |
| Imágenes oficiales pueden reutilizarse. | No se ha revisado licencia de uso. | BAJA | Mantener placeholders propios. |

## Gate antes de una migración

1. Confirmar y documentar el criterio editorial de identidad de Card y el manejo de nombres/errata.
2. Verificar al menos el contexto de unicidad de `collector_number` y los labels oficiales de cada printing.
3. Definir qué representa Set frente a producto/release/canal sin normalizar prematuramente.
4. Decidir la fuente y política para atributos impresos frente a reglas actuales, incluyendo copyright y errata.
5. Diseñar la estrategia de URL: slug de Card estable, detalle de printings y retrocompatibilidad.
6. Auditar impacto en consultas públicas, Admin, filtros, tests, Deck Builder y futuro mercado.
7. Preparar una migración reversible y plan de datos para el piloto, con conservación de provenance y sin pérdida de slugs.

Hasta cumplir estos gates, no se implementa `CardPrinting` ni se realiza carga masiva.
