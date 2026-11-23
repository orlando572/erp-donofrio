# 3. Módulos de Odoo 19 Community y mejoras propuestas

[← Índice](PLAN_PROYECTO.md)

## 3.1 Qué es Community y qué es Enterprise en Odoo 19 (verificado)

Se verificó revisando si cada módulo existe en la rama `19.0` de `github.com/odoo/odoo`: si está en el repositorio Community, es Community (licencia LGPL-3).

| Funcionalidad | Edición | Evidencia | Qué hacemos |
|---|---|---|---|
| CRM, Ventas, PdV, Inventario, MRP, Compras, Facturación (`account`), Empleados, Asistencias, Ausencias, Gastos, Website | **Community** (LGPL-3) | Los manifests existen en la 19.0 | Se usan |
| `product_expiry` (lotes con vencimiento), `mrp_account`, `stock_account` | Community | Existen en la 19.0 | Se usan |
| `l10n_pe` (plan contable, impuestos, tipos de documento LATAM, tipos de identificación RUC/DNI, distritos, bancos) y `l10n_pe_pos` | Community | Existen en la 19.0; `l10n_pe` versión 3.1, autores Vauxoo y Odoo S.A. | Se usan |
| Dashboards (`spreadsheet_dashboard`, `_sale`, `_stock_account`) | Community: tableros **de solo lectura** | Existen en la 19.0. La edición de hojas de cálculo (`spreadsheet_edition`) no está en Community | Se usan como complemento; el tablero propio es OWL |
| **Calidad** (`quality`, `quality_control`) | **Enterprise** | `addons/quality` no existe en la 19.0 de Community | Módulo propio `donofrio_calidad` (Fase 2, M1) |
| **Contabilidad completa** (reportes financieros `account_reports`) | **Enterprise** | No existe en Community | Solo Facturación. Opcional: OCA `account_financial_report` (19.0 disponible) |
| **Nómina** (`hr_payroll`) | **Enterprise** | No existe en Community | Fuera de alcance |
| **EDI SUNAT** (`l10n_pe_edi`) | **Enterprise** | No existe en Community | Limitación declarada; comprobantes sin envío a SUNAT/OSE |
| **Modo oscuro** | **Enterprise** (`web_enterprise`) | No existe en el core Community; OCA `web_dark_mode` 19.0 declara `excludes: web_enterprise` | Opcional con OCA `web_dark_mode` |
| Studio, IA, firma, MPS, PLM, mantenimiento de equipos, *shop floor* | Enterprise | — | No se usan |

**Cambios de Odoo 19 que afectan la carga de datos** (verificados en el código fuente 19.0):
- **UoM sin categorías:** ahora se usa `uom.uom.relative_uom_id` + `relative_factor`.
- **Productos:** `product.template.type` (`consu`/`service`/`combo`) + `is_storable` (lo agrega `stock`).
- **RR. HH.:** el módulo `hr_contract` ya no existe; los contratos se manejan con `hr.version`.
- **Usuarios:** `res.users.group_ids` (antes `groups_id`) y `res.groups.privilege_id` (nuevo modelo `res.groups.privilege`).
- **Datos demo:** desde 18.3 ya no se cargan por defecto (`--with-demo`).

## 3.2 Módulos OCA portados a 19.0 (verificado en las ramas `19.0` de GitHub)

