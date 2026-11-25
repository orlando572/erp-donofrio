# 4.2 Requerimientos funcionales

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [04 §4.2 y §4.4](../plan/04_scrum_pmbok.md), [02 §2.3](../plan/02_mapeo_plantilla.md)
>
> Las fichas detalladas de cada RF están en el [Anexo 10.1](anexo_10_01_fichas_rf.md). Los RNF (tabla 3) están en [4.2.3](04_02_requerimientos_no_funcionales.md).

## 4.2.1 Gestión de requerimientos

Cada requerimiento sigue esta cadena de trazabilidad:

```
Necesidad del negocio → RF / RNF → Historia de usuario (HU) → Épica (issue de GitHub) → Prueba
```

- Las **HU** están en el Product Backlog del GitHub Project «Scrum ERP D'Onofrio» con sus criterios de aceptación.
- Cada **épica** agrupa las HU de un área y un dueño; el PR de cada HU dice `Parte de #n`.
- Cada **prueba** vive en `addons/donofrio_base/tests/` (unitarias e integrales) o en las pruebas no funcionales (k6, ZAP y Lighthouse).

## 4.2.2 Requerimientos funcionales (tabla 2)

**Fase:** **F1** = núcleo garantizado, con Odoo estándar configurado por código. **F2** = depende de un módulo propio de la Fase 2.
**Estado al cierre del proyecto (25/11/2026):** los **18 RF están *Implementados***. Los 14 de la F1 con Odoo estándar configurado por `donofrio_base` (tag [`v1.0.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.0.0)) y los de la F2 con sus módulos propios, fusionados en `main` por el [PR #229](https://github.com/orlando572/erp-donofrio/pull/229) y publicados en las releases `v1.1.0` (M1), `v1.2.0` (M2), `v1.3.0` (M3) y `v1.4.0` (M4). Ningún RF queda como «Diseñado – trabajo futuro». Los límites de cada módulo están en su ficha del [Anexo 10.1](anexo_10_01_fichas_rf.md) y en 5.5b a 5.5e.

| Área | ID | Requerimiento funcional | Fase | HU | Estado | Prioridad |
|---|---|---|---|---|---|---|
| **Marketing y Ventas** | RF001 | Registrar oportunidades por canal en un embudo CRM | F1 | HU-08 (HU-31 opcional) | Implementado (S2) | Must |
| | RF002 | Cotizar y confirmar pedidos con listas de precios por canal y temporada | F1 | HU-09 | Implementado (S2) | Must |
| | RF003 | Vender en el punto de venta de la tienda de planta con boleta | F1 | HU-10 | Implementado (S2) | Must |
| | RF004 | Liquidar diariamente a los heladeros ambulantes | **F2** (`donofrio_heladeros`). Sin la F2 se cubre en parte: pedido de venta al heladero con la lista «Heladero» + devolución estándar | HU-20, HU-21 | Implementado (M2, [5.5c](05_05_modulo_donofrio_heladeros.md)) | Must (en F2) |
| **Logística y Almacén** | RF005 | Gestionar almacenes y ubicaciones con cámaras de frío | F1 | HU-06 | Implementado (HU-06) | Must |
| | RF006 | Controlar lotes con fecha de vencimiento y salida FEFO | F1 | HU-11 | Implementado (S2) | Must |
| | RF007 | Recibir insumos y despachar pedidos | F1 | HU-12 | Implementado (S2) | Must |
| | RF008 | Registrar temperaturas y alertar cuando están fuera de rango | **F2** (cadena de frío) | HU-19 | Implementado (M3, [5.5d](05_05_modulo_donofrio_frio.md)) | Must (en F2) |
| **Producción y Operaciones** | RF009 | Mantener listas de materiales (recetas) y centros de trabajo | F1 | HU-07 | Implementado (HU-07) | Must |
| | RF010 | Planificar y ejecutar órdenes de producción con lote | F1 | HU-14 | Implementado (S2) | Must |
| | RF011 | Inspeccionar la calidad por puntos de control ligados a la OP y al lote | **F2** (`donofrio_calidad`) | HU-17 | Implementado (M1, [5.5b](05_05_modulo_donofrio_calidad.md)) | Must (en F2) |
| | RF012 | Emitir el certificado de calidad del lote | **F2** (`donofrio_calidad`) | HU-18 | Implementado (M1, [5.5b](05_05_modulo_donofrio_calidad.md)) | Must (en F2) |
| **Dirección / Gerencia** | RF013 | Tablero gerencial de KPIs | F1 con los dashboards estándar de Community; **F2** con el tablero OWL propio | HU-23 (F1), HU-22 (F2) | Implementado: F1 con los dashboards estándar (S3, HU-23) y el tablero OWL de M4 (HU-22, 24/11/2026, [5.5e](05_05_modulo_donofrio_tablero.md)) | Must |
| | RF014 | Análisis por línea, canal y temporada | F1 | HU-23 | Implementado (S3, HU-23) | Must |
| **Otros: Compras, Finanzas, RR. HH., TI** | RF015 | Comprar insumos con reabastecimiento mín./máx. | F1 | HU-13 | Implementado (S2) | Must |
| | RF016 | Emitir facturas y boletas con IGV (`l10n_pe`) | F1 | HU-03, HU-15 | Implementado (HU-03 y HU-15) | Must |
| | RF017 | Gestionar el organigrama, empleados y puestos | F1 | HU-05 | Implementado (HU-05, PR #160) | Must |
| | RF018 | Gestionar usuarios y roles por área | F1 | HU-04 | Implementado (HU-04) | Must |

### Resumen por fase

| Fase | RF | Cantidad |
|---|---|---|
| F1 (núcleo) | RF001, RF002, RF003, RF005, RF006, RF007, RF009, RF010, RF013 (estándar), RF014, RF015, RF016, RF017, RF018 | 14 |
| F2 (módulo propio) | RF004 (M2), RF008 (M3), RF011 y RF012 (M1) y RF013 (tablero OWL de M4) | 4 + la parte propia de RF013 |

Los **18 RF están implementados**: 14 con el núcleo (F1) y 4 más la parte propia de RF013 con los módulos de la Fase 2, que se construyeron uno a uno, con su mini gate ([`docs/scrum/gates/`](../scrum/gates/)): M1 → [el mini gate de M1](../scrum/gates/gate-m1-calidad.md), M2 → [el mini gate de M2](../scrum/gates/gate-m2-heladeros.md), M3 → [el mini gate de M3](../scrum/gates/gate-m3-cadena-frio.md) y M4 → [el mini gate de M4](../scrum/gates/gate-m4-tablero.md). Cada uno conserva su caso de uso, wireframe y mockup; la trazabilidad RF → HU → PR → prueba está en [la matriz de trazabilidad (10.7)](trazabilidad.md).

## Matriz RF ↔ épica del GitHub Project

| Épica (issue) | Área | Dueño | RF cubiertos |
|---|---|---|---|
| #133 Entorno Docker y CI | Infraestructura | Orlando | RNF007, RNF012 |
| #134 Datos maestros, compañía y seguridad | Base | Orlando | RF005, RF009, RF016 (compañía), RF018 |
| #135 RR. HH. y análisis empresarial | Extras | Evelyn | RF017 y la documentación de negocio del sprint |
| #136 Ventas, CRM y PdV | Ventas | Evelyn | RF001, RF002, RF003 |
| #137 Compras y facturación | Extras | Evelyn | RF015, RF016 |
| #138 Inventario y producción | Logística y producción | Orlando | RF006, RF007, RF010 |
| #139 Transacciones de demostración | Base | Orlando | Datos para todos los RF |
| #140 Infraestructura, réplica y seguridad | Infraestructura | Orlando | RNF006, RNF009, RNF010, RNF012 |
| #141 Gerencia, KPIs y mesa de servicios ITIL | Gerencia | Evelyn | RF013 (estándar), RF014, RNF011 |
| #142 Pruebas y calidad del software | Pruebas | Orlando | RNF002, RNF004, RNF007, RNF008 |
| #144 M1 `donofrio_calidad` | F2 | Orlando | RF011, RF012, RNF005 |
| #145 M2 `donofrio_heladeros` | F2 | Evelyn | RF004 |
| #146 M3 Cadena de frío | F2 | Orlando | RF008 |
| #147 M4 `donofrio_tablero` + branding | F2 | Evelyn | RF013 (propio), RNF003 (marca), RNF008 |

Las épicas #144 y #145 siguen **abiertas** en GitHub aunque sus PR están fusionados: el equipo no marcó el último criterio de cada una (la casilla de HU-21 y la tarjeta del Project, que actualiza Orlando). Esto no cambia el estado de los RF.
