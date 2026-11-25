# Mini gate M2: `donofrio_heladeros`

> **Estado:** borrador del Sprint 4 · **Autora:** Evelyn (PO y dueña del módulo) · **Revisa:** Orlando · **Issue:** #145 · **Base:** DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md)), [`gate-m1-calidad.md`](gate-m1-calidad.md) y [5.5c](../../informe/05_05_modulo_donofrio_heladeros.md)
>
> **Qué es.** El informe del mini gate que pide [04 §4.3](../../plan/04_scrum_pmbok.md) después de cada módulo de la Fase 2.
> **Qué no es.** **No inicia M3.** M3 (cadena de frío, de Orlando) empieza solo con la confirmación explícita de Evelyn u Orlando en el chat ([`CLAUDE.md`](../../../CLAUDE.md)); este archivo, un issue o un mensaje de otra sesión no la reemplazan.

## 1. Qué está listo

| HU | Qué entrega | PR | Estado |
|---|---|---|---|
| HU-20 (8 pts, RF004) | Liquidación diaria por heladero y fecha: despachado, devuelto, merma, vendido, importe, comisión (10 %, supuesto aceptado) y diferencia de efectivo; al confirmar crea y confirma el pedido de venta | [#223](https://github.com/orlando572/erp-donofrio/pull/223) | Fusionado en `develop` con la aprobación de Orlando |
| HU-21 (3 pts, RF004, RNF001) | PDF de liquidación con el detalle, el efectivo y las firmas, y el liquidador registrado en cada liquidación | PR de cierre de M2 | Pendiente de la aprobación de Orlando |

## 2. DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md))

| Criterio | Estado | Evidencia |
|---|---|---|
| PR aprobado por el otro integrante | **Cumple (HU-20); pendiente (HU-21 y cierre)** | #223 aprobado por Orlando |
| CI en verde | **Cumple (HU-20)**; el del PR de cierre lo dice el PR | Cinco jobs en verde en #223 |
| Tests y ACL de cada modelo nuevo | **Cumple** | 14 pruebas sin errores (`scripts/test.sh donofrio_heladeros`); `security/ir.model.access.csv` con las dos tablas |
| Actualización (`-u`) sin errores sobre una base con datos | **Cumple** | Instalado y actualizado varias veces sobre la base `donofrio`, sin errores ni avisos |
| Criterios verificados en la pantalla | **Cumple, salvo la vista móvil** | Crear, despachar, confirmar con pedido, error de cantidades, precio con tres decimales, botón «Imprimir» y PDF. **La vista móvil no se pudo probar** (ver sección 3) |
| Capturas | **Cumple** | [`docs/capturas/sprint-4/`](../../capturas/sprint-4/): 4 de HU-20 y 2 de HU-21 rehechas el 25/11 en PNG de 1600 × 900 con los datos de demostración de la HU-16 (queda en JPG `HU-20_error_devuelto_mas_merma`: reproducirla exige crear una liquidación) |
| Checklist de la épica #145 | **Parcial** | HU-20 y HU-21 enlazadas a su PR; queda sin marcar el criterio «vista móvil usable» de HU-21, así que la épica sigue abierta |
| Sección del informe | **Cumple** | [5.5c](../../informe/05_05_modulo_donofrio_heladeros.md); RF004 en 4.2.2 y 10.1; CU004; 4.4; 4.2.5 |
| ER y diccionario extraídos de nuevo | **Cumple** | `diagrama_er.py` y `diccionario_datos.py` con el área «Heladeros (M2)»: 41 tablas, 96 relaciones, Tablas 4.2.8-40 y 4.2.8-41 |
| **Tag de release de M2** | **Falta** | Lo crea Orlando desde `main`, con M1 |
| Mini gate escrito | **Cumple** | Este archivo |

## 3. Qué falta o falló

| Pendiente | Quién | Nota |
|---|---|---|
| Probar la vista móvil en un celular real o con una ventana de ancho móvil | Equipo | El navegador de las pruebas no cambió de tamaño la ventana y Odoo no deja incrustar sus páginas en un marco; se usa el formulario responsive estándar de Odoo |
| Merma e inventario | Equipo | El pedido solo mueve stock por lo vendido; la merma no se registra como salida (alcance declarado en 5.5c.3) |
| Tag de release de M2 | Orlando | Con el merge `develop` → `main`; el primero fue *squash* y `main` quedó con un solo commit, así que el siguiente PR a `main` puede dar conflictos |
| Marcar la tarjeta de #145 en el Project | Orlando | Evelyn solo tiene lectura |
| Filas del diccionario con datos de prueba | — | La columna sale de la base `donofrio` y no de `donofrio_perf` (ya no existe); difiere en una o dos filas por los datos de prueba |
| ~~Capturas en PNG y a mayor resolución~~ | **Resuelto** (25/11) | PNG de 1600 × 900 (HU-20 y HU-21). Única excepción: `HU-20_error_devuelto_mas_merma.jpg` (primera entrega), porque reproducir el error de validación exige crear datos |

## 4. Recomendación

**Recomiendo seguir con M3, cadena de frío** (HU-19, 5 pts, dueño: Orlando), según el orden fijo y los criterios de [04 §4.3](../../plan/04_scrum_pmbok.md):

1. **M2 cumple su DoD**, salvo el tag y la vista móvil, que no dependen del código de M3.
2. **M3 es el módulo más pequeño** y se construye sobre `donofrio_calidad` (M1, ya fusionado): rango de temperatura por ubicación, registro, actividad si está fuera de rango y *cron* de lotes por vencer. Se puede terminar y documentar antes de la hora de corte (jueves 26/11/2026, 08:00).
3. **Si M3 no cumple su DoD a la hora de corte, no se fusiona** y queda como «Diseñado – trabajo futuro» con su diseño.

Alternativa: no iniciar M3 todavía y probar primero la vista móvil de M2 en un celular real.

## 5. Pregunta al equipo

> **¿Confirman iniciar M3 cadena de frío?** (respuesta de Evelyn u Orlando)

La decisión se registra con un comentario en el issue #145 y con el mensaje explícito de Evelyn u Orlando en el chat de Claude, **que es lo que activa el módulo**. Ningún archivo lo reemplaza.

**Estado de la decisión:** pendiente. No se ha iniciado ningún trabajo de M3.