| Módulo OCA | Repo | Estado 19.0 | Uso propuesto |
|---|---|---|---|
| `quality_control_oca` (19.0.1.0.0), `quality_control_stock_oca` | OCA/manufacture | Portados | **Referencia**, no dependencia (ver 3.4). `quality_control_mrp_oca` **no** está portado a 19.0 |
| `auditlog` (19.0.2.0.2) | OCA/server-tools | Portado | **Fase 1**: auditoría de cambios para la sección de seguridad |
| `auto_backup` | OCA/server-tools | Portado | Opcional (se prefiere `pg_dump` por script) |
| `web_responsive` (19.0.1.1.2, Production/Stable) | OCA/web | Portado | Opcional (Odoo 19 ya es responsive) |
| `web_dark_mode` | OCA/web | Portado | Opcional (puntos extra de UI) |
| `web_environment_ribbon` | OCA/web | Portado | **Fase 1**: cinta "DESARROLLO" o "PRUEBAS" según el entorno |
| `mis_builder` | OCA/mis-builder | Portado (depende de `date_range` y `report_xlsx`) | No se usa (agrega complejidad) |
| `account_financial_report` | OCA/account-financial-reporting | Portado | Opcional |
| OCA/l10n-peru | — | La rama 19.0 existe pero **está vacía** | No hay EDI comunitario para 19.0 |

Los módulos OCA se instalan en la imagen Docker clonando **un commit fijo** (reproducible). No se usan submódulos de git.


## 3.3 Configuración y datos por área

Todo lo de esta sección es **Fase 1** (salvo lo marcado como **F2**) y se carga **por código** en `donofrio_base`:
- Datos XML/CSV con `noupdate` donde aplica, **un archivo por área**: así cada integrante hace commits en su área y se reducen los conflictos.
- Un `post_init_hook` para el plan contable, idioma y moneda.
- El script `scripts/cargar_transacciones.py`, que corre con `odoo shell` y una semilla fija, para generar 3-4 meses de movimientos con estacionalidad.

La interfaz web solo se usa para verificar y tomar capturas.

### a) Marketing y Ventas: `crm`, `sale_management`, `point_of_sale`, `l10n_pe_pos` (F1, Evelyn)

| Se configura | Datos de D'Onofrio que se cargan |
|---|---|
| Equipos de venta: Canal Moderno, Canal Tradicional, Heladeros | 3 equipos con sus jefes (usuarios ficticios) |
| Etapas CRM: Prospecto → Calificado → Propuesta → Negociación → Ganado | Unas 20 oportunidades: distribuidores regionales, autoservicios y bodegas; también **reclutamiento de heladeros** (campaña de verano) |
| Listas de precios: Mayorista, Bodega, Heladero (descuento supuesto), Campaña Navidad (panetón), Verano (helados) | 5 listas con reglas por categoría y fechas de vigencia |
| Unidades de venta: unidad y caja ×24 (UoM 19 relativa) | En los productos |
| Plantillas de cotización (paquete bodega, paquete campaña) | 2 plantillas |
| Punto de venta "Tienda de planta / Heladería Av. Venezuela" con boleta (`l10n_pe_pos`), pago en efectivo y Yape como diario genérico | 1 PdV, 2 métodos de pago |
| Clientes con tipo de identificación (RUC/DNI) y distrito (`l10n_pe`) | Unos 30 clientes ficticios: distribuidores, autoservicios genéricos ("Supermercado Ejemplo SAC"), bodegas y heladeros-concesionarios |
| **Heladeros sin F2** (alternativa estándar) | Pedido de venta diario al heladero-concesionario con la lista "Heladero" + devolución estándar de lo no vendido. Así se documenta el proceso TO-BE mínimo, y `donofrio_heladeros` (F2-M2) lo automatiza |

### b) Logística: `stock`, `product_expiry`, `stock_account` (F1, Orlando)

