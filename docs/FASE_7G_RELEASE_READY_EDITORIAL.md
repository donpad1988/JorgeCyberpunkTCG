# Fase 7G — Release-Ready Editorial

## Contexto y auditoría

Cyberpunk TCG está en pre-lanzamiento; los cuatro Cards, cuatro CardPrintings y el Deck local son datos piloto para validar software, no contenido definitivo. `is_public` sólo expresaba acceso de visitante. Article usa `DRAFT/PUBLISHED` con fecha; Card usa `DRAFT/REVIEWED/PUBLISHED`; Video usa `is_active`. Deck necesitaba un ciclo editorial propio porque su vigencia no es igual a privacidad ni a disponibilidad de una Card.

## Workflow elegido

`Deck.editorial_status` usa el MVP independiente `DRAFT`, `PUBLISHED`, `ARCHIVED`, con default seguro `DRAFT`. `is_public` no se elimina: controla intención de acceso; el status controla preparación y vigencia.

| Estado + visibilidad | Política |
|---|---|
| DRAFT, público o privado | Sólo owner; no aparece en biblioteca, Video ni SEO. |
| PUBLISHED + público | Visible en detalle y biblioteca; indexable. |
| PUBLISHED + privado | Sólo owner. |
| ARCHIVED + público | URL permanente accesible como contenido histórico; queda en archivo separado, no como recomendación vigente, y `noindex`. |
| ARCHIVED + privado | Sólo owner. |

Owner puede cambiar el status desde metadata sin state machine. Builder permanece disponible para owner en los tres estados, de forma que un archivo puede corregirse o restaurarse sin bloqueo irreversible. Admin muestra y filtra el status. `DeckEditorialProfile`, `DeckKeyCard`, composición y slug no cambian al archivar.

## Presentación y relaciones

Un Deck archivado muestra aviso textual de archivo táctico. La biblioteca pública prioriza sólo `PUBLISHED`; los archivados públicos se muestran en una sección histórica separada. Video detail incluye Decks `PUBLISHED` y `ARCHIVED` públicos —estos últimos con badge histórico— para conservar contexto de vídeos antiguos. Nunca muestra Drafts ni privados. Deck detail sigue mostrando sólo Videos activos.

La URL `/mazos/<username>/<slug>/` no cambia al archivar. DRAFT y ARCHIVED se sirven con `noindex, nofollow`; PUBLISHED público mantiene indexación normal. No existe sitemap que ampliar y Home no promociona mazos.

## Compatibilidad de datos y lanzamiento

Deck sigue apuntando a `Card` lógica, nunca a `CardPrinting`; por tanto, cambios de coste, RAM, poder, collector o Set pueden revisarse en printings sin reescribir composición. Card conserva identidad lógica, CardPrinting representa una impresión y Set mantiene literalidad verificable. No se fusionan Cards ni se reconcilian datos automáticamente.

Los campos `source_name`, `source_url`, `verified_at` y notas conservan procedencia. `verified_at` significa “verificado contra la fuente indicada en esa fecha”, no validez perpetua. No hay scraping, API, importador ni sobrescritura automática.

Procedimiento conceptual de octubre de 2026: congelar cambios editoriales, revisar fuentes oficiales, comparar taxonomía, identificar Cards lógicas y printings, verificar Sets/valores/procedencia, revisar Decks piloto, archivar los obsoletos, crear fichas definitivas y asociar Videos nuevos. Si cambia sólo una impresión, conservar Card y revisar CardPrinting; si cambia la identidad, decidir manualmente; si cambia Set/taxonomía, preservar literalidad histórica y reconciliar manualmente.

## Verificación y límites

La migración `decks.0003_deck_editorial_status` no realiza migración de datos: el Deck existente queda como Draft seguro y se conserva íntegro. Tests cubren default, matriz completa de visibilidad, workflow owner-only, aviso histórico, biblioteca y Video↔Deck. RAM permanece `NOT_EVALUATED`; Choomdex, Cards, CardPrintings, Sets, Builder, imágenes y contenido externo no se modifican.

Pendiente: 7H para descubrimiento público y 7I para integración editorial transversal. No se inicia automáticamente ninguna.
