# 3.1.4.2 Módulo de Calidad (M1)

El módulo de calidad de Odoo solo existe en la edición Enterprise, así que el módulo de Calidad (`donofrio_calidad`, M1) se desarrolló para D'Onofrio (HU-17 y HU-18; RF011 y RF012; CU008). Se publicó en la versión v1.1.0 y se apoya en la configuración base y en Fabricación e Inventario de Odoo.

**Qué hace.** Define puntos de control (qué se mide y su norma) y, al terminar una orden de producción, crea una inspección por cada lote producido. El inspector mide los puntos y el lote se aprueba (solo si todo cumple) o se rechaza con motivo. Un lote rechazado no se despacha a un cliente (RNF005), ni por transferencia ni por el punto de venta, y de una inspección aprobada se emite el certificado de calidad del lote en PDF, con las mediciones, el responsable y el logo.

**Datos que maneja.** El punto de control (con un rango o «cumple / no cumple»), la inspección (una sola por orden y lote) y la línea de medición de cada punto, con su resultado calculado. La inspección pasa por **Pendiente** (se crea sola), **En medición** (genera una línea por cada punto que aplica al producto), **Aprobado** (todos los puntos cumplen; un punto sin medir no deja aprobar) y **Rechazado** (exige motivo y deja una actividad al responsable de la orden). Los cinco puntos cargados son pasteurización (80 a 85 °C), endurecimiento (−40 a −18 °C), peso neto por unidad (±2 %), análisis microbiológico y humedad del panetón (22 a 28 %); las normas son supuestos del caso. Los usuarios de inventario solo consultan las inspecciones, el inspector de calidad las crea y modifica, y la jefatura de calidad además administra los puntos de control; cualquier otro usuario recibe un aviso de acceso denegado.

![Inspección aprobada con sus cuatro mediciones dentro de la norma](../capturas/sprint-4/HU-17_inspeccion_aprobada.png)

*Figura 5.5b-a. Inspección INS/00180 aprobada, con las cuatro mediciones dentro de su norma (datos de demostración).*

**Pruebas.** El módulo tiene 45 pruebas sin errores: 13 de inspección y certificado, 2 del punto de venta, 1 de idioma y 29 de la cadena de frío (3.1.4.4). En la pantalla se verificaron la lista de inspecciones, la aprobación, el rechazo por pasteurización a 79.46 °C y el certificado PDF; el bloqueo del lote rechazado se verificó con pruebas automáticas.
