# Fase 6C.3 — Presentación táctica de Choomdex

## Objetivo y alcance

La fase mejora únicamente la interfaz de catálogo y ficha de Choomdex. El catálogo presenta un grid responsive de tarjetas HUD y el detalle una ficha táctica. No modifica modelos, vistas, URLs, migraciones ni datos del dataset local.

## Cambios visuales

- Catálogo con búsqueda y selectores GET para Set y Tipo, conservando los filtros ya soportados.
- Tarjetas con identificador de tipo, nombre, Set, placeholder CSS propio, datos estructurados y enlace al detalle.
- Ficha de detalle con panel de datos, enlace de retorno y procedencia discreta.
- Paginación accesible que preserva búsqueda y filtros.

## Datos condicionales y procedencia

Se muestran `collector_number`, `cost`, `ram` y `power` sólo cuando hay valor. El collector conserva su valor textual, incluidos ceros iniciales. `rules_text` se omite por completo cuando está vacío. Cuando existe `source_url`, el detalle ofrece “Fuente oficial” con `target="_blank"` y `rel="noopener noreferrer"`; no muestra la URL completa como contenido dominante.

## Accesibilidad y responsive

Los formularios conservan labels reales, los enlaces tienen texto comprensible y el foco visible procede del sistema global. El grid usa 2–4 columnas según el ancho, dos columnas en tablet y una en móvil; los nombres largos envuelven sin desbordamiento. No se usan imágenes externas, logos oficiales ni JavaScript adicional.

## Cobertura y límites

Se añadieron pruebas de tarjetas tácticas, atributos condicionales, detalle, omisión de rules text y enlace seguro de procedencia. Siguen fuera de alcance imágenes, rareza, keywords, facciones, mercado, Deck Builder, RAM Analyzer y `CardPrinting`; esta presentación no modifica sus decisiones arquitectónicas.
