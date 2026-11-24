# 4.2 Requerimientos funcionales

> **Estado:** borrador del Sprint 1 · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [04 §4.2 y §4.4](../plan/04_scrum_pmbok.md), [02 §2.3](../plan/02_mapeo_plantilla.md)
>
> Las fichas detalladas de cada RF van en el Anexo 10.1 (Sprint 2 y 3). Los RNF (tabla 3) los redacta Orlando.

## 4.2.1 Gestión de requerimientos

Cada requerimiento sigue esta cadena de trazabilidad:

```
Necesidad del negocio → RF / RNF → Historia de usuario (HU) → Épica (issue de GitHub) → Prueba
```

- Las **HU** están en el Product Backlog del GitHub Project «Scrum ERP D'Onofrio» con sus criterios de aceptación.
- Cada **épica** agrupa las HU de un área y un dueño; el PR de cada HU dice `Parte de #n`.
- Cada **prueba** vive en `addons/donofrio_base/tests/` (unitarias e integrales) o en las pruebas no funcionales (k6, ZAP, Lighthouse, SUS).

## 4.2.2 Requerimientos funcionales (tabla 2)

**Fase:** **F1** = núcleo garantizado, con Odoo estándar configurado por código. **F2** = depende de un módulo propio de la Fase 2.
**Estado** (al cierre de este borrador, Sprint 1): *Implementado*, *En curso* (HU de un sprint posterior de la F1) o *Diseñado – trabajo futuro* (RF de la F2 que solo pasa a *Implementado* si su módulo se construye; ver [02 §2.3](../plan/02_mapeo_plantilla.md)).

| Área | ID | Requerimiento funcional | Fase | HU | Estado | Prioridad |
|---|---|---|---|---|---|---|
| **Marketing y Ventas** | RF001 | Registrar oportunidades por canal en un embudo CRM | F1 | HU-08 (HU-31 opcional) | Implementado (S2) | Must |
| | RF002 | Cotizar y confirmar pedidos con listas de precios por canal y temporada | F1 | HU-09 | Implementado (S2) | Must |
| | RF003 | Vender en el punto de venta de la tienda de planta con boleta | F1 | HU-10 | Implementado (S2) | Must |
| | RF004 | Liquidar diariamente a los heladeros ambulantes | **F2** (`donofrio_heladeros`). Sin la F2 se cubre en parte: pedido de venta al heladero con la lista «Heladero» + devolución estándar | HU-20, HU-21 | Diseñado – trabajo futuro | Must (en F2) |
| **Logística y Almacén** | RF005 | Gestionar almacenes y ubicaciones con cámaras de frío | F1 | HU-06 | Implementado (HU-06) | Must |
| | RF006 | Controlar lotes con fecha de vencimiento y salida FEFO | F1 | HU-11 | Planificado (S2) | Must |
| | RF007 | Recibir insumos y despachar pedidos | F1 | HU-12 | Planificado (S2) | Must |
| | RF008 | Registrar temperaturas y alertar cuando están fuera de rango | **F2** (cadena de frío) | HU-19 | Diseñado – trabajo futuro | Must (en F2) |
| **Producción y Operaciones** | RF009 | Mantener listas de materiales (recetas) y centros de trabajo | F1 | HU-07 | Implementado (HU-07) | Must |
| | RF010 | Planificar y ejecutar órdenes de producción con lote | F1 | HU-14 | Planificado (S2) | Must |
| | RF011 | Inspeccionar la calidad por puntos de control ligados a la OP y al lote | **F2** (`donofrio_calidad`) | HU-17 | Implementado (M1, [5.5b](05_05_modulo_donofrio_calidad.md)) | Must (en F2) |
| | RF012 | Emitir el certificado de calidad del lote | **F2** (`donofrio_calidad`) | HU-18 | Implementado (M1, [5.5b](05_05_modulo_donofrio_calidad.md)) | Must (en F2) |
| **Dirección / Gerencia** | RF013 | Tablero gerencial de KPIs | F1 con los dashboards estándar de Community; **F2** con el tablero OWL propio | HU-23 (F1), HU-22 (F2) | Implementado (S3, HU-23) en F1; el tablero OWL queda como trabajo futuro | Must |
| | RF014 | Análisis por línea, canal y temporada | F1 | HU-23 | Implementado (S3, HU-23) | Must |
| **Otros: Compras, Finanzas, RR. HH., TI** | RF015 | Comprar insumos con reabastecimiento mín./máx. | F1 | HU-13 | Implementado (S2) | Must |
| | RF016 | Emitir facturas y boletas con IGV (`l10n_pe`) | F1 | HU-03, HU-15 | Implementado (HU-03 y HU-15) | Must |
| | RF017 | Gestionar el organigrama, empleados y puestos | F1 | HU-05 | Implementado (HU-05, PR #160) | Must |
| | RF018 | Gestionar usuarios y roles por área | F1 | HU-04 | Implementado (HU-04) | Must |

### Resumen por fase

| Fase | RF | Cantidad |
|---|---|---|
| F1 (núcleo) | RF001, RF002, RF003, RF005, RF006, RF007, RF009, RF010, RF013 (estándar), RF014, RF015, RF016, RF017, RF018 | 14 |
| F2 (módulo propio) | RF004, RF008, RF011, RF012 y RF013 (tablero OWL) | 4 + la parte propia de RF013 |

Con solo la Fase 1 el proyecto cumple los lineamientos: los RF de la F2 quedan documentados como **Diseñado – trabajo futuro**, con su caso de uso, wireframe y mockup ([02 §2.3](../plan/02_mapeo_plantilla.md)).

## Matriz RF ↔ épica del GitHub Project

| Épica (issue) | Área | Dueño | RF cubiertos |
|---|---|---|---|
| #133 Entorno Docker y CI | Infraestructura | Orlando | RNF007, RNF012 |
| #134 Datos maestros, compañía y seguridad | Base | Orlando | RF005, RF009, RF016 (compañía), RF018 |
| #135 RR. HH. y análisis empresarial | Extras | Evelyn | RF017 y la documentación de negocio del sprint |

> Las épicas de los sprints 2 y 3 se agregan a esta matriz cuando empiecen.
