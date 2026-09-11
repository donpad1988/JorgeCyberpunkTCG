# P0.4B — IMPLEMENTACIÓN Y ENDURECIMIENTO DE SEGURIDAD EN PRODUCCIÓN

**Proyecto:** JorgeCyberpunkTCG  
**Entorno de Producción Destino:** PythonAnywhere (`https://jorgecyberpunktcg.pythonanywhere.com/`)  
**Estado:** COMPLETADO Y VALIDADO EN LOCAL — PENDIENTE DE DESPLIEGUE CONTROLADO EN PYTHONANYWHERE  

---

## 1. OBJETIVO (A)

El objetivo de la fase **P0.4B — Production Security Hardening Implementation** es implementar de forma estructurada, comprobada y libre de regresiones los controles de seguridad de producción recomendados durante la auditoría P0.4:

1. Soporte para HSTS conservador (`Strict-Transport-Security`) a través de variable de entorno configurada en 3600 segundos (1 hora).
2. Configuración explícita del encabezado de proxy SSL (`SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`).
3. Definición estricta de la política de referente (`SECURE_REFERRER_POLICY = "same-origin"`).
4. Verificación de la estricta separación entre los entornos de desarrollo local y producción para garantizar que la navegación local (`http://127.0.0.1:8000/`) no se vea alterada o forzada a HTTPS.
5. Inclusión de suite de pruebas unitarias automatizadas de seguridad y regresión local.

---

## 2. BASELINE INICIAL (B)

Antes de realizar la implementación de P0.4B, se verificó el baseline real del proyecto en la rama `main` sincronizada con `origin/main` con el siguiente resultado:

* **Branch:** `main` (up to date with `origin/main`)
* **Working Tree:** Clean (sin cambios pendientes)
* **`python manage.py check`:** OK — `System check identified no issues (0 silenced)`
* **`python manage.py makemigrations --check`:** OK — `No changes detected`
* **`python manage.py test`:** OK — 158 tests ejecutados exitosamente en 160 segundos (`OK`).

---

## 3. CAMBIOS IMPLEMENTADOS (C)

Se modificaron y crearon los siguientes archivos mínimos requeridos:

| Archivo | Tipo de Cambio | Descripción |
| :--- | :--- | :--- |
| `config/settings/production.py` | MODIFICADO | Se añadieron `SECURE_PROXY_SSL_HEADER` y `SECURE_REFERRER_POLICY`. Se mantuvo `SECURE_HSTS_SECONDS` configurable vía entorno con valor por defecto de 3600s, `SECURE_HSTS_INCLUDE_SUBDOMAINS = False` y `SECURE_HSTS_PRELOAD = False`. |
| `.env.example` | MODIFICADO | Se documentó la variable de entorno `DJANGO_SECURE_HSTS_SECONDS=3600`. |
| `apps/core/tests/test_production_security.py` | MODIFICADO | Se añadieron pruebas para `SECURE_PROXY_SSL_HEADER`, `SECURE_REFERRER_POLICY` y aislamiento del entorno de desarrollo local. |
| `docs/P0_4_PRODUCTION_SECURITY_HARDENING.md` | MODIFICADO | Documentación completa de la fase P0.4B. |
| `docs/ROADMAP.md` | MODIFICADO | Actualización del estado global del proyecto y registro oficial de P0.4B. |

---

## 4. ESTRATEGIA Y CONFIGURACIÓN HSTS (D)

HTTP Strict Transport Security (HSTS) se implementa bajo una estrategia conservadora y gradual en `config/settings/production.py`:

```python
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
```

### Justificación Técnica:
1. **Duración Inicial (3600 segundos / 1 hora):** Permite verificar que todos los clientes reciban la cabecera HSTS sin arriesgar un bloqueo prolongado en caso de inconsistencia de certificados o proxy.
2. **`SECURE_HSTS_INCLUDE_SUBDOMAINS = False`:** El servicio opera sobre el subdominio administrado `jorgecyberpunktcg.pythonanywhere.com`. Mantener esta opción en `False` previene afectar otros posibles subdominios de la plataforma compartida.
3. **`SECURE_HSTS_PRELOAD = False`:** La inclusión en la lista global de precarga de navegadores (*HSTS Preload*) está reservada a dominios apex/TLD con subdominios SSL completos. No corresponde activarlo para subdominios de hosting compartido.

---

## 5. PROXY HTTPS (E)

Se incluyó en la configuración de producción:

