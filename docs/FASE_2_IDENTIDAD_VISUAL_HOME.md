# Fase 2 — Identidad visual y Home

## Resultado

Fase completada el 1 de septiembre de 2026. La página técnica mínima fue sustituida por una Home SSR con identidad visual propia para **JORGE CYBERPUNKTCG**, cuyo concepto de experiencia es **The Tactical Cyberdeck**.

## Sistema visual

- Paleta centralizada mediante variables CSS: fondo `#0D0D0D`, superficies tecnológicas oscuras, cian eléctrico, magenta, verde informativo y amarillo de foco.
- Tipografía segura: `Segoe UI`/Arial para lectura y Consolas/Courier New para estados de sistema.
- Componentes reutilizables: navbar, botones, badges, tarjetas, panel HUD, placeholder de vídeo y footer.
- Los fondos, grid, glow y formas HUD son CSS propio; los efectos son moderados y respetan `prefers-reduced-motion`.

## Home y límites

La Home contiene Hero, panel táctico conceptual sin métricas reales, DataStream para la última transmisión sin URL o ID inventado, Dataterm Táctico, herramientas futuras y llamada a comunidad. Choomdex Hispano, Deck Builder, Combat Terminal y Jack In se muestran con estados de desarrollo, sin rutas ni interfaces falsas.

## Responsive, accesibilidad y SEO

La navegación pasa a menú accionable con botón semántico, `aria-expanded` y `aria-controls` en móvil. Las rejillas pasan a una columna en pantallas estrechas; Hero, CTAs y vídeo evitan desbordamiento. Se incluyen landmarks, jerarquía de encabezados, enlace para saltar al contenido, foco visible, contraste y reducción de movimiento. `base.html` ofrece título y meta descripción extensibles; la Home los define de forma específica.

## JavaScript y assets

`static/js/main.js` sólo mejora la apertura/cierre de la navegación móvil; el contenido sigue siendo útil sin JavaScript. No se descargaron assets externos ni se incorporó propiedad intelectual de terceros.

## Archivos

- `templates/base.html` y `templates/core/home.html`
- `static/css/base.css`, `static/css/components.css`, `static/css/home.css`
- `static/js/main.js`
- `apps/core/views.py` y `apps/core/tests/test_views.py`
- `docs/ROADMAP.md`

## Pruebas y limitaciones

Se mantienen las pruebas del usuario personalizado y se añaden pruebas de la identidad y de ausencia de rutas internas futuras. No se creó modelo, migración, autenticación, herramienta ni integración de YouTube. Se realizó una inspección visual/manual local con la Home renderizada y se validaron los puntos de 360, 768, 1024 y 1440 px: no hubo desbordamiento horizontal y el menú móvil se abrió con su estado ARIA actualizado. No se añadieron dependencias de navegador.
