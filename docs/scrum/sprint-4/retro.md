# Sprint 4 (Módulos propios, Fase 2): Retrospectiva

**Fecha:** 25/11/2026 · **Facilita:** Orlando (SM)
**Estado:** acta de Orlando; Evelyn la confirma o la corrige. Todo sale de los PR, los issues, los mini gates y los commits reales del repositorio.

## Seguimiento de las acciones de la Retro del S3

| # | Acción | Resultado |
|---|---|---|
| 1 | Avisar al otro integrante antes de abrir un PR que toque `__manifest__.py`, `tests/__init__.py` o `ci.yml` | **Cumplida.** Cada módulo entró por su PR, uno a uno y en orden (M1 → M4) |
| 2 | Probar cada HU también en el entorno del CI | **Cumplida.** Los cuatro módulos pasan sus pruebas en el CI de cada PR (218 en total) |
| 3 | Marcar la checklist de la épica al fusionar | **Parcial.** Las épicas de M3 y M4 (#146 y #147) se cerraron; la de M2 (#145) quedó con la casilla de HU-21 sin marcar y la de M1 (#144) con su tarjeta en «Hecho» pero abierta |
| 4 | Dejar registrada la medición del tiempo de cada HU | **Parcial.** Las fechas reales salen de la fusión del último PR de cada HU (6.2), no de una hora de inicio |

## Qué salió bien

- **El orden fijo y los mini gates funcionaron.** Los cuatro módulos se hicieron entre el 24 y el 25/11, uno a uno, cada uno con su documentación, su mini gate y sus capturas en el mismo sprint; nada quedó a medias en `main`.
- **Los dueños por módulo repartieron la carga.** Orlando llevó M1 y M3, y Evelyn M2 y M4; cada PR lo aprobó el otro integrante.
- **Las verificaciones en pantalla encontraron errores que las pruebas no veían.** Ver la tabla de abajo.
- **La demostración completa (HU-16) dejó todas las vistas con datos creíbles** y reproducibles por código, de modo que las capturas se rehicieron en PNG de 1600 × 900 con datos reales de la demostración.
- **El informe se actualizó junto con el código:** cada módulo trajo su sección 5.5, sus fichas de requerimientos y sus capturas.

## Errores hallados al validar (y qué enseñan)

| Dónde | Qué pasó | Cómo se halló y se corrigió |
|---|---|---|
| **Tablero con el Inspector de Calidad (M4)** | El tablero falló con «Error de acceso» por las liquidaciones: una tarjeta de un módulo opcional podía romper todo el tablero | Al abrir el tablero con otro rol. Una tarjeta opcional solo sale si el usuario puede leer su modelo, con una prueba |
| **Jefe de Ventas y Vendedor ante el tablero (M4)** | Veían el menú y el tablero fallaba porque no leen lotes ni existencias | Revisión por roles del 24/11. Ahora reciben el aviso «Sin permiso», que dice qué falta y a quién pedirlo |
| **Inicio de sesión (M4)** | La pantalla de acceso y las ilustraciones de «sin datos» seguían en morado | Revisión de la marca el 24/11. Se pasaron a la marca amarilla |
| **Certificado de calidad con el administrador (M1)** | Imprimir el certificado daba un error 403 | Revisión pantalla por pantalla del 25/11. El administrador entra a los grupos de jefatura de calidad y de heladeros, con pruebas |
| **Datos de la demostración** | Textos en inglés y fechas y plazos fuera de la ventana de datos (3/8 al 22/11) | La misma revisión (HU-16, PR #230). Se llevaron a la ventana y se tradujeron |
| **Liquidaciones de la demostración** | Confirmar una liquidación habría creado otro pedido y duplicado la venta | Al cargar los datos. Las liquidaciones se marcan como liquidadas ligadas al pedido que ya existía |

## Empezar

- Revisar cada módulo **con cada rol** antes del mini gate, no solo con el gerente.
- Cargar la demostración completa **antes** de tomar las capturas, para no rehacerlas.
- Marcar la casilla de la épica en el mismo PR que cierra la HU.

## Dejar de hacer

- Dar por buena una pantalla porque la usa un solo rol.
- Dejar la actualización del Project para el final: varias tarjetas quedaron en «Backlog» con la épica cerrada.

## Continuar

- Un módulo a la vez, con pruebas, mini gate y capturas en el mismo sprint.
- Datos y configuración por código, y límites declarados con su evidencia (Lighthouse del tablero, sensores de temperatura).
- Una rama y un PR por HU, con `[HU-xx]` en el título y la aprobación del otro integrante.

## Acciones de mejora

| # | Acción | Responsable | Para cuándo |
|---|---|---|---|
| 1 | Marcar la casilla de HU-21 en la épica #145 y pasar a «Hecho» las tarjetas de #142, #146 y #147 | Orlando | Antes de la entrega |
| 2 | Activar el *workflow* «Item closed» del Project con el valor «Hecho» | Orlando | Antes de la entrega |
| 3 | Entregar el informe, los manuales y la presentación con margen antes del plazo (viernes 27/11, 14:30) | Evelyn (sube) y Orlando (verifica) | Cierre |

## Riesgos que cambian

| Riesgo | Hoy | Propuesta | Motivo |
|---|---|---|---|
| R1 Plazo | 3 × 3 = 9 Alta | Se mantiene hasta la entrega | La Fase 2 se terminó el 25/11, pero el plazo sigue siendo el viernes 27/11 a las 14:30 |
| R17 La Fase 2 deja un módulo a medias | Abierto | **Mitigado** | Los cuatro módulos se fusionaron completos, cada uno con su mini gate |
| R19 Sin Fase 2, un integrante sin código propio | Abierto | **Cerrado** | Cada integrante tiene dos módulos propios |
| R20 Fatiga | Abierto | Se mantiene hasta la entrega | Los cuatro módulos se hicieron en dos días y el Cierre sigue |
