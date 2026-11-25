# Sprint 4 (Módulos propios, Fase 2): Review

**Fecha:** 25/11/2026 · **Facilita:** Orlando (SM) · **PO:** Evelyn · **Estado:** acta preparada con lo que quedó fusionado en `develop` y `main`; todo sale de los PR, los issues, los mini gates y las capturas del repositorio.

## Objetivo

«Agregar M1, M2, M3 y M4, uno a uno, con mini gate.»

**Resultado: cumplido.** Los cuatro módulos propios están fusionados y publicados, cada uno con su mini gate, su sección en el informe (5.5b a 5.5e) y sus capturas. El Project cuenta **34 de 40 puntos**: faltan los 3 de HU-21 (su PR está fusionado y su casilla de la épica sigue sin marcar) y los 3 de la opcional HU-31 (landing), que no entró al sprint.

## Incremento mostrado

| Módulo | HU | PR | Release | Resultado |
|---|---|---|---|---|
| **M1** `donofrio_calidad` | HU-17 (inspecciones por puntos de control ligadas a la OP y al lote), HU-18 (certificado de calidad en PDF) | #219, #220, #221 (mini gate) | `v1.1.0` | Listo (Orlando). Un lote rechazado no se despacha ni por transferencia ni por el punto de venta |
| **M2** `donofrio_heladeros` | HU-20 (liquidación diaria), HU-21 (PDF de la liquidación) | #223, #225 (mini gate) | `v1.2.0` | Listo (Evelyn). La liquidación se liga a un pedido de venta y se imprime para firmar |
| **M3** cadena de frío (dentro de `donofrio_calidad`) | HU-19 (lecturas de temperatura, rangos por ubicación, alertas y *cron* de lotes por vencer) | #226 | `v1.3.0` | Listo (Orlando) |
| **M4** `donofrio_tablero` y marca | HU-22 (tablero gerencial OWL), HU-24 (marca visual del backend) | #227, #228 | `v1.4.0` | Listo (Evelyn). Lighthouse del tablero: 76 en escritorio y LCP de 2.11 s (cumple los 3 s) |

Lo que cerró el sprint fuera de los módulos:

| Entregable | PR | Qué dejó |
|---|---|---|
| Gate 0 y `v1.0.0` verificados, ER y diccionario con M1, ISO 9001/HACCP, traducciones `.po` y prueba del punto de venta | #222, #224 | El núcleo publicado como `v1.0.0` y la documentación al día con el primer módulo |
| Fusión de la Fase 2 en `main` y publicación de `v1.4.0` | #229 | Los cuatro módulos en `main`; las *releases* `v1.1.0` a `v1.4.0` con su imagen en GHCR y su zip |
| HU-16: demostración completa de las vistas | #230 | 188 inspecciones con sus certificados, 124 liquidaciones cuadradas con sus pedidos, 896 lecturas de temperatura con 7 alertas, 26 oportunidades de CRM, contactos con datos peruanos, 17 tickets y 45 reuniones |
| Revisión pantalla por pantalla de la demostración | #230 | Se corrigió el error 403 del certificado para el administrador, los textos en inglés y las fechas y plazos fuera de la ventana de datos (3/8 al 22/11) |
| Capturas en PNG de 1600 × 900 con datos de demostración | #231 | Las capturas de M1 a M4 se rehicieron con la demostración completa |
| Contenido final del informe con la Fase 2 | #232 | Secciones 1 a 10 con los cuatro módulos y sus límites |
| Informe sobre la plantilla del docente | #233 | Informe armado con índices, leyendas numeradas y historial de revisiones |

**Medidas del sprint** (corridas del 24 y 25/11/2026 sobre una PC con datos de demostración): **218 pruebas automáticas** en verde en el CI (137 de `donofrio_base`, 45 de `donofrio_calidad`, 15 de `donofrio_heladeros` y 21 de `donofrio_tablero`); 82 PR fusionados en total; cinco *releases* (`v1.0.0` a `v1.4.0`).

## Cómo se demuestra

1. Calidad › Inspecciones: una inspección rechazada con su motivo y el certificado en PDF de una aprobada (M1).
2. Calidad › Cadena de frío: una lectura fuera de rango con su alerta (M3).
3. Heladeros › Liquidaciones: una liquidación liquidada con su pedido y el PDF (M2).
4. Tablero › Gerencia: las seis tarjetas, el filtro por almacén y el aviso de «sin permiso» con el vendedor (M4).

## Pendiente y deuda técnica

- **HU-21:** la casilla de la épica #145 sigue sin marcar aunque su PR está fusionado; la actualiza Orlando.
- **HU-31 (landing opcional):** no empezó; se necesita la confirmación explícita de Evelyn u Orlando.
- **Rendimiento web:** el tablero propio saca 76 y el backend 59 frente a la meta de 80; es el costo del JavaScript del cliente web de Odoo y se declara como límite conocido.
- **Project:** el *workflow* «Item closed» sigue desactivado y varias tarjetas se actualizan a mano.

## Decisión del PO

Cada módulo tuvo su decisión explícita en su mini gate; el incremento completo (M1 a M4, `v1.1.0` a `v1.4.0`) se presenta al PO en esta Review.
