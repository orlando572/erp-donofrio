# 2.1.4 Identificación de oportunidades de innovación tecnológica

Cada problema del caso (1.2.3) se liga con la brecha que lo causa (2.1.1), la oportunidad que abre y la tecnología que la aprovecha. Los siete problemas quedan resueltos: cuatro con el núcleo (2, 5, 6 y 7) y tres con los módulos desarrollados para D'Onofrio.

**Tabla 4.2. De los problemas a las oportunidades**

| ID | Oportunidad | Tecnología | Resultado |
|---|---|---|---|
| 1 | Automatización de lo vendido, la merma y la comisión del heladero | El módulo de Liquidación de heladeros (M2, v1.2.0) | Liquidación por heladero y fecha, pedido automático y PDF para firmar |
| 2 | Integración en tiempo real del stock con su vencimiento | Inventario con lotes y el control de vencimientos de Odoo | La entrega reserva el lote que vence antes y no despacha uno vencido |
| 3 | Digitalización y alertas por rango de ubicación | Cadena de frío en el módulo de Calidad (M3, v1.3.0) | Lectura por cámara con su rango y alerta cuando sale de él |
| 4 | Trazabilidad de la inspección al lote | El módulo de Calidad (M1, v1.1.0) | Inspección por puntos de control, certificado en PDF y bloqueo del lote rechazado |
| 5 | Analítica por línea, canal y temporada | Dashboards y tablero OWL (M4, v1.4.0) | Seis tarjetas, gráfico de ventas y filtro por almacén |
| 6 | Integración en una sola base | Odoo 19 y PostgreSQL 16 | El ciclo vender, comprar, producir y facturar se prueba de punta a punta |
| 7 | Analítica (BI) con datos del día | Dashboards de Odoo | Reportes oportunos para la gerencia |

Al mapear las brechas aparecieron además oportunidades que el ERP aprovecha sin código propio: el reabastecimiento automático por reglas mín./máx. (RF015), los comprobantes desde el pedido (factura 01 o boleta 03 con IGV, sin envío a SUNAT, RF016), la venta de mostrador integrada con inventario (RF003), una única fuente de empleados y roles (RF017, RF018), la mesa de servicios con tipos ITIL (AXELOS, 2019), la continuidad con réplica y respaldos (tiempo de recuperación, RTO, de 31 s) y el costeo real por lote con FIFO (RF010).

Del FODA (1.6.1) salen cuatro oportunidades del entorno: un ERP abierto sin licencias Enterprise, en el que la inspección de calidad se cubre con un módulo desarrollado para D'Onofrio; datos de 16 semanas de demostración para planificar la estacionalidad; la trazabilidad como diferencial de calidad alineada con ISO 9001 (ISO, 2015) y HACCP; y el escenario Froneri, ante el cual un ERP que separa líneas y canales sigue siendo útil con chocolates y panetón. Sobre esta base se proyectan los sensores de temperatura (IoT), una aplicación móvil para el heladero, el envío electrónico a SUNAT mediante un OSE y un tablero por áreas (sección 8).