| Se configura | Datos que se cargan |
|---|---|
| Almacenes: **WH-LIM Planta Lima** y **WH-AQP CD Arequipa**; ruta de reabastecimiento Lima → Arequipa | 2 almacenes, 1 ruta |
| Ubicaciones: Cámara de congelación (−25 °C), Cámara de insumos refrigerados (2-6 °C), Almacén seco, Zona de despacho de triciclos | Unas 8 ubicaciones. En la F1, el rango de temperatura va en el nombre o la nota de la ubicación; en la **F2-M3** pasa a los campos `temp_min`/`temp_max` con control |
| Lotes y vencimientos: seguimiento **por lote** en producto terminado e insumos perecibles; **estrategia de retiro FEFO** (`product_expiry.removal_fefo`) en las categorías de producto | Vida útil supuesta: helado 12 meses, panetón 4 meses, chocolate 12 meses, leche 10 días; alerta 30 días antes |
| Operaciones en 2 pasos para el despacho (*pick* + *ship*) en Lima y en 1 paso en Arequipa | — |
| Valoración: FIFO automatizada en las categorías de terminados (con `stock_account`) | — |
| Inventario inicial | Ajuste de inventario por script con lotes y fechas de vencimiento escalonadas (algunos por vencer, para el KPI) |

### c) Producción: `mrp`, `mrp_account` (F1, Orlando) + `donofrio_calidad` (F2-M1)

| Se configura | Datos que se cargan |
|---|---|
| Centros de trabajo: Línea Helados (pasteurización → maduración → congelamiento → endurecimiento), Línea Chocolates (conchado → templado → moldeo), Línea Panetón (amasado → fermentación → horneado → enfriado → empaque) | 3 centros con capacidad y costo por hora supuestos |
| Listas de materiales (recetas) con operaciones. Las **instrucciones de cada operación** describen los controles (por ejemplo, "pasteurizar a 80-85 °C"), lo que en la F1 documenta los PCC sin código | Unas 12 BoM: helados (base láctea, pulpa de fruta, cobertura, palito, envoltura), chocolates (cacao, azúcar, leche en polvo, envoltura), panetón 900 g (harina, huevo, mantequilla, frutas confitadas, pasas, caja) |
| Productos terminados (nombres de referencia, supuesto S3) | Unos 25: paletas, conos, vasos, familiares 1 L, chocolates, panetón clásico, panetón premium |
| Insumos | Unos 20, con proveedor y tiempo de entrega |
| **F2-M1:** puntos de control de calidad (`donofrio_calidad`) | Pasteurización 80-85 °C, endurecimiento ≤ −18 °C, peso neto ±2 %, análisis microbiológico aprobado/rechazado, humedad del panetón |
| Órdenes de producción históricas | Las genera el script (con lotes) para los dashboards y la trazabilidad |

### d) Gerencia: `spreadsheet_dashboard*` + `ir.filters` (F1, Evelyn) + `donofrio_tablero` (F2-M4)

| Se configura | Contenido |
|---|---|
| **F1:** dashboards estándar de Community (`spreadsheet_dashboard`, `_sale`, `_stock_account`, y CRM y compras si están disponibles) | Sin código; de solo lectura en Community |
| **F1:** vistas pivote y gráficas guardadas por código (`ir.filters`, compartidas, en el menú de favoritos) | Ventas por línea, canal y mes (estacionalidad); producción por línea; stock por vencer en 30 días; top de clientes por canal |
| **F2-M4:** tablero gerencial OWL (acción de cliente) | Tarjetas de KPI: ventas del mes por canal, % de cumplimiento de producción, % de lotes aprobados*, stock por vencer, liquidaciones pendientes*, alertas de temperatura*; gráfico de ventas por mes con Chart.js (ya viene en Odoo). *Cada tarjeta aparece solo si su módulo está instalado |

### e) Extras: `purchase`, `purchase_stock`, `account` + `l10n_pe`, `hr`, `project` (F1)

