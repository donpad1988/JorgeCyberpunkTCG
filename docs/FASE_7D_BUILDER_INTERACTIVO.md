# Fase 7D — Builder interactivo de mazos

## Alcance y arquitectura

Se añadió un Builder SSR progresivo para el owner en `/mazos/<username>/<slug>/construir/`. El Builder separa Legends, catálogo MAIN, composición y validación parcial. No hay SPA, dependencias nuevas, imágenes oficiales, importación, scraping ni algoritmo RAM.

`DeckCompositionService` centraliza `add_legend`, `remove_legend`, `add_main_card`, `decrement_main_card` y `remove_main_card`. Cada operación usa `transaction.atomic()` y resuelve el Deck mediante el helper de ownership antes de leer o escribir. En SQLite esto aporta una unidad de cambio proporcional; una futura base concurrente podrá añadir bloqueo específico si el volumen lo exige.

## Endpoints y seguridad

Todos los endpoints de composición requieren owner autenticado y POST:

- `construir/`: GET, sólo owner.
- `legend/anadir/` y `legend/retirar/`.
- `main/anadir/`, `main/decrementar/` y `main/quitar/`.

Un tercero recibe 404 incluso para Deck público. Card IDs se resuelven en servidor, se verifican tipo y elegibilidad, y los entry IDs siempre se restringen al Deck de la URL resuelta para el owner. No se aceptan owner, username, cantidad arbitraria ni CardPrinting en payload. Los formularios incluyen CSRF y aplican PRG tras cada mutación.

## Reglas operacionales y validación

- Legends: Card elegible de tipo LEGEND, sin duplicados y máximo 3; sí puede retirarse hasta cero.
- MAIN: Card elegible no LEGEND; la primera adición crea cantidad 1, las siguientes llegan como máximo a 3.
- Decrementar 1 elimina la Entry; no existe cantidad persistida 0.
- MAIN no permite una operación que alcance 51; los drafts inferiores a 40 continúan permitidos.
- Cards históricas despublicadas permanecen visibles con warning, pero no pueden incrementarse; sí pueden reducirse o retirarse.

`DeckValidationService` continúa siendo la autoridad del resumen estructural. El Builder muestra conteos, errores y warnings, pero nunca afirma legalidad completa: RAM permanece `NOT_EVALUATED`.

## UX, búsqueda y filtros

Desktop usa dos paneles para catálogo MAIN y composición; en móvil se apilan verticalmente. Legends son una sección independiente. Botones tienen texto o etiquetas accesibles, foco visible global y no dependen de JavaScript.

La búsqueda usa `GET ?q=` por nombre. El catálogo MAIN filtra CardType existente y Set mediante la printing primaria, con `distinct()`; Legends se excluyen del catálogo MAIN y cuentan con selector propio. No se copió ni modificó la lógica de Choomdex.

El detalle de Deck sigue read-only para público y sólo muestra CTA “Construir mazo” al owner.

## Dataset y RAM

La base local se mantiene con cuatro Cards y cuatro CardPrintings. Ese conjunto no permite construir un MAIN completo real; el Builder muestra naturalmente una estructura incompleta y no inventa Cards. No se cargaron datos nuevos.

RAM, colores y legalidad total siguen fuera de alcance hasta cerrar el gate de reglas actuales y datos verificables.

## Tests y prueba manual posterior

Las pruebas cubren owner/anónimo/tercero, Deck público read-only, Legends, MAIN, límites de 3 y 50, búsqueda, filtros, Card/Entry ID attacks, histórico despublicado, GET no mutante, CSRF y regresión 7C.

Prueba manual propuesta: como owner abrir Builder, añadir Judy como Legend, comprobar duplicado, añadir Field Operator al MAIN hasta tres, intentar cuarta, decrementar y retirar; añadir Take Control/Sandevistan y revisar `RAM: NOT_EVALUATED`. Como segundo usuario, abrir un Deck público, confirmar detalle read-only y que Builder/POSTs devuelven 404.

La siguiente fase propuesta es 7E sólo después de una autorización y del cierre del gate RAM; no se inicia automáticamente.
