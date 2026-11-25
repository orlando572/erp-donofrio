# 10.1 Fichas de requerimientos funcionales (tabla 39)

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn · **Revisa:** Orlando · **Fuente:** [4.2.2](04_02_requerimientos_funcionales.md) (tabla 2), [casos de uso](04_02_casos_de_uso.md), [matriz de trazabilidad](trazabilidad.md), [04 §4.4 del plan](../plan/04_scrum_pmbok.md) (criterios de aceptación) y las pruebas de `addons/donofrio_base/tests/`
>
> Una ficha por RF, con el mismo formato. Los 14 RF de la **Fase 1**, los 2 de **M1** (RF011 y RF012), el de **M2** (RF004) el de **M3** (RF008) y el tablero OWL de **M4** (parte propia de RF013), desde el 24/11/2026, están *Implementados*: ya no queda ningún RF de la Fase 2 como *Diseñado – trabajo futuro*. El estado es el real al 25/11/2026, con los cuatro módulos en `main` ([PR #229](https://github.com/orlando572/erp-donofrio/pull/229)) y las releases `v1.1.0` a `v1.4.0`.

## Resumen

| RF | Requerimiento | Fase | HU | Estado |
|---|---|---|---|---|
| [RF001](#rf001) | Registrar oportunidades por canal en un embudo CRM | F1 | HU-08 | Implementado |
| [RF002](#rf002) | Cotizar y confirmar pedidos con listas de precios por canal y temporada | F1 | HU-09 | Implementado |
| [RF003](#rf003) | Vender en el punto de venta de la tienda de planta con boleta | F1 | HU-10 | Implementado |
| [RF004](#rf004) | Liquidar diariamente a los heladeros ambulantes | F2 | HU-20 | Implementado (M2) |
| [RF005](#rf005) | Gestionar almacenes y ubicaciones con cámaras de frío | F1 | HU-06 | Implementado |
| [RF006](#rf006) | Controlar lotes con fecha de vencimiento y salida FEFO | F1 | HU-11 | Implementado |
| [RF007](#rf007) | Recibir insumos y despachar pedidos | F1 | HU-12 | Implementado |
| [RF008](#rf008) | Registrar temperaturas y alertar cuando están fuera de rango | F2 | HU-19 | Implementado (M3) |
| [RF009](#rf009) | Mantener listas de materiales (recetas) y centros de trabajo | F1 | HU-07 | Implementado |
| [RF010](#rf010) | Planificar y ejecutar órdenes de producción con lote | F1 | HU-14 | Implementado |
| [RF011](#rf011) | Inspeccionar la calidad por puntos de control ligados a la OP y al lote | F2 | HU-17 | Implementado (M1) |
| [RF012](#rf012) | Emitir el certificado de calidad del lote | F2 | HU-18 | Implementado (M1) |
| [RF013](#rf013) | Tablero gerencial de KPIs | F1 y F2 | HU-23, HU-22 | Implementado (dashboards estándar y tablero OWL de M4) |
| [RF014](#rf014) | Análisis por línea, canal y temporada | F1 | HU-23 | Implementado |
| [RF015](#rf015) | Comprar insumos con reabastecimiento mín./máx. | F1 | HU-13 | Implementado |
| [RF016](#rf016) | Emitir facturas y boletas con IGV (`l10n_pe`) | F1 | HU-03 | Implementado |
| [RF017](#rf017) | Gestionar el organigrama, empleados y puestos | F1 | HU-05 | Implementado |
| [RF018](#rf018) | Gestionar usuarios y roles por área | F1 | HU-04 | Implementado |

**Pruebas:** el repositorio tiene **218 pruebas** (137 de `donofrio_base`, 45 de `donofrio_calidad`, 15 de `donofrio_heladeros` y 21 de `donofrio_tablero`; `scripts/test.sh`) que corren en el CI de cada PR; la última corrida, sobre `develop` `339c907` (25/11/2026), terminó con `0 failed, 0 error(s) of 218 tests`. Las capturas están en `docs/capturas/sprint-N/`.

**RF de la Fase 2: HU, PR y release.**

| RF | Módulo | HU | PR fusionados | Release |
|---|---|---|---|---|
| RF011, RF012 | M1 `donofrio_calidad` | HU-17, HU-18 | [#219](https://github.com/orlando572/erp-donofrio/pull/219), [#220](https://github.com/orlando572/erp-donofrio/pull/220), [#221](https://github.com/orlando572/erp-donofrio/pull/221) | [`v1.1.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.1.0) |
| RF004 | M2 `donofrio_heladeros` | HU-20, HU-21 | [#223](https://github.com/orlando572/erp-donofrio/pull/223), [#225](https://github.com/orlando572/erp-donofrio/pull/225) | [`v1.2.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.2.0) |
| RF008 | M3 cadena de frío (en `donofrio_calidad`) | HU-19 | [#226](https://github.com/orlando572/erp-donofrio/pull/226) | [`v1.3.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.3.0) |
| RF013 (parte propia) | M4 `donofrio_tablero` | HU-22, HU-24 | [#227](https://github.com/orlando572/erp-donofrio/pull/227), [#228](https://github.com/orlando572/erp-donofrio/pull/228) | [`v1.4.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.4.0) |

Los cuatro módulos llegaron a `main` juntos con el [PR #229](https://github.com/orlando572/erp-donofrio/pull/229) (*merge commit*). Los datos de demostración de todas las vistas (3/8 al 22/11/2026) son de la HU-16 ([PR #230](https://github.com/orlando572/erp-donofrio/pull/230)) y las capturas en PNG, del [PR #231](https://github.com/orlando572/erp-donofrio/pull/231).

## RF001

### Ficha RF001: Registrar oportunidades por canal en un embudo CRM

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF001 · Registrar oportunidades por canal en un embudo CRM |
| **Área** | Marketing y Ventas |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-08 (2 pts, Evelyn) |
| **Caso de uso** | CU001 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Ejecutivo comercial (principal), Vendedor |
| **Descripción** | Registrar posibles clientes (distribuidores, autoservicios, bodegas y heladeros por reclutar) y moverlos por un embudo de 5 etapas hasta ganarlos o perderlos. |
| **Criterios de aceptación** | 3 equipos de venta, 5 etapas (Prospecto, Calificado, Propuesta, Negociación, Ganado) y unas 20 oportunidades; de una oportunidad se pasa a una cotización. |
| **Reglas de negocio y limitaciones** | Cada oportunidad pertenece a un equipo de venta (canal). Datos ficticios. |
| **Implementación** | `addons/donofrio_base/data/crm_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_crm.py (5)` |
| **Evidencia** | `docs/capturas/sprint-2/HU-08_* (2)` |
| **PR fusionados** | [#168](https://github.com/orlando572/erp-donofrio/pull/168), [#172](https://github.com/orlando572/erp-donofrio/pull/172) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu001_embudo_crm.png` |
| **Estado** | **Implementado** |

## RF002

### Ficha RF002: Cotizar y confirmar pedidos con listas de precios por canal y temporada

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF002 · Cotizar y confirmar pedidos con listas de precios por canal y temporada |
| **Área** | Marketing y Ventas |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-09 (3 pts, Evelyn) |
| **Caso de uso** | CU002 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Vendedor (principal), Jefe de Ventas, Cliente (externo) |
| **Descripción** | Cotizar con el precio que corresponde al canal y a la fecha (verano, Navidad, heladero) y confirmar el pedido, que genera la entrega. |
| **Criterios de aceptación** | El precio cambia según la lista y la fecha; el pedido confirmado genera la entrega. |
| **Reglas de negocio y limitaciones** | Moneda PEN; IGV 18 %. La aprobación de descuentos es un paso manual con historial en la cotización (no hay regla automática). La vigencia de las listas se evalúa en hora de Lima (corrección del PR #171). |
| **Implementación** | `addons/donofrio_base/data/precios_data.xml`<br>`addons/donofrio_base/data/clientes_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_precios.py (6)`<br>`addons/donofrio_base/tests/test_flujo_venta.py::test_pedido_entrega_por_fefo_y_factura_con_ruc` |
| **Evidencia** | `docs/capturas/sprint-2/HU-09_* (2)` |
| **PR fusionados** | [#167](https://github.com/orlando572/erp-donofrio/pull/167), [#171](https://github.com/orlando572/erp-donofrio/pull/171), [#172](https://github.com/orlando572/erp-donofrio/pull/172) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu002_cotizacion.png` |
| **Estado** | **Implementado** |

## RF003

### Ficha RF003: Vender en el punto de venta de la tienda de planta con boleta

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF003 · Vender en el punto de venta de la tienda de planta con boleta |
| **Área** | Marketing y Ventas |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-10 (3 pts, Evelyn) |
| **Caso de uso** | CU003 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Cajero de PdV (principal), Cliente (externo) |
| **Descripción** | Vender en el mostrador de la tienda de planta, emitir la boleta y cerrar la caja. |
| **Criterios de aceptación** | Sesión de PdV, venta, boleta con DNI o cliente varios y cierre de caja cuadrado. |
| **Reglas de negocio y limitaciones** | Boleta tipo 03 para consumidor final; IGV 18 %. **Limitación:** el PdV no aplica FEFO ni comprueba el vencimiento del lote que escribe el cajero (RNF005). |
| **Implementación** | `addons/donofrio_base/hooks.py` |
| **Pruebas** | `addons/donofrio_base/tests/test_pdv.py (6)` |
| **Evidencia** | `docs/capturas/sprint-2/HU-10_* (8)` |
| **PR fusionados** | [#170](https://github.com/orlando572/erp-donofrio/pull/170), [#172](https://github.com/orlando572/erp-donofrio/pull/172) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu003_pdv.png` |
| **Estado** | **Implementado** |

## RF004

### Ficha RF004: Liquidar diariamente a los heladeros ambulantes

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF004 · Liquidar diariamente a los heladeros ambulantes |
| **Área** | Marketing y Ventas |
| **Fase** | F2 (`donofrio_heladeros`, M2) |
| **Prioridad** | Must (en F2) |
| **Historias de usuario** | HU-20 (8 pts) y HU-21 (3 pts), Evelyn |
| **Caso de uso** | CU004 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Liquidador de Heladeros (principal), Heladero concesionario, Supervisor de Heladeros |
| **Descripción** | Liquidar al heladero al volver de la ruta: despachado, devuelto, merma, vendido, importe y comisión, con el PDF para firmar. |
| **Criterios de aceptación** | Líneas con despachado, devuelto y merma; vendido = despachado − devuelto − merma (≥ 0); importe y comisión; al liquidar se crea y confirma el pedido de venta; PDF con las firmas y vista móvil usable. |
| **Reglas de negocio y limitaciones** | El heladero es concesionario (supuesto S4) y no empleado. Sin el módulo se cubre en parte con un pedido de venta con la lista «Heladero» y la devolución estándar (BPMN TO-BE 11). |
| **Implementación y evidencia** | `addons/donofrio_heladeros` ([5.5c](05_05_modulo_donofrio_heladeros.md)); `tests/test_liquidacion.py`; `docs/capturas/sprint-4/HU-20_*` y `HU-21_*` |
| **Diseño disponible** | `docs/diagramas/pantallas/mk_cu004_liquidacion.png`<br>`docs/diagramas/pantallas/mk_rp_liquidacion_heladero.png`<br>`docs/diagramas/bpmn/to-be_heladero_m2.png` |
| **Lo que falta** | Nada de lo diseñado para M2. Límites: el pedido solo mueve stock por lo vendido y la vista angosta se revisó en una ventana de 375 × 812. |
| **Estado** | **Implementado** (M2, 24/11/2026) |

## RF005

### Ficha RF005: Gestionar almacenes y ubicaciones con cámaras de frío

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF005 · Gestionar almacenes y ubicaciones con cámaras de frío |
| **Área** | Logística y Almacén |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-06 (3 pts, Orlando) |
| **Caso de uso** | CU005 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefe de Almacén (principal), CD Arequipa |
| **Descripción** | Tener los almacenes de Lima y Arequipa con ubicaciones de congelación, refrigeración y seco, y la ruta Lima → Arequipa. |
| **Criterios de aceptación** | 2 almacenes (WH-LIM y WH-AQP), 8 ubicaciones de frío y seco y la ruta de reposición Lima → Arequipa. |
| **Reglas de negocio y limitaciones** | Los rangos de temperatura van en el nombre de la ubicación; su registro con alertas es la cadena de frío (RF008). |
| **Implementación** | `addons/donofrio_base/data/almacenes_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_almacenes.py (5)` |
| **Evidencia** | `docs/capturas/sprint-1/HU-06_* (3)` |
| **PR fusionados** | [#156](https://github.com/orlando572/erp-donofrio/pull/156) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu005_recepcion_lote.png` |
| **Estado** | **Implementado** |

## RF006

### Ficha RF006: Controlar lotes con fecha de vencimiento y salida FEFO

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF006 · Controlar lotes con fecha de vencimiento y salida FEFO |
| **Área** | Logística y Almacén |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-11 (5 pts, Orlando) |
| **Caso de uso** | CU005 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefe de Almacén (principal), Comprador |
| **Descripción** | Pedir lote y vencimiento al recibir, reservar primero el lote que vence antes y avisar 30 días antes del vencimiento. |
| **Criterios de aceptación** | Al recibir se pide el lote y la fecha; la entrega reserva primero el lote que vence antes; un lote vencido no se reserva; alerta 30 días antes. |
| **Reglas de negocio y limitaciones** | FEFO en todas las categorías; helado y chocolate vencen a los 12 meses y el panetón a los 4. **Limitación:** el PdV no lo aplica. |
| **Implementación** | `addons/donofrio_base/data/productos_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_fefo.py (10)` |
| **Evidencia** | `docs/capturas/sprint-2/HU-11_* (2)` |
| **PR fusionados** | [#169](https://github.com/orlando572/erp-donofrio/pull/169), [#176](https://github.com/orlando572/erp-donofrio/pull/176) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu005_recepcion_lote.png` |
| **Estado** | **Implementado** |

## RF007

### Ficha RF007: Recibir insumos y despachar pedidos

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF007 · Recibir insumos y despachar pedidos |
| **Área** | Logística y Almacén |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-12 (3 pts, Orlando) |
| **Caso de uso** | CU005 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefe de Almacén (principal), Comprador, CD Arequipa |
| **Descripción** | Recibir contra la orden de compra y despachar en dos pasos (pick y ship) en Lima, con transferencia a Arequipa. |
| **Criterios de aceptación** | Recepción desde la OC; pick + ship en Lima; reposición a Arequipa con recepción. |
| **Reglas de negocio y limitaciones** | Despacho en 2 pasos en Lima y en 1 paso en Arequipa; recepción en 1 paso. |
| **Implementación** | `addons/donofrio_base/data/almacenes_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_recepcion_despacho.py (7)` |
| **Evidencia** | `docs/capturas/sprint-2/HU-12_* (2)` |
| **PR fusionados** | [#173](https://github.com/orlando572/erp-donofrio/pull/173), [#176](https://github.com/orlando572/erp-donofrio/pull/176) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu005_recepcion_lote.png` |
| **Estado** | **Implementado** |

## RF008

### Ficha RF008: Registrar temperaturas y alertar cuando están fuera de rango

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF008 · Registrar temperaturas y alertar cuando están fuera de rango |
| **Área** | Logística y Almacén |
| **Fase** | F2 (cadena de frío, M3) |
| **Prioridad** | Must (en F2) |
| **Historias de usuario** | HU-19 (5 pts, Orlando) |
| **Caso de uso** | CU006 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefe de Almacén (principal), Operario de cámara |
| **Descripción** | Registrar la temperatura de cada cámara y avisar cuando sale del rango de su ubicación. |
| **Criterios de aceptación** | Rango por ubicación; registro de temperaturas; si está fuera de rango se marca y se crea una actividad; *cron* de lotes por vencer; pruebas. |
| **Reglas de negocio y limitaciones** | Congelación: −25 °C (producto terminado a −18 °C o menos); refrigerado: 2 a 6 °C (supuesto S5). Los rangos cargados son de −30 a −18 °C (congelación) y de 2 a 6 °C (refrigerados). Las lecturas se registran a mano y la alerta es una actividad para el jefe de almacén; no se bloquean lotes. |
| **Diseño disponible** | `docs/diagramas/pantallas/mk_cu006_temperaturas.png` |
| **Implementación y evidencia** | `addons/donofrio_calidad` ([5.5d](05_05_modulo_donofrio_frio.md)); `tests/test_frio.py` (29 pruebas); `docs/capturas/sprint-4/HU-19_*` |
| **Lo que falta** | Nada de lo diseñado para M3. Límites: sin sensores, sin alerta por lecturas que faltan, y el cron de lotes por vencer convive con la alerta estándar de `product_expiry`. |
| **Estado** | **Implementado** (M3, 24/11/2026) |

## RF009

### Ficha RF009: Mantener listas de materiales (recetas) y centros de trabajo

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF009 · Mantener listas de materiales (recetas) y centros de trabajo |
| **Área** | Producción y Operaciones |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-07 (5 pts, Orlando) |
| **Caso de uso** | CU007 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefe de Producción (principal) |
| **Descripción** | Cargar productos terminados, insumos y recetas con operaciones y centros de trabajo. |
| **Criterios de aceptación** | 25 productos terminados, 22 insumos y 12 recetas con operaciones; seguimiento por lote y vida útil. |
| **Reglas de negocio y limitaciones** | La receta es una tanda industrial (por ejemplo 10 000 paletas); el control de calidad es documental en el nombre de la operación. |
| **Implementación** | `addons/donofrio_base/data/produccion_data.xml`<br>`addons/donofrio_base/data/productos_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_productos.py (11)` |
| **Evidencia** | `docs/capturas/sprint-1/HU-07_* (3)` |
| **PR fusionados** | [#158](https://github.com/orlando572/erp-donofrio/pull/158) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu007_orden_produccion.png` |
| **Estado** | **Implementado** |

## RF010

### Ficha RF010: Planificar y ejecutar órdenes de producción con lote

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF010 · Planificar y ejecutar órdenes de producción con lote |
| **Área** | Producción y Operaciones |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-14 (3 pts, Orlando); HU-33 (3 pts, compartida) |
| **Caso de uso** | CU007 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefe de Producción (principal), Operario de línea, Jefe de Almacén |
| **Descripción** | Ejecutar la orden de producción consumiendo insumos por FEFO y generando el lote con vencimiento y su costo. |
| **Criterios de aceptación** | La OP reserva insumos por FEFO; al producir se crea el lote con vencimiento; se calcula el costo (insumos FIFO más horas del centro de trabajo). |
| **Reglas de negocio y limitaciones** | Lote único por orden; el costo unitario sale menor que el precio de venta; valoración FIFO. |
| **Implementación** | `addons/donofrio_base/data/produccion_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_produccion.py (10)`<br>`addons/donofrio_base/tests/test_flujo_compra_produccion.py (4)` |
| **Evidencia** | `docs/capturas/sprint-2/HU-14_* (2)` |
| **PR fusionados** | [#174](https://github.com/orlando572/erp-donofrio/pull/174), [#176](https://github.com/orlando572/erp-donofrio/pull/176), [#191](https://github.com/orlando572/erp-donofrio/pull/191), [#192](https://github.com/orlando572/erp-donofrio/pull/192) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu007_orden_produccion.png` |
| **Estado** | **Implementado** |

## RF011

### Ficha RF011: Inspeccionar la calidad por puntos de control ligados a la OP y al lote

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF011 · Inspeccionar la calidad por puntos de control ligados a la OP y al lote |
| **Área** | Producción y Operaciones |
| **Fase** | F2 (`donofrio_calidad`, M1) |
| **Prioridad** | Must (en F2) |
| **Historias de usuario** | HU-17 (8 pts, Orlando) |
| **Caso de uso** | CU008 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Inspector de Calidad (principal), Jefe de Producción, Jefe de Almacén |
| **Descripción** | Inspeccionar cada lote por puntos de control (pasteurización, peso neto, microbiología) y aprobar o rechazar. |
| **Criterios de aceptación** | Al terminar la OP se crea la inspección; aprobar o rechazar con mediciones; un lote rechazado no puede entregarse; pruebas. |
| **Reglas de negocio y limitaciones** | Un lote rechazado no se despacha (RNF005). En Community no hay inspecciones de calidad (el módulo Calidad es Enterprise). |
| **Diseño disponible** | `docs/diagramas/pantallas/mk_cu008_inspeccion.png`<br>`docs/diagramas/bpmn/to-be_produccion_m1.png` |
| **Implementación y evidencia** | `addons/donofrio_calidad` ([5.5b](05_05_modulo_donofrio_calidad.md)); `tests/test_inspeccion.py`; `docs/capturas/sprint-4/HU-17_*` |
| **Lo que falta** | Nada de lo diseñado para M1. |
| **Estado** | **Implementado** (M1, 24/11/2026) |

## RF012

### Ficha RF012: Emitir el certificado de calidad del lote

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF012 · Emitir el certificado de calidad del lote |
| **Área** | Producción y Operaciones |
| **Fase** | F2 (`donofrio_calidad`, M1) |
| **Prioridad** | Must (en F2) |
| **Historias de usuario** | HU-18 (3 pts, Orlando) |
| **Caso de uso** | CU008 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefe de Calidad (principal), Inspector de Calidad |
| **Descripción** | Emitir en PDF el certificado de calidad de un lote aprobado. |
| **Criterios de aceptación** | Reporte QWeb con mediciones, responsable y logo; solo para inspecciones aprobadas. |
| **Reglas de negocio y limitaciones** | Depende de RF011. |
| **Diseño disponible** | `docs/diagramas/pantallas/mk_rp_certificado_calidad.png` |
| **Implementación y evidencia** | `report/calidad_report.xml`; `docs/capturas/sprint-4/HU-18_certificado_pdf.png` |
| **Lo que falta** | Nada de lo diseñado para M1. |
| **Estado** | **Implementado** (M1, 24/11/2026) |

## RF013

### Ficha RF013: Tablero gerencial de KPIs

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF013 · Tablero gerencial de KPIs |
| **Área** | Dirección / Gerencia |
| **Fase** | F1 (dashboards estándar) y F2 (tablero OWL, M4) |
| **Prioridad** | Must |
| **Historias de usuario** | HU-23 (3 pts, Evelyn); HU-22 (8 pts, Evelyn, F2) |
| **Caso de uso** | CU009 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Gerente General (principal), Contador |
| **Descripción** | Mostrar a la gerencia los indicadores de ventas, stock y vencimientos en un tablero. |
| **Criterios de aceptación** | F1: dashboards de Community activos y vistas guardadas por código. F2: acción OWL con hasta 6 tarjetas y un gráfico mensual, filtro por almacén, carga en menos de 3 s (medido: 30 a 57 ms la consulta y 177 ms la página, en una PC). |
| **Reglas de negocio y limitaciones** | Solo lectura en Community; el panel de ventas carga en menos de 3 s (RNF008). El rendimiento del backend es 59 frente a la meta de 80 (limitación declarada). Los títulos de algunos gráficos salen en inglés. |
| **Implementación** | `addons/donofrio_base/data/vistas_gerencia_data.xml` (F1) y `addons/donofrio_tablero` (M4, [5.5e](05_05_modulo_donofrio_tablero.md)) |
| **Pruebas** | `addons/donofrio_base/tests/test_gerencia.py (5)` y `addons/donofrio_tablero/tests/test_tablero.py (21)` |
| **Evidencia** | `docs/capturas/sprint-3/HU-23_* (5)` y `docs/capturas/sprint-4/HU-22_*` |
| **PR fusionados** | [#188](https://github.com/orlando572/erp-donofrio/pull/188), [#227](https://github.com/orlando572/erp-donofrio/pull/227), [#228](https://github.com/orlando572/erp-donofrio/pull/228) |
| **Lo que falta** | Nada de lo diseñado para M4. Límites: Lighthouse del tablero da **76** en escritorio (meta 80) y 39 en móvil, declarado como **límite conocido** (LCP de 2.11 s, cumple los 3 s; [4.6.4](04_06_wpo.md)); la tarjeta de cumplimiento cuenta las OP del mes que ya empezaron y el filtro de almacén no aplica a las liquidaciones ([5.5e.8](05_05_modulo_donofrio_tablero.md)). |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu009_tablero.png` |
| **Estado** | **Implementado** (dashboards estándar en F1; tablero OWL en M4, 24/11/2026) |

## RF014

### Ficha RF014: Análisis por línea, canal y temporada

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF014 · Análisis por línea, canal y temporada |
| **Área** | Dirección / Gerencia |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-23 (3 pts, Evelyn) |
| **Caso de uso** | CU010 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Gerente General, Jefe de Ventas |
| **Descripción** | Comparar ventas por línea de producto, canal y mes para ver la estacionalidad. |
| **Criterios de aceptación** | Vistas pivote y gráfico guardadas por código (`ir.filters`): ventas por línea, canal y mes; producción por producto y mes; stock por vencer a 30 días. |
| **Reglas de negocio y limitaciones** | Los filtros son compartidos; los datos son ficticios (supuesto S2). |
| **Implementación** | `addons/donofrio_base/data/vistas_gerencia_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_gerencia.py::test_ventas_por_linea_canal_y_mes_agrupa_con_datos` |
| **Evidencia** | `docs/capturas/sprint-3/HU-23_vista_ventas_linea_canal_mes.png` |
| **PR fusionados** | [#188](https://github.com/orlando572/erp-donofrio/pull/188) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu010_ventas_pivote.png` |
| **Estado** | **Implementado** |

## RF015

### Ficha RF015: Comprar insumos con reabastecimiento mín./máx.

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF015 · Comprar insumos con reabastecimiento mín./máx. |
| **Área** | Compras, Finanzas, RR. HH. y TI |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-13 (3 pts, Evelyn) |
| **Caso de uso** | CU011 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Comprador (principal), Jefe de Almacén, Proveedor (externo), Contador |
| **Descripción** | Generar la solicitud de cotización cuando el stock baja del mínimo y convertirla en orden de compra con su recepción. |
| **Criterios de aceptación** | La regla genera la RFQ; la OC confirmada crea la recepción. |
| **Reglas de negocio y limitaciones** | Mínimo = consumo semanal × (plazo + 7 días) / 7; máximo = mínimo + 2 semanas (supuestos); un proveedor principal por insumo (no se comparan proveedores). |
| **Implementación** | `addons/donofrio_base/data/reabastecimiento_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_reabastecimiento.py (5)` |
| **Evidencia** | `docs/capturas/sprint-2/HU-13_* (5)` |
| **PR fusionados** | [#179](https://github.com/orlando572/erp-donofrio/pull/179) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu011_rfq.png` |
| **Estado** | **Implementado** |

## RF016

### Ficha RF016: Emitir facturas y boletas con IGV (`l10n_pe`)

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF016 · Emitir facturas y boletas con IGV (`l10n_pe`) |
| **Área** | Compras, Finanzas, RR. HH. y TI |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-03 (3 pts, Orlando); HU-15 (3 pts, Evelyn) |
| **Caso de uso** | CU012 ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Contador (principal), Vendedor, Cliente (externo) |
| **Descripción** | Configurar la compañía con la localización peruana y emitir factura (01) o boleta (03) desde el pedido, con IGV 18 %. |
| **Criterios de aceptación** | RUC ficticio válido, PEN, IGV 18 %, `es_PE`, `America/Lima` y plan contable PE; diarios 01 y 03; el tipo de documento depende de RUC o DNI; PDF. |
| **Reglas de negocio y limitaciones** | **Limitación:** sin envío a SUNAT (`l10n_pe_edi` es Enterprise). La plantilla estándar titula «Factura» al PDF de la boleta y rotula «RUC» al DNI. |
| **Implementación** | `addons/donofrio_base/data/compania_data.xml`<br>`addons/donofrio_base/models/sale_order.py` |
| **Pruebas** | `addons/donofrio_base/tests/test_compania.py (7)`<br>`addons/donofrio_base/tests/test_facturacion.py (10)` |
| **Evidencia** | `docs/capturas/sprint-1/HU-03_* (2)`<br>`docs/capturas/sprint-2/HU-15_* (5)` |
| **PR fusionados** | [#155](https://github.com/orlando572/erp-donofrio/pull/155), [#178](https://github.com/orlando572/erp-donofrio/pull/178) |
| **Prototipo** | `docs/diagramas/pantallas/mk_cu012_factura.png` |
| **Estado** | **Implementado** |

## RF017

### Ficha RF017: Gestionar el organigrama, empleados y puestos

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF017 · Gestionar el organigrama, empleados y puestos |
| **Área** | Compras, Finanzas, RR. HH. y TI |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-05 (2 pts, Evelyn) |
| **Caso de uso** | — (sin caso de uso propio: configuración de RR. HH.) ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Jefa de Recursos Humanos (principal) |
| **Descripción** | Mantener el organigrama, los puestos y los empleados en el ERP. |
| **Criterios de aceptación** | Departamentos con jerarquía; 21 empleados ficticios y 18 puestos; vista de organigrama exportable. |
| **Reglas de negocio y limitaciones** | Datos personales ficticios y mínimos (Ley 29733, RNF013). |
| **Implementación** | `addons/donofrio_base/data/rrhh_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_rrhh.py (5)` |
| **Evidencia** | `docs/capturas/sprint-1/HU-05_* (2)` |
| **PR fusionados** | [#160](https://github.com/orlando572/erp-donofrio/pull/160) |
| **Estado** | **Implementado** |

## RF018

### Ficha RF018: Gestionar usuarios y roles por área

| Campo | Contenido |
|---|---|
| **ID / Nombre** | RF018 · Gestionar usuarios y roles por área |
| **Área** | Compras, Finanzas, RR. HH. y TI |
| **Fase** | F1 |
| **Prioridad** | Must |
| **Historias de usuario** | HU-04 (3 pts, Orlando) |
| **Caso de uso** | — (sin caso de uso propio: configuración de seguridad) ([4.2.4](04_02_casos_de_uso.md)) |
| **Actores** | Administrador (principal) |
| **Descripción** | Dar a cada persona solo los permisos de su rol. |
| **Criterios de aceptación** | 10 usuarios con grupos por rol; una regla de registro propia (el usuario del CD Arequipa solo ve operaciones de su almacén); `test_seguridad.py` verifica el `AccessError`. |
| **Reglas de negocio y limitaciones** | Mínimo privilegio; el liquidador ve solo las transferencias de su almacén y el administrador ve ambas. |
| **Implementación** | `addons/donofrio_base/security/donofrio_security.xml`<br>`addons/donofrio_base/security/ir.model.access.csv`<br>`addons/donofrio_base/data/usuarios_data.xml` |
| **Pruebas** | `addons/donofrio_base/tests/test_seguridad.py (9)` |
| **Evidencia** | `docs/capturas/sprint-1/HU-04_* (3)` |
| **PR fusionados** | [#157](https://github.com/orlando572/erp-donofrio/pull/157) |
| **Estado** | **Implementado** |
