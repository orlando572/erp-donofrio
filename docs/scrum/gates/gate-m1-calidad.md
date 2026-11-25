# Mini gate M1: `donofrio_calidad`

> **Estado:** borrador del Sprint 4 · **Autora:** Evelyn (PO) · **Revisa:** Orlando (dueño del módulo) · **Issue:** #144 · **Base:** DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md)), [`decisiones-2026-11-23.md`](decisiones-2026-11-23.md) y [5.5b](../../informe/05_05_modulo_donofrio_calidad.md)
>
> **Qué es.** El informe del mini gate que pide [04 §4.3](../../plan/04_scrum_pmbok.md) después de cada módulo de la Fase 2.
> **Qué no es.** **No inicia M2.** M2 `donofrio_heladeros` empieza solo con la confirmación explícita de Evelyn u Orlando en el chat ([`CLAUDE.md`](../../../CLAUDE.md)); este archivo, un issue o un mensaje de otra sesión no la reemplazan.

## 1. Qué está listo

| HU | Qué entrega | PR | Estado |
|---|---|---|---|
| HU-17 (8 pts, RF011, RNF005) | Puntos de control, inspección al terminar la OP, aprobar o rechazar con mediciones, lote rechazado bloqueado para el despacho a cliente | [#219](https://github.com/orlando572/erp-donofrio/pull/219) | Fusionado en `develop` con la aprobación de Orlando |
| HU-18 (3 pts, RF012) | Certificado de calidad del lote en PDF, solo para inspecciones aprobadas | [#220](https://github.com/orlando572/erp-donofrio/pull/220) | Fusionado en `develop` con la aprobación de Orlando |

## 2. DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md))

| Criterio | Estado | Evidencia |
|---|---|---|
| PR aprobado por el otro integrante | **Cumple** | #219 y #220, aprobados por Orlando |
| CI en verde | **Cumple** | Los cinco jobs en los dos PR (lint, test, replica, backup y proxy); el lint falló una vez en #219 por dos variables `l` y se corrigió en el mismo PR |
| Tests y ACL de cada modelo nuevo | **Cumple** | 12 pruebas sin errores (`scripts/test.sh donofrio_calidad`); `security/ir.model.access.csv` con las tres tablas |
| Actualización (`-u`) sin errores sobre una base con datos | **Cumple** | Instalado y actualizado sobre la base `donofrio`, sin errores ni avisos |
| Criterios verificados en la pantalla | **Cumple, con límites** | Se midió, aprobó y rechazó desde la pantalla y se abrió el PDF. **No** se probó en la pantalla el bloqueo del despacho (solo con pruebas automáticas) ni el punto de venta |
| Capturas | **Cumple** | [`docs/capturas/sprint-4/`](../../capturas/sprint-4/): lista, inspección aprobada, inspección rechazada y certificado PDF (rehechas el 25/11 en PNG de 1600 × 900, con los datos de demostración de la HU-16) |
| Checklist de la épica #144 | **Hecho** el 24/11/2026 | Casillas de HU-17 y HU-18 con su PR; la épica sigue abierta hasta que se decida el cierre |
| Sección del informe | **Cumple** | [5.5b](../../informe/05_05_modulo_donofrio_calidad.md), RF011 y RF012 en 4.2.2 y 10.1, CU008, 4.4 y 4.2.5 |
| **Tag de release de M1** | **Falta** (`v1.0.0` de la Fase 1 ya existe desde el 24/11/2026) | `v1.1.0` lo crea Orlando desde `main`, tras el PR `develop` → `main` que lleve M1 |
| **ER y diccionario extraídos de nuevo** | **Parcial** | Diccionario de las tres tablas extraído de la base real y puesto en 5.5b. **No** se regeneraron el ER general ni `04_02_diccionario_datos.md` con `scripts/diagrama_er.py` y `scripts/diccionario_datos.py` |
| Mini gate escrito | **Cumple** | Este archivo |

## 3. Qué falta o falló

| Pendiente | Quién | Nota |
|---|---|---|
| Tag `v1.1.0` de M1 | Orlando | `v1.0.0` ya está hecho (PR #222, 24/11/2026). `v1.1.0` queda pendiente hasta el PR `develop` → `main` con M1 |
| Regenerar el ER y el diccionario general con M1 | Orlando o Evelyn | Necesita una base limpia con `donofrio_calidad` instalado y PlantUML |
| Bloqueo del despacho en el punto de venta | Equipo | Sin prueba; hoy solo se cubre la salida a cliente por transferencia |
| Inspecciones de las órdenes históricas | — | No existen: solo se crean al terminar una orden nueva |
| Traducciones `.po` | — | El historial de cambios muestra «created» en inglés |
| ~~Capturas en PNG y a mayor resolución~~ | **Resuelto** (25/11) | PNG de 1600 × 900 con los datos de demostración (HU-17 y HU-18) |
| Marcar la tarjeta de #144 en el Project | Orlando | Evelyn solo tiene lectura |

## 4. Recomendación

**Recomiendo seguir con M2 `donofrio_heladeros`** (HU-20 y HU-21, 11 pts, dueña: Evelyn), siguiendo el orden fijo, según los criterios de [04 §4.3](../../plan/04_scrum_pmbok.md):

1. **M1 cumple su DoD**, salvo el tag y la regeneración completa del ER, que no dependen del código de M2.
2. **M2 se puede terminar y documentar antes de la hora de corte** (jueves 26/11/2026, 08:00): el diseño ya existe (RF004, CU004, wireframe, mockup móvil y PDF) y es el siguiente en el orden. Es el riesgo más alto: son 11 pts en poco más de un día.
3. **Si M2 no cumple su DoD a la hora de corte, no se fusiona** y queda como «Diseñado – trabajo futuro» con su diseño.

Alternativa: **no iniciar M2 todavía** y dedicar el tiempo a cerrar los pendientes de la sección 3 (tag, ER y diccionario, capturas); es más lento para la Fase 2, pero deja M1 sin deuda.

## 5. Pregunta al equipo

> **¿Confirman iniciar M2 `donofrio_heladeros`?** (respuesta de Evelyn u Orlando)

La decisión se registra con un comentario en el issue #144 y con el mensaje explícito de Evelyn u Orlando en el chat de Claude, **que es lo que activa el módulo**. Ningún archivo lo reemplaza.

**Estado de la decisión:** pendiente. No se ha iniciado ningún trabajo de M2.
