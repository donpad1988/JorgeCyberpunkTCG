# Fase 7E — Tactical Deck File / Biblioteca editorial de mazos

## Decisión estratégica

Mazos deja de ser una propuesta de Deck Builder público. La experiencia principal es una ficha editorial/táctica pública que complementa el contenido propio de JorgeCyberpunkTCG y podrá recibir un video relacionado en 7F. No pretende replicar ni competir con el Builder oficial. El Builder SSR de 7D se conserva para el owner como infraestructura de composición.

## Modelo editorial elegido

Se creó `DeckEditorialProfile` con relación `OneToOne` a `Deck`, y `DeckKeyCard` como relación editorial a una Card de la composición. La separación evita sobrecargar el modelo de dominio que representa ownership, privacidad y composición, y permite que el contenido editorial crezca sin mezclarlo con reglas de Deck Builder.

La migración `decks.0002_editorial_profile_and_key_cards` crea perfiles vacíos para Decks existentes y establece los modelos nuevos. No altera `Card`, `CardPrinting` ni `Set`, ni carga datos de juego.

Campos MVP del perfil: `archetype`, `short_summary`, `strategy_overview`, `game_plan`, `strengths` y `weaknesses`. Se usa un único `game_plan` flexible en vez de imponer fases early/mid/late a todo arquetipo. `DeckKeyCard` contiene Card, nota editorial propia y orden; exige que la Card pertenezca a Legends o MAIN del mismo Deck y no permite duplicados.

## Tactical Deck File

La URL canónica sigue siendo `/mazos/<username>/<slug>/`. Para Decks públicos, visitantes, otros usuarios y owner pueden leer una página indexable con título y meta description basados en contenido propio. Los privados mantienen 404 para terceros/anónimos y añaden `noindex, nofollow` para el owner.

La ficha muestra resumen, arquetipo, estrategia, plan, Legends destacadas, Cartas clave, MAIN ordenado de forma consistente, fortalezas, debilidades y validación estructural parcial. Cada Card de Legends, MAIN o Cartas clave enlaza a Choomdex únicamente cuando es pública; no se duplica el detalle de Card ni se usan imágenes oficiales.

La validación sigue expresando `Legends X/3`, `MAIN X/40–50` y `RAM: NOT_EVALUATED`. No declara legalidad de torneo. RAM queda como **FUTURE OPTIONAL FEATURE**, sujeto a valor agregado real, reglas/datos verificables y feedback de jugadores. Las sinergias complejas (`DeckSynergy`) quedan también como futuro; el análisis general y las notas de cartas clave cubren el MVP.

## Edición y seguridad

`/mazos/<username>/<slug>/editorial/` ofrece un formulario separado de la metadata y composición. Sólo el owner puede abrirlo o enviarlo; anónimos reciben el redirect de login y cualquier otro usuario obtiene 404, incluso si el Deck es público. El payload no contiene ni modifica owner o composición. Admin incluye el perfil y las cartas clave para gestión editorial, sin sustituir la interfaz del owner.

La biblioteca `/mazos/publicos/` muestra sólo Decks públicos, resumen/arquetipo cuando existan y contadores de Legends/MAIN. `Mis mazos` sigue orientada a gestión e incluye accesos a ver, editar contenido y construir. No se añadieron CTAs falsos de video: el área y relación real se reservan para 7F.

## Verificación y límites

Las pruebas cubren el perfil 1:1, cascade, Card clave integrante/no duplicada, lectura pública, protección privada, actualización editorial owner-only, enlaces a Choomdex y biblioteca pública. Las pruebas existentes de CRUD/Builder siguen protegiendo ownership, privacidad, CSRF, límites de composición y `NOT_EVALUATED`.

No se modificaron ni cargaron Cards; se preservan Cards=4 y CardPrintings=4. No se integró YouTube, RAM, importación, scraping, imágenes oficiales, mercado, sinergias complejas ni Home destacada. Próximo paso permitido: 7F, para diseñar la relación Deck↔YouTube sin ampliar el dominio de composición.
