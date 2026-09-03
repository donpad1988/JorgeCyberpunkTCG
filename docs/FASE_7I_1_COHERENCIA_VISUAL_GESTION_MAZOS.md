# FASE 7I.1 — COHERENCIA VISUAL Y SEMÁNTICA DE GESTIÓN DE MAZOS

## 1. OBJETIVO Y CONTEXTO

Fase de pulido UX/UI acotada para resolver dos hallazgos detectados tras la finalización de la Fase 7I:

1. **Contradicción semántica del Eyebrow en Tactical Deck File**: El descriptor superior mostraba `PUBLIC NETWORK` incluso cuando el usuario propietario estaba previsualizando un mazo en estado `DRAFT` o un mazo publicado en modo privado (`is_public=False`).
2. **Desfase visual y lingüístico del formulario de metadata (`/mazos/<username>/<slug>/editar/`)**: El formulario `DeckMetadataForm` presentaba etiquetas por defecto en inglés, fondo blanco en controles y falta de integración con el sistema de diseño cibernético (Neural Interface / 7H.2).

## 2. CAMBIOS REALIZADOS

### A. Eyebrow del Tactical Deck File (`templates/decks/deck_detail.html`)
Se ajustó la lógica del descriptor superior `TACTICAL DECK FILE // ...` para reflejar con precisión el ciclo de vida editorial y el estado de visibilidad pública:
- **`DRAFT` (visto por el propietario)**: `TACTICAL DECK FILE // OWNER PREVIEW`
- **`PUBLISHED` + `is_public=True`**: `TACTICAL DECK FILE // PUBLIC NETWORK`
- **`PUBLISHED` + `is_public=False` (visto por el propietario)**: `TACTICAL DECK FILE // OWNER PREVIEW`
- **`ARCHIVED`**: `TACTICAL DECK FILE // ARCHIVED RECORD`

Se preserva sin modificaciones el badge del estado editorial (`Borrador`, `Publicado`, `Archivado`) y el aviso histórico de archivo táctico.

### B. Formulario de Metadata (`apps/decks/forms.py` & `templates/decks/deck_form.html`)
- **Traducción de labels**:
  - `name` → `Nombre del mazo`
  - `description` → `Descripción`
  - `is_public` → `Visible públicamente`
  - `editorial_status` → `Estado editorial`
- **Textos de ayuda (help_text)**:
  - `is_public`: *"Controla si otras personas pueden acceder al mazo."*
  - `editorial_status`: *"Indica si el análisis está en borrador, publicado o archivado."*
- **Estructura del formulario y Meta**: Se consolidaron de forma no duplicada las etiquetas y help texts en `DeckMetadataForm.Meta`, preservando la declaración explicativa limpia del campo `editorial_status`.
- **Integración visual Neural Interface**:
  - Encapsulamiento del formulario dentro de un panel con jerarquía ciberpunk (`.deck-metadata`).
  - Inputs, Textarea y Select oscuros (`#0c0e11`) con border cibernético y focus cian.
  - Checkbox nativo accesible integrado en contenedor (`.deck-metadata__checkbox-wrapper`) con label explicativo y acento cian.
  - Renderizado textual de errores por campo y globales con atributo `role="alert"` y estilo destacado en magenta (`.deck-metadata__errors`).
- **Acciones y botones**:
  - Botón primario `Guardar mazo`: Ancho natural en desktop y 100% en dispositivos móviles.
  - Botón secundario `Volver al mazo` (`button--ghost`): Añadido dinámicamente cuando el formulario edita un mazo existente (`deck.get_absolute_url()`).

### C. Estilos CSS (`static/css/decks.css`)
- Añadidas las reglas CSS de `.deck-metadata` y sus subcomponentes (`__panel`, `__field`, `__label`, `__checkbox-wrapper`, `__help`, `__errors`, `__actions`).
- Totalmente responsive con breakpoints para mobile (<760px) manteniendo contraste WCAG y accesibilidad.

## 3. VERIFICACIÓN Y TESTS

Se crearon e integraron tests automatizados en `apps/decks/tests/test_editorial_status.py` y `apps/decks/tests/test_crud.py`:
1. `test_eyebrow_contextual_descriptor_matrix`: Valida que `DRAFT` y `PUBLISHED private` muestren `OWNER PREVIEW`, `PUBLISHED public` muestre `PUBLIC NETWORK` y `ARCHIVED` muestre `ARCHIVED RECORD`.
2. `test_metadata_form_get_labels_help_text_and_cta`: Valida la presencia de las etiquetas en español, textos de ayuda, CTA "Volver al mazo" y la ausencia de etiquetas por defecto en inglés.
3. `test_metadata_form_post_updates_all_fields_and_validates`: Valida la actualización por POST de todos los campos del formulario y el comportamiento del manejo de errores ante datos inválidos.

Total suite: **122 / 122 tests pasados exitosamente**.

## 4. LÍMITES Y REGLAS PRESERVADAS
- NINGÚN cambio en `models.py` ni migraciones de base de datos (`makemigrations --check` limpio).
- NINGUNA línea de JavaScript añadida.
- Modelos y datos intactos: Cards = 4, CardPrintings = 4, Decks = 1 (Piloto DRAFT, RAM NOT_EVALUATED).
- Builder, Editor Editorial (7H.2), Biblioteca Pública (7H.1) y vista Delete intactos.
