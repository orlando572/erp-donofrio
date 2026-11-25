# 4.5.2 Riesgos de la etapa de desarrollo (tabla 11)

> **Estado:** versión final del Cierre (25/11/2026); las tablas son la foto del 23/11 y el apartado 4.5.2.6 trae la actualización · **Autora:** Evelyn · **Revisa:** Orlando · **Fuente:** [`docs/pm/plan_riesgos.md`](../pm/plan_riesgos.md) (registro de riesgos, etapa «Desarrollo»), [07 §7.1](../plan/07_riesgos_entrega.md) y las actas de [`docs/scrum/`](../scrum/)
>
> Los riesgos de despliegue y mantenimiento (4.5.3 y 4.5.4) los redacta Orlando. El **nivel** es impacto × probabilidad con las escalas de [4.5.1](../pm/plan_riesgos.md): prioridad **Alta** de 6 a 9, **Media** de 3 a 5 y **Baja** de 1 a 2. Los valores de impacto y probabilidad son los del registro; esta sección **no los cambia**, solo agrega la situación real al 23/11/2026, actualizada al 25/11/2026 en el apartado 4.5.2.6.

## 4.5.2.1 Resumen de la etapa

El registro tiene **15 riesgos de la etapa de desarrollo** (R1 a R6, R10, R12, R15 a R20 y RS-07) y dos impedimentos (IMP-01 e IMP-02).

| Prioridad | Riesgos | Cantidad |
|---|---|---|
| **Alta** (6 a 9) | R1 (9); R2, R4, R5, R6, R15 y R17 (6) | 7 |
| **Media** (3 a 5) | R3 (3, cerrado); R16, R18, R19, R20 y RS-07 (4) | 6 |
| **Baja** (1 a 2) | R10 y R12 (2) | 2 |

**Lectura de la situación real.**
- **1 cerrado** (R3) y **2 mitigados** con evidencia (R2 y R18).
- **1 se materializó en parte y se aceptó** (R6): en Community no hay calidad ni envío a SUNAT; se declaró como limitación.
- **El riesgo dominante es el plazo (R1)**, que condiciona a R15, R17, R19 y R20: la Fase 1 se terminó en unas 21 horas, pero la Fase 2 y las pruebas con usuarios dependen del tiempo que queda hasta el viernes 27/11 a las 14:30.
- Los demás siguen abiertos con acciones concretas (ver la tabla).

## 4.5.2.2 Tabla de riesgos de desarrollo

