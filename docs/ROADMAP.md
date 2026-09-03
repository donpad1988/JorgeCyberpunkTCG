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
| 6A.1 | Verificación de fuentes Choomdex — **completada** | Contrato 6B refinado con fuentes oficiales; sin implementación. |
| 6B | MVP Choomdex — **completada** | Catálogo y administración vacíos con datos verificados manualmente. |
| 6C.1 | Dataset piloto Choomdex — **completada** | Un Set y cuatro Cards documentados desde fuentes oficiales; sin carga automática de datos. |
| 6C.3 | Presentación táctica Choomdex — **completada** | Grid HUD, ficha táctica y atributos condicionales sin alterar datos ni modelo. |
| 6D.1 | Arquitectura Card vs CardPrinting — **completada** | Decisión trazable para identidad, impresión y Set; migración condicionada a gates de verificación. |
| 6D.2 | Verificación de identidad, printings y taxonomías — **completada** | Evidencia oficial y gates revisados; diseño de migración permitido sólo con condiciones. |
| 6D.3 | Diseño de migración CardPrinting — **completada** | Plan expand–migrate–contract reversible para el piloto, sin ejecutar cambios técnicos. |
| 6D.4 | Implementación controlada CardPrinting — **completada** | CardPrinting, migraciones controladas, consumidores, admin y regresión verificados sin ampliar el dominio. |
| 7A | Diseño funcional y arquitectura Deck Builder — **completada** | Diseño de dominio, seguridad, UX y gates; implementación RAM condicionada a reglas/datos verificables. |
| 7B | Fundación técnica Deck Builder — **completada** | Modelos, constraints, servicio estructural, Admin y pruebas; RAM permanece sin evaluar. |
| 7C | CRUD y seguridad Deck Builder — **completada** | Metadata, privacidad, ownership, navegación y composición read-only; RAM permanece sin evaluar. |
| 7D | Builder interactivo de mazos — **completada** | Composición SSR segura, límites estructurales, búsqueda y filtros; RAM permanece sin evaluar. |
| 7E | Tactical Deck File / Biblioteca editorial — **completada** | El detalle público es una ficha táctica editorial; Builder se conserva como infraestructura privada del owner. |
| 7F | Deck ↔ YouTube — **completada** | Relación editorial opcional M2M, visible sólo entre Videos activos y Decks públicos. |
| 7G | Release-Ready Editorial — **completada** | Vigencia editorial de Decks separada de visibilidad, archivo histórico y preparación para la revisión de lanzamiento. |
| 7H | Tactical Deck Library — **completada** | Biblioteca pública editorial, búsqueda segura, archivo histórico y descubrimiento de Tactical Deck Files. |
| 7H.1 | Pulido visual Tactical Deck Library — **completada** | Buscador condicional y estados editoriales encapsulados sin ampliar el dominio. |
| 7H.2 | Pulido UX del editor de Tactical Deck File — **completada** | Editor editorial tematizado, labels en español y formset de Cartas clave preservado. |
| 7I | Integración editorial transversal — **pendiente** | Evolución de relaciones editoriales tras validar el flujo de lanzamiento. |
| Futuro opcional | RAM Analyzer | Despriorizado: requiere valor agregado real, reglas verificadas y feedback antes de reabrir el gate. |
| Futuro | INGESTA CONTROLADA DE DATOS CHOOMDEX — SUSPENDIDA HASTA DISPONER DE FUENTE AUTORIZADA | Requiere Card/CardPrinting estable, fuente aprobada, deduplicación, dry-run, idempotencia y tests. |
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

Desde 7E el proyecto **no busca competir con el Deck Builder oficial**. Mazos es principalmente una biblioteca táctica/editorial conectable al contenido propio de YouTube; el Builder queda como infraestructura para preparar y mantener composiciones.

## Hitos de decisión previos a módulos con datos externos

- Antes de Fase 5: decidir fuente, permisos y cadencia de actualización de metadatos de YouTube.
- Antes de Fase 6: validar fuentes y licencia de cada dato del juego; definir política de evidencia y correcciones.
- Antes de incorporar mercado: investigar APIs, términos, costes, límites y atribución; si no existe una fuente fiable, mantener «Sin datos de mercado».
- Antes de Fases 9–10: definir política de comunidad, moderación, retención de auditoría y límites antiabuso.
