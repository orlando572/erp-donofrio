# Gate 0: verificación de los criterios de salida de la Fase 1

> **Estado:** borrador de verificación de Orlando (SM) · **Para:** Evelyn (PO), que redacta sobre esta base el informe del gate (`docs/scrum/gates/gate-0-fase1.md`) · **Fuente:** [`docs/plan/04_scrum_pmbok.md` §4.3](../../plan/04_scrum_pmbok.md) («Criterios de salida de la Fase 1») y [`docs/plan/02_mapeo_plantilla.md`](../../plan/02_mapeo_plantilla.md) · **Issue:** #143 (primera casilla)
>
> **Qué es y qué no es.** Este archivo **solo verifica** cada criterio con su estado real y un enlace a su evidencia. **No es** el informe del Gate 0, **no recomienda** módulos de la Fase 2 y **no empieza ninguno**: esa decisión es del equipo, con confirmación explícita de Evelyn u Orlando en el chat ([`CLAUDE.md`](../../../CLAUDE.md)). Tampoco crea el tag `v1.0.0` ni fusiona `develop` en `main`: se hacen con confirmación aparte.
>
> **Corte de los datos:** 23/11/2026, `develop` en `6bca5c7` (PR #212; actualizado después de fusionar los PR de informe de Evelyn #207, #208, #210, #211, #212, #214 y #215). Salen de `gh` y `git` en solo lectura y de los archivos del repositorio; cada número se puede volver a medir con el comando que se indica. Los PR de Orlando que siguen **abiertos** (#209, #213 y este) se cuentan como «borrador en un PR abierto», no como parte de `develop`.
>
> **Actualización del 24/11/2026 (después del corte).** Lo que este archivo describe como pendiente en `main` ya se hizo; el resto del documento conserva el estado del corte del 23/11/2026. Estado al 24/11/2026:
>
> - **`main`:** el PR #222 fusionó la Fase 1 con *merge commit* (`4d0d94d`). El CI de `main` pasó en verde (`lint`, `test`, `replica`, `backup` y `proxy`).
> - **Tag y Release:** el tag `v1.0.0` está en `main` y existe la GitHub Release «ERP D'Onofrio v1.0.0» (publicada el 24/11/2026, 05:43 UTC).
> - **Pendiente de verificar:** que la Release lleve adjunto `erp-donofrio-v1.0.0.zip`; que la imagen exista en GHCR (el paquete respondía 404) y su visibilidad pública; las capturas pendientes de 6.4.
> - **Sin cambio:** `lint` y `test` todavía **no** son checks obligatorios en `main`. HU-30 sigue diferida.
> - **M1** (HU-17 y HU-18, #219, #220 y #221) ya está en `develop`; su tag `v1.1.0` aún no existe (ver [`gate-m1-calidad.md`](gate-m1-calidad.md)).

## Resumen: los cinco criterios

| # | Criterio de salida (04 §4.3) | Estado real | En una línea |
|---|---|---|---|
| 1 | Todas las HU de la F1 en «Hecho»; CI en verde en `main`; tag `v1.0.0` | **Parcial** | 24 de 25 HU (81 de 83 puntos) en `develop` con CI en verde; **HU-30 diferida**. **`main` no tiene ninguna HU** (84 commits detrás), **nunca corrió el CI** y **no hay tag ni release** *(24/11: `main` fusionado con el PR #222, CI verde, tag `v1.0.0` y Release publicados; ver la actualización al inicio)* |
| 2 | Video corto de la demo de punta a punta | **No cumplido: diferido** | Diferido por decisión del equipo (23/11/2026) al final, después del S4. Hay evidencia alternativa por flujo (pruebas y capturas) |
| 3 | Evidencias de réplica, respaldos, seguridad, pruebas y despliegue | **Cumple, con el SUS diferido** | Todas existen y están fechadas en `docs/capturas/sprint-3/`; faltan las pruebas de usabilidad (HU-30) y el despliegue **publicado** (release, GHCR) |
| 4 | Informe con las secciones 1 a 10 en borrador completo (F1) y los dos manuales | **Parcial** | De 49 filas de la Tabla 3: 13 completas, 34 en borrador (5 de ellas en el PR #209, abierto) y 2 que faltan (portada, historial e índices, y el PDF final: del Cierre). Manuales en borrador |
| 5 | GitHub Project al día | **Parcial** | Checklists de #133 a #140 y #142 marcadas; #141 abierta por HU-30; tarjetas de #141, #142 y #143 en «Backlog»; iteraciones en fechas planificadas |

> Nota: el reparto del criterio 4 sale de la Tabla 3 de este archivo; si Evelyn reclasifica una sección, hay que cambiar solo esa fila.

---

## Criterio 1. Historias de la Fase 1, CI y `v1.0.0`

### 1.1 Las 25 HU de la Fase 1, una por una

La Fase 1 son 25 HU y **83 puntos** (S1: 24, S2: 30, S3: 29). «Hecho» según la DoD ([`.github/pull_request_template.md`](../../../.github/pull_request_template.md)): PR aprobado por el otro integrante, CI en verde y fusionado en `develop`. Todos los PR de esta tabla están **fusionados** (`gh pr list --state merged`), con base `develop` y con la aprobación del otro integrante. Evidencia de cada una en `docs/capturas/sprint-N/` y en [`trazabilidad.md`](../../informe/trazabilidad.md).

**Tabla 1. HU de la Fase 1 con su PR y su estado**

| HU | Historia | Pts | Dueño | Sprint | PR | Evidencia | Estado |
|---|---|---|---|---|---|---|---|
| HU-01 | Entorno Docker con Odoo 19 y PostgreSQL 16 | 3 | O | S1 | [#153](https://github.com/orlando572/erp-donofrio/pull/153) | [`HU-01_odoo_login.png`](../../capturas/sprint-1/HU-01_odoo_login.png), [`S1_docker_compose_ps.png`](../../capturas/sprint-1/S1_docker_compose_ps.png) | Hecho |
| HU-02 | CI: instala los módulos y corre los tests en cada PR | 5 | O | S1 | [#154](https://github.com/orlando572/erp-donofrio/pull/154), [#159](https://github.com/orlando572/erp-donofrio/pull/159) | [`ci.yml`](../../../.github/workflows/ci.yml); corridas en Actions | Hecho |
| HU-03 | Compañía con localización peruana | 3 | O | S1 | [#155](https://github.com/orlando572/erp-donofrio/pull/155) | [`HU-03_compania.png`](../../capturas/sprint-1/HU-03_compania.png) | Hecho |
| HU-04 | Usuarios por rol con permisos mínimos | 3 | O | S1 | [#157](https://github.com/orlando572/erp-donofrio/pull/157) | [`HU-04_usuarios.png`](../../capturas/sprint-1/HU-04_usuarios.png) | Hecho |
| HU-05 | Organigrama, puestos y empleados | 2 | E | S1 | [#160](https://github.com/orlando572/erp-donofrio/pull/160) | [`HU-05_organigrama_empleados.png`](../../capturas/sprint-1/HU-05_organigrama_empleados.png) | Hecho |
| HU-06 | Almacenes de Lima y Arequipa con ubicaciones de frío | 3 | O | S1 | [#156](https://github.com/orlando572/erp-donofrio/pull/156) | [`HU-06_almacenes.png`](../../capturas/sprint-1/HU-06_almacenes.png) | Hecho |
| HU-07 | Productos, insumos y recetas cargados | 5 | O | S1 | [#158](https://github.com/orlando572/erp-donofrio/pull/158) | [`HU-07_recetas.png`](../../capturas/sprint-1/HU-07_recetas.png) | Hecho |
| HU-08 | Embudo CRM por canal | 2 | E | S2 | [#168](https://github.com/orlando572/erp-donofrio/pull/168), [#172](https://github.com/orlando572/erp-donofrio/pull/172) | [`HU-08_embudo_kanban.png`](../../capturas/sprint-2/HU-08_embudo_kanban.png) | Hecho |
| HU-09 | Listas de precios por canal y temporada | 3 | E | S2 | [#167](https://github.com/orlando572/erp-donofrio/pull/167), [#171](https://github.com/orlando572/erp-donofrio/pull/171), [#172](https://github.com/orlando572/erp-donofrio/pull/172) | [`HU-09_listas_de_precios.png`](../../capturas/sprint-2/HU-09_listas_de_precios.png) | Hecho |
| HU-10 | Punto de venta con boleta | 3 | E | S2 | [#170](https://github.com/orlando572/erp-donofrio/pull/170), [#172](https://github.com/orlando572/erp-donofrio/pull/172) | [`HU-10_pdv_pago_boleta.png`](../../capturas/sprint-2/HU-10_pdv_pago_boleta.png) | Hecho |
| HU-11 | Lotes con vencimiento y salida FEFO | 5 | O | S2 | [#169](https://github.com/orlando572/erp-donofrio/pull/169), [#176](https://github.com/orlando572/erp-donofrio/pull/176) | [`HU-11_lote_por_vencer.png`](../../capturas/sprint-2/HU-11_lote_por_vencer.png), `test_fefo.py` | Hecho |
| HU-12 | Recibir insumos y despachar en 2 pasos | 3 | O | S2 | [#173](https://github.com/orlando572/erp-donofrio/pull/173), [#176](https://github.com/orlando572/erp-donofrio/pull/176) | [`HU-12_pick_lima_reposicion_aqp.png`](../../capturas/sprint-2/HU-12_pick_lima_reposicion_aqp.png) | Hecho |
| HU-13 | Reabastecimiento mín./máx. de insumos | 3 | E | S2 | [#179](https://github.com/orlando572/erp-donofrio/pull/179) | [`HU-13_rfq_generadas_por_el_planificador.png`](../../capturas/sprint-2/HU-13_rfq_generadas_por_el_planificador.png) | Hecho |
| HU-14 | OP que consume insumos y genera un lote | 3 | O | S2 | [#174](https://github.com/orlando572/erp-donofrio/pull/174), [#176](https://github.com/orlando572/erp-donofrio/pull/176) | [`HU-14_op_terminada_con_lote.png`](../../capturas/sprint-2/HU-14_op_terminada_con_lote.png) | Hecho |
| HU-15 | Factura y boleta con IGV desde el pedido | 3 | E | S2 | [#178](https://github.com/orlando572/erp-donofrio/pull/178) | [`HU-15_boleta_03_con_igv.png`](../../capturas/sprint-2/HU-15_boleta_03_con_igv.png) | Hecho |
| HU-16 | Transacciones de demostración por script (semilla fija) | 5 | O+E | S2 | [#175](https://github.com/orlando572/erp-donofrio/pull/175), [#180](https://github.com/orlando572/erp-donofrio/pull/180) | [`HU-16_ventas_por_canal_y_mes.png`](../../capturas/sprint-2/HU-16_ventas_por_canal_y_mes.png) | Hecho |
| HU-23 | Tablero mínimo con lo estándar (dashboards y vistas guardadas) | 3 | E | S3 | [#188](https://github.com/orlando572/erp-donofrio/pull/188) | [`HU-23_dashboard_ventas.png`](../../capturas/sprint-3/HU-23_dashboard_ventas.png) y 4 más | Hecho |
| HU-25 | Réplica en caliente de PostgreSQL | 3 | O | S3 | [#186](https://github.com/orlando572/erp-donofrio/pull/186) | [`HU-25_evidencia_replica.txt`](../../capturas/sprint-3/HU-25_evidencia_replica.txt) | Hecho |
| HU-26 | Respaldos diarios y restauración probada | 3 | O | S3 | [#187](https://github.com/orlando572/erp-donofrio/pull/187) | [`HU-26_evidencia_respaldo.txt`](../../capturas/sprint-3/HU-26_evidencia_respaldo.txt) | Hecho |
| HU-27 | Despliegue protegido (TLS, producción, 2FA, contraseñas, bloqueo, auditoría) | 5 | O | S3 | [#189](https://github.com/orlando572/erp-donofrio/pull/189) | [`HU-27_evidencia_seguridad.txt`](../../capturas/sprint-3/HU-27_evidencia_seguridad.txt) | Hecho |
| HU-28 | Pruebas de carga (k6), seguridad (ZAP) y WPO (Lighthouse) | 5 | O+E | S3 | [#196](https://github.com/orlando572/erp-donofrio/pull/196) (k6 y ZAP), [#194](https://github.com/orlando572/erp-donofrio/pull/194) (Lighthouse) | [`HU-28_evidencia_k6_zap.txt`](../../capturas/sprint-3/HU-28_evidencia_k6_zap.txt), [`HU-28_lighthouse_resultados.csv`](../../capturas/sprint-3/HU-28_lighthouse_resultados.csv) | Hecho (backend en 59 de 80: limitación declarada) |
| HU-29 | Release automática (imagen en GHCR y zip) | 3 | O | S3 | [#190](https://github.com/orlando572/erp-donofrio/pull/190) | [`HU-29_evidencia_release.txt`](../../capturas/sprint-3/HU-29_evidencia_release.txt) | Hecho (el flujo está probado en ensayo; se publica con el tag) |
| **HU-30** | **Usabilidad con 5 personas y SUS** | 2 | E | S3 | [#195](https://github.com/orlando572/erp-donofrio/pull/195) (solo plan, cuestionario y script) | [`docs/usabilidad/`](../../usabilidad/plan_de_pruebas.md), [6.12](../../informe/06_12_usabilidad.md) | **Diferida por decisión del equipo (23/11/2026)** al final, después del S4 |
| HU-32 | Mesa de servicios en Project con tipos de ticket ITIL y SLA | 2 | E | S3 | [#193](https://github.com/orlando572/erp-donofrio/pull/193) | [`HU-32_mesa_servicios_kanban.png`](../../capturas/sprint-3/HU-32_mesa_servicios_kanban.png) | Hecho |
| HU-33 | Pruebas de integración de los flujos estándar | 3 | O+E | S3 | [#192](https://github.com/orlando572/erp-donofrio/pull/192) (compra y OP), [#191](https://github.com/orlando572/erp-donofrio/pull/191) (venta) | `test_flujo_compra_produccion.py`, `test_flujo_venta.py` | Hecho |

**Resultado:** **24 de 25 HU** en «Hecho» y **81 de 83 puntos**. La que falta es HU-30, **diferida por decisión del equipo** (ver «Desviaciones aceptadas»). Comprobación: `gh pr list --state merged --search "HU-" --limit 100`. Ninguna HU de la F1 tiene un PR abierto ni una rama sin fusionar.

### 1.2 CI en `develop`

| Qué | Dato | Cómo se comprobó |
|---|---|---|
| Última corrida de `develop` (23/11/2026, 23:45 UTC, `5e1fcb2`) | **Correcta**: [`45291533593`](https://github.com/orlando572/erp-donofrio/actions/runs/45291533593) con los cinco jobs `lint`, `test`, `replica`, `backup` y `proxy` en `success` | `gh run view 45291533593 --json jobs` |
| Historial de `develop` por *push* | 53 corridas: **44 correctas, 9 canceladas** (las reemplazó una corrida más nueva del mismo grupo de concurrencia) y **0 en rojo** | `gh run list --limit 400` |
| Todo el CI del repositorio | 137 corridas: 117 correctas, 13 canceladas, 2 en rojo (los dos intentos del PR #189, corregidos en el mismo PR) y 4 en curso al cortar. La corrida programada semanal: 1, correcta (`45279340817`) | ídem |
| Pruebas | 136 pruebas de `donofrio_base` sin errores (`scripts/test.sh`); `scripts/check_legacy.sh`: «sin patrones legacy» (corrido hoy) | [`S3-informe6_evidencia_tests.txt`](../../capturas/sprint-3/S3-informe6_evidencia_tests.txt) |
| Los 7 PR de Evelyn (#207, #208, #210, #211, #212, #214 y #215) | **Fusionados** en `develop` el 23/11/2026 con *squash* y aprobación de Orlando; antes de fusionar: sus checks `lint`, `backup`, `proxy` y `replica` pasan; `test` pasa en los que ya terminaron | `gh pr checks <n>` |

### 1.3 `main` y el tag `v1.0.0`

| Qué | Estado real | Dato |
|---|---|---|
| `main` frente a `develop` | **84 commits detrás, 0 por delante** | `git rev-list --count origin/main..origin/develop` |
| Contenido de `main` | Solo el commit inicial del Sprint 0 (`284e9bf`): **no tiene ninguna de las HU** ni los workflows | `git log --oneline origin/main` |
| Conflictos al fusionar `develop` en `main` | **Ninguno**: la fusión es limpia | `git merge-tree --write-tree origin/main origin/develop` |
| CI en `main` | **Nunca corrió** (0 corridas en la rama `main`); el criterio «CI en verde en `main`» solo se cumple después de fusionar | `gh run list --branch main` |
| Protección de `main` | 1 aprobación, conversaciones resueltas, sin *force push* ni borrado; **sin checks obligatorios**; no aplica a administradores | `gh api …/branches/main/protection` |
| Tag `v1.0.0` | **No existe** (0 tags) | `gh api repos/orlando572/erp-donofrio/tags` |
| GitHub Releases | **Ninguna** | `gh release list` |
| Imagen en GHCR (`ghcr.io/orlando572/erp-donofrio`) | **No existe** (la página responde 404) | `gh api users/orlando572/packages/container/erp-donofrio` |

> **Actualización del 24/11/2026.** La tabla de arriba es la del corte del 23/11. Hoy: `main` contiene la Fase 1 (PR #222, *merge commit* `4d0d94d`) y su CI pasó en verde; el tag `v1.0.0` existe en `main`; la GitHub Release «ERP D'Onofrio v1.0.0» está publicada (24/11/2026, 05:43 UTC). **Pendiente de verificar:** el zip adjunto, la imagen en GHCR (el paquete daba 404) y su visibilidad pública. `lint` y `test` aún no son checks obligatorios en `main`. Los pasos 3 a 6 de abajo se cumplieron; el paso 7 sigue abierto.

**Qué falta para crear `v1.0.0`** (según [`docs/dev/release.md`](../../dev/release.md) y la protección de `main`). **Nada de esto se hizo aquí** y se ejecuta **con confirmación aparte** de Evelyn u Orlando en el chat:

1. Fusionar en `develop` los PR de Orlando que quedan abiertos (#209, #213 y #216, que necesitan la aprobación de Evelyn); así el zip lleva el informe al día.
2. Que Evelyn termine `gate-0-fase1.md` y el equipo tome la decisión del gate (comentario en #143).
3. Abrir el PR **`develop` → `main`** con la plantilla de PR, la aprobación del otro integrante y las conversaciones resueltas, y fusionarlo con **merge commit** (no *squash*). El repositorio lo permite (`allow_merge_commit = true`).
4. Esperar el CI de `main` (se dispara con el *push*) y comprobar que los cinco jobs pasen. Después, poner `lint` y `test` como checks obligatorios en `main` (6.4 lo deja anotado).
5. Desde `main` actualizado: `git tag -a v1.0.0 -m "Núcleo v1.0.0 (Fase 1)"` y `git push origin v1.0.0`.
6. Mirar la corrida **Release**: construye y prueba la imagen, arma el zip y, **solo con tag**, publica en GHCR y crea la Release con `erp-donofrio-v1.0.0.zip`. Ensayo previo: PR #190, 2 min 59 s, imagen de 3.25 GB y zip de 17 MB sin `.env`.
7. Comprobar la Release (zip adjunto), el paquete (Packages) y poner el paquete en **visibilidad pública**; tomar las capturas pendientes de 6.4 y quitar de 5.15 y 6.4 los «aún no existe».

---

## Criterio 2. Video de la demo

**Estado: no cumplido, diferido por decisión del equipo (23/11/2026) al final, después del Sprint 4.** No hay video. Para que el informe del gate tenga qué mostrar mientras tanto, cada flujo del criterio tiene una **evidencia alternativa verificable** (no sustituye al video):

| Flujo que debe mostrar el video | Evidencia alternativa que existe | Archivos |
|---|---|---|
| CRM → pedido → entrega FEFO → factura o boleta | Prueba de integración pedido → entrega FEFO por lote → factura o boleta con IGV (4 pruebas, HU-33) y capturas de los pasos | `test_flujo_venta.py`; [`HU-08_embudo_kanban.png`](../../capturas/sprint-2/HU-08_embudo_kanban.png), [`HU-15_boleta_03_con_igv.png`](../../capturas/sprint-2/HU-15_boleta_03_con_igv.png) |
| Punto de venta | Capturas de la sesión de PdV, pago con boleta y cierre de caja cuadrado; 6 pruebas | `test_pdv.py`; [`HU-10_pdv_cierre_de_caja_cuadrado.png`](../../capturas/sprint-2/HU-10_pdv_cierre_de_caja_cuadrado.png) |
| Compra → recepción | Prueba compra → recepción → OP → lote (4 pruebas, HU-33) y capturas del planificador y la recepción | `test_flujo_compra_produccion.py`; [`HU-13_recepcion_creada_por_la_oc.png`](../../capturas/sprint-2/HU-13_recepcion_creada_por_la_oc.png) |
| OP → lote | Captura de la OP terminada con lote y la prueba que valida el lote con vencimiento | [`HU-14_op_terminada_con_lote.png`](../../capturas/sprint-2/HU-14_op_terminada_con_lote.png); `test_produccion.py` |
| Dashboards | Cinco capturas de HU-23 (dashboards y vistas guardadas) | [`HU-23_dashboard_ventas.png`](../../capturas/sprint-3/HU-23_dashboard_ventas.png), [`HU-23_vista_ventas_linea_canal_mes.png`](../../capturas/sprint-3/HU-23_vista_ventas_linea_canal_mes.png) |

El guion de la demo cruzada, que también quedó diferida, está en [`docs/scrum/sprint-2/demo_cruzada.md`](../sprint-2/demo_cruzada.md).

---

## Criterio 3. Evidencias de infraestructura, seguridad, pruebas y despliegue

**Tabla 2. Evidencias y su estado** (todas en `develop`, fechadas el 23/11/2026)

| Evidencia | Resultado medido | Archivo de la evidencia | Documento del informe | Estado |
|---|---|---|---|---|
| **Réplica** de PostgreSQL | `pg_stat_replication` en `streaming` (asíncrona), retraso de 2.3 ms, `pg_is_in_recovery()` = `t`; la escritura en la réplica falla; el rol de Odoo no replica ni es superusuario; job `replica` del CI | [`HU-25_evidencia_replica.txt`](../../capturas/sprint-3/HU-25_evidencia_replica.txt) | [5.9](../../informe/05_07_a_05_09_arquitectura_bd.md) | **Cumple** (promoción de la réplica no probada) |
| **Respaldos** | `backup.sh` (dump, *filestore* y SHA-256) y `restore.sh` en una base nueva: **RTO 31 s** frente a 2 h; un respaldo alterado se rechaza; retención de 7 días; job `backup` del CI | [`HU-26_evidencia_respaldo.txt`](../../capturas/sprint-3/HU-26_evidencia_respaldo.txt) | [5.9b](../../informe/05_07_a_05_09_arquitectura_bd.md), [5.14 Tabla 24 d](../../informe/05_13_a_05_14_pruebas.md) | **Cumple** (el *cron* diario no está instalado) |
| **Seguridad: roles** | 10 usuarios por rol sin administradores, regla del CD Arequipa (`AccessError`); 9 pruebas | `test_seguridad.py`; [`HU-04_usuarios.png`](../../capturas/sprint-1/HU-04_usuarios.png) | [5.11 C-01](../../informe/05_10_a_05_12_seguridad.md) | **Cumple** |
| **Seguridad: 2FA, contraseñas, TLS** | 2FA del administrador y el gerente (`/web/login/totp`), contraseñas de 12 o más, bloqueo tras 5 intentos, TLS 1.2 y 1.3 (1.1 rechazado), HSTS y cabeceras, `list_db = False`; `verificar_despliegue.sh` (job `proxy`); 12 pruebas de endurecimiento | [`HU-27_evidencia_seguridad.txt`](../../capturas/sprint-3/HU-27_evidencia_seguridad.txt) | [5.11 C-02 a C-09](../../informe/05_10_a_05_12_seguridad.md) | **Cumple** (certificado autofirmado; 2FA solo con `proxy_mode`) |
| **Pruebas unitarias** | 136 pruebas `TransactionCase` de `donofrio_base`, sin errores, en el CI de cada PR | [`S3-informe6_evidencia_tests.txt`](../../capturas/sprint-3/S3-informe6_evidencia_tests.txt) | [6.10](../../informe/06_09_a_06_13_pruebas.md) | **Cumple** |
| **Pruebas integrales** | 8 pruebas de HU-33 (venta y compra → producción) y los jobs `replica`, `backup` y `proxy` | `test_flujo_venta.py`, `test_flujo_compra_produccion.py` | [6.11](../../informe/06_09_a_06_13_pruebas.md) | **Cumple** |
| **Carga (k6)** | 20 usuarios virtuales: p95 de 11.6 ms en listas y 9.1 ms en formularios frente al límite de 2 s; 0 % de errores; esfuerzo: unos 100 ms | [`HU-28_evidencia_k6_zap.txt`](../../capturas/sprint-3/HU-28_evidencia_k6_zap.txt), [`HU-28_k6_resumen.json`](../../capturas/sprint-3/HU-28_k6_resumen.json), [`HU-28_k6_esfuerzo_resumen.json`](../../capturas/sprint-3/HU-28_k6_esfuerzo_resumen.json) | [5.14 Tabla 22](../../informe/05_13_a_05_14_pruebas.md) | **Cumple** (RNF002) |
| **Seguridad (ZAP baseline)** | 0 alertas altas (4 medias y 3 bajas aceptadas con su motivo); pasivo y sin sesión | [`HU-28_zap_reporte.html`](../../capturas/sprint-3/HU-28_zap_reporte.html), [`.json`](../../capturas/sprint-3/HU-28_zap_reporte.json) | [5.14 Tabla 24 a](../../informe/05_13_a_05_14_pruebas.md) | **Cumple con límites** (RNF009) |
| **WPO (Lighthouse)** | Login 98 → 100; dashboard 45 → 80 (LCP 1.9 s); backend 35 → **59** (meta 80, no cumplida) | [`HU-28_lighthouse_resultados.csv`](../../capturas/sprint-3/HU-28_lighthouse_resultados.csv) | [4.6.4](../../informe/04_06_wpo.md) | **Parcial** (RNF008) |
| **SUS (usabilidad)** | Plan, cuestionario y script de cálculo listos; **no medido** | [`docs/usabilidad/`](../../usabilidad/plan_de_pruebas.md) | [6.12](../../informe/06_12_usabilidad.md) | **Diferido** (HU-30) |
| **Despliegue** | Despliegue protegido local (`scripts/levantar_prod.sh`, `https://localhost:8443`) verificado; imagen de release y zip probados en **ensayo**; **sin release ni GHCR publicados**; sin VM en la nube | [`HU-27_evidencia_seguridad.txt`](../../capturas/sprint-3/HU-27_evidencia_seguridad.txt), [`HU-29_evidencia_release.txt`](../../capturas/sprint-3/HU-29_evidencia_release.txt) | [5.15](../../informe/05_15_despliegue.md), [6.4](../../informe/06_04_a_06_06_repositorio.md) | **Cumple en local; sin publicar** |
| **Mesa de servicios (ITIL)** | Proyecto «Mesa de Servicios TI» con 5 etapas, 3 tipos de ticket y SLA por prioridad (HU-32) | [`HU-32_mesa_servicios_kanban.png`](../../capturas/sprint-3/HU-32_mesa_servicios_kanban.png), [`HU-32_pivote_cumplimiento_sla.png`](../../capturas/sprint-3/HU-32_pivote_cumplimiento_sla.png) | [4.7](../../informe/04_07_acuerdos_de_nivel_de_servicio.md) | **Cumple** |

Resumen de los 13 RNF al cierre del S3 (de [4.2.3](../../informe/04_02_requerimientos_no_funcionales.md) en el PR #209, aún abierto): 6 *Cumple*, 1 *Cumple con límites*, 5 *Parcial* y 1 *Pendiente*. Los que **no están medidos**: RNF001 (tres navegadores y móvil), RNF011 (disponibilidad en el tiempo) y RNF003 (SUS, diferido). Fichas en el anexo 10.2 del mismo PR.

---

## Criterio 4. Informe con todas las secciones 1 a 10 en borrador completo (F1) y los dos manuales

**Cómo se clasifica** (la plantilla fija la numeración en [02 §2.2](../../plan/02_mapeo_plantilla.md); el criterio de «sección completa» es el de su final):

- **Completa:** contenido de la Fase 1 terminado, fusionado en `develop` y aprobado por el otro integrante, sin marcas «[cita]» ni «Pendiente» propias. Siempre falta lo común del Cierre: maquetación en Word, índices y la cita APA 7 de la sección 9.
- **Borrador:** hay contenido real de la F1, pero con pendientes propios (marcas, capturas, partes del otro integrante o de la F2) **o** está en un PR abierto.
- **Falta:** no hay archivo en `develop` ni en un PR abierto.

**Tabla 3. Estado de cada sección** (según `develop` en `6bca5c7` y el PR abierto #209)

| Sección | Archivo | Dueño | Estado | Observación |
|---|---|---|---|---|
| Portada, historial de revisiones e índices | Word (no hay archivo) | E | **Falta** | Se hacen en Word en el Cierre |
| 1. Resumen | `01_resumen.md` | E | Borrador | PR #205 fusionado |
| 2. Abstract | `02_abstract.md` | O | Borrador | Revisar contra el Resumen de Evelyn |
| 3.1 a 3.7 Aspectos generales | `03_aspectos_generales.md` | E | Borrador | Marcas «[cita]» resueltas en #212 (fusionado) |
| 4.1.1 Análisis de sistemas | `04_01_analisis_sistemas.md` | E | Borrador | Los puntos de la F2 «Pendiente: M1/M2/M3» dependen del Gate 0 |
| 4.1.2 BPMN AS-IS y TO-BE | `04_01_analisis_sistemas.md`, `docs/diagramas/bpmn/` | E+O | Borrador | 5 AS-IS y 7 TO-BE hechos |
| 4.1.3 Arquitectura empresarial | `04_01_arquitectura_empresarial.md` | O | Borrador | Marca «[cita]» resuelta en #212 (fusionado) |
| 4.1.4 Oportunidades de innovación | `04_01_04_oportunidades_innovacion.md` | E | Borrador (fusionado en [#207](https://github.com/orlando572/erp-donofrio/pull/207)) | |
| 4.2.1 y 4.2.2 Gestión de RF | `04_02_requerimientos_funcionales.md` | E | Borrador | Estados de RF del cierre del S1 |
| 4.2.3 RNF | `04_02_requerimientos_no_funcionales.md` | O | Borrador (PR [#209](https://github.com/orlando572/erp-donofrio/pull/209) abierto) | En `develop` sigue el estado del S1; #209 lo pone al día (el conflicto con #212 ya está resuelto en la rama de #209) |
| 4.2.4 Casos de uso | `04_02_casos_de_uso.md` | E+O | Borrador | |
| 4.2.5 a 4.2.8 Clases, ER, lógico y diccionario | `04_02_modelo_de_datos.md`, `04_02_diccionario_datos.md` | O | **Completa** | PR #197 |
| 4.2.9 Calendarización | `04_02_calendarizacion.md` | E | Borrador | Falta la captura del Roadmap como ilustración 6 |
| 4.2.10 a 4.2.12 Roles, artefactos y eventos | `04_02_10_a_12_scrum.md` | E | Borrador (fusionado en [#208](https://github.com/orlando572/erp-donofrio/pull/208)) | |
| 4.3.1 a 4.3.3 y 4.3.7 | `04_03_infraestructura.md` | O | **Completa** | PR #198 y anteriores |
| 4.3.4 IDEs y lenguajes; 4.3.9 gestión de proyectos | `04_03_04_ides_y_gestion_proyectos.md` | E | Borrador (fusionado en [#210](https://github.com/orlando572/erp-donofrio/pull/210)) | |
| 4.3.5 Librerías y dependencias | `05_01_a_05_06_backend.md` (5.2 a 5.4) | O | **Completa** | |
| 4.3.6 Controles de versionamiento y 4.3.8 Plataformas cloud | `04_03_infraestructura.md` | O | Borrador (PR #209 abierto) | |
| 4.4.1 y 4.4.2 Wireframes y mockups | `04_04_prototipos.md` | E | Borrador | Pendiente: reemplazar mockups por pantallas reales |
| 4.5.1 Plan de gestión de riesgos | `docs/pm/plan_riesgos.md` | E | Borrador | Redactado por Orlando en el S0; Evelyn debe revisarlo |
| 4.5.2 Riesgos de desarrollo | `04_05_02_riesgos_desarrollo.md` | E | Borrador (fusionado en [#211](https://github.com/orlando572/erp-donofrio/pull/211)) | |
| 4.5.3 y 4.5.4 Riesgos de despliegue y mantenimiento | `04_05_riesgos_despliegue_y_mantenimiento.md` | O | Borrador (PR #209 abierto) | Con niveles propuestos para validar |
| 4.6.1 a 4.6.3 Buenas prácticas, prototipos web y reportes | `04_06_prototipos_web_y_reportes.md` | E | Borrador | Pendiente: tres navegadores y móvil (RNF001) |
| 4.6.4 WPO | `04_06_wpo.md` | E | **Completa** | Backend en 59 declarado como limitación |
| 4.7 Métricas, KPI y SLA | `04_07_acuerdos_de_nivel_de_servicio.md` | E | Borrador | SUS «Pendiente» (HU-30 diferida) |
| 5.1 a 5.6 Backend, paquetes, patrones | `05_01_a_05_06_backend.md` | O | **Completa** | |
| 5.7 a 5.9b Arquitectura, BD y réplica | `05_07_a_05_09_arquitectura_bd.md` | O | **Completa** | `pg_stat_statements` declarado no activado |
| 5.10 a 5.12 Seguridad: riesgos, controles y ataques | `05_10_a_05_12_seguridad.md` | O | **Completa** | |
| 5.13 Pruebas funcionales | `05_13_a_05_14_pruebas.md` | E+O | Borrador | Falta el espacio reservado de Evelyn (ventas, heladeros y gerencia) |
| 5.14 Pruebas no funcionales | `05_13_a_05_14_pruebas.md` | O+E | Borrador | La Tabla 23 de Evelyn remite a 4.6.4 y 6.12; usabilidad sin medir |
| 5.15 Despliegue | `05_15_despliegue.md` | O | Borrador | Release y GHCR sin publicar |
| 5.16 Gestión de servicios (ITIL) | `05_15_despliegue.md` (5.15.6) | O | Borrador | Falta consultar al docente si espera estas secciones; sin BPMN |
| 6.1 a 6.3 Equipo, sprints y Project | `06_01_a_06_03_equipo_sprints_y_project.md` | E | Borrador | Iteraciones en fechas planificadas |
| 6.4 a 6.6 GitHub, ramas y fusión | `06_04_a_06_06_repositorio.md` | O | Borrador | Capturas pendientes hasta que exista la release; cifras con fecha |
| 6.7 y 6.8 Commits e issues | `06_07_a_06_08_commits_e_issues.md` | E | **Completa** | Se vuelven a medir con `scripts/estadisticas_repo.py` al final |
| 6.9 a 6.11 Pruebas: resumen, unitarias e integrales | `06_09_a_06_13_pruebas.md` | O | **Completa** | |
| 6.12 Pruebas de usabilidad | `06_12_usabilidad.md` | E | Borrador | Sin las 5 personas: diferido |
| 6.13 Pruebas de seguridad | `06_09_a_06_13_pruebas.md` | O | **Completa** | |
| 7. Conclusiones | `07_conclusiones.md` | E+O | Borrador | Provisional: se reescribe tras el Gate 0 y HU-30 |
| 8.1 Recomendaciones de negocio | `08_01_recomendaciones_negocio.md` | E | Borrador (fusionado en [#215](https://github.com/orlando572/erp-donofrio/pull/215)) | Va en un archivo aparte del de 8.2 |
| 8.2 Recomendaciones técnicas | `08_recomendaciones.md` | O | Borrador (PR #209 abierto) | La 8.1 de Evelyn está aparte, en `08_01_recomendaciones_negocio.md` (#215, fusionado) |
| 9. Referencias (APA 7) | `09_referencias.md` | E | Borrador (fusionado en [#212](https://github.com/orlando572/erp-donofrio/pull/212)) | No existe en `develop` |
| 10.1 Fichas de RF | `anexo_10_01_fichas_rf.md` | E | Borrador (fusionado en [#214](https://github.com/orlando572/erp-donofrio/pull/214)) | |
| 10.2 Fichas de RNF | `anexo_10_02_fichas_rnf.md` | O | Borrador (PR #209 abierto) | |
| 10.3 Solicitud de servicio y 10.5 Incidente | `anexo_10_03_solicitud_servicio.md`, `anexo_10_05_incidente.md` | E | Borrador | PR #203 |
| 10.4 RFC | `anexo_10_04_rfc.md` | O | **Completa** | PR #200 |
| 10.6 SoA ISO 27001 y política | `anexo_10_06_soa_iso27001.md` | O | **Completa** | PR #200 |
| Trazabilidad requisito → HU → PR → prueba (anexo extra) | `trazabilidad.md` | O | **Completa** | Generada con `scripts/trazabilidad.py` |
| Informe final en PDF | — | E | **Falta** | Maquetación en Word en el Cierre |

**Los dos manuales** (entregables b y c del lineamiento): [`manual_instalacion.md`](../../manuales/manual_instalacion.md) y [`manual_herramientas.md`](../../manuales/manual_herramientas.md), ambos de Orlando, en **borrador** (PR #202, fusionado); se completan con capturas y se exportan a PDF en el Cierre. El criterio pide «en borrador»: **cumple**.

**Resultado:** el informe tiene **contenido de la Fase 1 en todas las secciones 1 a 10** en `develop`, salvo las de Orlando que están en el PR #209 (4.2.3 actualizada, 4.3.6 y 4.3.8, 4.5.3 y 4.5.4, 8.2 y 10.2), que **siguen abiertas**. Con #209 fusionado, el criterio **se cumple como borrador**, salvo portada, historial, índices y el PDF, que son del Cierre.

---

## Criterio 5. GitHub Project y checklists de las épicas

El Project «Scrum ERP D'Onofrio» (<https://github.com/users/orlando572/projects/4>, público) tiene **22 ítems**: 10 en «Hecho», 2 en «En curso» y 10 en «Backlog». Comprobación: `gh project item-list 4 --owner orlando572 --format json`.

**Tabla 4. Épicas y gestión (23/11/2026)**

| Issue | Título | Sprint | Resp. | Issue | Casillas marcadas | Tarjeta | Estado |
|---|---|---|---|---|---|---|---|
| #129 | Constitución del proyecto y GitHub Project | S0 | E | Cerrado | 11 de 11 | Hecho | Al día |
| #130 | Repo, ramas, plantillas y agente de IA | S0 | O | Cerrado | 6 de 6 | Hecho | Al día |
| #131 | Registro de riesgos | S0 | E | **Abierto** | 2 de 28 | En curso | **Pendiente (Evelyn)**: se cierra al terminar el sprint, con el comentario de seguimiento de la Retro del S3 |
| #132 | Dailies | S0 | O | **Abierto** | sin casillas | En curso | Se cierra cuando la Daily de Orlando esté fusionada (PR #213) |
| #133 | [HU-01, HU-02] Entorno Docker y CI | S1 | O | Cerrado | 8 de 8 | Hecho | Al día |
| #134 | [HU-03, HU-04, HU-06, HU-07] Datos maestros, compañía y seguridad | S1 | O | Cerrado | 14 de 14 | Hecho | Al día |
| #135 | [HU-05] RR. HH. | S1 | E | Cerrado | 4 de 4 | Hecho | Al día |
| #136 | [HU-08, HU-09, HU-10] Ventas, CRM y PdV | S2 | E | Cerrado | 9 de 9 | Hecho | Al día |
| #137 | [HU-13, HU-15] Compras y facturación | S2 | E | Cerrado | 8 de 8 | Hecho | Al día |
| #138 | [HU-11, HU-12, HU-14] Inventario y producción | S2 | O | Cerrado | 12 de 12 | Hecho | Al día |
| #139 | [HU-16] Transacciones de demostración | S2 | O | Cerrado | 3 de 3 | Hecho | Al día |
| #140 | [HU-25, HU-26, HU-27, HU-29] Infraestructura, réplica y seguridad | S3 | O | Cerrado | 16 de 17 | **Hecho** (movida por Orlando el 23/11) | Al día: la casilla sin marcar es «`v1.0.0` = núcleo» (se crea en el Gate 0) |
| #141 | [HU-23, HU-30, HU-32] Gerencia, KPIs y mesa de servicios ITIL | S3 | E | **Abierto** | 10 de 12 | Backlog | Abierta por HU-30 (diferida); falta mover la tarjeta |
| #142 | [HU-28, HU-33] Pruebas y calidad del software | S3 | O+E | Cerrado | 7 de 7 | **Backlog** | **Desfasado:** el issue está cerrado y la tarjeta en «Backlog» |
| #143 | Gate 0 | S3 | E | **Abierto** | 0 de 3 | Backlog | Pendiente: esta verificación cubre la primera casilla |
| #144 a #148 | Módulos M1 a M4 y opcionales (Fase 2) | S4 | E+O | Abiertos | 0 | Backlog | **Sin empezar**, a la espera de la decisión del Gate 0 |
| #149 | Informe final | Cierre | E | Abierto | 0 de 45 | Backlog | La checklist no se ha marcado; la Tabla 3 de este archivo es el estado real |
| #150 | Entrega | Cierre | O | Abierto | 0 de 8 | Backlog | Del Cierre |

**Lo que sigue desactualizado en el Project:** (1) las tarjetas de #141, #142 y #143 siguen en «Backlog»; (2) las **iteraciones están en las fechas planificadas** (S1 el 23/11, S2 el 24/11, S3 el 25/11, S4 el 26/11, Cierre el 27/11) y no en las reales, así que «Sprint actual» sigue mostrando el S1; (3) el *workflow* «Item closed» está desactivado, por eso las tarjetas no pasan solas a «Hecho»; (4) el acceso de Evelyn al Project es de solo lectura, así que mover tarjetas y activar el *workflow* tiene que hacerlo Orlando (el dueño) o dárselo a ella. Orlando solo movió la de #140.

---

## Desviaciones aceptadas

Decisión del equipo del **23/11/2026** (en el chat, antes de la verificación): quedan para el final, **después del Sprint 4**, y no son un incumplimiento oculto ni cambian el plazo del Cierre.

| Desviación | Criterio que toca | Qué queda en su lugar | Quién lo hace |
|---|---|---|---|
| **Video de la demo** | 2 | Evidencia alternativa por flujo (Criterio 2); el video de respaldo (2 a 3 min por persona) | Evelyn y Orlando |
| **HU-30: usabilidad con 5 personas y SUS** | 1 y 3 | Plan, cuestionario SUS y script de cálculo listos (#195); RNF003 «Parcial» | Evelyn (Orlando revisa el plan) |
| **Demo cruzada** (una HU del otro) | Retro del S2 y R4 | Guion en `demo_cruzada.md` | Evelyn y Orlando |

Además, **límites que no son desviaciones sino limitaciones declaradas** y que el informe del gate debe mencionar: rendimiento del backend en 59 (RNF008); RNF001 sin hacer; disponibilidad sin medir (RNF011); `enforce_admins` desactivado por decisión del PO; certificado autofirmado y sin VM en la nube; promoción de la réplica y *cron* de respaldos sin hacer.

## Pendientes por dueño

**Orlando**

- Pedir la aprobación de Evelyn a #209 (informe) y #213 (Retro, Daily y Review) y (los PR de Evelyn #207, #208, #210, #211, #212, #214 y #215 ya están revisados y fusionados).
- Cerrar #132 cuando #213 esté fusionado.
- Mantener el seguimiento de los riesgos de despliegue y mantenimiento en #131 una vez que Evelyn valide los niveles propuestos.
- **Con confirmación aparte:** PR `develop` → `main`, tag `v1.0.0`, comprobar la Release y el paquete (puntos 3 a 7 del Criterio 1.3).
- Manuales: capturas y exportación a PDF (Cierre); verificación de la entrega archivo por archivo (#150).
- Después del S4: demo cruzada y video, junto con Evelyn.

**Evelyn**

- Redactar `gate-0-fase1.md` sobre este archivo y lo que decida el equipo; comentar la decisión en #143. **Ningún módulo de la Fase 2 empieza sin la confirmación explícita en el chat.**
- Aceptar o rechazar el incremento del S3 (Review) y confirmar la Retro.
- Validar los niveles de riesgo propuestos y cerrar #131.
- Su parte del informe: portada, historial e índices; revisar el estado de 4.2.9 (Roadmap), 4.4, 4.5.1 y 5.13 (casos de ventas, heladeros y gerencia); 7 al cierre del gate; informe final en PDF.
- Las pruebas de usabilidad de HU-30 (después del S4).
- Mover las tarjetas del Project (#141, #142, #143) y las iteraciones, o dar permiso a Orlando.

**Los dos**

- Decidir antes de la entrega si se activa `enforce_admins` y se ponen checks obligatorios en `main`.
- Consultar al docente si espera la sección de gestión de servicios (5.16).
- Ensayos cronometrados y la subida única a UTP+Class (viernes 27/11, 14:30).

---

## Cómo volver a medir lo de este archivo

```bash
git fetch && git log --oneline -1 origin/develop
git rev-list --count origin/main..origin/develop          # commits que le faltan a main
gh run list --branch develop --limit 3                    # CI de develop
gh pr list --state open; gh pr list --state merged --limit 100
gh release list; gh api repos/orlando572/erp-donofrio/tags --jq length
gh project item-list 4 --owner orlando572 --format json   # Project
scripts/check_legacy.sh && scripts/test.sh donofrio_base  # pruebas
```
