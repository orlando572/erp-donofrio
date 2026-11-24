# Registro de decisiones del equipo: 23/11/2026

> **Qué es.** El registro de las decisiones que el equipo tomó el 23/11/2026 sobre el plan: Fase 2 completa, hora de corte, Cierre ampliado y manual de usuario. Dice qué se decidió, quién, cuándo y en qué documento del plan quedó reflejado.
>
> **Qué NO es.** **No es la confirmación de inicio de M1** ni de ningún otro módulo de la Fase 2. La regla de [`CLAUDE.md`](../../../CLAUDE.md) no cambia: cada módulo empieza solo con la confirmación explícita, en el chat, de Evelyn u Orlando, y después de cada módulo hay un mini gate y se vuelve a esperar. Este archivo tampoco es el informe del Gate 0 (`gate-0-fase1.md`, que redacta Evelyn) ni lo reemplaza.

**Quién decidió:** Orlando (Scrum Master), en el chat, con el acuerdo de Evelyn (Product Owner) en persona. **Cuándo:** 23/11/2026.

## Decisiones y documentos que cambian

| # | Decisión | Quién · cuándo | Qué documento cambia |
|---|---|---|---|
| 1 | Se hace **toda la Fase 2** (M1 `donofrio_calidad`, M2 `donofrio_heladeros`, M3 cadena de frío, M4 `donofrio_tablero` + marca), en el orden fijo, uno a uno y con mini gate después de cada uno. La nota «lo más probable es que solo entre M1» se sustituye; la red de seguridad es la hora de corte | Orlando, con acuerdo de Evelyn · 23/11/2026 | [04 §4.3](../../plan/04_scrum_pmbok.md) (nota del plazo, criterios), [04 §4.6](../../plan/04_scrum_pmbok.md) (fila S4), [03](../../plan/03_modulos_odoo.md), [05 §5.1](../../plan/05_reparto_equipo.md), [02 §2.3](../../plan/02_mapeo_plantilla.md), [01](../../plan/01_alcance_escenario.md), [PLAN_PROYECTO](../../plan/PLAN_PROYECTO.md), [07](../../plan/07_riesgos_entrega.md) (R1) |
| 2 | **Hora de corte de la Fase 2: jueves 26/11/2026, 08:00** (texto literal más abajo). Desde ahí empieza el Cierre (≈30 h hasta la entrega), que no se toca | Orlando, con acuerdo de Evelyn · 23/11/2026 | [04 §4.3](../../plan/04_scrum_pmbok.md), [04 §4.6 y §4.10](../../plan/04_scrum_pmbok.md) (S4, Cierre, H5), [05 §5.3](../../plan/05_reparto_equipo.md), [07 §7.1](../../plan/07_riesgos_entrega.md) (R17 principal, R1) y [§7.2](../../plan/07_riesgos_entrega.md) (checklist) |
| 3 | El **informe final y los manuales se redactan después de terminar la Fase 2**, en el Cierre. La documentación por módulo (5.5, clases, ER y diccionario, capturas, mini gate) se mantiene como estaba: la hace quien no construye el módulo | Orlando, con acuerdo de Evelyn · 23/11/2026 | [04 §4.3](../../plan/04_scrum_pmbok.md), [05 §5.3](../../plan/05_reparto_equipo.md), [07](../../plan/07_riesgos_entrega.md) (R15), [02 §2.3](../../plan/02_mapeo_plantilla.md) |
| 4 | **Diferidos al final** (después del S4, dentro del Cierre): **HU-30** (5 personas, 4 tareas cronometradas, SUS), la **demo cruzada** y el **video** de la demo. En el Gate 0 quedan como **desviaciones aceptadas por el equipo**, no como cumplidos | Orlando, con acuerdo de Evelyn · 23/11/2026 | [04 §4.3](../../plan/04_scrum_pmbok.md) (criterios 1-3 y nota), [04 §4.4](../../plan/04_scrum_pmbok.md) (fila HU-30), [04 §4.6 y §4.10](../../plan/04_scrum_pmbok.md), [05 §5.1, §5.2, §5.3 y §5.4](../../plan/05_reparto_equipo.md), [02 §2.2](../../plan/02_mapeo_plantilla.md) (6.12, 5.14), [03](../../plan/03_modulos_odoo.md), [PLAN_PROYECTO](../../plan/PLAN_PROYECTO.md) |
| 5 | **Manual de usuario: entregable nuevo**, con la plantilla del docente. **Dueña: Evelyn** (lleva la interfaz y los prototipos); **Orlando lo verifica**. Se redacta en el Cierre, para el estado final del sistema | Orlando, con acuerdo de Evelyn · 23/11/2026 | [02 §2.4](../../plan/02_mapeo_plantilla.md) (nuevo), [05 §5.1 y §5.3](../../plan/05_reparto_equipo.md), [07 §7.2](../../plan/07_riesgos_entrega.md) (checklist g y nombre de archivo), [04 §4.3, §4.6 y §4.10](../../plan/04_scrum_pmbok.md) |

