# FASE 14 — CIERRE DOCUMENTAL DEL DESPLIEGUE INICIAL EN PRODUCCIÓN (PYTHONANYWHERE)

## A. Objetivo

Documentar formalmente la ejecución, arquitectura final y procedimiento operativo del **despliegue técnico inicial en producción** del proyecto **JorgeCyberpunkTCG** en la plataforma **PythonAnywhere**.

Este hito representa la estabilización de la infraestructura base (MVP) en un entorno real con acceso vía HTTPS, sirviendo como plataforma de integración y pruebas pre-lanzamiento de cara al lanzamiento oficial del juego TCG previsto para **octubre de 2026**.

---

## B. Arquitectura Final Utilizada

- **Plataforma de Hosting**: PythonAnywhere Web App.
- **Motor de Base de Datos**: SQLite (`db.sqlite3`) limpia en la raíz del proyecto en producción.
- **Servido de Archivos Estáticos**: Mapeo estático nativo administrado directamente por Nginx/PythonAnywhere (sin WhiteNoise).
- **Servidor WSGI**: WSGI Native Managed por PythonAnywhere (sin Gunicorn ni uWSGI adicional).
- **Aislamiento**: Entorno virtual independiente (`.venv`).
- **Base de Datos No Relacional / Servidores Externos**: Excluidos deliberadamente para el MVP (sin PostgreSQL, Redis ni Celery).

---

## C. Repositorio GitHub

- **URL del Repositorio**: `https://github.com/donpad1988/JorgeCyberpunkTCG.git`
- **Rama Desplegada**: `main`
- **Último Commit de Producción**: `59f92bc` (*Preparar configuración de producción para PythonAnywhere*)

---

## D. URL de Producción

- **URL Pública**: `https://jorgecyberpunktcg.pythonanywhere.com/`

---

## E. Versiones del Stack

- **Python (Entorno Local de Desarrollo)**: 3.13.14
- **Python (Servidor PythonAnywhere)**: 3.13.1
- **Django**: 6.0.6

---

## F. Directorios de Producción en PythonAnywhere

- **Código Fuente (Root Directory)**: `/home/jorgecyberpunktcg/JorgeCyberpunkTCG`
- **Directorio de Recopilación Estática (`STATIC_ROOT`)**: `/home/jorgecyberpunktcg/JorgeCyberpunkTCG/staticfiles`

---

## G. Virtualenv de Producción

- **Ruta del Entorno Virtual**: `/home/jorgecyberpunktcg/JorgeCyberpunkTCG/.venv`

---

## H. Configuración Django de Producción

- **Módulo de Settings Activo**: `config.settings.production`

---

## I. Estrategia de Variables de Entorno y Seguridad

- Las variables de entorno sensibles (claves secretas, credenciales, hosts autorizados) **NO están versionadas en Git**.
- La clave `DJANGO_SECRET_KEY` está configurada directamente en el servidor de producción (vía archivo de configuración WSGI de PythonAnywhere).
- **Regla Estricta de Gobernanza**: Ningún secreto, contraseña de superusuario ni clave de API se documenta, imprime, versiona o reconstruye en el repositorio de código ni en la documentación.

---

## J. Estado de la Base de Datos en Producción

- **Motor**: SQLite (`db.sqlite3`).
- **Estado Inicial**: Base de datos **limpia**, generada desde cero en producción mediante la ejecución directa de las migraciones de Django (`python manage.py migrate`).
- **Políticas de Ingesta y Migración de Datos**:
  - NO se copió el archivo `db.sqlite3` del entorno local de desarrollo.
  - NO se migraron cuentas de usuario de desarrollo.
  - NO se migró el mazo piloto local.
  - NO se migraron automáticamente cartas ni impresiones de prueba.
- **Superusuario**: Creado desde cero directamente en la consola de producción.

---

## K. Archivos Estáticos (Static Files)

- **Mapeo en Panel Web de PythonAnywhere**:
  - URL URL prefix: `/static/`
  - Directory: `/home/jorgecyberpunktcg/JorgeCyberpunkTCG/staticfiles`
- **Comando Ejecutado**: `python manage.py collectstatic --noinput --settings=config.settings.production`
- **Resultado**: **138 archivos estáticos** copiados satisfactoriamente al directorio `STATIC_ROOT`.

---

## L. Configuración WSGI

Conceptualmente, el archivo WSGI administrado por PythonAnywhere (`/var/www/jorgecyberpunktcg_pythonanywhere_com_wsgi.py`) realiza las siguientes funciones:
1. Añade `/home/jorgecyberpunktcg/JorgeCyberpunkTCG` al `sys.path`.
2. Asigna la variable de entorno `DJANGO_SETTINGS_MODULE = "config.settings.production"`.
3. Inyecta `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS` desde el entorno del servidor.
4. Inicializa la aplicación WSGI mediante `get_wsgi_application()`.

---

