# P1.3A — Editorial Foundation

## Estado
COMPLETADA LOCALMENTE — PENDIENTE DE APROBACIÓN DEL PROPIETARIO

## Objetivo
Crear y publicar una fundación editorial mínima y auténtica para que Guías y Estrategias dejen de estar vacías durante el prelaunch (exactamente 2 Guías y 1 Estrategia).

## Baseline
- **Rama**: main
- **HEAD**: 410eb8c Complete P1.2 content product readiness audit
- **Origin**: Sincronizada con origin/main
- **Working tree**: Clean
- **Django Check**: System check identified no issues (0 silenced)
- **Makemigrations**: No changes detected
- **Test Suite**: 163 tests OK

## Backup previo
- **Archivo**: `backups/db_backup_20260911_133723.sqlite3` (331,776 bytes)
- **Estado**: Exitoso (`PRAGMA integrity_check;` -> ok)

## Fuentes permitidas
Se utilizó únicamente documentación interna del repositorio, código existente, modelos, views, templates y datos locales verificados. Cero búsquedas web externas, cero scraping y cero fuentes no documentadas.

## Restricciones editoriales
Contenido original redactado en español, con estilo claro, táctico y coherente con el entorno cibernético de JorgeCyberpunkTCG.
- Cero reglas no verificadas presentadas como hechos.
- Cero métricas o claims de metajuego (winrates, tier lists, mulligans, probabilidades).
- Cero declaraciones de afiliación oficial.

## Contenido creado

### Guía 1
- **Título**: Bienvenido a JorgeCyberpunkTCG
- **Slug**: `bienvenido-a-jorgecyberpunktcg`
- **Categoría**: Plataforma (creada)
- **Estado**: Publicado (`PUBLISHED`)
- **Resumen**: Introducción a la plataforma independiente JorgeCyberpunkTCG: nuestra visión en fase prelaunch, la estructura del sitio y las herramientas disponibles para el usuario.

### Guía 2
- **Título**: Cómo usar tu Cyberdeck: Choomdex, cartas y mazos
- **Slug**: `como-usar-tu-cyberdeck`
- **Categoría**: Plataforma (creada)
- **Estado**: Publicado (`PUBLISHED`)
- **Resumen**: Manual de uso para las herramientas de JorgeCyberpunkTCG: aprende a consultar el Choomdex, examina la información de las cartas y gestiona tus mazos.

### Estrategia 1
- **Título**: Antes de construir: define el propósito de tu mazo
- **Slug**: `antes-de-construir-define-el-proposito-de-tu-mazo`
- **Categoría**: Construcción de Mazos (creada)
- **Estado**: Publicado (`PUBLISHED`)
- **Resumen**: Reflexiones sobre planificación de mazos: aprende a establecer un objetivo claro, evaluar la función de cada carta y revisar decisiones con método.

## Validación de URLs
Comprobación mediante cliente HTTP local (HTTP_HOST='127.0.0.1'):
- `/guias/` -> HTTP 200 OK
- `/guias/bienvenido-a-jorgecyberpunktcg/` -> HTTP 200 OK
- `/guias/como-usar-tu-cyberdeck/` -> HTTP 200 OK
- `/estrategias/` -> HTTP 200 OK
- `/estrategias/antes-de-construir-define-el-proposito-de-tu-mazo/` -> HTTP 200 OK
- `/` (Home) -> HTTP 200 OK (comportamiento confirmado: la Home estática no requiere forzar la inclusión de artículos).

## Conteos antes
- **Categorías**: 0
- **Guías**: 0
- **Estrategias**: 0
- **Videos**: 0
- **Cartas**: 4
- **CardPrinting**: 4
- **Mazos**: 1
- **Usuarios**: 3

## Conteos después
- **Categorías**: 2 (`Plataforma`, `Construcción de Mazos`)
- **Guías**: 2 (`bienvenido-a-jorgecyberpunktcg`, `como-usar-tu-cyberdeck`)
- **Estrategias**: 1 (`antes-de-construir-define-el-proposito-de-tu-mazo`)
- **Videos**: 0 (sin cambios)
- **Cartas**: 4 (sin cambios)
- **CardPrinting**: 4 (sin cambios)
- **Mazos**: 1 (sin cambios)
- **Usuarios**: 3 (sin cambios)

## Verificación de no regresión
- Cero modificaciones de código funcional (Python, HTML, CSS, JS, modelos, vistas, URLs, settings, tests, migraciones).
- 163 tests de la suite ejecutan y pasan correctamente.

## Archivos modificados
- `docs/ROADMAP.md`

## Archivos creados
- `docs/P1_3A_EDITORIAL_FOUNDATION.md`

## Datos modificados
Escritura controlada exclusiva en la base de datos SQLite local:
- 2 registros creados en `ContentCategory`.
- 3 registros creados, refinados y publicados en `Article`.

## Producción
NO MODIFICADA.

## Revisión editorial posterior

- **Revisión manual del propietario**: Efectuada tras la ejecución previa.
- **Markdown crudo detectado**: Identificado el renderizado literal de marcas Markdown (`###`, `**`) en `article_detail.html`.
- **Causa encontrada**: La plantilla renderiza `article.body` mediante el filtro `|linebreaks` como texto plano. El modelo y las vistas no contienen ni requieren un parser de Markdown.
- **Solución utilizada (Opción A)**: Se reestructuró el cuerpo de los 3 artículos a texto plano limpio y ordenado en párrafos naturales sin sintaxis Markdown visible. No se añadieron librerías externas ni se modificaron código o plantillas.
- **Seguridad**: Totalmente preservada. Sin inclusión de `|safe`, `mark_safe()`, `autoescape off` ni contenido HTML.
- **Afirmaciones eliminadas/reformuladas**:
  - *Guía 1*: Eliminada la afirmación de que la Home despliega automáticamente guías/estrategias o actividad reciente. Aclarado que la Biblioteca de Mazos se encuentra en estado inicial a la espera de publicaciones públicas.
  - *Guía 2*: Eliminada la promesa de "filtrado y búsqueda" futura. Eliminada la referencia a "Navegación Relacionada" (al no existir en el detalle de cartas). Precisado el alcance del Archivo Personal de Mazos y la Biblioteca Pública.
  - *Estrategia 1*: Eliminados supuestos de mecánica no verificados ("alto costo", "fases tempranas", "curva de recursos", "inactivas en la mano", "alterar la iniciativa"). Sustituida la taxonomía rígida de cartas por preguntas analíticas neutrales de evaluación.
- **Limpieza de artefactos temporales**: El directorio `scratch/` y los scripts de carga/actualización fueron eliminados por completo del entorno de trabajo.
- **Resultado final**: Textos legibles, precisos y seguros. 163 tests OK.