| Módulo | Se configura | Datos |
|---|---|---|
| Compras (E) | Reglas de reabastecimiento mín./máx. para insumos; acuerdos de precio con proveedores | Unos 6 proveedores ficticios (lácteos, cacao, molino, frutas, envases, cartón) |
| Facturación + `l10n_pe` (E) | Plan contable PE, IGV 18 %, diarios de **Factura (01)** y **Boleta (03)**, nota de crédito (07), PEN, términos de pago 30/60; logo y colores de la compañía en el layout de reportes | Las facturas las genera el script desde los pedidos; aviso en el informe: **sin envío a SUNAT** |
| RR. HH. (E) | Departamentos (organigrama de [01 §1.5](01_alcance_escenario.md)), puestos y jefes | Unos 20 empleados ficticios; los heladeros se modelan como **contactos-concesionarios** (S4), no como empleados |
| Usuarios y grupos (O) | Un usuario por rol: gerente, jefe de ventas, vendedor, cajero PdV, jefe de almacén, jefe de producción, inspector de calidad, liquidador de heladeros, compras, contador; `ir.rule` del CD Arequipa | 10 usuarios con contraseñas de prueba desde `.env.example` (nunca en el código) |
| Project, mesa de servicios TI (E) | Proyecto, etapas y etiquetas ITIL ([09 §9.3](09_normas_marcos.md)) | 5 tickets de ejemplo |
| Seguridad (O) | `auth_totp`, `auth_totp_mail`, `auth_password_policy`, parámetros de *cooldown* | `ir.config_parameter` por XML |

Idioma `es_PE`, zona horaria `America/Lima` y moneda PEN se activan en el `post_init_hook`.

## 3.4 Mejoras y módulos propios, por fase

**Principio: cumplir todo lo que piden la plantilla y los lineamientos en la Fase 1, sin módulos propios de lógica. La Fase 2 agrega módulos propios uno a uno, con un punto de control antes de cada uno** (ver [04 §4.3](04_scrum_pmbok.md)).

### Fase 1: núcleo garantizado

| # | Elemento | Fase | Dueño | Justificación |
|---|---|---|---|---|
| 1 | **`donofrio_base`**: configuración y datos maestros por código (todo 3.3 F1) + `scripts/cargar_transacciones.py` + **tests** de datos, seguridad e integración de flujos estándar | **F1** | O (estructura y hooks), E (datos de su área) | Hace todo reproducible y es el único módulo propio garantizado: sostiene la sección 5.5 aunque no haya F2 |
| 2 | **Réplica PostgreSQL** (*streaming*) + scripts de backup y restauración | **F1** | O | Secciones 5.9 y 5.9b |
| 3 | **CI/CD** en GitHub Actions: lint + chequeo legacy + instalación y tests en Docker + *release* con zip | **F1** | O | Secciones 5.15 y 6.4-6.10; entregable "código comprimido" |
| 4 | **Nginx** con TLS, gzip y caché de `/web/assets` | **F1** | O | Seguridad (5.10-5.12) y WPO antes/después (4.6.4) |
| 5 | Seguridad Community: `auth_totp` + `auth_totp_mail`, `auth_password_policy`, *cooldown*, OCA **`auditlog`** + `web_environment_ribbon` | **F1** | O | Controles de la SoA ([09](09_normas_marcos.md)) |
| 6 | Pruebas no funcionales: **k6**, **OWASP ZAP baseline**, **Lighthouse**, **SUS** | **F1** | O (k6, ZAP), E (Lighthouse, SUS) | Tablas 22-24 y 6.9-6.13 |
| 7 | **SchemaSpy + script de diccionario de datos** | **F1** | O | 4.2.6-4.2.8 (núcleo); se vuelve a ejecutar con cada módulo de la F2 |
| 8 | Gerencia mínima: dashboards estándar + `ir.filters` | **F1** | E | Cubre el área "Dirección o Gerencia General" sin código |
| 9 | Mesa de servicios TI en Project (ITIL) | **F1** | E | ITIL 4 / ISO 20000-1 sin Helpdesk (Enterprise) |

### Fase 2: extensión (orden fijo, uno a uno, cada uno entregable por sí solo)

El orden y las HU de cada módulo están en [04 §4.5](04_scrum_pmbok.md). Con el plazo (viernes 27 de noviembre, 14:30), lo más probable es que solo entre M1; el resto queda como trabajo futuro si no alcanza.

