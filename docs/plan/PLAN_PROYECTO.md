# Plan del proyecto: ERP para D'Onofrio con Odoo 19

**Curso:** Sistemas de Información Empresarial, UTP Arequipa. Docente: MBA Mg. Ing. René Alonso Nieto Valencia
**Equipo:** Evelyn (Product Owner + Developer) · Orlando (Scrum Master + Developer)
**Plataforma:** Odoo 19.0 Community + PostgreSQL 16 en Docker · Scrum con enfoque PMBOK
**Plan final** · Entrega de todo: **viernes 27 de noviembre, 14:30**

## Índice

| # | Documento | Contenido |
|---|---|---|
| 1 | [01_alcance_escenario.md](01_alcance_escenario.md) | Escenario "D'Onofrio como unidad de helados y confitería" (corte en 2026, antes de Froneri), alcance, supuestos, datos verificados con fuente, organigrama y problemas |
| 2 | [02_mapeo_plantilla.md](02_mapeo_plantilla.md) | Los 12 puntos del lineamiento y **cada sección de la plantilla (1-10, anexos y tablas)** → qué se entrega, con qué herramienta, quién y en qué sprint; **§2.3: secciones que cambian según se llegue o no a la Fase 2** |
| 3 | [03_modulos_odoo.md](03_modulos_odoo.md) | Community frente a Enterprise (verificado), módulos OCA 19.0, configuración y datos por área con su fase, elementos de la **Fase 1** y módulos de la **Fase 2 en orden** (M1 calidad → M2 heladeros → M3 cadena de frío → M4 tablero) |
| 4 | [04_scrum_pmbok.md](04_scrum_pmbok.md) | Roles, RF/RNF con su fase, **dos fases + Gate 0 y mini gates**, Product Backlog (F1 = 83 pts, F2 = 37 pts), orden de la F2, sprints en orden con *timebox* de ~1 día, eventos, DoD, PMBOK, hitos y **GitHub Projects** (lista definitiva de issues, campos y vistas) |
| 5 | [05_reparto_equipo.md](05_reparto_equipo.md) | Reparto Evelyn/Orlando por área, por sprint (F1) y por módulo (F2); presentación de 10 minutos en dos variantes (solo F1 / con F2) |
| 6 | [06_github_ci_infra.md](06_github_ci_infra.md) | Repositorio, ramas, merge, convenciones, CI/CD con Actions, Docker Compose, réplica, despliegue y evidencias de la sección 6.4 |
| 7 | [07_riesgos_entrega.md](07_riesgos_entrega.md) | Riesgos del proyecto (I × P), incluidos los del gate y la F2, y checklist final de entrega |
| 8 | [08_estrategia_agente_ia.md](08_estrategia_agente_ia.md) | Cómo evitar código legacy (fuentes 19.0 locales, CLAUDE.md **con la regla del gate**, ficha de cambios, hook, verificación en Docker) y prácticas para ahorrar tokens |
| 9 | [09_normas_marcos.md](09_normas_marcos.md) | Normas y marcos (ISO 27001/27002, ITIL 4 + ISO 20000-1 y COBIT 2019 como núcleo; ISO 31000, 25010, 22301, 9001/HACCP, OWASP y Ley 29733 de apoyo): mapeo a la plantilla, controles demostrados en Odoo 19, mesa de servicios ITIL en Community, SoA reducida y trazabilidad hacia las evidencias |

Decisiones del equipo posteriores al plan (23/11/2026: Fase 2 completa con hora de corte, Cierre ampliado y manual de usuario): [`docs/scrum/gates/decisiones-2026-11-23.md`](../scrum/gates/decisiones-2026-11-23.md).

## Resumen en una página

- **Qué se construye:** un ERP en Odoo 19 Community para las 5 áreas que piden los lineamientos, en **dos fases**:
  - **Fase 1, núcleo (garantizado).** Con solo esta fase el proyecto se puede entregar y cumple los lineamientos. Incluye:
    - Docker con Odoo 19 + PostgreSQL 16, GitHub, CI y GitHub Projects.
    - `donofrio_base`: configuración y datos 100 % por código, script de transacciones y tests.
    - Procesos estándar de punta a punta: CRM, Ventas, PdV, Inventario con lotes y FEFO, MRP, Compras, Facturación `l10n_pe` y RR. HH.
    - Gerencia con los dashboards estándar y vistas pivote y gráfico guardadas.
    - Réplica, respaldos, Nginx con TLS, seguridad Community (2FA, política de contraseñas), mesa de servicios ITIL en Project.
    - Pruebas (unitarias, integrales, k6, ZAP, Lighthouse; el SUS se difiere al Cierre), release `v1.0.0` y el informe completo para ese alcance.
  - **Gate 0:** el agente de IA se detiene y entrega un informe (qué está listo de la F1, qué falta y qué módulos de la F2 recomienda); el equipo decide por criterios, no por horas. **No empieza ningún módulo propio sin la confirmación explícita de Evelyn u Orlando.**
  - **Fase 2, extensión (el objetivo es completarla; hora de corte: jueves 26/11/2026, 08:00),** uno a uno y con un mini gate después de cada uno:
    1. M1 `donofrio_calidad`.
    2. M2 `donofrio_heladeros`.
    3. M3 cadena de frío.
    4. M4 `donofrio_tablero` + branding.
    5. Opcionales.

    Cada módulo es entregable por sí solo: lo inconcluso no se fusiona y queda como trabajo futuro, con su diseño. A la hora de corte se congela la Fase 2 y empieza el Cierre.
