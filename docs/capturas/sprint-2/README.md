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
