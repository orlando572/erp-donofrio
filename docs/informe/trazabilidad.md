# Matriz de trazabilidad: requisito → HU → PR → módulo → prueba → evidencia

> **Estado:** borrador del Sprint 3 · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [4.2.2](04_02_requerimientos_funcionales.md), [4.2.3](04_02_requerimientos_no_funcionales.md), [6.4 a 6.6](06_04_a_06_06_repositorio.md), [6.9 a 6.13](06_09_a_06_13_pruebas.md)
>
> **Generada por `scripts/trazabilidad.py`** a partir de los PR fusionados ([`S3-informe6_prs_fusionados.tsv`](../capturas/sprint-3/S3-informe6_prs_fusionados.tsv), 23/11/2026) y de las tablas de requisitos del propio script. **Cada celda se comprueba al generar:** el script falla si un archivo, una evidencia o una función de prueba no existe. Para regenerar: `python3 scripts/trazabilidad.py` (o `--gh` para volver a leer los PR de GitHub). No edites este archivo a mano.

**Cómo leerla.** *HU → PR*: las HU de cada requisito y los PR fusionados a `develop` cuyo título o rama llevan esa HU. *Prueba*: archivo de `addons/donofrio_base/tests/` con su número de pruebas, o una prueba concreta. *Evidencia*: archivos del repositorio (el número entre paréntesis es cuántos archivos coinciden con el patrón). *Estado*: el real al 23/11/2026, que puede ser distinto del de las tablas 2 y 3 del informe, escritas en el Sprint 1.

**Resumen.** 18 RF y 13 RNF. Los requisitos de la Fase 2 sin implementar (4 filas: RF004, RF008, RF011 y RF012) están como «Diseñado – trabajo futuro»; la parte propia de RF013 (tablero OWL) también. Las pruebas de `donofrio_base`: **136** (ver [6.10](06_09_a_06_13_pruebas.md)).

## Tabla A. Requisitos funcionales (RF)

