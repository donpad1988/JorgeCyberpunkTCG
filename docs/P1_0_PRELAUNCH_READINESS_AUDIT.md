# P1.0 — PRELAUNCH READINESS AUDIT

**Proyecto:** JorgeCyberpunkTCG  
**Entorno Auditado:** Local (`http://127.0.0.1:8000/`) y Producción (`https://jorgecyberpunktcg.pythonanywhere.com/`)  
**Fecha:** 2026-09-10  
**Estado:** COMPLETADA — DECISIÓN: **GO CON CONDICIONES**  

---

## 1. OBJETIVO

Evaluar de forma integral e imparcial la preparación técnica, funcional, visual, legal y operacional de **JorgeCyberpunkTCG** como producto pre-lanzamiento (*prelaunch*) de cara al lanzamiento oficial del juego TCG en **octubre de 2026**.

La auditoría verifica que cualquier visitante o usuario registrado pueda navegar por las funcionalidades habilitadas de forma segura, comprensible y sin errores, garantizando que el sitio refleja con claridad qué herramientas están activas, cuáles están en desarrollo (*Próximamente*) y cuáles se encuentran congeladas/hold por políticas oficiales.

---

## 2. BASELINE VERIFICADO

El baseline técnico ejecutado sobre la rama `main` limpia del repositorio arrojó:

