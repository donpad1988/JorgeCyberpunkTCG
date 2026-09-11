# P1.2 — Prelaunch Content & Product Readiness Audit

## Estado
COMPLETADA

## Objetivo
Determinar con evidencia empírica si JorgeCyberpunkTCG dispone de suficiente contenido real, coherencia de producto y orientación para que usuarios externos participen en pruebas prelaunch controladas sin percibir un sitio vacío, incompleto o engañoso.

## Baseline
- **Rama**: `main`
- **HEAD inicial**: `ddfc5ed` (`Complete P1.1 responsive footer hardening`)
- **Estado respecto a origin/main**: Sincronizada (up to date)
- **Working Tree**: Clean
- **Django Check**: `System check identified no issues (0 silenced)`
- **Migraciones Check**: `No changes detected`
- **Tests Baseline**: 163 tests OK (163.427s)

## Alcance
Inspección cuantitativa y cualitativa no destructiva de:
- Modelos y base de datos local (Guías, Estrategias, Videos, Choomdex, Mazos, Usuarios).
- Vistas, templates y navegación.
- Manejo de estados vacíos y placeholders.
- Coherencia narrativa del producto e independencia de la plataforma.

## Exclusiones
- NO se modificó ni creó código funcional (Python, JS, HTML, CSS).
- NO se redactó ni ingresó nuevo contenido en la base de datos (BD en SOLO LECTURA).
- NO se realizó scraping ni consultas a fuentes/APIs externas.
- NO se alteró la producción ni la configuración de HSTS (permanece en 3600 segundos).

## Metodología
Consulta directa a través de la capa ORM de Django en entorno local sin modificar registros, seguida de verificación de renderizado de vistas mediante el cliente HTTP de Django.

---

## Inventario Cuantitativo Real

| Módulo | Total | Público | Borrador / Privado | Observación |
| :--- | :---: | :---: | :---: | :--- |
| **Guías (`Article GUIDE`)** | 0 | 0 | 0 | Archivo editorial vacío. Muestra empty state de preparación. |
| **Estrategias (`Article STRATEGY`)** | 0 | 0 | 0 | Archivo editorial vacío. Muestra empty state de preparación. |
| **YouTube (`Video`)** | 0 | 0 | 0 | DataStream sin registros. Muestra widget `SIGNAL READY`. |
| **Sets (`Set`)** | 1 | 1 | 0 | 'Welcome to Night City - Retail'. |
| **Cartas (`Card`)** | 4 | 4 | 0 | 'Judy Álvarez', 'Field Operator', 'Take Control', 'Sandevistan'. |
| **Impresiones (`CardPrinting`)** | 4 | 4 | 0 | 1 por carta. 0 imágenes de archivo subidas (placeholders CSS). |
| **Mazos (`Deck`)** | 1 | 0 | 1 | 'Mazo Privado Prueba' (`DRAFT`, 2 cartas). Biblioteca pública vacía. |
| **Perfiles Editoriales Mazos** | 1 | 0 | 1 | 1 perfil borrador en mazo privado. |
| **Usuarios agregados** | 3 | N/A | 3 | 1 superuser, 1 staff, 3 activos. |

---

## Evaluación por Módulo

### 1. Home (Product Readiness)
- **Branding y propósito**: Declara con claridad el concepto "JORGE CYBERPUNKTCG: Cyberdeck táctico independiente para la comunidad hispana".
- **Transparencia e Independencia**: Presente en nota legal de footer y disclaimers ("No está afiliado oficialmente con CD PROJEKT RED ni WeirdCo").
- **Promesas y Claims**: Transparentes. Muestra badges de "Próximamente" en Comunidad/RAM Budget y "En desarrollo" en Combat Terminal, evitando engañar al visitante.
- **Calificación Home**: `READY WITH CONDITIONS` (Estructura visual e informativa excelente; falta contenido editorial publicado en los accesos directos).

### 2. Guías
- **Infraestructura**: `READY` (Modelos, URLs, vistas, templates y SEO sitemap implementados).
- **Contenido**: `INSUFFICIENT PRELAUNCH` (0 guías publicadas). Muestra un empty state digno: *"ARCHIVO TÁCTICO VACÍO - Las primeras guías están siendo preparadas"*.

