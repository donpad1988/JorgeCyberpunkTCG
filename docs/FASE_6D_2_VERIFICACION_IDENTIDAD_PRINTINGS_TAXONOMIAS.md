# Fase 6D.2 — Verificación de identidad, printings y taxonomías

## Alcance, clasificación y fuentes

Esta fase sólo investiga y documenta. No se modificaron modelos, datos, base de datos, tests, migraciones ni código. **CONFIRMADO** significa que una fuente oficial lo expresa o muestra; **INFERENCIA FUERTE** es una conclusión de arquitectura respaldada por esa evidencia; **PENDIENTE** y **NO VERIFICADO** no autorizan implementación.

| Fuente | Naturaleza | Uso en esta fase |
|---|---|---|
| [Base oficial de cartas](https://cyberpunktcg.com/cards) | Nivel A, catálogo navegable | Agrupación de fichas, filtros y datos visibles. |
| [Gameplay Guide](https://cyberpunktcg.com/gameplay-guide) | Nivel A, guía oficial | Tipos, coste, RAM, power, keywords y límites de copias. |
| [Errata oficial](https://cyberpunktcg.com/errata) | Nivel A, política oficial de texto | Distinguir texto impreso de texto vigente y correcciones. |
| [Judy](https://cyberpunktcg.com/cards/judy-a-lvarez-braindance-maestro), [Field Operator](https://cyberpunktcg.com/cards/field-operator), [Take Control](https://cyberpunktcg.com/cards/take-control), [Sandevistan](https://cyberpunktcg.com/cards/sandevistan) | Nivel A, casos piloto | Printings, labels, números, Set, rareza e ilustrador. |
| [FAQ oficial](https://cyberpunktcg.com/faq) | Nivel A, FAQ de producto | Diferencia entre productos Kickstarter/Beta, Retail, Starter Deck y variantes de arte. |
| [Terms of Service](https://cyberpunktcg.com/terms-of-service) | Nivel A, términos | Restricciones antes de automatizar ingesta. |

`robots.txt` y una API/dataset oficial documentado no se localizaron mediante esta consulta puntual. La referencia visible a Netdeck como proveedor de la base tampoco es autorización para consumir una API ni prueba de un endpoint público.

## Los siete gates de 6D.1 — estado antes de 6D.2

| Gate | Pregunta | Estado antes de 6D.2 | Evidencia necesaria |
|---|---|---|---|
| 1. Confirmar y documentar el criterio editorial de identidad de Card y el manejo de nombres/errata. | ¿Cómo se determina una Card lógica sin inventar ID oficial? | ABIERTO | Fichas que agrupen printings y política oficial de errata/nombres. |
| 2. Verificar al menos el contexto de unicidad de `collector_number` y los labels oficiales de cada printing. | ¿Número y labels identifican una impresión? | ABIERTO | Múltiples printings oficiales comparables. |
| 3. Definir qué representa Set frente a producto/release/canal sin normalizar prematuramente. | ¿Cuál es la semántica de Retail/Beta/Starter/Demo/Pre-Release? | ABIERTO | Taxonomía oficial expresa. |
| 4. Decidir la fuente y política para atributos impresos frente a reglas actuales, incluyendo copyright y errata. | ¿Cómo se almacenan/revisan datos impresos y vigentes? | ABIERTO | Guía, errata y condiciones de uso. |
| 5. Diseñar la estrategia de URL: slug de Card estable, detalle de printings y retrocompatibilidad. | ¿Cómo conservar `/choomdex/<slug>/`? | ABIERTO | Decisión de UX y arquitectura. |
| 6. Auditar impacto en consultas públicas, Admin, filtros, tests, Deck Builder y futuro mercado. | ¿Qué consumidores cambian? | ABIERTO | Análisis del MVP actual y reglas oficiales. |
| 7. Preparar una migración reversible y plan de datos para el piloto, con conservación de provenance y sin pérdida de slugs. | ¿Cómo transformar los cuatro registros sin pérdida? | ABIERTO | Mapeo de campos y estrategia técnica posterior. |

## Identidad lógica y cuatro casos piloto

La página oficial de cada caso agrupa explícitamente varias entradas bajo un único título, tipo y URL. Esto es **CONFIRMADO** como evidencia de agrupación de catálogo y una **INFERENCIA FUERTE** de que hay una identidad lógica útil para Choomdex. No se expone un `official_card_id`/UUID/printing ID público verificable en las fichas revisadas; el slug/URL es un identificador de navegación, no una clave oficial documentada.

| Card lógica mostrada | URL oficial | Printings visibles | Labels y collector numbers observados | Igualdad / cambio verificable |
|---|---|---:|---|---|
| Judy Álvarez — Braindance Maestro | `/cards/judy-a-lvarez-braindance-maestro` | 4 | Welcome to Night City — Retail `108`; Welcome to Night City — Beta `β108`; Welcome to Night City — Beta `β157`; Pre-Release Beta `010` | Mismo título/tipo en la ficha; cambian labels, números y el listado muestra más de un ilustrador. |
| Field Operator | `/cards/field-operator` | 5 | Welcome to Night City — Retail `078`; Welcome to Night City — Beta `β078`; Embracing Power — Retail Starter Deck `016`; Embracing Power — Beta Starter Deck `β016`; Arasaka Demo Deck `012` | Mismo título/tipo en la ficha; cambian labels y números. |
| Take Control | `/cards/take-control` | 2 | Welcome to Night City — Retail `103`; Welcome to Night City — Beta `β103` | Mismo título/tipo en la ficha; cambia label/número. |
| Sandevistan | `/cards/sandevistan` | 4 | Welcome to Night City — Retail `095`; Welcome to Night City — Beta `β095`; Embracing Power — Retail Starter Deck `019`; Embracing Power — Beta Starter Deck `β019` | Mismo título/tipo en la ficha; cambian labels y números. |

La fuente pública revisada muestra valores de la ficha lógica, pero no ofrece en su texto extraído una comparación de coste, RAM y power para cada printing. Por tanto, su igualdad entre printings es **PENDIENTE**; no se deduce de los cuatro casos.

## Card, CardPrinting, Set y taxonomías

**Card = identidad lógica/jugable** es una **INFERENCIA FUERTE**: agrupa los printings que el catálogo oficial presenta bajo una ficha. La resolución editorial futura debe usar título canónico, CardType, URL/ficha agrupadora y evidencia de reglas; nunca sólo el nombre. **CardPrinting = manifestación física/editorial concreta** es **CONFIRMADO** en lo mínimo: labels/números múltiples pertenecen a entradas listadas bajo esa ficha. **Set** queda **PENDIENTE** como taxonomía definitiva: la fuente escribe “SET: Welcome to Night City — Retail”, mientras la FAQ distingue productos Kickstarter/Beta de productos retail y Starter Decks. Esto prueba etiquetas de producto, no que “Retail” sea una entidad semántica universal.

| Concepto | Término oficial / evidencia | Entidad propuesta | Estado | Confianza |
|---|---|---|---|---|
| CardType | LEGEND, UNIT, PROGRAM, GEAR en guía y fichas | Card | CONFIRMADO | ALTA |
| Set | Campo `SET` de ficha; “Welcome to Night City — Retail” | Set literal ligado a CardPrinting | CONFIRMADO para etiqueta; PENDIENTE para taxonomía | MEDIA |
| Printing label | Retail, Beta, Retail Starter Deck, Beta Starter Deck, Demo Deck, Pre-Release Beta | `CardPrinting.printing_label` texto flexible inicial | CONFIRMADO como labels | ALTA |
| Collector number | `078`, `β078`, `016`, etc. bajo cada label | CardPrinting, texto | CONFIRMADO | ALTA |
| Rarity | Campo `RARITY` visible | CardPrinting | CONFIRMADO como dato visible; cambio entre printings PENDIENTE | MEDIA |
| Illustrator | Campo `ILLUSTRATED BY`; Judy lista ilustradores distintos | CardPrinting | CONFIRMADO | ALTA |
| Cost | Campo/guía oficial; cada ficha lógica lo muestra si aplica | Valor impreso en CardPrinting; actual futuro separado | CONFIRMADO/PENDIENTE | MEDIA |
| RAM | Campo/guía oficial; límite por color de Legends | Valor impreso en CardPrinting; identidad/juego actual pendiente | CONFIRMADO/PENDIENTE | MEDIA |
| Power | Campo/guía oficial y aplicable a combate | Valor impreso en CardPrinting | CONFIRMADO/PENDIENTE | MEDIA |
| Keywords | Guía distingue keywords y timing triggers | Card lógica/reglas vigentes, si se modela | CONFIRMADO como concepto; por carta PENDIENTE | MEDIA |
| Subtypes / traits | Fichas muestran textos adicionales, sin esquema formal revisado | PENDIENTE | PENDIENTE | BAJA |
| Colors | Guía habla de valores de RAM por color | Card/reglas vigentes, snapshot opcional | CONFIRMADO como concepto | MEDIA |
| Factions | No se verificó taxonomía oficial separada de color | — | NO VERIFICADO | BAJA |
| Variant / alternate art | FAQ confirma art variants exclusivas de producto Beta | CardPrinting inicialmente | CONFIRMADO como concepto; granularidad PENDIENTE | MEDIA |
| Promo | FAQ describe una carta promocional/bonus y foil/non-foil | CardPrinting/label flexible | CONFIRMADO como concepto; taxonomía PENDIENTE | MEDIA |
| Full art | No se verificó término oficial en las fuentes revisadas | — | NO VERIFICADO | BAJA |

La opción mínima es `printing_label` flexible en CardPrinting, no enums ni entidad Variant. Una entidad hija se considera sólo si la fuente futura muestra múltiples variantes comercialmente distintas bajo una misma combinación de Card, Set y número.

## Número, atributos, reglas, arte y estado

`collector_number` pertenece a CardPrinting: los casos oficiales lo cambian con el label/producto y conserva formatos no enteros (`β078`) y ceros iniciales. La conclusión es **CONFIRMADO** para pertenencia de impresión; la unicidad por Set o por combinación no está demostrada y queda **PENDIENTE**. No se crea restricción.

Coste, RAM y power son **CONFIRMADOS** como conceptos oficiales. Coste es el valor de juego para jugar una carta; power aplica a combate; RAM se relaciona con límites por color de Legends. En arquitectura, los valores visibles deben tratarse como `printed_*` de CardPrinting. `Card.gameplay_cost`, `gameplay_ram` o `gameplay_power` sólo se justifican después de definir una fuente vigente; no hay evidencia de que los cuatro casos sean inmutables entre printings. El valor actual/oracle queda **PENDIENTE**.

La [página de errata](https://cyberpunktcg.com/errata) confirma que existe texto impreso, correcciones y características actualizadas que sustituyen el texto impreso durante juego. Por ello `printed_rules_text`, `current_rules_text`, `errata` y `rulings` son conceptos arquitectónicamente distintos; sólo errata y la regla actual superadora están **CONFIRMADOS** como política. No se copia texto de reglas. La guía confirma keywords y timing triggers como conceptos formales; su presencia y cardinalidad por Card sigue **PENDIENTE**.

Rareza e ilustrador aparecen oficialmente. El caso Judy muestra que el listado de printings puede asociar ilustradores distintos, por lo que ilustrador pertenece a CardPrinting. La rareza debe modelarse también por printing hasta que se demuestre lo contrario. Las fichas muestran arte y la FAQ confirma variantes de arte para Beta; arquitectónicamente la representación visual pertenece a CardPrinting. El uso de imágenes oficiales continúa **PENDIENTE DE DECISIÓN LEGAL/POLÍTICA**.

`DRAFT`, `REVIEWED` y `PUBLISHED` permanecen como workflow editorial local de Card. Una futura verificación por CardPrinting puede ser independiente, pero no debe representar disponibilidad oficial del producto.

## Deduplicación e importador futuro

La identidad ideal sería un identificador oficial estable de Card y otro de CardPrinting, pero no se verificó uno. El importador futuro debe usar una cola de revisión, nunca una clave de nombre sola.

| Clave candidata | Uso | Clasificación | Riesgo |
|---|---|---|---|
| ID oficial de Card / printing, si se documenta | Clave ideal | NO VERIFICADO | No se expone en las páginas revisadas. |
| URL/slug oficial de ficha + CardType + revisión editorial | Card fallback | INFERENCIA FUERTE | Slug podría cambiar y no es ID oficial documentado. |
| Card resuelta + label literal + Set literal + collector_number textual | Printing fallback | INFERENCIA FUERTE | No se ha probado unicidad universal. |
| Nombre solo | Señal de candidato | NO RECOMENDADO | Colisiones, localización o cambio de nombre. |

| Caso de importación | Política conceptual |
|---|---|
| A. Nueva Card lógica | Crear sólo tras no encontrar coincidencia por clave ideal/fallback y revisión de identidad. |
| B. Card existente + nueva CardPrinting | Crear printing candidata con provenance y revisión humana. |
| C. Printing existente sin cambios | Marcar `UNCHANGED`, actualizar sólo `source_last_seen_at` futuro. |
| D. Printing existente con datos modificados | `UPDATE CANDIDATE`; no sobrescribir valor verificado silenciosamente. |
| E. Registro ambiguo | `REVIEW REQUIRED`; no crear ni fusionar. |

Cada lote futuro debe registrar fuente, URL, fecha/hora de verificación, notas, identificador fuente si existe, última vez visto e identificador de lote. Debe ofrecer obligatoriamente `--dry-run` que informe Cards nuevas, Printings nuevas, sin cambios, cambios detectados, ambiguos y errores. La idempotencia requiere persistir claves verificadas y comparar normalizaciones controladas: ejecutar el mismo dataset dos veces no debe duplicar Set, Card ni CardPrinting.

La fuente oficial ofrece un catálogo navegable y filtros, pero no se verificó API o feed documentado. Los [términos](https://cyberpunktcg.com/terms-of-service) prohíben copiar/redistribuir contenido sin permiso escrito y usar bots o herramientas de scraping para extraer datos. En consecuencia, la jerarquía futura es: API/dataset oficial autorizado; luego fuente estructurada pública explícitamente autorizada; después carga manual/semiautomática autorizada. HTML scraping queda fuera hasta revisión técnica, de términos y permiso expreso.

## Deck Builder, mercado, piloto y URLs

La guía oficial limita a tres copias de “the same card” y exige Legends de nombres únicos; no menciona printings en esa regla. Por tanto, que Deck Builder refiera Card lógica es una **INFERENCIA FUERTE** y la opción más coherente para límites de copias, pendiente de una interpretación oficial más específica. Mercado debe referir CardPrinting y, si procede, variante/finish, condición, moneda, región, fecha y fuente.

| Campo actual del piloto | Card futuro | CardPrinting futuro | Set futuro | Acción / riesgo |
|---|---|---|---|---|
| `name`, `slug`, `card_type`, `status` | Sí | snapshot sólo si se necesita | — | Conservar slug y workflow editorial; resolver identidad manualmente. |
| `set` | — | Relación sí | Conservar registro literal | Mover relación; no reinterpretar Retail/Beta. |
| `collector_number`, `cost`, `ram`, `power` | — | Valores impresos | — | Mover sin convertir a entero; valor actual pendiente. |
| `rules_text` | Regla actual futura, si se autoriza | Texto impreso futuro, si se autoriza | — | Piloto vacío: no inventar ni copiar. |
| provenance y timestamps | Hechos de identidad | Hechos impresos | Hechos de Set | Duplicar/particionar trazabilidad con nota de transformación. |

`/choomdex/` debe mostrar una Card lógica por entrada con una printing primaria verificada. `/choomdex/<card-slug>/` conserva su rol y slug actual; más adelante puede listar printings sin forzar una URL de printing. La futura migración debe ser reversible, preservar URLs/provenance y probar que no pierde los cuatro slugs piloto.

## Los siete gates de 6D.1 — estado después de 6D.2

| Gate | Estado después de 6D.2 | Decisión | Evidencia | Riesgo residual |
|---|---|---|---|---|
| 1. Criterio de identidad y nombres/errata | CERRADO CON CONDICIONES | URL/ficha agrupadora + tipo + revisión editorial; no nombre solo. | Fichas agrupadas y errata oficial. | No hay ID oficial ni política completa de nombres/localización. |
| 2. Contexto de número y labels | CERRADO CON CONDICIONES | Número es de printing textual; labels se guardan literales. | Cuatro casos con múltiples números/labels. | Unicidad universal no probada. |
| 3. Set frente a producto/release/canal | ABIERTO | Conservar etiquetas literales; no normalizar taxonomía. | Fichas y FAQ distinguen productos, no un modelo formal. | Riesgo de clasificar mal Retail/Beta/Starter. |
| 4. Atributos impresos/reglas actuales/copyright | CERRADO CON CONDICIONES | Printed values en printing; regla vigente/errata separada; no copiar contenido. | Guía, errata y Terms. | Falta política/permiso de contenido y modelo de revisiones. |
| 5. URLs y retrocompatibilidad | CERRADO CON CONDICIONES | Mantener slug de Card y añadir printings dentro del detalle primero. | Decisión de UX documentada. | Sin URL definitiva de printing ni redirects. |
| 6. Impacto en consumidores | CERRADO CON CONDICIONES | Card para catálogo/Deck Builder; printing para mercado; auditar implementación en 6D.3. | Modelo actual, guía y análisis. | Faltan diseño técnico y tests de migración. |
| 7. Plan reversible del piloto | CERRADO CON CONDICIONES | Particionar campos, conservar slug/status/provenance y probar reversión. | Matriz de piloto anterior. | Falta migración concreta y ensayo en base desechable. |

## Gate separado: importación masiva del catálogo oficial

**NO-GO.** Permanece bloqueada hasta tener Card/CardPrinting estable, estrategia de identidad y deduplicación, fuente aprobada, política de actualización, `--dry-run`, idempotencia, revisión de uso de datos/contenidos y tests. Los términos oficiales impiden tratar el catálogo HTML como fuente automatizable por defecto.

## Decisión para 6D.3

**GO CON CONDICIONES** para diseñar una migración controlada, no para ejecutarla. Puede avanzar sólo con el mantenimiento de etiquetas literales de Set/printing, una migración reversible de los cuatro registros, pruebas de compatibilidad de slug/provenance y sin automatizar ingesta. La taxonomía formal de productos y cualquier importador masivo siguen fuera de alcance.
