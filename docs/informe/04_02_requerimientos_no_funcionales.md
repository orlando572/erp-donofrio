# 4.2.3 Requerimientos no funcionales

> **Estado:** versión final del Cierre (25/11/2026) · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [04 §4.2](../plan/04_scrum_pmbok.md), [09 §9.1](../plan/09_normas_marcos.md), [5.14](05_13_a_05_14_pruebas.md), [6.9 a 6.13](06_09_a_06_13_pruebas.md), [trazabilidad](trazabilidad.md)
>
> Los RNF son el complemento de los RF ([4.2.2](04_02_requerimientos_funcionales.md)). Los RNF se verifican sobre el núcleo (Odoo estándar + `donofrio_base`) y, desde el 24/11/2026, también sobre los **módulos de la Fase 2 (M1 a M4)**, que se construyeron y agregaron casos de prueba y mediciones (RNF005, RNF008 y RNF010 en particular). Las fichas detalladas (una por RNF) están en el [Anexo 10.2](anexo_10_02_fichas_rnf.md).

## Cómo se clasifican y se verifican

- **Clasificación:** cada RNF se asigna a una característica del modelo de calidad **ISO/IEC 25010:2023** (ISO/IEC, 2023), que tiene nueve: adecuación funcional, eficiencia de desempeño, compatibilidad, capacidad de interacción, fiabilidad, seguridad, mantenibilidad, flexibilidad (antes portabilidad) y protección (*safety*). Ninguno de los RNF de este proyecto cae en *compatibilidad* ni en *protección*.
- **Verificación:** cada RNF tiene una métrica y una prueba concreta. Las pruebas automáticas viven en `addons/donofrio_base/tests/` y corren en el CI en cada PR; las no funcionales (k6, ZAP, Lighthouse, restauración cronometrada y réplica) se ejecutaron en el Sprint 3, el Lighthouse del tablero de M4 el 24/11/2026, y sus resultados están en la sección [5.14](05_13_a_05_14_pruebas.md).
- **Trazabilidad:** RNF → HU → épica (issue) → prueba, como en [4.2.1](04_02_requerimientos_funcionales.md).

## Tabla 3: requerimientos no funcionales

**Estado al cierre del proyecto** (25/11/2026; para los RNF del núcleo, la medición del 23/11/2026): *Cumple* (hecho, medido o probado, con evidencia en el repositorio), *Cumple con límites* (cumple la meta, con una limitación declarada que no la invalida) o *Parcial* (una parte cumple y otra no). El detalle de cada RNF, con su evidencia y sus límites, está en las fichas del [Anexo 10.2](anexo_10_02_fichas_rnf.md).