* **Branch:** `main` (sincronizada con `origin/main`)
* **Working Tree:** Clean (sin cambios pendientes)
* **`python manage.py check`:** OK — `System check identified no issues (0 silenced)`
* **`python manage.py makemigrations --check`:** OK — `No changes detected`
* **`python manage.py test`:** OK — `Ran 163 tests in 165.478s (OK)`
* **Producción PythonAnywhere:** Respondiendo `HTTP 200 OK`, HTTPS forzado, `Strict-Transport-Security: max-age=3600`, `Referrer-Policy: same-origin`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`. Interfaz visual `components.css` restaurada y validada en vivo (commit `da9b094`).

---

## 3. ALCANCE Y EXCLUSIONES

### Incluido en la Auditoría:
* Todas las rutas públicas (Home, Guías, Estrategias, Choomdex, YouTube, Registro, Login, Recuperación de contraseña, Páginas legales, Sitemap, Robots, Health check, 404).
* Rutas y flujos de usuario autenticado (Perfil, Edición de perfil, Mis mazos, Mazos públicos, Detalle de mazo, Editor táctico/editorial).
* Evaluación de contenido, UX/UI, accesibilidad básica, SEO/Discovery, seguridad funcional y estados vacíos.

### Exclusiones del Alcance (Congeladas / HOLD / Post-Launch):
* **Fase 8 (Herramientas):** *RAM Budget* (HOLD temporal por inestabilidad de costes/reglas oficiales), *Companion App* (PENDIENTE).
* **Fases 9–12 (Comunidad, Gamificación, Dashboard, Eventos):** POST-LAUNCH / HOLD.
* **Deck Builder / Herramientas Tácticas Avanzadas:** Simulación de matchups, simulator de mulligan, generador avanzado de combos y sinergias, métricas avanzadas y validación automática de RAM.
* **Choomdex:** Ingesta masiva mediante scraping o bots (SUSPENDIDA / HOLD hasta disponer de fuente autorizada).

---

## 4. INVENTARIO DE RUTAS Y FUNCIONALIDADES

### 4.1 Inventario Público (P1.0-A)

| Ruta | Nombre URL | Estado | Descripción / Evaluación |
| :--- | :--- | :--- | :--- |
| `/` | `core:home` | OK | Landing page principal con Hero, accesos a contenido, disclaimer y footer cibernético. |
| `/guias/` | `content:guide_list` | OK | Catálogo de guías tácticas publicadas e indexables. |
| `/guias/<slug>/` | `content:guide_detail` | OK | Vista de detalle de artículo de guía táctica. |
| `/estrategias/` | `content:strategy_list` | OK | Catálogo de estrategias publicadas. |
| `/estrategias/<slug>/` | `content:strategy_detail` | OK | Vista de detalle de artículo de estrategia. |
| `/videos/` | `videos:list` | OK | Catálogo de videos de YouTube integrados. |
| `/videos/<slug>/` | `videos:detail` | OK | Detalle de video con reproductor embed y notas tácticas. |
| `/choomdex/` | `cards:catalog` | OK | Catálogo interactivo de cartas (`CardPrinting`) con filtros por facción, tipo, rareza. |
| `/choomdex/<slug>/` | `cards:detail` | OK | Ficha táctica detallada de carta e impresiones. |
| `/cuenta/registro/` | `accounts:register` | OK | Formulario de registro de usuario con leyenda legal y enlaces a Privacidad/Términos. |
| `/cuenta/login/` | `accounts:login` | OK | Formulario de autenticación *Jack In*. |
| `/cuenta/password-reset/` | `accounts:password_reset` | OK | Flujo completo de recuperación de contraseña por correo. |
| `/privacidad/` | `core:privacy` | OK | Política de Privacidad indexable. |
| `/terminos/` | `core:terms` | OK | Términos de Uso e Independent Site Disclosure. |
| `/sitemap.xml` | `sitemap` | OK | Sitemap dinámico XML con URLs canónicas HTTPS. |
| `/robots.txt` | `robots_txt` | OK | Archivo de directivas para buscadores administrado por Django. |
| `/health/` | `health_check` | OK | Endpoint JSON de monitorización de salud (`{"status": "ok"}`). |
| `/ruta-inexistente/` | N/A | OK | Página de error 404 personalizada con diseño *Neural Interface*. |

### 4.2 Inventario Autenticado (P1.0-B)

| Ruta | Nombre URL | Estado | Descripción / Evaluación |
| :--- | :--- | :--- | :--- |
| `/cuenta/perfil/` | `accounts:profile` | OK | Dashboard de perfil cibernético del Netrunner. |
| `/cuenta/perfil/editar/` | `accounts:profile_edit` | OK | Edición de alias, bio e identidad del perfil. |
| `/cuenta/logout/` | `accounts:logout` | OK | Cierre de sesión seguro *Jack Out* vía POST + CSRF. |
| `/mazos/` | `decks:my_decks` | OK | Biblioteca personal de mazos (*Tactical Deck File*). |
| `/mazos/publicos/` | `decks:public_decks` | OK | Galería pública de mazos de la comunidad. |
| `/mazos/crear/` | `decks:deck_create` | OK | Formulario de creación de mazo. |
| `/mazos/<user>/<slug>/` | `decks:deck_detail` | OK | Vista de detalle táctico de mazo. |
| `/mazos/<user>/<slug>/construir/` | `decks:deck_builder` | OK | Editor interactivo de mazo. |
| `/mazos/<user>/<slug>/editorial/` | `decks:deck_editorial_update` | OK | Editor de notas editoriales y análisis táctico. |
| `/mazos/<user>/<slug>/editar/` | `decks:deck_update` | OK | Edición de metadatos de mazo. |
| `/mazos/<user>/<slug>/eliminar/` | `decks:deck_delete` | OK | Confirmación y eliminación de mazo. |

---

## 5. AUDITORÍA DE USER JOURNEYS (P1.0-C)

| # | User Journey | Calificación | Observaciones / Hallazgos |
| :--- | :--- | :--- | :--- |
| **J1** | Visitante → Home → Guías → Artículo → Navegación | **PASS** | Flujo fluido, enlaces funcionales, breadcrumbs y retorno a Home impecable. |
| **J2** | Visitante → Estrategias → Contenido disponible | **PASS** | Navegación limpia hacia artículos de estrategia táctica. |
| **J3** | Visitante → Choomdex → Filtros → Detalle de carta | **PASS** | Búsqueda y filtrado por taxonomías responde correctamente. |
| **J4** | Visitante → Registro → Login → Perfil | **PASS** | Creación de cuenta operativa, redirección a perfil correcta, validación de contraseñas. |
| **J5** | Usuario Autenticado → Crear Mazo → Editor Táctico | **PASS** | Creación y edición funcional dentro de los límites del editor de soporte. |
| **J6** | Usuario → Logout → Intento de acceso a `/mazos/` | **PASS** | Redirección obligatoria al Login (`LOGIN_URL = 'accounts:login'`). |
| **J7** | Password Reset | **PASS** | Generación de token y envío de correo SMTP HTTPS validado (P0.1). |
| **J8** | Navegación Legal (Privacidad / Términos) | **PASS** | Textos claros, responsivos, aviso de independencia visible y links de retorno a Home. |
| **J9** | Manejo de Rutas Inexistentes (404) | **PASS** | Muestra `404.html` nativo con botón de retorno a Home. |
| **J10**| Navegación Mobile Responsive | **PASS CON OBS**| Menú hamburguesa funcional. *(Obs: En viewport < 360px el texto del disclaimer del footer requiere ajuste de padding).* |

---

## 6. AUDITORÍA POR ÁREAS TÉCNICAS

### 6.1 Content Readiness (P1.0-D)
* **Estado:** Adecuado para fase prelaunch.
* **Evaluación:** Existen guías y artículos publicados como muestra editorial funcional. El Choomdex contiene la estructura de taxonomías y fichas activas. Se explicita con claridad la independencia del proyecto respecto a CD PROJEKT RED y WeirdCo.

### 6.2 UX y Coherencia Visual (P1.0-E)
* **Estado:** Excelente tras la restauración de `components.css`.
* **Evaluación:** Identidad cibernética *Neural Interface* consistente. La paleta de colores (Cyan, Dark Surface, Yellow accent, Green status) se aplica homogéneamente en cabecera, botones, formularios, cards y footer.

### 6.3 Accesibilidad Básica (P1.0-F)
* **Estado:** Satisfactorio.
* **Evaluación:** Jerarquía de headings `<h1>`-`<h3>` respetada; atributo `lang="es"` en `<html>`; enlaces con `aria-label` descriptivos; soporte de salto directo al contenido (`skip-link`); campos de formulario con `<label>` explícitos.

### 6.4 SEO / Discovery (P1.0-G)
* **Estado:** Totalmente configurado.
* **Evaluación:** `sitemap.xml` dinámico sirviendo URLs canónicas HTTPS; `robots.txt` activo; directiva `noindex` aplicada correctamente en vistas privadas (`/cuenta/`, `/mazos/crear/`).

### 6.5 Seguridad Funcional (P1.0-H)
* **Estado:** Hardening completo en producción.
* **Evaluación:** `SECURE_HSTS_SECONDS = 3600`, `SECURE_PROXY_SSL_HEADER`, `SECURE_REFERRER_POLICY = "same-origin"`, cookies de sesión y CSRF en `SECURE=True`, `DEBUG=False` incondicional en producción y aislado en desarrollo.

### 6.6 Estados Vacíos y Placeholders (P1.0-I)
* **Estado:** Transparente.
* **Evaluación:** Las secciones pendientes (Comunidad, RAM Budget, Dashboard Netrunner) muestran la insignia clara **`Comunidad · Próximamente`** o **`En preparación`**, evitando falsas expectativas sin presentar roturas ni errores visuales.

### 6.7 Errores y Logs (P1.0-J)
* **Estado:** Limpio.
* **Evaluación:** Cero excepciones no capturadas; logs de PythonAnywhere sin errores 500 post-despliegue; 163 tests automatizados pasando en verde.

### 6.8 Datos y Base de Datos (P1.0-K)
* **Estado:** Operativo y respaldado.
* **Evaluación:** SQLite en producción operando con esquema limpio; script `scripts/backup_sqlite.py` probado y validado con copias de seguridad de integridad (`PRAGMA integrity_check`).

---

## 7. MATRIZ DE READINESS

| Área / Módulo | Estado Readiness | Evidencia / Justificación |
| :--- | :--- | :--- |
| **Infraestructura** | `READY` | PythonAnywhere WSGI + SQLite limpia + servido estático nativo. |
| **Seguridad** | `READY` | HSTS 3600s, SSL Proxy, Referrer Policy `same-origin`, `DEBUG=False`. |
| **Autenticación** | `READY` | Custom User model, Login/Logout POST CSRF, Perfil Netrunner. |
| **Recuperación de Cuenta** | `READY` | Gmail SMTP TLS operativo con URLs canónicas HTTPS en vivo. |
| **Legal / Privacidad** | `READY` | Privacidad, Términos y Disclaimer de independencia publicados. |
| **Home** | `READY` | Landing page responsive con tokens cibernéticos *Neural Interface*. |
| **Guías / Estrategias** | `READY` | CMS editorial funcional con URLs slug indexables. |
| **YouTube** | `READY` | Integración de video propio como soporte editorial. |
| **Choomdex** | `READY WITH CONDITIONS` | Catálogo base listo; ingesta masiva congelada hasta fuente autorizada. |
| **Mazos** | `READY WITH CONDITIONS` | Tactical Deck File/Library listos; herramientas avanzadas en HOLD. |
| **Perfil / Edición** | `READY` | Dashboard de usuario y edición de metadatos operativos. |
| **Navegación / Responsive**| `READY` | Navbar restaurada en `components.css`, menú mobile funcional. |
| **Accesibilidad Básica** | `READY` | Structure H1-H3, skip-links, labels y aria-labels implementados. |
| **SEO / Discovery** | `READY` | `sitemap.xml`, `robots.txt`, canonicals y `noindex` en zonas privadas. |
| **Estados Vacíos** | `READY` | Badges "Próximamente" transparentes en secciones no disponibles. |
| **Backup / Recovery** | `READY` | Backup automatizado `backup_sqlite.py` comprobado en producción. |

---

## 8. HALLAZGOS Y PRIORIZACIÓN

### P0 — Bloqueantes Prelaunch (0 Hallazgos)
* *Ningún bloqueante crítico detectado.*

### P1 — Necesario antes de ampliar usuarios reales (1 Hallazgo)
1. **[UX / Mobile] Ajuste menor de responsive en footer para pantalla súper estrecha (< 360px):**
   * **Área:** UX / CSS.
   * **Riesgo:** BAJO.
   * **Descripción:** En dispositivos móviles extremadamente estrechos (< 360px), la nota legal del footer muestra un margen lateral ligeramente ajustado.

### P2 — Recomendable antes del lanzamiento oficial (2 Hallazgos)
1. **[Choomdex] Ampliación editorial del catálogo inicial:**
   * **Área:** CONTENT.
   * **Riesgo:** BAJO.
   * **Descripción:** Incorporar manualmente más cartas de muestra de forma editorial antes del lanzamiento oficial de octubre de 2026.
2. **[HSTS] Escalado de HSTS a 30 días post-observación:**
   * **Área:** SECURITY.
   * **Riesgo:** BAJO.
   * **Descripción:** Tras 5–7 días de operación estable en producción, incrementar `DJANGO_SECURE_HSTS_SECONDS` a `2592000` (30 días).

### P3 — Post-Launch (Fases 9–12)
* Módulo de Comunidad (Comentarios, Favoritos).
* Sistema de Gamificación (XP, Street Cred, Eddies).
* Dashboard / Terminal Netrunner avanzado.
* Módulo de Eventos y Torneos.

### HOLD / Congelados
* Ingesta masiva por scraping de cartas.
* RAM Budget / RAM Analyzer / Companion App.
* Mulligan simulator y herramientas competitivas complejas.

---

## 9. DECISIÓN FINAL P1.0

### **DECISIÓN: GO CON CONDICIONES**

**Justificación Factual:**
El proyecto **JorgeCyberpunkTCG** presenta una base de código extremadamente limpia, segura y arquitectónicamente sólida. Todos los módulos habilitados (Autenticación, Guías, Choomdex base, Mazos, YouTube, SEO, Legal, Backup y Security Hardening) funcionan sin fallos y cumplen rigurosamente con los estándares de producción. El producto está listo para pruebas controladas y evolución prelaunch hacia octubre de 2026.

---

## 10. BACKLOG PRIORIZADO DE TRABAJOS POSTERIORES (NO IMPLEMENTADOS)

1. **[P1.1] Monitoreo y observación de HSTS en producción (Etapa 1: 3600s).**
2. **[P1.2] Retoque menor de espaciado responsive en footer en viewports ultra-estrechos.**
3. **[P1.3] Curaduría y carga editorial controlada de nuevas cartas en Choomdex.**
4. **[P1.4] Elevación de HSTS a Etapa 2 (30 días) tras verificar estabilidad en producción.**