### 3. Estrategias
- **Infraestructura**: `READY` (Modelos, URLs, vistas, templates y SEO sitemap implementados).
- **Contenido**: `INSUFFICIENT PRELAUNCH` (0 estrategias publicadas). Muestra un empty state digno: *"ARCHIVO TÁCTICO VACÍO - Las primeras estrategias están siendo preparadas"*.

### 4. YouTube
- **Infraestructura**: `READY` (Modelo Video, vista de lista, detalle con reproductor embed, asociación a mazos).
- **Contenido**: `INSUFFICIENT PRELAUNCH` (0 videos en BD). En Home se muestra el widget `datastream` en estado `SIGNAL READY` ("Transmisión pendiente de sincronización").

### 5. Choomdex
- **Infraestructura**: `READY` (Modelos Set, Card, CardPrinting, vista de catálogo con filtros por tipo/set, paginador, buscador por nombre/número, detalle de carta con stats).
- **Contenido**: `READY WITH CONDITIONS` (4 cartas verificadas para demostración técnica con stats completas). No posee imágenes oficiales (usa placeholders CSS tácticos). Ingesta masiva en `HOLD`.

### 6. Mazos
- **Infraestructura**: `READY` (CRUD completo de mazos, Deck Builder interactivo, validación de Legends y Main count, perfiles editoriales y búsqueda en biblioteca pública).
- **Contenido público**: `INSUFFICIENT PRELAUNCH` (0 mazos en `/mazos/publicos/` debido a que el único mazo en BD está en estado `DRAFT`). Muestra un panel de biblioteca vacía orientativo con botones hacia Guías, Videos y Choomdex.

---

## Estados Vacíos y Placeholders

### Estados Vacíos Evaluados
1. `/guias/`: Explica que las primeras guías se están preparando (`CORRECTO`).
2. `/estrategias/`: Explica que las primeras estrategias se están preparando (`CORRECTO`).
3. `/videos/`: Indica `SIGNAL READY` y transmisiones pendientes (`CORRECTO`).
4. `/choomdex/`: Base preparada para registros verificados (`CORRECTO`).
5. `/mazos/publicos/`: Notifica preparación de análisis e invita a explorar otras áreas (`CORRECTO`).

### Placeholders Evaluados
- **Home Datastream**: Widget cibernético simulando espera de señal (`CORRECTO`, sin pretender ser un video falso).
- **Choomdex Placeholders**: Reemplazo por CSS de la ilustración de carta (`CORRECTO`, evita infringir derechos o mostrar imágenes rotas).

---

## Experiencia de Usuario Nuevo

1. **¿Entiende qué es el sitio?**: SÍ
2. **¿Entiende que es independiente?**: SÍ
3. **¿Encuentra contenido sin registrarse?**: PARCIALMENTE (Encuentra Home, Legales y 4 cartas en Choomdex; 0 guías/videos/mazos).
4. **¿Entiende para qué sirve registrarse?**: SÍ (Para crear y administrar mazos propios en el Cyberdeck).
5. **¿Encuentra alguna utilidad después de registrarse?**: SÍ (Puede crear mazos en el Deck Builder).
6. **¿Encuentra secciones vacías inesperadas?**: PARCIALMENTE (Empty states son claros, pero las secciones principales carecen de artículos).
7. **¿Puede distinguir "Próximamente" de "roto"?**: SÍ (Badges explícitos en nav y cards).
8. **¿Puede descubrir Choomdex?**: SÍ (Navegación directa en header y footer).
9. **¿Puede descubrir Mazos?**: SÍ (Navegación directa en header y footer).
10. **¿Tiene una razón real para volver?**: PARCIALMENTE (Sitio técnicamente atractivo, pero requiere contenido editorial para justificar visitas recurrentes).

---

## Hallazgos Priorizados

### P0 — Bloqueantes
* Ninguno. El proyecto es completamente estable, seguro y navegable.

