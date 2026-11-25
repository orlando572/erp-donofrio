# 10.1 Fichas de requerimientos funcionales (tabla 39)

Los 18 requerimientos funcionales están implementados: 14 con la Fase 1 y los de la Fase 2 con los módulos M1 (RF011 y RF012), M2 (RF004), M3 (RF008) y M4 (parte propia de RF013). Todos tienen prioridad Must. La tabla resume la ficha de cada uno; los casos de uso están en 4.2.4 y la matriz de trazabilidad en 10.7.

### Tabla 39. Fichas de requerimientos funcionales

| ID | Requerimiento | HU (puntos) | CU | Pruebas automáticas | Estado |
| --- | --- | --- | --- | --- | --- |
| RF001 | Registrar oportunidades por canal en un embudo CRM (3 equipos, 5 etapas, unas 20 oportunidades; de una oportunidad se pasa a cotización) | HU-08 (2) | CU001 | `test_crm` (5) | Implementado |
| RF002 | Cotizar y confirmar pedidos con listas de precios por canal y temporada | HU-09 (3) | CU002 | `test_precios` (6) y flujo de venta | Implementado |
| RF003 | Vender en el punto de venta de la tienda de planta con boleta | HU-10 (3) | CU003 | `test_pdv` (6) | Implementado |
| RF004 | Liquidar diariamente a los heladeros ambulantes (vendido, comisión, diferencia de efectivo, pedido y PDF) | HU-20 (8) y HU-21 (3) | CU004 | `test_liquidacion` (15) | Implementado (M2, `v1.2.0`) |
| RF005 | Gestionar almacenes y ubicaciones con cámaras de frío | HU-06 (3) | CU005 | `test_almacenes` (5) | Implementado |
| RF006 | Controlar lotes con fecha de vencimiento y salida FEFO | HU-11 (5) | CU005 | `test_fefo` (10) | Implementado |
| RF007 | Recibir insumos y despachar pedidos | HU-12 (3) | CU005 | `test_recepcion_despacho` (7) | Implementado |
| RF008 | Registrar temperaturas y alertar cuando están fuera de rango | HU-19 (5) | CU006 | `test_frio` (29) | Implementado (M3, `v1.3.0`) |
| RF009 | Mantener listas de materiales (recetas) y centros de trabajo | HU-07 (5) | CU007 | `test_productos` (11) | Implementado |
| RF010 | Planificar y ejecutar órdenes de producción con lote | HU-14 (3) y HU-33 (3) | CU007 | `test_produccion` (10) y flujo compra-producción (4) | Implementado |
| RF011 | Inspeccionar la calidad por puntos de control ligados a la orden y al lote | HU-17 (8) | CU008 | `test_inspeccion` (13) | Implementado (M1, `v1.1.0`) |
| RF012 | Emitir el certificado de calidad del lote | HU-18 (3) | CU008 | Certificado de aprobada y error en las demás (2) | Implementado (M1, `v1.1.0`) |
| RF013 | Tablero gerencial de KPIs (dashboards estándar y tablero OWL) | HU-23 (3) y HU-22 (8) | CU009 | `test_gerencia` (5) y `test_tablero` (21) | Implementado (M4, `v1.4.0`) |
| RF014 | Análisis por línea, canal y temporada | HU-23 (3) | CU010 | `test_gerencia` | Implementado |
| RF015 | Comprar insumos con reabastecimiento mín./máx. | HU-13 (3) | CU011 | `test_reabastecimiento` (5) | Implementado |
| RF016 | Emitir facturas y boletas con IGV (`l10n_pe`) | HU-03 (3) y HU-15 (3) | CU012 | `test_compania` y `test_facturacion` (10) | Implementado |
| RF017 | Gestionar el organigrama, empleados y puestos | HU-05 (2) | — | `test_rrhh` (5) | Implementado |
| RF018 | Gestionar usuarios y roles por área | HU-04 (3) | — | `test_seguridad` (9) | Implementado |

**Reglas de negocio y límites destacados.** RF004: el pedido usa solo lo vendido y la comisión del 10 % es un supuesto editable. RF008: las lecturas se registran a mano y no hay sensores. RF011 y RF012: los puntos de control son supuestos del caso y un lote sin inspección no se bloquea. RF013: el tablero tiene Lighthouse 76 en escritorio (límite conocido). RF016: se emiten comprobantes con IGV 18 % pero no se envían a SUNAT, porque `l10n_pe_edi` es Enterprise. Las 218 pruebas del repositorio corren en el CI de cada PR sin errores.
