# Fase 4 — Guías y estrategias editoriales

## Arquitectura y modelos

Se creó `apps.content` como única app editorial. `ContentCategory` aporta nombre, slug, descripción, estado activo y fechas. `Article` concentra Guía y Estrategia mediante `TextChoices`, se relaciona con el Custom User mediante `settings.AUTH_USER_MODEL`, y contiene título, slug, categoría, autor, resumen, cuerpo, estado y fechas.

## Publicación, URLs y vistas

La consulta pública `Article.objects.publicly_visible()` exige estado publicado y `published_at <= timezone.now()`. Por tanto, borradores, artículos futuros y publicados sin fecha devuelven 404 incluso con slug conocido. Las URLs son `/guias/`, `/guias/<slug>/`, `/estrategias/` y `/estrategias/<slug>/`. Los listados comparten implementación y muestran un estado vacío cuando no hay contenido real.

## Administración, SEO y seguridad

Los dos modelos están registrados en Django Admin con filtros, búsquedas, slugs prepopulados y jerarquía de fecha. El detalle usa título y resumen reales para title y meta description. El body usa `linebreaks`, sin `safe`, por lo que HTML arbitrario se escapa. No existe edición pública ni contenido inicial inventado.

## Integración y calidad

Navbar y tarjetas de Dataterm enlazan a Guías/Estrategias; Choomdex, Mazos, Comunidad y RAM siguen futuros. Se añadió `content.css` para tarjetas y lectura larga responsive, con metadata semántica y elementos `time`. La migración `content.0001_initial` crea únicamente los modelos editoriales. Resultado: 17 tests correctos, checks sin incidencias y sin dependencias, assets externos o APIs nuevas.

## Limitaciones

No se implementaron comentarios, favoritos, búsqueda, uploads, editor WYSIWYG, Markdown externo, YouTube, Choomdex, mazos ni herramientas. El contenido real se incorporará posteriormente desde el Admin tras su revisión.
