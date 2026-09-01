# Fase 5 — Integración editorial con YouTube

Se creó `apps.videos` con `Video`: URL pública, ID, slug, resumen, estado activo, fecha y relación ManyToMany con artículos. La administración es manual mediante Django Admin; no hay API, OAuth, scraping, sincronización ni datos permanentes de vídeos.

El catálogo público `/videos/` muestra sólo vídeos activos y su estado vacío. El detalle `/videos/<slug>/` construye el iframe desde el ID usando `youtube-nocookie.com`, muestra un enlace externo seguro y filtra los artículos relacionados mediante la consulta pública editorial. YouTube en navbar enlaza al catálogo. La migración `videos.0001_initial` crea el modelo y su relación.

Los tests usan únicamente datos temporales. No se descargaron assets ni se incorporaron vídeos, URLs o IDs reales. La evolución futura podrá automatizar metadatos tras evaluar API, permisos y costes.
