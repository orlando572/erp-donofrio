# 5.5c Documentación del módulo `donofrio_heladeros` (M2)

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn (dueña del módulo) · **Revisa:** Orlando · **Fuente:** `addons/donofrio_heladeros/` en `develop` (HU-20 en el PR #223; HU-21 y el cierre del módulo en el PR #225; release [`v1.2.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.2.0), mini gate en [`gate-m2-heladeros.md`](../scrum/gates/gate-m2-heladeros.md)), la base de desarrollo `donofrio` y las capturas de [`docs/capturas/sprint-4/`](../capturas/sprint-4/)
>
> Complementa 5.5 (`donofrio_base`) y 5.5b (`donofrio_calidad`). Las dos tablas del módulo **ya están** en el ER general ([4.2.6](04_02_modelo_de_datos.md), 41 tablas) y en el diccionario ([4.2.8, Tablas 40 y 41](04_02_diccionario_datos.md)); aquí solo se explica cómo funcionan.

## 5.5c.1 Qué hace

El heladero es un **concesionario** (supuesto S4): compra al precio de la lista «Heladero» (25 % de descuento supuesto) y liquida cada día. M2 (HU-20 y HU-21; RF004; CU004) reemplaza el papel y el Excel:

1. El liquidador abre una **liquidación por heladero y fecha** y registra por producto lo **despachado, devuelto y la merma**.
2. El sistema calcula el **vendido** (despachado − devuelto − merma), el **importe** a precio de heladero, la **comisión** y la **diferencia de efectivo**.
3. Al confirmar, crea y **confirma el pedido de venta** con lo vendido, que sigue el flujo estándar (entrega con FEFO y factura o boleta).
4. Imprime el **PDF** de la liquidación con las firmas del heladero y del liquidador.

## 5.5c.2 Archivos

| Ruta (`addons/donofrio_heladeros/`) | Contenido |
|---|---|
| `__manifest__.py` | Depende de `donofrio_base`, `sale` y `stock`; módulo con aplicación (menú «Heladeros») |
| `models/liquidacion.py` | `donofrio.liquidacion` y `donofrio.liquidacion.linea`: cálculos, validaciones, estados y pedido de venta |
| `models/report_liquidacion.py`, `report/liquidacion_report.xml` | Reporte QWeb del PDF; error si la liquidación está en borrador |
| `security/` | Grupos `Heladeros: liquidador` y `Heladeros: jefatura` y `ir.model.access.csv` |
| `data/heladeros_data.xml` | Secuencia `LIQ/año/` y asigna el grupo al usuario Liquidador de `donofrio_base` |
| `views/liquidacion_views.xml` | Lista, formulario, búsqueda, acción y menú |
| `tests/test_liquidacion.py` | 15 pruebas |

## 5.5c.3 Estados, cálculos y reglas

| Estado | Cómo se llega | Qué permite |
|---|---|---|
| Borrador | Al crear | Editar heladero, fecha y productos; «Marcar despachado» (exige al menos un producto) |
| Despachado | «Marcar despachado» | «Confirmar liquidación», «Volver a borrador» e «Imprimir» |
| Liquidado | «Confirmar liquidación» (exige al menos una unidad vendida) | Solo consulta e «Imprimir»; ya no vuelve a borrador |

| Cálculo | Fórmula |
|---|---|
| Vendido | despachado − devuelto − merma (nunca negativo: se rechaza si devuelto + merma supera lo despachado) |
| Importe de la línea | vendido × precio de la lista «Heladero» a la fecha (el precio se muestra con tres decimales: 1.125) |
| Comisión | importe vendido × porcentaje de comisión |
| Diferencia de efectivo | efectivo entregado − importe vendido. **Positiva:** el heladero entregó de más (a su favor). **Negativa:** entregó de menos y debe la diferencia |

- **Comisión del 10 %:** valor **supuesto**, tomado del mockup (204.00 → 20.40) y aceptado por Evelyn el 24/11/2026. Se puede cambiar en cada liquidación.
- **Una liquidación por heladero y día** (restricción `UNIQUE`), y solo para contactos con la etiqueta «Heladero concesionario».
- **El pedido de venta usa solo lo vendido.** La mercadería devuelta nunca sale del almacén del sistema y la merma no se registra como salida de inventario ni se factura. Es el alcance de M2; modelar la merma como ajuste de inventario sería un cambio aparte.
- **El liquidador** queda registrado en cada liquidación (por defecto, quien la crea) y sale en el PDF.

## 5.5c.4 Seguridad

| Grupo | Puede |
|---|---|
| Vendedores (`sales_team.group_sale_salesman`) | Solo leer liquidaciones |
| `Heladeros: liquidador` (incluye vendedor) | Crear y modificar liquidaciones y sus líneas |
| `Heladeros: jefatura` | Todo lo anterior, más borrar liquidaciones |

Un usuario sin esos grupos (por ejemplo, el comprador) recibe `AccessError` (prueba `test_permisos_del_liquidador_y_de_un_usuario_sin_grupo`). El usuario de prueba «Liquidador de Heladeros (CD Arequipa)» recibe el grupo de liquidador al instalar el módulo.

## 5.5c.5 Pruebas y evidencia

`scripts/test.sh donofrio_heladeros`: **15 pruebas, sin errores** (vendido, precio de la lista «Heladero», comisión y diferencia, rechazo de devuelto + merma mayor que lo despachado y de cantidades negativas, una liquidación por día, flujo completo con su pedido confirmado, estados no permitidos, permisos, y el PDF en despachada, con deuda y en borrador).

Verificado en la pantalla de Odoo (base `donofrio`, usuario Liquidador, con los datos de demostración de la HU-16; PNG de 1600 × 900, tomados el 25/11/2026):

| Qué se verificó | Captura |
|---|---|
| Liquidación despachada (LIQ/2026/00126) con vendido, importe, comisión y diferencia de efectivo | [`HU-20_liquidacion_despachada.png`](../capturas/sprint-4/HU-20_liquidacion_despachada.png) |
| Liquidación confirmada (Liquidado) (LIQ/2026/00124) con su pedido de venta S00435 | [`HU-20_liquidacion_confirmada_con_pedido.png`](../capturas/sprint-4/HU-20_liquidacion_confirmada_con_pedido.png) |
| Lista de liquidaciones con totales | [`HU-20_lista_liquidaciones.png`](../capturas/sprint-4/HU-20_lista_liquidaciones.png) |
| Precio con tres decimales (LIQ/2026/00122) y el importe que cuadra | [`HU-20_liquidacion_precio_3_decimales.png`](../capturas/sprint-4/HU-20_liquidacion_precio_3_decimales.png) |
| Error de validación al devolver y mermar más de lo despachado (captura de la primera entrega, en JPG: reproducirla exige crear una liquidación, y la HU-16 pidió no tocar los datos) | [`HU-20_error_devuelto_mas_merma.jpg`](../capturas/sprint-4/HU-20_error_devuelto_mas_merma.jpg) |
| Formulario con el botón «Imprimir» y el campo Liquidador | [`HU-21_formulario_con_imprimir_y_liquidador.png`](../capturas/sprint-4/HU-21_formulario_con_imprimir_y_liquidador.png) |
| PDF de LIQ/2026/00124 con el detalle, el efectivo y las firmas | [`HU-21_pdf_liquidacion.png`](../capturas/sprint-4/HU-21_pdf_liquidacion.png) |

## 5.5c.6 Límites

- **La vista móvil no se probó en un celular real ni con una pantalla de ancho móvil** (**[PENDIENTE: prueba en un celular real, a cargo del equipo]**). El navegador de las pruebas no permite reducir el ancho de la ventana (la ventana no cambió de tamaño y Odoo no entró en modo móvil), y Odoo no deja incrustar sus páginas en un marco. Se usa el formulario responsive estándar de Odoo; las columnas de precio e importe se pueden ocultar con el selector de columnas de la lista (`optional="show"`). Una condición como `uiEnv.isSmall` no es válida en las vistas de Odoo 19 y se descartó.
- **Inventario:** el pedido solo mueve stock por lo vendido (la prueba de pantalla generó su entrega `LIM/PICK/00227` por 100 unidades). Ver 5.5c.3.
- **Las liquidaciones de las capturas y sus pedidos** son datos de demostración (HU-16) en la base de desarrollo, no en el repositorio; se tomaron solo con lectura. Su liquidador es el usuario «Liquidador de Heladeros (CD Arequipa)».
- **Filas del diccionario:** la columna «Filas» de 4.2.8 sale ahora de la base de desarrollo `donofrio` (la base `donofrio_perf` con la que se midió ya no existe) e incluye los datos de prueba de M1 y M2; por eso `sale_order` pasó de 437 a 438. Las cifras de 4.2.6 siguen citando `donofrio_perf`.
- **El PDF no valida stock ni comprobantes:** es un documento para firmar; no reemplaza a la factura o boleta del pedido.
- El módulo no trae traducciones `.po`: los textos de las vistas, los mensajes y el reporte están en español en el código.
