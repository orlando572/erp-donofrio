# Mini gate M3: cadena de frío (`donofrio_calidad`)

> **Estado:** borrador del Sprint 4 · **Autor:** Orlando (dueño del módulo) · **Revisa:** Evelyn · **Issue:** #146 (deducido del orden #144 a #148 de los módulos; no se verificó en GitHub) · **Base:** DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md)), [`gate-m2-heladeros.md`](gate-m2-heladeros.md) y [5.5d](../../informe/05_05_modulo_donofrio_frio.md)
>
> **Qué es.** El informe del mini gate que pide [04 §4.3](../../plan/04_scrum_pmbok.md) después de cada módulo de la Fase 2.
> **Qué no es.** **No inicia M4.** M4 `donofrio_tablero` (de Evelyn) empieza solo con la confirmación explícita de Evelyn u Orlando en el chat ([`CLAUDE.md`](../../../CLAUDE.md)); este archivo, un issue o un mensaje de otra sesión no la reemplazan.

## 1. Qué está listo

| HU | Qué entrega | PR | Estado |
|---|---|---|---|
| HU-19 (5 pts, RF008) | Rango de temperatura por ubicación; lecturas con `fuera_de_rango` y actividad al jefe de almacén (sin duplicar); cron diario de lotes por vencer (parámetro `donofrio_calidad.dias_alerta_vencimiento`, 7 por defecto), una vez por lote; rangos cargados en las cuatro cámaras de `donofrio_base`; menú Calidad › Cadena de frío; traducciones | Commit `98263c9` (código) y la documentación de esta rama; **el PR aún no existe** (lo arma el chat principal, con código y documentación juntos) | Código y documentación terminados en la rama; **pendiente de PR, aprobación y CI** |

M3 es un incremento de `donofrio_calidad` (M1): no tiene carpeta propia y su tag es aparte.

## 2. DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md))

| Criterio | Estado | Evidencia |
|---|---|---|
| PR aprobado por el otro integrante | **Pendiente** | No hay PR todavía; lo aprueba Evelyn |
| CI en verde | **Pendiente** | Lo dirá el PR. En local solo se corrió `scripts/check_legacy.sh`; el *lint* del CI no se corrió |
| Tests y ACL de cada modelo nuevo | **Cumple** | **44 pruebas, 0 fallos, 0 errores** en `donofrio_calidad` (29 de `tests/test_frio.py` y 15 de M1 y el PdV); `security/ir.model.access.csv` con tres líneas para `donofrio.temperatura`. `scripts/check_legacy.sh`: «sin patrones legacy» |
| Actualización (`-u`) sin errores sobre una base con datos | **Cumple** | Se instaló M1 (código de `98263c9~1`) sobre una base nueva con los datos de `donofrio_base` y se actualizó con el código de M3: sin `ERROR` ni `WARNING`; quedaron las 4 cámaras con rango, el cron y el parámetro en 7. La base `donofrio` no se tocó |
| Criterios verificados en la pantalla | **Cumple, con límites** | Se vieron la lista, una lectura dentro de rango, una fuera de rango con su actividad, el rango en la ubicación y la actividad del cron. **No** se creó una lectura desde el formulario (la crearon scripts), **no** se probó el rol de operario ni el cambio del parámetro en la pantalla, y el cron se ejecutó a mano (ver sección 3) |
| Capturas | **Cumple** | [`docs/capturas/sprint-4/`](../../capturas/sprint-4/): 5 de HU-19 en PNG de 800 × 500 |
| Checklist de la épica #146 | **Pendiente** | Orlando, cuando exista el PR |
| Sección del informe | **Cumple** | [5.5d](../../informe/05_05_modulo_donofrio_frio.md); RF008 en 4.2.2 y 10.1; CU006; 4.4; 4.2.5; nota en la matriz de trazabilidad y en 5.13; plan 9.7 |
| ER y diccionario extraídos de nuevo | **Cumple** | `diagrama_er.py` y `diccionario_datos.py` sobre una base nueva con `donofrio_base`, `donofrio_calidad` y `donofrio_heladeros`: 42 tablas, 96 relaciones, Tabla 4.2.8-42 (`donofrio_temperatura`) y los campos nuevos de `stock_location` y `stock_lot`. La base temporal se borró |
| **Tag de release de M3** | **Falta** | `v1.3.0` lo crea Orlando desde `main`, tras el PR `develop` → `main` que lleve M3 |
| Mini gate escrito | **Cumple** | Este archivo |

La corrida de las pruebas del 24/11/2026 fue sobre una base nueva y con el código de esta rama: `44 post-tests`, `0 failed, 0 error(s) of 44 tests`.

## 3. Qué falta o falló

