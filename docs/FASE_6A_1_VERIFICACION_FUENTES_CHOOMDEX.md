# Fase 6A.1 — Verificación de fuentes Choomdex

## Fuentes Nivel A

- Gameplay Guide oficial: https://cyberpunktcg.com/gameplay-guide
- Comprehensive Rules oficial: https://cyberpunktcg.com/comprehensive-rules
- Sitio oficial/WeirdCo: https://cyberpunktcg.com/

## Verificado

**Cyberpunk Trading Card Game (TCG)** es producido por WeirdCo y el sitio declara licencia de CD PROJEKT RED. **Welcome to Night City** está confirmado como producto inicial; código, fecha y conteo permanecen opcionales hasta una fuente específica.

CardType queda verificado con valores canónicos `LEGEND`, `UNIT`, `PROGRAM`, `GEAR`; la traducción es sólo etiqueta UI. La guía confirma tipo, coste, RAM/color de Legends, poder de Units, texto de carta y keywords/timing triggers, pero no como campos homogéneos de todos los tipos. Keywords es formal; sus valores se posponen y podrán ser ManyToMany futura.

RAM está verificada como límite por color aportado por Legends; reglas de construcción verificadas: 3 Legends de nombres únicos, 40–50 cartas principales sin Legends, máximo 3 copias por nombre y límites RAM. Estas reglas son para Deck Builder futuro, no restricciones de Card 6B.

## Contrato 6B

Card: nombre, slug, Set, estado, procedencia, timestamps y CardType; opcionales verificados según tipo: coste, texto, RAM, color, poder y número flexible de texto. Set: nombre, slug, descripción/activo/procedencia; código, fecha y conteo sólo si se verifican. Rareza, subtipo, facción, formato de collector number, traducciones, imágenes y CardPrinting siguen pendientes/pospuestos. No hay evidencia suficiente para CardPrinting en 6B.

6B usará `source_name`, `source_url`, `verified_at`, `verification_notes` por registro. Imágenes: placeholder propio; reglas: política conservadora; mercado: separado y pospuesto. **FASE 6B — GO**, sólo para el contrato anterior, catálogo vacío y carga manual revisada.