```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

Esta directiva instruye a Django a confiar en la cabecera `X-Forwarded-Proto: https` inyectada por el reverse proxy frontal de PythonAnywhere, asegurando que `request.is_secure()` devuelva `True` adecuadamente sin causar bucles infinitos de redirección HTTPS.

---

## 6. REFERRER POLICY (F)

Se implementó explícitamente:

```python
SECURE_REFERRER_POLICY = "same-origin"
```

Esta directiva restringe el envío de la cabecera HTTP `Referer` únicamente a las solicitudes que permanezcan en el mismo origen (mismo dominio y protocolo), impidiendo la fuga involuntaria de URLs internas cuando los usuarios navegan hacia enlaces externos.

---

## 7. GARANTÍA DE DESARROLLO LOCAL (G)

Para evitar romper el entorno local (`http://127.0.0.1:8000/`), todos los ajustes de hardening se encuentran estrictamente confinados en `config/settings/production.py`.

* En `config/settings/development.py`:
  * `DEBUG = True`
  * `SECURE_SSL_REDIRECT` no se define (por defecto `False`).
  * `SESSION_COOKIE_SECURE` y `CSRF_COOKIE_SECURE` no se fuerzan a `True`.
  * `SECURE_HSTS_SECONDS` no se activa (0).

Esto garantiza que el servidor local de desarrollo (`python manage.py runserver`) continúe operando sobre HTTP sin ser forzado a conexiones SSL.

---

## 8. TESTS DE REGRESIÓN (H)

La suite en `apps/core/tests/test_production_security.py` incluye verificaciones automatizadas para:

1. `DEBUG == False` en producción.
2. `SECURE_SSL_REDIRECT == True` en producción.
3. `SESSION_COOKIE_SECURE == True` y `CSRF_COOKIE_SECURE == True` en producción.
4. `SECURE_CONTENT_TYPE_NOSNIFF == True` y `X_FRAME_OPTIONS == "DENY"`.
5. `SECURE_HSTS_SECONDS == 3600`.
6. `SECURE_HSTS_INCLUDE_SUBDOMAINS == False`.
7. `SECURE_HSTS_PRELOAD == False`.
8. `SECURE_PROXY_SSL_HEADER == ("HTTP_X_FORWARDED_PROTO", "https")`.
9. `SECURE_REFERRER_POLICY == "same-origin"`.
10. Aislamiento de desarrollo local (`DEBUG == True`, `SECURE_SSL_REDIRECT` no forzado, `SECURE_HSTS_SECONDS == 0`).

---

## 9. RESULTADOS DE VALIDACIÓN (I)

* **`python manage.py check`:** OK (0 errores).
* **`python manage.py makemigrations --check`:** OK (No changes detected).
* **`python manage.py test`:** OK (161 tests pasando sin fallos).
* **`python manage.py check --deploy --settings=config.settings.production`:**
  * `security.W004` (HSTS Seconds missing): **RESUELTO**.
  * `security.W005` (includeSubDomains): Warning aceptado intencionalmente por arquitectura.
  * `security.W021` (HSTS Preload): Warning aceptado intencionalmente por arquitectura.

---

## 10. RIESGOS PENDIENTES Y VERIFICACIONES POST-DESPLIEGUE (J)

* **Riesgos Resueltos:**
  * Cabecera HSTS activa de forma conservadora.
  * Encabezado de proxy SSL reconocido formalmente por Django.
  * Cabecera de política de referente endurecida a `same-origin`.
* **Riesgos Aceptados:**
  * Desactivación de `includeSubDomains` y `preload` por tratarse de un subdominio en PythonAnywhere.
* **Verificaciones Pendientes tras Despliegue Real:**
  * Confirmación de la cabecera `Strict-Transport-Security: max-age=3600` mediante `curl -I` en vivo en PythonAnywhere.
  * Confirmación de respuesta HTTP 200/301 sin bucles de redirección SSL bajo `SECURE_PROXY_SSL_HEADER`.

---

## 11. PLAN CRONOLÓGICO HSTS (K)

| Etapa | Estado | Duración (`max-age`) | Criterio de Elevación |
| :--- | :--- | :--- | :--- |
| **Etapa 1 (P0.4B)** | **Implementado localmente** | **3,600 segundos (1 hora)** | Despliegue en PythonAnywhere y verificación inicial de cabeceras HTTP. |
| **Etapa 2 (Estabilización)** | Pendiente | 2,592,000 segundos (30 días) | Operación continua estable en producción durante 5–7 días. |
| **Etapa 3 (Estado Estable)** | Pendiente | 31,536,000 segundos (1 año) | Lanzamiento oficial (Octubre 2026). |

---

## 12. PRÓXIMO PASO OPERATIVO (L)

El siguiente paso operativo formal será:

1. Ejecución del commit git local `Implement P0.4B production security hardening`.
2. Despliegue controlado en PythonAnywhere mediante el procedimiento estándar (`git pull origin main`, reload de la aplicación).
3. Verificación HTTP real mediante `curl -I https://jorgecyberpunktcg.pythonanywhere.com/`.
4. Inicio de la fase prelaunch **P1 — Prelaunch Readiness**.
