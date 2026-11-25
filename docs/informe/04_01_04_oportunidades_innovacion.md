# 4.1.4 Identificación de oportunidades de innovación tecnológica

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn · **Revisa:** Orlando · **Fuente:** [3.2.4](03_aspectos_generales.md) (tabla 1), [4.1.1](04_01_analisis_sistemas.md) (brechas por área) y [3.6](03_aspectos_generales.md) (FODA y estrategias cruzadas)
>
> Todos los problemas son **supuestos AS-IS (S7)**: no hay acceso a los sistemas internos de D'Onofrio. El estado final es el real al 25/11/2026, con la Fase 1 y la Fase 2 (M1 a M4) terminadas y publicadas en las releases `v1.0.0` a `v1.4.0`.

## 4.1.4.1 De los problemas a las oportunidades (tabla 1)

Cada problema del caso ([3.2.4](03_aspectos_generales.md)) se liga con la **brecha** que lo causa ([4.1.1](04_01_analisis_sistemas.md)), con el tipo de **oportunidad** que abre y con la **tecnología** que la aprovecha. La última columna dice cuánto se alcanzó.

| ID | Problema empresarial | Brecha que lo causa (4.1.1) | Oportunidad | Tecnología propuesta | Estado final |
|---|---|---|---|---|---|
| 1 | La liquidación diaria de los heladeros se hace en papel o Excel, con descuadres y mermas no trazadas | Heladeros: vales de papel y cálculo a mano, sin vínculo con el lote ni con el pedido | **Automatización** del cálculo de lo vendido, la merma y la comisión | `donofrio_heladeros` (Fase 2, M2); en la Fase 1, pedido de venta con la lista «Heladero» + devolución estándar | **Resuelto** con M2 (HU-20 y HU-21, `v1.2.0`): liquidación por heladero y fecha con vendido, importe, comisión y diferencia de efectivo, pedido de venta automático y PDF para firmar. Antes (solo Fase 1) era parcial: precio de heladero y devolución estándar (HU-09). Límite: no probada en un celular real |
| 2 | El vencimiento de los lotes no se controla y el despacho no sigue FEFO | Logística: kárdex en Excel y revisión visual de fechas | **Integración en tiempo real** del stock con su vencimiento | Inventario de Odoo con lotes y `product_expiry` | **Resuelto** (HU-11, HU-12, HU-33): la entrega reserva el lote que vence antes y no despacha uno vencido |
| 3 | Las temperaturas de las cámaras se anotan a mano y las alertas llegan tarde | Cadena de frío: planilla en papel sin historial | **Digitalización y alertas** de los rangos por ubicación | Cadena de frío en `donofrio_calidad` (Fase 2, M3) | **Resuelto** con M3 (HU-19, `v1.3.0`): rango por ubicación, lecturas con alerta fuera de rango y *cron* de lotes por vencer. Antes (solo Fase 1) no estaba resuelto. Límites: lecturas a mano, sin sensores |
| 4 | Las inspecciones de calidad están en papel y no se ligan al lote | Calidad: formatos en papel; la inspección no bloquea el despacho | **Trazabilidad** de la inspección al lote | `donofrio_calidad` + MRP (Fase 2, M1); en la Fase 1, lotes y trazabilidad estándar | **Resuelto** con M1 (HU-17 y HU-18, `v1.1.0`): inspección por puntos de control ligada a la orden y al lote, certificado en PDF y bloqueo del lote rechazado. Antes (solo Fase 1) era parcial: el lote se sigue de la compra a la entrega (HU-14, HU-33) |
| 5 | La planificación de campañas se hace sin datos consolidados | Gerencia: reportes armados a mano al cierre del mes | **Analítica** de ventas por línea, canal y temporada | Dashboards estándar y vistas guardadas (Fase 1) + tablero OWL (Fase 2, M4) | **Resuelto** en lo estándar (HU-23) y reforzado con el tablero OWL de M4 (HU-22, `v1.4.0`): 6 tarjetas, gráfico de ventas y filtro por almacén. Límite: Lighthouse 76 (límite conocido, [4.6.4](04_06_wpo.md)) |
| 6 | Ventas, almacén y producción usan sistemas separados y digitan dos veces | Información dispersa: cada área con su propia herramienta | **Integración de sistemas** en una sola base de datos | ERP Odoo 19 Community único sobre PostgreSQL 16 | **Resuelto** (HU-08 a HU-16, HU-33): el ciclo vender, comprar, producir y facturar se prueba de punta a punta |
| 7 | La gerencia no tiene reportes oportunos | Decisiones tardías: datos inconsistentes entre áreas | **Analítica (BI)** con datos del día | Dashboards estándar de Odoo | **Resuelto** (HU-23, HU-22, 4.7) |

**Lectura.** De los 7 problemas, **los 7 quedan resueltos**: 4 con la Fase 1 (2, 5, 6 y 7) y 3 más con los módulos propios de la Fase 2 (1 con M2, 3 con M3 y 4 con M1). Con solo la Fase 1 habrían quedado 4 resueltos, 2 parciales (1 y 4) y 1 sin resolver (3). Las conclusiones por problema están en [7.2](07_conclusiones.md); lo que queda abierto, en 4.1.4.4.