| Orden | Módulo | Contenido | Dueño | Justificación del orden |
|---|---|---|---|---|
| **M1** | **`donofrio_calidad`** | Puntos de control (`donofrio.calidad.punto`), inspecciones (`donofrio.calidad.inspeccion` + líneas de medición) ligadas a `mrp.production` y `stock.lot`; estados borrador → en curso → aprobada/rechazada; un lote rechazado no se despacha; reporte QWeb **Certificado de calidad del lote** | O | Calidad es Enterprise y `quality_control_mrp_oca` no está portado a 19.0; es el corazón de Producción; da contenido al diagrama de clases, al ER y diccionario y a la 5.5; respalda ISO 9001/HACCP |
| **M2** | **`donofrio_heladeros`** | Liquidación diaria (`donofrio.liquidacion` + líneas: despachado, devuelto, merma, vendido calculado, precio de heladero, importe, comisión); borrador → despachado → liquidado; al liquidar crea y confirma un `sale.order`; reporte QWeb **Liquidación del heladero**; vista móvil | E | El proceso más reconocible de D'Onofrio (problema 1); código propio para Evelyn |
| **M3** | **Cadena de frío** (incremento de `donofrio_calidad`, tag propio) | `donofrio.temperatura` + `temp_min`/`temp_max` en `stock.location`; si sale de rango, crea una actividad; *cron* de lotes por vencer | O | El más pequeño; cierra los PCC de temperatura de HACCP; requiere M1 |
| **M4** | **`donofrio_tablero`** + branding | Acción de cliente OWL con `get_kpis()` (`_read_group`) y Chart.js; SCSS del backend y *favicon*; las tarjetas se adaptan a los módulos instalados | E | Gerencia ya está cubierta en la F1, así que tiene el menor valor marginal; mejora el front-end (4.6) y el WPO |
| Opc. 5 | App **Website**: landing "Únete como heladero" (→ lead en CRM) | Aviso de proyecto académico y `noindex` si se publica | E | Mejor historia de WPO |
| Opc. 6 | Monitoreo con Uptime Kuma sobre `/web/health` | — | O | Evidencia de SLA y del control 8.16 |
| Opc. 7 | VM en la nube + CD por SSH | Decisión abierta | O | La 4.3.8 se cubre con GitHub/GHCR aunque no haya VM |
| Opc. 8 | OCA `web_dark_mode` / `web_responsive` | — | E | Solo estética |

**Regla de entregabilidad:**
- Cada módulo se fusiona a `main` con su tag **solo cuando cumple la DoD del módulo**.
- Lo que quede a medias **no se fusiona**: se queda en su rama `feature/*` y se documenta como trabajo futuro, con su diseño (CU, wireframe, mockup, clases propuestas).
- Así la release entregada nunca contiene trabajo roto.

**Descartado por complejidad:**
- `mis_builder`.
- Pronóstico de demanda con ML.
- App móvil nativa.
- Integración con OSE/SUNAT.
- Multi-compañía para simular Froneri.
- Kubernetes: se menciona en la tabla 25 como "no aplica, se justifica".

### Por qué un módulo de calidad propio (M1) y no `quality_control_oca`

1. `quality_control_mrp_oca` (el enlace con la OP) **no está portado a 19.0**. Sin él, OCA solo cubre inspecciones genéricas y de *picking*.
2. La cadena de frío y el certificado por lote no existen en OCA.
3. Un modelo propio de unas 300 líneas es más fácil de explicar en la sustentación y aporta al diagrama de clases y al diccionario de datos.
4. El diseño de OCA (pruebas → preguntas → inspección) se cita como referencia en el informe.
5. **Sin la F2**, Calidad se documenta como limitación de Community con su diseño (CU, wireframes y clases propuestas) y con los controles de la F1: lotes, FEFO, instrucciones de operación y fecha de retiro.
