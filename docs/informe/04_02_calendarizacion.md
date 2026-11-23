# 4.2.9 Gestión de calendarización (tabla 6 e ilustración 6)

> **Estado:** borrador del Sprint 2 · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [04 §4.3 y §4.10](../plan/04_scrum_pmbok.md), [05 §5.2](../plan/05_reparto_equipo.md), `docs/scrum/`
>
> Las fechas de los sprints cerrados son **las reales de ejecución** (commits, PR y actas del repositorio), no las planificadas. Las fechas de lo que falta son **previstas**, hasta el único plazo fijo: la entrega del **viernes 27/11/2026 a las 14:30**.

## Cómo se calendariza el proyecto

El plazo es de pocos días, así que cada sprint dura **un día** (*timebox* de ~1 día en cada `planning.md`) y los hitos se ordenan por **criterio de salida**, no por horas estimadas ([04 §4.10](../plan/04_scrum_pmbok.md)). El cronograma se mantiene en el GitHub Project «Scrum ERP D'Onofrio» (campo *Iteración* y vista *Roadmap*) y aquí se resume con las fechas reales.

## Tabla 6: cronograma de hitos

| Hito | Entregable verificable | Sprint | Resp. | Fecha | Estado |
|---|---|---|---|---|---|
| H0 | Acta de constitución; empresa confirmada con el docente | S0 | E | 22/11/2026 | Hecho: acta redactada y empresa asignada por el docente (ver `docs/pm/acta_constitucion.md`) |
| H1 | Entorno Docker + repo + CI en verde | S1 | O | 22/11/2026 | Hecho |
| H2 | Datos maestros de D'Onofrio por código (`donofrio_base`) | S1 | O | 23/11/2026 | Hecho |
| H3 | Ciclo estándar de punta a punta + transacciones | S2 | E+O | 23/11/2026 | Hecho: HU-08 a HU-16 fusionadas en `develop`, 16 semanas de datos de demostración |
| **H4** | **Núcleo v1.0.0 entregable → Gate 0** | **S3** | **E+O** | 24/11/2026 (previsto) | Pendiente |
| H5 | Módulos de la F2 confirmados en el gate, cada uno con su tag (v1.1.0…) | S4 | E+O | 25-26/11/2026 (previsto) | Pendiente: lo decide el equipo en el Gate 0 |
| H6 | Informe PDF, manuales, PPT y zip finales | Cierre | E+O | 26/11/2026 (previsto) | Pendiente |
| H7 | 2 ensayos cronometrados (≤ 10 min) | Cierre | E+O | 26/11/2026 (previsto) | Pendiente |
| **H8** | **Entrega de todo** (UTP+Class, un integrante, un solo intento) | Cierre | E (sube), O (verifica) | **27/11/2026, 14:30** | Pendiente |

## Ilustración 6: diagrama de Gantt

```mermaid
gantt
    title Cronograma real y previsto del proyecto ERP D'Onofrio
    dateFormat YYYY-MM-DD HH:mm
    axisFormat %d/%m
    section Hecho (fechas reales)
    S0 Inicio                      :done, s0, 2026-11-22 08:00, 1d
    S1 Fundaciones (HU-01 a HU-07) :done, s1, 2026-11-22 12:00, 1d
    S2 Procesos estándar (HU-08 a HU-16) :done, s2, 2026-11-23 08:00, 1d
    section Previsto
    S3 Calidad del núcleo (H4)     :active, s3, 2026-11-24 08:00, 1d
    Gate 0                         :milestone, g0, 2026-11-24 20:00, 0d
    S4 Módulos propios, uno a uno  :s4, 2026-11-25 08:00, 2d
    Cierre: informe, manuales, PPT, ensayos :cierre, 2026-11-26 08:00, 1d
    Entrega (H8)                   :crit, milestone, h8, 2026-11-27 14:30, 0d
```

La barra de la Fase 2 (S4) se **recorta o se omite** según lo que decida el equipo en el Gate 0; el Cierre y la entrega **no se mueven** ([07 §7.1, R1](../plan/07_riesgos_entrega.md)).

## Cómo se actualiza

1. Al cerrar cada sprint, se pasan sus fechas de «previsto» a las reales de su `review.md`.
2. Al llegar a H4, el informe del Gate 0 ([`docs/scrum/gates/gate-0-fase1.md`](../scrum/gates/)) fija qué módulos de la F2 entran.
3. El Gantt de GitHub Projects (vista *Roadmap*) debe coincidir con este; si no, manda el del Project y se corrige este archivo.

## Pendiente

- Captura de la vista *Roadmap* del Project como ilustración 6 final (Sprint 3), porque el Project es la fuente de las fechas reales.
- Confirmar con Orlando las fechas previstas de S3, S4 y el Cierre.
