# Fase 7F — Integración editorial Deck ↔ YouTube

## Objetivo y decisión de modelo

La integración conecta Video, Tactical Deck File, composición y Choomdex como navegación editorial propia. No convierte Mazos en un competidor del Deck Builder oficial ni añade API, OAuth, scraping, estadísticas o automatización de YouTube.

Se eligió una relación opcional `ManyToMany` en `Video.related_decks`, con el reverso `Deck.related_videos`. Un vídeo puede comparar varios mazos y un mazo puede conservar una guía, actualización o análisis de partida. `apps.videos` ya era el agregado editorial que relaciona artículos, por lo que mantiene la dirección de dependencia; no se crea modelo intermedio porque el MVP no necesita rol, orden, video principal ni timestamps.

La migración `videos.0002_video_related_decks` añade sólo esa relación. Video puede existir sin Deck y Deck sin Video; no se cargan Videos ni relaciones en datos reales. `Deck.get_absolute_url()` y `Video.get_absolute_url()` centralizan las URLs canónicas sin hardcodearlas.

## Visibilidad, UI y administración

La relación almacenada no equivale a publicación. En Video detail se prefetchean y muestran únicamente Decks `is_public=True`; un Deck privado no deja nombre, URL, resumen ni composición en el contexto renderizado. En Tactical Deck File se prefetchean únicamente Videos `is_active=True`, la misma política pública ya existente en Videos. No se añadió ningún endpoint de edición público.

El Deck público muestra una sección **Transmisión relacionada** sólo si hay Videos activos, con título, resumen y CTA hacia el detalle interno. Se eligió CTA + metadata en vez de un segundo iframe: el embed seguro existente queda centralizado en Video detail y la ficha sigue ligera. Video detail muestra **Mazos relacionados** sólo si existen Decks públicos, con autor, arquetipo/resumen cuando estén disponibles, conteos anotados y enlace a la ficha táctica. El listado de Videos y Home no se sobrecargan.

La relación se administra desde Video Admin mediante `filter_horizontal`; no se duplica la selección en la interfaz owner de Deck. Article ↔ Video continúa intacta. Las secciones usan headings y enlaces textuales; las tarjetas existentes se adaptan a móvil mediante el grid global. Los Decks públicos siguen indexables y los enlaces internos aportan SEO sin schema nuevo.

## Rendimiento, pruebas y límites

Video detail usa `Prefetch` con Decks públicos, owner y perfil editorial, además de anotaciones de Legends/MAIN, para evitar consultas por tarjeta. Deck detail prefetchea Videos activos. Las pruebas cubren opcionalidad, 1 Video→2 Decks, 2 Videos→1 Deck, retirada de relación sin borrado, privacidad de Deck, visibilidad de Video, secciones ausentes, URLs canónicas y regresiones de Video/Deck.

Se conservan Cards=4, CardPrintings=4 y Decks=1 en la base local. RAM sigue `NOT_EVALUATED`; Builder, Card/CardPrinting/Set, Choomdex, importación y datos externos no se modifican. Futuro, sin implementar: video principal/orden, roles, timestamps de Cards, variantes de Deck, sinergias, forks, likes y comentarios.

## Prueba manual posterior

Cuando exista un Video real, relacionarlo desde Admin con un Deck público, abrir ambos detalles como visitante y comprobar los enlaces bidireccionales. Relacionar también un Deck privado y confirmar que no aparece en Video detail; desactivar un Video y confirmar que deja de aparecer en la ficha pública. No crear contenido ficticio en la base real.
