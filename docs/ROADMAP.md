# Roadmap maestro — JorgeCyberpunkTCG

## Visión General y Estado del Proyecto

El proyecto **JorgeCyberpunkTCG** ha completado su **despliegue técnico inicial en producción** sobre la plataforma **PythonAnywhere** (`https://jorgecyberpunktcg.pythonanywhere.com/`).

> [!IMPORTANT]
> **Diferenciación Pre-lanzamiento vs Lanzamiento Oficial**:
> Este hito marca la finalización del *despliegue técnico inicial* de la infraestructura MVP. El proyecto se mantiene en estado **prelaunch** (pre-lanzamiento), alineado con el lanzamiento oficial del juego TCG previsto para **octubre de 2026**. Los datos, reglas, cartas y contenidos continuarán evolucionando en el entorno pre-lanzamiento.

---

## Mapeo entre Subfases Operativas y Roadmap Maestro

Durante el desarrollo reciente se utilizaron nomenclaturas operativas para agrupar paquetes de trabajo (tales como `8A`, `8C`, `8D.1`, `8D.2` y `8D.3`). Estas denominaciones **no sustituyen las fases funcionales originales (8 a 12)** del roadmap maestro, sino que corresponden a trabajos transversales y hitos de preparación:

- **8A (Release Readiness & Roadmap Realignment)**: Hito operativo de auditoría de producto y realineación del roadmap.
- **8C (SEO & Discovery Readiness)**: Trabajo adelantado conceptualmente perteneciente a la **Fase 13 (SEO / Seguridad / Rendimiento)**.
- **8D.1 (Production Architecture & Deployment Audit)**: Preparación transversal de arquitectura para **Fases 13 y 14**.
- **8D.2 (Production Configuration Implementation)**: Configuración técnica de producción perteneciente a las **Fases 13 y 14**.
- **8D.3 (Deployment Execution)**: Ejecución del despliegue técnico inicial de la **Fase 14 (Producción)**.

Las fases funcionales originales **Fase 8 (Herramientas)**, **Fase 9 (Comunidad)**, **Fase 10 (Gamificación)**, **Fase 11 (Dashboard)** y **Fase 12 (Eventos)** permanecen vigentes en el roadmap maestro como fases pendientes, en HOLD o congeladas según las necesidades reales del producto.

---

## Estado Real del Roadmap Maestro (Fases 0–14)

### FASE 0 — Constitución Técnica
- **Estado**: `COMPLETADA`
- **Descripción**: Definición de arquitectura inicial, convenciones, stack (Django, Python 3.13, Vanilla CSS *Neural Interface*) y gobernanza de código.

### FASE 1 — Core + Identidad Visual (Fundación Django)
- **Estado**: `COMPLETADA`
- **Descripción**: Configuración base de Django, sistema de usuarios personalizado, design system cibernético *Neural Interface*, entorno estructurado y tests base.

### FASE 2 — Home
- **Estado**: `COMPLETADA`
- **Descripción**: Landing page principal responsive, integración de tokens de diseño, navegación, footer y estructura accesible orientada a contenido propio.

### FASE 3 — Usuarios
- **Estado**: `COMPLETADA`
- **Descripción**: Autenticación, registro de usuarios, login, logout, gestión de perfil cibernético y permisos base.

### FASE 4 — Guías / Estrategias
- **Estado**: `COMPLETADA`
- **Descripción**: Sistema de gestión de contenidos editoriales, categorías, artículos tácticos, slugs y vistas públicas indexables.

### FASE 5 — YouTube
- **Estado**: `COMPLETADA`
- **Descripción**: Integración de contenido audiovisual (videos de YouTube) como apoyo editorial a las guías y estrategias sin dependencias complejas de APIs de terceros.

### FASE 6 — Choomdex
- **Estado**: `COMPLETADA (Base Arquitectónica) / HOLD (Ingesta Masiva)`
- **Descripción**: Modelo de datos unificado (`Card` + `CardPrinting`), taxonomías (facciones, tipos, rarezas, ilustradores, sets), vistas de catálogo y detalle táctico.
- **Política de Ingesta (CONGELADA / HOLD)**: La ingesta masiva continúa **suspendida** hasta disponer de una fuente autorizada. Se aplican estrictamente las reglas:
  - *No scraping* ni bots.
  - *No importación masiva* desde sitios oficiales sin permisos.
  - *No uso de imágenes oficiales* sin licencia o autorización expresa.
  - El Choomdex crecerá exclusivamente mediante un flujo **editorial y controlado**.

