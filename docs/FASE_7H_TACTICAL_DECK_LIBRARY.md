# Fase 7H — Tactical Deck Library

## Objetivo y contexto

`/mazos/publicos/` pasa de listado CRUD a puerta pública de Tactical Deck Files: descubrir, entender, abrir el análisis, navegar a Video y explorar Cards en Choomdex. No compite con el Builder oficial. Los datos actuales siguen siendo piloto pre-lanzamiento; la biblioteca funciona intencionalmente aun sin Decks publicados y no crea contenido ficticio.

## UX pública

La página presenta un encabezado compacto de **Biblioteca táctica de mazos**, búsqueda SSR por GET y una colección de análisis actuales. Las tarjetas muestran únicamente datos existentes: nombre, arquetipo y resumen cuando existen, autor, Legends reales, suma MAIN real, indicador discreto de Video activo y CTA explícito hacia `Deck.get_absolute_url()`. No convierte la tarjeta completa en enlace ni muestra ruido por campos vacíos.

El estado vacío usa copy editorial y enlaces funcionales a Guías, Videos y Choomdex. Si una búsqueda no encuentra resultados, muestra un mensaje distinto y acción para limpiarla. Drafts y privados no se incluyen en queryset, HTML ni payload.

## Visibilidad, archivo y navegación

La biblioteca reutiliza los selectores `Deck.objects.public_current()` y `Deck.objects.public_archive()` para conservar la política 7G. `PUBLISHED + is_public` es la colección vigente. `ARCHIVED + is_public` aparece sólo en una sección secundaria **Archivo histórico**, con badge textual y explicación; no se mezcla como recomendación actual. Drafts no aparecen nunca.

El Tactical Deck File incorpora enlace de retorno a la biblioteca. Conserva enlaces a Choomdex y el CTA de Video de 7F. Home y navbar ya usan “Mazos” y no requirieron cambio. Usuarios autenticados mantienen `Mis mazos`; owner conserva los controles del detalle.

## Búsqueda, orden y rendimiento

`?q=` consulta nombre, arquetipo y resumen corto, no estrategia completa. No existen filtros por arquetipo, facción, RAM, formato, Set, rankings o metajuego. Publicados se ordenan por `updated_at DESC, name`; se pagina a 12 por página conservando `q`. Archivados permanecen completos en la sección secundaria hasta que el volumen real justifique otra política.

La vista anota Legends mediante `Count(distinct=True)`, MAIN con subconsulta `Sum(quantity)` y disponibilidad de Video mediante `Exists`; evita ejecutar `DeckValidationService` o consultas por tarjeta. Usa `select_related` para owner y perfil.

## SEO, accesibilidad y límites

La biblioteca tiene título/meta description propios e indexables. Las búsquedas no reciben infraestructura SEO adicional; no se implementa canonical ni sitemap. Cada Deck archivado conserva la política `noindex, nofollow` de 7G. HTML usa `header`, `section`, `article`, `form`, labels y headings jerárquicos; el buscador es `type=search`, las acciones tienen texto y el layout se apila en móvil.

No se añadieron migraciones, Cards, CardPrintings, Sets, Videos reales, imágenes, JavaScript, APIs, scraping, RAM, sinergias, ratings, perfiles públicos o filtros rígidos. Cards=4, CardPrintings=4, Decks=1 y el Deck piloto continúa Draft.

## Pruebas

Las pruebas cubren estado vacío, exclusión de Deck piloto Draft, búsqueda por nombre/arquetipo/resumen, ausencia de Draft/privados, no resultados, conteos Legends/MAIN por suma de cantidades, Video activo, archivo histórico, detalle anónimo y navegación Library → Deck → Card/Video. Las regresiones de 7D–7G, Videos, Choomdex y Content continúan en la suite completa.