| Área | ID | Requerimiento no funcional | Característica 25010:2023 (ISO/IEC, 2023) | Métrica o prueba | HU · sprint | Estado al cierre |
|---|---|---|---|---|---|---|
| **Marketing y Ventas** | RNF001 | Portabilidad: interfaz adaptable que se usa en un navegador moderno de escritorio y en una ventana angosta (pedidos y PdV; liquidación y tablero si hay F2) | Flexibilidad (adaptabilidad) | Revisión de las pantallas en el navegador de escritorio y en una ventana de 375 × 812 | HU-09, HU-10 · S2-S3 | **Parcial**: el tablero y la liquidación se revisaron en una ventana de 375 × 812, sin desplazamiento horizontal ([5.5e.6.1](05_05_modulo_donofrio_tablero.md)). **Límite declarado:** la revisión usó Chrome; no hay una matriz de navegadores |
| | RNF002 | Rendimiento: p95 < 2 s en listas y formularios con 20 usuarios concurrentes | Eficiencia de desempeño (comportamiento temporal) | k6 con 20 usuarios virtuales | HU-28 · S3 | **Cumple** (k6, 23/11/2026): p95 de **11.6 ms** en listas y **9.1 ms** en formularios con 20 usuarios y pausas; unos 100 ms sin pausas. [5.14, Tabla 22](05_13_a_05_14_pruebas.md) |
| | RNF003 | Usabilidad: interfaz en español y tareas clave en ≤ 3 pasos | Capacidad de interacción | Revisión pantalla por pantalla por roles y evaluación heurística de Nielsen ([6.12](06_12_usabilidad.md)) | HU-03, HU-24 · S1, S4 | **Cumple con límites**: interfaz en español (`es_PE`, HU-03); la revisión por roles del 25/11/2026 encontró y corrigió textos en inglés, un error 403 del certificado y fechas fuera de ventana; la evaluación heurística de M1 a M4 está en 6.12. **Límite declarado:** la hizo el propio equipo, con datos de demostración |
| **Logística** | RNF004 | Trazabilidad del 100 % de los lotes de producto terminado (de la OP al cliente) | Adecuación funcional (corrección funcional) | Test de integración OP → lote → entrega | HU-14, HU-33 · S2-S3 | **Cumple**: pruebas de integración compra → recepción → OP → lote con vencimiento (HU-33, PR #192) y pedido → entrega FEFO por lote → factura (PR #191), en el CI; TC-PRO-10 y TC-CAL-03 |
| | RNF005 | Integridad: no se despacha un lote vencido (F1: FEFO y fecha de retiro); tampoco uno rechazado por calidad (F2) | Seguridad (integridad) | Test de la entrega con lotes vencidos | HU-11 · S2 | **Cumple con límites** (M1, 24/11/2026): FEFO y fecha de retiro probados en la entrega (`test_fefo.py`, 10 pruebas) y, con `donofrio_calidad`, un **lote rechazado no se despacha** ni por transferencia ni por el punto de venta (`test_inspeccion.py` y `test_pdv.py`, TC-CAL-07). **Límites:** el punto de venta no verifica el vencimiento (el cajero escribe el lote) y el bloqueo del PdV se probó con pruebas automáticas, no en la pantalla |
| **Producción** | RNF006 | Respaldo diario (RPO 24 h) y réplica en caliente (RPO de segundos); RTO ≤ 2 h | Fiabilidad (recuperabilidad) | Restauración cronometrada y `pg_stat_replication` | HU-25, HU-26 · S3 | **Cumple**: **RTO medido de 31 s** (meta 2 h) con respaldo `.dump` y *filestore* verificados por SHA-256; réplica en *streaming* con retraso de 2.3 ms y escritura rechazada. **Límites:** el *cron* diario está documentado y no instalado; la promoción de la réplica no se probó. [5.14, Tabla 24 d](05_13_a_05_14_pruebas.md) |
| | RNF007 | Mantenibilidad: módulos versionados, lint y tests en CI, sin API obsoleta | Mantenibilidad (modularidad, capacidad de ser probado) | CI en verde: `ruff`, `check_legacy.sh` y tests con `--test-enable` | HU-02 · S1 | **Cumple**: CI obligatorio en `develop` (`lint` y `test`) y **218 pruebas** (137 de `donofrio_base`, 45 de `donofrio_calidad`, 15 de `donofrio_heladeros` y 21 de `donofrio_tablero`; eran 38 al cierre del S1), en verde sobre `develop` `339c907`; `check_legacy.sh` sin patrones legacy y `ruff` sin avisos |
| **Gerencia** | RNF008 | El tablero (estándar en F1, OWL en F2) carga en < 3 s; Lighthouse Performance ≥ 80 (escritorio) en login | Eficiencia de desempeño | Lighthouse en login, backend y dashboard | HU-23, HU-28 · S3 | **Parcial**: login **100**, dashboard **80** con LCP de 1.9 s; el **tablero propio de M4 carga en 2.11 s (LCP, cumple los 3 s) pero saca 76** en escritorio y 39 en móvil, y el **backend queda en 59**. Los dos puntajes bajo 80 son un **límite conocido**: los explica el JavaScript de Odoo (TBT) y no el código del equipo; no se corrigen con configuración. Ver [4.6.4](04_06_wpo.md) |
| | RNF009 | Seguridad: RBAC, HTTPS, gestor de BD deshabilitado, 2FA para el administrador | Seguridad (confidencialidad, autenticidad) | ZAP baseline + tests de acceso | HU-04, HU-27, HU-28 · S1-S3 | **Cumple con límites**: RBAC con 10 roles y regla del CD Arequipa (HU-04), `list_db = False`, Nginx con TLS 1.2 y 1.3 y HSTS, 2FA para el administrador y el gerente, contraseñas de 12 o más y bloqueo por intentos (HU-27); ZAP sin alertas altas. **Límites:** ZAP pasivo y sin sesión; certificado autofirmado; el 2FA se exige solo en el despliegue protegido |
| **Otros** | RNF010 | Auditoría de cambios en datos sensibles (precios, pedidos; liquidaciones e inspecciones en la F2) | Seguridad (responsabilidad) | Chatter + `auditlog` | HU-27 · S3 | **Cumple** para precios, pedidos de venta y de compra (`auditlog` de OCA, `test_cambio_de_precio_queda_auditado`). Las liquidaciones, inspecciones y lecturas de temperatura de M1 a M3 dejan su historial en el chatter (`tracking`), pero no pasan por `auditlog` |
| | RNF011 | Disponibilidad ≥ 99 % en horario laboral; reinicio automático y *healthcheck* | Fiabilidad (disponibilidad) | Registros de `/web/health` y Uptime Kuma | HU-01, HU-32 · S1, S3 | **Parcial**: `restart: unless-stopped` y *healthcheck* en `db`, `odoo` y `db-replica` (los tres `healthy`); **la disponibilidad en el tiempo no se midió** (Uptime Kuma no se implementó) y la meta del 99 % no se puede afirmar como cumplida |
| | RNF012 | Reproducibilidad: el entorno completo se levanta con un comando | Flexibilidad (instalabilidad) | `docker compose up` en una PC limpia | HU-01, HU-29 · S1, S3 | **Cumple**: reproducido desde cero en la PC de Orlando y en la de Evelyn; el CI usa el mismo `docker-compose.yml`; imagen de release construida y probada en ensayo (`probar_imagen.sh`, HU-29). **Verificado el 24 y 25/11/2026:** el tag `v1.0.0` y las releases `v1.1.0` a `v1.4.0` publican la imagen en GHCR y el zip del código (de 23,5 a 26,1 MiB) |
| | RNF013 | Cumplimiento de la Ley 29733: datos personales ficticios y mínimos | Seguridad (confidencialidad) | Revisión de los datos maestros | Todas las HU de datos | **Parcial**: datos de compañía, usuarios, productos, proveedores y empleados ficticios (RUC `20999999990` inventado, correos `.example.com`); no hay política de privacidad ni consentimiento porque no se tratan datos reales |

## Resumen por característica ISO/IEC 25010:2023

| Característica | RNF | Cantidad |
|---|---|---|
| Seguridad | RNF005, RNF009, RNF010, RNF013 | 4 |
| Fiabilidad | RNF006, RNF011 | 2 |
| Eficiencia de desempeño | RNF002, RNF008 | 2 |
| Flexibilidad | RNF001, RNF012 | 2 |
| Mantenibilidad | RNF007 | 1 |
| Capacidad de interacción | RNF003 | 1 |
| Adecuación funcional | RNF004 | 1 |
| **Total** | | **13** |

## Estado al cierre del proyecto

| Estado | RNF | Cantidad |
|---|---|---|
| Cumple | RNF002, RNF004, RNF006, RNF007, RNF010, RNF012 | 6 |
| Cumple con límites | RNF003, RNF005, RNF009 | 3 |
| Parcial | RNF001, RNF008, RNF011, RNF013 | 4 |
| **Total** | | **13** |

**Cambios frente al cierre del Sprint 3** (23/11/2026: 6 *Cumple*, 1 *Cumple con límites*, 5 *Parcial* y 1 sin evidencia):

| RNF | Antes (S3) | Ahora (cierre) | Qué lo cambió |
|---|---|---|---|
| RNF005 | Parcial | **Cumple con límites** | M1: el lote rechazado no se despacha, ni por transferencia ni por el PdV (HU-17, [PR #219](https://github.com/orlando572/erp-donofrio/pull/219) y #224) |
| RNF007 | Cumple | **Cumple** | De 136 a 218 pruebas con los cuatro módulos propios |
| RNF008 | Parcial | **Parcial** | Se midió el tablero propio de M4: LCP de 2.11 s (cumple) y puntaje 76 (límite conocido) |
| RNF010 | Cumple | **Cumple** | M1 a M3 usan el historial del chatter; no pasan por `auditlog` |
| RNF003 | Parcial | **Cumple con límites** | M4 sumó la marca (HU-24); la revisión por roles del 25/11 y la evaluación heurística de M1 a M4 ([6.12](06_12_usabilidad.md)) |
| RNF012 | Cumple | **Cumple** | Publicadas `v1.1.0` a `v1.4.0` con su imagen y su zip |
| RNF001 | Sin evidencia | **Parcial** | El tablero y la liquidación se revisaron en una ventana de 375 × 812 sin desplazamiento horizontal |
| RNF011 y RNF013 | — | Sin cambio | La disponibilidad en el tiempo no se midió |

> **Límites declarados.** Los valores de rendimiento (p95 < 2 s, 20 usuarios) y de disponibilidad (99 %) son metas académicas sobre una instancia local; el rendimiento se midió con datos de demostración, con k6 y el servidor en la misma PC y solo con lecturas (ver [5.14](05_13_a_05_14_pruebas.md)). **Lo que no se midió:** la disponibilidad en el tiempo (RNF011) y la compatibilidad con otros navegadores distintos de Chrome (RNF001). RNF012 se da por *Cumple* con la evidencia de dos PC distintas (Orlando y Evelyn) y con las releases publicadas (`v1.0.0` a `v1.4.0`).

---

## Notas sobre las fuentes

1. **ISO/IEC 25010:2023** (modelo de calidad del producto) está en la [sección 9](09_referencias.md). Los nombres de las nueve características y de las subcaracterísticas asignadas **no se cotejaron con el texto de la norma** (es de pago); se declara como límite.
2. La asignación de cada RNF a una característica, y las metas numéricas (p95 < 2 s, 20 usuarios, 99 %, RPO y RTO), son **juicios del equipo** (supuestos académicos), no valores tomados de la norma.
