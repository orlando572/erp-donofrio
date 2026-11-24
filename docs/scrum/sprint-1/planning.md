# Sprint 1 (Fundaciones): Planning

**Fecha:** 22/11/2026 (la iteración `S1` del Project empieza el 23/11) · **Timebox:** ~1 día · **Facilita:** Orlando (SM) · **PO:** Evelyn (pendiente de revisar este planning)

## Objetivo del sprint

"Odoo 19 corre igual en ambas PC, con CI y datos maestros de D'Onofrio."

Fuente: [04 §4.6](../../plan/04_scrum_pmbok.md) y [05 §5.2](../../plan/05_reparto_equipo.md). Fase 1 (núcleo): no hay ningún módulo de la Fase 2 en este sprint.

## Historias de usuario (HU-01 a HU-07: 24 puntos)

| HU | Historia | Criterios de aceptación (resumen) | Pts | Resp. | Req. | Épica |
|---|---|---|---|---|---|---|
| HU-01 | Entorno Docker con Odoo 19 y PostgreSQL 16 | `docker compose up` levanta Odoo en :8069; README con los pasos; la otra persona lo reproduce en su PC | 3 | Orlando | RNF012 | #133 |
| HU-02 | CI que instala los módulos y corre los tests en cada PR | El workflow corre en el PR; falla si hay error de instalación, test rojo o patrón legacy; la protección de rama exige CI verde | 5 | Orlando | RNF007 | #133 |
| HU-03 | Compañía con localización peruana | RUC ficticio válido, PEN, IGV 18 %, `es_PE`, `America/Lima`, plan contable PE; logo y colores en los reportes | 3 | Orlando | RF016 | #134 |
| HU-04 | Usuarios por rol con permisos mínimos | 10 usuarios con `group_ids`; un `ir.rule` propio (CD Arequipa solo ve su almacén); `test_seguridad.py` verifica el `AccessError` | 3 | Orlando | RF018 | #134 |
| HU-05 | Organigrama, puestos y empleados | Departamentos con jerarquía; unos 20 empleados; vista de organigrama exportable | 2 | Evelyn | RF017 | #135 |
| HU-06 | Almacenes de Lima y Arequipa con ubicaciones de frío | 2 almacenes; ruta Lima → AQP; ubicaciones de congelación, refrigeración y seco | 3 | Orlando | RF005 | #134 |
| HU-07 | Productos, insumos y recetas cargados | Unos 25 terminados, unos 20 insumos y unas 12 BoM con operaciones; seguimiento por lote y vida útil | 5 | Orlando | RF009 | #134 |
| | **Total** | | **24** | Orlando 22 · Evelyn 2 | | |

### Épicas del sprint (Project «Scrum ERP D'Onofrio»)

| Issue | Título | Puntos | Responsable | Estado en el Project |
|---|---|---|---|---|
| #133 | [HU-01, HU-02] Entorno Docker y CI | 8 | Orlando | Por hacer |
| #134 | [HU-03, HU-04, HU-06, HU-07] Datos maestros, compañía y seguridad | 14 | Orlando | Por hacer |
| #135 | [HU-05] RR. HH. y análisis empresarial | 2 | Evelyn | Por hacer |

## Orden de ejecución

1. **HU-01** (rama `feature/HU-01-entorno-docker`): Docker Compose con `db` + `odoo`, `.env.example`, README. Base de todo lo demás.
2. **HU-02**: CI. Necesita que `donofrio_base` tenga al menos el esqueleto instalable (`__manifest__.py`), que se incluye en esa HU.
3. **HU-03, HU-06, HU-04, HU-07**: datos y configuración **siempre por código** en `addons/donofrio_base` (XML/CSV/hooks), con tests.
4. **HU-05** (Evelyn) en paralelo, sobre el `donofrio_base` que deja la HU-02.

## Documentación del sprint

| Responsable | Entregables |
|---|---|
| Evelyn | Sección 3 (3.1-3.7), 4.1.1, BPMN AS-IS de ventas, heladeros y compras, tabla de RF (con fase), CU de ventas, heladeros y gerencia |
| Orlando | BPMN AS-IS de producción y almacén, tabla de RNF, 4.1.3, 4.3.1, 4.3.7 |

## Definition of Done (resumen, [04 §4.8](../../plan/04_scrum_pmbok.md))

- PR a `develop` aprobado por el otro integrante y CI en verde.
- Tests para la lógica nueva y ACL para cada modelo nuevo.
- Textos en español, criterios verificados en la UI y capturas en `docs/capturas/sprint-1/`.
- Épica marcada en el Project con el enlace al PR (`Parte de #n`; el último PR de la épica cierra con `Closes #n`).

## Riesgos y dependencias del sprint

- La HU-01 solo se da por cumplida cuando **Evelyn la reproduce en su PC** (criterio de aceptación); hasta entonces queda "En revisión".
- Los puntos se concentran en Orlando (22 de 24); la documentación de negocio de Evelyn compensa la carga ([05 §5.1](../../plan/05_reparto_equipo.md)).
- La etiqueta de la imagen de Odoo se fija con fecha ([06 §6.5](../../plan/06_github_ci_infra.md)) para que el CI y las dos PC usen la misma.
