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

## Evidencias de HU-28, mi parte: Lighthouse (Evelyn)

Medido el 23/11/2026 con Lighthouse 12 (modo escritorio) en el login, el backend y el dashboard; mediana de 3 corridas. Análisis en [`docs/informe/04_06_wpo.md`](../../informe/04_06_wpo.md).

| Archivo | HU | Qué contiene |
|---|---|---|
| `HU-28_lighthouse_resultados.csv` | HU-28 | Una fila por vista y etiqueta (`ANTES` en desarrollo con `?debug=assets`; `DESPUES` con Nginx y TLS): puntaje, FCP, LCP, TBT, CLS, Speed Index, peticiones y KB transferidos |

## Capturas de HU-32 (Evelyn)

Tomadas el 23/11/2026 en la BD `donofrio`, con los cinco tickets de ejemplo de la «Mesa de Servicios TI» (proyecto de la app Project de Community, cargado por `donofrio_base`).

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-32_mesa_servicios_kanban` | HU-32 | Tablero Kanban de la mesa con las etapas Nuevo, En análisis, En atención, Resuelto y Cerrado (plegada); tickets abiertos con su tipo ITIL, prioridad en estrellas y fecha límite del SLA |
| `HU-32_pivote_cumplimiento_sla` | HU-32 | Vista guardada «Cumplimiento del SLA por tipo de ticket»: 5 tickets por tipo (Incidente, Solicitud de servicio y Solicitud de acceso) y por estado del SLA (abierto, cumplido, incumplido) |

## Evidencias de HU-28 (Orlando): k6 y ZAP

Corridas del 23/11/2026 sobre el despliegue protegido (`scripts/levantar_prod.sh`) y una base con los datos completos de `scripts/cargar_transacciones.py`. Cómo repetirlas y qué significan: [docs/dev/pruebas_no_funcionales.md](../../dev/pruebas_no_funcionales.md).

| Archivo | HU | Qué muestra |
|---|---|---|
| `HU-28_evidencia_k6_zap.txt` | HU-28 | Salida real de `verificar_despliegue.sh`, de k6 (normal y de esfuerzo, con `docker stats`) y de ZAP antes y después, con el volumen de datos |
| `HU-28_k6_resumen.json`, `HU-28_k6_esfuerzo_resumen.json` | HU-28 | Resumen de métricas de k6 (`--summary-export`) de la prueba normal y de la de esfuerzo |
| `HU-28_zap_reporte.html`, `HU-28_zap_reporte.json` | HU-28 | Reporte de ZAP baseline final: 0 alertas altas; las medias y bajas están aceptadas con su motivo en `scripts/perf/zap-reglas.conf` |

## Evidencias de la sección 5 del informe (Orlando)

Generadas el 23/11/2026; las consultas a PostgreSQL fueron de solo lectura y las pruebas se corrieron en un proyecto de Compose aparte, sin tocar las bases de desarrollo.

| Archivo | Sección | Qué contiene |
|---|---|---|
| `S3-informe5_evidencia_tests_y_dependencias.txt` | 5.4, 5.5 y 5.13 | `scripts/test.sh donofrio_base` (136 pruebas, 0 fallidas, 2 min 1 s) y la salida de `scripts/grafo_dependencias.py` (62 módulos en el árbol de `depends`, 122 con `auto_install`, comparación con una base real) |
| `S3-informe5_evidencia_inyeccion_xss.txt` | 5.12 | Intento de inyección SQL en la búsqueda de contactos (0 filas y la tabla intacta) y de XSS en el parámetro `redirect` del login (sale escapado) |

## Capturas de la sección 4.6 (Evelyn)

Tomadas el 23/11/2026 en la BD `donofrio` con los datos de demostración. Son las pantallas reales que se comparan con los mockups en [`04_06_prototipos_web_y_reportes.md`](../../informe/04_06_prototipos_web_y_reportes.md).

| Archivo | Qué muestra |
|---|---|
| `S3-4.6_pantalla_pedido_de_venta` | Pedido de venta S00437 (lista «Heladero», IGV 18 %, entrega y facturas ligadas) |
| `S3-4.6_reporte_nota_de_entrega` | PDF de la nota de entrega AQP/OUT/00230, con el logo y los datos de la compañía |
| `S3-4.6_reporte_orden_de_produccion` | PDF de la orden de producción WH/MO/00188 con sus operaciones y códigos de barras |

## Evidencias de la sección 6 del informe (Orlando)

Extraídas el 23/11/2026 con `gh` y `git` en modo de solo lectura (no cambian el repositorio) y con `scripts/test.sh` en un proyecto de Compose aparte.

| Archivo | Sección | Qué contiene |
|---|---|---|
| `S3-informe6_evidencia_github.txt` | 6.4 a 6.6 | Configuración del repositorio (métodos de fusión permitidos), protección de `develop` y `main` (`enforce_admins`), ramas remotas, resumen de los 49 PR, ejecuciones y jobs de GitHub Actions, y la ausencia de releases, tags y paquete GHCR |
| `S3-informe6_prs_fusionados.tsv` | 6.6 y trazabilidad | Una fila por PR fusionado: autor, quién fusionó, método (squash o merge commit), aprobación del otro integrante, rama, fecha, commits y merges de `develop`. La lee `scripts/trazabilidad.py` |
| `S3-informe6_evidencia_tests.txt` | 6.10 | `scripts/test.sh donofrio_base` (136 pruebas, 0 fallidas, 125 s), pruebas por archivo, `check_legacy.sh` y `ruff` |

## Evidencias de las secciones 6.1 a 6.3, 6.7 y 6.8 (Evelyn)

Extraídas el 23/11/2026 de GitHub en modo de solo lectura (`gh`, `git` y capturas de las páginas públicas del repositorio y del Project). Texto en [`06_01_a_06_03_equipo_sprints_y_project.md`](../../informe/06_01_a_06_03_equipo_sprints_y_project.md) y [`06_07_a_06_08_commits_e_issues.md`](../../informe/06_07_a_06_08_commits_e_issues.md).

| Archivo | Sección | Qué contiene |
|---|---|---|
| `S3-informe6_burndown.csv` / `.svg` / `.png` | 6.2 | Burndown por puntos de los sprints 1 a 3 (`scripts/burndown.py --csv --svg`): puntos pendientes tras cada HU terminada |
| `S3-6.3_project_sprint_actual.png` | 6.3 | Vista «Sprint actual» (tablero) del GitHub Project |
| `S3-6.3_project_product_backlog.png` | 6.3 | Vista «Product Backlog» (tabla de épicas) |
| `S3-6.3_project_roadmap.png` | 6.3 | Vista «Roadmap» con las iteraciones planificadas |
| `S3-6.3_project_insights.png` | 6.3 | Insights: gráfico *burn up* de ítems |
| `S3-6.7_github_contributors.png` | 6.7 | Contributors de GitHub: commits y líneas por autor en `develop` |
| `S3-informe6_estadisticas_commits_issues.md` | 6.7 y 6.8 | Salida de `scripts/estadisticas_repo.py`: commits por autor y tipo, convención e issues por tipo, área, fase y milestone |
