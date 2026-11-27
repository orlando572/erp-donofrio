# Matriz de trazabilidad: requisito → HU → prueba

Los 18 requisitos funcionales y los 13 no funcionales se relacionan con su historia de usuario y con las pruebas que los verifican (entre paréntesis, la cantidad de pruebas del archivo). Todos los RF están implementados; el repositorio tiene 224 pruebas.

### Tabla 41. Matriz de trazabilidad

| Requisito | HU | Pruebas | Estado |
|---|---|---|---|
| RF001 Registrar oportunidades por canal en un embudo CRM | HU-08 | Pruebas del CRM (5) | Cumple |
| RF002 Cotizar y confirmar pedidos con listas de precios por canal y temporada | HU-09 | Pruebas de precios (6), prueba del flujo de venta (1) | Cumple |
| RF003 Vender en el punto de venta con boleta | HU-10 | Pruebas del punto de venta (6) | Cumple |
| RF004 Liquidar diariamente a los heladeros ambulantes (módulo de Liquidación de heladeros) | HU-20, HU-21 | Pruebas de liquidación (15) | Cumple |
| RF005 Gestionar almacenes y ubicaciones con cámaras de frío | HU-06 | Pruebas de almacenes (5) | Cumple |
| RF006 Controlar lotes con vencimiento y salida FEFO | HU-11 | Pruebas de salida por vencimiento (10) | Cumple |
| RF007 Recibir insumos y despachar pedidos | HU-12 | Pruebas de recepción y despacho (7) | Cumple |
| RF008 Registrar temperaturas y alertar fuera de rango (cadena de frío) | HU-19 | Pruebas de la cadena de frío (29) | Cumple |
| RF009 Mantener listas de materiales (recetas) y centros de trabajo | HU-07 | Pruebas de productos (11) | Cumple |
| RF010 Planificar y ejecutar órdenes de producción con lote | HU-14, HU-33 | Pruebas de producción (10), prueba del flujo de compra y producción (4) | Cumple |
| RF011 Inspeccionar la calidad por puntos de control (módulo de Calidad) | HU-17 | Pruebas de inspección (13) | Cumple |
| RF012 Emitir el certificado de calidad del lote (módulo de Calidad) | HU-18 | Pruebas de inspección (2) | Cumple |
| RF013 Tablero gerencial de KPIs | HU-23, HU-22, HU-24 | Pruebas de gerencia (5), pruebas del tablero (21) | Cumple |
| RF014 Análisis por línea, canal y temporada | HU-23 | Pruebas de gerencia (1) | Cumple |
| RF015 Comprar insumos con reabastecimiento mín./máx. | HU-13 | Pruebas de reabastecimiento (5) | Cumple |
| RF016 Emitir facturas y boletas con IGV (la localización peruana de Odoo) | HU-03, HU-15 | Pruebas de la compañía (8), pruebas de facturación (10) | Cumple |
| RF017 Gestionar el organigrama, empleados y puestos | HU-05 | Pruebas de RR. HH. (5) | Cumple |
| RF018 Gestionar usuarios y roles por área | HU-04 | Pruebas de permisos (9) | Cumple |
| RNF001 Portabilidad: navegador de escritorio y vista adaptable | HU-09, HU-10 | revisión en ventana angosta | Cumple |
| RNF002 Rendimiento: p95 < 2 s con 20 usuarios (k6) | HU-28 | k6 (carga normal y de esfuerzo) | Cumple |
| RNF003 Usabilidad: español y tareas en ≤ 3 pasos | HU-03, HU-06, HU-24 | Pruebas de idioma (6), revisión por roles y evaluación heurística | Cumple |
| RNF004 Trazabilidad del 100 % de los lotes (de la OP al cliente) | HU-14, HU-33 | Prueba del flujo de compra y producción (1), pruebas de producción (1) | Cumple |
| RNF005 Integridad: no se despacha un lote vencido ni uno rechazado por calidad | HU-11, HU-17 | Pruebas de salida por vencimiento (2), prueba del flujo de venta (1), pruebas de inspección (1), pruebas del punto de venta (1) | Cumple |
| RNF006 Respaldo diario (RPO 24 h), réplica (RPO de segundos) y RTO ≤ 2 h | HU-25, HU-26 | restauración cronometrada y el script de verificación de la réplica | Cumple |
| RNF007 Mantenibilidad: lint y tests en CI, sin API obsoleta | HU-02 | Prueba de instalación (1) | Cumple |
| RNF008 El tablero carga en < 3 s; Lighthouse ≥ 80 en el login | HU-23, HU-28, HU-22 | Pruebas del tablero (1) | Cumple |
| RNF009 Seguridad: RBAC, HTTPS, gestor de BD cerrado y 2FA | HU-04, HU-27, HU-28 | Pruebas de permisos (9), pruebas de endurecimiento (12) | Cumple |
| RNF010 Auditoría de cambios en datos sensibles | HU-27 | Pruebas de endurecimiento (2) | Cumple para precios, pedidos y compras |
| RNF011 Disponibilidad ≥ 99 %; reinicio automático y chequeo de salud | HU-01 | chequeos de salud de Docker | Configurado |
| RNF012 Reproducibilidad: el entorno se levanta con un comando | HU-01, HU-29 | levantar el entorno en una PC limpia y el script de prueba de la imagen | Cumple |
| RNF013 Ley 29733: datos personales ficticios y mínimos | HU-03, HU-05, HU-16 | Pruebas de clientes (3) | Cumple |

