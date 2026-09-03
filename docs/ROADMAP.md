# Roadmap maestro — JorgeCyberpunkTCG

## Método de ejecución

Cada fase se cierra con alcance definido, pruebas proporcionales, documentación de decisiones y verificación. Una fase no se considera completada por tener interfaz: debe cumplir sus controles de seguridad, datos y mantenimiento correspondien## Estrategia y Categorización del Roadmap

### 1. COMPLETADO
- **0 → 7I.1**: Fundación técnica, Usuarios, Guías, YouTube, MVP Choomdex (Card/CardPrinting), Deck Builder CRUD/Interactivo, Tactical Deck File, Tactical Deck Library, Editor Editorial, Tactical Deck Analysis Experience y Coherencia Visual de Gestión.
- **8A — Release Readiness & Roadmap Realignment** (Hito de decisión y auditoría de producto).
- **8C — SEO & Discovery Readiness — completada**: Sitemap dinámico (`sitemap.xml`), `robots.txt` controlado por Django, enlaces canónicos limpios (`<link rel="canonical">`) y coherencia `noindex` en áreas privadas/borradores.

### 2. PRE-LANZAMIENTO (Recomendado antes del despliegue oficial)
- **8B — Experimento de contenido real & flujo táctico (HOLD)**: Suspendido temporalmente hasta la estabilización de las reglas/cartas definitivas del juego.
- **8D — Production Readiness**: Configuración de `production.py`, servido de archivos estáticos (WhiteNoise), base de datos de producción (PostgreSQL) y variables de entorno.
- **8E — Auditoría transversal pre-lanzamiento**: Verificación final de seguridad, performance y checklist de despliegue.

### 3. POST-LANZAMIENTO / CONDICIONAL (Solo bajo demanda de usuarios)
- **Fase 9 — Comunidad (MVP)**: Comentarios moderados, reportes y antiabuso (exige tráfico y audiencia activa previa).
- **Fase 10 — Gamificación y Netrunner Dashboard**: Street Cred, Eddies, avatares y recompensas comunitarias.

### 4. BLOQUEADO POR FUENTES EXTERNAS / NO-GO ACTUAL
- **INGESTA MASIVA DE CHOOMDEX**: Suspendida hasta disponer de fuente oficial autorizada o API directa.
- **RAM ANALYZER**: Despriorizado (`NOT_EVALUATED`) a la espera de reglas oficiales verificadas.

---

## Cuadro de Registro de Fases

| Fase | Resultado esperado | Condición de cierre |
|---|---|---|
| 0 | Constitución, arquitectura y planificación | Documentos aprobados; no hay código Django. |
| 1 | Fundación técnica Django — **completada** | Proyecto mínimo, settings por entorno, usuario personalizado, pruebas y Git ignorando secretos. |
| 2 | Sistema visual y Home — **completada** | Design tokens originales, layout responsive/accesible y Home basada en contenido propio. |
| 3 | Usuarios y autenticación — **completada** | Registro, acceso, recuperación y perfil base con permisos verificados. |
| 4 | Guías y estrategias — **completada** | Modelo editorial, categorías, slugs, administración y páginas indexables. |
| 5 | Integración editorial con YouTube — **completada** | Metadatos propios y relaciones con guías sin depender de API externa. |
| 6A–6D.4 | MVP Choomdex & CardPrinting — **completada** | Catálogo, impresiones, sets, procedencia y gates de verificación pasados. |
| 7A–7I.1 | Ecosistema de Mazos — **completada** | Builder interactivo, Ficha Táctica, Biblioteca pública, Editor Editorial y Análisis 7I. Módulo congelado. |
| 8A | Auditoría y Realineación — **completada** | Auditoría de producto, congelación de Mazos y propuesta de roadmap aprobada. |
| 8C | SEO & Discovery Readiness — **completada** | Sitemap.xml, robots.txt, canonicals y meta robots sin dependencias externas ni cambios de esquema. |
| 8D | Production Readiness | Configuración segura, observabilidad, estáticos/media, despliegue y plan de recuperación. |

## Ajuste razonado

Se conserva el orden conceptual. La Fase 1 debe fijar el usuario personalizado antes de cualquier migración, aunque el flujo de autenticación visible se posponga a la Fase 3. La Fase 13 no sustituye los controles previos: consolida una auditoría transversal final.

Desde 7E el proyecto **no busca competir con el Deck Builder oficial**. Mazos es principalmente una biblioteca táctica/editorial conectable al contenido propio de YouTube; el Builder queda como infraestructura para preparar y mantener composiciones.

## Hitos de decisión previos a módulos con datos externos

- Antes de Fase 5: decidir fuente, permisos y cadencia de actualización de metadatos de YouTube.
- Antes de Fase 6: validar fuentes y licencia de cada dato del juego; definir política de evidencia y correcciones.
- Antes de incorporar mercado: investigar APIs, términos, costes, límites y atribución; si no existe una fuente fiable, mantener «Sin datos de mercado».
- Antes de Fases 9–10: definir política de comunidad, moderación, retención de auditoría y límites antiabuso.
