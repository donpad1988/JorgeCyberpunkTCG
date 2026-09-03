# Fase 7C — CRUD y seguridad de mazos

## Alcance implementado

La fase añade CRUD de metadata y lectura de composición para mazos persistidos. No añade Builder interactivo, cambio de Legends/Entries desde UI, JavaScript complejo, RAM, exportación, funciones sociales, integraciones editoriales, importación, scraping ni imágenes.

## Rutas y permisos

| Ruta | Acceso | Acción |
|---|---|---|
| `/mazos/` | usuario autenticado | Sólo sus propios mazos |
| `/mazos/publicos/` | público | Sólo mazos con `is_public=True` |
| `/mazos/crear/` | usuario autenticado | Crea metadata, con owner de `request.user` |
| `/mazos/<username>/<slug>/` | owner o público | Detalle read-only |
| `/mazos/<username>/<slug>/editar/` | sólo owner | Edita nombre, descripción y privacidad |
| `/mazos/<username>/<slug>/eliminar/` | sólo owner | GET confirma; POST elimina |

Un mazo privado de otro usuario responde 404 para no revelar su existencia. Las rutas de actualización y borrado filtran simultáneamente por owner autenticado, username y slug: el username de URL nunca concede autorización.

## Formularios, ownership y slug

`DeckMetadataForm` permite únicamente `name`, `description` e `is_public`. Owner, slug, timestamps, Legends y Entries no son campos de payload. En creación, la vista asigna siempre `deck.owner = request.user`.

El slug se genera desde el nombre al crear y se conserva tras editar el nombre, de modo que las URLs existentes no se rompen. Si el mismo owner intenta crear otro nombre que derive en el mismo slug, el formulario rechaza la operación: no sobrescribe ningún Deck. Otro usuario puede usar el mismo slug.

## Privacidad, seguridad y mutaciones

- Todos los create/update/delete usan login requerido.
- Toda mutación ocurre por POST; el borrado nunca se realiza por GET.
- Los formularios incluyen CSRF y no existe `csrf_exempt`.
- Owner, composición y timestamps no se aceptan desde el cliente.
- La composición existente sigue sólo de lectura; no hay acciones +1/−1 ni edición de Legends/Entries.

La futura 7D deberá implementar composición con `transaction.atomic()` cuando actualice varias Entries, manteniendo checks de ownership y validación server-side.

## Validación y rendimiento

El detalle reutiliza `DeckValidationService`. Presenta “Estructura válida” o “Estructura incompleta o inválida” y muestra explícitamente `RAM: NOT_EVALUATED`; no afirma legalidad completa. Los listados muestran metadata sin ejecutar una validación por mazo. El detalle carga relaciones de composición de forma agrupada.

La navegación principal enlaza Mazos a Mis mazos para usuarios autenticados y a Mazos públicos para visitantes. Home enlaza a esas rutas funcionales con copy limitado a metadata y composición en progreso, sin prometer Builder completo.

## Pruebas y datos existentes

Se añadieron pruebas de listados, creación, owner impuesto en servidor, colisiones de slug, privacidad, detalle público/privado, update, delete, CSRF, navbar y composición read-only. Las pruebas usan bases temporales.

No se crearon migraciones en 7C. Tras la validación, Choomdex conserva Cards=4 y CardPrintings=4. RAM continúa bloqueado hasta disponer de datos de reglas actuales/color verificables.

Siguiente fase propuesta: **7D — Builder SSR progresivo**, sin iniciarla automáticamente.
