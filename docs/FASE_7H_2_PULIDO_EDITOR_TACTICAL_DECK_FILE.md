# Fase 7H.2 — Pulido UX del editor de Tactical Deck File

## Objetivo y alcance

El editor editorial de `/mazos/<username>/<slug>/editorial/` conservaba su flujo SSR de 7E, pero se percibía como un formulario Django sin tematizar. Esta fase mejora exclusivamente su presentación: no altera modelos, migraciones, reglas, composición, permisos ni workflow editorial.

## Perfil táctico

El formulario se divide en dos paneles: **Perfil táctico** y **Cartas clave**. Los campos del perfil usan labels visibles en español: Arquetipo, Resumen corto, Estrategia, Plan de juego, Fortalezas y Debilidades. Inputs, textareas y select usan superficie oscura, bordes del sistema, foco cian, placeholders breves y separación consistente entre label, control y error.

## Cartas clave y errores

El formset existente permanece intacto, incluido `management_form`, su formulario extra y la regla de que una carta clave debe formar parte del mazo. Cada formulario se presenta como un panel numerado con Carta, Nota editorial, Orden de visualización y Eliminar esta carta clave. Los errores de campo, de formulario y de formset conservan texto visible, borde magenta y semántica de alerta.

## Navegación, responsive y accesibilidad

El guardado sigue siendo POST con CSRF y PRG. En escritorio la acción primaria mantiene ancho natural y se añade el enlace secundario **Volver al mazo**; en móvil ambos controles se apilan. El layout limita el ancho editorial, evita overflow, mantiene labels asociados y no depende de placeholders. No se añade JavaScript, AJAX, tabs ni accordions.

## Seguridad, pruebas y límites

La vista sigue siendo exclusiva del owner; usuarios ajenos reciben 404. Las pruebas cubren labels en español, ausencia de labels editoriales antiguos, labels de cartas clave, borrado funcional del formset, error visible de pertenencia y POST de otro owner sin cambios. Se conservan las regresiones de Tactical Deck File, biblioteca, videos, Choomdex, Builder y `RAM: NOT_EVALUATED`.

No se modifican Cards, CardPrintings, Sets, datos, imágenes, migraciones, modelos, navbar, footer, Home ni dependencias. 7I permanece pendiente.
