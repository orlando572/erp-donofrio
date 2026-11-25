# 10.2 Anexo: fichas de requerimientos no funcionales

> **Estado:** versión final del Cierre (25/11/2026) · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [4.2.3](04_02_requerimientos_no_funcionales.md) (tabla 3), [02 §2.2](../plan/02_mapeo_plantilla.md) (10.2), [5.13 y 5.14](05_13_a_05_14_pruebas.md), [6.9 a 6.13](06_09_a_06_13_pruebas.md), [trazabilidad](trazabilidad.md)
>
> Una ficha por RNF, con el formato de la tabla 40 de la plantilla (campo y valor), su característica ISO/IEC 25010:2023, el resultado real al cierre del proyecto (25/11/2026) y su evidencia. Las fichas de RF son el anexo 10.1 (de Evelyn). **Las características de la norma** (ISO/IEC, 2023; ver el final de 4.2.3) son juicios del equipo y no se cotejaron con el texto de la norma. Los estados usan la escala de 4.2.3: *Cumple*, *Cumple con límites*, *Parcial* y *Pendiente*.

## Resumen de las fichas

| RNF | Requerimiento | Característica 25010:2023 | Estado | Evidencia principal |
|---|---|---|---|---|
| [RNF001](#rnf001) | Portabilidad: navegador de escritorio y vista adaptable | Flexibilidad (adaptabilidad) | **Parcial** | [5.5e.6.1](05_05_modulo_donofrio_tablero.md) |
| [RNF002](#rnf002) | Rendimiento: p95 < 2 s con 20 usuarios concurrentes | Eficiencia de desempeño (comportamiento temporal) | **Cumple** | [Tabla 22](05_13_a_05_14_pruebas.md) |
| [RNF003](#rnf003) | Usabilidad: español y tareas en ≤ 3 pasos | Capacidad de interacción | **Cumple con límites** | [6.12](06_12_usabilidad.md) |
| [RNF004](#rnf004) | Trazabilidad del 100 % de los lotes | Adecuación funcional (corrección funcional) | **Cumple** | Pruebas HU-33 |
| [RNF005](#rnf005) | Integridad: no se despacha un lote vencido ni uno rechazado por calidad | Seguridad (integridad) | **Cumple con límites** | `test_fefo.py` y `test_inspeccion.py` |
| [RNF006](#rnf006) | Respaldo diario, réplica en caliente y RTO ≤ 2 h | Fiabilidad (recuperabilidad) | **Cumple** | HU-25 y HU-26 |
| [RNF007](#rnf007) | Mantenibilidad: módulos versionados, lint y tests en CI | Mantenibilidad (modularidad y capacidad de ser probado) | **Cumple** | CI y 218 pruebas |
| [RNF008](#rnf008) | Rendimiento del tablero y del acceso (Lighthouse ≥ 80) | Eficiencia de desempeño | **Parcial** (límite conocido) | [4.6.4](04_06_wpo.md) |
| [RNF009](#rnf009) | Seguridad: RBAC, HTTPS, gestor de BD cerrado y 2FA | Seguridad (confidencialidad y autenticidad) | **Cumple con límites** | HU-27 y HU-28 |
| [RNF010](#rnf010) | Auditoría de cambios en datos sensibles | Seguridad (responsabilidad) | **Cumple** | HU-27 |
| [RNF011](#rnf011) | Disponibilidad ≥ 99 %, reinicio automático y healthcheck | Fiabilidad (disponibilidad) | **Parcial** | Tabla 24 c |
| [RNF012](#rnf012) | Reproducibilidad: el entorno se levanta con un comando | Flexibilidad (instalabilidad) | **Cumple** | HU-29 |
| [RNF013](#rnf013) | Cumplimiento de la Ley 29733: datos ficticios y mínimos | Seguridad (confidencialidad) | **Parcial** | C-18 de 5.11 |

## RNF001

### Tabla 40.1. Ficha de RNF001: Portabilidad: navegador de escritorio y vista adaptable

| Campo | Valor |
|---|---|
| Identificador | RNF001 |
| Nombre | Portabilidad: navegador de escritorio y vista adaptable |
| Área | Marketing y Ventas |
| Descripción | El ERP debe funcionar en un navegador moderno de escritorio y ser usable en una ventana angosta en los procesos de pedidos y punto de venta (y en la liquidación del heladero de M2 y el tablero de M4). |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Flexibilidad (adaptabilidad) |
| Meta o criterio de aceptación | Los casos de uso de pedidos (CU002) y PdV (CU003) se completan sin errores visibles, y las pantallas de M2 y M4 caben sin desplazamiento horizontal en 375 × 812. |
| Método de verificación | Revisión de las pantallas en el navegador de escritorio y en una ventana de 375 × 812, con capturas. |
| HU, PR y sprint | HU-09 (PR #167, #171, #172) y HU-10 (PR #170, #172); S2 y S3 |
| Resultado al cierre | **Parcial.** Odoo 19 usa un cliente web adaptable y las pantallas del núcleo son las estándar. La liquidación (M2) y el tablero (M4) se revisaron en una ventana de 375 × 812, sin desplazamiento horizontal ([5.5e.6.1](05_05_modulo_donofrio_tablero.md)). |
| Estado | **Parcial** |
| Evidencia | Capturas del tablero y del acceso en 375 × 812 ([5.5e.6.1](05_05_modulo_donofrio_tablero.md)). |
| Límites declarados | La revisión usó Chrome y las capturas del informe son de un solo navegador. El PdV se probó en escritorio. |
| Riesgos relacionados | R1 (plazo). No tiene riesgo propio en el registro. |
| Qué falta o siguiente paso | Extender la revisión de CU002 y CU003 a otros navegadores y a la ventana angosta, y registrarla con capturas. Va en [8.2](08_recomendaciones.md). |

## RNF002

### Tabla 40.2. Ficha de RNF002: Rendimiento: p95 < 2 s con 20 usuarios concurrentes

| Campo | Valor |
|---|---|
| Identificador | RNF002 |
| Nombre | Rendimiento: p95 < 2 s con 20 usuarios concurrentes |
| Área | Marketing y Ventas |
| Descripción | Las listas y los formularios responden con un percentil 95 menor a 2 s con 20 usuarios concurrentes. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Eficiencia de desempeño (comportamiento temporal) |
| Meta o criterio de aceptación | p95 < 2 000 ms por tipo de petición; fallos HTTP < 1 %; errores de JSON-RPC < 1 %; comprobaciones > 99 %. |
| Método de verificación | k6 (`grafana/k6:1.7.1`) con 20 usuarios virtuales: subida de 20 s, 3 min con los 20 activos y bajada de 10 s, contra el despliegue protegido (Nginx con TLS y Odoo con 2 *workers*), en la base `donofrio_perf` (143 MB). |
| HU, PR y sprint | HU-28, parte de k6 (PR #196); S3 |
| Resultado al cierre | **Normal** (pausas de 1 a 3 s): 2 765 peticiones, 0 fallidas, p95 de **11.6 ms** en listas y **9.1 ms** en formularios (tablero 13.0 ms, aplicación 17.8 ms, inicio de sesión 342 ms). **Esfuerzo** (sin pausas, 20 veces más rápido): p95 de unos 100 ms y 1 petición fallida de 20 888. Odoo llegó a 160 % de una CPU y 513 MiB. |
| Estado | **Cumple** |
| Evidencia | [la evidencia de k6 y ZAP](../capturas/sprint-3/HU-28_evidencia_k6_zap.txt), [el resumen de k6](../capturas/sprint-3/HU-28_k6_resumen.json), [el resumen de k6 sin pausas](../capturas/sprint-3/HU-28_k6_esfuerzo_resumen.json); [5.14, Tabla 22](05_13_a_05_14_pruebas.md); `scripts/perf/carga.js` y `k6.sh`. |
| Límites declarados | Datos de demostración; k6 y el servidor comparten la PC (sin red de por medio); solo lecturas (no escrituras concurrentes ni el PdV); una petición `load_menus` falló en la prueba de esfuerzo y no se investigó la causa; no hay proyección de usuarios de la temporada alta. |
| Riesgos relacionados | R7 (poca RAM, mitigado: la carga cabe con holgura). |
| Qué falta o siguiente paso | Medir escrituras concurrentes y el PdV; investigar la petición fallida del esfuerzo. |

## RNF003

### Tabla 40.3. Ficha de RNF003: Usabilidad: español y tareas en ≤ 3 pasos

| Campo | Valor |
|---|---|
| Identificador | RNF003 |
| Nombre | Usabilidad: español y tareas en ≤ 3 pasos |
| Área | Marketing y Ventas |
| Descripción | La interfaz está en español y las tareas clave se hacen en pocos pasos; se revisan por roles y con las heurísticas de Nielsen. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Capacidad de interacción |
| Meta o criterio de aceptación | Interfaz en español; tareas clave en ≤ 3 pasos. |
| Método de verificación | Revisión pantalla por pantalla por roles (administrador, inspector, vendedor y gerente, 25/11/2026) y evaluación heurística de M1 a M4 con las 10 heurísticas de Nielsen ([6.12](06_12_usabilidad.md)). |
| HU, PR y sprint | HU-03 (idioma `es_PE`, PR #155) y HU-24 (marca); S1 y S4 |
| Resultado al cierre | **Cumple con límites.** Interfaz en español cumplida (HU-03). La revisión por roles del 25/11/2026 corrigió textos en inglés, el error 403 del certificado, fechas fuera de ventana y plazos de tickets; la evaluación heurística (6.12) no halló tareas clave de más de tres pasos en las pantallas revisadas. **Límite:** la hizo el propio equipo, con datos de demostración. |
| Estado | **Parcial** |
| Evidencia | Sección 6.12 (revisión por roles del 25/11/2026 y evaluación heurística) y las capturas de M1 a M4. |
| Límites declarados | La revisión y la evaluación las hizo el propio equipo con datos de demostración; no hay una medición con tiempos por tarea. |
| Riesgos relacionados | R4 y R15 (carga desigual y documentación al final). |
| Qué falta o siguiente paso | Observar a usuarios reales con sus tareas, cuando el sistema entre en operación ([8.1](08_01_recomendaciones_negocio.md)). |

## RNF004

### Tabla 40.4. Ficha de RNF004: Trazabilidad del 100 % de los lotes

| Campo | Valor |
|---|---|
| Identificador | RNF004 |
| Nombre | Trazabilidad del 100 % de los lotes |
| Área | Logística |
| Descripción | Cada lote de producto terminado se puede seguir desde la orden de producción hasta el cliente. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Adecuación funcional (corrección funcional) |
| Meta o criterio de aceptación | El lote producido por una OP aparece en la entrega del pedido, y la compra de insumos llega al lote terminado. |
| Método de verificación | Pruebas de integración en `addons/donofrio_base/tests/` (en el CI). |
| HU, PR y sprint | HU-14 (PR #174, #176) y HU-33 (PR #191 de Evelyn y #192 de Orlando); S2 y S3 |
| Resultado al cierre | Las pruebas pasan: compra → recepción → orden de producción → lote con vencimiento (`test_flujo_compra_produccion.py::test_flujo_completo_del_planificador_al_lote_terminado`), el lote producido sale después por FEFO (`test_produccion.py`) y pedido → entrega por lote → factura (`test_flujo_venta.py`). 136 pruebas del módulo en verde. |
| Estado | **Cumple** |
| Evidencia | TC-PRO-10 y TC-CAL-03 ([5.13](05_13_a_05_14_pruebas.md)); [la evidencia de las pruebas](../capturas/sprint-3/S3-informe6_evidencia_tests.txt); [6.11](06_09_a_06_13_pruebas.md). |
| Límites declarados | La trazabilidad hacia atrás desde un cliente concreto (retiro del mercado) no tiene una prueba propia; se apoya en el seguimiento estándar de lotes de Odoo. |
| Riesgos relacionados | — |
| Qué falta o siguiente paso | Agregar una prueba de trazabilidad inversa (de un lote al cliente) si hay tiempo. |

## RNF005

### Tabla 40.5. Ficha de RNF005: Integridad: no se despacha un lote vencido

| Campo | Valor |
|---|---|
| Identificador | RNF005 |
| Nombre | Integridad: no se despacha un lote vencido |
| Área | Logística |
| Descripción | No se despacha un lote vencido ni en su fecha de retiro (F1); tampoco uno rechazado por calidad (F2). |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Seguridad (integridad) |
| Meta o criterio de aceptación | Un lote vencido o en fecha de retiro no se reserva; sale primero el que vence antes (FEFO). |
| Método de verificación | Pruebas de la entrega con lotes vencidos y en fecha de retiro. |
| HU, PR y sprint | HU-11 (PR #169, #176); S2 |
| Resultado al cierre | **Cumple en inventario y ventas:** `test_lote_vencido_no_se_reserva`, `test_lote_en_fecha_de_retiro_no_se_reserva` (`test_fefo.py`, 10 pruebas) y `test_un_lote_vencido_no_entra_en_la_entrega_del_pedido`. **No cumple en el punto de venta:** el cajero escribe el lote y Odoo estándar no comprueba su vencimiento. **«Rechazado por calidad» (M1, 24/11/2026):** con `donofrio_calidad` un lote rechazado no se despacha ni por transferencia (`test_inspeccion.py::test_un_lote_rechazado_no_se_despacha`) ni por el punto de venta (`test_pdv.py::test_el_pdv_no_saca_del_stock_un_lote_rechazado`). |
| Estado | **Cumple con límites** |
| Evidencia | `addons/donofrio_base/tests/test_fefo.py` y `test_flujo_venta.py`; [la evidencia de las pruebas](../capturas/sprint-3/S3-informe6_evidencia_tests.txt); TC-CAL-01 y TC-CAL-02 ([5.13](05_13_a_05_14_pruebas.md)). |
| Límites declarados | Limitación aceptada en la Fase 1 y declarada en la Retro del Sprint 2. |
| Riesgos relacionados | RS-06 (la alerta a 30 días depende del *cron* de Odoo; la exclusión no). |
| Qué falta o siguiente paso | Validar el vencimiento del lote en el PdV (mejora) o dejarlo declarado; el lote rechazado ya lo bloquea `donofrio_calidad` (M1). |

## RNF006

### Tabla 40.6. Ficha de RNF006: Respaldo diario, réplica en caliente y RTO ≤ 2 h

| Campo | Valor |
|---|---|
| Identificador | RNF006 |
| Nombre | Respaldo diario, réplica en caliente y RTO ≤ 2 h |
| Área | Producción |
| Descripción | Hay un respaldo diario (RPO de 24 h), una réplica en caliente (RPO de segundos) y la recuperación toma 2 h o menos. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Fiabilidad (recuperabilidad) |
| Meta o criterio de aceptación | RPO 24 h con respaldo y de segundos con la réplica; RTO ≤ 2 h (7 200 s). |
| Método de verificación | Restauración cronometrada en una base nueva y `pg_stat_replication`; `scripts/verificar_backup.sh` y `verificar_replica.sh` (jobs `backup` y `replica` del CI). |
| HU, PR y sprint | HU-25 (PR #186) y HU-26 (PR #187); S3 |
| Resultado al cierre | **RTO medido de 31 s** (11 s en la de `verificar_backup.sh`). Respaldo `.dump` de 7.4 MB y *filestore* de 5.4 MB en 2 s; sumas SHA-256 verificadas y **un respaldo alterado se rechaza**; la restauración no pisa una base existente; módulos, usuarios, adjuntos y contactos coinciden (105, 14, 751 y 33). **Réplica:** estado `streaming`, asíncrona, retraso de 2.3 ms, escritura rechazada en la réplica y el rol de Odoo sin permisos de superusuario ni de replicación. |
| Estado | **Cumple** |
| Evidencia | [la evidencia del respaldo](../capturas/sprint-3/HU-26_evidencia_respaldo.txt), [la evidencia de la réplica](../capturas/sprint-3/HU-25_evidencia_replica.txt); [5.9](05_07_a_05_09_arquitectura_bd.md); [5.14, Tabla 24 d](05_13_a_05_14_pruebas.md). |
| Límites declarados | El *cron* diario está documentado y **no instalado**; los respaldos no se cifran y viven en el mismo equipo; la promoción de la réplica y el *failover* automático no se probaron. |
| Riesgos relacionados | R8, RS-04 (mitigado), RS-05 (disco al 91 %). |
| Qué falta o siguiente paso | Instalar el *cron*, copiar los respaldos fuera del equipo y probar la promoción ([8.2](08_recomendaciones.md)). |

## RNF007

### Tabla 40.7. Ficha de RNF007: Mantenibilidad: módulos versionados, lint y tests en CI

| Campo | Valor |
|---|---|
| Identificador | RNF007 |
| Nombre | Mantenibilidad: módulos versionados, lint y tests en CI |
| Área | Producción |
| Descripción | El código está versionado, con lint, pruebas en el CI y sin API obsoleta de Odoo. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Mantenibilidad (modularidad y capacidad de ser probado) |
| Meta o criterio de aceptación | CI en verde: `ruff`, `check_legacy.sh` y pruebas con `--test-enable`; instalación sin `ERROR`. |
| Método de verificación | Job `lint` (`scripts/check_legacy.sh` y `ruff` 0.8.4) y job `test` (`scripts/test.sh`), obligatorios en `develop`. |
| HU, PR y sprint | HU-02 (PR #154, #159); S1, con pruebas de todas las HU posteriores |
| Resultado al cierre | Las pruebas pasaron de 38 (S1) a **136** de `donofrio_base` (S3) y a **218** con los módulos propios (137 + 45 + 15 + 21); la corrida del CI sobre `develop` `339c907` (25/11/2026) dio `0 failed, 0 error(s) of 218 tests`; `check_legacy.sh`: sin patrones legacy; `ruff`: sin avisos. En el CI, `lint` tuvo 101 ejecuciones correctas y `test` 98 correctas (3 canceladas por una corrida más nueva). La última corrida de `develop` está en verde. |
| Estado | **Cumple** |
| Evidencia | [la evidencia de las pruebas](../capturas/sprint-3/S3-informe6_evidencia_tests.txt); [6.4, Tabla 28](06_04_a_06_06_repositorio.md); [6.10](06_09_a_06_13_pruebas.md); [4.3.6](04_03_infraestructura.md). |
| Límites declarados | No se mide la cobertura de código ni hay `pylint-odoo` (el plan lo contemplaba); no hay un job `upgrade` (`-u` sobre una base con datos). |
| Riesgos relacionados | R2 (API obsoleta, mitigado), RS-01. |
| Qué falta o siguiente paso | Job `upgrade` y medición de cobertura (opcionales). |

## RNF008

### Tabla 40.8. Ficha de RNF008: Rendimiento del tablero y del acceso (Lighthouse ≥ 80)

| Campo | Valor |
|---|---|
| Identificador | RNF008 |
| Nombre | Rendimiento del tablero y del acceso (Lighthouse ≥ 80) |
| Área | Gerencia |
| Descripción | El tablero carga en menos de 3 s y el puntaje de rendimiento de Lighthouse es de al menos 80 en escritorio en el login. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Eficiencia de desempeño |
| Meta o criterio de aceptación | LCP del tablero < 3 s; Lighthouse Performance ≥ 80 en el login. |
| Método de verificación | Lighthouse 12 (escritorio) en login, backend y dashboard, mediana de 3 corridas, antes (desarrollo, `?debug=assets`) y después (despliegue protegido con Nginx, gzip y caché). |
| HU, PR y sprint | HU-23 (PR #188) y HU-28, parte de Lighthouse (PR #194, de Evelyn); S3 |
| Resultado al cierre | Login: 98 → **100**; dashboard: 45 → **80** con LCP de **1.9 s**; backend: 35 → **59** (LCP de 2.2 s, pero TBT de 384 ms por el JavaScript del cliente web de Odoo). Cumple en el login y en el dashboard estándar, no en el backend. **Tablero propio de M4 (24/11/2026):** LCP de **2.11 s** (cumple la carga en menos de 3 s) y puntaje **76** en escritorio (50 antes) y **39** en móvil. |
| Estado | **Parcial** |
| Evidencia | [4.6.4](04_06_wpo.md), [los resultados de Lighthouse](../capturas/sprint-3/HU-28_lighthouse_resultados.csv); `scripts/perf/lighthouse.py`. |
| Límites declarados | **Límite conocido:** el backend en 59 y el tablero en 76 (39 en móvil) son el costo del JavaScript del cliente web de Odoo, no del código del equipo, y no se corrigen con configuración; el dashboard estándar cumple «justo» (80). Mediciones en una PC con datos de demostración; la del tablero, en otra PC y con el Jefe de Almacén ([los resultados de Lighthouse de M4](../capturas/sprint-4/S4_lighthouse_m4_resultados.csv)). |
| Riesgos relacionados | — |
| Qué falta o siguiente paso | Reducir el JavaScript cargado en el backend (módulos instalados, cliente web) y volver a medir ([8.2](08_recomendaciones.md)). |

## RNF009

### Tabla 40.9. Ficha de RNF009: Seguridad: RBAC, HTTPS, gestor de BD cerrado y 2FA

| Campo | Valor |
|---|---|
| Identificador | RNF009 |
| Nombre | Seguridad: RBAC, HTTPS, gestor de BD cerrado y 2FA |
| Área | Gerencia |
| Descripción | Control de acceso por roles, tráfico cifrado, gestor de bases de datos deshabilitado y segundo factor para el administrador. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Seguridad (confidencialidad y autenticidad) |
| Meta o criterio de aceptación | 10 roles con la regla del CD Arequipa; HTTPS con TLS 1.2 o superior; `list_db = False`; 2FA para el administrador y el gerente; ZAP sin alertas altas. |
| Método de verificación | ZAP baseline (`ghcr.io/zaproxy/zaproxy:2.17.0`) sobre el despliegue protegido; `scripts/verificar_despliegue.sh` (7 grupos, job `proxy`); `test_seguridad.py` y `test_hardening.py`. |
| HU, PR y sprint | HU-04 (PR #157), HU-27 (PR #189) y HU-28, parte de ZAP (PR #196); S1 a S3 |
| Resultado al cierre | ZAP: **0 altas**, 4 medias y 3 bajas aceptadas con su motivo (`FAIL-NEW 0 · WARN-NEW 0 · IGNORE 10 · PASS 58`); la primera corrida tenía 6 medias y 7 bajas y se corrigió en Nginx (CSP, `Permissions-Policy`, COOP y cookies `Secure`/`SameSite`). TLS 1.2 y 1.3 aceptados y 1.1 rechazado, HSTS, `/web/database/manager` → 404, contraseñas de 12 o más, bloqueo tras 5 intentos y 2FA (`admin` y `gerente` → `/web/login/totp`). 21 pruebas de acceso y endurecimiento en el CI. |
| Estado | **Cumple con límites** |
| Evidencia | [la evidencia de seguridad](../capturas/sprint-3/HU-27_evidencia_seguridad.txt), [`HU-28_zap_reporte.html`](../capturas/sprint-3/HU-28_zap_reporte.html), [la evidencia de k6 y ZAP](../capturas/sprint-3/HU-28_evidencia_k6_zap.txt); [5.10 a 5.12](05_10_a_05_12_seguridad.md) (18 controles); [6.13](06_09_a_06_13_pruebas.md). |
| Límites declarados | ZAP es pasivo y sin sesión (no ve el backend autenticado); certificado autofirmado; el 2FA solo se exige con `proxy_mode`; la CSP necesita `unsafe-inline` y `unsafe-eval` por OWL; el sitio web público de Odoo (`/web/signup`, `/contactus`) responde y hay que revisarlo antes de publicar en Internet. |
| Riesgos relacionados | RS-02 (mitigado con límites), RS-03 (mitigado). |
| Qué falta o siguiente paso | Análisis activo y autenticado con ZAP, certificado válido y revisar el sitio web público ([8.2](08_recomendaciones.md)). |

## RNF010

### Tabla 40.10. Ficha de RNF010: Auditoría de cambios en datos sensibles

| Campo | Valor |
|---|---|
| Identificador | RNF010 |
| Nombre | Auditoría de cambios en datos sensibles |
| Área | Otros |
| Descripción | Los cambios en precios, pedidos y compras quedan registrados con usuario, fecha y valor anterior. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Seguridad (responsabilidad) |
| Meta o criterio de aceptación | Un cambio en una lista de precios o un pedido deja un registro de auditoría. |
| Método de verificación | `auditlog` de OCA (reglas por código) y *chatter* de Odoo; pruebas en `test_hardening.py`. |
| HU, PR y sprint | HU-27 (PR #189); S3 |
| Resultado al cierre | Reglas sobre las listas de precios y sus líneas (crear, modificar, borrar) y sobre los pedidos de venta y de compra (modificar, borrar). La prueba `test_cambio_de_precio_queda_auditado` pasa y el cambio 15 → 20 → 15 del jefe de ventas queda con usuario, fecha, valor anterior y nuevo; `test_reglas_de_auditoria_confirmadas`. |
| Estado | **Cumple** |
| Evidencia | [la evidencia de seguridad](../capturas/sprint-3/HU-27_evidencia_seguridad.txt); control C-12 de [5.11](05_10_a_05_12_seguridad.md); `addons/donofrio_base/models/auditlog_rule.py`. |
| Límites declarados | Las liquidaciones, las inspecciones y las lecturas de temperatura de M1 a M3 dejan su historial en el chatter (`tracking`) y **no** pasan por `auditlog`; `auditlog` es un módulo de OCA fijado por *commit* (sin Dependabot). |
| Riesgos relacionados | — |
| Qué falta o siguiente paso | Extender `auditlog` a las liquidaciones, las inspecciones y las temperaturas de M1 a M3 ([8.2](08_recomendaciones.md)). |

## RNF011

### Tabla 40.11. Ficha de RNF011: Disponibilidad ≥ 99 %, reinicio automático y healthcheck

| Campo | Valor |
|---|---|
| Identificador | RNF011 |
| Nombre | Disponibilidad ≥ 99 %, reinicio automático y healthcheck |
| Área | Otros |
| Descripción | El sistema está disponible al menos el 99 % del horario laboral y se reinicia solo si falla. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Fiabilidad (disponibilidad) |
| Meta o criterio de aceptación | Disponibilidad ≥ 99 % en horario laboral; `restart` automático y *healthcheck* en los servicios. |
| Método de verificación | Registros de `GET /web/health` y Uptime Kuma (no implementado). |
| HU, PR y sprint | HU-01 (PR #153), HU-32 (PR #193, mesa de servicios y SLA); S1 y S3 |
| Resultado al cierre | **Hecho:** `restart: unless-stopped` en `db`, `odoo` y `db-replica`; *healthcheck* de Odoo (`/web/health` cada 15 s) y de PostgreSQL (`pg_isready` cada 5 s); los tres contenedores `healthy` el 23/11/2026; réplica caliente. **No hecho:** la medición continua de la disponibilidad; la meta del 99 % **no se puede afirmar como cumplida**. |
| Estado | **Parcial** |
| Evidencia | `docker inspect` y `docker compose ps` ([5.14, Tabla 24 c](05_13_a_05_14_pruebas.md)); [la evidencia de la réplica](../capturas/sprint-3/HU-25_evidencia_replica.txt); [`S1_docker_compose_ps.png`](../capturas/sprint-1/S1_docker_compose_ps.png). |
| Límites declarados | Un solo nodo y sin *failover* automático; no hay registro en el tiempo. |
| Riesgos relacionados | RS-06 (el *healthcheck* no detecta un *cron* detenido). |
| Qué falta o siguiente paso | Instalar Uptime Kuma (perfil `tools`) o un registro periódico de `/web/health` ([8.2](08_recomendaciones.md)). |

## RNF012

### Tabla 40.12. Ficha de RNF012: Reproducibilidad: el entorno se levanta con un comando

| Campo | Valor |
|---|---|
| Identificador | RNF012 |
| Nombre | Reproducibilidad: el entorno se levanta con un comando |
| Área | Otros |
| Descripción | El entorno completo se levanta con un comando, igual en cualquier PC. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Flexibilidad (instalabilidad) |
| Meta o criterio de aceptación | `docker compose up` en una PC limpia deja Odoo y PostgreSQL `healthy` y la base `donofrio` instalada. |
| Método de verificación | Reproducción desde cero en dos PC (`docker compose up -d --build` y `scripts/init_db.sh`); ensayo de la release (`scripts/probar_imagen.sh`). |
| HU, PR y sprint | HU-01 (PR #153) y HU-29 (PR #190); S1 y S3 |
| Resultado al cierre | Reproducido en la PC de Orlando y en la de Evelyn (ambos servicios `healthy` y login con respuesta 200); el CI usa el mismo `docker-compose.yml`. **Release:** imagen de 3.25 GB construida y probada (Odoo 19.0, `donofrio_base` y `auditlog` dentro, configuración de desarrollo y de producción correctas) y zip de 17 MB sin `.env` en el ensayo. |
| Estado | **Cumple** |
| Evidencia | [la evidencia de la release](../capturas/sprint-3/HU-29_evidencia_release.txt), [`HU-01_odoo_login.png`](../capturas/sprint-1/HU-01_odoo_login.png); [manual de instalación](../manuales/manual_instalacion.md); [la guía de release](../dev/release.md). |
| Límites declarados | Publicado el 24 y 25/11/2026: `v1.0.0` (zip de 23,5 MiB) y `v1.1.0` a `v1.4.0` (hasta 26,1 MiB), cada uno con su GitHub Release e imagen en GHCR. El paquete de GHCR no se pudo listar con la CLI (falta el permiso `read:packages`); su visibilidad pública se verificó en el navegador para `v1.0.0`. |
| Riesgos relacionados | R7, R14. |
| Qué falta o siguiente paso | Publicar `v1.0.0` y verificar la Release y el paquete (Gate 0). |

## RNF013

### Tabla 40.13. Ficha de RNF013: Cumplimiento de la Ley 29733: datos ficticios y mínimos

| Campo | Valor |
|---|---|
| Identificador | RNF013 |
| Nombre | Cumplimiento de la Ley 29733: datos ficticios y mínimos |
| Área | Otros |
| Descripción | Los datos personales del sistema son ficticios y mínimos, de modo que no se trata información real de personas. |
| Característica ISO/IEC 25010:2023 (ISO/IEC, 2023) | Seguridad (confidencialidad) |
| Meta o criterio de aceptación | Ningún dato real de personas ni RUC real en el repositorio. |
| Método de verificación | Revisión de los datos maestros de cada HU de datos. |
| HU, PR y sprint | HU-03 (PR #155), HU-05 (PR #160), HU-16 (PR #175, #180) y las demás HU de datos; S1 y S2 |
| Resultado al cierre | Compañía con RUC inventado `20999999990`, correos `.example.com`, empleados, usuarios, clientes y proveedores ficticios; los campos privados de los empleados los protege el grupo de RR. HH. de Odoo. Aviso de «proyecto académico, no afiliado» en el README. |
| Estado | **Parcial** |
| Evidencia | [5.11, control C-18](05_10_a_05_12_seguridad.md); [`trazabilidad`](trazabilidad.md); el README; `addons/donofrio_base/data/clientes_data.xml` y `rrhh_data.xml`. |
| Límites declarados | No hay política de privacidad ni consentimiento (no aplica con datos ficticios); la revisión de los datos de cada HU no se registró de forma sistemática. |
| Riesgos relacionados | R11 (marca e identidad). |
| Qué falta o siguiente paso | Revisión final de los datos maestros antes de la entrega. |

---

## Notas

1. Los estados de este anexo son los de la tabla 3 de [4.2.3](04_02_requerimientos_no_funcionales.md) y los de la matriz de [trazabilidad](trazabilidad.md); si uno cambia, se cambian los tres. Las metas numéricas (p95 de 2 s, 20 usuarios, 99 %, RPO y RTO) son **supuestos académicos del equipo**.
2. **Fuera de las fichas:** la medición de la disponibilidad (RNF011) y la compatibilidad con navegadores distintos de Chrome (RNF001) son los dos puntos sin medición; el primero depende del tiempo.