## 4.1.4.2 Oportunidades que no estaban en la tabla 1

Al mapear las brechas por área aparecieron mejoras que no son un «problema» del caso, pero que el ERP aprovecha sin código propio.

| # | Brecha | Oportunidad de innovación | Cómo se aprovechó | HU | Estado |
|---|---|---|---|---|---|
| A | Compras: faltantes detectados «a simple vista» y órdenes en Word | **Reabastecimiento automático**: el planificador de Odoo genera la solicitud de cotización cuando el stock baja del mínimo | Reglas mín./máx. por insumo (RF015) | HU-13 | Resuelto |
| B | Facturación: doble digitación y tipo de documento a criterio de la persona | **Comprobantes desde el pedido**: factura (01) si hay RUC y boleta (03) si hay DNI, con IGV 18 % | Diarios y tipos de documento de `l10n_pe` configurados por código (RF016). Limitación: sin envío a SUNAT porque `l10n_pe_edi` es Enterprise | HU-15 | Resuelto, con limitación |
| C | Punto de venta: la venta del mostrador no descuenta stock ni llega a facturación | **Venta de mostrador integrada** con inventario y boleta | Punto de Venta con sesión, boleta y cierre de caja (RF003). Limitación: no aplica FEFO | HU-10 | Resuelto, con limitación |
| D | RR. HH.: el organigrama se desactualiza y no se liga con los usuarios | **Una sola fuente** de empleados, puestos y usuarios por rol | Organigrama en Odoo y 10 usuarios con permisos mínimos (RF017, RF018) | HU-04, HU-05 | Resuelto |
| E | TI: el soporte se pide por correo, sin registro ni plazo | **Mesa de servicios** con tipos de ticket ITIL y plazo según la prioridad | Proyecto de Odoo con etapas, etiquetas y pivote de cumplimiento del SLA | HU-32 | Resuelto |
| F | Continuidad: no hay respaldo ni réplica descritos para la unidad | **Continuidad en temporada alta**: réplica en caliente y restauración medida | Réplica de PostgreSQL y `backup.sh` con `restore.sh` (RTO de 31 s) | HU-25, HU-26 | Resuelto |
| G | Costo del lote desconocido | **Costeo real por lote**: insumos por FIFO más las horas del centro de trabajo | Orden de producción con valoración (RF010) | HU-14 | Resuelto |

## 4.1.4.3 Oportunidades del entorno

Del [FODA](03_aspectos_generales.md) (3.6.1) y de la [cascada COBIT](03_aspectos_generales.md) (3.6.4) salen cuatro oportunidades externas que el proyecto aprovecha o deja abiertas:

1. **ERP abierto sin licencias Enterprise.** Odoo 19 Community cubre las cinco áreas con costo de licencia cero. El costo es que hay funciones que no existen en Community (calidad, EDI de SUNAT, nómina) y se declaran como limitación o se cubren con módulo propio.
2. **Datos para planificar la estacionalidad.** Con las transacciones de demostración (HU-16: 16 semanas del núcleo, ampliadas al 22/11/2026 para que todas las vistas tengan datos) se ven las curvas de helados en verano y de panetón en Navidad; es la base de la estrategia FO de [3.6.2](03_aspectos_generales.md).
3. **Trazabilidad como diferencial de calidad.** El lote trazable de la compra al cliente es un argumento comercial y respalda las prácticas de ISO 9001 y HACCP ([09 del plan](../plan/09_normas_marcos.md)).
4. **Escenario Froneri.** Si el negocio de helados cambia de dueño, un ERP que separa líneas de producto y canales sigue siendo útil con chocolates y panetón. No se modela la transición (supuesto S1).

## 4.1.4.4 Qué queda como trabajo futuro

Los cuatro módulos de la Fase 2 **ya están construidos**. Lo que queda abierto son mejoras sobre ellos y oportunidades que el proyecto no abordó; el detalle, la evidencia y el orden de prioridad están en [8](08_recomendaciones.md) y [8.1](08_01_recomendaciones_negocio.md).

| Oportunidad sin construir | Relacionada con | Por qué quedó fuera |
|---|---|---|
| Sensores de temperatura (IoT) en las cámaras y alerta por lecturas que faltan | M3 (RF008) | Las lecturas son manuales; no se contó con hardware |
| Aplicación móvil (o PWA probada en celular real) para el heladero | M2 (RF004) | La vista móvil se verificó solo en un emulador |
| Envío electrónico de comprobantes a SUNAT vía OSE | RF016 | `l10n_pe_edi` es Enterprise |
| Auditoría con `auditlog` de liquidaciones, inspecciones y temperaturas | RNF010 | M1 a M3 usan el historial del chatter |
| Versión parcial del tablero por áreas y mejora del rendimiento del tablero | M4 (RF013, RNF008) | Lighthouse da 76; es un límite conocido |

La construcción de los módulos se hizo uno a uno, con confirmación explícita del equipo y un mini gate por módulo (`docs/scrum/gates/gate-m1-calidad.md` a `gate-m4-tablero.md`).
