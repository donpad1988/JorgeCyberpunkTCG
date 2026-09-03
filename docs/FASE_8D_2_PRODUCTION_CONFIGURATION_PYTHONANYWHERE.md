# FASE 8D.2 — CONFIGURACIÓN DE PRODUCCIÓN PARA PYTHONANYWHERE + SQLITE

## SECCIÓN A: CAMBIOS IMPLEMENTADOS EN CÓDIGO

Se ha preparado la base técnica del proyecto para su despliegue seguro en **PythonAnywhere** utilizando **SQLite** como motor de base de datos MVP y el servido estático nativo de la plataforma.

### 1. Configuración de Producción (`config/settings/production.py`)
- **Base de Datos**: Se mantiene SQLite `db.sqlite3` en la raíz del proyecto (`ROOT_DIR / "db.sqlite3"`), aprovechando el sistema de archivos persistente de PythonAnywhere sin requerir PostgreSQL ni drivers adicionales.
- **Estrategia HSTS Progresiva**: Se desactivó el HSTS agresivo pre-lanzamiento fijando `SECURE_HSTS_SECONDS = 0`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = False` y `SECURE_HSTS_PRELOAD = False` para permitir la verificación progresiva de SSL en producción.
- **CSRF Trusted Origins**: Se añadió soporte para `CSRF_TRUSTED_ORIGINS` leyendo la variable de entorno `DJANGO_CSRF_TRUSTED_ORIGINS` (lista separada por comas).
- **Correo SMTP Configurable**: Se añadió soporte para backend de correo en producción vía variables de entorno (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`), manteniendo aislamiento en entorno de pruebas.
- **Logging a Consola**: Se configuró `LOGGING` dirigiendo los niveles `WARNING` y `ERROR` a `StreamHandler` (`stdout`/`stderr`), capturados automáticamente por los archivos de log del panel Web de PythonAnywhere.

### 2. Páginas de Error Personalizadas
- `templates/404.html`: Plantilla con estética cibernética *Neural Interface*, en español, responsive y accesible ("SEÑAL NO ENCONTRADA") con CTA hacia inicio y metadato `noindex, nofollow`.
- `templates/500.html`: Plantilla de fallo crítico ("FALLO DEL SISTEMA") que no expone stack traces, variables ni datos internos de configuración.

### 3. Endpoint de Monitoreo (`/health/`)
- Mapeado en `/health/` retornando `200 OK` con JSON `{"status": "healthy"}` y cabecera `X-Robots-Tag: noindex, nofollow`.
- Consulta barata sin acceso a base de datos ni revelación de versiones o datos internos. Excluido explícitamente del `sitemap.xml`.

---

## SECCIÓN B: PROCEDIMIENTO FUTURO DE DESPLIEGUE EN PYTHONANYWHERE

*(Guía paso a paso para ejecutar durante la Fase 8D.3. No requiere ejecución actual)*.

> **Placeholders de referencia**:
> - `<PA_USERNAME>`: Nombre de usuario de la cuenta en PythonAnywhere.
> - `<DOMAIN>`: Dominio asignado (ej. `<PA_USERNAME>.pythonanywhere.com` o dominio propio).
> - `<SECRET_KEY>`: Clave secreta generada para producción.

### Pasos de Despliegue:

1. **Crear cuenta en PythonAnywhere**: Registrarse en la plataforma y acceder al Dashboard.
2. **Abrir Bash Console en PythonAnywhere**: Desde la pestaña *Consoles*, iniciar una consola Bash.
3. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/JorgeCyberpunkTCG.git /home/<PA_USERNAME>/JorgeCyberpunkTCG
   cd /home/<PA_USERNAME>/JorgeCyberpunkTCG
   ```
4. **Crear y activar Virtual Environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 jorgecyberpunk-venv
   # O alternativamente: python3 -m venv .venv && source .venv/bin/activate
   ```
5. **Instalar dependencias directas**:
   ```bash
   pip install -r requirements.txt
   ```
6. **Configurar Variables de Entorno en PythonAnywhere**:
   En el archivo WSGI o mediante archivo `.env` local en servidor inyectar:
   ```bash
   export DJANGO_SETTINGS_MODULE="config.settings.production"
   export DJANGO_SECRET_KEY="<SECRET_KEY>"
   export DJANGO_ALLOWED_HOSTS="<DOMAIN>"
   export DJANGO_CSRF_TRUSTED_ORIGINS="https://<DOMAIN>"
   ```
7. **Ejecutar migraciones en producción**:
   ```bash
   python manage.py migrate --noinput
   ```
8. **Compilar archivos estáticos (`collectstatic`)**:
   ```bash
   python manage.py collectstatic --noinput
   ```
9. **Configurar Web App en PythonAnywhere**:
   - En la pestaña *Web*, crear una nueva Web App seleccionando *Manual configuration* con Python 3.x.
10. **Configurar WSGI Configuration File**:
    En el editor del archivo WSGI de PythonAnywhere (`/var/www/<PA_USERNAME>_pythonanywhere_com_wsgi.py`):
    ```python
    import os
    import sys

    path = '/home/<PA_USERNAME>/JorgeCyberpunkTCG'
    if path not in sys.path:
        sys.path.append(path)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
    os.environ['DJANGO_SECRET_KEY'] = '<SECRET_KEY>'
    os.environ['DJANGO_ALLOWED_HOSTS'] = '<DOMAIN>'

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    ```
11. **Mapear Static Files en el panel Web**:
    - URL: `/static/`
    - Directory: `/home/<PA_USERNAME>/JorgeCyberpunkTCG/staticfiles`
12. **Activar HTTPS**:
    - Habilitar opción *Force HTTPS* en la pestaña *Web* de PythonAnywhere.
13. **Crear Superusuario de Producción**:
    ```bash
    python manage.py createsuperuser
    ```
14. **Recargar Web App**:
    Hacer clic en el botón verde **Reload <DOMAIN>** en la pestaña *Web*.
15. **Verificar Endpoint de Salud**:
    Visitar `https://<DOMAIN>/health/` y confirmar respuesta `{"status": "healthy"}`.
16. **Verificar SEO e Infraestructura**:
    Comprobar `https://<DOMAIN>/sitemap.xml`, `https://<DOMAIN>/robots.txt` y `<link rel="canonical">`.
17. **Inspeccionar Logs de Consola**:
    Revisar los archivos `/var/log/<PA_USERNAME>_pythonanywhere_com.server.log` y `error.log`.
18. **Copia de Seguridad Inicial**:
    Descargar copia inicial del archivo `/home/<PA_USERNAME>/JorgeCyberpunkTCG/db.sqlite3`.
