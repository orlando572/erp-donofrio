# 4.2.9 Gestión de calendarización

El plazo es de pocos días y la entrega es el viernes 27/11/2026 a las 14:30, así que cada sprint dura **un día** y los hitos se ordenan por criterio de salida y no por horas estimadas. El cronograma se mantiene en el GitHub Project «Scrum ERP D'Onofrio» y las fechas de los sprints cerrados son **las reales de ejecución** (commits, PR y actas), no las planificadas.

**Tabla 4.7. Cronograma de hitos**

| Hito | Entregable | Fecha |
|---|---|---|
| H0 a H2 | Constitución, entorno Docker con CI y datos maestros por código (S0 y S1) | 22 y 23/11/2026 |
| H3 | Ciclo estándar de punta a punta con 16 semanas de datos de demostración (S2) | 23/11/2026 |
| **H4** | **Núcleo `v1.0.0` y punto de control entre fases (S3)** | 23 y 24/11/2026 |
| H5 | Módulos M1 a M4 con sus versiones `v1.1.0` a `v1.4.0` (S4) | 23 al 25/11/2026 |
| H6 y H7 | Informe, manuales, presentación y dos ensayos cronometrados (Cierre) | 25 y 26/11/2026 |
| **H8** | **Entrega de todo** (un integrante, un solo intento) | **27/11/2026, 14:30** |

```mermaid
gantt
    title Cronograma del proyecto ERP D'Onofrio
    dateFormat YYYY-MM-DD HH:mm
    axisFormat %d/%m
    section Ejecución
    S0 Inicio                      :done, s0, 2026-11-22 08:00, 1d
    S1 Fundaciones (HU-01 a HU-07) :done, s1, 2026-11-22 12:00, 1d
    S2 Procesos estándar (HU-08 a HU-16) :done, s2, 2026-11-23 02:00, 12h
    S3 Calidad del núcleo (HU-23 a HU-33) :done, s3, 2026-11-23 15:00, 2h
    Núcleo v1.0.0                  :milestone, g0, 2026-11-24 00:38, 0d
    S4 Módulos propios M1 a M4 (v1.1.0 a v1.4.0) :done, s4, 2026-11-23 23:58, 27h
    section Cierre
    Informe, manuales, presentación y ensayos :active, cierre, 2026-11-25 08:00, 2d
    Entrega (H8)                   :crit, milestone, h8, 2026-11-27 14:30, 0d
```

*Figura 4.15. Diagrama de Gantt con las fechas reales de ejecución y el Cierre hasta la entrega (hora de Lima).*

La Fase 2 se completó antes de la hora de corte fijada para decidir su alcance (jueves 26/11, 08:00); el Cierre y la entrega no se movieron.
