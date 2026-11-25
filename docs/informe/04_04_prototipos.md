# 4.4 Diseño de prototipos: wireframes y mockups

Los prototipos se hicieron con un generador propio en Python: es gratuito, deja el diseño versionado y revisable en un PR, y de una sola descripción de cada pantalla salen el wireframe y el mockup, de modo que no se desfasan. Los datos que aparecen en las pantallas son ficticios.

- **Wireframes (4.4.1).** Escala de grises y sin marca, para acordar la estructura: qué campos, tabla y acciones tiene cada pantalla. Hay uno por caso de uso.
- **Mockups (4.4.2).** Alta fidelidad con la paleta de marca: el **amarillo de los carritos** (`#F7C60A`, desde 1919) como color de acción y de cabecera, tinta oscura para el texto, y verde, rojo y azul solo para alertas.
- **Pantallas de la Fase 2.** Las de liquidación, inspección, temperaturas y tablero se diseñaron antes de implementarse y hoy tienen su pantalla real. Las pantallas estándar son una propuesta de cómo se vería Odoo configurado con la marca.
- **Vista móvil.** Solo la liquidación del heladero la necesita, porque el liquidador la usa de pie, junto al despacho.

**Tabla 4.22. Resumen de pantallas diseñadas**

| CU | Pantalla | Módulo de Odoo | Estado |
|---|---|---|---|
| CU001 | Embudo CRM por canal | CRM | Implementada (estándar) |
| CU002 | Cotización con lista de precios | Ventas | Implementada (estándar) |
| CU003 | Punto de venta con boleta | Punto de venta | Implementada (estándar) |
| CU004 | Liquidación diaria del heladero (y vista móvil) | Heladeros (M2) | Implementada; móvil revisada en 375 × 812 |
| CU005 | Recepción de insumos con lote y vencimiento | Inventario | Implementada (estándar) |
| CU006 | Registro de temperaturas de las cámaras | Cadena de frío (M3) | Implementada |
| CU007 | Orden de producción con lote | Fabricación | Implementada (estándar) |
| CU008 | Inspección de calidad del lote | Calidad (M1) | Implementada |
| CU009 | Tablero gerencial de KPI | Tablero (M4) | Implementada |
| CU010 | Análisis de ventas por línea, canal y temporada | Ventas | Implementada (estándar) |
| CU011 | Solicitud de cotización por regla mín./máx. | Compras | Implementada (estándar) |
| CU012 | Factura (01) o boleta (03) con IGV | Facturación | Implementada (estándar) |

## 4.4.1 y 4.4.2 Wireframes y mockups clave

Se muestran los de las pantallas propias más representativas: la liquidación diaria del heladero (CU004) y la inspección de calidad (CU008) con su wireframe y su mockup, y el tablero gerencial (CU009) con su mockup.

![Wireframe de la liquidación diaria del heladero](../diagramas/pantallas/wf_cu004_liquidacion.png)

*Figura 4.17. Wireframe de la liquidación diaria del heladero (CU004).*

![Mockup de la liquidación diaria del heladero](../diagramas/pantallas/mk_cu004_liquidacion.png)

*Figura 4.18. Mockup de la liquidación diaria del heladero (CU004).*

![Wireframe de la inspección de calidad del lote](../diagramas/pantallas/wf_cu008_inspeccion.png)

*Figura 4.19. Wireframe de la inspección de calidad del lote (CU008).*

![Mockup de la inspección de calidad del lote](../diagramas/pantallas/mk_cu008_inspeccion.png)

*Figura 4.20. Mockup de la inspección de calidad del lote (CU008).*

![Mockup del tablero gerencial de KPI](../diagramas/pantallas/mk_cu009_tablero.png)

*Figura 4.21. Mockup del tablero gerencial de KPI (CU009).*

**Decisiones de diseño.** Una acción principal por pantalla, en amarillo y a la izquierda, con las secundarias en blanco. La barra de estado muestra el ciclo del documento (borrador → confirmado → hecho), como en Odoo, para no cambiar los hábitos del usuario. Los colores de alerta siempre llevan un texto y el contraste cumple el mínimo de 4.5 (4.6.1). Las etiquetas están en español y los montos en soles (`S/`), con el IGV a la vista cuando aplica. La rejilla de productos del punto de venta, el kanban del CRM y la tabla de líneas siguen la estructura de Odoo 19, por lo que el wireframe sirve también como guía de configuración.