### P1 — Necesario Antes de Ampliar Pruebas Controladas
- `P1-CONTENT-01` [CONTENT / GUIDES]: Redactar y publicar 2–3 guías tácticas introductorias.
- `P1-CONTENT-02` [CONTENT / STRATEGIES]: Redactar y publicar 1–2 artículos de estrategia.
- `P1-DECKS-01` [DECKS / PUBLIC]: Publicar y completar el perfil editorial de al menos 1–2 mazos tácticos representativos para la biblioteca pública.
- `P1-YOUTUBE-01` [YOUTUBE / DATASTREAM]: Vincular al menos 1 video real en el módulo de transmisiones.

### P2 — Recomendable Antes del Lanzamiento Oficial
- `P2-CHOOMDEX-01` [CHOOMDEX / CARDS]: Ampliar el catálogo de cartas a un set representativo cuando exista fuente oficial verificada.
- `P2-HOME-01` [HOME / UX]: Destacar en la Home el mazo u origen editorial principal una vez que existan registros publicados.

### P3 — Crecimiento Post-Launch
- `P3-COMMUNITY-01` [COMMUNITY]: Implementación de reputación, Street Cred, Eddies y Gigs (congelados).
- `P3-TOOLS-01` [TOOLS]: Combat Terminal para partidas presenciales.

### HOLD — Congelado / Bloqueado
- `HOLD-CHOOMDEX-SCRAPING`: Ingesta masiva o scraping no autorizado.
- `HOLD-RAM-VALIDATION`: Reglas avanzadas de RAM Budget.
- `HOLD-FASES-8-12`: Fases 8 a 12 congeladas.

---

## Matriz Content Readiness

| Área | Infraestructura | Contenido | Estado | Evidencia |
| :--- | :---: | :---: | :---: | :--- |
| **Home** | READY | LIMITADO | READY WITH CONDITIONS | Landing responsive impecable; falta contenido activo. |
| **Guías** | READY | INSUFFICIENT | READY WITH CONDITIONS | 0 guías; empty state correcto. |
| **Estrategias** | READY | INSUFFICIENT | READY WITH CONDITIONS | 0 estrategias; empty state correcto. |
| **YouTube** | READY | INSUFFICIENT | READY WITH CONDITIONS | 0 videos; widget `SIGNAL READY` activo. |
| **Choomdex** | READY | READY W/ COND | READY WITH CONDITIONS | 4 cartas verificadas; placeholders CSS limpios; ingesta masiva en HOLD. |
| **Mazos** | READY | INSUFFICIENT | READY WITH CONDITIONS | Builder funcional; 0 mazos publicados en biblioteca. |
| **Perfil** | READY | READY | READY | Gestión de cuenta y mazos propia. |
| **Legal** | READY | READY | READY | Privacidad y Términos con disclaimers de independencia. |
| **Estados Vacíos** | READY | READY | READY | Mensajes explicativos y limpios en todas las secciones. |
| **Navegación** | READY | READY | READY | Sin enlaces rotos ni errores HTTP. |
| **Experiencia Nuevo Usuario**| READY | PARCIALMENTE | READY WITH CONDITIONS | Arquitectura clara; requiere masa crítica editorial mínima. |

---

## Decisión P1.2

### **GO CON CONDICIONES**

**Fundamentación**:
1. La infraestructura técnica, seguridad, navegación y experiencia visual están en estado **GO** (163 tests OK, 0 vulnerabilidades, 0 errores 404/500).
2. Para iniciar o ampliar pruebas con usuarios externos sin que el proyecto se perciba como una cáscara vacía, se debe cumplir la **CONDICIÓN P1**: publicar un volumen editorial mínimo inicial (2 guías, 1 estrategia, 1 mazo público analizado y 1 video).

---

## Backlog Derivado (Pendiente de Decisión del Propietario)

1. `P1-CONTENT-01`: Redacción e ingesta de Guías Tácticas Prelaunch (Prioridad P1).
2. `P1-CONTENT-02`: Redacción e ingesta de Artículos de Estrategia (Prioridad P1).
3. `P1-DECKS-01`: Creación y publicación de Tactical Deck Files de muestra (Prioridad P1).
4. `P1-YOUTUBE-01`: Sincronización de primer video en DataStream (Prioridad P1).
5. `P2-CHOOMDEX-01`: Ampliación editorial del Choomdex (Prioridad P2).

---

## Producción
- **Estado**: NO MODIFICADA.
- **HSTS**: Permanece en 3600 segundos (`SECURE_HSTS_SECONDS = 3600`).