| Id | Tipo | Riesgo | I | P | Nivel | Prioridad | Estrategia y control | Resp. | Situación real al 23/11/2026 | Estado |
|---|---|---|---|---|---|---|---|---|---|---|
| **R1** | Externo | Plazo muy corto: entrega de todo el viernes 27/11 a las 14:30 | 3 | 3 | **9** | Alta | Mitigar: sprints de ~1 día en orden fijo; la Fase 1 garantiza el entregable; Gate 0 por criterios; Cierre reservado | Evelyn | Los S1 a S3 se hicieron entre el 22/11 a las 22:38 y el 23/11 a las 16:51 (81 de 83 puntos de la Fase 1). La HU-30 (2 puntos) y las pruebas con 5 personas se **difieren** hasta después del S4 por decisión del equipo. El Gate 0 está por redactar | **Abierto** (mitigado en la Fase 1; vigente hasta el 27/11) |
| **R2** | Técnico | API obsoleta de Odoo generada por el asistente de IA o por tutoriales viejos | 3 | 2 | 6 | Alta | Mitigar: fuentes 19.0 locales, ficha de cambios, *hook*, `check_legacy.sh` en el CI, instalación con pruebas en cada PR | Orlando | El CI corre `lint` (con `check_legacy.sh` y `ruff`) y `test` en cada PR; `develop` está en verde en su último commit. `donofrio_base` pasó de 38 a 136 pruebas. En el S2 la revisión cruzada halló un error de vigencia (UTC frente a hora de Lima) que no era de API obsoleta | **Mitigado** (S1); se revisa en el Gate 0 |
| **R3** | Organizacional | Otro grupo elige la misma empresa | 3 | 1 | 3 | Media | Evitar: el docente asignó D'Onofrio y es el único grupo con esta empresa | Evelyn | Confirmado el 22/11/2026 (registro de riesgos) | **Cerrado** |
| **R4** | Humano | Carga desigual o un integrante no puede defender su parte | 3 | 2 | 6 | Alta | Mitigar: reparto por áreas de punta a punta, revisión cruzada, demos cruzadas, dos ensayos | Evelyn y Orlando | Puntos terminados **por una sola persona**: Orlando 47, Evelyn 21 y 13 compartidos (81 en total). Autoría de los commits en `develop`: Orlando 54 y Evelyn 31 de 85. La revisión cruzada sí se cumplió (46 PR con aprobación vigente). La **demo cruzada sigue sin hacerse** en vivo | **Abierto**: la carga fue desigual en S0 y S1; hacer la demo cruzada antes del Gate 0 |
| **R5** | Organizacional | El uso de IA no declarado se interpreta como plagio | 3 | 2 | 6 | Alta | Evitar: declarar el asistente de IA en la metodología; todo revisado y entendido por quien lo firma; fuentes citadas | Evelyn y Orlando | El asistente se declara en [4.3.4](04_03_04_ides_y_gestion_proyectos.md), en la [infraestructura 4.3.1](04_03_infraestructura.md) y en la sección 10 del manual de herramientas. Las reglas de uso están en `CLAUDE.md`. **Falta** un párrafo de metodología con la lista de qué se hizo con apoyo de IA y que cada uno revisó | **Abierto**: redactar el párrafo antes del informe final |
| **R6** | Técnico | Módulo OCA o funcionalidad no disponible en Community 19 | 2 | 3 | 6 | Alta | Aceptar y mitigar: módulo propio pequeño; EDI y nómina declarados como limitación | Orlando | **Se materializó en parte.** No hay envío electrónico a SUNAT (`l10n_pe_edi` es Enterprise) ni inspecciones de calidad ligadas a la orden (Calidad es Enterprise). El primero se declaró como limitación (RF016); la segunda queda como módulo M1 de la Fase 2 | **Aceptado** con limitaciones declaradas |
| **R10** | Externo | Cambia el escenario de Froneri antes de la entrega | 1 | 2 | 2 | Baja | Aceptar: fecha de corte 2026 declarada; solo se actualiza el párrafo del entorno | Evelyn | El escenario está fijado con corte en 2026 y como supuesto S1 ([3.2.5](03_aspectos_generales.md)); la transición se menciona como oportunidad y amenaza, pero no se modela. No hubo novedades que obliguen a reescribir | **Abierto** (monitoreo) |
| **R12** | Organizacional | El título 6.3 de la plantilla nombra otra herramienta y el evaluador espera verla | 1 | 2 | 2 | Baja | Mitigar: una línea bajo el título que justifica GitHub Projects y aviso al docente | Evelyn | La justificación está en 6.3 y en [4.3.9](04_03_04_ides_y_gestion_proyectos.md). **Falta** el aviso al docente | **Mitigando** |
| **R15** | Organizacional | La documentación se deja para el final | 3 | 2 | 6 | Alta | Evitar: la DoD exige un borrador por HU; checklist de secciones en el issue «Informe final»; el Gate 0 exige el informe en borrador | Evelyn | Cada sprint entregó su documentación en PR aparte (por ejemplo #161, #181, #201 y #203). Con esta tanda quedan en borrador las secciones 4.1.4, 4.2.10 a 4.2.12, 4.3.4, 4.3.9, 4.5.2, 8.1, 9 y 10.1. Quedan por hacer 4.5.3 y 4.5.4 (Orlando), la maquetación y los índices | **Mitigado en lo avanzado**; vigente hasta el Cierre |
| **R16** | Técnico | La evidencia de Scrum se concentra en pocos días | 2 | 2 | 4 | Media | Mitigar: commits pequeños y diarios de ambos; actas fechadas | Orlando | **Se materializó por diseño del plan:** los 85 commits de `develop` están entre el 22 y el 23/11/2026 y los sprints duran un día. Mitigación real: cada acta lleva su fecha y los PR tienen hora de fusión ([`S3-informe6_prs_fusionados.tsv`](../capturas/sprint-3/S3-informe6_prs_fusionados.tsv)) | **Aceptado** |
| **R17** | Organizacional | La Fase 2 se come el tiempo del Cierre o deja un módulo a medias | 3 | 2 | 6 | Alta | Evitar: Gate 0 y mini gates por criterios; Cierre reservado; lo inconcluso no se fusiona | Orlando (criterios), Evelyn (decisión) | **No se empezó ningún módulo** de la Fase 2: `addons/` solo contiene `donofrio_base`. El Cierre sigue reservado. La decisión queda en el informe del Gate 0 (`docs/scrum/gates/gate-0-fase1.md`, por redactar) | **Controlado**; se revisa en cada gate |
| **R18** | Técnico | El agente de IA sigue con la Fase 2 sin autorización tras el gate | 2 | 2 | 4 | Media | Evitar: regla del gate en `CLAUDE.md`; solo vale la confirmación explícita en el chat | Orlando | La regla está en `CLAUDE.md` desde el S0 y no hay código de la Fase 2 en el repositorio | **Mitigado** |
| **R19** | Humano | Sin Fase 2, un integrante se queda sin código propio que defender | 2 | 2 | 4 | Media | Mitigar: cada uno es dueño de sus datos, pruebas y configuración en `donofrio_base` | Evelyn y Orlando | Cada integrante firma sus HU con datos, pruebas y evidencias. Las de Evelyn: HU-05, 08, 09, 10, 13, 15, 23, 32 y su parte de HU-16, 28 y 33 | **Abierto**: depende de la decisión del Gate 0 (el módulo M2 `donofrio_heladeros` es de Evelyn) |
| **R20** | Humano | Fatiga por el ritmo de un sprint por día | 2 | 2 | 4 | Media | Mitigar: dailies cortas, revisión cruzada, CI como red de seguridad, Cierre sin desarrollo | Evelyn y Orlando | Los tres sprints se hicieron en unas 21 horas. El CI atrapó errores sin esfuerzo humano; el Cierre sigue sin desarrollo. Es un riesgo real mientras dure la semana de entrega | **Abierto** |
| **RS-07** | Organizacional | Normas, cifras o competidores del informe citados sin verificar la fuente | 2 | 2 | 4 | Media | Mitigar: marcas «[cita]» en el borrador y lista de pendientes en [`03_aspectos_generales.md`](03_aspectos_generales.md); verificar cada fuente y citarla en APA 7 | Evelyn | Las marcas «[cita]» de la sección 3 y de 4.1.3 y 4.2.3 se resuelven con las referencias de la sección 9; las cifras con una sola fuente se redactan con «según…» | **Mitigando**: se cierra al fusionar la sección 9 y quitar las marcas |

## 4.5.2.3 Impedimentos del equipo

| Id | Impedimento | Acción | Situación real |
|---|---|---|---|
| IMP-01 | GitHub Free no permite proteger ramas en repositorios privados | Se hizo público el repositorio (decisión de Orlando, 22/11) | **Resuelto**: `main` y `develop` protegidas |
| IMP-02 | Evelyn no pudo hacer su parte del S0 y la hizo Orlando | Evelyn revisa los artefactos del PO y los aprueba o corrige | **Abierto**: la Review del S0 sigue con la decisión del PO sin registrar |

## 4.5.2.4 Seguimiento, frecuencia, herramienta y validación

| Aspecto | Cómo se hace |
|---|---|
| **Seguimiento** | En cada Planning y Retro; **R2, R17 y R18** también en cada gate. Se registra como comentario en el issue «Registro de riesgos» (#131) |
| **Frecuencia** | Una vez por sprint (Retro) y en cada gate |
| **Herramienta** | [`docs/pm/plan_riesgos.md`](../pm/plan_riesgos.md) (registro y valores) y el issue #131 del GitHub Project (historial) |
| **Validación** | El PO valida y ambos revisan |

**Historial del seguimiento (issue #131).** Hay un comentario por la Retro del S1 (23/11/2026: R2 baja de P=3 a P=2, entra RS-07 y RS-01 a RS-06 quedan sin cambios) y otro por la Retro del S2 (sin cambios). **Falta** el comentario de la Retro del S3 y, con él, el cierre del issue, que se hace cuando esta sección esté fusionada.

## 4.5.2.6 Actualización al cierre de la Fase 2 (25/11/2026)

Las filas de arriba conservan lo medido el 23/11/2026, antes del Gate 0. Con la Fase 2 completa, lo que cambió es esto (los valores de impacto y probabilidad del registro **no se tocaron**; el seguimiento formal en el issue #131 sigue abierto):

| Riesgo | Qué pasó | Situación al 25/11/2026 |
|---|---|---|
| **R1** Plazo | La Fase 2 completa (M1 a M4) se terminó el 25/11, antes de la hora de corte (jueves 26/11, 08:00); el Cierre se mantuvo reservado | **Mitigado** en lo técnico; el plazo sigue siendo el viernes 27/11 a las 14:30 |
| **R4** Carga desigual | Cada integrante es dueño de dos módulos: Orlando M1 y M3, Evelyn M2 y M4; los PR de cada uno los aprobó el otro (79 de 82 con aprobación vigente). La demo cruzada **no se hizo todavía** | **Abierto**: **[PENDIENTE: demo cruzada en vivo]** |
| **R6** Funcionalidad no disponible en Community | La inspección de calidad (Enterprise) se cubrió con el módulo propio M1; el envío electrónico a SUNAT sigue sin existir | Se materializó y se mitigó con módulo propio, salvo SUNAT (limitación declarada, [8](08_recomendaciones.md)) |
| **R15** Documentación al final | Cada módulo trajo su documentación (5.5b a 5.5e), su mini gate y sus capturas con su PR; este informe pasó a su estado final en el Cierre | **Mitigado** |
| **R17** La Fase 2 se come el Cierre o deja un módulo a medias | Los cuatro módulos se fusionaron completos, cada uno con su mini gate; los límites de cada uno están declarados (vista móvil en celular real, Lighthouse, sensores) | **Mitigado**: ningún módulo quedó a medias |
| **R18** El agente de IA sigue sin autorización | Cada módulo empezó con la confirmación explícita de Evelyn u Orlando en el chat, según `CLAUDE.md` | **Mitigado** |
| **R19** Sin Fase 2, un integrante sin código propio | Ya no aplica: la Fase 2 se construyó y cada integrante tiene módulos propios | **Cerrado** |
| **R20** Fatiga | Los cuatro módulos se hicieron entre el 24 y el 25/11, y el Cierre sigue en curso | **Abierto** hasta la entrega |

## 4.5.2.5 Acciones antes del Gate 0 (histórico, 23/11/2026)

1. Hacer la **demo cruzada** en vivo (R4).
2. Escribir el **párrafo de metodología** sobre el uso del asistente de IA (R5).
3. **Avisar al docente** sobre el uso de GitHub Projects en lugar de la herramienta de la plantilla (R12).
4. Fusionar la sección 9 y **quitar las marcas «[cita]»** (RS-07).
5. Registrar el seguimiento de la **Retro del S3** en el issue #131 y cerrarlo.
6. Revisar **R2, R17 y R18** en el informe del Gate 0.
