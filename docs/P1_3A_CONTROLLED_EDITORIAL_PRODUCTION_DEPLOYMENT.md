# P1.3A — Controlled Editorial Production Deployment

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
- **Autor**: Resuelto de forma estable mediante `User.objects.get(username="jorgecyberpunktcg")`. Si el usuario no existe en la base destino, la ejecución aborta.
- **Soporte Dry-Run**: `--dry-run` ejecuta toda la validación dentro de una transacción con rollback forzado, retornando los estados que se aplicarían sin alterar la base de datos.

## Pruebas Automáticas del Cargador
Implementadas en `apps/content/tests/test_load_p1_3a_command.py` (12/12 tests passing):
1. Creación en base limpia (2 categorías, 3 artículos).
2. Idempotencia en segunda ejecución (salida `EXISTS`).
3. Verificación del flag `--dry-run` (0 cambios persistidos).
4. Aborto por ausencia de usuario autor.
5. Aborto y rollback ante conflicto de categoría.
6. Aborto y rollback ante conflicto de artículo.
7. No alteración de registros no relacionados.
8. Visibilidad pública inmediata vía `Article.objects.publicly_visible()`.

## Procedimiento de Despliegue en Producción
1. **Push del cargador**: `git push origin main` con el comando y sus tests.
2. **Pre-check en PythonAnywhere**: Verificar repositorio limpio en `/home/jorgecyberpunktcg/JorgeCyberpunkTCG`.
3. **Backup en producción**: Ejecutar `python scripts/backup_sqlite.py` antes de cualquier escritura.
4. **Git pull**: Actualizar repositorio en producción (`git pull origin main`).
5. **Check**: Ejecutar `python manage.py check` y `python manage.py makemigrations --check`.
6. **Dry-Run en producción**: Ejecutar `python manage.py load_p1_3a_editorial_content --dry-run`.
7. **Carga real**: Ejecutar `python manage.py load_p1_3a_editorial_content`.
8. **Segunda Dry-Run de verificación**: Confirmar idempotencia (5 `EXISTS`).
9. **Validación HTTP**: Verificar respuesta HTTP 200 en las 5 URLs públicas.
10. **Seguridad e HSTS**: Confirmar que HSTS permanece en 3600 segundos (`Strict-Transport-Security: max-age=3600`).
