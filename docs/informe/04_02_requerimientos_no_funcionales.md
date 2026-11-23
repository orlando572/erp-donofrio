# 4.2.3 Requerimientos no funcionales

> **Estado:** borrador del Sprint 1 · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [04 §4.2](../plan/04_scrum_pmbok.md), [09 §9.1](../plan/09_normas_marcos.md)
>
> Los RNF son el complemento de los RF ([4.2.2](04_02_requerimientos_funcionales.md)). **Todos son de la Fase 1**: se verifican sobre el núcleo (Odoo estándar + `donofrio_base`) y los módulos de la Fase 2, si llegan a construirse, solo agregan casos de prueba. Las fichas detalladas (una por RNF) van en el Anexo 10.2 (Sprints 2 y 3).

## Cómo se clasifican y se verifican

- **Clasificación:** cada RNF se asigna a una característica del modelo de calidad **ISO/IEC 25010:2023**, que tiene nueve: adecuación funcional, eficiencia de desempeño, compatibilidad, capacidad de interacción, fiabilidad, seguridad, mantenibilidad, flexibilidad (antes portabilidad) y protección (*safety*). Ninguno de los RNF de este proyecto cae en *compatibilidad* ni en *protección*.
- **Verificación:** cada RNF tiene una métrica y una prueba concreta. Las pruebas automáticas viven en `addons/donofrio_base/tests/` y corren en el CI en cada PR; las no funcionales (k6, ZAP, Lighthouse, SUS, restauración cronometrada) se ejecutan en el Sprint 3 y sus resultados van a la sección 5.14.
- **Trazabilidad:** RNF → HU → épica (issue) → prueba, como en [4.2.1](04_02_requerimientos_funcionales.md).

## Tabla 3: requerimientos no funcionales

**Estado** al cierre del Sprint 1: *Implementado* (hecho y probado), *Parcial* (una parte ya está en `develop`) o *Planificado* (con su sprint).

| Área | ID | Requerimiento no funcional | Característica 25010:2023 | Métrica o prueba | HU · sprint | Estado |
|---|---|---|---|---|---|---|
| **Marketing y Ventas** | RNF001 | Portabilidad: navegadores Chrome, Firefox y Edge; responsive en móvil (pedidos y PdV; liquidación si hay F2) | Flexibilidad (adaptabilidad) | Prueba manual en 3 navegadores y en vista móvil | HU-09, HU-10 · S2-S3 | Planificado |
| | RNF002 | Rendimiento: p95 < 2 s en listas y formularios con 20 usuarios concurrentes | Eficiencia de desempeño (comportamiento temporal) | k6 con 20 usuarios virtuales | HU-28 · S3 | Planificado |
| | RNF003 | Usabilidad: interfaz en español, tareas clave en ≤ 3 pasos, SUS ≥ 70 | Capacidad de interacción | SUS con 5 usuarios y 4 tareas cronometradas | HU-30 · S3 | Parcial: interfaz en español (`es_PE`, HU-03); falta el SUS |
| **Logística** | RNF004 | Trazabilidad del 100 % de los lotes de producto terminado (de la OP al cliente) | Adecuación funcional (corrección funcional) | Test de integración OP → lote → entrega | HU-14, HU-33 · S2-S3 | Planificado (productos con lote y vida útil ya cargados, HU-07) |
| | RNF005 | Integridad: no se despacha un lote vencido (F1: FEFO y fecha de retiro); tampoco uno rechazado por calidad (F2) | Seguridad (integridad) | Test de la entrega con lotes vencidos | HU-11 · S2 | Parcial: FEFO y fechas de retiro configurados por categoría (HU-07); falta la prueba de entrega |
| **Producción** | RNF006 | Respaldo diario (RPO 24 h) y réplica en caliente (RPO de segundos); RTO ≤ 2 h | Fiabilidad (recuperabilidad) | Restauración cronometrada y `pg_stat_replication` | HU-25, HU-26 · S3 | Planificado |
| | RNF007 | Mantenibilidad: módulos versionados, lint y tests en CI, sin API obsoleta | Mantenibilidad (modularidad, capacidad de ser probado) | CI en verde: `ruff`, `check_legacy.sh` y tests con `--test-enable` | HU-02 · S1 | **Implementado** (CI en cada PR, en `develop` y `main`, con corrida semanal; 38 pruebas en `donofrio_base`) |
| **Gerencia** | RNF008 | El tablero (estándar en F1, OWL en F2) carga en < 3 s; Lighthouse Performance ≥ 80 (escritorio) en login | Eficiencia de desempeño | Lighthouse en login, backend y dashboard | HU-23, HU-28 · S3 | Planificado |
| | RNF009 | Seguridad: RBAC, HTTPS, gestor de BD deshabilitado, 2FA para el administrador | Seguridad (confidencialidad, autenticidad) | ZAP baseline + tests de acceso | HU-04, HU-27, HU-28 · S1-S3 | Parcial: RBAC con 10 roles y regla del CD Arequipa (HU-04), gestor de BD deshabilitado (`list_db = False`, HU-01); faltan HTTPS y 2FA (HU-27) |
| **Otros** | RNF010 | Auditoría de cambios en datos sensibles (precios, pedidos; liquidaciones e inspecciones en F2) | Seguridad (responsabilidad) | Chatter + `auditlog` | HU-27 · S3 | Planificado |
| | RNF011 | Disponibilidad ≥ 99 % en horario laboral; reinicio automático y *healthcheck* | Fiabilidad (disponibilidad) | Registros de `/web/health` y Uptime Kuma | HU-01, HU-32 · S1, S3 | Parcial: `restart: unless-stopped` y *healthcheck* en ambos servicios (HU-01); falta la medición |
| | RNF012 | Reproducibilidad: el entorno completo se levanta con un comando | Flexibilidad (instalabilidad) | `docker compose up` en una PC limpia | HU-01, HU-29 · S1, S3 | **Implementado** en la PC de Orlando desde cero (BD nueva con `scripts/init_db.sh`); falta repetirlo en la PC de Evelyn |
| | RNF013 | Cumplimiento de la Ley 29733: datos personales ficticios y mínimos | Seguridad (confidencialidad) | Revisión de los datos maestros | Todas las HU de datos | Parcial: los datos de compañía, usuarios, productos, proveedores y empleados cargados son ficticios (RUC `20999999990` inventado, correos `.example.com`); se revisan los de cada HU posterior |

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

## Estado al cierre del Sprint 1

| Estado | RNF | Cantidad |
|---|---|---|
| Implementado | RNF007, RNF012 | 2 |
| Parcial | RNF003, RNF005, RNF009, RNF011, RNF013 | 5 |
| Planificado | RNF001, RNF002, RNF004, RNF006, RNF008, RNF010 | 6 |

> **Límites declarados.** Los valores de rendimiento (p95 < 2 s, 20 usuarios) y de disponibilidad (99 %) son metas académicas sobre una instancia local; la medición real llega en el Sprint 3. RNF012 se da por *Implementado* solo con la evidencia de una PC; el criterio de la HU-01 pide además reproducirlo en la PC de la otra persona.
