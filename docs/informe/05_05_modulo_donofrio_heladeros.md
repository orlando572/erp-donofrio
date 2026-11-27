# 3.1.4.3 Módulo de Liquidación de heladeros (M2)

El heladero es un concesionario: compra al precio de la lista «Heladero» (25 % de descuento supuesto) y liquida cada día. El módulo de Liquidación de heladeros (`donofrio_heladeros`, M2; HU-20 y HU-21; RF004; CU004) reemplaza el papel y el Excel de esa liquidación. Se publicó en la versión v1.2.0 y se apoya en la configuración base y en Ventas e Inventario de Odoo.

**Qué hace.** El liquidador abre una liquidación por heladero y fecha (una por día, solo para contactos con la etiqueta «Heladero concesionario») y registra por producto lo despachado, devuelto y la merma. El sistema calcula lo vendido, el importe a precio de heladero, la comisión y la diferencia de efectivo; al confirmar, crea y confirma el pedido de venta con lo vendido, que sigue el flujo estándar (entrega con FEFO y factura o boleta), y permite imprimir el PDF con las firmas del heladero y del liquidador.

**Datos y cálculos.** La liquidación (cabecera, con estados y totales) y sus líneas, una por producto. La liquidación pasa de Borrador a Despachado (exige al menos un producto) y a Liquidado (exige al menos una unidad vendida; ya no vuelve a borrador).

| Cálculo | Fórmula |
|---|---|
| Vendido | despachado − devuelto − merma (se rechaza si devuelto + merma supera lo despachado) |
| Importe de la línea | vendido × precio de la lista «Heladero» a la fecha |
| Comisión | importe vendido × porcentaje (10 % supuesto, editable) |
| Diferencia de efectivo | efectivo entregado − importe vendido (positiva: entregó de más; negativa: debe la diferencia) |

El pedido usa solo lo vendido: la mercadería devuelta no sale del almacén y la merma no se factura. El liquidador crea y modifica liquidaciones, la jefatura de heladeros además las borra y los vendedores solo las consultan.

![Liquidación confirmada con su pedido de venta](../capturas/sprint-4/HU-20_liquidacion_confirmada_con_pedido.png)

*Figura 5.5c-a. Liquidación LIQ/2026/00124 en estado Liquidado, con su pedido de venta ligado (datos de demostración).*

**Pruebas.** El módulo tiene 15 pruebas sin errores: cálculos, rechazo de cantidades inválidas, una liquidación por día, flujo completo con su pedido, estados, permisos y PDF. En la pantalla se verificaron la liquidación despachada y la confirmada, la lista con totales y el PDF con las firmas, que acompaña a la factura o boleta del pedido.
