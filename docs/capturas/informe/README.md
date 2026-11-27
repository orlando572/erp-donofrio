# Capturas del informe final (2.6.2)

Pantallas reales del sistema implementado que acompañan a los mockups de 2.4.2, en el mismo orden. Se tomaron el 27/11/2026 sobre la base `donofrio` con los datos de demostración (del 3/8 al 22/11/2026), ya con los textos en español de la HU-06. Son PNG de 1600 × 900, tomadas con Chromium sin interfaz entrando con el usuario de demostración de cada rol (por ejemplo `cajero@donofrio.example.com`) y solo con lectura: no se creó, confirmó ni borró ningún registro.

| Archivo | Rol | Menú | Qué muestra |
|---|---|---|---|
| [`01_crm_embudo_por_etapa.png`](01_crm_embudo_por_etapa.png) | Jefe de ventas | CRM › Ventas › Mi flujo | Embudo de oportunidades por etapa (Prospecto a Ganado) con importes y canal |
| [`02_pdv_heladeria.png`](02_pdv_heladeria.png) | Cajero | Punto de venta › Heladería Av. Venezuela | Pantalla de venta con los productos de la heladería y el cliente «Consumidor Final» |
| [`03_liquidacion_despachada.png`](03_liquidacion_despachada.png) | Liquidador | Heladeros › Liquidaciones › LIQ/2026/00126 | Liquidación despachada: despachado, devuelto, merma, vendido, precio, importe y comisión |
| [`04_recepcion_lote_vencimiento.png`](04_recepcion_lote_vencimiento.png) | Jefe de almacén | Inventario › Operaciones › Recepciones › LIM/IN/00016 › Detalles | Recepción hecha con las operaciones detalladas de la pulpa de fresa: lote, fecha de caducidad y de remoción |
| [`05_orden_produccion_terminada.png`](05_orden_produccion_terminada.png) | Jefe de producción | Manufactura › Operaciones › Órdenes de fabricación › WH/MO/00188 | Orden hecha del panetón clásico con su lote y los componentes consumidos |
| [`06_inspeccion_en_medicion.png`](06_inspeccion_en_medicion.png) | Inspector | Calidad › Inspecciones › INS/00184 | Inspección en medición con sus puntos de control y los botones «Aprobar lote» y «Rechazar lote» |
| [`07_lecturas_temperatura.png`](07_lecturas_temperatura.png) | Jefe de almacén | Calidad › Cadena de frío › Lecturas de temperatura | Lecturas por cámara con su rango; la del 21/11 a 7.30 °C está fuera de rango y sale en rojo |
| [`08_tablero_gerencial.png`](08_tablero_gerencial.png) | Gerente | Tablero › Gerencia | Tablero con las seis tarjetas, las ventas por mes y las ventas del mes por canal |
| [`09_factura_igv.png`](09_factura_igv.png) | Contador | Facturación › Clientes › Facturas › F 00000257 | Factura (01) pagada con IGV 18 % por línea, subtotal, IGV y total |

## Ajustes solo de pantalla

- En los formularios (liquidación, recepción, orden de fabricación, inspección y factura) se ocultó el panel de mensajes: su historial lo creó la carga del 24/11 y queda fuera de 3/8–22/11.
- En la factura se ocultó el botón inteligente de apuntes contables, cuyo rótulo Odoo no trae traducido; los apuntes siguen en la pestaña «Apuntes contables».
- En la recepción se eligió la pulpa de fresa porque su lote vence en 2027; el de la leche fresca ya venció y Odoo lo pinta de rojo.
