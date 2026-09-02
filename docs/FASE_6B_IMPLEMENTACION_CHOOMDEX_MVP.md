# Fase 6B — MVP Choomdex

`apps.cards` implementa Set y Card con procedencia, slugs, CardType verificado y estados DRAFT/REVIEWED/PUBLISHED. Sólo `PUBLISHED` de Set activo es público mediante `Card.objects.public()`. El catálogo `/choomdex/` ofrece búsqueda SQLite, filtros GET y paginación; el detalle devuelve 404 para registros privados. No se cargan datos, imágenes, mercado, keywords, rareza, facciones, CardPrinting, mazos ni RAM Analyzer. Administración Django permite carga manual revisada.