| Requisito | Fase | HU → PR | Módulo o archivo | Prueba (n.º de pruebas) | Evidencia | Estado |
|---|---|---|---|---|---|---|
| **RF001** Registrar oportunidades por canal en un embudo CRM | F1 | HU-08: [#168](https://github.com/orlando572/erp-donofrio/pull/168), [#172](https://github.com/orlando572/erp-donofrio/pull/172) | `addons/donofrio_base/data/crm_data.xml` | `test_crm.py` (5) | `docs/capturas/sprint-2/HU-08_*` (2 archivos) | Implementado |
| **RF002** Cotizar y confirmar pedidos con listas de precios por canal y temporada | F1 | HU-09: [#167](https://github.com/orlando572/erp-donofrio/pull/167), [#171](https://github.com/orlando572/erp-donofrio/pull/171), [#172](https://github.com/orlando572/erp-donofrio/pull/172) | `addons/donofrio_base/data/precios_data.xml`<br>`addons/donofrio_base/data/clientes_data.xml` | `test_precios.py` (6)<br>`test_flujo_venta.py::test_pedido_entrega_por_fefo_y_factura_con_ruc` | `docs/capturas/sprint-2/HU-09_*` (2 archivos) | Implementado |
| **RF003** Vender en el punto de venta con boleta | F1 | HU-10: [#170](https://github.com/orlando572/erp-donofrio/pull/170), [#172](https://github.com/orlando572/erp-donofrio/pull/172) | `addons/donofrio_base/hooks.py` | `test_pdv.py` (6) | `docs/capturas/sprint-2/HU-10_*` (8 archivos) | Implementado |
| **RF004** Liquidar diariamente a los heladeros ambulantes (`donofrio_heladeros`) | F2 | HU-20: sin PR (Fase 2)<br>HU-21: sin PR (Fase 2) | — | — | — | Diseñado – trabajo futuro |
| **RF005** Gestionar almacenes y ubicaciones con cámaras de frío | F1 | HU-06: [#156](https://github.com/orlando572/erp-donofrio/pull/156) | `addons/donofrio_base/data/almacenes_data.xml` | `test_almacenes.py` (5) | `docs/capturas/sprint-1/HU-06_*` (3 archivos) | Implementado |
| **RF006** Controlar lotes con vencimiento y salida FEFO | F1 | HU-11: [#169](https://github.com/orlando572/erp-donofrio/pull/169), [#176](https://github.com/orlando572/erp-donofrio/pull/176) | `addons/donofrio_base/data/productos_data.xml` | `test_fefo.py` (10) | `docs/capturas/sprint-2/HU-11_*` (2 archivos) | Implementado |
| **RF007** Recibir insumos y despachar pedidos | F1 | HU-12: [#173](https://github.com/orlando572/erp-donofrio/pull/173), [#176](https://github.com/orlando572/erp-donofrio/pull/176) | `addons/donofrio_base/data/almacenes_data.xml` | `test_recepcion_despacho.py` (7) | `docs/capturas/sprint-2/HU-12_*` (2 archivos) | Implementado |
| **RF008** Registrar temperaturas y alertar fuera de rango (cadena de frío) | F2 | HU-19: sin PR (Fase 2) | — | — | — | Diseñado – trabajo futuro |
| **RF009** Mantener listas de materiales (recetas) y centros de trabajo | F1 | HU-07: [#158](https://github.com/orlando572/erp-donofrio/pull/158) | `addons/donofrio_base/data/produccion_data.xml`<br>`addons/donofrio_base/data/productos_data.xml` | `test_productos.py` (11) | `docs/capturas/sprint-1/HU-07_*` (3 archivos) | Implementado |
| **RF010** Planificar y ejecutar órdenes de producción con lote | F1 | HU-14: [#174](https://github.com/orlando572/erp-donofrio/pull/174), [#176](https://github.com/orlando572/erp-donofrio/pull/176)<br>HU-33: [#191](https://github.com/orlando572/erp-donofrio/pull/191), [#192](https://github.com/orlando572/erp-donofrio/pull/192) | `addons/donofrio_base/data/produccion_data.xml` | `test_produccion.py` (10)<br>`test_flujo_compra_produccion.py` (4) | `docs/capturas/sprint-2/HU-14_*` (2 archivos) | Implementado |
| **RF011** Inspeccionar la calidad por puntos de control (`donofrio_calidad`) | F2 | HU-17: sin PR (Fase 2) | — | — | — | Diseñado – trabajo futuro |
| **RF012** Emitir el certificado de calidad del lote (`donofrio_calidad`) | F2 | HU-18: sin PR (Fase 2) | — | — | — | Diseñado – trabajo futuro |
| **RF013** Tablero gerencial de KPIs | F1 (dashboards estándar) | HU-23: [#188](https://github.com/orlando572/erp-donofrio/pull/188) | `addons/donofrio_base/data/vistas_gerencia_data.xml` | `test_gerencia.py` (5) | `docs/capturas/sprint-3/HU-23_*` (5 archivos) | Implementado con dashboards estándar; el tablero OWL propio (HU-22): Diseñado – trabajo futuro |
| **RF014** Análisis por línea, canal y temporada | F1 | HU-23: [#188](https://github.com/orlando572/erp-donofrio/pull/188) | `addons/donofrio_base/data/vistas_gerencia_data.xml` | `test_gerencia.py::test_ventas_por_linea_canal_y_mes_agrupa_con_datos` | `docs/capturas/sprint-3/HU-23_vista_ventas_linea_canal_mes.png` | Implementado |
| **RF015** Comprar insumos con reabastecimiento mín./máx. | F1 | HU-13: [#179](https://github.com/orlando572/erp-donofrio/pull/179) | `addons/donofrio_base/data/reabastecimiento_data.xml` | `test_reabastecimiento.py` (5) | `docs/capturas/sprint-2/HU-13_*` (5 archivos) | Implementado |
| **RF016** Emitir facturas y boletas con IGV (`l10n_pe`) | F1 | HU-03: [#155](https://github.com/orlando572/erp-donofrio/pull/155)<br>HU-15: [#178](https://github.com/orlando572/erp-donofrio/pull/178) | `addons/donofrio_base/data/compania_data.xml`<br>`addons/donofrio_base/models/sale_order.py` | `test_compania.py` (7)<br>`test_facturacion.py` (10) | `docs/capturas/sprint-1/HU-03_*` (2 archivos)<br>`docs/capturas/sprint-2/HU-15_*` (5 archivos) | Implementado |
| **RF017** Gestionar el organigrama, empleados y puestos | F1 | HU-05: [#160](https://github.com/orlando572/erp-donofrio/pull/160) | `addons/donofrio_base/data/rrhh_data.xml` | `test_rrhh.py` (5) | `docs/capturas/sprint-1/HU-05_*` (2 archivos) | Implementado |
| **RF018** Gestionar usuarios y roles por área | F1 | HU-04: [#157](https://github.com/orlando572/erp-donofrio/pull/157) | `addons/donofrio_base/security/donofrio_security.xml`<br>`addons/donofrio_base/security/ir.model.access.csv`<br>`addons/donofrio_base/data/usuarios_data.xml` | `test_seguridad.py` (9) | `docs/capturas/sprint-1/HU-04_*` (3 archivos) | Implementado |

## Tabla B. Requisitos no funcionales (RNF)

| Requisito | Fase | HU → PR | Módulo o archivo | Prueba (n.º de pruebas) | Evidencia | Estado |
|---|---|---|---|---|---|---|
| **RNF001** Portabilidad: Chrome, Firefox y Edge; responsive | F1 | HU-09: [#167](https://github.com/orlando572/erp-donofrio/pull/167), [#171](https://github.com/orlando572/erp-donofrio/pull/171), [#172](https://github.com/orlando572/erp-donofrio/pull/172)<br>HU-10: [#170](https://github.com/orlando572/erp-donofrio/pull/170), [#172](https://github.com/orlando572/erp-donofrio/pull/172) | — | — | — | Sin evidencia: la prueba manual en 3 navegadores no se registró |
| **RNF002** Rendimiento: p95 < 2 s con 20 usuarios (k6) | F1 | HU-28: [#194](https://github.com/orlando572/erp-donofrio/pull/194), [#196](https://github.com/orlando572/erp-donofrio/pull/196) | `scripts/perf/carga.js`<br>`scripts/perf/k6.sh` | — | `docs/capturas/sprint-3/HU-28_k6_resumen.json`<br>`docs/capturas/sprint-3/HU-28_k6_esfuerzo_resumen.json`<br>`docs/capturas/sprint-3/HU-28_evidencia_k6_zap.txt` | Cumple (p95 de 12 ms) |
| **RNF003** Usabilidad: SUS ≥ 70 y tareas en ≤ 3 pasos | F1 | HU-30: [#195](https://github.com/orlando572/erp-donofrio/pull/195) | `scripts/usabilidad_sus.py`<br>`docs/usabilidad/plan_de_pruebas.md`<br>`docs/usabilidad/formulario_sus.md` | — | `docs/informe/06_12_usabilidad.md` | Parcial: método listo, sin mediciones con las 5 personas |
| **RNF004** Trazabilidad del 100 % de los lotes (de la OP al cliente) | F1 | HU-14: [#174](https://github.com/orlando572/erp-donofrio/pull/174), [#176](https://github.com/orlando572/erp-donofrio/pull/176)<br>HU-33: [#191](https://github.com/orlando572/erp-donofrio/pull/191), [#192](https://github.com/orlando572/erp-donofrio/pull/192) | `addons/donofrio_base/data/produccion_data.xml` | `test_flujo_compra_produccion.py::test_flujo_completo_del_planificador_al_lote_terminado`<br>`test_produccion.py::test_el_lote_producido_sale_despues_por_fefo` | `docs/capturas/sprint-3/S3-informe6_evidencia_tests.txt` | Cumple |
| **RNF005** Integridad: no se despacha un lote vencido (y, en F2, uno rechazado) | F1 | HU-11: [#169](https://github.com/orlando572/erp-donofrio/pull/169), [#176](https://github.com/orlando572/erp-donofrio/pull/176) | `addons/donofrio_base/data/productos_data.xml` | `test_fefo.py::test_lote_vencido_no_se_reserva`<br>`test_fefo.py::test_lote_en_fecha_de_retiro_no_se_reserva`<br>`test_flujo_venta.py::test_un_lote_vencido_no_entra_en_la_entrega_del_pedido` | `docs/capturas/sprint-3/S3-informe6_evidencia_tests.txt` | Parcial: cumple en inventario y ventas; no en el PdV; el lote rechazado depende de la F2 |
| **RNF006** Respaldo diario (RPO 24 h), réplica (RPO de segundos) y RTO ≤ 2 h | F1 | HU-25: [#186](https://github.com/orlando572/erp-donofrio/pull/186)<br>HU-26: [#187](https://github.com/orlando572/erp-donofrio/pull/187) | `scripts/backup.sh`<br>`scripts/restore.sh`<br>`scripts/verificar_backup.sh`<br>`scripts/verificar_replica.sh`<br>`docker/postgres/primary`<br>`docker/postgres/replica` | — | `docs/capturas/sprint-3/HU-26_evidencia_respaldo.txt`<br>`docs/capturas/sprint-3/HU-25_evidencia_replica.txt` | Cumple (RTO medido de 31 s); la promoción de la réplica no se probó |
| **RNF007** Mantenibilidad: lint y tests en CI, sin API obsoleta | F1 | HU-02: [#154](https://github.com/orlando572/erp-donofrio/pull/154), [#159](https://github.com/orlando572/erp-donofrio/pull/159) | `.github/workflows/ci.yml`<br>`scripts/test.sh`<br>`scripts/check_legacy.sh` | `test_instalacion.py` (1) | `docs/capturas/sprint-3/S3-informe6_evidencia_tests.txt` | Cumple |
| **RNF008** El tablero carga en < 3 s; Lighthouse ≥ 80 en el login | F1 | HU-23: [#188](https://github.com/orlando572/erp-donofrio/pull/188)<br>HU-28: [#194](https://github.com/orlando572/erp-donofrio/pull/194), [#196](https://github.com/orlando572/erp-donofrio/pull/196) | `scripts/perf/lighthouse.py` | — | `docs/capturas/sprint-3/HU-28_lighthouse_resultados.csv`<br>`docs/informe/04_06_wpo.md` | Parcial: login 100 y dashboard 80; el backend queda en 59 |
| **RNF009** Seguridad: RBAC, HTTPS, gestor de BD cerrado y 2FA | F1 | HU-04: [#157](https://github.com/orlando572/erp-donofrio/pull/157)<br>HU-27: [#189](https://github.com/orlando572/erp-donofrio/pull/189)<br>HU-28: [#194](https://github.com/orlando572/erp-donofrio/pull/194), [#196](https://github.com/orlando572/erp-donofrio/pull/196) | `docker/nginx/seguridad.conf`<br>`addons/donofrio_base/data/seguridad_data.xml`<br>`scripts/verificar_despliegue.sh`<br>`scripts/perf/zap.sh` | `test_seguridad.py` (9)<br>`test_hardening.py` (12) | `docs/capturas/sprint-3/HU-27_evidencia_seguridad.txt`<br>`docs/capturas/sprint-3/HU-28_zap_reporte.html` | Cumple con límites (ZAP pasivo y sin sesión) |
| **RNF010** Auditoría de cambios en datos sensibles | F1 | HU-27: [#189](https://github.com/orlando572/erp-donofrio/pull/189) | `addons/donofrio_base/models/auditlog_rule.py`<br>`addons/donofrio_base/data/seguridad_data.xml` | `test_hardening.py::test_cambio_de_precio_queda_auditado`<br>`test_hardening.py::test_reglas_de_auditoria_confirmadas` | `docs/capturas/sprint-3/HU-27_evidencia_seguridad.txt` | Cumple para precios, pedidos y compras |
| **RNF011** Disponibilidad ≥ 99 %; reinicio automático y healthcheck | F1 | HU-01: [#153](https://github.com/orlando572/erp-donofrio/pull/153) | `docker-compose.yml` | — | `docs/capturas/sprint-1/S1_docker_compose_ps.png` | Parcial: hay healthchecks y reinicio; falta la medición (Uptime Kuma no se implementó) |
| **RNF012** Reproducibilidad: el entorno se levanta con un comando | F1 | HU-01: [#153](https://github.com/orlando572/erp-donofrio/pull/153)<br>HU-29: [#190](https://github.com/orlando572/erp-donofrio/pull/190) | `docker-compose.yml`<br>`scripts/init_db.sh`<br>`.github/workflows/release.yml`<br>`scripts/probar_imagen.sh` | — | `docs/capturas/sprint-3/HU-29_evidencia_release.txt`<br>`docs/capturas/sprint-1/HU-01_odoo_login.png` | Implementado; la imagen en GHCR se publica en el Gate 0 |
| **RNF013** Ley 29733: datos personales ficticios y mínimos | F1 | HU-03: [#155](https://github.com/orlando572/erp-donofrio/pull/155)<br>HU-05: [#160](https://github.com/orlando572/erp-donofrio/pull/160)<br>HU-16: [#175](https://github.com/orlando572/erp-donofrio/pull/175), [#180](https://github.com/orlando572/erp-donofrio/pull/180) | `addons/donofrio_base/data/clientes_data.xml`<br>`addons/donofrio_base/data/rrhh_data.xml` | `test_clientes.py` (3) | `docs/informe/05_10_a_05_12_seguridad.md` | Parcial: datos ficticios; sin política de privacidad |

## Tabla C. HU → PR (todas las HU con PR fusionado)

| HU | Qué cubre | PR |
|---|---|---|
| HU-01 | RNF011, RNF012 · Entorno Docker con Odoo 19 y PostgreSQL 16 | [#153](https://github.com/orlando572/erp-donofrio/pull/153) |
| HU-02 | RNF007 · Esqueleto de donofrio_base, `test.sh` y CI | [#154](https://github.com/orlando572/erp-donofrio/pull/154), [#159](https://github.com/orlando572/erp-donofrio/pull/159) |
| HU-03 | RF016, RNF013 | [#155](https://github.com/orlando572/erp-donofrio/pull/155) |
| HU-04 | RF018, RNF009 | [#157](https://github.com/orlando572/erp-donofrio/pull/157) |
| HU-05 | RF017, RNF013 | [#160](https://github.com/orlando572/erp-donofrio/pull/160) |
| HU-06 | RF005 | [#156](https://github.com/orlando572/erp-donofrio/pull/156) |
| HU-07 | RF009 | [#158](https://github.com/orlando572/erp-donofrio/pull/158) |
| HU-08 | RF001 | [#168](https://github.com/orlando572/erp-donofrio/pull/168), [#172](https://github.com/orlando572/erp-donofrio/pull/172) |
| HU-09 | RF002, RNF001 | [#167](https://github.com/orlando572/erp-donofrio/pull/167), [#171](https://github.com/orlando572/erp-donofrio/pull/171), [#172](https://github.com/orlando572/erp-donofrio/pull/172) |
| HU-10 | RF003, RNF001 | [#170](https://github.com/orlando572/erp-donofrio/pull/170), [#172](https://github.com/orlando572/erp-donofrio/pull/172) |
| HU-11 | RF006, RNF005 | [#169](https://github.com/orlando572/erp-donofrio/pull/169), [#176](https://github.com/orlando572/erp-donofrio/pull/176) |
| HU-12 | RF007 | [#173](https://github.com/orlando572/erp-donofrio/pull/173), [#176](https://github.com/orlando572/erp-donofrio/pull/176) |
| HU-13 | RF015 | [#179](https://github.com/orlando572/erp-donofrio/pull/179) |
| HU-14 | RF010, RNF004 | [#174](https://github.com/orlando572/erp-donofrio/pull/174), [#176](https://github.com/orlando572/erp-donofrio/pull/176) |
| HU-15 | RF016 | [#178](https://github.com/orlando572/erp-donofrio/pull/178) |
| HU-16 | RNF013 · Transacciones de demostración (script con semilla fija) | [#175](https://github.com/orlando572/erp-donofrio/pull/175), [#180](https://github.com/orlando572/erp-donofrio/pull/180) |
| HU-23 | RF013, RF014, RNF008 | [#188](https://github.com/orlando572/erp-donofrio/pull/188) |
| HU-25 | RNF006 | [#186](https://github.com/orlando572/erp-donofrio/pull/186) |
| HU-26 | RNF006 | [#187](https://github.com/orlando572/erp-donofrio/pull/187) |
| HU-27 | RNF009, RNF010 | [#189](https://github.com/orlando572/erp-donofrio/pull/189) |
| HU-28 | RNF002, RNF008, RNF009 | [#194](https://github.com/orlando572/erp-donofrio/pull/194), [#196](https://github.com/orlando572/erp-donofrio/pull/196) |
| HU-29 | RNF012 · Release: imagen GHCR y zip (se publica en el Gate 0) | [#190](https://github.com/orlando572/erp-donofrio/pull/190) |
| HU-30 | RNF003 | [#195](https://github.com/orlando572/erp-donofrio/pull/195) |
| HU-32 | Mesa de servicios TI en Project (ITIL, SLA) | [#193](https://github.com/orlando572/erp-donofrio/pull/193) |
| HU-33 | RF010, RNF004 · Pruebas integrales (pedido → factura; compra → OP → lote) | [#191](https://github.com/orlando572/erp-donofrio/pull/191), [#192](https://github.com/orlando572/erp-donofrio/pull/192) |

**HU de requisitos sin PR fusionado:** HU-17, HU-18, HU-19, HU-20, HU-21 (Fase 2: no se implementó ningún módulo propio; la HU-31 del CRM extendido era opcional y no se hizo).

## Qué no cubre esta matriz

- Los PR #172 y #176 solo agregan las capturas de HU que se implementaron en otros PR; aparecen junto a esas HU porque su título las nombra.
- Los PR de documentación (informe, Scrum, capturas) no llevan HU y no aparecen: están en el [TSV completo](../capturas/sprint-3/S3-informe6_prs_fusionados.tsv).
- La columna *Estado* es la evaluación del 23/11/2026; los criterios de aceptación de cada HU están en el Project y en los PR.
- La trazabilidad hacia las normas (ISO 27001, ITIL, COBIT) está en el anexo [10.6](anexo_10_06_soa_iso27001.md).

