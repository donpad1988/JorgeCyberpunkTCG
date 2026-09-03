# Fase 7H.1 — Pulido visual Tactical Deck Library

## Motivo

La revisión visual de 7H detectó que la biblioteca vacía ofrecía un buscador sin universo vigente, que label/input carecían de suficiente separación visual y que los headings de estados competían con el título principal. La corrección se limita a UX/UI de `/mazos/publicos/`.

## Buscador condicional

La vista expone `has_published_decks`, derivado una vez desde el queryset de Decks públicos vigentes. El formulario sólo aparece si existe al menos un `PUBLISHED + is_public`. Draft público accidental, Published privado y Archive público no lo activan. Una `q` manual tampoco fuerza el formulario si no hay colección vigente.

Cuando existe colección, el formulario conserva label asociado, búsqueda GET, input `type=search`, botón Buscar y Limpiar búsqueda. En no-results se presenta una única acción clara de limpieza dentro de su panel.

## Estados editoriales

El estado global vacío y el de búsqueda sin resultados usan una misma familia de panel editorial: borde contextual, fondo discreto, contención y jerarquía secundaria `h2`. Su copy diferencia biblioteca en preparación de búsqueda sin coincidencias. Los CTAs del vacío conservan exclusivamente rutas reales a Guías, Videos y Choomdex.

El layout del formulario separa label y controles mediante una fila específica; se mantiene horizontal en escritorio y se apila en móvil. No se rediseñaron las tarjetas publicadas, Archivo histórico, Tactical Deck File, Home, navbar, Guías, Videos ni Choomdex.

## Accesibilidad, límites y pruebas

Se preservan estructura semántica, label, foco global, contraste y botones/enlaces textuales. No se añadió JavaScript, modelo, migración, datos, Cards, Videos, API, scraping ni CSS global. Las anotaciones manuales `# type: ignore` permanecen intactas.

Las pruebas verifican buscador oculto en vacío/Draft/privado/archive, visible para Published público, búsqueda existente, no-results, estado vacío y Archivo histórico. Los datos locales continúan Cards=4, CardPrintings=4, Decks=1 y el Deck piloto sigue Draft. La observación de densidad futura de navbar queda fuera de alcance para una revisión transversal posterior.
