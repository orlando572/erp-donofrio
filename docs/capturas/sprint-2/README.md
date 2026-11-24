# Capturas del Sprint 2 (Orlando)

Tomadas el 23/11/2026 en la BD `donofrio` recién creada con `scripts/init_db.sh` y cargada con `scripts/cargar_transacciones.py` (datos ficticios, semilla 2026).

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-11_recepcion_lote_y_vencimiento` | HU-11 | Detalle de una recepción en Lima: el lote de leche fresca con su fecha de caducidad y de remoción |
| `HU-11_lote_por_vencer` | HU-11 | Lote con la etiqueta «Por vencer»: caducidad, alerta (30 días antes) y fecha de remoción |
| `HU-12_recepcion_insumos` | HU-12 | Recepción de insumos hecha en Lima/Stock, con fecha de origen `DEMO-REC` |
| `HU-12_pick_lima_reposicion_aqp` | HU-12 | Primer paso (pick) de la reposición Lima → Arequipa, de LIM/Stock a LIM/Output |
| `HU-14_op_terminada_con_lote` | HU-14 | Orden de producción hecha: lote `H01-261119` y componentes consumidos |
| `HU-14_op_ordenes_de_trabajo` | HU-14 | Las 4 operaciones de la línea de helados, con duración esperada y real |

## Capturas de HU-13 (Evelyn)

Tomadas el 23/11/2026 en la BD `donofrio`, sin existencias de insumos. Las RFQ las generó el planificador de Odoo (`stock.rule._run_scheduler_tasks`, la tarea programada), no se crearon a mano. El comprador confirmó la de Lácteos.

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-13_reglas_de_reabastecimiento` | HU-13 | Las 22 reglas de los insumos en LIM/Stock, ruta «Comprar», disparo «Auto», con su mínimo y máximo |
| `HU-13_rfq_generadas_por_el_planificador` | HU-13 | Las 6 RFQ (una por proveedor), en soles y a cargo del Comprador |
| `HU-13_rfq_proveedor_lacteos` | HU-13 | RFQ P00001 con leche fresca, crema, leche en polvo y mantequilla, cada una hasta su máximo; se entrega en Planta Lima |
| `HU-13_orden_de_compra_confirmada` | HU-13 | La misma RFQ confirmada («Orden de compra») |
| `HU-13_recepcion_creada_por_la_oc` | HU-13 | Recepción `LIM/IN/00001` creada al confirmar la OC, en estado «Listo», con origen P00001 |
## Capturas de HU-15 (Evelyn)

Tomadas el 23/11/2026 en la BD `donofrio`, con una factura y una boleta de ejemplo generadas desde un pedido de venta de 100 y 20 paletas de fresa (S/ 1.50 con IGV incluido). El PDF se generó con el servidor levantado (`/report/pdf/account.report_invoice/<id>`).

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-15_facturas_y_boletas_en_soles` | HU-15 | Lista de facturas: `F 00000001` (cliente con RUC) y `B 00000001` (cliente con DNI), en soles |
| `HU-15_factura_01_con_igv` | HU-15 | Factura en el diario «Facturas», tipo de documento (01), IGV 18 %: subtotal S/ 127.12, IGV S/ 22.88, total S/ 150.00 |
| `HU-15_boleta_03_con_igv` | HU-15 | Boleta en el diario «Boletas», tipo de documento (03), subtotal S/ 25.42, IGV S/ 4.58, total S/ 30.00 |
| `HU-15_pdf_factura` | HU-15 | PDF de la factura, en español, con el RUC del cliente y el IGV |
| `HU-15_pdf_boleta` | HU-15 | PDF de la boleta. Limitación: la plantilla estándar la titula «Factura» y rotula «RUC» al DNI |

## Capturas de HU-16 (Evelyn)

Tomadas el 23/11/2026 en la BD `donofrio` recién creada con `scripts/init_db.sh` y cargada con `scripts/cargar_transacciones.py` completo (16 semanas, del 3/8 al 22/11/2026). Con la semilla fija, cada corrida da lo mismo: 437 pedidos de venta por S/ 9 106 775, 939 pedidos de mostrador y 95 compras.

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-16_ventas_por_mes_grafico` | HU-16 | Análisis de ventas por mes: sube de agosto a octubre (estacionalidad) |
| `HU-16_ventas_por_canal_y_mes` | HU-16 | Unidades vendidas por mes y por equipo de ventas (Heladeros, Canal Tradicional y Canal Moderno) |
| `HU-16_facturas_y_boletas_de_clientes` | HU-16 | 516 documentos de cliente: facturas `F` a crédito (registradas, por vencer) y boletas `B` pagadas |
| `HU-16_facturas_de_proveedor` | HU-16 | 95 facturas de proveedor (01, con IGV) de las compras enlazadas a las recepciones de insumos |
| `HU-16_pdv_sesiones_cerradas` | HU-16 | 96 sesiones de caja de la Heladería Av. Venezuela, de 9:00 a 17:00, todas cerradas y registradas |
