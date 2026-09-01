# Fase 3 — Usuarios, autenticación y perfil base

## Objetivo y arquitectura

La fase implementa la identidad inicial con el `User` personalizado existente (`apps.accounts.models.User`) y las vistas, formularios, sesiones, validadores de contraseña y tokens de Django. El modelo no se modificó ni se creó un perfil adicional o migración.

## Rutas y flujos

| Ruta | Nombre | Propósito |
|---|---|---|
| `/cuenta/registro/` | `accounts:register` | Crea una cuenta con usuario, email y contraseña; inicia sesión automáticamente y redirige al perfil. |
| `/cuenta/login/` | `accounts:login` | Inicio de sesión nativo por nombre de usuario y contraseña. |
| `/cuenta/logout/` | `accounts:logout` | Cierre de sesión exclusivamente mediante POST y retorno a Home. |
| `/cuenta/perfil/` | `accounts:profile` | Perfil protegido con datos reales del usuario autenticado. |
| `/cuenta/perfil/editar/` | `accounts:profile_edit` | Edición limitada de nombre, apellido y correo. |
| `/cuenta/password-reset/` | `accounts:password_reset` | Inicio de recuperación de contraseña con las vistas y tokens nativos de Django. |

El reset incluye las pantallas de solicitud, confirmación de envío, token/nueva contraseña y finalización. En desarrollo se configura el backend de correo de consola: no se usan SMTP, credenciales ni correo externo. El runner de tests sustituye ese backend por la bandeja de salida de pruebas.

## Integración visual y accesibilidad

Los templates de `accounts` extienden `base.html` y usan `accounts.css`; no duplican el layout. Los formularios incluyen labels, mensajes de validación visibles, foco de alto contraste y atributos `autocomplete` que proporciona Django para usuario y contraseñas. La navbar muestra Jack In a visitantes y `@username`, Mi perfil y Jack Out (POST) a usuarios autenticados. El CTA de comunidad de la Home dirige a registro o perfil según la sesión.

## Seguridad

Todos los formularios POST incluyen CSRF. Las contraseñas se validan y almacenan mediante `UserCreationForm`/Django; no se manejan manualmente. El perfil y su edición están protegidos por `login_required`, siempre usan `request.user`, y el formulario excluye username, permisos y campos de futuros sistemas. Logout es POST-only y recuperación utiliza los tokens nativos de Django.

## Tests y comprobaciones

Se conservan los cinco tests de fases previas y se añaden ocho para registro, errores de registro, login/logout, login inválido, recuperación (incluido el enlace token), protección/edición del perfil y navegación autenticada. Resultado final: 13 tests correctos. También se ejecutaron `manage.py check` y `manage.py makemigrations --check`, sin incidencias ni cambios de modelo. La revisión visual local confirmó el formulario con CSRF y labels, sin desbordamiento horizontal a 360 y 1440 px.

## Limitaciones conscientes

No hay verificación real de email, SMTP de producción, OAuth, avatar, gamificación, Street Cred, Eddies, Gigs, Choomdex, Deck Builder ni Combat Terminal. Estas funcionalidades pertenecen a fases posteriores.
