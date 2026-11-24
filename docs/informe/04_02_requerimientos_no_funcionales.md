# 4.2.3 Requerimientos no funcionales

> **Estado:** borrador actualizado al cierre del Sprint 3 (23/11/2026) · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [04 §4.2](../plan/04_scrum_pmbok.md), [09 §9.1](../plan/09_normas_marcos.md), [5.14](05_13_a_05_14_pruebas.md), [6.9 a 6.13](06_09_a_06_13_pruebas.md), [trazabilidad](trazabilidad.md)
>
> Los RNF son el complemento de los RF ([4.2.2](04_02_requerimientos_funcionales.md)). **Todos son de la Fase 1**: se verifican sobre el núcleo (Odoo estándar + `donofrio_base`) y los módulos de la Fase 2, si llegan a construirse, solo agregan casos de prueba. Las fichas detalladas (una por RNF) están en el [Anexo 10.2](anexo_10_02_fichas_rnf.md).

## Cómo se clasifican y se verifican

- **Clasificación:** cada RNF se asigna a una característica del modelo de calidad **ISO/IEC 25010:2023** (ISO/IEC, 2023), que tiene nueve: adecuación funcional, eficiencia de desempeño, compatibilidad, capacidad de interacción, fiabilidad, seguridad, mantenibilidad, flexibilidad (antes portabilidad) y protección (*safety*). Ninguno de los RNF de este proyecto cae en *compatibilidad* ni en *protección*.
- **Verificación:** cada RNF tiene una métrica y una prueba concreta. Las pruebas automáticas viven en `addons/donofrio_base/tests/` y corren en el CI en cada PR; las no funcionales (k6, ZAP, Lighthouse, restauración cronometrada y réplica) se ejecutaron en el Sprint 3 y sus resultados están en la sección [5.14](05_13_a_05_14_pruebas.md); el SUS (HU-30) quedó diferido por decisión del equipo.
- **Trazabilidad:** RNF → HU → épica (issue) → prueba, como en [4.2.1](04_02_requerimientos_funcionales.md).

## Tabla 3: requerimientos no funcionales

**Estado al cierre del Sprint 3** (23/11/2026): *Cumple* (hecho, medido o probado, con evidencia en el repositorio), *Cumple con límites* (cumple la meta, con una limitación declarada que no la invalida), *Parcial* (una parte cumple y otra no) o *Pendiente* (todavía no se hizo). El detalle de cada RNF, con su evidencia y sus límites, está en las fichas del [Anexo 10.2](anexo_10_02_fichas_rnf.md).

