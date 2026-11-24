# 7. Conclusiones

> **Estado:** borrador del Sprint 3 · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [02 §2.2](../plan/02_mapeo_plantilla.md) (fila «7. Conclusiones»: una por objetivo y por área), [3.2.4](03_aspectos_generales.md) (problemas), [4.2.2](04_02_requerimientos_funcionales.md) (RF), [4.2.3](04_02_requerimientos_no_funcionales.md) (RNF) y las evidencias de `docs/capturas/sprint-3/`
>
> **Borrador provisional:** se escribió antes del Gate 0, así que la **Fase 2** y las pruebas de usabilidad aparecen como pendientes; hay que reescribir esos puntos cuando se decida el Gate 0 y se hagan las pruebas. Los datos de D'Onofrio son ficticios y las mediciones salen de una sola PC.

## 7.1 Conclusión general

El proyecto cumple su **meta principal con la Fase 1**: un ERP sobre Odoo 19 Community y PostgreSQL 16, sin licencias Enterprise, donde cada lote se puede seguir desde el insumo hasta el cliente y la gerencia ve datos consolidados. El núcleo se entregó configurado por código, con 24 de las 25 historias de usuario terminadas, 136 pruebas automáticas y un despliegue protegido y respaldado. Lo que no cumple todavía es lo que depende de la **Fase 2** (liquidación de heladeros, calidad, cadena de frío y tablero propio) y de las **pruebas con usuarios**.

## 7.2 Una conclusión por problema del caso

| # | Problema (3.2.4) | Conclusión | Evidencia |
|---|---|---|---|
| 1 | La liquidación de heladeros es manual | **Cubierta en parte.** Con la Fase 1 se vende al heladero con su lista de precios y se registra la devolución; el cálculo automático de lo vendido, la merma y la comisión no se construyó (Fase 2) | Lista «Heladero» (HU-09); BPMN TO-BE; diseño del módulo M2 |
| 2 | Los lotes vencen sin control y no hay FEFO | **Resuelto.** Los lotes llevan vencimiento, la salida respeta el orden por vencimiento, un lote vencido no se despacha y hay alerta 30 días antes | HU-11; prueba del flujo pedido → entrega → factura (HU-33) |
| 3 | Las temperaturas se anotan a mano | **No resuelto en la Fase 1.** Solo hay diseño del registro con alertas | Wireframe y mockup de CU006 |
| 4 | La calidad no se liga al lote | **Parcial.** El lote es trazable de la compra a la entrega; la inspección ligada al lote es de la Fase 2 | HU-11, HU-14, HU-33; diseño del certificado |
| 5 | La planificación no usa datos consolidados | **Resuelto en lo estándar.** Dashboards y vistas guardadas por línea, canal y mes | HU-23; 4.7 |
| 6 | Cada área digita por separado | **Resuelto.** Un solo ERP; el ciclo vender-comprar-producir-facturar se prueba de punta a punta con 16 semanas de datos de demostración | HU-16 y HU-33 |
| 7 | La gerencia no tiene reportes a tiempo | **Resuelto en lo estándar.** El tablero y los análisis salen del propio ERP; el tablero propio es de la Fase 2 | HU-23 |

**Lectura:** de los 7 problemas, **4 se resuelven con la Fase 1** (2, 5, 6 y 7), **1 queda parcial** (4) y **2 dependen de módulos propios** (1 y 3, con una alternativa estándar para el 1).

## 7.3 Una conclusión por área

| Área | Conclusión |
|---|---|
| **Marketing y ventas** | El embudo CRM, las listas de precios por canal y temporada, el punto de venta con boleta y la facturación con IGV cubren el flujo de venta y se probaron de punta a punta. Queda como limitación que no hay envío electrónico a SUNAT (necesita un módulo Enterprise) |
| **Logística y almacén** | Lotes con vencimiento, FEFO, recepción y despacho en dos pasos y reposición a Arequipa funcionan y están probados. La cadena de frío con alertas es de la Fase 2 |
| **Producción** | Las órdenes de producción consumen insumos por FEFO, crean el lote con vencimiento y calculan el costo. La inspección de calidad y el certificado son de la Fase 2 |
| **Gerencia** | Los dashboards estándar y las vistas guardadas muestran ventas, producción y stock por vencer; el panel de ventas carga en menos de 3 s. El backend queda en 59 de rendimiento, por debajo de la meta de 80 |
| **Compras, finanzas, RR. HH. y TI** | La compra por reabastecimiento mín./máx., la factura de proveedor, los usuarios por rol y la mesa de servicios con SLA funcionan. La disponibilidad del servicio no se midió en el tiempo |
| **Infraestructura y seguridad** | La réplica, los respaldos (restauración en 31 s), el despliegue con Nginx y TLS, la verificación en dos pasos y la auditoría están hechos y verificados |

## 7.4 Una conclusión por requerimiento no funcional

| RNF | Resultado | Cumple |
|---|---|---|
| RNF002 rendimiento | p95 de 9 a 18 ms con 20 usuarios virtuales | Sí |
| RNF003 usabilidad | Interfaz en español; el SUS con 5 personas está pendiente | Pendiente |
| RNF004 trazabilidad de lotes | Probada en pedido → entrega y en compra → recepción y producción → lote | Sí |
| RNF005 no se despacha un lote vencido | Probado; el punto de venta no aplica FEFO (limitación declarada) | Parcial |
| RNF006 continuidad | RPO de segundos con la réplica y RTO de 31 s | Sí |
| RNF008 rendimiento del tablero | Login 100, dashboard 80 con LCP de 1.9 s, backend 59 | Parcial |
| RNF009 seguridad | ZAP sin alertas altas, 2FA, TLS, política de contraseñas | Sí |
| RNF011 disponibilidad | Reinicio automático y *healthcheck*; el 99 % no se midió | Parcial |
| RNF012 reproducibilidad | El entorno se levanta con un comando | Sí |

> Los estados de la tabla de [4.2.3](04_02_requerimientos_no_funcionales.md) para RNF002, RNF004, RNF006 y RNF009 todavía dicen «Planificado» o «Parcial» (se escribieron antes de HU-25 a HU-29); esta tabla refleja los resultados medidos y hay que **actualizar 4.2.3** para que coincidan.

## 7.5 Conclusión sobre la gestión del proyecto

- **Scrum y revisión cruzada funcionaron.** Cada cambio entró por un PR aprobado por el otro integrante y con el CI en verde; la velocidad fue de 24, 30 y 27 puntos en los tres primeros sprints.
- **El tiempo fue el factor decisivo.** El plazo único (viernes 27/11 a las 14:30) obligó a hacer sprints de un día; los tres sprints del núcleo se completaron en unas 21 horas, y la Fase 2 quedó fuera del plazo previsto.
- **La gestión tiene cosas por mejorar:** las iteraciones del Project están en fechas planificadas y no reales, y el estado de algunas tarjetas se actualiza a mano.
- **Lo que se aprendió de Odoo 19:** muchas necesidades se resuelven mejor con la configuración estándar que con código propio, y las diferencias de la versión (por ejemplo, los grupos, las prioridades de tareas o la forma de elegir el equipo de ventas) conviene verificarlas en el código antes de prometerlas.

## 7.6 Lo que queda pendiente

- Las pruebas de usabilidad con 5 personas (HU-30).
- La decisión del Gate 0 y, según ella, los módulos de la Fase 2.
- La verificación en Chrome, Firefox y Edge y en móvil (RNF001), y la medición de la disponibilidad en el tiempo.
