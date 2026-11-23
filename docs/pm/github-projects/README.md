# GitHub Project «Scrum ERP D'Onofrio»

[← docs/pm](..)

El proyecto se gestiona en **un solo GitHub Project (v2)** vinculado al repo `erp-donofrio` ([plan 04 §4.11](../../plan/04_scrum_pmbok.md)): https://github.com/users/orlando572/projects/4. Es gratuito, está integrado con los issues, los PR y los commits, y el docente lo ve sin invitación porque el repo y el Project son públicos. Con él se desarrollan las secciones 4.2.11, 4.3.9 y 6.3 de la plantilla.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| [crear_project.sh](crear_project.sh) | Crea los **campos** con la CLI `gh`. El Sprint es de tipo Iteración y se crea con GraphQL porque la CLI no lo soporta |
| [crear_vistas.sh](crear_vistas.sh) | Crea las 3 **vistas** con GraphQL (la CLI `gh` no tiene comando para vistas) |
| [epicas.csv](epicas.csv) | Los **22 issues** de la lista definitiva: tipo, sprint, responsable, prioridad, fase, HU de la checklist y puntos |

## Issues: 22 + bugs

Las HU van como **checklist dentro de un issue de épica** (una por área y dueño en cada sprint). Los riesgos viven en [../plan_riesgos.md](../plan_riesgos.md) y los entregables del informe, en la checklist del issue «Informe final». Hay 15 épicas y 7 issues de gestión (Constitución, Repo, Registro de riesgos, Dailies, Gate 0, Informe final y Entrega); la lista completa está en `epicas.csv`.

- **Título de la épica** con sus HU: `[HU-08, HU-09, HU-10] Ventas, CRM y PdV`.
- **Ramas y commits:** una rama por HU (`feature/HU-xx-*`) y `[HU-xx]` en cada commit.
- **PR:** dice `Parte de #n` y marca su HU en la checklist; **el último PR de la épica la cierra con `Closes #n`**.
- Los módulos de la F2 que el gate no apruebe se cierran como *not planned*, con un enlace al informe del gate. Los mini gates son un comentario en el issue de su módulo.
- «Registro de riesgos» recibe un comentario en cada Retro y «Dailies», un comentario por Daily.

## Campos

| Campo | Tipo | Valores |
|---|---|---|
| Status | Selección | Backlog / Por hacer / En curso / En revisión / Hecho |
| Sprint | Iteración | S0, S1, S2, S3, S4, Cierre |
| Puntos | Número | Suma de los puntos de las HU de la épica; 0 en gestión y bugs |
| Responsable | Selección | Evelyn / Orlando (un solo valor) |
| Fase | Selección | F1 / F2 |
| Tipo | Selección | Épica / Gestión / Bug |
| Prioridad | Selección | Must (F1 y gestión) / Should (M1-M4) / Could (opcionales) |

## Vistas

| Vista | Diseño | Filtro | Uso |
|---|---|---|---|
| Product Backlog | Tabla | `tipo:Épica` | Tabla 8 de la plantilla |
| Sprint actual | Board por Status | `sprint:@current` | Sprint Backlog (tabla 9), Planning, Daily, Review |
| Roadmap | Roadmap | — | Gantt de la 4.2.9 |

## Cómo se creó

```bash
gh project create --owner orlando572 --title "Scrum ERP D'Onofrio"
gh project link 4 --owner orlando572 --repo orlando572/erp-donofrio
gh project edit 4 --owner orlando572 --visibility PUBLIC
docs/pm/github-projects/crear_project.sh 4
docs/pm/github-projects/crear_vistas.sh 4
```

Los issues se crearon con `gh issue create` y se agregaron al Project con `gh project item-add` y `item-edit` a partir de `epicas.csv` y del plan. Requiere el permiso `project` del token (`gh auth refresh -s project`).

## Supuestos y límites

- **Fase:** los issues de gestión llevan F1 (cubren el núcleo); las épicas M1-M4 y «Opcionales» llevan F2.
- **Sprint (Iteración):** el campo exige fechas: S0 = 22/11, S1 = 23/11, S2 = 24/11, S3 = 25/11, S4 = 26/11 y Cierre = 27/11, de 1 día cada una (el *timebox* del plan). Son **provisionales** y se ajustan a las fechas reales de ejecución, que son las que muestra el Gantt de la 4.2.9.
- **Pasos manuales:** la API no configura la **agrupación ni el orden** de las vistas. En *Product Backlog* se agrupa por Fase y se ordena por Prioridad; en *Roadmap* se elige el campo Sprint como fechas.
- **Responsable:** en Transacciones y Pruebas figura Orlando y en el Gate 0, Evelyn; el cuerpo de cada issue nombra a los dos y qué hace cada uno.
- **Burndown:** `scripts/burndown.py` suma los puntos de las épicas cerradas leyendo `gh project item-list 4 --owner orlando572 --format json` (HU de S3).
