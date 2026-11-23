# Sprint 2 (Procesos estándar): Planning

**Fecha:** 23/11/2026 · **Timebox:** ~1 día · **Facilita:** Orlando (SM) · **PO:** Evelyn (pendiente de revisar este planning)

## Objetivo del sprint

"El ciclo vender-comprar-producir-facturar funciona de punta a punta con datos."

Fuente: [04 §4.6](../../plan/04_scrum_pmbok.md) y [05 §5.2](../../plan/05_reparto_equipo.md). Fase 1 (núcleo): no hay ningún módulo de la Fase 2 en este sprint.

## Historias de usuario (HU-08 a HU-16: 30 puntos)

| HU | Historia | Criterios de aceptación (resumen) | Pts | Resp. | Req. | Épica |
|---|---|---|---|---|---|---|
| HU-08 | Embudo CRM por canal | 3 equipos, 5 etapas y unas 20 oportunidades; de una oportunidad se pasa a una cotización | 2 | Evelyn | RF001 | #136 |
| HU-09 | Cotizar con listas de precios por canal y temporada | El precio cambia según la lista y la fecha; el pedido confirmado genera la entrega | 3 | Evelyn | RF002 | #136 |
| HU-10 | Vender en el PdV con boleta | Sesión de PdV, venta, boleta con DNI o cliente varios; cierre de caja cuadrado | 3 | Evelyn | RF003 | #136 |
| HU-11 | Lotes con vencimiento y salida FEFO | Al recibir se pide el lote y la fecha; la entrega reserva primero el lote que vence antes; alerta 30 días antes | 5 | Orlando | RF006, RNF005 | #138 |
| HU-12 | Recibir insumos y despachar en 2 pasos | Recepción desde la OC; *pick* + *ship* en Lima; transferencia a AQP | 3 | Orlando | RF007 | #138 |
| HU-13 | Reabastecimiento mín./máx. de insumos | La regla genera la RFQ; la OC confirmada crea la recepción | 3 | Evelyn | RF015 | #137 |
| HU-14 | Órdenes de producción que consumen insumos y generan un lote | La OP reserva insumos por FEFO; al producir se crea el lote con vencimiento; se calcula el costo | 3 | Orlando | RF010 | #138 |
| HU-15 | Factura y boleta con IGV desde el pedido | Diarios 01 y 03; el tipo de documento depende de RUC o DNI; IGV correcto; PDF | 3 | Evelyn | RF016 | #137 |
| HU-16 | 3-4 meses de transacciones generadas por script | `cargar_transacciones.py` con semilla fija; estacionalidad visible. Evelyn: ventas, PdV y compras · Orlando: inventario y producción | 5 | Orlando + Evelyn | — | #139 |
| | **Total** | | **30** | Evelyn 14 · Orlando 11 · compartido 5 | | |

### Épicas del sprint (Project «Scrum ERP D'Onofrio»)

| Issue | Título | Puntos | Responsable |
|---|---|---|---|
| #136 | [HU-08, HU-09, HU-10] Ventas, CRM y PdV | 8 | Evelyn |
| #137 | [HU-13, HU-15] Compras y facturación | 6 | Evelyn |
| #138 | [HU-11, HU-12, HU-14] Inventario y producción | 11 | Orlando |
| #139 | [HU-16] Transacciones de demostración | 5 | Orlando + Evelyn |

## Orden de ejecución de la parte de Orlando

1. **HU-11** (rama `feature/HU-11-lotes-fefo`): pruebas de lotes, FEFO y alerta; el jefe de almacén como responsable de la alerta. Deja las utilidades de prueba que reutilizan las demás.
2. **HU-12** (rama `feature/HU-12-recepcion-despacho`): pruebas de recepción desde la OC, pick + ship y reposición a Arequipa.
3. **HU-14** (rama `feature/HU-14-ordenes-produccion`): valoración FIFO, cuentas de valoración, pruebas de la OP y ajuste de las recetas a tandas industriales.
4. **HU-16** (rama `feature/HU-16-transacciones-inventario`): `cargar_transacciones.py` con inventario inicial, recepciones, órdenes de producción y reposición; deja las funciones de ventas, PdV y compras para Evelyn.

Cada PR se abre **directo contra `develop`**, uno a la vez: cada rama se rebasa sobre `develop` cuando se fusiona la anterior, para no repetir la excepción de los PR apilados del Sprint 1 (ver 4.3.1).

## Documentación del sprint

| Responsable | Entregables |
|---|---|
| Evelyn | BPMN TO-BE de ventas, heladeros y compras; wireframes y mockups de todas las pantallas (incluidas las de la F2); fichas de CU; 4.2.9 |
| Orlando | BPMN TO-BE de producción y de recepción y despacho (con y sin M1); fichas de CU005 a CU008; 4.3.2; 4.3.3; manual de instalación (borrador) |

## Definition of Done (resumen, [04 §4.8](../../plan/04_scrum_pmbok.md))

- PR a `develop` aprobado por el otro integrante y CI en verde.
- Tests para la lógica nueva y ACL para cada modelo nuevo.
- Textos en español, criterios verificados en la UI y capturas en `docs/capturas/sprint-2/`.
- Épica marcada en el Project con el enlace al PR (`Parte de #n`; el último PR de la épica cierra con `Closes #n`).

## Riesgos y dependencias del sprint

- **Cambios de datos `noupdate`.** El ajuste de las recetas (HU-14) obliga a recrear la base en las dos PC. Se avisa a Evelyn antes de fusionarlo.
- **Volumen de las existencias.** Con recetas por tanda industrial el stock de terminados con receta es de decenas de miles de unidades; los terminados sin receta solo tienen inventario inicial. Evelyn dimensiona sus ventas con el resumen que imprime el script.
- **HU-16 depende de las dos partes.** El script es uno solo; la épica #139 se cierra cuando Evelyn agrega ventas, PdV y compras.
- **Aprobación cruzada.** Cada PR de Orlando necesita la aprobación de Evelyn; conviene pedirla apenas el CI esté en verde.
