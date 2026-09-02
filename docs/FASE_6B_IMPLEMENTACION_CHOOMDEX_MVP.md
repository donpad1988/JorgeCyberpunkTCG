# Fase 6B — MVP Choomdex

`apps.cards` implementa Set y Card con procedencia, slugs, CardType verificado y estados DRAFT/REVIEWED/PUBLISHED. Sólo `PUBLISHED` de Set activo es público mediante `Card.objects.public()`. El catálogo `/choomdex/` ofrece búsqueda SQLite, filtros GET y paginación; el detalle devuelve 404 para registros privados. La tarjeta Choomdex Hispano de Home enlaza funcionalmente al catálogo y ya no se presenta como módulo futuro.

La corrección postimplementación incorporó una batería de 14 tests descubribles en `apps.cards`: modelos, visibilidad pública, catálogo, detalle, búsqueda, filtros, paginación y registros de administración. Junto con la suite existente, el total final es de 34 tests. No se cargan datos, imágenes, mercado, keywords, rareza, facciones, CardPrinting, mazos ni RAM Analyzer. Administración Django permite carga manual revisada.