## M. Validaciones de Producción Realizadas

1. **Django Production Check**: `System check identified no issues (0 silenced)`.
2. **Migraciones**: Aplicadas correctamente 100% desde cero (`accounts`, `admin`, `auth`, `cards`, `content`, `contenttypes`, `decks`, `sessions`, `videos`).
3. **Superusuario**: Creado e instalado correctamente en producción.
4. **Archivos Estáticos**: 138 archivos servidos sin errores 404.
5. **Página Principal (Home)**: Funcional, con carga correcta de estilos e interfaz.
6. **Identidad Visual (Neural Interface)**: CSS fully functional y responsivo.
7. **Navegación**: Menús, enlaces y rutas operativas.
8. **Choomdex**: Operativo y vacío, reflejando fielmente la base limpia de producción.
9. **Endpoint de Salud (`/health/`)**: Retorna HTTP 200 OK con payload `{"status": "healthy"}`.
10. **Archivo `robots.txt`**: Servido dinámicamente con directivas correctas.
11. **Mapa del Sitio (`sitemap.xml`)**: XML válido generando únicamente URLs con protocolo `https://`.
12. **Redirección HTTPS**: Redirección automática de HTTP a HTTPS verificada.
13. **Comando `check --deploy`**:
    - Ejecutado: `python manage.py check --deploy --settings=config.settings.production`
    - Resultado: Solo emite la advertencia `security.W004` relativa a `SECURE_HSTS_SECONDS = 0`.

---

## N. Política HSTS (HTTP Strict Transport Security)

- **Configuración Actual**: `SECURE_HSTS_SECONDS = 0`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = False`, `SECURE_HSTS_PRELOAD = False`.
- **Justificación Técnica**: Esta configuración es una **decisión deliberada y temporal**. La estrategia aprobada es un **HSTS Progresivo**, el cual evita bloquear dominios o subdominios durante los primeros días/semanas de estabilización del servidor web y SSL. El valor se incrementará de forma paulatina una vez confirmada la estabilidad de producción a largo plazo.

---

## O. Estado del Contenido en Producción

La base de datos de producción se mantiene **intencionalmente limpia**. No se ingresarán conjuntos masivos de cartas ni mazos piloto sin validación previa. La ingesta de datos seguirá un canal estrictamente editorial y verificado.

---

## P. Procedimiento Estándar para Futuros Despliegues

Para desplegar futuras actualizaciones de código a producción, se debe seguir el siguiente flujo estandarizado:

### 1. En el Entorno Local de Desarrollo:
```bash
# Verify baseline state
git status
python manage.py check
python manage.py makemigrations --check
python manage.py test

# Commit and Push
git add .
git commit -m "feat/fix: descripción del cambio"
git push origin main
```

### 2. En la Consola Bash de PythonAnywhere:
```bash
cd /home/jorgecyberpunktcg/JorgeCyberpunkTCG
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
```

### 3. En el Panel Web de PythonAnywhere:
- Hacer clic en el botón verde **Reload jorgecyberpunktcg.pythonanywhere.com**.
- Verificar la respuesta en `https://jorgecyberpunktcg.pythonanywhere.com/health/`.

---

## Q. Estrategia de Rollback y Copias de Seguridad

- **Código Fuente**: Git permite revertir el código a cualquier commit previo mediante `git checkout` o `git reset`.
- **Base de Datos SQLite**:
  - > [!CAUTION]
  - > **Git NO es un sistema de backup de la base de datos**.
  - Antes de ejecutar migraciones complejas en producción, se debe generar un respaldo manual del archivo SQLite:
    ```bash
    cp /home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3 /home/jorgecyberpunktcg/backups/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3
    ```

---

## R. Pendientes Pre-lanzamiento (Prelaunch Backlog)

1. **Configuración de SMTP Real**: Integración de credenciales SMTP para habilitar el restablecimiento de contraseñas de usuarios externos.
2. **Revisión de Textos Legales**: Revisión final de la Política de Privacidad y Términos de Uso.
3. **Disclaimer de No Afiliación**: Verificación del aviso legal de independencia respecto a las marcas oficiales del TCG.
4. **Elevación de HSTS**: Configuración paulatina de `SECURE_HSTS_SECONDS` a valores de producción final.
5. **Crecimiento Editorial de Cartas**: Carga progresiva y manual de impresiones de cartas con autorización o datos públicos validados.
6. **Revisión de Cartas/Reglas en Lanzamiento (Octubre 2026)**: Auditoría de alineación cuando el juego oficial se lance formalmente.
7. **Estrategia de Copias de Seguridad**: Automatización de respaldos periódicos del archivo `db.sqlite3`.
8. **Monitoreo de Error Logs**: Revisión periódica de los logs de error de PythonAnywhere.
9. **Polishing Responsive**: Ajuste continuo de elementos de UI en dispositivos móviles (e.g. componentes de barra de navegación).
