# Fase 7I — Tactical Deck Analysis Experience

## Problema y decisión de producto

El Tactical Deck File ya contenía datos editoriales, composición y Videos relacionados, pero su orden inicial daba demasiado peso a la referencia de composición. La experiencia se reorganiza para responder primero qué hace el mazo, cómo funciona, cómo se juega y qué Cards importan. No replica el Deck Builder oficial: éste permanece como herramienta interna del owner.

## Circuito editorial y datos reutilizados

La ficha canónica `/mazos/<username>/<slug>/` conecta el circuito **YouTube → Tactical Deck File → análisis táctico → Cartas clave → Choomdex**. Reutiliza `DeckEditorialProfile`, `DeckKeyCard`, `DeckLegend`, `DeckEntry`, `Video.related_decks`, `Card` y sus URLs canónicas; no crea modelo, campo, relación ni dato nuevo.

## Jerarquía y presentación

La identidad y el resumen táctico aparecen primero cuando hay contenido. Estrategia y Plan de juego son secciones independientes de lectura larga; Fortalezas y Debilidades se comparan en escritorio y se apilan en móvil. Cartas clave reciben un panel propio, con nota editorial y enlace a Choomdex sólo para Cards públicas. La composición sigue disponible como referencia secundaria, seguida de validación estructural parcial y Videos activos relacionados.

Los campos editoriales vacíos se omiten sin bloques de relleno. La sección de Video se omite cuando no existe relación activa. Archived conserva su aviso histórico y las acciones del owner permanecen disponibles sin dominar la experiencia del visitante.

## Privacidad, SEO, rendimiento y límites

La política 7G permanece intacta: Draft y privado responden 404 a terceros; Published público es indexable; Archived público conserva `noindex, nofollow`. La vista ya usa `select_related` para owner/perfil y `prefetch_related` para Legends, MAIN, Cartas clave y Videos activos, sin validación duplicada ni consultas por Card.

Las pruebas cubren jerarquía editorial, omisión de campos vacíos, Card no pública sin enlace roto y las regresiones existentes de estado, composición, Video, owner y seguridad. No se añaden JavaScript, imágenes, APIs, scraping, datos, RAM, matchups, mulligan, combos, sinergias estructuradas, métricas, precios o mercado.

## Decisiones pospuestas

Matchups, mulligan, combos, sinergias estructuradas, métricas, RAM Analyzer, market/pricing y la revisión responsive transversal de navbar quedan como decisiones futuras, no compromisos de implementación.
