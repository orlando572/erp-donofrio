# 4.2 Requerimientos funcionales

## 4.2.1 Gestión de requerimientos

Cada requerimiento sigue una cadena de trazabilidad: **necesidad del negocio → RF o RNF → historia de usuario (HU) → épica (issue de GitHub) → prueba**. Las HU están en el Product Backlog del GitHub Project con sus criterios de aceptación; cada épica agrupa las HU de un área y un dueño, y cada prueba vive en las pruebas automáticas de los módulos o en las pruebas no funcionales (k6, ZAP y Lighthouse). La matriz completa de trazabilidad está en el anexo 10.7 y las fichas detalladas, en los anexos 10.1 y 10.2.

## 4.2.2 Requerimientos funcionales

Los 18 requerimientos funcionales están **implementados**: los 14 del núcleo con Odoo estándar configurado por `donofrio_base` (versión `v1.0.0`) y los de la Fase 2 con los módulos propios, publicados en las versiones `v1.1.0` (M1), `v1.2.0` (M2), `v1.3.0` (M3) y `v1.4.0` (M4). Todos tienen prioridad *Must*.

**Tabla 4.6. Requerimientos funcionales**

| Código | Requerimiento | Módulo | Estado |
|---|---|---|---|
| RF001 | Registrar oportunidades por canal en un embudo CRM | CRM (estándar) | Implementado |
| RF002 | Cotizar y confirmar pedidos con listas de precios por canal y temporada | Ventas (estándar) | Implementado |
| RF003 | Vender en el punto de venta de la tienda de planta con boleta | Punto de venta (estándar) | Implementado |
| RF004 | Liquidar diariamente a los heladeros ambulantes | `donofrio_heladeros` (M2) | Implementado |
| RF005 | Gestionar almacenes y ubicaciones con cámaras de frío | Inventario (estándar) | Implementado |
| RF006 | Controlar lotes con fecha de vencimiento y salida FEFO | Inventario (estándar) | Implementado |
| RF007 | Recibir insumos y despachar pedidos | Inventario (estándar) | Implementado |
| RF008 | Registrar temperaturas y alertar cuando están fuera de rango | `donofrio_calidad` (M3) | Implementado |
| RF009 | Mantener listas de materiales (recetas) y centros de trabajo | Manufactura (estándar) | Implementado |
| RF010 | Planificar y ejecutar órdenes de producción con lote | Manufactura (estándar) | Implementado |
| RF011 | Inspeccionar la calidad por puntos de control ligados a la orden y al lote | `donofrio_calidad` (M1) | Implementado |
| RF012 | Emitir el certificado de calidad del lote | `donofrio_calidad` (M1) | Implementado |
| RF013 | Tablero gerencial de KPI | Dashboards estándar y `donofrio_tablero` (M4) | Implementado |
| RF014 | Análisis por línea, canal y temporada | Dashboards y vistas guardadas (estándar) | Implementado |
| RF015 | Comprar insumos con reabastecimiento mín./máx. | Compras (estándar) | Implementado |
| RF016 | Emitir facturas y boletas con IGV | Facturación con `l10n_pe` (estándar) | Implementado |
| RF017 | Gestionar el organigrama, empleados y puestos | RR. HH. (estándar) | Implementado |
| RF018 | Gestionar usuarios y roles por área | Usuarios y grupos (`donofrio_base`) | Implementado |

Por fase, 14 requerimientos corresponden al núcleo y cuatro (RF004, RF008, RF011 y RF012) más la parte propia de RF013 a los módulos de la Fase 2, que se construyeron uno a uno. Los límites de cada módulo figuran en las fichas del anexo 10.1 y en la sección 5.5.
