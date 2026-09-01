# Fase 6A — Diseño y auditoría de Choomdex

## Definición y MVP 6B

Choomdex será la base táctica interna de consulta de cartas en español; no será una galería ni una fuente de mercado. **APROBABLE AHORA:** 6B debe incluir catálogo vacío operativo, detalle, administración, búsqueda SQLite por nombre/número, Set, Card, slugs, estado público, paginación, placeholders propios y SEO. **POSPONER:** precios, Deck Builder, RAM Analyzer, scraping, APIs, imágenes oficiales y CardPrinting.

## Entidades y diagrama

**APROBABLE AHORA:** `Set` y `Card`; Set permite evitar repetir información de procedencia y preparar navegación. Card representa el registro consultable tal como sea verificado para 6B. **POSPONER:** `CardPrinting`; separar identidad lógica e impresión es correcto si aparecen reimpresiones/promos/foils, pero adelantarlo sin evidencia oficial aumenta complejidad. Variantes se documentarán inicialmente como notas verificables del registro y se migrarán a Printing sólo cuando una fuente aprobada confirme necesidad.

```text
Set
 └── Card ──↔ Articles
       └──↔ Videos

Futuro: Set ── CardPrinting ── Card
```

## Card, Set y taxonomías

Card obligatorio 6B: nombre verificado, slug, Set, estado editorial, identificador/collector number sólo si la fuente lo confirma, timestamps y procedencia resumida. Opcional: texto de reglas, tipo, subtipo, rareza, atributos, coste/RAM, flavor text, idioma de impresión y URL de imagen autorizada. Derivado: URL y SEO. **REQUIERE VERIFICACIÓN:** todos los tipos, rarezas, atributos, keywords, colores/facciones y valores del juego. Empezar como texto/choices únicamente cuando se estabilicen fuentes; entidades propias sólo si hay múltiples valores o vocabulario oficial estable.

Set recomendado con nombre, código, descripción, activo, fechas y procedencia; fecha de lanzamiento sigue pendiente de verificación. RAM puede ser nullable como dato impreso verificado; reglas de RAM y construcción pertenecen al futuro dominio de mazos, nunca a Card.

## Idioma, imágenes, reglas e IP

Guardar idioma de impresión y distinguir texto original, nombre localizado y explicación editorial. No presentar traducción editorial como oficial. El texto de reglas queda vacío hasta contar con fuente y criterio de uso aprobados. 6B funciona sin imágenes; usar placeholder propio. Una URL externa sólo se registra tras autorización/licencia y el almacenamiento local requiere derecho explícito. Estrategia conservadora: datos mínimos, identidad propia y referencias verificables; no se emiten conclusiones legales absolutas.

## Procedencia, estados y relaciones

Fuentes: Nivel A oficial/autorizada para hechos y texto; B secundaria para contraste; C comunidad sólo como pista no publicable sin revisión; D editorial para análisis propio. **APROBABLE AHORA:** fuente principal, URL, fecha de verificación, notas y estado por Card/Set. **POSPONER:** VerificationRecord por campo si el volumen lo justifica. Estados recomendados: `DRAFT` (interno), `REVIEWED` (contrastado, no implica oficial) y `PUBLISHED` (visible); datos no revisados nunca públicos.

Relaciones futuras Card↔Article y Card↔Video deben reutilizar los modelos existentes y filtrar contenido editorial público/activo. No copiar análisis en Card.

## Búsqueda, filtros y mercado

Búsqueda 6B: `icontains` SQLite por nombre y número verificados. Filtros mínimos seguros: Set y estado; tipo sólo si hay taxonomía confirmada. Filtros futuros: subtipo, rareza, keywords, atributos y RAM tras verificación. Mercado se **POSPONE**: un precio depende de impresión, condición, moneda, región, fecha y fuente; futuro `MarketObservation` debe ser separado, nunca `Card.current_price`.

## Matriz de campos

| Campo | Entidad | Obligatorio | Fuente | 6B | Observación |
|---|---|---:|---|---:|---|
| nombre, slug, estado | Card | Sí | A/B contrastada | Sí | slug derivado |
| set | Set/Card | Sí | A/B | Sí | código si confirmado |
| número/tipo/reglas/RAM | Card | No | A | Condicional | pendiente de verificación |
| idioma/traducción | Card | No | A/D | Futuro | distinguir oficial/editorial |
| imagen | Card | No | licencia | No | placeholder propio |
| procedencia | Card/Set | Sí | A–D | Sí | resumen por registro |
| precio | MarketObservation | No | fuente mercado | No | dominio separado |

## Matriz de fuentes

| Información | Preferida | Secundaria | Riesgo | Política |
|---|---|---|---|---|
| nombre, set, número, tipo | A | B | clasificación incorrecta | publicar tras contraste |
| atributos/reglas | A | B | copyright/reglas erróneas | vacío hasta aprobación |
| imágenes | autorización/licencia | ninguna | IP alta | no usar inicialmente |
| traducción | A | D marcada | confusión oficial | etiquetar editorial |
| precio/fecha lanzamiento | fuente verificable | B | volatilidad | posponer/fechar |

## Riesgos e información pendiente

Faltan fuentes oficiales aprobadas, taxonomía oficial, política de texto e imágenes, idiomas disponibles, clasificación de sets/variantes y reglas de mazo/RAM. No se inventarán restricciones. Riesgos: IP, datos inexactos, modelar taxonomías prematuramente y confundir análisis/editorial con hechos. 6B debe empezar vacío, administrado sólo por Admin, con consultas públicas seguras y paginadas.
