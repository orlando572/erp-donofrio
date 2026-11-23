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

## Evidencias de HU-28 (Orlando): k6 y ZAP

Corridas del 23/11/2026 sobre el despliegue protegido (`scripts/levantar_prod.sh`) y una base con los datos completos de `scripts/cargar_transacciones.py`. Cómo repetirlas y qué significan: [docs/dev/pruebas_no_funcionales.md](../../dev/pruebas_no_funcionales.md).

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-28_evidencia_k6_zap.txt` | HU-28 | Salida real de `verificar_despliegue.sh`, de k6 (normal y de esfuerzo, con `docker stats`) y de ZAP antes y después, con el volumen de datos |
| `HU-28_k6_resumen.json`, `HU-28_k6_esfuerzo_resumen.json` | HU-28 | Resumen de métricas de k6 (`--summary-export`) de la prueba normal y de la de esfuerzo |
| `HU-28_zap_reporte.html`, `HU-28_zap_reporte.json` | HU-28 | Reporte de ZAP baseline final: 0 alertas altas; las medias y bajas están aceptadas con su motivo en `scripts/perf/zap-reglas.conf` |
