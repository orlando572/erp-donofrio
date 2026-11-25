# 4.6 Desarrollo front-end: prototipos web, buenas prácticas de UI/UX y reportes

## 4.6.1 Buenas prácticas de conversión de prototipos a web UI/UX

El sistema no se programa pantalla por pantalla: se configura Odoo 19 Community con datos y vistas guardadas por código. La conversión de un prototipo en pantalla real consiste en elegir la pantalla estándar de Odoo que se parece al mockup y dejarla bien configurada. Las prácticas siguieron las heurísticas de Nielsen.

La **visibilidad del estado** se logra con la barra de estado del documento (borrador → confirmado → hecho); la **relación con el mundo real**, con la interfaz en español peruano, soles, IGV 18 % y los términos del negocio (lote, FEFO, heladero, boleta); el **control del usuario**, con descartar cambios, volver a borrador y archivar en vez de borrar; la **consistencia**, al mantener las pantallas estándar de Odoo; la **prevención de errores**, porque no se recibe un insumo sin lote, FEFO no reserva un lote vencido y el comprobante y el IGV salen según el cliente; y la **eficiencia**, con listas de precios por canal, vistas guardadas en «Favoritos» y una acción principal por pantalla.

**Contraste y adaptabilidad.** El contraste de los pares de color de los mockups cumple el mínimo de WCAG 2.1 (4.5): texto oscuro sobre el amarillo de marca da 8.79 y los colores de alerta sobre blanco, de 5.13 a 5.75; el amarillo como texto sobre blanco da 1.61 y no cumple, por lo que **se usa solo como fondo** y las alertas siempre llevan un texto. La liquidación y el tablero se revisaron en una ventana de 375 × 812 sin desplazamiento horizontal (solo con Chrome, RNF001). Todo el texto visible está en español, salvo los títulos de algunos gráficos del dashboard «Métricas del almacén», que Odoo no traduce.

## 4.6.2 Propuesta de prototipos web

Cada caso de uso tiene su mockup y su pantalla real configurada. Las de la Fase 1 son pantallas estándar de Odoo; las de la Fase 2 son propias y se muestran con datos de demostración en 5.5 (inspección de calidad, liquidación del heladero y tablero gerencial). La estructura es la del mockup; cambian el color (el mockup usa el amarillo de marca) y algunos nombres de campo.

## 4.6.3 Prototipos de informes y reportes

Los reportes se hacen con **QWeb**, el motor nativo de Odoo, y no con JasperReports como sugiere la plantilla: no requiere un servidor aparte, se versiona como XML, genera el PDF con el mismo motor de Odoo y hereda el layout de la compañía (logo, nombre, RUC y dirección).

La **factura (01) y la boleta (03)** llevan el logo y los datos de la compañía (la boleta usa la plantilla de la factura y se titula «Factura»). La **nota de entrega** es un comprobante interno de la salida, sin valor tributario, porque la guía de remisión electrónica requiere `l10n_pe_edi`, que es Enterprise. La **orden de producción** es un documento interno de taller con códigos de barras. Los dos reportes propios son el **certificado de calidad del lote** (M1, hoja A4) y la **liquidación del heladero** con detalle por producto y firmas de ambas partes (M2).

La prueba automática de los reportes revisa el HTML, porque `wkhtmltopdf` se cuelga si corre dentro del propio servidor; el PDF se verifica a mano.
