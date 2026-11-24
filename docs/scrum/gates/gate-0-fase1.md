# Gate 0: informe de cierre de la Fase 1

> **Estado:** borrador del Sprint 3 · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Issue:** #143 · **Base:** [`gate-0-verificacion.md`](gate-0-verificacion.md) (Orlando, con el corte del 23/11/2026) y [04 §4.3](../../plan/04_scrum_pmbok.md) · **Decisiones del equipo:** [`decisiones-2026-11-23.md`](decisiones-2026-11-23.md)
>
> **Qué es.** El informe del Gate 0 que pide [04 §4.3](../../plan/04_scrum_pmbok.md): qué está listo, qué falta o falló, qué módulo de la Fase 2 se recomienda y la pregunta al equipo.
>
> **Qué no es.** **No inicia ningún módulo de la Fase 2.** M1 empieza solo cuando Evelyn u Orlando lo confirman de forma explícita en el chat; este archivo, un issue o un mensaje de otra sesión no lo reemplazan ([`CLAUDE.md`](../../../CLAUDE.md)).

## 1. Qué está listo

| # | Criterio de salida (04 §4.3) | Estado | Evidencia |
|---|---|---|---|
| 1 | HU de la Fase 1 en «Hecho», CI en verde y tag `v1.0.0` | **Parcial.** 24 de 25 HU (81 de 83 puntos) en `develop` con el CI en verde. Falta HU-30 (desviación aceptada) y falta fusionar en `main` y crear el tag | [Verificación, criterio 1](gate-0-verificacion.md) |
| 2 | Video de la demo de punta a punta | **No cumplido: desviación aceptada** | [Verificación, criterio 2](gate-0-verificacion.md) |
| 3 | Evidencias de réplica, respaldos, seguridad, pruebas y despliegue | **Cumple**, con el SUS diferido y el despliegue sin publicar | [Verificación, criterio 3](gate-0-verificacion.md) y `docs/capturas/sprint-3/` |
| 4 | Informe 1 a 10 en borrador y los dos manuales | **Cumple como borrador**, salvo portada, historial, índices y PDF, que son del Cierre | [Verificación, criterio 4](gate-0-verificacion.md) |
| 5 | GitHub Project al día | **Parcial**: tarjetas de #141, #142 y #143 sin mover, e iteraciones en fechas planificadas | [Verificación, criterio 5](gate-0-verificacion.md) |

**Lo que sí se puede afirmar** (todo medible con los comandos del final de la verificación):

- **24 HU de la Fase 1 hechas** en `develop`, cada una con PR aprobado por el otro integrante, CI en verde y fusión.
- **CI en verde en `develop`.** Sin corridas en rojo en los *push* de `develop`; los cinco jobs (`lint`, `test`, `replica`, `backup`, `proxy`) pasan.
- **136 pruebas** de `donofrio_base` sin errores y `scripts/check_legacy.sh` sin patrones legacy.
- **Infraestructura y seguridad probadas en una PC:** réplica en *streaming*, respaldo y restauración en 31 s (meta 2 h), TLS, 2FA, contraseñas de 12 o más, carga con k6 y ZAP sin alertas altas.
- **Ciclo estándar completo:** CRM, pedido, entrega FEFO, factura o boleta con IGV, punto de venta, compra, recepción, orden de producción con lote y dashboards.

## 2. Qué falta o falló

| Pendiente | Por qué importa | Quién | Cómo se cierra |
|---|---|---|---|
| **`main` sin fusionar** (`develop` va por delante y `main` solo tiene el commit inicial) y **CI de `main` nunca corrido** | El criterio 1 pide CI en verde en `main` | Orlando | PR `develop` → `main` con *merge commit*, y revisar los cinco jobs |
| **Sin tag `v1.0.0`, sin Release y sin imagen en GHCR** | El núcleo no es «entregable» hasta que exista el tag | Orlando | Tag desde `main` actualizado y revisar la corrida Release (pasos 3 a 7 de la verificación) |
| **Project desfasado** | Criterio 5 | Orlando o Evelyn con permiso | Mover tarjetas de #141, #142 y #143 y corregir las iteraciones |
| **Backend de Lighthouse en 59 de 80** (RNF008) | Limitación declarada, no un error oculto | Equipo | Se informa como limitación; se mide en el servidor real |
| **RNF001 (tres navegadores y móvil) y RNF011 (disponibilidad en el tiempo) sin medir** | No hay evidencia, solo diseño | Equipo | Se declaran pendientes |
| **Límites de la infraestructura:** certificado autofirmado, sin VM en la nube, promoción de la réplica y *cron* de respaldos sin hacer, `enforce_admins` desactivado | Se presentan como limitaciones, no como cumplidos | Equipo | Documentados en 5.9, 5.11 y 5.15 |
| **Review y retro del S3 sin la decisión del PO** | Falta cerrar el sprint | Evelyn | Decisión escrita en `docs/scrum/sprint-3/review.md` |

