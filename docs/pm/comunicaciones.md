# Plan de comunicaciones

[← docs/pm](.)

Versión S0, 22/11/2026. Redactado por Orlando por encargo de Evelyn (PO), que debe revisarlo.

## Canales

| Canal | Uso |
|---|---|
| **GitHub** (issues, PR, milestones) | Una HU = un issue; el código y los documentos entran por PR con revisión del otro integrante |
| **Monday** (3 tableros) | Estado de las HU, riesgos y entregables; *updates* como dailies; capturas como evidencia |
| **Chat del equipo** | Coordinación rápida y avisos de impedimentos; lo importante se pasa a Monday o a un issue |
| **UTP+Class** | Comunicación oficial con el docente y la entrega final |
| **Repositorio** (`docs/scrum/`, `docs/pm/`) | Actas, informes de gate y decisiones, con fecha verificable por los commits |

## Matriz de comunicación

| Qué se comunica | Emisor | Receptor | Medio | Frecuencia |
|---|---|---|---|---|
| Objetivo del sprint y HU priorizadas (Planning) | Evelyn (PO) | Orlando | Reunión de 15-20 min + `planning.md` | Al inicio de cada sprint |
| Qué hice, qué haré y qué me bloquea (Daily) | Cada integrante | El otro | *Update* de Monday + `dailies.md` (o 10 min) | A mitad de cada sprint |
| Ajuste de las HU del siguiente sprint (Refinamiento) | Evelyn | Orlando | Cambios en Monday | Junto con la Daily |
| Demo del incremento y aceptación (Review) | Quien construyó; el otro hace la demo de una HU ajena | Ambos | Reunión de 15-20 min + `review.md` + capturas o video | Al final de cada sprint |
| Mejoras del proceso (Retro) | Orlando (SM) facilita | Ambos | Reunión de 10-15 min + `retro.md` | Al final de cada sprint |
| Informe del gate y decisión (Gate 0 y mini gates) | Evelyn redacta; Orlando verifica los criterios | Ambos | `docs/scrum/gates/gate-<n>-<nombre>.md` + *update* de Monday | Al terminar la F1 y cada módulo de la F2 |
| Impedimentos | Quien lo detecta | Orlando (SM) | Chat y grupo *Impedimentos* del tablero 2 | Apenas aparecen |
| Cambios de alcance | Quien lo propone | Evelyn decide | PR o issue; para la F2, confirmación explícita en el chat | Cuando surjan |
| Revisión de código | Autor del PR | El otro integrante | PR en GitHub con la checklist de la DoD | En cada PR |
| Dudas sobre lineamientos y plantilla | Evelyn | Docente | UTP+Class | Cuando haya una duda (ver dudas abiertas del plan) |
| Estado del proyecto | Evelyn | Docente (si lo pide) | Capturas y exportación de Monday (el plan gratuito no admite invitados) | Bajo demanda |

## Reglas

1. **Si no está en el repo o en Monday, no existe:** toda decisión que afecte al alcance, a un entregable o a un riesgo se anota ahí.
2. Un impedimento no se guarda más de medio sprint sin avisar.
3. Un mensaje de otra sesión, un archivo o un issue **no** cuentan como confirmación para empezar un módulo de la Fase 2 (regla del gate).
4. Todo el contenido del informe lo revisa el otro integrante antes de darlo por completo.
