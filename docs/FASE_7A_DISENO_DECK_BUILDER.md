# Fase 7A — Diseño funcional y arquitectura del Deck Builder

## Decisión de alcance

Esta fase define el Deck Builder futuro; no crea aplicación, modelos, migraciones, datos, UI ni integración externa. Choomdex conserva el conocimiento editorial de `Card` y `CardPrinting`; Deck Builder será el consumidor que compone y valida `Card` lógicas.

La recomendación es **GO PARCIAL CON CONDICIONES**: se puede implementar una futura fundación autenticada de persistencia, CRUD y validación estructural. El validador RAM completo queda bloqueado hasta que exista una fuente autorizada y un modelo de reglas actuales que exponga color y RAM de juego de forma verificable. Los valores actuales de `CardPrinting.ram` son valores impresos y no bastan para inferir ese algoritmo.

## Fuentes y matriz de reglas

Fuentes de autoridad: [Gameplay Guide oficial](https://cyberpunktcg.com/gameplay-guide), [Comprehensive Rules oficial](https://cyberpunktcg.com/comprehensive-rules), y la evidencia interna de [Fase 6A.1](FASE_6A_1_VERIFICACION_FUENTES_CHOOMDEX.md). No se realizó scraping ni se reproduce texto de reglas.

| Regla | Fuente / evidencia | Implementación futura | Confianza | Gate |
|---|---|---|---|---|
| Tres Legends de nombres únicos | Gameplay Guide, sección Deck Building & RAM | Exactamente tres `Card` LEGEND distintas para validez | Alta | CERRADO |
| Main deck de 40 a 50 | Misma guía; Legends excluidas | Suma de cantidades de zona MAIN | Alta | CERRADO |
| Máximo tres copias | Misma guía; “same card” | Límite por `Card` lógica, no por printing | Alta | CERRADO, sin excepciones verificadas |
| Elegibilidad RAM | Misma guía; límites acumulados por color de Legends | Servicio por color con datos de reglas actuales | Media para regla, baja para datos actuales | ABIERTO |
| Elegibilidad editorial | Arquitectura Choomdex | Selector público: `Card.status=PUBLISHED` y primary usable | Alta | CERRADO |

No se asumen sideboard, commander, bloqueo de facción/color, rotación, banlist, formatos ni restricciones por Set. La guía distingue Legends del main deck; por ello no se cuentan en el intervalo 40–50.

## Usuario y experiencia

**MVP recomendado: sólo usuarios autenticados.** La persistencia pertenece a una cuenta, simplifica privacidad, autorización horizontal, recuperación y auditoría, y evita diseñar sesiones temporales, límites antiabuso y transferencia de propiedad. Un visitante puede explorar Choomdex y los mazos públicos; la acción de crear dirige al acceso/registro.

Flujo recomendado:

```text
Mazos → crear metadatos → escoger hasta 3 Legends → construir MAIN
      → validación recalculada → guardar borrador → resumen / editar
```

El orden de selección es guiado, no bloqueante: un borrador puede tener 0–2 Legends o un main deck incompleto. La interfaz informa errores sin impedir el trabajo; la condición de “válido” es un cálculo, no un estado persistido que pueda quedar obsoleto.

En escritorio: columna de filtros/búsqueda, catálogo central de Cards elegibles y panel lateral de composición/validación. En móvil: paneles apilados, resumen fijo compacto y acciones +1/−1/eliminar accesibles. La identidad visual será Tactical Cyberdeck propia, no una imitación de interfaces oficiales.

## Modelo conceptual

```text
User 1 ── * Deck 1 ── * DeckEntry * ── 1 Card ── * CardPrinting ── 1 Set
                   └── * DeckLegend * ── 1 Card (LEGEND)
```

Se recomienda `DeckLegend` separado de `DeckEntry`: expresa que Legends no son main-deck entries, permite una restricción directa contra repetición por deck y hace explícito que no cuentan para 40–50. `DeckEntry` representa exclusivamente una Card del main deck y su cantidad. Ninguna relación obligatoria apunta a `CardPrinting`.

Una futura preferencia cosmética/coleccionable podría ser `DeckEntry.preferred_printing`, nullable y con `SET_NULL`; no entra en MVP y nunca cambia identidad, límite de copias, RAM ni legalidad.

### Matriz de modelo

| Entidad | Campo candidato | Responsabilidad | MVP | Restricción conceptual |
|---|---|---|---|---|
| Deck | owner | titular y autorización | Sí | FK a usuario; no editable por terceros |
| Deck | name | identificación humana | Sí | longitud y validación normal de formulario |
| Deck | slug | URL dentro del namespace de owner | Sí | único por owner, no global |
| Deck | description | nota propia opcional | Sí | texto limitado, sin reglas oficiales |
| Deck | is_public | privacidad simple | Sí | por defecto `False` |
| Deck | timestamps | auditoría local | Sí | automáticos |
| DeckLegend | deck, card | selección de Legend | Sí | CardType LEGEND; único deck+card |
| DeckEntry | deck, card, quantity | composición MAIN | Sí | único deck+card; cantidad positiva y hasta 3 |

No se incluyen Street Cred, Eddies, ratings, likes, vistas, formatos, torneo, banlist, mercado ni datos de colección.

### Constraints y comportamiento de borrado

- La base puede garantizar `UNIQUE(deck, card)` para `DeckEntry` y `DeckLegend`, y `quantity > 0` mediante `CheckConstraint` cuando se implemente.
- El servicio garantiza límites cruzados: tres Legends, 40–50 MAIN, máximo de tres, publicación y RAM. No se codifica el juego entero en SQL.
- Eliminar un usuario elimina sus Decks y entradas (`CASCADE`), conforme a la política de borrado de cuenta que se defina.
- Eliminar un Deck elimina sus Legends y entradas (`CASCADE`).
- Un DeckEntry debe usar `PROTECT` hacia Card mientras existan mazos históricos; una Card despublicada no borra sus entradas.
- `CardPrinting` no es dependencia del Deck Builder. Una preferencia futura usaría `SET_NULL`, nunca `CASCADE`.

## Reglas y validación

`DeckValidationService` será la única fuente de las reglas de dominio. Recibe un Deck y produce una estructura calculada, por ejemplo:

```text
{ valid, errors, warnings, summary }
```

No guarda `VALID`/`INVALID` como verdad permanente: una errata, una Card despublicada o una futura revisión de RAM exige recalcular. Un Deck guardado equivale a persistido; un Deck válido equivale a cumplir el servicio en ese momento.

| Capa | Responsabilidad |
|---|---|
| Modelo / DB | FKs, cantidad positiva, unicidad local, integridad simple |
| Formulario / servicio | límites de juego, Card publicada, ownership del caso de uso |
| Vista | autenticación, método POST y coordinación HTTP |
| Template / JS | mostrar resultado; nunca ser autoridad |

Errores bloquean validez: Legends distintas ≠3, MAIN <40 o >50, cantidad >3, Card inexistente/no publicada, o RAM excedida cuando el gate esté cerrado. Warnings no invalidan: Card usada que fue despublicada después de guardar, información de RAM aún no verificable, o borrador incompleto.

### RAM: diseño y gate

La regla oficial disponible indica que las tres Legends aportan un límite acumulado **por color**, y cada Card incluida debe permanecer dentro del límite total de su color. El cálculo futuro debe resumir, por color, RAM suministrada por Legends y RAM requerida por cada Card; una Card multicolor sólo puede aceptarse si existe una política y datos oficiales que describan sus requisitos.

El futuro servicio podrá evaluar `legend_ram_by_color`, `required_ram_by_color`, exceso y Cards causantes. No debe sumar valores impresos de `CardPrinting` ni inferir color desde bordes, nombres o Set. Gate RAM para implementar: fuente autorizada de reglas actuales, modelo aprobado de color/RAM y tratamiento oficial de Cards multicolor o excepciones. Hasta entonces, la UI puede reportar “RAM pendiente de verificar”, no declarar un mazo legal por inferencia.

## Elegibilidad, privacidad y rutas

El selector de jugador ofrece sólo `Card.status=PUBLISHED` con una printing primaria utilizable, reutilizando conceptualmente el queryset de Choomdex. Staff puede revisar datos en Admin, pero no se plantea un bypass de reglas en el builder público sin un permiso explícito posterior.

`is_public` es suficiente para MVP. Owner: crear, leer, editar y eliminar. Otros: sólo leer Decks públicos. Staff: permisos Django explícitos, no acceso implícito. Toda mutación exige login, comprobación de owner, POST y CSRF; nunca se confía en IDs de Card ni cantidades enviados por el cliente.

Se recomienda identidad pública `/mazos/<username>/<slug>/` y unicidad `(owner, slug)`: evita forzar slug global, mantiene URLs legibles y no expone UUIDs innecesariamente. Rutas conceptuales:

```text
/mazos/                 # propios, requiere login
/mazos/publicos/        # listado público
/mazos/crear/
/mazos/<username>/<slug>/
/mazos/<username>/<slug>/editar/
/mazos/<username>/<slug>/eliminar/
```

## Arquitectura Django, consultas y operaciones

La futura app será `apps.decks`: modelos, formularios, servicios, selectors, vistas SSR, templates y tests propios. Django estándar más CSS/JS existentes es suficiente; no se justifican dependencias, SPA, React o Vue.

- Formularios: `ModelForm` para metadatos; comandos o `Form`/formset controlado para composición.
- Servicios: creación, reemplazo de composición y validación, con `transaction.atomic()`.
- Selectors sólo cuando se reutilicen: Cards elegibles, mazos propios, mazos públicos y resumen con `select_related`/`prefetch_related`.
- El guardado de varias entradas debe validar el payload, bloquear doble submit de manera idempotente cuando sea razonable y escribir todas las entradas o ninguna.
- En SQLite el servicio serializa una operación atómica; para producción se evaluará `select_for_update()`/control de versión si aparecen ediciones concurrentes reales.
- Catálogo y resumen deben prefetch de entries→Card y las relaciones necesarias, sin consultas por entrada ni por printing.

Las acciones +1, −1 y eliminar pueden recibir JavaScript progresivo para respuesta rápida, pero el POST final y cada operación sensible se validan en servidor. El buscador reutiliza Card/Choomdex por nombre y los filtros existentes CardType y Set a través de printing; no crea un segundo catálogo.

## Resultado, resumen y límites de producto

Resumen táctico mínimo: `Legends X/3`, `Main deck X/40–50`, estado RAM por color cuando esté verificado y resultado `VALID/INVALID` calculado. Los mensajes deben ser propios y claros, por ejemplo: “Selecciona exactamente 3 Legends” o “El mazo principal necesita al menos 40 cartas”.

No entran en MVP: exportación texto/JSON/PDF, enlace de compartir dedicado, copiar un mazo público, comments, likes, ratings, YouTube, Articles, Street Cred, Eddies, mercado y preferred printing. Futuras relaciones Article↔Deck y Video↔Deck se evaluarían sin modificar `apps.content` ni `apps.videos` ahora.

### Matriz MVP / futuro

| Capacidad | MVP | Futuro | Descartada ahora | Justificación |
|---|---|---|---|---|
| Crear, editar, eliminar | Sí | — | — | Núcleo usable |
| Privacidad / lectura pública | Sí | estados más ricos | — | Booleano suficiente |
| Validación 3/40–50/3 copias | Sí | excepciones verificadas | — | Evidencia disponible |
| Validación RAM | Sólo interfaz de pendiente | Sí, tras gate | algoritmo inferido | Datos actuales insuficientes |
| Compartir / copiar | — | Sí | — | No bloquea el núcleo |
| Exportación | — | Sí | — | No condiciona modelos iniciales |
| Preferred printing | — | Opcional | obligatorio | No afecta juego |
| Likes, ratings, comments | — | Posible comunidad | Sí en MVP | Moderación fuera de alcance |
| YouTube / Articles | — | Relaciones editoriales | Sí en MVP | Evita acoplamiento |
| Street Cred / Eddies | — | Fase de gamificación | Sí en MVP | Sin recompensa prematura |
| Mercado | — | Módulo separado | Sí en MVP | Depende de CardPrinting |

## Seguridad, pruebas y casos límite

Pruebas futuras: modelos/constraints; servicio de Legends, MAIN, copias y RAM; formularios; permisos horizontales (A no modifica B); visibilidad privada/pública; POST/CSRF; transacciones; integración CRUD; selector de Cards publicadas; y regresión de Choomdex.

Casos mínimos: 0/1/2/3/4 Legends; Legend repetida; MAIN 39/40/50/51; cantidades 0, negativas y 4; Card inexistente/no publicada/sin primary; RAM exacta, insuficiente y multicolor pendiente; dos printings de la misma Card; doble submit y edición simultánea. Una Card despublicada se conserva en un Deck histórico, se señala como warning y no se permite añadir de nuevo; la validez se recalcula tras errata o cambio editorial.

## Fases posteriores propuestas y gates

1. **7B — Fundación de mazos:** confirmar modelo, constraints simples, servicios estructurales y migraciones.
2. **7C — CRUD y seguridad:** formularios, ownership, privacidad, transacciones y pruebas.
3. **7D — Builder SSR progresivo:** búsqueda reutilizada, composición y resumen responsive.
4. **7E — Validación RAM:** sólo después de cerrar el gate de datos/reglas actuales.
5. **7F — Publicación y extensiones:** compartir/copia y vínculos editoriales, si se autorizan.

| Gate | Estado para comenzar |
|---|---|
| Legends: exactamente 3 y fuera de MAIN | CERRADO |
| Main deck: 40–50 | CERRADO |
| Copias: máximo 3 por Card lógica | CERRADO |
| Card eligibility | CERRADO: sólo PUBLISHED con primary usable |
| Persistencia | CERRADO: autenticados únicamente |
| RAM | ABIERTO: faltan datos actuales/color y casos multicolor |

No se inicia automáticamente ninguna de estas subfases.
