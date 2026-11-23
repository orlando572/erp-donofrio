# Capturas del Sprint 3

## Capturas de HU-23 (Evelyn)

Tomadas el 23/11/2026 en la BD `donofrio` con los datos de `scripts/cargar_transacciones.py` (16 semanas, del 3/8 al 22/11/2026). Los dashboards son los estándar de Community (`spreadsheet_dashboard_*`); las vistas son las guardadas por código en `donofrio_base/data/vistas_gerencia_data.xml`.

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-23_dashboard_ventas` | HU-23 | Dashboard «Ventas» con los datos del script: 358 órdenes y S/ 6.9 M de ingreso en 90 días; las ventas mensuales suben de agosto a octubre |
| `HU-23_dashboard_metricas_almacen` | HU-23 | Dashboard «Métricas del almacén»: stock disponible por ubicación (Lima y Arequipa) y 0 líneas con stock negativo. Limitaciones: los títulos de los gráficos salen en inglés (Odoo no los traduce) y la tarjeta de lo reservado dice «No data» porque no hay stock reservado |
| `HU-23_vista_ventas_linea_canal_mes` | HU-23 | Vista guardada «Ventas por línea, canal y mes»: pivote por categoría, equipo de venta (canal) y mes, en soles y en unidades |
| `HU-23_vista_produccion_producto_mes` | HU-23 | Vista guardada «Producción por producto y mes»: cantidad producida por producto y mes de inicio de la orden (agosto a noviembre) |
| `HU-23_vista_stock_por_vencer` | HU-23 | Vista guardada «Stock por vencer (30 días)»: lotes con existencias que vencen en 30 días |
