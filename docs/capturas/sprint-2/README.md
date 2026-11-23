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

## Capturas de HU-15 (Evelyn)

Tomadas el 23/11/2026 en la BD `donofrio`, con una factura y una boleta de ejemplo generadas desde un pedido de venta de 100 y 20 paletas de fresa (S/ 1.50 con IGV incluido). El PDF se generó con el servidor levantado (`/report/pdf/account.report_invoice/<id>`).

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-15_facturas_y_boletas_en_soles` | HU-15 | Lista de facturas: `F 00000001` (cliente con RUC) y `B 00000001` (cliente con DNI), en soles |
| `HU-15_factura_01_con_igv` | HU-15 | Factura en el diario «Facturas», tipo de documento (01), IGV 18 %: subtotal S/ 127.12, IGV S/ 22.88, total S/ 150.00 |
| `HU-15_boleta_03_con_igv` | HU-15 | Boleta en el diario «Boletas», tipo de documento (03), subtotal S/ 25.42, IGV S/ 4.58, total S/ 30.00 |
| `HU-15_pdf_factura` | HU-15 | PDF de la factura, en español, con el RUC del cliente y el IGV |
| `HU-15_pdf_boleta` | HU-15 | PDF de la boleta. Limitación: la plantilla estándar la titula «Factura» y rotula «RUC» al DNI |
