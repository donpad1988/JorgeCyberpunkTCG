# P1.3A — Controlled Editorial Production Deployment

## Estado
COMPLETADA Y VALIDADA EN PRODUCCIÓN

## Objetivo
Desplegar exclusivamente el contenido editorial aprobado de la fase P1.3A (2 categorías, 3 artículos) a la base de datos de producción en PythonAnywhere de forma determinista, idempotente y segura, sin copiar ni sobrescribir la base de datos local.

## Fuente Canónica
La fuente de datos para `title`, `summary`, `body`, `article_type`, `category_slug`, `status` y `published_at` es la versión corregida y aprobada localmente en P1.3A:
- **Categoría 1**: `plataforma` (Plataforma)
- **Categoría 2**: `construccion-de-mazos` (Construcción de Mazos)
- **Guía 1**: `bienvenido-a-jorgecyberpunktcg`
- **Guía 2**: `como-usar-tu-cyberdeck`
- **Estrategia 1**: `antes-de-construir-define-el-proposito-de-tu-mazo`

## Mecanismo de Despliegue
- **Comando Django**: `apps/content/management/commands/load_p1_3a_editorial_content.py`
- **Atomicidad**: Operaciones encapsuladas en `transaction.atomic()`. Ante cualquier error o conflicto, se realiza rollback automático total.
- **Idempotencia**:
  - Si una categoría o artículo no existe: `CREATE`.
  - Si existe y coincide exactamente en todos sus campos clave: `EXISTS` (no se modifica nada).
  - Si existe pero difiere en algún campo: `CONFLICT` (aborta inmediatamente sin alterar registros).
- **Autor**: Resuelto de forma estable y case-insensitive mediante `User.objects.filter(username__iexact="jorgecyberpunktcg")` (resuelve `JORGECYBERPUNKTCG` o `jorgecyberpunktcg`). Aborta si no hay coincidencia o existen múltiples coincidencias.
- **Soporte Dry-Run**: Flag `--dry-run` para pre-validación sin persistencia de datos.

## Pruebas Automáticas del Cargador
Implementadas en `apps/content/tests/test_load_p1_3a_command.py` (12/12 tests passing, total suite 171 tests OK):
1. Creación en base limpia (2 categorías, 3 artículos).
2. Idempotencia en segunda ejecución (salida `EXISTS`).
3. Verificación del flag `--dry-run` (0 cambios persistidos).
4. Aborto por ausencia de usuario autor.
5. Aborto y rollback ante conflicto de categoría.
6. Aborto y rollback ante conflicto de artículo.
7. No alteración de registros no relacionados.
8. Visibilidad pública inmediata vía `Article.objects.publicly_visible()`.

## Procedimiento de Despliegue en PythonAnywhere
1. **Ruta en producción**: `/home/jorgecyberpunktcg/JorgeCyberpunkTCG`
2. **Respaldo previo de SQLite en producción**: Executado `python scripts/backup_sqlite.py` (`integrity_check` OK).
3. **Actualización de código**: `git pull origin main` (Commit `ecec50c Add controlled P1.3A editorial deployment`).
4. **Verificación Django**: `python manage.py check --settings=config.settings.production` (0 issues).
5. **Dry-Run en producción**: `python manage.py load_p1_3a_editorial_content --dry-run --settings=config.settings.production` (2 categorías `CREATE`, 3 artículos `CREATE`, 0 conflictos).
6. **Carga real**: `python manage.py load_p1_3a_editorial_content --settings=config.settings.production` (2 categorías creadas, 3 artículos creados).
7. **Segunda Dry-Run de verificación**: `python manage.py load_p1_3a_editorial_content --dry-run --settings=config.settings.production` (5 registros `EXISTS`, 0 `CREATE`, 0 `CONFLICT`).

## Conteos en Producción (Antes / Después)
- **ContentCategory**: 0 $\rightarrow$ 2 (`Plataforma`, `Construcción de Mazos`)
- **Guías (Article GUIDE)**: 0 $\rightarrow$ 2 (`bienvenido-a-jorgecyberpunktcg`, `como-usar-tu-cyberdeck`)
- **Estrategias (Article STRATEGY)**: 0 $\rightarrow$ 1 (`antes-de-construir-define-el-proposito-de-tu-mazo`)
- **Videos**: 0 $\rightarrow$ 0 (Sin cambios)
- **Cards**: 4 $\rightarrow$ 4 (Sin cambios)
- **CardPrinting**: 4 $\rightarrow$ 4 (Sin cambios)
- **Decks**: 1 $\rightarrow$ 1 (Sin cambios)
- **Users**: 3 $\rightarrow$ 3 (Sin cambios)

## Validación de URLs e Infraestructura
- `https://jorgecyberpunktcg.pythonanywhere.com/guias/` $\rightarrow$ **HTTP 200 OK**
- `https://jorgecyberpunktcg.pythonanywhere.com/guias/bienvenido-a-jorgecyberpunktcg/` $\rightarrow$ **HTTP 200 OK**
- `https://jorgecyberpunktcg.pythonanywhere.com/guias/como-usar-tu-cyberdeck/` $\rightarrow$ **HTTP 200 OK**
- `https://jorgecyberpunktcg.pythonanywhere.com/estrategias/` $\rightarrow$ **HTTP 200 OK**
- `https://jorgecyberpunktcg.pythonanywhere.com/estrategias/antes-de-construir-define-el-proposito-de-tu-mazo/` $\rightarrow$ **HTTP 200 OK**
- **Formato**: Sin Markdown crudo, sin HTML expuesto, texto estructurado en párrafos limpios.
- **Seguridad**: `Strict-Transport-Security: max-age=3600` verificado en producción.