### FASE 7 — Deck Builder / Sistema Táctico de Mazos
- **Estado**: `COMPLETADA (Arquitectura) / CONGELADA (Funcionalmente)`
- **Descripción**: Ecosistema completo de mazos (Builder interactivo, *Tactical Deck File*, *Tactical Deck Library*, Editor Editorial y *Tactical Deck Analysis Experience*).
- **Enfoque de Producto**: Redefinido para centrarse en la **Tactical Deck Library / Tactical Deck File** como herramienta de divulgación editorial. El Deck Builder interno actúa como infraestructura auxiliar de soporte.
- **Límites de Alcance**: **No competir** con el Deck Builder oficial del TCG. Permanecen congelados/no implementados hasta que la demanda y el contenido real lo justifiquen:
  - Matchups
  - Mulligan simulator
  - Generador de combos y sinergias complejas
  - Métricas avanzadas
  - RAM validation automática

### FASE 8 — Herramientas
- **Estado**: `PENDIENTE / HOLD`
- **RAM Budget**: En **NO-GO temporal** debido a que los datos y reglas oficiales de costo/RAM aún no son lo suficientemente estables o verificados.
- **Companion App**: **PENDIENTE**. No se implementará en la etapa prelaunch actual.

### FASE 9 — Comunidad
- **Estado**: `PENDIENTE`
- **Descripción**: Módulo de interacción social (comentarios moderados, favoritos, mazos públicos con interacción, reportes y antiabuso).
- **Consideraciones**: Introduce complejidad operacional (moderación, spam, privacidad, concurrencia). Su implementación se evaluará tras el lanzamiento público si existe audiencia activa. Podría justificar la migración a PostgreSQL en el futuro, aunque **no es requerida para el MVP**.

### FASE 10 — Gamificación
- **Estado**: `PENDIENTE`
- **Descripción**: Economía interna y sistema de incentivos comunitarios (XP, Street Cred, Eddies, Gigs).
- **Criterio**: Se evita crear una economía artificial previa al lanzamiento. Se implementará únicamente cuando se identifiquen comportamientos reales de los usuarios que valga la pena recompensar.

### FASE 11 — Dashboard (Terminal de Netrunner)
- **Estado**: `PENDIENTE`
- **Descripción**: Panel de control avanzado y métricas para el usuario Netrunner.
- **Criterio**: Se construirá posteriormente a la existencia de actividad comunitaria real para evitar presentar un panel con métricas ficticias o placeholders.

### FASE 12 — Eventos
- **Estado**: `PENDIENTE`
- **Descripción**: Módulo para la organización y seguimiento de eventos y comunidad presencial.
- **Criterio**: Se evaluará una vez que el juego oficial esté lanzado y existan comunidades presenciales activas.

### FASE 13 — SEO / Seguridad / Rendimiento
- **Estado**: `PARCIALMENTE ADELANTADA`
- **SEO & Discovery (Completado en 8C)**:
  - `sitemap.xml` dinámico.
  - `robots.txt` gestionado dinámicamente por Django.
  - Etiquetas `<link rel="canonical">` y directivas `noindex` en zonas privadas/borradores.
  - Visibilidad orientada al descubrimiento orgánico prelaunch.
- **Production Readiness (Completado en 8D.2)**:
  - Configuración modular de producción (`config.settings.production`).
  - Endpoint de salud `/health/` retornando `200 OK`.
  - Páginas personalizadas de error `404.html` y `500.html`.
  - HTTPS, secure cookies, SSL redirect y logging a consola.
- **Política HSTS**: `SECURE_HSTS_SECONDS = 0` se mantiene **deliberadamente** durante la fase de estabilización inicial (HSTS progresivo).

### FASE 14 — Producción / Despliegue
- **Estado**: `DESPLIEGUE TÉCNICO INICIAL COMPLETADO`
- **Hosting**: PythonAnywhere.
- **URL Producción**: `https://jorgecyberpunktcg.pythonanywhere.com/`
- **Arquitectura de Producción**: PythonAnywhere WSGI + SQLite limpia + servido estático nativo de PythonAnywhere.
- **Carácter del Despliegue**: Despliegue técnico inicial pre-lanzamiento. El entorno de producción servirá como plataforma de pruebas controladas e integración continua hacia el lanzamiento oficial en **octubre de 2026**.

### Hitos Transversales de Auditoría Prelaunch (Asociados a Fases 13–14)

* **P0.1 — Email & Account Recovery**: `COMPLETADA`
  - Gmail SMTP operativo en producción (`smtp.gmail.com:587` TLS).
  - Flujo real de Password Reset de Django validado end-to-end en producción recibiendo correo con URL HTTPS canónica.
  - Incidencia de orden en la capa WSGI operacional de PythonAnywhere corregida (variables de entorno `EMAIL_*` declaradas antes de `get_wsgi_application()`).
  - Configuración sensible y secretos (App Password, `DJANGO_SECRET_KEY`) preservados estrictamente fuera del repositorio Git.