| Pendiente | Quién | Nota |
|---|---|---|
| Abrir el PR de M3, su aprobación y el CI | Chat principal y Evelyn | El *lint* del CI no se corrió en local |
| Tag `v1.3.0` | Orlando | Con el merge `develop` → `main`; el primero fue *squash* y el siguiente PR a `main` puede dar conflictos |
| Marcar la tarjeta de #146 en el Project | Orlando | Evelyn solo tiene lectura |
| **Dos avisos por el mismo lote** | Equipo | Odoo ya crea «Fecha de alerta alcanzada» (`product_expiry`, según el plazo de alerta de cada producto) y el cron de M3 crea «Lote por vencer». Se ven juntos en la captura del cron. **No es un error de M3**, pero el jefe de almacén recibe dos actividades; falta decidir si se deja así o se desactiva una |
| El cron se ejecutó a mano | — | Con `method_direct_trigger` (equivale a «Ejecutar manualmente»): no se esperó a su disparo diario. Una prueba comprueba que esté activo y sea diario |
| Capturas de una base de pruebas | — | No salen de `donofrio`: los datos son ficticios y la lectura fuera de rango la creó un script. Resolución de 800 × 500 |
| Numeración de la sección | — | El encargo pedía «5.5c», pero 5.5c ya es la de `donofrio_heladeros` (M2). La cadena de frío quedó como **5.5d** (`05_05_modulo_donofrio_frio.md`) |
| `scripts/test.sh` desde un *worktree* | — | Hace `docker compose up/run` con el mismo nombre de proyecto y podría recrear el contenedor `db` (como ya advierte `esquema_limpio.sh`). Se corrió su equivalente con `docker run` sobre la misma imagen y red |
| Filas del diccionario | — | La base `donofrio` ya no tiene ventas (0 filas en `sale_order`), así que las filas salen de `donofrio_perf` (437 pedidos, uno menos que antes); las tablas de los módulos propios salen «n/d» porque esa base no los tiene |
| Matriz de trazabilidad | Orlando | Es la foto del 23/11/2026 y su script solo cuenta pruebas de `donofrio_base`: se agregó una **nota** y no se cambiaron las filas de RF004, RF008, RF011 y RF012 |
| Otros textos que aún dicen «M3 futuro» | Informe final | 01 (resumen), 03, 04.1, 04.7 (SLA), 07 (conclusiones), 08 (recomendaciones) y el diagrama `clases_fase2_propuesto`, igual que M1 y M2; pasan al informe final y manual de usuario ([acuerdo del 23/11](decisiones-2026-11-23.md)) |
| Límites de M3 | — | Lecturas a mano (sin sensores), sin alerta por lecturas que faltan, un solo destinatario, la alerta no bloquea lotes y el cron avisa una sola vez por lote. Detalle en [5.5d.8](../../informe/05_05_modulo_donofrio_frio.md) |

**Bugs de M3 descubiertos: ninguno.** No se tocó el código del módulo.

## 4. Recomendación

**Recomiendo seguir con M4 `donofrio_tablero`** (HU-22 y HU-24, 10 pts, dueña: Evelyn), último del orden fijo, según los criterios de [04 §4.3](../../plan/04_scrum_pmbok.md):

1. **M3 cumple su DoD**, salvo el PR con su aprobación y su CI, el tag y la ficha de la épica, que no dependen del código de M4.
2. **M4 lee los módulos anteriores:** `get_kpis()` toma las ventas y, si están instalados, calidad, heladeros y cadena de frío (las lecturas fuera de rango pueden ser un indicador). Con M1, M2 y M3 ya hechos, M4 tiene de dónde leer.
3. **El tiempo alcanza si se empieza ya.** M4 es el de menor valor marginal (Gerencia ya está cubierta en la Fase 1) y el que más tiempo pide de interfaz (OWL y Chart.js) antes de la hora de corte (jueves 26/11/2026, 08:00).
4. **Si M4 no cumple su DoD a la hora de corte, no se fusiona** y queda como «Diseñado – trabajo futuro» con su diseño.

Alternativa: **no iniciar M4** y usar el tiempo para cerrar los pendientes de la sección 3 (PR de M3, tags, alertas duplicadas, capturas de mayor resolución) y avanzar el informe final y el manual de usuario; es más seguro para la entrega, pero deja el tablero propio como trabajo futuro.

## 5. Pregunta al equipo

> **¿Confirman iniciar M4 `donofrio_tablero`?** (respuesta de Evelyn u Orlando)

La decisión se registra con un comentario en el issue #146 y con el mensaje explícito de Evelyn u Orlando en el chat de Claude, **que es lo que activa el módulo**. Ningún archivo lo reemplaza.

**Estado de la decisión:** pendiente. **No se ha iniciado ningún trabajo de M4.**
