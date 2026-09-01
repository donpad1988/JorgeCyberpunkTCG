# Roadmap maestro — JorgeCyberpunkTCG

## Método de ejecución

Cada fase se cierra con alcance definido, pruebas proporcionales, documentación de decisiones y verificación. Una fase no se considera completada por tener interfaz: debe cumplir sus controles de seguridad, datos y mantenimiento correspondientes.

| Fase | Resultado esperado | Condición de cierre |
|---|---|---|
| 0 | Constitución, arquitectura y planificación | Documentos aprobados; no hay código Django. |
| 1 | Fundación técnica Django — **completada** | Proyecto mínimo, settings por entorno, usuario personalizado, pruebas y Git ignorando secretos. |
| 2 | Sistema visual y Home — **completada** | Design tokens originales, layout responsive/accesible y Home basada en contenido propio. |
| 3 | Usuarios y autenticación — **completada** | Registro, acceso, recuperación y perfil base con permisos verificados. |
| 4 | Guías y estrategias — **completada** | Modelo editorial, categorías, slugs, administración y páginas indexables. |
| 5 | Integración editorial con YouTube — **completada** | Metadatos propios y relaciones con guías sin depender de API externa. |
| 6A | Diseño y auditoría Choomdex — **completada** | Arquitectura, política de fuentes y MVP definidos sin implementar datos. |
| 6 | Choomdex | Catálogo con procedencia de datos, filtros y estados explícitos de datos ausentes. |
| 7 | Deck Builder | Mazos, restricciones configurables y validación servidor. |
| 8 | RAM Budget Analyzer y herramientas presenciales | Analizador de RAM separado de Eddies y terminal móvil de partida. |
| 9 | Comunidad | Comentarios/discusiones, reportes, permisos, moderación y antiabuso. |
| 10 | Gamificación | Street Cred, Gigs, recompensas trazables y controles antiabuso. |
| 11 | Terminal de Netrunner | Dashboard de perfil, progreso, actividad y mazos. |
| 12 | Eventos | Gestión editorial de eventos y datos de organizadores. |
| 13 | Auditoría transversal | SEO, seguridad, rendimiento, accesibilidad, cobertura de pruebas y revisión de dependencias. |
| 14 | Producción | Configuración segura, observabilidad, estáticos/media, despliegue y plan de recuperación. |

## Ajuste razonado

Se conserva el orden conceptual. La Fase 1 debe fijar el usuario personalizado antes de cualquier migración, aunque el flujo de autenticación visible se posponga a la Fase 3. La Fase 13 no sustituye los controles previos: consolida una auditoría transversal final.

## Hitos de decisión previos a módulos con datos externos

- Antes de Fase 5: decidir fuente, permisos y cadencia de actualización de metadatos de YouTube.
- Antes de Fase 6: validar fuentes y licencia de cada dato del juego; definir política de evidencia y correcciones.
- Antes de incorporar mercado: investigar APIs, términos, costes, límites y atribución; si no existe una fuente fiable, mantener «Sin datos de mercado».
- Antes de Fases 9–10: definir política de comunidad, moderación, retención de auditoría y límites antiabuso.
