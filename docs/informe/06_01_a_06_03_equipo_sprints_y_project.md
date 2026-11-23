# 6.1 a 6.3 Equipo Scrum, cuadro de sprints y GitHub Projects

> **Estado:** borrador del Sprint 3 · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [02 §2.2](../plan/02_mapeo_plantilla.md), [04 §4.1, §4.4 y §4.11](../plan/04_scrum_pmbok.md), [05 §5.1](../plan/05_reparto_equipo.md), `docs/scrum/`, `docs/pm/roles.md`
>
> Las cifras salen de GitHub (solo lectura) con [`scripts/burndown.py`](../../scripts/burndown.py) al 23/11/2026. Se pueden repetir en cualquier momento con `python3 scripts/burndown.py`.

## 6.1 Descripción del Scrum Team

El equipo tiene **dos personas** que comparten todos los roles de desarrollo. La Guía Scrum permite que el Product Owner y el Scrum Master también sean Developers; en un equipo de dos es la única opción realista, y los roles se reparten para que **quien hace una responsabilidad no sea quien debe controlarla** (por ejemplo, el PR de cada uno lo aprueba el otro).

| Rol | Responsable | Responsabilidades |
|---|---|---|
| **Product Owner** | Evelyn | Ordena el Product Backlog; redacta las HU y sus criterios de aceptación; representa a D'Onofrio (gerencia y áreas); acepta o rechaza el incremento en la Review; mantiene el GitHub Project; redacta el informe del Gate 0 y lleva la decisión; sube la entrega final |
| **Scrum Master** | Orlando | Facilita Planning, Daily, Review y Retro; cuida la Definition of Done y el CI; elimina impedimentos técnicos (Docker, Odoo, agente de IA); mide la velocidad y el burndown; protege el *timebox*; verifica los criterios de salida del gate y la entrega |
| **Developers** | Evelyn y Orlando | Construyen el incremento: módulos, configuración, pruebas y documentación. Cada uno revisa **todos** los PR del otro |

**Asistente de IA.** Es una herramienta de los Developers y **no es un rol**. Se declara en la metodología del informe (riesgo R5), y el equipo revisa y entiende todo lo que firma.

### Reparto por áreas

| | Evelyn | Orlando |
|---|---|---|
| Áreas de negocio | Marketing y Ventas (CRM, ventas, PdV, heladeros), Gerencia, y los extras administrativos (compras, facturación, RR. HH., mesa de servicios TI) | Logística (almacenes, lotes, FEFO), Producción (MRP), configuración base, infraestructura y seguridad |
| Módulos de la Fase 2 (dueño) | M2 `donofrio_heladeros`, M4 `donofrio_tablero` | M1 `donofrio_calidad`, M3 cadena de frío |
| Entregables finales | Informe, presentación; sube la entrega | Manuales, zip de la última release; verifica la entrega |

### Cómo trabaja el equipo

