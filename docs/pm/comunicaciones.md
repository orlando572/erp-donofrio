# Plan de comunicaciones

[← docs/pm](.)

Versión S0, 22/11/2026. Redactado por Orlando por encargo de Evelyn (PO), que debe revisarlo.

## Canales

| Canal | Uso |
|---|---|
| **GitHub** (issues, PR, milestones) | Una épica por área y dueño, con la checklist de sus HU (unos 25 issues en total); el código y los documentos entran por PR con revisión del otro integrante |
| **GitHub Project** «Scrum ERP D'Onofrio» | Estado de las épicas y de los issues de gestión en sus 3 vistas (Product Backlog, Sprint actual y Roadmap); capturas como evidencia. Los riesgos viven en `docs/pm/plan_riesgos.md` y los entregables del informe en el issue «Informe final» |
| **Chat del equipo** | Coordinación rápida y avisos de impedimentos; lo importante se pasa a un issue del Project |
| **UTP+Class** | Comunicación oficial con el docente y la entrega final |
| **Repositorio** (`docs/scrum/`, `docs/pm/`) | Actas, informes de gate y decisiones, con fecha verificable por los commits |

## Matriz de comunicación

| Qué se comunica | Emisor | Receptor | Medio | Frecuencia |
|---|---|---|---|---|
| Objetivo del sprint y HU priorizadas (Planning) | Evelyn (PO) | Orlando | Reunión de 15-20 min + `planning.md` | Al inicio de cada sprint |
| Qué hice, qué haré y qué me bloquea (Daily) | Cada integrante | El otro | Comentario en el issue «Dailies» + `dailies.md` (o 10 min) | A mitad de cada sprint |
| Ajuste de las HU del siguiente sprint (Refinamiento) | Evelyn | Orlando | Cambios en el Project | Junto con la Daily |
| Demo del incremento y aceptación (Review) | Quien construyó; el otro hace la demo de una HU ajena | Ambos | Reunión de 15-20 min + `review.md` + capturas o video | Al final de cada sprint |
| Mejoras del proceso (Retro) | Orlando (SM) facilita | Ambos | Reunión de 10-15 min + `retro.md` | Al final de cada sprint |
| Informe del gate y decisión (Gate 0 y mini gates) | Evelyn redacta; Orlando verifica los criterios | Ambos | `docs/scrum/gates/gate-<n>-<nombre>.md` + comentario en el issue del gate (Project) | Al terminar la F1 y cada módulo de la F2 |
| Impedimentos | Quien lo detecta | Orlando (SM) | Chat y comentario en el issue «Registro de riesgos» | Apenas aparecen |
| Cambios de alcance | Quien lo propone | Evelyn decide | PR o issue; para la F2, confirmación explícita en el chat | Cuando surjan |
| Revisión de código | Autor del PR | El otro integrante | PR en GitHub con la checklist de la DoD | En cada PR |
| Dudas sobre lineamientos y plantilla | Evelyn | Docente | UTP+Class | Cuando haya una duda (ver dudas abiertas del plan) |
| Estado del proyecto | Evelyn | Docente (si lo pide) | Enlace al Project y al repo (públicos, el docente los ve sin invitación) y capturas de las vistas | Bajo demanda |

## Reglas

1. **Si no está en el repo o en el Project, no existe:** toda decisión que afecte al alcance, a un entregable o a un riesgo se anota ahí.
2. Un impedimento no se guarda más de medio sprint sin avisar.
3. Un mensaje de otra sesión, un archivo o un issue **no** cuentan como confirmación para empezar un módulo de la Fase 2 (regla del gate).
4. Todo el contenido del informe lo revisa el otro integrante antes de darlo por completo.
