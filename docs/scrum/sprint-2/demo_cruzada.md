# Sprint 2: Demo cruzada ([05 §5.1](../../plan/05_reparto_equipo.md))

**Fecha de preparación:** 23/11/2026 · **Quién demuestra:** Evelyn muestra una HU de Orlando (HU-14) y Orlando una de Evelyn (HU-15 o HU-10) · **Estado:** guion y verificación hechos; **falta repetirla en vivo con Orlando antes del Gate 0.**

## HU de Orlando que demuestra Evelyn: HU-14 (órdenes de producción)

**Criterio de aceptación:** la OP reserva insumos por FEFO; al producir se crea el lote con vencimiento; se calcula el costo.

### Guion (base con los datos de demostración cargados)

1. Fabricación → Órdenes de producción: abrir una orden hecha, por ejemplo `WH/MO/00188`.
2. Mostrar los componentes consumidos y el **lote reservado** de cada insumo; el lote es el que vence antes (FEFO).
3. Mostrar el **lote producido** y su fecha de vencimiento.
4. Abrir los asientos de valoración de la orden: costo FIFO de los insumos más las horas del centro de trabajo.
5. Comparar el costo unitario con el precio de venta: debe ser menor.

### Verificación hecha en la base de Evelyn (23/11/2026)

| Comprobación | Resultado |
|---|---|
| Órdenes de producción creadas y hechas | 188 de 188 |
| Lotes producidos con fecha de vencimiento | Sí (ejemplo: `WH/MO/00188` produjo el lote `P01-261119`, vence el 19/03/2027; `WH/MO/00187`, el lote `H07-261119`, vence el 19/11/2027) |
| Asientos de valoración publicados de las órdenes | Presentes (Orlando reporta 581 en total) |
| Lotes en stock ordenados por vencimiento | El primero en salir es el que vence antes |

La verificación fue una consulta a la base y la revisión de los datos, **no** una demostración en vivo ante Orlando; la prueba automática de la HU está en `tests/test_produccion.py`.

## HU de Evelyn que demuestra Orlando: HU-15 (factura y boleta con IGV)

1. Ventas → un pedido confirmado con un cliente con RUC → crear la factura: diario «Facturas», tipo (01), numeración `F`.
2. Repetir con un cliente con DNI: diario «Boletas», tipo (03), numeración `B`.
3. Comprobar el IGV: 100 paletas × S/ 1.50 con IGV incluido = base 127.12 + IGV 22.88 = S/ 150.00.
4. Imprimir el PDF; recordar la limitación: la plantilla estándar titula «Factura» a la boleta.

Alternativa: HU-10 (PdV): abrir sesión, vender, cobrar con boleta y cerrar la caja cuadrada.

## Qué queda por hacer

- [ ] Hacer las dos demos en vivo, cada una con el otro integrante mirando.
- [ ] Anotar aquí las observaciones que salgan y marcar esta lista.