- **Un sprint dura un día** (*timebox* de ~1 día): el plazo es único y fijo, la entrega del viernes 27/11 a las 14:30.
- **Daily asíncrona**, escrita en `docs/scrum/sprint-N/dailies.md` y en el issue «Dailies» (#132).
- **Una rama y un PR por HU**, directo contra `develop`, con aprobación del otro integrante y CI en verde (anexo 10.4).
- **Conocimiento cruzado:** en cada Review el otro integrante demuestra una HU ajena (regla de [05 §5.1](../plan/05_reparto_equipo.md)).

**Evidencia de la revisión cruzada.** Todos los PR fusionados tienen al menos una revisión del otro integrante (medido en [6.4 a 6.6](06_04_a_06_06_repositorio.md)).

## 6.2 Resumen del cuadro de sprints

### Cuadro de sprints

Los **puntos** salen de las HU de cada épica (no de la tarjeta de la épica), porque una épica puede estar a medias. Una HU cuenta como terminada si su casilla está marcada o su épica está cerrada; su fecha es la del último PR fusionado con su `[HU-xx]`. Las fechas reales están en **hora de Lima**.

| Sprint | Objetivo | HU | Puntos planificados | Puntos completados | Avance | Fechas en el Project (planificadas) | Fechas reales (primera y última HU) |
|---|---|---|---|---|---|---|---|
| **S0 Inicio** | Proyecto constituido y backlog inicial | — | 0 | 0 | — | 22/11 | 22/11 |
| **S1 Fundaciones** | Odoo 19 corre igual en ambas PC, con CI y datos maestros de D'Onofrio | 7 (HU-01 a 07) | 24 | 24 | 100 % | 23/11 | 22/11 22:38 a 23:39 |
| **S2 Procesos estándar** | El ciclo vender-comprar-producir-facturar funciona de punta a punta con datos | 9 (HU-08 a 16) | 30 | 30 | 100 % | 24/11 | 23/11 02:14 a 14:26 |
| **S3 Calidad del núcleo** | Núcleo v1.0.0 entregable: seguro, replicado, probado, desplegado y documentado | 9 | 29 | 27 | 93 % | 25/11 | 23/11 15:04 a 16:51 (HU-30 pendiente) |
| **S4 Módulos propios** (Fase 2) | Agregar M1, M2, M3 y M4, uno a uno, con mini gate | 8 | 40 | 0 | 0 % | 26/11 | No iniciado: depende del Gate 0 |
| **Cierre** | Entrega | — | 0 | 0 | — | 27/11, 14:30 | — |
| **Total** | | 33 | **123** | **81** | **66 %** | | |

- **Velocidad:** 24, 30 y 27 puntos por sprint; **promedio de 27**. El S3 queda en 27 de 29 solo por la HU-30 (2 puntos), que espera las pruebas de usabilidad con personas.
- **Incrementos y actas:** cada sprint tiene su planning, daily, review y retro en `docs/scrum/sprint-N/`. Del S3 existe el planning; su daily, su review y su retro se escriben al cerrar el sprint.
- Los S1 a S3 son de **Fase 1**; el S4 es la **Fase 2**, que solo empieza con la confirmación del equipo tras el Gate 0.

### Burndown por puntos

![Burndown de los sprints 1 a 3](../capturas/sprint-3/S3-informe6_burndown.png)

Cada punto de la línea amarilla es una HU terminada (fecha de fusión de su último PR); la línea punteada es el ritmo ideal. Los datos exactos están en [`S3-informe6_burndown.csv`](../capturas/sprint-3/S3-informe6_burndown.csv).

**Lectura del gráfico.**
- Los tres sprints bajan **en escalones** y no en pendiente suave: el trabajo de varias HU se fusionó casi a la vez (por ejemplo, tres HU del S2 entre las 02:14 y las 02:15). Es lo esperado cuando cada HU entra por un PR que se aprueba y se fusiona en tandas.
- **S1 y S2 llegan a 0.** El S2 termina con las dos últimas HU (HU-13 y HU-16), que esperaron a que se fusionaran sus dependencias.
- **S3 termina en 2:** los puntos de la HU-30.

### Diferencia entre las fechas del Project y las reales

Las iteraciones del Project se crearon con **un día cada una desde el 23/11** (S1 = 23/11, S2 = 24/11, S3 = 25/11). Pero el equipo avanzó mucho más rápido: los **tres sprints se hicieron en unas 21 horas, entre el 22/11 a las 22:38 y el 23/11 a las 16:51**. Consecuencias:

- La vista «Sprint actual» del Project filtra por `sprint:@current` y por eso **sigue mostrando el S1** (ver 6.3).
- Las barras del Roadmap muestran las fechas planificadas, no las reales.

Las fechas **reales** de esta tabla salen de las fusiones de los PR. Queda como tarea de cierre actualizar las iteraciones del Project a las fechas reales.

## 6.3 Resumen del Monday: GitHub Projects

La gestión del proyecto se hace con **GitHub Projects**, la herramienta gratuita del equipo: está integrada con los issues, los PR y los commits, y el docente la ve sin invitación porque el repositorio es público. (La plantilla menciona Monday; se usó GitHub Projects por esas razones y se declara aquí.)

**Proyecto:** «Scrum ERP D'Onofrio» (<https://github.com/users/orlando572/projects/4>), público, con **22 ítems**: 15 épicas y 7 de gestión.

### Campos

| Campo | Valores | Para qué sirve |
|---|---|---|
| **Status** | Backlog · Por hacer · En curso · En revisión · Hecho | Estado de la tarjeta. Se cambia **a mano**: de los 6 *workflows* del Project solo está activo «Auto-add sub-issues»; «Item closed» (pasar a «Hecho» al cerrar el issue) está desactivado |
| **Puntos** | Número (de la épica) | Alimenta el cuadro de 6.2 |
| **Sprint** | S0 · S1 · S2 · S3 · S4 · Cierre (iteración de 1 día) | Sprint al que pertenece la épica |
| **Responsable** | Evelyn · Orlando | Dueño de la épica |
| **Fase** | F1 · F2 | Núcleo o módulos propios |
| **Tipo** | Épica · Gestión · Bug | Clase de ítem |
| **Prioridad** | Must · Should · Could | Orden |

### Vistas

| Vista | Tipo | Qué muestra | Captura |
|---|---|---|---|
| **Sprint actual** | Tablero (*board*), filtro `sprint:@current` | Las tarjetas del sprint en curso, por estado | ![Sprint actual](../capturas/sprint-3/S3-6.3_project_sprint_actual.png) |
| **Product Backlog** | Tabla, filtro `tipo:Épica`, agrupada por fase y ordenada por sprint | Las 15 épicas con su estado, PR enlazados, sprint y fase | ![Product Backlog](../capturas/sprint-3/S3-6.3_project_product_backlog.png) |
| **Roadmap** | Línea de tiempo por la fecha de cada iteración | Cuándo toca cada épica | ![Roadmap](../capturas/sprint-3/S3-6.3_project_roadmap.png) |
| **Insights** | Gráfico *burn up* de ítems cerrados y abiertos | El avance en el tiempo | ![Insights](../capturas/sprint-3/S3-6.3_project_insights.png) |

El issue **«Dailies» (#132)** es el registro de las dailies; el detalle de cada una está en `docs/scrum/sprint-N/dailies.md`.

### Hallazgos de gestión (al 23/11/2026)

1. **El estado de algunas tarjetas está atrasado.** Las épicas #140 y #142 están **cerradas** en GitHub, pero su tarjeta sigue en «Backlog» (se ve en la captura del Product Backlog); la #141 también está en «Backlog» porque tiene una HU pendiente. La causa es que el *workflow* «Item closed» del Project está **desactivado**, así que el estado solo cambia a mano. Por eso el *burn up* de Insights (que cuenta ítems) no coincide con el burndown por puntos de 6.2, que sale de los issues y los PR. **Mejora:** activar «Item closed» con el valor «Hecho».
2. **Insights cuenta ítems, no puntos.** Para medir por puntos se usa `scripts/burndown.py`.
3. **Las fechas de las iteraciones son las planificadas** (ver 6.2).
4. Las capturas de Insights «al cierre de cada sprint» que pide el plan **se repetirán al cerrar el S3** con los estados al día.