* **P0.2 — Privacy & Independent-Site Disclosure**: `COMPLETADA`
  - Páginas públicas de Política de Privacidad (`/privacidad/`) y Términos de Uso (`/terminos/`) implementadas e indexables.
  - Disclaimer factual de independencia respecto a CD PROJEKT RED y WeirdCo reforzado en el footer y en páginas legales.
  - Leyenda informativa de transparencia pre-registro añadida en `register.html` con hipervínculos hacia privacidad y términos.
  - Coherencia visual *Neural Interface*, 136 tests pasando, sin modelos nuevos ni migraciones.

* **P0.3 — SQLite Backup & Recovery**: `IMPLEMENTACIÓN LOCAL COMPLETADA / VALIDACIÓN PRODUCCIÓN PENDIENTE`
  - Script standalone `scripts/backup_sqlite.py` creado con soporte nativo para `sqlite3.Connection.backup()`, verificación de integridad con `PRAGMA integrity_check;`, rotación de 10 copias rutinarias y exención de respaldos etiquetados.
  - Test suite completa de 13 pruebas unitarias e integración con simulación de disaster recovery creada y superada.
  - Manual operacional `docs/P0_3_SQLITE_BACKUP_RECOVERY.md` elaborado.
  - Pendiente ejecución del primer backup real y validación final durante el despliegue de P0.2 en PythonAnywhere.

---

## Cuadro de Resumen del Roadmap Maestro

| Fase | Título | Estado | Descripción Sintética |
|---|---|---|---|
| 0 | Constitución técnica | `COMPLETADA` | Arquitectura, stack y gobernanza técnica. |
| 1 | Fundación Django | `COMPLETADA` | Settings, usuario personalizado, design tokens Neural Interface. |
| 2 | Home | `COMPLETADA` | Landing page cibernética responsive y estructurada. |
| 3 | Usuarios | `COMPLETADA` | Registro, autenticación, perfiles y permisos. |
| 4 | Guías / Estrategias | `COMPLETADA` | Publicaciones editoriales y categorización táctica. |
| 5 | YouTube | `COMPLETADA` | Integración de video propio como soporte editorial. |
| 6 | Choomdex | `COMPLETADA (Base) / HOLD (Ingesta)` | Modelo Card/CardPrinting. Ingesta masiva congelada (no scraping, crecimiento editorial). |
| 7 | Sistema Táctico de Mazos | `COMPLETADA (Arq) / CONGELADA (Func)` | Tactical Deck Library / File. Sin funciones complejas ni competencia con app oficial. |
| 8 | Herramientas | `PENDIENTE / HOLD` | RAM Budget (NO-GO temporal) y Companion App (Pendiente). |
| 9 | Comunidad | `PENDIENTE` | Comentarios, favoritos y moderación. Evaluación post-lanzamiento. |
| 10 | Gamificación | `PENDIENTE` | Sistema de XP, Street Cred y Eddies. Pendiente a hábitos reales. |
| 11 | Dashboard Netrunner | `PENDIENTE` | Terminal de usuario. Requiere actividad comunitaria previa. |
| 12 | Eventos | `PENDIENTE` | Eventos presenciales y torneos. Pendiente a lanzamiento oficial. |
| 13 | SEO / Seguridad / Performance | `PARCIALMENTE ADELANTADA` | SEO completado (8C). Security settings y health completados (8D.2). HSTS=0 deliberado. |
| 14 | Producción / Despliegue | `DESPLIEGUE TÉCNICO INICIAL` | Live en PythonAnywhere con SQLite limpia. Prelaunch hacia octubre 2026. |

---

## Directrices de Decisiones Futuras

1. **Evaluación de Datos Oficiales (Octubre 2026)**: Cualquier actualización masiva de cartas o reglas del TCG debe esperar a la publicación oficial de fuentes autorizadas o licencias explícitas.
2. **Evolución a PostgreSQL**: Se mantendrá SQLite mientras la carga de lectura y ausencia de concurrencia masiva de escritura lo permitan. La migración a PostgreSQL solo se justificará si la Fase 9 (Comunidad) o la Fase 10 (Gamificación) introducen alta frecuencia de transacciones de usuarios simultáneos.
3. **Activación Progresiva de HSTS**: Una vez verificada la estabilidad del dominio y SSL en producción a lo largo de varias semanas de operación prelaunch, se programará la elevación gradual de `SECURE_HSTS_SECONDS`.