| Área | ID | Requerimiento no funcional | Característica 25010:2023 (ISO/IEC, 2023) | Métrica o prueba | HU · sprint | Estado al cierre del S3 |
|---|---|---|---|---|---|---|
| **Marketing y Ventas** | RNF001 | Portabilidad: navegadores Chrome, Firefox y Edge; responsive en móvil (pedidos y PdV; liquidación si hay F2) | Flexibilidad (adaptabilidad) | Prueba manual en 3 navegadores y en vista móvil | HU-09, HU-10 · S2-S3 | **Pendiente**: la prueba manual en los tres navegadores y en vista móvil no se hizo ni se registró |
| | RNF002 | Rendimiento: p95 < 2 s en listas y formularios con 20 usuarios concurrentes | Eficiencia de desempeño (comportamiento temporal) | k6 con 20 usuarios virtuales | HU-28 · S3 | **Cumple** (k6, 23/11/2026): p95 de **11.6 ms** en listas y **9.1 ms** en formularios con 20 usuarios y pausas; unos 100 ms sin pausas. [5.14, Tabla 22](05_13_a_05_14_pruebas.md) |
| | RNF003 | Usabilidad: interfaz en español, tareas clave en ≤ 3 pasos, SUS ≥ 70 | Capacidad de interacción | SUS con 5 usuarios y 4 tareas cronometradas | HU-30 · S3 | **Parcial**: interfaz en español (`es_PE`, HU-03); plan, cuestionario y script del SUS hechos ([6.12](06_12_usabilidad.md)); **la prueba con 5 personas está diferida por decisión del equipo (23/11/2026) para después del Sprint 4**, así que el SUS no se midió |
| **Logística** | RNF004 | Trazabilidad del 100 % de los lotes de producto terminado (de la OP al cliente) | Adecuación funcional (corrección funcional) | Test de integración OP → lote → entrega | HU-14, HU-33 · S2-S3 | **Cumple**: pruebas de integración compra → recepción → OP → lote con vencimiento (HU-33, PR #192) y pedido → entrega FEFO por lote → factura (PR #191), en el CI; TC-PRO-10 y TC-CAL-03 |
| | RNF005 | Integridad: no se despacha un lote vencido (F1: FEFO y fecha de retiro); tampoco uno rechazado por calidad (F2) | Seguridad (integridad) | Test de la entrega con lotes vencidos | HU-11 · S2 | **Parcial** (sin cambio desde el S2): FEFO y fecha de retiro probados en la entrega (`test_fefo.py`, 10 pruebas); **limitación declarada:** el punto de venta no lo verifica (el cajero escribe el lote) y el lote rechazado por calidad depende del módulo de la Fase 2, que no se construyó |
| **Producción** | RNF006 | Respaldo diario (RPO 24 h) y réplica en caliente (RPO de segundos); RTO ≤ 2 h | Fiabilidad (recuperabilidad) | Restauración cronometrada y `pg_stat_replication` | HU-25, HU-26 · S3 | **Cumple**: **RTO medido de 31 s** (meta 2 h) con respaldo `.dump` y *filestore* verificados por SHA-256; réplica en *streaming* con retraso de 2.3 ms y escritura rechazada. **Límites:** el *cron* diario está documentado y no instalado; la promoción de la réplica no se probó. [5.14, Tabla 24 d](05_13_a_05_14_pruebas.md) |
| | RNF007 | Mantenibilidad: módulos versionados, lint y tests en CI, sin API obsoleta | Mantenibilidad (modularidad, capacidad de ser probado) | CI en verde: `ruff`, `check_legacy.sh` y tests con `--test-enable` | HU-02 · S1 | **Cumple**: CI obligatorio en `develop` (`lint` y `test`) y **136 pruebas** de `donofrio_base` (eran 38 al cierre del S1); `check_legacy.sh` sin patrones legacy y `ruff` sin avisos |
| **Gerencia** | RNF008 | El tablero (estándar en F1, OWL en F2) carga en < 3 s; Lighthouse Performance ≥ 80 (escritorio) en login | Eficiencia de desempeño | Lighthouse en login, backend y dashboard | HU-23, HU-28 · S3 | **Parcial**: login **100**, dashboard **80** con LCP de 1.9 s; el **backend queda en 59** (TBT del JavaScript de Odoo; no se corrige con configuración), ver [4.6.4](04_06_wpo.md) |
| | RNF009 | Seguridad: RBAC, HTTPS, gestor de BD deshabilitado, 2FA para el administrador | Seguridad (confidencialidad, autenticidad) | ZAP baseline + tests de acceso | HU-04, HU-27, HU-28 · S1-S3 | **Cumple con límites**: RBAC con 10 roles y regla del CD Arequipa (HU-04), `list_db = False`, Nginx con TLS 1.2 y 1.3 y HSTS, 2FA para el administrador y el gerente, contraseñas de 12 o más y bloqueo por intentos (HU-27); ZAP sin alertas altas. **Límites:** ZAP pasivo y sin sesión; certificado autofirmado; el 2FA se exige solo en el despliegue protegido |
| **Otros** | RNF010 | Auditoría de cambios en datos sensibles (precios, pedidos; liquidaciones e inspecciones en F2) | Seguridad (responsabilidad) | Chatter + `auditlog` | HU-27 · S3 | **Cumple** para precios, pedidos de venta y de compra (`auditlog` de OCA, `test_cambio_de_precio_queda_auditado`); liquidaciones e inspecciones son de la Fase 2 |
| | RNF011 | Disponibilidad ≥ 99 % en horario laboral; reinicio automático y *healthcheck* | Fiabilidad (disponibilidad) | Registros de `/web/health` y Uptime Kuma | HU-01, HU-32 · S1, S3 | **Parcial**: `restart: unless-stopped` y *healthcheck* en `db`, `odoo` y `db-replica` (los tres `healthy`); **la disponibilidad en el tiempo no se midió** (Uptime Kuma no se implementó) y la meta del 99 % no se puede afirmar como cumplida |
| | RNF012 | Reproducibilidad: el entorno completo se levanta con un comando | Flexibilidad (instalabilidad) | `docker compose up` en una PC limpia | HU-01, HU-29 · S1, S3 | **Cumple**: reproducido desde cero en la PC de Orlando y en la de Evelyn; el CI usa el mismo `docker-compose.yml`; imagen de release construida y probada en ensayo (`probar_imagen.sh`, HU-29). **Límite:** la imagen en GHCR y el zip se publican con el tag `v1.0.0` del Gate 0 |
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

## Estado al cierre del Sprint 3

| Estado | RNF | Cantidad |
|---|---|---|
| Cumple | RNF002, RNF004, RNF006, RNF007, RNF010, RNF012 | 6 |
| Cumple con límites | RNF009 | 1 |
| Parcial | RNF003, RNF005, RNF008, RNF011, RNF013 | 5 |
| Pendiente | RNF001 | 1 |
| **Total** | | **13** |

**Cambios frente al cierre del Sprint 1** (entonces: 2 *Implementado*, 5 *Parcial* y 6 *Planificado*):

| RNF | Antes (S1) | Ahora (S3) | Qué lo cambió |
|---|---|---|---|
| RNF001 | Planificado | **Pendiente** | No se hizo la prueba manual en tres navegadores y móvil |
| RNF002 | Planificado | **Cumple** | k6 de HU-28 (PR #196) |
| RNF004 | Planificado | **Cumple** | Pruebas de integración de HU-33 (PR #191 y #192) |
| RNF006 | Planificado | **Cumple** | Réplica (HU-25, PR #186) y respaldo y restauración (HU-26, PR #187) |
| RNF008 | Parcial | **Parcial** | Se midió (HU-28, PR #194): login 100, dashboard 80, backend 59 |
| RNF009 | Parcial | **Cumple con límites** | HTTPS y 2FA (HU-27, PR #189) y ZAP (HU-28, PR #196) |
| RNF010 | Planificado | **Cumple** | `auditlog` (HU-27) |
| RNF012 | Implementado | **Cumple** | Se agregó la imagen de release en ensayo (HU-29, PR #190) |
| RNF003, RNF005, RNF011 y RNF013 | Parcial | **Parcial** | Sin cambio de estado; RNF003 y RNF011 avanzaron en material (plan del SUS y *healthchecks*) pero no en medición |

> **Límites declarados.** Los valores de rendimiento (p95 < 2 s, 20 usuarios) y de disponibilidad (99 %) son metas académicas sobre una instancia local; el rendimiento se midió con datos de demostración, con k6 y el servidor en la misma PC y solo con lecturas (ver [5.14](05_13_a_05_14_pruebas.md)). **Lo que no se midió:** RNF001 (navegadores y móvil), la disponibilidad en el tiempo (RNF011) y el SUS (RNF003, diferido). RNF012 se da por *Cumple* con la evidencia de dos PC distintas (Orlando y Evelyn) y con el ensayo local de la release; la imagen publicada en GHCR llega con el tag `v1.0.0`.

---

## Pendiente de citar antes del informe final

1. **ISO/IEC 25010:2023** (modelo de calidad del producto): confirmar con el texto de la norma los nombres de las nueve características y de las subcaracterísticas asignadas (por ejemplo, instalabilidad dentro de flexibilidad y recuperabilidad dentro de fiabilidad), y agregar la referencia APA 7 en la sección 9. Los nombres de esta tabla se escribieron de memoria.
2. La asignación de cada RNF a una característica, y las metas numéricas (p95 < 2 s, 20 usuarios, 99 %, RPO y RTO), son **juicios del equipo** (supuestos académicos), no valores tomados de la norma.
