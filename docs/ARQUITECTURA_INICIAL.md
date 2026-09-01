# Arquitectura inicial propuesta — JorgeCyberpunkTCG

## Decisiones para la Fase 1

Se recomienda Django moderno con renderizado del lado servidor como base. Esto favorece SEO, accesibilidad, simplicidad inicial y una progresión gradual hacia interactividad donde aporte valor. No se necesita una SPA ni una API pública en la fundación.

### Usuario personalizado: decisión obligatoria

**Sí: crear un Custom User Model en Fase 1, antes de la primera migración.** Debe extender `AbstractUser` inicialmente, sin convertirlo en un modelo de perfil monolítico. La decisión preserva compatibilidad con la autenticación segura de Django y deja espacio para preferencias, reputación y relaciones futuras sin el coste de cambiar `AUTH_USER_MODEL` cuando ya existan migraciones y relaciones.

`AUTH_USER_MODEL` se declarará desde el primer settings. Los datos que no son credenciales (avatar, estadísticas, inventario, actividad) vivirán más adelante en modelos especializados, no como campos añadidos por anticipación.

### Aplicaciones iniciales

En Fase 1 solamente se crearán:

- `apps.core`: páginas y utilidades transversales mínimas, health/errores y convenciones compartidas.
- `apps.accounts`: modelo de usuario personalizado y su configuración administrativa mínima; el flujo de UI de autenticación pertenece a la Fase 3.

No se crearán apps vacías. `content`, `guides`, `youtube`, `cards`, `decks`, `tools`, `community`, `gamification` y `events` se introducirán en las fases que las necesiten. Si una app futura crece, sus reglas de dominio se mantendrán dentro de esa app para evitar acoplamiento.

### Estructura proyectada

```
config/                 # settings, URLs, ASGI/WSGI
apps/
  core/
  accounts/
templates/              # base global y fragmentos compartidos
static/                 # assets fuente propios, por namespaces de app
media/                  # archivos de usuario en ejecución; nunca versionados
tests/                  # pruebas transversales; las pruebas de app viven junto a cada app
docs/
```

Dentro de una app se prefieren `templates/<app>/`, `static/<app>/`, `forms.py`, `services/`, `selectors/` sólo cuando haya consultas reutilizables, y `tests/`. No se crearán directorios vacíos: la estructura se materializa al necesitarla.

### Settings y secretos

Usar un módulo `config.settings` dividido por entorno: `base`, `local`, `production` y `test`, con un punto de entrada explícito. Las variables se leerán de entorno; un archivo `.env` local será opcional para desarrollo y estará ignorado por Git. Se versionará únicamente `.env.example` sin valores reales.

La configuración de producción requerirá, como mínimo, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, cookies seguras, HTTPS, configuración de estáticos/media y base de datos gestionada fuera del código. No registrar secretos ni datos personales en logs.

### Templates, estáticos y media

El template base contendrá estructura semántica y bloques claros. Los componentes reutilizables serán parciales con una API de contexto pequeña; no concentrarán reglas. CSS y JavaScript se dividirán por responsabilidad y namespace de app, con design tokens para el futuro sistema visual. Se aplicará `prefers-reduced-motion` a efectos opcionales.

Los media de usuario se validarán en backend por tipo, tamaño y almacenamiento; no se servirán como si fueran estáticos. La estrategia concreta de almacenamiento se decide para producción en Fase 14.

### Servicios de dominio

Vistas y formularios coordinan HTTP; modelos representan persistencia e invariantes simples; `services/` ejecuta casos de uso con transacciones cuando cambian varias entidades o hay recompensas/saldos. Las validaciones críticas permanecen en servidor. No se crearán capas ceremoniales para CRUD simple. Para operaciones sensibles futuras, el servicio será el único punto de escritura y generará trazabilidad.

### Tests y calidad

Usar el runner nativo de Django inicialmente. Cada app tendrá pruebas de modelos, formularios, vistas, permisos y casos límite. Pruebas transversales (configuración, seguridad o flujos entre apps) vivirán en `tests/`. Se evitará depender de paquetes de testing hasta que aporten una mejora concreta.

En cada fase se ejecutarán: `python manage.py check`, `python manage.py makemigrations --check` y `python manage.py test`.

## Dependencias mínimas propuestas (sin instalar)

- `Django`: único requisito de aplicación para la Fase 1; usar una versión LTS vigente compatible con el Python local que se vaya a aprobar.
- `python-dotenv` (opcional): sólo si se decide cargar `.env` en desarrollo; las variables de entorno del sistema siguen siendo la fuente de configuración.

No se justifican aún REST framework, Celery, Redis, un framework CSS, librerías de gamificación, APIs de YouTube, scraping, almacenamiento cloud ni paquetes de autenticación externos.

## Riesgos y mitigaciones

| Área | Riesgo | Mitigación prevista |
|---|---|---|
| Técnico | Crear todas las apps o una SPA antes de necesidad real. | Fundación pequeña, SSR y crecimiento por fases. |
| Seguridad | Cambiar tarde el usuario, exponer secretos, permisos horizontales débiles. | `AUTH_USER_MODEL` temprano, settings por entorno y autorización servidor. |
| Propiedad intelectual | Uso no autorizado de arte, logos o datos. | Identidad original, placeholders y revisión de derechos antes de incorporar assets/datos. |
| Datos externos | Reglas, precios o APIs no verificadas. | Procedencia explícita, política «Sin datos» e investigación previa. |
| Escalabilidad | N+1, embeds pesados y lógica duplicada. | Select/prefetch, paginación, carga diferida y servicios acotados. |
| Moderación | Spam, abuso de recompensas y contenido dañino. | Reportes, límites, permisos, auditoría y transacciones en fases pertinentes. |

## Criterio de inicio de Fase 1

Antes de iniciar, confirmar versión de Python disponible y elegir una versión LTS de Django compatible. Entonces: crear entorno virtual, instalar la dependencia aprobada, inicializar el proyecto y las dos apps mínimas, configurar usuario personalizado antes de migrar, añadir `.gitignore` y `.env.example`, y verificar los tres comandos de calidad. La Fase 1 no implementará Home ni funcionalidades de producto.
