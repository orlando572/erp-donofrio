# Matriz de trazabilidad: requisito → HU → prueba

Los 18 requisitos funcionales y los 13 no funcionales se relacionan con la historia de usuario que los implementa y con las pruebas automáticas que los verifican (entre paréntesis, la cantidad de pruebas del archivo). Todos los RF están implementados, los de la Fase 2 con los módulos M1 a M4 (releases `v1.1.0` a `v1.4.0`). El repositorio tiene **218** pruebas (137 de `donofrio_base`, 45 de `donofrio_calidad`, 15 de `donofrio_heladeros` y 21 de `donofrio_tablero`) y cada celda de archivo, prueba y evidencia se comprobó al generar la matriz.

### Tabla 41. Matriz de trazabilidad

| Requisito | HU | Pruebas | Estado |
|---|---|---|---|
| **RF001** Registrar oportunidades por canal en un embudo CRM | HU-08 | `test_crm` (5) | Cumple |
| **RF002** Cotizar y confirmar pedidos con listas de precios por canal y temporada | HU-09 | `test_precios` (6), `test_flujo_venta` (1) | Cumple |
| **RF003** Vender en el punto de venta con boleta | HU-10 | `test_pdv` (6) | Cumple |
| **RF004** Liquidar diariamente a los heladeros ambulantes (`donofrio_heladeros`) | HU-20, HU-21 | `test_liquidacion` (15) | Cumple |
| **RF005** Gestionar almacenes y ubicaciones con cámaras de frío | HU-06 | `test_almacenes` (5) | Cumple |
| **RF006** Controlar lotes con vencimiento y salida FEFO | HU-11 | `test_fefo` (10) | Cumple |
| **RF007** Recibir insumos y despachar pedidos | HU-12 | `test_recepcion_despacho` (7) | Cumple |
| **RF008** Registrar temperaturas y alertar fuera de rango (cadena de frío) | HU-19 | `test_frio` (29) | Cumple |
| **RF009** Mantener listas de materiales (recetas) y centros de trabajo | HU-07 | `test_productos` (11) | Cumple |
| **RF010** Planificar y ejecutar órdenes de producción con lote | HU-14, HU-33 | `test_produccion` (10), `test_flujo_compra_produccion` (4) | Cumple |
| **RF011** Inspeccionar la calidad por puntos de control (`donofrio_calidad`) | HU-17 | `test_inspeccion` (13) | Cumple |
| **RF012** Emitir el certificado de calidad del lote (`donofrio_calidad`) | HU-18 | `test_inspeccion` (2) | Cumple |
| **RF013** Tablero gerencial de KPIs | HU-23, HU-22, HU-24 | `test_gerencia` (5), `test_tablero` (21) | Cumple |
| **RF014** Análisis por línea, canal y temporada | HU-23 | `test_gerencia` (1) | Cumple |
| **RF015** Comprar insumos con reabastecimiento mín./máx. | HU-13 | `test_reabastecimiento` (5) | Cumple |
| **RF016** Emitir facturas y boletas con IGV (`l10n_pe`) | HU-03, HU-15 | `test_compania` (8), `test_facturacion` (10) | Cumple |
| **RF017** Gestionar el organigrama, empleados y puestos | HU-05 | `test_rrhh` (5) | Cumple |
| **RF018** Gestionar usuarios y roles por área | HU-04 | `test_seguridad` (9) | Cumple |
| **RNF001** Portabilidad: navegador de escritorio y vista adaptable | HU-09, HU-10 | revisión en ventana angosta | Parcial |
| **RNF002** Rendimiento: p95 < 2 s con 20 usuarios (k6) | HU-28 | k6 (carga normal y de esfuerzo) | Cumple |
| **RNF003** Usabilidad: español y tareas en ≤ 3 pasos | HU-03, HU-24 | revisión por roles y evaluación heurística | Cumple con límites |
| **RNF004** Trazabilidad del 100 % de los lotes (de la OP al cliente) | HU-14, HU-33 | `test_flujo_compra_produccion` (1), `test_produccion` (1) | Cumple |
| **RNF005** Integridad: no se despacha un lote vencido ni uno rechazado por calidad | HU-11, HU-17 | `test_fefo` (2), `test_flujo_venta` (1), `test_inspeccion` (1), `test_pdv` (1) | Cumple con límites |
| **RNF006** Respaldo diario (RPO 24 h), réplica (RPO de segundos) y RTO ≤ 2 h | HU-25, HU-26 | restauración cronometrada y `verificar_replica.sh` | Cumple |
| **RNF007** Mantenibilidad: lint y tests en CI, sin API obsoleta | HU-02 | `test_instalacion` (1) | Cumple |
| **RNF008** El tablero carga en < 3 s; Lighthouse ≥ 80 en el login | HU-23, HU-28, HU-22 | `test_tablero` (1) | Parcial |
| **RNF009** Seguridad: RBAC, HTTPS, gestor de BD cerrado y 2FA | HU-04, HU-27, HU-28 | `test_seguridad` (9), `test_hardening` (12) | Cumple con límites |
| **RNF010** Auditoría de cambios en datos sensibles | HU-27 | `test_hardening` (2) | Cumple para precios, pedidos y compras |
| **RNF011** Disponibilidad ≥ 99 %; reinicio automático y healthcheck | HU-01 | *healthchecks* de Docker | Parcial |
| **RNF012** Reproducibilidad: el entorno se levanta con un comando | HU-01, HU-29 | levantar el entorno en una PC limpia y `probar_imagen.sh` | Cumple |
| **RNF013** Ley 29733: datos personales ficticios y mínimos | HU-03, HU-05, HU-16 | `test_clientes` (3) | Parcial |

