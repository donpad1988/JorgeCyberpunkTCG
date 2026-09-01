# Constitución maestra — JorgeCyberpunkTCG

## Propósito

**JORGE CYBERPUNKTCG** será una plataforma hispanohablante, independiente y útil para jugadores de Cyberpunk TCG. Su concepto es **The Tactical Cyberdeck**: un punto de entrada a guías, análisis táctico, herramientas, contenido editorial conectado con YouTube y, progresivamente, comunidad.

Eslogan provisional: *«Tu Cyberdeck táctico para hackear el meta y convertirte en Leyenda.»*

El sitio debe aportar valor por sí mismo: una persona que llegue desde un buscador debe poder aprender o consultar una herramienta sin conocer previamente el canal de YouTube.

## Límites de la Fase 0

Esta fase documenta decisiones. No crea proyecto Django, aplicaciones, entorno virtual, paquetes, base de datos, migraciones, modelos ni interfaces. Tampoco descarga assets, integra APIs, realiza scraping ni incorpora datos del juego.

## Principios vinculantes

- Avanzar módulo a módulo: analizar, implementar, probar, documentar, verificar y cerrar antes de abrir el siguiente.
- Mantener separación entre presentación, vistas, formularios, modelos y reglas de dominio; no colocar reglas de negocio en templates o JavaScript.
- Usar Django como fuente de verdad para validaciones, permisos, operaciones sensibles y autenticación.
- Aplicar diseño responsive, accesible y de rendimiento contenido desde el inicio.
- Preferir datos administrables y configurables frente a reglas dudosas codificadas de forma fija.
- Mantener una identidad cyberpunk original: geometría, HUD, terminales, cian/magenta y efectos moderados; nunca copiar interfaces, marcas ni assets de terceros.

## Datos y propiedad intelectual

Todo dato de cartas, reglas, rarezas, precios, expansiones y personajes deberá conservar posteriormente su naturaleza o procedencia cuando aplique: `OFFICIAL`, `COMMUNITY`, `EDITORIAL` o `MARKET`. La ausencia de datos se comunicará como «Sin datos», nunca con valores inventados.

No se hará scraping ni se consumirá una API de terceros sin una evaluación posterior de licencia, condiciones de uso, coste, fiabilidad y límites. Los assets iniciales serán propios, geométricos o placeholders reemplazables.

## Seguridad y comunidad

Las futuras funciones privadas usarán autenticación y autorización de Django, CSRF, validación de backend, permisos por objeto cuando correspondan y secretos fuera del repositorio. Contenido, archivos, comentarios, recompensas, mazos y publicaciones se diseñarán con prevención de abuso, moderación, auditoría y trazabilidad. Los Eddies son moneda virtual no financiera, no canjeable y sin representación de dinero real.

## Criterios permanentes de calidad

- HTML semántico, foco visible, labels, texto alternativo, contraste suficiente y respeto por `prefers-reduced-motion`.
- Mobile-first para navegación, lectura y herramientas presenciales; escritorio para análisis y contenido enriquecido.
- URLs semánticas, slugs, metadatos y contenido indexable para SEO.
- Consultas eficientes, paginación, carga diferida y sin JavaScript o embeds innecesarios.
- Pruebas por módulo antes de cerrar una fase.

La verificación mínima de cada fase Django será `python manage.py check`, `python manage.py makemigrations --check` y `python manage.py test`.