## Texto literal de la hora de corte

> **Hora de corte de la Fase 2: jueves 26/11/2026, 08:00.** A esa hora se congela: lo fusionado entra; lo que no esté listo (o no cumpla su DoD) no se fusiona y queda como «Diseñado – trabajo futuro» con su CU, wireframe y mockup. Desde ahí empieza el Cierre (≈30 h hasta la entrega). El Cierre no se toca.

## Criterio para que un módulo entre o se quede fuera

Un módulo entra en la entrega si, **antes de la hora de corte**, cumple su DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md)):
1. Sus HU cumplen la DoD: PR aprobado por el otro integrante, **CI en verde**, **tests** y **ACL** de cada modelo nuevo, actualización (`-u`) sin errores, criterios verificados en la UI y capturas.
2. Tiene su tag de release.
3. Las secciones del informe afectadas están actualizadas y el ER y el diccionario se extrajeron de nuevo.
4. Su **mini gate** está escrito y el equipo decidió.

Si a la hora de corte no lo cumple, **«lo inconcluso no se fusiona»**: el módulo (o la HU) no entra en `develop` ni en `main`, el RF queda «Diseñado – trabajo futuro» y el informe lo presenta como diseño (CU, wireframe, mockup), nunca como implementado. Un módulo en curso a la hora de corte no se termina durante el Cierre.

## Qué queda registrado como desviación aceptada en el Gate 0

Con la decisión 4, el informe del Gate 0 (`gate-0-fase1.md`) debe presentar estos tres puntos como **desviaciones aceptadas por el equipo**, con fecha de cierre prevista en el Cierre, y no como cumplidos:
- Criterio de salida 1 (todas las HU en «Hecho»): falta **HU-30**.
- Criterio de salida 2 (video de la demo de punta a punta): diferido.
- La demo cruzada de [05 §5.1](../../plan/05_reparto_equipo.md): diferida.

La verificación de Orlando ([`gate-0-verificacion.md`](gate-0-verificacion.md)) ya los muestra con ese estado.

## Documentos que contradicen o no recogen esta decisión (a actualizar)

Estos archivos no se editaron en el PR que creó este registro (su alcance es solo `docs/plan/` y este registro). Quedan para una actualización aparte:

| Documento | Qué dice hoy | Qué hay que ajustar |
|---|---|---|
| [`docs/pm/plan_riesgos.md`](../../pm/plan_riesgos.md) | R17: P = 2, nivel 6; R1 y R15 sin la hora de corte ni el Cierre de ≈30 h; la matriz (fila de nivel 3) lista R17 en el nivel 6 | Igualar a [07 §7.1](../../plan/07_riesgos_entrega.md): R17 con P = 3 (nivel 9) y la hora de corte, R1 y R15 con la decisión, y la matriz de calor |
| [`docs/pm/acta_constitucion.md`](../../pm/acta_constitucion.md) | La Fase 2 aparece «si alcanza el tiempo» | Decir que el objetivo es la Fase 2 completa, con la hora de corte |
| [`docs/plan/06_github_ci_infra.md`](../../plan/06_github_ci_infra.md) | La carpeta `docs/manuales/` lista solo el manual de instalación y el de herramientas | Agregar el manual de usuario |
| [`docs/scrum/sprint-3/planning.md`](../sprint-3/planning.md) | Planeó la demo cruzada «antes del Gate 0» | Es histórico del planning: no se cambia; la `review.md` y la `retro.md` ya registran el diferimiento |
