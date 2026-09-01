# Fase 1 — Fundación técnica Django

## Estado

**Completada el 1 de septiembre de 2026.** El alcance se ha limitado a la infraestructura técnica; no se desarrollaron funcionalidades de la Fase 2 ni módulos de producto.

## Entorno y dependencia

- Python: `3.13.14`.
- Intérprete usado: `D:\01.Proyectos_Web\JorgeCyberpunkTCG\.venv\Scripts\python.exe`.
- Entorno virtual: `.venv` dentro de la raíz del proyecto.
- Django: `6.0.6`, versión estable compatible con Python 3.13 y fijada en `requirements.txt`.
- Dependencias directas: solamente `Django==6.0.6`.

No se añadió `python-dotenv`: la configuración obtiene variables directamente del entorno, lo que evita una dependencia adicional en esta fase. Django instala sus propias dependencias transitivas dentro de `.venv`, pero no se listan en `requirements.txt` porque no son dependencias directas del proyecto.

## Estructura creada

```
config/
  settings/{base,development,production}.py
apps/
  core/                 # smoke page mínima
  accounts/             # identidad de usuario
templates/core/
static/{css,js,img}/
media/                  # ignorado por Git
tests/
manage.py
requirements.txt
.env.example
.gitignore
```

## Usuario y administración

`apps.accounts.models.User` hereda de `django.contrib.auth.models.AbstractUser` y permanece intencionadamente sin campos de producto. `AUTH_USER_MODEL = "accounts.User"` se declaró en `config/settings/base.py` antes de generar migraciones. El modelo está registrado en el admin mediante una extensión mínima de `UserAdmin`.

La migración `apps/accounts/migrations/0001_initial.py` creó el usuario personalizado como la primera migración de la app. No se creó superusuario ni se inventaron credenciales.

## Configuración

- `base.py`: aplicaciones, middleware, templates, estáticos, media, localización y usuario personalizado compartidos.
- `development.py`: SQLite local, `DEBUG` controlado por `DJANGO_DEBUG`, hosts configurables y fallback conocido únicamente para desarrollo local.
- `production.py`: `DEBUG=False`, exige `DJANGO_SECRET_KEY` y `DJANGO_ALLOWED_HOSTS`, no permite comodines y habilita protecciones HTTPS/cookies/HSTS. La base de datos de producción se decidirá al preparar el despliegue.

`.env.example` sólo contiene nombres y valores de ejemplo. `.env`, `.venv`, `db.sqlite3`, `media/` y artefactos locales están excluidos de Git.

## Base de datos, pruebas y verificación

Se usó SQLite en `db.sqlite3` para desarrollo. Se ejecutó `migrate` correctamente con las migraciones `accounts`, `admin`, `auth`, `contenttypes` y `sessions` aplicadas.

Se implementaron tres pruebas reales:

1. La ruta principal devuelve HTTP 200 y usa su template mínimo.
2. El usuario personalizado se crea con el gestor de Django y su contraseña queda hasheada.
3. `get_user_model()` apunta a `accounts.User`.

Resultados ejecutados con el intérprete de `.venv`:

- `python manage.py check`: sin incidencias.
- `python manage.py makemigrations --check`: sin cambios detectados.
- `python manage.py test`: 3 pruebas correctas.
- `python manage.py showmigrations`: todas las migraciones aplicables aparecen aplicadas; `core` no tiene migraciones por no tener modelos.

## Git e incidencias

Git se inicializa localmente en la rama `main` tras esta documentación. Antes del commit se verificará que los archivos excluidos no estén preparados para seguimiento. No se configura remoto ni se hace push.

La única incidencia fue el bloqueo inicial de acceso de red del entorno aislado durante la instalación de Django. La instalación se completó tras aprobar explícitamente el acceso a PyPI, dentro de `.venv` y sin modificar ningún proyecto externo.
