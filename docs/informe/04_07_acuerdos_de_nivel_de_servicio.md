# 4.7 Acuerdos de niveles de servicio (ANS)

> **Estado:** borrador del Sprint 3 · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [02 §2.2](../plan/02_mapeo_plantilla.md) (4.7), [09 §9.3](../plan/09_normas_marcos.md) (ITIL), [03 §3.3](../plan/03_modulos_odoo.md), RNF en [4.2.3](04_02_requerimientos_no_funcionales.md)
>
> Las **mediciones** de esta sección salen de corridas reales del Sprint 3 (k6, Lighthouse, respaldos y réplica) sobre una PC con Docker y los datos de demostración; ver [limitaciones](#limitaciones). Las **metas** son supuestos del proyecto (S7 del plan): D'Onofrio es un caso académico y no firmó ningún ANS real.

## 4.7.1 Identificación de métricas clave (tabla 14)

Las métricas se agrupan en cuatro tipos. La columna «Fuente» dice de dónde sale cada una; las que dependen de un módulo de la Fase 2 se marcan.

**Tabla 14. Métricas clave**

| Tipo | Métrica | Qué mide | Fuente | Medición actual |
|---|---|---|---|---|
| **Técnica** | Tiempo de respuesta p95 | Lo que tardan el 95 % de las peticiones del cliente web | k6 con 20 usuarios virtuales (`scripts/perf/`) | 9 a 18 ms en listas, formularios, tablero y aplicación; 342 ms en el inicio de sesión |
| | Tasa de errores | Peticiones fallidas sobre el total | k6 | 0 de 2 765 en la carga normal; 1 de 20 888 (0.005 %) en la de esfuerzo |
| | Rendimiento web | Puntaje de rendimiento y LCP de Lighthouse | Lighthouse (`scripts/perf/lighthouse.py`) | Login 100; dashboard 80 (LCP 1.9 s); backend 59 |
| | Disponibilidad del servicio | Tiempo en que el ERP responde | `/web/health` y reinicio automático (`restart: unless-stopped`) | **No medida en el tiempo** (ver limitaciones) |
| | Retraso de la réplica | Lo que tarda la réplica en aplicar un cambio | `pg_stat_replication` (`replay_lag`) | 2 ms |
| | Tiempo de restauración (RTO) | Lo que tarda restaurar un respaldo en una base nueva | `scripts/restore.sh` | 31 s y 11 s en dos restauraciones |
| | Seguridad | Alertas altas de ZAP baseline | ZAP 2.17.0 sobre el despliegue protegido | 0 altas; 4 medias (3 de la política CSP) y 3 bajas |
| **De usuario** | SUS | Percepción de usabilidad, de 0 a 100 | Cuestionario con 5 personas | **Pendiente** (HU-30) |
| | Éxito y tiempo por tarea | Tareas completadas sin ayuda y segundos | Pruebas de usabilidad | **Pendiente** (HU-30) |
| | Cumplimiento del SLA de tickets | Tickets de la mesa de servicios cerrados dentro de su plazo | Pivote «Cumplimiento del SLA por tipo de ticket» (HU-32) | 1 cumplido, 1 incumplido y 3 abiertos (tickets de ejemplo) |
| **De negocio** | Ventas por canal, línea y mes | Importe vendido | Vista guardada «Ventas por línea, canal y mes» y dashboard Ventas (HU-23) | S/ 7.7 M entre agosto y noviembre de 2026 (datos de demostración) |
| | Producción por producto y mes | Unidades producidas | Vista guardada «Producción por producto y mes» (HU-23) | 3 405 000 unidades en 188 órdenes |
| | Stock por vencer | Lotes con existencias que vencen en 30 días | Vista guardada «Stock por vencer (30 días)» y alerta de 30 días (HU-11, HU-23) | Se consulta en cada corrida; ver 4.7.2 |
| | Valor del inventario | Valor del stock por ubicación | Dashboard «Métricas del almacén» | S/ 4.44 M entre Lima y Arequipa |
| | % de lotes aprobados por calidad | Lotes que pasan la inspección | Módulo de calidad (M1, **Fase 2**) | No disponible en la Fase 1 |
| | Liquidaciones pendientes y merma de heladeros | Heladeros sin liquidar y merma por zona | Módulo de heladeros (M2, **Fase 2**) | No disponible en la Fase 1 |
| | Alertas de temperatura | Lecturas fuera de rango en cámaras | Módulo de cadena de frío (M3, **Fase 2**) | No disponible en la Fase 1 |
| **Otras** | Pruebas automáticas | Pruebas de `donofrio_base` que pasan en el CI | `scripts/test.sh` y GitHub Actions | 136 de 136 al cierre del Sprint 3 (la cifra crece con cada HU) |
| | Cumplimiento de la entrega | HU terminadas sobre las planificadas | GitHub Projects | Sprint 1: 24 de 24 pts; Sprint 2: 30 de 30 pts |

## 4.7.2 Definición de KPIs

Un KPI es una métrica con una fórmula, una meta y una fuente. En la **Fase 1** se calculan con los **dashboards estándar de Odoo Community** y con las **vistas guardadas** de HU-23, sin código propio. En la **Fase 2** se centralizarían en el tablero propio (M4, `donofrio_tablero`), que muestra una tarjeta por KPI y solo la de cada módulo que esté instalado.

**Tabla 14b. KPI de la Fase 1**

| KPI | Fórmula | Meta (supuesto) | Fuente | Responsable |
|---|---|---|---|---|
| Ventas del mes por canal | Σ importe sin IGV de los pedidos confirmados del mes, por equipo de venta | Crecer frente al mes anterior en temporada alta (verano y Navidad) | Vista «Ventas por línea, canal y mes» | Jefe de ventas |
| Participación por línea | Importe de la línea ÷ importe total del mes | Sin meta fija: se vigila la estacionalidad | La misma vista | Gerente |
| Cumplimiento de producción | Unidades producidas ÷ unidades planificadas del mes | ≥ 95 % | Vista «Producción por producto y mes» y la orden de producción | Jefe de producción |
| Stock por vencer | N.º de lotes con existencias que vencen en 30 días | 0 lotes sin acción; cada uno con su alerta atendida | Vista «Stock por vencer (30 días)» | Jefe de almacén |
| Rotación de lotes (FEFO) | Lotes despachados fuera del orden FEFO ÷ lotes despachados | 0 % (lo garantiza la estrategia de salida) | Entregas con su lote reservado | Jefe de almacén |
| Cumplimiento del SLA de TI | Tickets cerrados dentro del plazo ÷ tickets cerrados | ≥ 90 % | Pivote «Cumplimiento del SLA por tipo de ticket» | Responsable de TI |
| Cumplimiento de pruebas | Pruebas que pasan ÷ pruebas totales | 100 % en `develop` | CI | Equipo |

**Cumplimiento de producción: limitación.** En la Fase 1 el plan semanal vive en el script de datos de demostración y no en un campo de Odoo, así que la vista muestra lo producido y no la comparación con lo planificado. La fórmula completa necesita registrar la cantidad planificada por mes; queda como mejora (el tablero de la Fase 2 la incluye).

**KPI de la Fase 2 (diseño, sin construir hasta el Gate 0)**

| KPI | Fórmula | Meta (supuesto) | Módulo |
|---|---|---|---|
| % de lotes aprobados | Lotes aprobados ÷ lotes inspeccionados | ≥ 98 % | M1 `donofrio_calidad` |
| Merma de heladeros | Unidades de merma ÷ unidades despachadas, por heladero y zona | ≤ 3 % | M2 `donofrio_heladeros` |
| Liquidaciones pendientes | Liquidaciones en borrador o despachadas al cierre del día | 0 al final de cada día | M2 |
| Alertas de temperatura abiertas | Lecturas fuera de rango sin atender | 0 | M3 cadena de frío |
| Ventas, producción y stock en una sola vista | Las tarjetas del tablero | Carga en menos de 3 s (RNF008) | M4 `donofrio_tablero` |

## 4.7.3 Definición y clasificación de acuerdos de servicio (SLA)

Un SLA fija lo que el equipo de TI se compromete a dar a los usuarios del ERP. Se clasifican en cinco grupos y se relacionan con ISO/IEC 20000-1 (gestión de servicios) y con las prácticas ITIL 4 de [09 §9.3](../plan/09_normas_marcos.md).

**Tabla 15. Acuerdos de servicio**

| Grupo | Indicador | Meta del acuerdo | Medido (Sprint 3) | Cumple | Requisito ISO 20000-1 |
|---|---|---|---|---|---|
| **Disponibilidad** | Disponibilidad en horario laboral | ≥ 99 % (RNF011); reinicio automático y *healthcheck* | Reinicio automático y *healthcheck* configurados; el porcentaje real no se midió | Parcial | Gestión de la disponibilidad |
| **Tiempo de respuesta** | Petición del cliente web, p95 | < 2 s con 20 usuarios (RNF002) | 9 a 18 ms (342 ms en el login) | Sí | Gestión de la capacidad |
| | Carga del tablero | < 3 s (RNF008) | LCP de 1.9 s | Sí | Gestión de la capacidad |
| **Tiempo de resolución** | Ticket **P1 Crítica** (urgente) | Respuesta 30 min · resolución 4 h | Se mide la resolución; la respuesta no se registra | Parcial | Gestión de incidentes |
| | Ticket **P2 Alta** | Respuesta 2 h · resolución 8 h | Ídem | Parcial | Gestión de incidentes |
| | Ticket **P3 Media** | Respuesta 8 h · resolución 3 días | Ídem | Parcial | Gestión de solicitudes de servicio |
| | Ticket **P4 Baja** | Respuesta 1 día · resolución 5 días | Ídem | Parcial | Gestión de solicitudes de servicio |
| **Continuidad (RPO y RTO)** | Respaldo diario | RPO de 24 h | Respaldo diario con retención de 7 días | Sí | Gestión de la continuidad |
| | Réplica en caliente | RPO de segundos | `replay_lag` de 2 ms | Sí | Gestión de la continuidad |
| | Restauración | RTO ≤ 2 h (7 200 s) | 31 s y 11 s | Sí | Gestión de la continuidad |
| **Soporte** | Horario de atención | Lunes a viernes de 8:00 a 18:00 (supuesto) | Mesa de servicios en Project | Sí | Gestión de solicitudes de servicio |
| | Canal | Mesa de servicios TI (Project) y GitHub para cambios | Cargada por código (HU-32) | Sí | Gestión de incidentes |

**Matriz de prioridad.** La prioridad sale de **impacto × urgencia**, y se carga en la mesa de servicios como las cuatro prioridades de Odoo 19: **Urgente (P1)**, **Alta (P2)**, **Media (P3)** y **Baja (P4)**. La fecha límite del ticket se calcula sola según la tabla (4 h, 8 h, 3 días y 5 días, desde su creación); el campo «Cumplimiento del SLA» lo marca como cumplido o incumplido al cerrarse, y de ahí sale el KPI de la sección 4.7.2.

**Cómo se hace cumplir.** El SLA de resolución se vigila con el filtro «Fecha límite → De retraso» de Project (tickets con el plazo pasado) y con el pivote de cumplimiento; el de respuesta, el de continuidad y el de capacidad se comprueban con `scripts/perf/`, `scripts/restore.sh` y `scripts/verificar_replica.sh`.

## Limitaciones

- **Una sola PC.** Las mediciones de k6 y Lighthouse vienen de una PC con 12 procesadores lógicos y 14 GB de RAM, con Docker y sin red real. Sirven para comparar, no como garantía de producción.
- **Disponibilidad sin medir.** No hay un monitor que registre el tiempo en línea: Uptime Kuma es una HU opcional (HU-31). El 99 % queda como meta con sus mecanismos de recuperación (reinicio automático, *healthcheck*, respaldo y réplica), no como un valor medido.
- **El SLA de respuesta no se mide.** Odoo Project no registra cuándo se atendió por primera vez un ticket; solo se mide la resolución. Los tiempos de respuesta de la tabla son el acuerdo, pero hoy no tienen un campo que los compruebe.
- **Horas corridas.** El plazo de un ticket cuenta horas seguidas, no horas de oficina, y no considera feriados.
- **Datos ficticios.** Las cifras de negocio (ventas, producción, inventario) son de los datos de demostración; las metas son supuestos.
- **SUS pendiente.** El cuestionario de usabilidad no se ha aplicado todavía; ver [6.12](06_12_usabilidad.md).
- **Backend de Lighthouse.** El puntaje del backend (59) no llega a 80; ver [4.6.4](04_06_wpo.md).
