# FASE 8C — SEO & DISCOVERY READINESS

## 1. OBJETIVO Y CONTEXTO

Implementar la infraestructura técnica de SEO y descubrimiento para **JorgeCyberpunkTCG** previa al lanzamiento oficial, garantizando que los motores de búsqueda y rastreadores puedan descubrir e indexar eficientemente el contenido público del sitio sin comprometer la seguridad ni exponer áreas privadas o borradores.

Dado que la Fase 8B (Carga de Contenido Real) se encuentra temporalmente en estado **HOLD** a la espera de la estabilización del juego, la Fase 8C actúa de forma 100% técnica sin depender ni inventar contenido ficticio.

## 2. ARQUITECTURA TÉCNICA E IMPLEMENTACIÓN

### A. Dynamic Sitemap (`/sitemap.xml`)
Implementado mediante el framework nativo de Django (`django.contrib.sitemaps`).
- **Vista y URL**: Servido dinámicamente en `/sitemap.xml` con `Content-Type: application/xml`.
- **Componentes de Sitemap**:
  - `StaticViewSitemap`: URLs estructurales públicas (`home`, `guide_list`, `strategy_list`, `videos:list`, `cards:catalog`, `decks:public_decks`).
  - `ArticleSitemap`: Artículos publicados públicamente (`Article.objects.publicly_visible()`).
  - `VideoSitemap`: Videos activos (`Video.objects.filter(is_active=True)`).
  - `CardSitemap`: Cartas públicas (`Card.objects.public()`).
  - `DeckSitemap`: Mazos publicados y públicos (`Deck.objects.public_current()`).
- **Exclusiones estrictas**:
  - Mazos `DRAFT` o privados (`is_public=False`).
  - Mazos `ARCHIVED` (conservados históricamente pero con política `noindex`).
  - Artículos en borrador o con fecha de publicación futura.
  - Videos inactivos y cartas no públicas.
  - Rutas de administración (`/admin/`), autenticación (`/cuenta/`), editores y builder (`/construir/`, `/editorial/`, `/editar/`).
  - URLs con query strings (`?q=`, `?page=`, `?set=`, `?type=`).

### B. Dynamic Robots.txt (`/robots.txt`)
- **Vista y URL**: Servido dinámicamente desde `apps/core/views.py` como `text/plain; charset=utf-8`.
- **Instrucciones**:
  - `User-agent: *`
  - `Disallow: /admin/`
  - `Disallow: /cuenta/`
  - `Disallow: /mazos/*/editar/`, `/editorial/`, `/construir/`, `/eliminar/`
  - `Sitemap: <URL_ABSOLUTA_DINÁMICA>` (generada mediante `request.build_absolute_uri(reverse("sitemap"))` sin dominios hardcodeados).

### C. Enlaces Canónicos (`<link rel="canonical">`)
- **Infraestructura**: Bloque `{% block canonical %}{% endblock %}` integrado en `templates/base.html`.
- **Generación estricta**:
  - Landings públicas y páginas de búsqueda (`?q=`, `?page=`) renderizan la URL canónica limpia sin parámetros GET.
  - Páginas de detalle públicas renderizan su método canónico `get_absolute_url()` (ej. `Article.get_absolute_url()`, `Card.get_absolute_url()`, `Video.get_absolute_url()`, `Deck.get_absolute_url()`).
  - Ninguna URL o dominio fue hardcodeado; se utiliza la infraestructura dinámica del request (`request.scheme` y `request.get_host`).

### D. Coherencia Meta Robots
- Se añadieron bloques `{% block robots %}<meta name="robots" content="noindex, nofollow">{% endblock %}` en todas las vistas privadas y de gestión: login, registro, perfil, edición de perfil, recuperación de contraseña, mis mazos, editores y builder.
- Mazos archivados (`ARCHIVED`) o privados preservan su etiqueta `noindex, nofollow`.

## 3. VERIFICACIÓN Y COBERTURA DE TESTS

Se creó el módulo de tests [apps/core/tests/test_seo.py](file:///d:/01.Proyectos_Web/JorgeCyberpunkTCG/apps/core/tests/test_seo.py) con cobertura completa:
- `test_sitemap_xml_returns_200_and_xml_content_type`
- `test_sitemap_includes_public_landings_and_public_entities`
- `test_sitemap_excludes_drafts_private_archived_builder_editors_and_auth`
- `test_robots_txt_returns_200_text_plain_and_dynamic_sitemap_directive`
- `test_canonical_urls_and_query_string_stripping`
- `test_meta_robots_noindex_on_private_and_archived_pages`

Resultados de la suite: **128 / 128 tests pasados exitosamente**.

## 4. RESTRICCIONES Y REGLAS CUMPLIDAS
- **0 modelos de base de datos modificados**.
- **0 migraciones generadas**.
- **0 datos persistentes modificados** (Cards=4, CardPrintings=4, Decks=1, piloto DRAFT, RAM NOT_EVALUATED).
- **0 dependencias externas instaladas** (uso 100% de `django.contrib.sitemaps` nativo).
- **Módulo de Mazos**: Permanece funcionalmente congelado.
