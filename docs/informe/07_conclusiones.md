# 7. Conclusiones

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [02 §2.2](../plan/02_mapeo_plantilla.md) (fila «7. Conclusiones»: una por objetivo y por área), [3.2.4](03_aspectos_generales.md) (problemas), [4.2.2](04_02_requerimientos_funcionales.md) (RF), [4.2.3](04_02_requerimientos_no_funcionales.md) (RNF), los mini gates de [`docs/scrum/gates/`](../scrum/gates/) y las evidencias de `docs/capturas/sprint-3/` y `sprint-4/`
>
> Las conclusiones son las del proyecto **con la Fase 2 completa** (M1 a M4 en `main` desde el [PR #229](https://github.com/orlando572/erp-donofrio/pull/229), releases `v1.1.0` a `v1.4.0`). Los datos de D'Onofrio son ficticios y las mediciones salen de una sola PC.

## 7.1 Conclusión general

El proyecto cumple su **meta principal**: un ERP sobre Odoo 19 Community y PostgreSQL 16, sin licencias Enterprise, donde cada lote se puede seguir desde el insumo hasta el cliente, la calidad y la temperatura dejan rastro ligado al lote, el heladero liquida con un documento firmable y la gerencia ve datos consolidados. El núcleo (`donofrio_base`) se entregó configurado por código y los **cuatro módulos propios de la Fase 2** (calidad, liquidación de heladeros, cadena de frío y tablero) se construyeron uno a uno, con su mini gate. En números: **115 de 121 puntos** de historias de usuario ([6.2](06_01_a_06_03_equipo_sprints_y_project.md)), **218 pruebas automáticas** en verde en el CI, **82 PR fusionados**, cinco *releases* (`v1.0.0` a `v1.4.0`), un despliegue protegido y respaldado, y una restauración de 31 s. Lo que no cumple todavía es el **rendimiento web del backend y del tablero** (límite conocido).

## 7.2 Una conclusión por problema del caso

| # | Problema (3.2.4) | Conclusión | Evidencia |
|---|---|---|---|
| 1 | La liquidación de heladeros es manual | **Resuelto con M2.** La liquidación diaria por heladero calcula lo vendido (despachado − devuelto − merma), el importe a precio de heladero, la comisión y la diferencia de efectivo, crea y confirma el pedido de venta y se imprime con firmas. Límite: la vista móvil solo se vio en un emulador | HU-20 y HU-21 ([PR #223](https://github.com/orlando572/erp-donofrio/pull/223) y [#225](https://github.com/orlando572/erp-donofrio/pull/225)); [5.5c](05_05_modulo_donofrio_heladeros.md); `v1.2.0` |
| 2 | Los lotes vencen sin control y no hay FEFO | **Resuelto.** Los lotes llevan vencimiento, la salida respeta el orden por vencimiento, un lote vencido no se despacha y hay alerta 30 días antes | HU-11; prueba del flujo pedido → entrega → factura (HU-33) |
| 3 | Las temperaturas se anotan a mano | **Resuelto con M3.** Cada cámara tiene su rango, las lecturas fuera de rango crean una actividad para el jefe de almacén y un *cron* avisa de los lotes por vencer. Límite: lecturas manuales, sin sensores | HU-19 ([PR #226](https://github.com/orlando572/erp-donofrio/pull/226)); [5.5d](05_05_modulo_donofrio_frio.md); `v1.3.0` |
| 4 | La calidad no se liga al lote | **Resuelto con M1.** La inspección por puntos de control queda ligada a la orden y al lote, el certificado se emite en PDF y un lote rechazado no se despacha, ni por transferencia ni por el punto de venta | HU-17 y HU-18 ([PR #219](https://github.com/orlando572/erp-donofrio/pull/219) y [#220](https://github.com/orlando572/erp-donofrio/pull/220)); [5.5b](05_05_modulo_donofrio_calidad.md); `v1.1.0` |
| 5 | La planificación no usa datos consolidados | **Resuelto.** Dashboards y vistas guardadas por línea, canal y mes, y el tablero propio de M4 con seis tarjetas, gráfico de ventas y filtro por almacén | HU-23 y HU-22; 4.7; [5.5e](05_05_modulo_donofrio_tablero.md); `v1.4.0` |
| 6 | Cada área digita por separado | **Resuelto.** Un solo ERP; el ciclo vender-comprar-producir-facturar se prueba de punta a punta con datos de demostración (del 3/8 al 22/11/2026) | HU-16 y HU-33 |
| 7 | La gerencia no tiene reportes a tiempo | **Resuelto.** El tablero y los análisis salen del propio ERP; el tablero propio carga en 2.11 s (LCP) | HU-23 y HU-22 |

**Lectura:** de los 7 problemas, **los 7 se resuelven**: 4 con la Fase 1 (2, 5, 6 y 7) y 3 más con los módulos de la Fase 2 (1 con M2, 3 con M3 y 4 con M1). Con solo la Fase 1 habrían quedado 4 resueltos, 2 parciales y 1 sin resolver. Que estén resueltos significa que el sistema lo cubre con datos de demostración; **no se probó con usuarios ni datos reales**.

## 7.3 Una conclusión por área

| Área | Conclusión |
|---|---|
| **Marketing y ventas** | El embudo CRM, las listas de precios por canal y temporada, el punto de venta con boleta y la facturación con IGV cubren el flujo de venta y se probaron de punta a punta. La liquidación del heladero (M2) cierra el canal más reconocible de D'Onofrio. Queda como limitación que no hay envío electrónico a SUNAT (necesita un módulo Enterprise) |
| **Logística y almacén** | Lotes con vencimiento, FEFO, recepción y despacho en dos pasos y reposición a Arequipa funcionan y están probados. La cadena de frío (M3) agrega rangos por cámara, alertas fuera de rango y el aviso de lotes por vencer |
| **Producción** | Las órdenes de producción consumen insumos por FEFO, crean el lote con vencimiento y calculan el costo. Con M1, al terminar la orden nace la inspección del lote y su certificado |
| **Gerencia** | Los dashboards estándar, las vistas guardadas y el tablero propio de M4 muestran ventas, producción, stock por vencer y, según los módulos instalados, calidad, liquidaciones y temperatura. El tablero carga en menos de 3 s (LCP de 2.11 s) pero saca **76** de rendimiento y el backend, **59**, por debajo de la meta de 80: **límite conocido** del JavaScript de Odoo |
| **Compras, finanzas, RR. HH. y TI** | La compra por reabastecimiento mín./máx., la factura de proveedor, los usuarios por rol y la mesa de servicios con SLA funcionan. La disponibilidad del servicio no se midió en el tiempo |
| **Infraestructura y seguridad** | La réplica, los respaldos (restauración en 31 s), el despliegue con Nginx y TLS, la verificación en dos pasos y la auditoría están hechos y verificados; las *releases* `v1.0.0` a `v1.4.0` publican imagen y zip. Las liquidaciones, inspecciones y temperaturas usan el historial del documento y no `auditlog` |

## 7.4 Una conclusión por requerimiento no funcional

| RNF | Resultado | Cumple |
|---|---|---|
| RNF001 portabilidad | Interfaz adaptable de Odoo; el tablero y la liquidación se revisaron en una ventana de 375 × 812 sin desplazamiento horizontal (revisión hecha con Chrome) | Parcial |
| RNF002 rendimiento | p95 de 9 a 18 ms con 20 usuarios virtuales | Sí |
| RNF003 usabilidad | Interfaz en español y marca visual (HU-24); revisión por roles del 25/11 y evaluación heurística de M1 a M4 (6.12) | Cumple con límites |
| RNF004 trazabilidad de lotes | Probada en pedido → entrega y en compra → recepción y producción → lote | Sí |
| RNF005 no se despacha un lote vencido ni rechazado | Probado; con M1 un lote rechazado no sale ni por transferencia ni por el PdV; el PdV no verifica el vencimiento (limitación declarada) | Cumple con límites |
| RNF006 continuidad | RPO de segundos con la réplica y RTO de 31 s | Sí |
| RNF007 mantenibilidad | CI obligatorio con 218 pruebas, `ruff` y `check_legacy.sh` | Sí |
| RNF008 rendimiento del tablero | Login 100, dashboard 80, **tablero 76** (LCP de 2.11 s, cumple los 3 s) y backend 59: **límite conocido** | Parcial |
| RNF009 seguridad | ZAP sin alertas altas, 2FA, TLS, política de contraseñas | Sí, con límites |
| RNF010 auditoría | `auditlog` en precios, pedidos y compras; chatter en los módulos de la Fase 2 | Sí |
| RNF011 disponibilidad | Reinicio automático y *healthcheck*; el 99 % no se midió | Parcial |
| RNF012 reproducibilidad | El entorno se levanta con un comando; cinco *releases* con imagen y zip | Sí |
| RNF013 datos personales | Datos ficticios; sin política de privacidad | Parcial |

Resumen del estado de los 13 RNF: **6 cumplen** (RNF002, 004, 006, 007, 010 y 012), **3 cumplen con límites** (RNF003, 005 y 009) y **4 son parciales** (RNF001, 008, 011 y 013); el detalle está en [4.2.3](04_02_requerimientos_no_funcionales.md).

## 7.5 Conclusión sobre la gestión del proyecto

- **Scrum y revisión cruzada funcionaron.** Cada cambio entró por un PR aprobado por el otro integrante y con el CI en verde (79 de 82 PR con la aprobación vigente); la velocidad fue de 24, 30, 27 y 34 puntos en los cuatro sprints.
- **El tiempo fue el factor decisivo.** El plazo único (viernes 27/11 a las 14:30) obligó a hacer sprints de un día. Los tres sprints del núcleo se completaron en unas 21 horas y la Fase 2 completa se terminó entre el 24 y el 25/11, antes de la hora de corte, gracias al orden fijo M1 → M4 y a los mini gates.
- **Lo inconcluso no se fusionó.** Ningún módulo quedó a medias; los límites de cada uno están declarados en su sección 5.5 y en el anexo 10.1. Lo que quedó fuera es la landing opcional (HU-31).
- **La gestión tiene cosas por mejorar:** las iteraciones del Project están en fechas planificadas y no reales y el estado de varias tarjetas se actualiza a mano (el *workflow* «Item closed» está desactivado).
- **Lo que se aprendió de Odoo 19:** muchas necesidades se resuelven mejor con la configuración estándar que con código propio, y las diferencias de la versión (por ejemplo, los grupos, las prioridades de tareas, la sintaxis de las vistas o la forma de elegir el equipo de ventas) conviene verificarlas en el código antes de prometerlas. Los módulos propios se limitaron a lo que Community no trae (calidad, liquidación, tablero).

## 7.6 Lo que queda para el futuro

- La medición de la disponibilidad en el tiempo (RNF011) y la revisión de la portabilidad en otros navegadores (RNF001).
- Lo que el proyecto recomienda como trabajo futuro real, más allá de los cuatro módulos construidos: sensores de temperatura, app móvil para el heladero, envío electrónico a SUNAT, `auditlog` en los módulos nuevos y pruebas de JavaScript ([8](08_recomendaciones.md)).
