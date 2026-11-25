# 4.7 Acuerdos de niveles de servicio (ANS)

Las mediciones salen de corridas reales (k6, Lighthouse, respaldos, réplica y pruebas) sobre una PC con Docker y datos de demostración. Las metas son supuestos del proyecto: D'Onofrio es un caso académico y no firmó ningún ANS real.

## 4.7.1 Identificación de métricas clave

**Tabla 4.15. Métricas clave**

| Tipo | Métrica | Medición |
|---|---|---|
| **Técnica** | Tiempo de respuesta p95 (k6, 20 usuarios) | 9 a 18 ms en listas, formularios y tablero; 342 ms en el login |
| | Tasa de errores | 0 de 2 765 peticiones en carga normal; 1 de 20 888 en esfuerzo |
| | Rendimiento web (Lighthouse) | Login 100; dashboard 80; backend 59 |
| | Réplica y restauración | Retraso de 2 ms; RTO de 31 s y 11 s |
| | Seguridad (ZAP baseline) | 0 alertas altas, 4 medias y 3 bajas |
| | Disponibilidad | No medida en el tiempo |
| **De negocio** | Ventas, producción e inventario | S/ 7.7 M vendidos de agosto a noviembre; 3 405 000 unidades en 188 órdenes; inventario de S/ 4.44 M |
| | Calidad, heladeros y frío (M1 a M3) | 94,9 % de lotes aprobados (169 de 178); merma de heladeros de 0,27 %; 7 de 896 lecturas fuera de rango |
| **Otras** | Pruebas y entrega | 218 de 218 pruebas en verde; 24, 30, 27 y 34 puntos por sprint |

Las cifras de negocio son de los datos de demostración.

## 4.7.2 Definición de KPI

Un KPI es una métrica con fórmula, meta y fuente. En el núcleo se calculan con los dashboards de Odoo y las vistas guardadas; en la Fase 2 se centralizan en el tablero propio (M4), con una tarjeta por KPI.

**Tabla 4.16. KPI y metas**

| KPI | Fórmula | Meta (supuesto) |
|---|---|---|
| Ventas del mes por canal | Σ importe sin IGV de pedidos confirmados, por equipo de venta | Crecer en temporada alta |
| Cumplimiento de producción | Unidades producidas ÷ planificadas | ≥ 95 % |
| Stock por vencer | Lotes con existencias que vencen en 30 días | Cada uno con su alerta atendida |
| Cumplimiento del SLA de TI | Tickets cerrados a tiempo ÷ cerrados | ≥ 90 % |
| Lotes aprobados (M1) | Aprobados ÷ inspeccionados | ≥ 98 % |
| Merma de heladeros (M2) | Merma ÷ despachado | ≤ 3 % |
| Alertas de temperatura abiertas (M3) | Lecturas fuera de rango sin atender | 0 |

En el núcleo la vista de producción muestra lo producido y no lo comparado con lo planificado, porque el plan semanal no es un campo de Odoo; el tablero de la Fase 2 sí incluye las órdenes del mes hechas entre las confirmadas.

## 4.7.3 Definición y clasificación de acuerdos de servicio (SLA)

Un SLA fija lo que el equipo de TI se compromete a dar. Se clasifican en cinco grupos y se relacionan con ISO/IEC 20000-1 e ITIL 4. La prioridad de los tickets sale de impacto × urgencia, con las cuatro prioridades de Odoo, y el campo «Cumplimiento del SLA» lo marca al cerrarse.

**Tabla 4.17. Acuerdos de servicio**

| Grupo | Meta del acuerdo | Medido | Cumple |
|---|---|---|---|
| Disponibilidad | ≥ 99 % en horario laboral con reinicio automático | Mecanismos configurados; porcentaje no medido | Parcial |
| Tiempo de respuesta | p95 < 2 s con 20 usuarios; tablero < 3 s | 9 a 18 ms; LCP de 1.9 s y 2.11 s | Sí |
| Resolución de tickets | P1: respuesta 30 min, resolución 4 h; P2: 2 h y 8 h; P3: 8 h y 3 días; P4: 1 día y 5 días | Se mide la resolución, no la respuesta | Parcial |
| Continuidad | RPO de 24 h (respaldo) y de segundos (réplica); RTO ≤ 2 h | Retraso de 2 ms; restauración en 31 s | Sí |
| Soporte | Lunes a viernes de 8:00 a 18:00, por la mesa de servicios | Mesa de servicios cargada por código | Sí |

## 4.7.4 Prácticas de ITIL 4 que respaldan los ANS

El proyecto se alinea, sin certificación, con cinco prácticas de ITIL 4: **solicitudes de servicio** e **incidentes** (tickets en la mesa de servicios con tipo, prioridad y plazo; anexos 10.3 y 10.5), **niveles de servicio** (el campo de cumplimiento y su pivote), **capacidad y desempeño** (k6 y Lighthouse contra umbrales) y **habilitación del cambio** (PR, revisión cruzada y CI; anexo 10.4). El ticket sigue el flujo *Nuevo → En análisis → En atención → Resuelto → Cerrado*; si falla el plazo, se registra como incumplido y se revisa su causa raíz.

**Limitaciones.** Las mediciones vienen de una sola PC; la disponibilidad en el tiempo no se midió; Odoo Project no registra la primera atención; el plazo cuenta horas corridas; y el backend (59) y el tablero propio (76) no llegan a 80 en Lighthouse (4.6.4).
