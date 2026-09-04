# P0.1 — EMAIL & ACCOUNT RECOVERY EN PRODUCCIÓN

## 1. OBJETIVO

Documentar y formalizar la resolución técnica del bloque de infraestructura **P0.1 — Email & Account Recovery** para la plataforma **JorgeCyberpunkTCG**, validada en el entorno de producción real hosted en PythonAnywhere (`https://jorgecyberpunktcg.pythonanywhere.com/`).

El propósito de este bloque fue garantizar que el flujo nativo de recuperación de contraseña de Django (`PasswordResetView`, `PasswordResetDoneView`, `PasswordResetConfirmView`, `PasswordResetCompleteView`) funcione correctamente de extremo a extremo (end-to-end) enviando correos transaccionales reales mediante Gmail SMTP sin exponer credenciales ni fallar con errores de conexión en el servidor.

---

## 2. ESTADO FINAL

* **Estado:** `COMPLETADO Y VALIDADO EN PRODUCCIÓN`
* **Servicio de Correo:** Gmail SMTP (`smtp.gmail.com:587` con TLS).
* **Cuenta Remitente Oficial:** `jorgecyberpunktcg@gmail.com`
* **Autenticación:** Contraseña de Aplicación (Gmail App Password) configurada operacionalmente en la capa WSGI de PythonAnywhere.
* **Resultado del Flujo:** Validado exitosamente. Se recibió en la bandeja de entrada real el correo con la URL HTTPS canónica de restablecimiento de contraseña sobre el dominio de producción.

---

## 3. ARQUITECTURA DE CORREO EN PRODUCCIÓN

La arquitectura de correo del proyecto en el entorno de producción combina la configuración modular de Django en `config.settings.production` con las variables de entorno inyectadas en la capa del servidor WSGI administrado por PythonAnywhere:

```text
[Cliente Web / Formulario]
       │ (POST /cuenta/password-reset/)
       ▼
[Django PasswordResetView]
       │
       ▼ (Lee settings.EMAIL_* desde os.environ)
[django.core.mail.backends.smtp.EmailBackend]
       │
       ▼ (Conexión TLS Encriptada - Puerto 587)
[smtp.gmail.com:587] ──(Autenticación App Password)──► [Bandeja de Entrada Usuario]
```

### Configuración en Django (`config/settings/production.py`):
```python
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in {"1", "true", "yes", "on"}
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")
```

---

## 4. PRUEBAS REALIZADAS Y RESULTADOS

Las pruebas operativas se realizaron directamente en la consola Bash y en la interfaz web de PythonAnywhere:

### Prueba A — Conectividad TCP SMTP
* **Comando:** Verificación de socket TCP hacia `smtp.gmail.com` en puerto `587`.
* **Resultado:** `OK` — Conexión TCP exitosa desde los servidores de PythonAnywhere hacia el puerto 587 de Google.

### Prueba B — Autenticación SMTP Manual
* **Cuenta probada:** `jorgecyberpunktcg@gmail.com` mediante App Password dedicada.
* **Resultado:** `OK` — Autenticación SMTP aceptada por Google.

### Prueba C — Envío SMTP Directo
* **Prueba:** Transmisión directa de correo de prueba desde la instancia PythonAnywhere hacia `jorgecyberpunktcg@gmail.com`.
* **Resultado:** Correo entregado y verificado en bandeja de entrada.

---

## 5. PROBLEMA DETECTADO EN EL FLUJO DJANGO

Durante la primera prueba del flujo web de restablecimiento de contraseña en producción (`/cuenta/password-reset/`), se observó el siguiente comportamiento:

1. El usuario ingresaba su correo y la aplicación mostraba la vista de confirmación *"REVISA TU CORREO"*.
2. El correo transaccional **no llegaba** a la bandeja de entrada.
3. El log de errores de PythonAnywhere (`/var/log/...error.log`) permanecía vacío o sin registrar fallos SMTP.

---

## 6. CAUSA RAÍZ