**Hasta que se fusione `main` y exista el tag, el criterio 1 no está cumplido del todo.** Orlando lo hace en paralelo a este informe; el equipo decide con ese conocimiento (ver la recomendación).

## 3. Desviaciones aceptadas por el equipo (no cumplidas)

Decisión del 23/11/2026 ([`decisiones-2026-11-23.md`](decisiones-2026-11-23.md), decisión 4). Quedan **después del Sprint 4, dentro del Cierre**. **No se presentan como cumplidas.**

| Desviación | Criterio que toca | Qué queda en su lugar | Cierre previsto |
|---|---|---|---|
| **HU-30:** usabilidad con 5 personas y SUS | 1 y 3 | Plan, cuestionario SUS y script de cálculo listos (#195); RNF003 en «Parcial»; **no hay ninguna medición** | Cierre (Evelyn; Orlando revisa el plan) |
| **Demo cruzada** | Retro del S2 y R4 | Guion en [`demo_cruzada.md`](../sprint-2/demo_cruzada.md) | Cierre (Evelyn y Orlando) |
| **Video de la demo** | 2 | Evidencia alternativa por flujo: pruebas de integración y capturas | Cierre (Evelyn y Orlando) |

## 4. Recomendación

**Recomiendo iniciar M1, `donofrio_calidad`, y luego seguir el orden fijo:** M1 calidad, M2 heladeros, M3 cadena de frío, M4 tablero. Se avanza **uno a uno**, con mini gate al terminar cada módulo.

Según los tres criterios de decisión de [04 §4.3](../../plan/04_scrum_pmbok.md) (no por horas):

1. **La Fase 1 cumple sus criterios de salida, salvo lo anterior.** Lo que falta (`main` y tag) es de Orlando y se hace en paralelo. Si el criterio 1 no se cierra, se termina eso primero; por eso **recomiendo que M1 se cree desde `develop` y no se fusione hasta que `main` y el tag estén listos**, para no mezclar ambos cierres.
2. **M1 se puede terminar y documentar antes de la hora de corte** (jueves 26/11/2026, 08:00). Es el primero del orden fijo, el que más peso tiene (Calidad es Enterprise, no hay alternativa de Community) y respalda ISO 9001 y HACCP. Cubre RF011 y RF012, con diseño ya hecho (CU006, wireframe y mockup).
3. **Lo que no cumpla su DoD de módulo a la hora de corte no se fusiona:** queda como «Diseñado – trabajo futuro» con su CU, wireframe y mockup.

**M2, M3 y M4 no se recomiendan todavía como módulos confirmados.** Siguen en el plan y se deciden **uno por uno en el mini gate del módulo anterior**, según si el siguiente se puede terminar y documentar antes de la hora de corte. M3 depende de M1.

Riesgo principal: la Fase 2 completa en poco más de dos días (R1 y R17 en [07](../../plan/07_riesgos_entrega.md)). La red de seguridad es la hora de corte, no un cambio de plazo; el Cierre no se toca.

## 5. Pregunta al equipo

> **¿Confirman iniciar M1 `donofrio_calidad`?** (respuesta de Evelyn u Orlando)

La decisión se registra:

- en un comentario en el issue #143, y
- con el mensaje explícito de Evelyn u Orlando en el chat de Claude («Confirmo iniciar M1 donofrio_calidad»), **que es lo que activa el módulo**. Ningún archivo lo reemplaza.

**Estado de la decisión:** pendiente. No se ha iniciado ningún módulo de la Fase 2.
