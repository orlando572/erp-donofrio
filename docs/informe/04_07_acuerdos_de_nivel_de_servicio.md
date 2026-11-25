# 4.7 Acuerdos de niveles de servicio (ANS)

Las mediciones salen de corridas reales (k6, Lighthouse, respaldos, réplica y pruebas) sobre una PC con Docker y datos de demostración. Las metas son supuestos del proyecto: D'Onofrio es un caso académico y no firmó ningún ANS real.

## 4.7.1 Identificación de métricas clave

**Tabla 4.15. Métricas clave**

| Tipo | Métrica | Medición |
|---|---|---|
| **Técnica** | Tiempo de respuesta p95 (k6, 20 usuarios) | 9 a 18 ms en listas, formularios y tablero; 342 ms en el login |
| | Rendimiento web (Lighthouse) | Login 100; dashboard 80; backend 59 |
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

## 4.7.3 Definición y clasificación de acuerdos de servicio (SLA)

Un SLA fija lo que el equipo de TI se compromete a dar (ISO/IEC 20000-1 e ITIL 4). La prioridad de los tickets sale de impacto × urgencia y el campo «Cumplimiento del SLA» lo marca al cerrarse.

**Tabla 4.17. Acuerdos de servicio**

| Grupo | Meta del acuerdo | Medido | Cumple |
|---|---|---|---|
| Disponibilidad | ≥ 99 % en horario laboral con reinicio automático | Mecanismos configurados; porcentaje no medido | Parcial |
| Tiempo de respuesta | p95 < 2 s con 20 usuarios; tablero < 3 s | 9 a 18 ms; LCP de 1.9 s y 2.11 s | Sí |
| Resolución de tickets | P1: respuesta 30 min, resolución 4 h; P2: 2 h y 8 h; P3: 8 h y 3 días; P4: 1 día y 5 días | Se mide la resolución, no la respuesta | Parcial |
| Continuidad | RPO de 24 h (respaldo) y de segundos (réplica); RTO ≤ 2 h | Retraso de 2 ms; restauración en 31 s | Sí |
| Soporte | Lunes a viernes de 8:00 a 18:00, por la mesa de servicios | Mesa de servicios cargada por código | Sí |

## 4.7.4 Prácticas de ITIL 4 que respaldan los ANS

Sin certificación, el proyecto sigue las prácticas de ITIL 4 de solicitudes e incidentes (anexos 10.3 y 10.5), niveles de servicio, capacidad y cambios (anexo 10.4).