Al inspeccionar la configuración del servidor web en PythonAnywhere (`/var/www/jorgecyberpunktcg_pythonanywhere_com_wsgi.py`), se identificó que las variables de entorno operacionales (`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, etc.) habían sido declaradas **DESPUÉS** de la invocación:

```python
# SINTAXIS CON PROBLEMA (INCORRECTA)
application = get_wsgi_application()

# Las variables EMAIL_* se definían después de instanciar WSGI
os.environ["EMAIL_HOST"] = "smtp.gmail.com"
...
```

Dado que `get_wsgi_application()` desencadena la inicialización de Django y la carga del módulo `config.settings.production`, los valores por defecto vacíos eran evaluados al arrancar el proceso de la aplicación WSGI. Al momento de enviar el correo, Django utilizaba `EMAIL_HOST = ""` (vacío), fallando silenciosamente la conexión o no alcanzando el servidor SMTP de Gmail.

---

## 7. CORRECCIÓN APLICADA EN WSGI

Se reorganizó la estructura del script WSGI operacional en PythonAnywhere para garantizar que **todas las variables de entorno de producción** (incluyendo secretos, hosts permitidos y configuración SMTP) sean inyectadas en `os.environ` **ANTES** de invocar `get_wsgi_application()`.

### Orden Conceptual Correcto del WSGI:
1. `import os, sys`
2. Configuración de `PROJECT_PATH` y `sys.path`
3. Asignación de `DJANGO_SETTINGS_MODULE` (`config.settings.production`)
4. Asignación de `DJANGO_SECRET_KEY`
5. Asignación de `DJANGO_ALLOWED_HOSTS`
6. Asignación de `DJANGO_CSRF_TRUSTED_ORIGINS`
7. Asignación de variables `EMAIL_*` (`EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`)
8. `from django.core.wsgi import get_wsgi_application`
9. `application = get_wsgi_application()`

---

## 8. VALIDACIÓN END-TO-END EN PRODUCCIÓN

Tras guardar los cambios en el WSGI y recargar (*Reload*) la webapp en PythonAnywhere:

1. Se navegó al flujo real `/cuenta/password-reset/`.
2. Se solicitó la recuperación para la cuenta del superusuario oficial de producción.
3. Django procesó la solicitud mostrando la plantilla de éxito `password_reset_done.html`.
4. El log de errores de WSGI permaneció completamente limpio.
5. Se confirmó la recepción en Gmail de la notificación con el asunto:  
   **"Restablece tu acceso a Jorge CyberpunkTCG"**.
6. El cuerpo del correo contenía el enlace canónico HTTPS válido:  
   `https://jorgecyberpunktcg.pythonanywhere.com/cuenta/password-reset/MQ/set-password/`
7. El token y link HTTPS fueron verificados. La contraseña existente permaneció intacta y segura.

**Conclusión:** El flujo de restablecimiento de contraseña queda **100% verificado y funcional** para usuarios en producción.

---

## 9. GESTIÓN DE SECRETOS Y DISTINCIÓN DE CAPAS

* **Aislamiento en Git:** El archivo WSGI `/var/www/jorgecyberpunktcg_pythonanywhere_com_wsgi.py` pertenece exclusivamente al entorno de ejecución en PythonAnywhere y **NO forma parte del repositorio Git**.
* **Protección de Credenciales:** La contraseña de aplicación de Gmail (App Password) y la clave `DJANGO_SECRET_KEY` residen únicamente en la infraestructura del servidor de hosting. **Ningún secreto está o estará commiteado en el repositorio de GitHub.**

---

## 10. PROCEDIMIENTO DE DIAGNÓSTICO EN CASO DE FALLO DE CORREO

Si en el futuro los correos transaccionales dejaran de entregarse, seguir este procedimiento secuencial sin imprimir contraseñas:

1. **Estado Web:** Verificar que el sitio responde `200 OK` en `/health/`.
2. **Conectividad Saliente:** Abrir consola Bash en PythonAnywhere y probar puerto 587 (`python3 -c "import socket; s=socket.create_connection(('smtp.gmail.com', 587), timeout=5); print(s)"`).
3. **Estado de App Password:** Verificar en la cuenta de Google (`jorgecyberpunktcg@gmail.com`) que la contraseña de aplicación continúe activa y no haya sido revocada.
4. **Orden en WSGI:** Confirmar en el archivo WSGI de PythonAnywhere que las líneas `os.environ["EMAIL_*"]` precedan a `get_wsgi_application()`.
5. **Reload:** Ejecutar *Reload* desde el panel web de PythonAnywhere.
6. **Prueba Controlada:** Solicitar restablecimiento en `/cuenta/password-reset/` hacia la cuenta oficial y revisar `/var/log/...error.log`.

---

## 11. CRITERIOS DE ACEPTACIÓN CUMPLIDOS

- [x] Conectividad SMTP con Gmail probada y operativa desde el hosting.
- [x] Variables de entorno inyectadas antes de la inicialización de WSGI.
- [x] Flujo de Password Reset de Django probado de extremo a extremo.
- [x] Enlace canónico HTTPS entregado correctamente por correo.
- [x] Repositorio Git libre de contraseñas, secretos y datos sensibles.

---

## 12. RESULTADO FINAL

**COMPLETADO — P0.1 Email & Account Recovery está plenamente operativo en producción.**
