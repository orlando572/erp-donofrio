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
