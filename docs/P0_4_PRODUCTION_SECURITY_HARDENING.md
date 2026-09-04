# P0.4 — AUDITORÍA Y ENDURECIMIENTO DE SEGURIDAD EN PRODUCCIÓN (HSTS)

**Proyecto:** JorgeCyberpunkTCG
**Entorno:** PythonAnywhere (`https://jorgecyberpunktcg.pythonanywhere.com/`)
**Estado:** IMPLEMENTACIÓN LOCAL COMPLETADA / VALIDACIÓN PRODUCCIÓN PENDIENTE

---

## 1. RESUMEN DE LA AUDITORÍA TÉCNICA DE SEGURIDAD

La auditoría técnica realizada sobre el entorno de producción (`config/settings/production.py`) confirmó que la aplicación mantiene una postura de seguridad altamente sólida:

*   **Variables de Entorno y Secretos:** `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y credenciales de correo SMTP se gestionan fuera de Git a través de variables de entorno en WSGI.
*   **Depuración Desactivada:** `DEBUG = False` configurado de forma incondicional.
*   **Aislamiento HTTPS y Cookies:** `SECURE_SSL_REDIRECT = True`, `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`.
*   **Cabeceras de Protección Básicas:** `SECURE_CONTENT_TYPE_NOSNIFF = True` y `X_FRAME_OPTIONS = "DENY"`.

Al ejecutar `python manage.py check --deploy --settings=config.settings.production` se obtuvo **únicamente 1 WARNING**: `security.W004` (debido a `SECURE_HSTS_SECONDS = 0`). No se detectó ningún otro warning o error de configuración.

---

## 2. ACTIVACIÓN PROGRESIVA CONSERVADORA DE HSTS (P0.4B)

HTTP Strict Transport Security (HSTS) es una cabecera de seguridad HTTP (`Strict-Transport-Security`) enviada por la aplicación que instruye a los navegadores web a convertir automáticamente cualquier intento de conexión HTTP en HTTPS antes de realizar la solicitud de red.

Para evitar bloqueos irreversibles o problemas de conectividad en el cliente, la implementación de HSTS se realiza de forma **conservadora y progresiva**:

### Configuración P0.4B en `config/settings/production.py`:
```python
# Progressive HSTS strategy (initial conservative stage: max-age=3600 / 1 hour)
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
```

### Parámetros seleccionados y justificación técnica:

1.  **Duración Inicial (`max-age=3600` / 1 Hora):**
    Proporciona la protección básica de HSTS en producción permitiendo un periodo de ventana muy corto en el navegador del usuario. Si ocurriera una eventualidad crítica de infraestructura, la política expirará en los clientes en solo 1 hora.
2.  **`SECURE_HSTS_INCLUDE_SUBDOMAINS = False`:**
    JorgeCyberpunkTCG opera sobre el subdominio administrado `jorgecyberpunktcg.pythonanywhere.com`. Como no existen sub-subservicios bajo dicho subdominio, desactivar esta directiva evita complejidades innecesarias sin comprometer la seguridad del sitio principal.
3.  **`SECURE_HSTS_PRELOAD = False`:**
    El registro de precarga HSTS en navegadores (*Chrome/Firefox HSTS Preload List*) está reservado exclusivamente para dominios apex / TLD (ej. `pythonanywhere.com`) con `includeSubDomains`. Un subdominio de un servicio de hosting compartido **no puede ni debe** agregarse a la lista global de preload.

---

## 3. DECISIONES ARQUITECTÓNICAS Y EXCLUSIONES DEL ALCANCE

Para mantener este bloque como un cambio pequeño, aislado, testeable y fácilmente reversible, se excluyeron deliberadamente las siguientes configuraciones:

1.  **Diferimiento de `SECURE_PROXY_SSL_HEADER`:**
    La directiva `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` exige verificar previamente que la infraestructura de proxies inversos de PythonAnywhere configure y sanitice de forma confiable el encabezado `X-Forwarded-Proto` en cada petición entrante. No debe agregarse únicamente por la presencia de un reverse proxy sin validación explícita de cabeceras de red.
2.  **Diferimiento de `SECURE_REFERRER_POLICY`:**
    Se evaluará en una fase posterior para mantener P0.4B enfocado únicamente en la activación conservadora de HSTS.

---

## 4. CRONOGRAMA FUTURO DE INCREMENTO DE HSTS

Una vez validada la Etapa 1 en producción durante el periodo prelaunch, la duración del `max-age` se incrementará progresivamente mediante la variable de entorno `DJANGO_SECURE_HSTS_SECONDS`:

| Etapa | Estado | Duración (`max-age`) | Objetivo / Condición de paso |
| :--- | :--- | :--- | :--- |
| **Etapa 1 (P0.4B)** | **Actual** | **3,600 segundos (1 hora)** | Validación inicial de envío de la cabecera en PythonAnywhere. |
| **Etapa 2 (Estabilización)** | Pendiente | 2,592,000 segundos (30 días) | Operación continua sin incidencias durante el pre-lanzamiento. |
| **Etapa 3 (Estado Estable)** | Pendiente | 31,536,000 segundos (1 año / 365 días) | Lanzamiento oficial (Octubre 2026). |

---

## 5. PROCEDIMIENTO DE ROLLBACK OPERACIONAL

En caso de requerirse la suspensión inmediata de la política HSTS en producción:

1.  Acceder a PythonAnywhere Web tab / WSGI configuration.
2.  Establecer la variable de entorno `DJANGO_SECURE_HSTS_SECONDS` en `"0"`:
    ```python
    os.environ["DJANGO_SECURE_HSTS_SECONDS"] = "0"
    ```
3.  Reiniciar la aplicación web (`touch /var/www/jorgecyberpunktcg_pythonanywhere_com_wsgi.py`).

> [!WARNING]
> **Advertencia sobre persistencia en clientes:** La directiva HSTS almacenada por los navegadores de usuarios que hayan visitado el sitio mientras HSTS estaba activo permanecerá en el cliente hasta que expire el tiempo indicado en `max-age` (3,600 segundos en la Etapa 1).

---

## 6. PROCEDIMIENTO DE VALIDACIÓN EN PYTHONANYWHERE (DESPLIEGUE P0.4B)

Cuando se autorice el despliegue en producción:

1.  Acceder a la consola Bash de PythonAnywhere.
2.  Navegar a la carpeta del proyecto y verificar status limpio.
3.  Ejecutar el backup pre-deploy de SQLite (P0.3):
    ```bash
    python scripts/backup_sqlite.py --source db.sqlite3 --destination-dir /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG --label pre_P0.4
    ```
4.  Descargar los cambios: `git pull origin main`.
5.  Recopilar estáticos: `python manage.py collectstatic --noinput --settings=config.settings.production`.
6.  Reload de la aplicación: `touch /var/www/jorgecyberpunktcg_pythonanywhere_com_wsgi.py`.
7.  Verificar en la respuesta HTTP la presencia del encabezado:
    ```bash
    curl -I https://jorgecyberpunktcg.pythonanywhere.com/
    ```
    *Respuesta esperada:* `Strict-Transport-Security: max-age=3600`
8.  Inspeccionar la salida de las últimas 50 líneas del log de errores:
    `tail -n 50 /var/log/jorgecyberpunktcg.pythonanywhere.com.error.log`.
