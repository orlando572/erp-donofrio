# 4.1.4 Identificación de oportunidades de innovación tecnológica

> **Estado:** borrador del Sprint 3 · **Autora:** Evelyn · **Revisa:** Orlando · **Fuente:** [3.2.4](03_aspectos_generales.md) (tabla 1), [4.1.1](04_01_analisis_sistemas.md) (brechas por área) y [3.6](03_aspectos_generales.md) (FODA y estrategias cruzadas)
>
> Todos los problemas son **supuestos AS-IS (S7)**: no hay acceso a los sistemas internos de D'Onofrio. El estado final es el real al 23/11/2026, con la Fase 1 terminada y la Fase 2 sin construir.

## 4.1.4.1 De los problemas a las oportunidades (tabla 1)

Cada problema del caso ([3.2.4](03_aspectos_generales.md)) se liga con la **brecha** que lo causa ([4.1.1](04_01_analisis_sistemas.md)), con el tipo de **oportunidad** que abre y con la **tecnología** que la aprovecha. La última columna dice cuánto se alcanzó.

| ID | Problema empresarial | Brecha que lo causa (4.1.1) | Oportunidad | Tecnología propuesta | Estado final |
|---|---|---|---|---|---|
| 1 | La liquidación diaria de los heladeros se hace en papel o Excel, con descuadres y mermas no trazadas | Heladeros: vales de papel y cálculo a mano, sin vínculo con el lote ni con el pedido | **Automatización** del cálculo de lo vendido, la merma y la comisión | `donofrio_heladeros` (Fase 2, M2); en la Fase 1, pedido de venta con la lista «Heladero» + devolución estándar | **Parcial.** Con la Fase 1 se vende al heladero a su precio y se registra la devolución (HU-09); el cálculo automático y el PDF para firmar quedan como diseño |
| 2 | El vencimiento de los lotes no se controla y el despacho no sigue FEFO | Logística: kárdex en Excel y revisión visual de fechas | **Integración en tiempo real** del stock con su vencimiento | Inventario de Odoo con lotes y `product_expiry` | **Resuelto** (HU-11, HU-12, HU-33): la entrega reserva el lote que vence antes y no despacha uno vencido |
| 3 | Las temperaturas de las cámaras se anotan a mano y las alertas llegan tarde | Cadena de frío: planilla en papel sin historial | **Digitalización y alertas** de los rangos por ubicación | Cadena de frío en `donofrio_calidad` (Fase 2, M3) | **No resuelto.** Solo hay diseño (CU006, wireframe y mockup); en la Fase 1 los rangos están en el nombre de la ubicación |
| 4 | Las inspecciones de calidad están en papel y no se ligan al lote | Calidad: formatos en papel; la inspección no bloquea el despacho | **Trazabilidad** de la inspección al lote | `donofrio_calidad` + MRP (Fase 2, M1); en la Fase 1, lotes y trazabilidad estándar | **Parcial.** El lote se sigue de la compra del insumo a la entrega (HU-14, HU-33); la inspección y el certificado son diseño |
| 5 | La planificación de campañas se hace sin datos consolidados | Gerencia: reportes armados a mano al cierre del mes | **Analítica** de ventas por línea, canal y temporada | Dashboards estándar y vistas guardadas (Fase 1) + tablero OWL (Fase 2, M4) | **Resuelto en lo estándar** (HU-23); el tablero propio es diseño |
| 6 | Ventas, almacén y producción usan sistemas separados y digitan dos veces | Información dispersa: cada área con su propia herramienta | **Integración de sistemas** en una sola base de datos | ERP Odoo 19 Community único sobre PostgreSQL 16 | **Resuelto** (HU-08 a HU-16, HU-33): el ciclo vender, comprar, producir y facturar se prueba de punta a punta |
| 7 | La gerencia no tiene reportes oportunos | Decisiones tardías: datos inconsistentes entre áreas | **Analítica (BI)** con datos del día | Dashboards estándar de Odoo | **Resuelto en lo estándar** (HU-23, 4.7) |

**Lectura.** De los 7 problemas, **4 quedan resueltos con la Fase 1** (2, 5, 6 y 7), **2 quedan parciales** (1 y 4) y **1 no se resuelve** (3). Los tres últimos dependen de módulos propios que no se construyeron; el Gate 0 decide si alguno se construye (ver [7.2](07_conclusiones.md)).

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
2. **Datos para planificar la estacionalidad.** Con 16 semanas de transacciones de demostración (HU-16) se ven las curvas de helados en verano y de panetón en Navidad; es la base de la estrategia FO de [3.6.2](03_aspectos_generales.md).
3. **Trazabilidad como diferencial de calidad.** El lote trazable de la compra al cliente es un argumento comercial y respalda las prácticas de ISO 9001 y HACCP ([09 del plan](../plan/09_normas_marcos.md)).
4. **Escenario Froneri.** Si el negocio de helados cambia de dueño, un ERP que separa líneas de producto y canales sigue siendo útil con chocolates y panetón. No se modela la transición (supuesto S1).

## 4.1.4.4 Qué queda como trabajo futuro

| Oportunidad sin construir | Módulo | Requisito | Dónde está el diseño |
|---|---|---|---|
| Liquidación automática del heladero | `donofrio_heladeros` (M2) | RF004 | CU004, [4.4](04_04_prototipos.md) y BPMN TO-BE 12 |
| Inspección de calidad y certificado del lote | `donofrio_calidad` (M1) | RF011, RF012 | CU008, [4.4](04_04_prototipos.md) y BPMN TO-BE 7 |
| Temperaturas con alertas | Cadena de frío (M3) | RF008 | CU006, [4.4](04_04_prototipos.md) |
| Tablero gerencial propio | `donofrio_tablero` (M4) | RF013 (parte propia) | CU009, [4.4](04_04_prototipos.md) |

Ninguno se empieza sin la confirmación explícita del equipo en el Gate 0 (`docs/scrum/gates/gate-0-fase1.md`).
