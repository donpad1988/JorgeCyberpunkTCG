# P0.2 — PRIVACY & INDEPENDENT-SITE DISCLOSURE

## 1. OBJETIVO

Implementar la capa técnica mínima y transparente de información sobre **Privacidad**, **Términos de Uso** y **Exención Factual de Afiliación Oficial** para la plataforma **JorgeCyberpunkTCG**, orientada a permitir la entrada segura de usuarios reales en producción antes del lanzamiento oficial del juego en octubre de 2026.

---

## 2. BASELINE Y RESULTADOS DE VERIFICACIÓN

* **HEAD Inicial:** `6689200 Documentar recuperación de cuenta en producción`
* **Rama Git:** `main` (sincronizada con `origin/main`).
* **Verificación de Diagnóstico:** `python manage.py check` (0 errores), `makemigrations --check` (No changes detected).
* **Pruebas Automatizadas:** 136 tests ejecutados correctamente.

---

## 3. INVENTARIO DE CAMBIOS IMPLEMENTADOS

1. **Vistas Públicas (`apps/core/views.py`):**
   - `privacy_policy(request)`: Renderiza la plantilla `core/privacy.html`.
   - `terms_of_service(request)`: Renderiza la plantilla `core/terms.html`.
2. **Rutas URL (`apps/core/urls.py`):**
   - `/privacidad/` (`name="privacy"`)
   - `/terminos/` (`name="terms"`)
3. **Plantillas Nuevas:**
   - [`templates/core/privacy.html`](file:///d:/01.Proyectos_Web/JorgeCyberpunkTCG/templates/core/privacy.html): Política de Privacidad estructurada basándose **exclusivamente** en el modelo de datos y tratamiento real de la aplicación.
   - [`templates/core/terms.html`](file:///d:/01.Proyectos_Web/JorgeCyberpunkTCG/templates/core/terms.html): Términos de Uso, normas comunitarias y exención de responsabilidad.
4. **Actualización de Plantillas Existentes:**
   - [`templates/base.html`](file:///d:/01.Proyectos_Web/JorgeCyberpunkTCG/templates/base.html): Se integraron los enlaces permanentes a `/privacidad/` y `/terminos/` en el pie de página (`site-footer`) y se reforzó la leyenda factual del pie:
     > *"JorgeCyberpunkTCG es un proyecto independiente de comunidad y contenido táctico. No está afiliado oficialmente con CD PROJEKT RED ni WeirdCo."*
   - [`templates/accounts/register.html`](file:///d:/01.Proyectos_Web/JorgeCyberpunkTCG/templates/accounts/register.html): Se añadió la leyenda informativa pre-registro con hipervínculos hacia Privacidad y Términos antes del botón de envío.
5. **SEO & Sitemap (`apps/core/sitemaps.py`):**
   - Se incorporaron `"core:privacy"` y `"core:terms"` dentro de `StaticViewSitemap.items()` para garantizar el descubrimiento orgánico. Ambas páginas cuentan con título, meta descripción y `<link rel="canonical">` limpio.
6. **Estilos Visuales (`static/css/components.css` y `static/css/accounts.css`):**
   - Estilos `.legal-doc` y `.auth-legal-notice` integrados de forma ligera en el Design System cibernético *Neural Interface* sin añadir librerías ni dependencias adicionales.

---

## 4. DETALLE FACTUAL DE LA POLÍTICA DE PRIVACIDAD IMPLEMENTADA

* **Identidad y Contacto:** Plataforma independiente. Correo único de contacto: `jorgecyberpunktcg@gmail.com`.
* **Datos Recopilados:** `username`, `email`, hashes criptográficos de contraseñas (Django `pbkdf2_sha256`), `first_name` y `last_name` opcionales, metadatos de sesión y mazos creados.
* **Finalidad:** Registro, autenticación, restablecimiento de clave y atribución de autoría sobre mazos públicos.
* **Visibilidad:** El correo electrónico y nombres son estrictamente privados. El `username` solo se muestra públicamente cuando el usuario decide publicar un mazo.
* **Cookies Técnicas:** `sessionid` (sesión) y `csrftoken` (seguridad CSRF). Sin cookies publicitarias ni rastreo de terceros.
* **YouTube Embebido:** Uso exclusivo del dominio `youtube-nocookie.com` para reproducciones de video de apoyo táctico.

---

## 5. DETALLE FACTUAL DE LOS TÉRMINOS DE USO IMPLEMENTADOS

* **Uso Aceptable:** Normas comunitarias contra contenido ilegal, spam, abuso o suplantación.
* **Moderación:** Reserva de facultad del administrador para despublicar contenidos que infrinjan las reglas o pongan en riesgo la seguridad.
* **Carácter Divulgativo:** Los análisis tácticos y reglas explicadas son puramente informativos; prevalecen siempre los manuales oficiales de Cyberpunk TCG.
* **Independencia Factual:** Declaración expresa de no afiliación con CD PROJEKT RED ni WeirdCo.

---

## 6. DECISIONES DE ALCANCE Y TRANSPARENCIA

1. **Ausencia de Checkbox Obligatorio:** Decisión técnica de alcance MVP. Se optó por una leyenda transparente e informativa previa al envío del formulario de registro. Se evita almacenar timestamps o alterar el modelo de usuario.
2. **Ausencia de Cookie Banner Floater:** Las únicas cookies emitidas por la aplicación son cookies técnicas esenciales de Django (`sessionid`, `csrftoken`). No hay banners flotantes invasivos que perjudiquen la UX.
3. **Sin Falsas Afirmaciones:** No se añadieron frases corporativas ficticias, NITs inventados, declaraciones de *fair use* ni promesas de seguridad absoluta.

---

## 7. PRUEBAS Y VALIDACIÓN AUTOMATIZADA

Se crearon 4 nuevos tests en `apps/core/tests/test_privacy_terms.py` y se actualizaron las aserciones en `apps/core/tests/test_seo.py`, elevando la suite total de **132 a 136 tests pasando exitosamente (100% OK)**.

---

## 8. MIGRACIONES Y BASE DE DATOS

* **Migraciones requeridas:** `0` (Cero).
* No se modificó ningún modelo de datos ni se añadieron dependencias externas.

---

## 9. RESULTADO FINAL

**COMPLETADO — P0.2 Privacy & Independent-Site Disclosure se encuentra implementado y validado con 136 tests pasando.**