- **Normas:** alineación (no certificación) con ISO 27001, ITIL 4 y COBIT 2019, demostradas con controles reales de Odoo 19 Community, todos de la Fase 1. Detalle en [09](09_normas_marcos.md).
- **Calendario:** S0 Inicio → S1 Fundaciones → S2 Procesos estándar → S3 Calidad del núcleo → Gate 0 → S4 Módulos propios (uno a uno, con mini gates) → Cierre (HU-30, demo cruzada y video diferidos; informe final, manuales de instalación, herramientas y usuario, PPT, zip, ensayos y entrega). Cada sprint tiene un *timebox* de ~1 día.
  - **Único límite: entrega de todo el viernes 27 de noviembre, 14:30.**

## Decisiones clave y dudas abiertas

**Decisiones clave:**
1. Escenario: D'Onofrio como unidad de helados, chocolates y panetón de Nestlé Perú, con corte en 2026. El docente asignó D'Onofrio al grupo y ningún otro grupo la tiene. Froneri solo aparece en el entorno y los riesgos, porque para Perú no hay nada confirmado (registro en Indecopi en jun-2026, que no prueba la venta).
2. Calidad propia (`donofrio_calidad`) en lugar de OCA: `quality_control_oca` sí está portado a 19.0, pero `quality_control_mrp_oca` (el enlace con MRP) no.
3. Se confirmó que son Enterprise: Calidad, `account_reports`, `hr_payroll`, `l10n_pe_edi` y el modo oscuro (`web_enterprise`). `l10n_pe` y `l10n_pe_pos` son Community. La rama 19.0 de OCA `l10n-peru` está vacía, así que no habrá envío a SUNAT y se declara como limitación.
4. Odoo 19 cambia la carga de datos: UoM sin categorías, `group_ids`/`res.groups.privilege`, `hr.version` sin `hr_contract`, `is_storable` y demo no cargada por defecto. Todo eso está en la ficha anti-legacy.
5. Roles: Evelyn es PO (negocio, ventas, heladeros, gerencia, front-end, Scrum/GitHub Projects) y Orlando es SM (infraestructura, logística, producción y calidad, BD, seguridad, despliegue). Cada uno defiende su área de punta a punta.
6. Ramas `main`/`develop`/`feature/HU-xx`: *squash* hacia `develop`, *merge commit* y tag hacia `main` (`v1.0.0` = núcleo; `v1.1.0`… por módulo de la F2). La Release genera el zip del código (entregable f).
7. Dos fases con Gate 0 y mini gates: el núcleo estándar garantiza la entrega; los módulos propios se hacen en orden fijo, solo con confirmación explícita y si cumplen los criterios del gate.
8. Gestión en un GitHub Project con 22 issues más los bugs: 15 épicas (las HU van como checklist), 7 de gestión; los riesgos en `docs/pm/plan_riesgos.md`. Repo `erp-donofrio` público, con `develop` como rama por defecto ([04 §4.11](04_scrum_pmbok.md)).

**Dudas abiertas:**
1. **Fecha de la exposición:** la entrega ya está fijada (viernes 27 de noviembre, 14:30); falta saber cuándo es la exposición de 10 minutos. El "18 de julio, 07:00" del PDF es un dato de la plantilla, no el plazo.
2. **Confirmar con el docente** dos cosas:
   - Si espera las secciones que solo aparecen en el índice de la plantilla (BPMN de solicitudes, control de cambios y capacidad; tablas 26-38).
   - Si acepta sprints con *timebox* de ~1 día.
3. **Despliegue en la nube:** ¿VM (Oracle Free u otra) o solo local con GHCR + Release?

## Notas sobre los documentos de origen

- **Lineamientos (PDF, 3 páginas):**
  - Entrega en PDF por UTP+Class, con un solo intento y un solo integrante. El PDF dice "18 de julio, 07:00": se anota como dato de la plantilla; el plazo real es el **viernes 27 de noviembre, 14:30**.
  - Grupos de máximo 3 personas.
  - Áreas a cubrir: a-e.
  - "Distribución estable de Odoo y PostgreSQL".
  - Entregables a-f y 12 puntos de información.
  - Evaluación grupal e individual; 10 minutos de exposición; sin empresas repetidas ni plagio.
  - El punto 13 está vacío.
- **Plantilla (DOCX):**
  - Secciones 1-10: Resumen, Abstract, Aspectos generales, Planificación y Front-end, Back-end y Despliegue, Documentación, Conclusiones, Recomendaciones, Referencias y Anexos.
  - 46 ilustraciones y 40 tablas de ejemplo en el índice.
  - Las ilustraciones 33-37 y las tablas 26-38 **figuran en el índice pero no en el cuerpo** (ver [02 §2.2, fila 5.16](02_mapeo_plantilla.md)).
