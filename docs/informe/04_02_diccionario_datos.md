# 4.2.8 Diccionario de datos del núcleo (tablas centrales)

> **Archivo generado** por [`scripts/diccionario_datos.py`](../../scripts/diccionario_datos.py); no se edita a mano. Origen: BD limpia con `donofrio_base`, `donofrio_calidad` y `donofrio_heladeros` instalados desde `develop` (Odoo 19.0, PostgreSQL 16).
>
> Formato de la «Tabla 5» de la plantilla: una tabla por entidad con su clave (PK/FK), campo, tipo, tamaño, si admite nulo y descripción. **Tipo y tamaño** salen de `information_schema`; la **descripción**, de la etiqueta y la ayuda del campo en `ir_model_fields` (es_PE). Tamaño: caracteres en `varchar`, `precisión,escala` en `numeric`, bytes en los tipos fijos y «variable» en `text` y `jsonb`. Las columnas que agregó un módulo propio a una tabla de otro módulo van marcadas con **[donofrio_base]**, **[donofrio_calidad]** o **[donofrio_heladeros]**.

## Resumen de las tablas centrales

| Área | Tabla | Modelo de Odoo | Módulo | Columnas | Filas (`donofrio_perf`) |
|---|---|---|---|---|---|
| Ventas y CRM | `sale_order` | `sale.order` | `sale` | 49 | 437 |
| Ventas y CRM | `sale_order_line` | `sale.order.line` | `sale` | 44 | 1.454 |
| Ventas y CRM | `crm_lead` | `crm.lead` | `crm` | 63 | 20 |
| Ventas y CRM | `pos_order` | `pos.order` | `point_of_sale` | 48 | 939 |
| Maestros | `res_partner` | `res.partner` | `base` | 87 | 63 |
| Maestros | `product_template` | `product.template` | `product` | 57 | 48 |
| Maestros | `product_product` | `product.product` | `product` | 17 | 48 |
| Maestros | `product_category` | `product.category` | `product` | 20 | 13 |
| Maestros | `product_pricelist` | `product.pricelist` | `product` | 10 | 6 |
| Maestros | `product_pricelist_item` | `product.pricelist.item` | `product` | 27 | 7 |
| Maestros | `product_supplierinfo` | `product.supplierinfo` | `product` | 20 | 22 |
| Maestros | `hr_employee` | `hr.employee` | `hr` | 50 | 22 |
| Inventario | `stock_warehouse` | `stock.warehouse` | `stock` | 43 | 2 |
| Inventario | `stock_location` | `stock.location` | `stock` | 24 | 30 |
| Inventario | `stock_picking_type` | `stock.picking.type` | `stock` | 53 | 24 |
| Inventario | `stock_picking` | `stock.picking` | `stock` | 32 | 1.647 |
| Inventario | `stock_move` | `stock.move` | `stock` | 65 | 6.063 |
| Inventario | `stock_move_line` | `stock.move.line` | `stock` | 28 | 6.535 |
| Inventario | `stock_lot` | `stock.lot` | `stock` | 19 | 488 |
| Inventario | `stock_quant` | `stock.quant` | `stock` | 22 | 1.737 |
| Inventario | `stock_warehouse_orderpoint` | `stock.warehouse.orderpoint` | `stock` | 22 | 22 |
| Producción | `mrp_bom` | `mrp.bom` | `mrp` | 23 | 12 |
| Producción | `mrp_bom_line` | `mrp.bom.line` | `mrp` | 14 | 71 |
| Producción | `mrp_production` | `mrp.production` | `mrp` | 39 | 188 |
| Producción | `mrp_workorder` | `mrp.workorder` | `mrp` | 25 | 734 |
| Producción | `mrp_workcenter` | `mrp.workcenter` | `mrp` | 22 | 3 |
| Producción | `mrp_routing_workcenter` | `mrp.routing.workcenter` | `mrp` | 14 | 47 |
| Compras | `purchase_order` | `purchase.order` | `purchase` | 40 | 101 |
| Compras | `purchase_order_line` | `purchase.order.line` | `purchase` | 34 | 368 |
| Facturación | `account_move` | `account.move` | `account` | 75 | 3.369 |
| Facturación | `account_move_line` | `account.move.line` | `account` | 61 | 17.852 |
| Facturación | `account_journal` | `account.journal` | `account` | 34 | 11 |
| Seguridad y mesa de servicios | `res_users` | `res.users` | `base` | 25 | 14 |
| Seguridad y mesa de servicios | `res_groups` | `res.groups` | `base` | 11 | 76 |
| Seguridad y mesa de servicios | `auditlog_rule` | `auditlog.rule` | `auditlog` | 18 | 4 |
| Seguridad y mesa de servicios | `project_task` | `project.task` | `project` | 41 | n/d |
| Calidad (M1) | `donofrio_calidad_punto` | `donofrio.calidad.punto` | `donofrio_calidad` | 13 | n/d |
| Calidad (M1) | `donofrio_calidad_inspeccion` | `donofrio.calidad.inspeccion` | `donofrio_calidad` | 13 | n/d |
| Calidad (M1) | `donofrio_calidad_linea` | `donofrio.calidad.linea` | `donofrio_calidad` | 12 | n/d |
| Heladeros (M2) | `donofrio_liquidacion` | `donofrio.liquidacion` | `donofrio_heladeros` | 19 | n/d |
| Heladeros (M2) | `donofrio_liquidacion_linea` | `donofrio.liquidacion.linea` | `donofrio_heladeros` | 13 | n/d |
| Cadena de frío (M3) | `donofrio_temperatura` | `donofrio.temperatura` | `donofrio_calidad` | 12 | n/d |

## Lo que agregan los módulos propios al esquema

`donofrio_base` **no crea tablas propias** en la Fase 1: sus registros (compañía, almacenes, productos, clientes, listas de precios, listas de materiales, empleados, usuarios, grupos y reglas) se cargan por XML/CSV en las tablas de Odoo de arriba. En el esquema solo agrega:

* `project_task.sla_estado` (varchar, calculada y almacenada): Cumplimiento del SLA.

`donofrio_calidad` (M1 y el incremento M3 de cadena de frío, Fase 2) **sí crea tablas propias**: `donofrio_calidad_inspeccion`, `donofrio_calidad_linea`, `donofrio_calidad_punto`, `donofrio_temperatura`.

Además agrega estas columnas a tablas de otros módulos:

* `stock_location.control_temperatura` (boolean): Controlar temperatura.
* `stock_location.temp_min` (double precision): Temperatura mínima (°C).
* `stock_location.temp_max` (double precision): Temperatura máxima (°C).
* `stock_lot.alerta_vencimiento_fecha` (timestamp): Alerta de vencimiento enviada.

`donofrio_heladeros` (M2, Fase 2) **sí crea tablas propias**: `donofrio_liquidacion`, `donofrio_liquidacion_linea`. No agrega columnas a las tablas de otros módulos.

## Ventas y CRM

### Tabla 4.2.8-1. `sale_order`

**Orden de venta** · modelo `sale.order` · módulo `sale` · 49 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `campaign_id` | integer | 4 B | Sí | Campaña → `utm_campaign` — Este es el nombre que te ayuda a identificar tus campañas, por ejemplo: descuentos_octubre, rebajas_de_navidad |
| FK | `source_id` | integer | 4 B | Sí | Origen → `utm_source` — Esta es la fuente del enlace. Por ejemplo: motor de búsqueda, otro dominio o nombre de lista de correos electrónicos |
| FK | `medium_id` | integer | 4 B | Sí | Medio → `utm_medium` — Este es el método de entrega. Por ejemplo: correo postal, correo electrónico, publicidad web |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `partner_id` | integer | 4 B | No | Cliente → `res_partner` |
| FK | `pending_email_template_id` | integer | 4 B | Sí | Plantilla de correo pendiente → `mail_template` |
| FK | `journal_id` | integer | 4 B | Sí | Diario de facturación → `account_journal` — Si se establece, las órdenes de venta se facturarán en este diario. De lo contrario, se utilizará el diario de ventas con la secuencia má… |
| FK | `partner_invoice_id` | integer | 4 B | No | Dirección de factura → `res_partner` |
| FK | `partner_shipping_id` | integer | 4 B | No | Dirección de entrega → `res_partner` |
| FK | `fiscal_position_id` | integer | 4 B | Sí | Posición fiscal → `account_fiscal_position` — Las posiciones fiscales se utilizan para adaptar impuestos y cuentas para determinados clientes u órdenes de venta o facturas. El valor p… |
| FK | `payment_term_id` | integer | 4 B | Sí | Términos de pago → `account_payment_term` |
| FK | `preferred_payment_method_line_id` | integer | 4 B | Sí | Método de pago → `account_payment_method_line` |
| FK | `pricelist_id` | integer | 4 B | Sí | Lista de precios → `product_pricelist` — Si modifica la lista de precios, solo afectará a las nuevas líneas que agregó. |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `user_id` | integer | 4 B | Sí | Vendedor → `res_users` |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `name` | varchar | variable | No | Referencia de la orden |
|  | `state` | varchar | variable | Sí | Estado |
|  | `client_order_ref` | varchar | variable | Sí | Referencia del cliente |
|  | `origin` | varchar | variable | Sí | Documento origen — Referencia del documento que generó esta solicitud de orden de venta. |
|  | `reference` | varchar | variable | Sí | Ref. de pago — La comunicación de pago de esta orden de venta. |
|  | `signed_by` | varchar | variable | Sí | Firmada por |
|  | `invoice_status` | varchar | variable | Sí | Estado de la factura |
|  | `validity_date` | date | 4 B | Sí | Vencimiento — Validity of the quotation. After this date, you will no longer be able to sign and pay it. |
|  | `note` | text | variable | Sí | Términos y condiciones |
|  | `currency_rate` | numeric | variable | Sí | Tasa de cambio |
|  | `amount_untaxed` | numeric | variable | Sí | Subtotal |
|  | `amount_tax` | numeric | variable | Sí | Impuestos |
|  | `amount_total` | numeric | variable | Sí | Total |
|  | `locked` | boolean | 1 B | Sí | Bloqueado — No puede modificar las órdenes bloqueadas. |
|  | `require_signature` | boolean | 1 B | Sí | Firma en línea — Solicite al cliente que firme en línea para confirmar la orden. |
|  | `require_payment` | boolean | 1 B | Sí | Pago en línea — Solicite al cliente que pague en línea para confirmar la orden. |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |
|  | `commitment_date` | timestamp | 8 B | Sí | Fecha de entrega — Esta es la fecha de entrega prometida al cliente. Si se establece, la orden de entrega se programará en función de esta fecha en lugar de… |
|  | `date_order` | timestamp | 8 B | No | Fecha de la orden — Fecha de creación del borrador o envío de las órdenes, Fecha de confirmación de las órdenes confirmadas. |
|  | `signed_on` | timestamp | 8 B | Sí | Firmado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `prepayment_percent` | double precision | 8 B | Sí | Porcentaje de pago anticipado — El porcentaje del importe que el cliente debe pagar para confirmar la orden. |
| FK | `opportunity_id` | integer | 4 B | Sí | Oportunidad → `crm_lead` |
| FK | `incoterm` | integer | 4 B | Sí | Incoterm → `account_incoterms` — Los términos de comercio internacional son una serie de condiciones comerciales que se usan en las transacciones internacionales. |
| FK | `warehouse_id` | integer | 4 B | Sí | Almacén → `stock_warehouse` |
|  | `incoterm_location` | varchar | variable | Sí | Ubicación del incoterm |
|  | `picking_policy` | varchar | variable | No | Política de envío — Si entregas todos los productos al mismo tiempo, la orden de entrega se programará según el mayor plazo de entrega del producto. De lo co… |
|  | `delivery_status` | varchar | variable | Sí | Estado de la entrega — Azul: Sin entregar/Entrega en curso Naranja: Entregado de forma parcial Verde: Entregado |
|  | `effective_date` | timestamp | 8 B | Sí | Fecha efectiva — Fecha de finalización de la primera orden de entrega. |

### Tabla 4.2.8-2. `sale_order_line`

**Línea de la orden de venta** · modelo `sale.order.line` · módulo `sale` · 44 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `order_id` | integer | 4 B | No | Referencia de la orden → `sale_order` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `order_partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `salesman_id` | integer | 4 B | Sí | Vendedor → `res_users` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `product_uom_id` | integer | 4 B | Sí | Unidad → `uom_uom` |
| FK | `linked_line_id` | integer | 4 B | Sí | Línea de orden de venta vinculada → `sale_order_line` |
| FK | `combo_item_id` | integer | 4 B | Sí | Artículo del combo → `product_combo_item` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `state` | varchar | variable | Sí | Estado de la orden |
|  | `display_type` | varchar | variable | Sí | Mostrar tipo |
|  | `virtual_id` | varchar | variable | Sí | Virtual |
|  | `linked_virtual_id` | varchar | variable | Sí | Vinculado virtual |
|  | `qty_delivered_method` | varchar | variable | Sí | Método para actualizar la cantidad entregada — Según la configuración del producto, la cantidad enviada se puede calcular de forma automática con uno de los siguientes mecanismos: - Ma… |
|  | `invoice_status` | varchar | variable | Sí | Estado de la factura |
|  | `analytic_distribution` | jsonb | variable | Sí | Distribución analítica |
|  | `extra_tax_data` | jsonb | variable | Sí | Datos adicionales sobre impuestos |
|  | `name` | text | variable | No | Descripción |
|  | `product_uom_qty` | numeric | variable | No | Cantidad |
|  | `price_unit` | numeric | variable | No | Precio unitario |
|  | `discount` | numeric | variable | Sí | Descuento (%) |
|  | `price_subtotal` | numeric | variable | Sí | Subtotal |
|  | `price_total` | numeric | variable | Sí | Total |
|  | `price_reduce_taxexcl` | numeric | variable | Sí | Precio reducido con impuestos excluidos |
|  | `price_reduce_taxinc` | numeric | variable | Sí | Precio reducido con impuestos incluidos |
|  | `qty_delivered` | numeric | variable | Sí | Cantidad de entrega |
|  | `qty_invoiced` | numeric | variable | Sí | Cantidad facturada |
|  | `qty_to_invoice` | numeric | variable | Sí | Cantidad a facturar |
|  | `untaxed_amount_invoiced` | numeric | variable | Sí | Importe sin impuestos facturado |
|  | `untaxed_amount_to_invoice` | numeric | variable | Sí | Importe sin impuestos a facturar |
|  | `is_downpayment` | boolean | 1 B | Sí | Es un anticipo — Los anticipos se producen cuando se crean facturas desde una orden de venta. No se copian al duplicar una orden. |
|  | `is_expense` | boolean | 1 B | Sí | Es gasto — Es verdadero si la línea de orden de venta proviene de un gasto o de las facturas de un proveedor |
|  | `collapse_prices` | boolean | 1 B | Sí | Colapsar precios |
|  | `collapse_composition` | boolean | 1 B | Sí | Colapsar composición |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `technical_price_unit` | double precision | 8 B | Sí | Precio unitario técnico |
|  | `price_tax` | double precision | 8 B | Sí | Total de impuestos |
|  | `customer_lead` | double precision | 8 B | No | Plazo de entrega — Número de días entre la confirmación de la orden y la entrega de los productos al cliente |
| FK | `warehouse_id` | integer | 4 B | Sí | Almacén → `stock_warehouse` |

### Tabla 4.2.8-3. `crm_lead`

**Lead** · modelo `crm.lead` · módulo `crm` · 63 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `campaign_id` | integer | 4 B | Sí | Campaña → `utm_campaign` — Este es el nombre que te ayuda a identificar tus campañas, por ejemplo: descuentos_octubre, rebajas_de_navidad |
| FK | `source_id` | integer | 4 B | Sí | Origen → `utm_source` — Esta es la fuente del enlace. Por ejemplo: motor de búsqueda, otro dominio o nombre de lista de correos electrónicos |
| FK | `medium_id` | integer | 4 B | Sí | Medio → `utm_medium` — Este es el método de entrega. Por ejemplo: correo postal, correo electrónico, publicidad web |
|  | `message_bounce` | integer | 4 B | Sí | Devuelto — Número de correos electrónicos devueltos de este contacto |
| FK | `user_id` | integer | 4 B | Sí | Vendedor → `res_users` |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `stage_id` | integer | 4 B | Sí | Etapa → `crm_stage` |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `recurring_plan` | integer | 4 B | Sí | Plan recurrente → `crm_recurring_plan` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` — Contacto vinculado (opcional). Usualmente se crea al convertir el lead. Puede encontrar un contacto por su nombre, identificación fiscal,… |
| FK | `lang_id` | integer | 4 B | Sí | Idioma → `res_lang` |
| FK | `state_id` | integer | 4 B | Sí | Estado → `res_country_state` |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `lost_reason_id` | integer | 4 B | Sí | Motivo de pérdida → `crm_lost_reason` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `phone_sanitized` | varchar | variable | Sí | Número depurado — Campo utilizado para almacenar el número de teléfono válido. Ayuda a agilizar las búsquedas y comparaciones. |
|  | `email_normalized` | varchar | variable | Sí | Correo electrónico normalizado — Este campo se utiliza para buscar en la dirección de correo electrónico, ya que el campo de correo electrónico principal puede contener m… |
|  | `email_cc` | varchar | variable | Sí | CC del correo electrónico |
|  | `name` | varchar | variable | No | Oportunidad |
|  | `referred` | varchar | variable | Sí | Recomendado por |
|  | `type` | varchar | variable | No | Tipo |
|  | `priority` | varchar | variable | Sí | Prioridad |
|  | `contact_name` | varchar | variable | Sí | Nombre del contacto |
|  | `partner_name` | varchar | variable | Sí | Nombre de la empresa — El nombre de la futura empresa del contacto que se creará al convertir el lead en oportunidad |
|  | `function` | varchar | variable | Sí | Puesto de trabajo |
|  | `email_from` | varchar | variable | Sí | Correo electrónico |
|  | `email_domain_criterion` | varchar | variable | Sí | Critero de dominio de correo electrónico |
|  | `phone` | varchar | variable | Sí | Teléfono |
|  | `phone_state` | varchar | variable | Sí | Calidad de llamada |
|  | `email_state` | varchar | variable | Sí | Calidad de correo electrónico |
|  | `website` | varchar | variable | Sí | Sitio web — Sitio web del contacto |
|  | `street` | varchar | variable | Sí | Calle |
|  | `street2` | varchar | variable | Sí | Calle2 |
|  | `zip` | varchar | variable | Sí | Código postal |
|  | `city` | varchar | variable | Sí | Ciudad |
|  | `won_status` | varchar | variable | Sí | Ganado/Perdido |
|  | `date_deadline` | date | 4 B | Sí | Cierre esperado — Fecha estimada en la que se ganará la oportunidad. |
|  | `lead_properties` | jsonb | variable | Sí | Propiedades |
|  | `description` | text | variable | Sí | Notas |
|  | `expected_revenue` | numeric | variable | Sí | Ingreso esperado |
|  | `prorated_revenue` | numeric | variable | Sí | Ingreso prorrateado |
|  | `recurring_revenue` | numeric | variable | Sí | Ingresos recurrentes |
|  | `recurring_revenue_monthly` | numeric | variable | Sí | MMR esperado |
|  | `recurring_revenue_monthly_prorated` | numeric | variable | Sí | MRR prorrateado |
|  | `recurring_revenue_prorated` | numeric | variable | Sí | Ingresos recurrentes prorrateados |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `date_closed` | timestamp | 8 B | Sí | Fecha de cierre |
|  | `date_automation_last` | timestamp | 8 B | Sí | Última acción |
|  | `date_open` | timestamp | 8 B | Sí | Fecha de asignación |
|  | `date_last_stage_update` | timestamp | 8 B | Sí | Última actualización de la etapa |
|  | `date_conversion` | timestamp | 8 B | Sí | Fecha de conversión |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `day_open` | double precision | 8 B | Sí | Días hasta asignar |
|  | `day_close` | double precision | 8 B | Sí | Días para el cierre |
|  | `probability` | double precision | 8 B | Sí | Probabilidad |
|  | `automated_probability` | double precision | 8 B | Sí | Probabilidad automatizada |
|  | `reveal_id` | varchar | variable | Sí | Mostrar ID |
|  | `iap_enrich_done` | boolean | 1 B | Sí | Enriquecimiento terminado — Si el servicio de compras dentro de la aplicación para el enriquecimiento de leads basado en correo electrónico se ha realizado en este l… |
| FK | `lead_mining_request_id` | integer | 4 B | Sí | Solicitud de minado de leads → `crm_iap_lead_mining_request` |

### Tabla 4.2.8-4. `pos_order`

**Órdenes del punto de venta** · modelo `pos.order` · módulo `point_of_sale` · 48 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Empleado → `res_users` — Empleado que usa la caja registradora. |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `pricelist_id` | integer | 4 B | Sí | Lista de precios → `product_pricelist` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
|  | `sequence_number` | integer | 4 B | Sí | Número de secuencia — Un número de secuencia único para la sesión para la orden. Será negativo si lo generó el cliente |
| FK | `session_id` | integer | 4 B | Sí | Sesión → `pos_session` |
| FK | `config_id` | integer | 4 B | Sí | Punto de venta → `pos_config` |
| FK | `account_move` | integer | 4 B | Sí | Recibo/Factura → `account_move` |
| FK | `preset_id` | integer | 4 B | Sí | Preestablecido → `pos_preset` |
|  | `nb_print` | integer | 4 B | Sí | Número de copias |
| FK | `sale_journal` | integer | 4 B | Sí | Diario de ventas → `account_journal` — Diario contable que se utiliza para registrar asientos contables de sesiones de PdV y pagos de factura de PdV. |
| FK | `fiscal_position_id` | integer | 4 B | Sí | Posición fiscal → `account_fiscal_position` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `name` | varchar | variable | No | Ref. de la orden |
|  | `last_order_preparation_change` | varchar | variable | Sí | Último cambio de preparación — Último estado impreso de la orden |
|  | `state` | varchar | variable | Sí | Estado |
|  | `floating_order_name` | varchar | variable | Sí | Nombre de la orden |
|  | `pos_reference` | varchar | variable | Sí | Número de recibo |
|  | `ticket_code` | varchar | variable | Sí | Código de ticket — Código alfanumérico de 5 dígitos que el usuario del portal debe usar para solicitar una factura. |
|  | `tracking_number` | varchar | variable | Sí | Número de orden |
|  | `uuid` | varchar | variable | Sí | UUID |
|  | `email` | varchar | variable | Sí | Correo electrónico |
|  | `mobile` | varchar | variable | Sí | Celular |
|  | `source` | varchar | variable | Sí | Origen |
|  | `shipping_date` | date | 4 B | Sí | Fecha de envío |
|  | `general_customer_note` | text | variable | Sí | Nota general para el cliente |
|  | `internal_note` | text | variable | Sí | Nota interna |
|  | `amount_difference` | numeric | variable | Sí | Diferencia |
|  | `amount_tax` | numeric | variable | No | Impuestos |
|  | `amount_total` | numeric | variable | No | Total |
|  | `amount_paid` | numeric | variable | No | Pagado |
|  | `amount_return` | numeric | variable | No | Devuelto |
|  | `currency_rate` | numeric | variable | Sí | Tasa de cambio — El tipo de cambio de la divisa a la divisa del tipo de cambio aplicable en la fecha de la orden |
|  | `tip_amount` | numeric | variable | Sí | Monto de la propina |
|  | `is_refund` | boolean | 1 B | Sí | Es un reembolso |
|  | `to_invoice` | boolean | 1 B | Sí | Por facturar |
|  | `is_tipped` | boolean | 1 B | Sí | ¿Se aplicó una propina? |
|  | `has_deleted_line` | boolean | 1 B | Sí | Tiene una línea eliminada |
|  | `date_order` | timestamp | 8 B | Sí | Fecha |
|  | `preset_time` | timestamp | 8 B | Sí | Hora — Hora del día para la orden |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `employee_id` | integer | 4 B | Sí | Cajero → `hr_employee` — El empleado que usa la caja registradora. |
|  | `cashier` | varchar | variable | Sí | Nombre del cajero |
|  | `next_online_payment_amount` | numeric | variable | Sí | La siguiente cantidad que pagar en línea |

## Maestros

### Tabla 4.2.8-5. `res_partner`

**Contacto** · modelo `res.partner` · módulo `base` · 87 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `name` | varchar | variable | Sí | Nombre |
| FK | `parent_id` | integer | 4 B | Sí | Empresa relacionada → `res_partner` |
| FK | `user_id` | integer | 4 B | Sí | Vendedor → `res_users` — El usuario interno a cargo de este contacto. |
| FK | `state_id` | integer | 4 B | Sí | Estado → `res_country_state` |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `industry_id` | integer | 4 B | Sí | Industria → `res_partner_industry` |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `commercial_partner_id` | integer | 4 B | Sí | Entidad comercial → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `complete_name` | varchar | variable | Sí | Nombre completo |
|  | `ref` | varchar | variable | Sí | Referencia |
|  | `lang` | varchar | variable | Sí | Idioma — Todos los correos electrónicos y documentos enviados a este contacto se traducirán a este idioma. |
|  | `tz` | varchar | variable | Sí | Zona horaria — Al imprimir documentos y exportar e importar datos, los valores de fechas y horas se calculan con base en esta zona horaria. Si no ha con… |
|  | `vat` | varchar | variable | Sí | Número de Identificación — Número de identificación para el tipo seleccionado |
|  | `company_registry` | varchar | variable | Sí | ID de la empresa — El número de registro de la empresa. Úselo si es diferente al de la identificación fiscal. Debe ser único para todos los contactos del mi… |
|  | `website` | varchar | variable | Sí | Enlace del sitio web |
|  | `function` | varchar | variable | Sí | Puesto de trabajo |
|  | `type` | varchar | variable | Sí | Tipo de dirección |
|  | `street` | varchar | variable | Sí | Calle |
|  | `street2` | varchar | variable | Sí | Calle2 |
|  | `zip` | varchar | variable | Sí | Código postal |
|  | `city` | varchar | variable | Sí | Ciudad |
|  | `email` | varchar | variable | Sí | Correo electrónico |
|  | `phone` | varchar | variable | Sí | Teléfono |
|  | `commercial_company_name` | varchar | variable | Sí | Entidad del nombre de la empresa |
|  | `company_name` | varchar | variable | Sí | Nombre de la empresa |
|  | `properties` | jsonb | variable | Sí | Propiedades |
|  | `barcode` | jsonb | variable | Sí | Código de barras — Use el código de barras para identificar este contacto. |
|  | `comment` | text | variable | Sí | Notas |
|  | `partner_latitude` | numeric | variable | Sí | Geo latitud |
|  | `partner_longitude` | numeric | variable | Sí | Geo longitud |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `employee` | boolean | 1 B | Sí | Empleado — Si este contacto es un empleado. |
|  | `is_company` | boolean | 1 B | Sí | Es una empresa — Marque esta casilla si el contacto es una empresa. De lo contrario, es una persona. |
|  | `partner_share` | boolean | 1 B | Sí | Compartir contacto — Ya sea cliente (no usuario) o usuario compartido. Indique si el contacto actual es un cliente sin acceso o con acceso limitado creado par… |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `message_bounce` | integer | 4 B | Sí | Devuelto — Número de correos electrónicos devueltos de este contacto |
|  | `email_normalized` | varchar | variable | Sí | Correo electrónico normalizado — Este campo se utiliza para buscar en la dirección de correo electrónico, ya que el campo de correo electrónico principal puede contener m… |
|  | `signup_type` | varchar | variable | Sí | Tipo de token de registro |
|  | `calendar_last_notif_ack` | timestamp | 8 B | Sí | Última notificación marcada como leída desde el calendario principal |
|  | `phone_sanitized` | varchar | variable | Sí | Número depurado — Campo utilizado para almacenar el número de teléfono válido. Ayuda a agilizar las búsquedas y comparaciones. |
|  | `specific_property_product_pricelist` | jsonb | variable | Sí | Propiedad específica de la lista de precios del producto |
| FK | `city_id` | integer | 4 B | Sí | ID de la ciudad → `res_city` |
|  | `street_name` | varchar | variable | Sí | Nombre de la calle |
|  | `street_number` | varchar | variable | Sí | Casa |
|  | `street_number2` | varchar | variable | Sí | Puerta |
| FK | `invoice_template_pdf_report_id` | integer | 4 B | Sí | Reporte de la factura → `ir_act_report_xml` |
|  | `supplier_rank` | integer | 4 B | Sí | Rango de proveedor |
|  | `customer_rank` | integer | 4 B | Sí | Rango del cliente |
|  | `autopost_bills` | varchar | variable | No | Registrar facturas en automático — Registrar facturas en automático para este contacto de confianza |
|  | `credit_limit` | jsonb | variable | Sí | Límite de crédito — Límite de crédito específico para este contacto. |
|  | `property_account_payable_id` | jsonb | variable | Sí | Cuenta por pagar |
|  | `property_account_receivable_id` | jsonb | variable | Sí | Cuenta por cobrar |
|  | `property_account_position_id` | jsonb | variable | Sí | Posición fiscal — La posición fiscal determina los impuestos/cuentas que se utilizan para este contacto. |
|  | `property_payment_term_id` | jsonb | variable | Sí | Términos de pago del cliente |
|  | `property_supplier_payment_term_id` | jsonb | variable | Sí | Términos de pago de proveedor |
|  | `trust` | jsonb | variable | Sí | Grado de confianza en este deudor |
|  | `ignore_abnormal_invoice_date` | jsonb | variable | Sí | Ignorar fecha de facturación anormal |
|  | `ignore_abnormal_invoice_amount` | jsonb | variable | Sí | Ignorar importe de facturación anormal |
|  | `invoice_sending_method` | jsonb | variable | Sí | Envío de facturas |
|  | `invoice_edi_format_store` | jsonb | variable | Sí | Almacenamiento de formato EDI de factura |
|  | `property_outbound_payment_method_line_id` | jsonb | variable | Sí | Línea de método de pago de salida de la propiedad |
|  | `property_inbound_payment_method_line_id` | jsonb | variable | Sí | Línea de método de pago de entrada de la propiedad |
|  | `property_stock_customer` | jsonb | variable | Sí | Ubicación del cliente — La ubicación de existencias que se utiliza como destino al enviar artículos a este contacto. |
|  | `property_stock_supplier` | jsonb | variable | Sí | Ubicación del proveedor — La ubicación de existencias que se utiliza como origen al recibir productos de este contacto. |
|  | `picking_warn_msg` | text | variable | Sí | Mensaje para recolección de existencias |
|  | `global_location_number` | varchar | variable | Sí | GLN — Número global de localización |
|  | `peppol_endpoint` | varchar | variable | Sí | Punto de conexión de Peppol — El identificador único que utiliza la facturación BIS 3.0 y sus derivados, también conocido como "ID del punto extremo". |
|  | `peppol_eas` | varchar | variable | Sí | Dirección electrónica de Peppol (EAS) — El código que se utiliza para identificar el punto extremo para la facturación BIS 3.0 y sus derivadas. La lista se encuentra disponible… |
|  | `vies_valid` | boolean | 1 B | Sí | Válido dentro de la Comunidad Europea — Los números de IVA europeos se verifican de forma automática en la base de datos VIES. |
| FK | `buyer_id` | integer | 4 B | Sí | Comprador → `res_users` |
|  | `property_purchase_currency_id` | jsonb | variable | Sí | Moneda del proveedor — Esta moneda se usará para compras del contacto actual. |
|  | `receipt_reminder_email` | jsonb | variable | Sí | Recordatorio de entrega — Envíe automáticamente un correo electrónico de confirmación al proveedor X días antes de la fecha de entrega prevista. En este correo le… |
|  | `reminder_date_before_receipt` | jsonb | variable | Sí | Días antes de la recepción — Número de días para enviar un correo electrónico de recordatorio antes de la fecha de recepción prometida |
|  | `purchase_warn_msg` | text | variable | Sí | Mensaje para la orden de compra |
| FK | `l10n_latam_identification_type_id` | integer | 4 B | Sí | Tipo de Identificación → `l10n_latam_identification_type` — Tipo de identificación |
|  | `suggest_days` | integer | 4 B | Sí | Días sugeridos |
|  | `suggest_percent` | integer | 4 B | Sí | Porcentaje sugerido |
|  | `suggest_based_on` | varchar | variable | Sí | Sugerir según |
|  | `group_rfq` | varchar | variable | No | Agrupar solicitud de cotización — Define si las solicitudes de cotización se deben agrupar según la recepción esperada, excepto en las operaciones de triangulación de órde… |
|  | `group_on` | varchar | variable | No | Día de la semana |
|  | `sale_warn_msg` | text | variable | Sí | Mensaje para la orden de venta |
| FK | `l10n_pe_district` | integer | 4 B | Sí | Distrito → `l10n_pe_res_city_district` — Los distritos forman parte de una ciudad o provincia |

### Tabla 4.2.8-6. `product_template`

**Producto** · modelo `product.template` · módulo `product` · 57 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Proporciona el orden de secuencia al mostrar una lista de productos |
| FK | `categ_id` | integer | 4 B | Sí | Categoría del producto → `product_category` |
| FK | `uom_id` | integer | 4 B | No | Unidad → `uom_uom` — Unidad de medida de uso predeterminado para todas las operaciones de existencias. |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `type` | varchar | variable | No | Tipo de producto — Los bienes son productos materiales tangibles que usted proporciona. Los servicios son productos inmateriales que usted proporciona. |
|  | `service_tracking` | varchar | variable | No | Crear en la orden |
|  | `default_code` | varchar | variable | Sí | Referencia interna |
|  | `name` | jsonb | variable | No | Nombre |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `description_purchase` | jsonb | variable | Sí | Descripción de compra |
|  | `description_sale` | jsonb | variable | Sí | Descripción de ventas — La descripción del producto que le quiera dar a sus clientes. Se copiará esta descripción a cada orden de venta y entrega, así como a las… |
|  | `product_properties` | jsonb | variable | Sí | Propiedades |
|  | `list_price` | numeric | variable | Sí | Precio de venta — Precio al que se vende el producto a los clientes. |
|  | `volume` | numeric | variable | Sí | Volumen |
|  | `weight` | numeric | variable | Sí | Peso |
|  | `sale_ok` | boolean | 1 B | Sí | Ventas |
|  | `purchase_ok` | boolean | 1 B | Sí | Compras |
|  | `active` | boolean | 1 B | Sí | Activo — Si no está marcado, permitirá ocultar el producto sin eliminarlo. |
|  | `can_image_1024_be_zoomed` | boolean | 1 B | Sí | ¿Se puede ampliar la imagen 1024? |
|  | `has_configurable_attributes` | boolean | 1 B | Sí | Es un producto configurable |
|  | `is_favorite` | boolean | 1 B | Sí | Favorito |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `property_account_income_id` | jsonb | variable | Sí | Cuenta de ingresos — Mantén este campo vacío para usar el valor predeterminado de la categoría del producto. |
|  | `property_account_expense_id` | jsonb | variable | Sí | Cuenta de gastos — Mantén este campo vacío para usar el valor predeterminado de la categoría de producto. Si se configura la contabilidad anglosajona con el… |
|  | `sale_delay` | integer | 4 B | Sí | Plazo de entrega al cliente — El plazo de entrega en días. Es el número de días prometidos al cliente entre la confirmación de la orden de venta y la entrega. |
| FK | `lot_sequence_id` | integer | 4 B | Sí | Secuencia de los números de serie o lote → `ir_sequence` — Campo técnico: El registro Ir.Sequence que se utiliza para generar los números de serie o lote para este producto. |
|  | `tracking` | varchar | variable | No | Seguimiento — Asegure la trazabilidad de los productos almacenables en su almacén. |
|  | `responsible_id` | jsonb | variable | Sí | Responsable — Este usuario será responsable de las próximas actividades relacionadas con las operaciones logísticas de este producto. |
|  | `property_stock_production` | jsonb | variable | Sí | Ubicación de producción — Se usará esta ubicación de existencias en lugar de la predeterminada, como la ubicación origen para los movimientos de existencias genera… |
|  | `property_stock_inventory` | jsonb | variable | Sí | Ubicación de inventario — Se usará esta ubicación de existencias, en lugar de la predeterminada, como la ubicación origen para los movimientos de existencias gener… |
|  | `description_picking` | jsonb | variable | Sí | Descripción en recolección |
|  | `description_pickingout` | jsonb | variable | Sí | Descripción en las órdenes de entrega |
|  | `description_pickingin` | jsonb | variable | Sí | Descripción en recepciones |
|  | `is_storable` | boolean | 1 B | Sí | Rastrear inventario — Los productos almacenables son productos para los que gestiona el inventario. |
|  | `expiration_time` | integer | 4 B | Sí | Fecha de caducidad — Número de días después de la recepción de los productos (del proveedor o de las existencias después de la producción) después de los cual… |
|  | `use_time` | integer | 4 B | Sí | Fecha de consumo preferente — Número de días antes de la fecha de caducidad después de los cuales los bienes se empiezan a deteriorar sin llegar a representar un pelig… |
|  | `removal_time` | integer | 4 B | Sí | Fecha de remoción — Número de días antes de la fecha de caducidad después del que los productos deben ser retirados del inventario y que deben dejar de ser c… |
|  | `alert_time` | integer | 4 B | Sí | Fecha de alerta — Número de días antes de la fecha de caducidad después de los cuales se debe emitir una alarma para el número de lote o serie. Se calcular… |
|  | `use_expiration_date` | boolean | 1 B | Sí | Usar fecha de caducidad — Si la casilla está seleccionada puede especificar fechas para gestionar la caducidad de un producto, ya sea en el producto o en sus númer… |
|  | `purchase_method` | varchar | variable | Sí | Política de control — Sobre cantidades ordenadas: Controla las facturas según las cantidades solicitadas. Sobre cantidades recibidas: Controla las facturas seg… |
|  | `purchase_line_warn_msg` | text | variable | Sí | Mensaje para la línea de la orden de compra |
|  | `property_price_difference_account_id` | jsonb | variable | Sí | Cuenta de diferencia de precio — Con valuación perpetua, esta cuenta almacena la diferencia de precio entre el precio estándar y el precio de la factura. |
|  | `lot_valuated` | boolean | 1 B | Sí | Valuación por lote o número de serie — Si se encuentra seleccionado, la valoración será específica para cada número de serie o lote. |
|  | `pos_sequence` | integer | 4 B | Sí | Secuencia del PdV — Determine el orden de visualización en la terminal de PdV |
|  | `public_description` | jsonb | variable | Sí | Descripción del producto |
|  | `available_in_pos` | boolean | 1 B | Sí | Disponible en PdV — Indique si quiere que este producto aparezca en el punto de venta. |
|  | `to_weight` | boolean | 1 B | Sí | Por pesar con báscula — Indique si se debe integrar un hardware de báscula para poder pesar el producto. |
|  | `service_type` | varchar | variable | Sí | Seguimiento del servicio — Establecer las cantidades en la orden de forma manual: facture según la cantidad que usted ingrese, sin crear una cuenta analítica. Hojas… |
|  | `expense_policy` | varchar | variable | Sí | Volver a facturar los costos — Puede volver a facturar gastos validados, facturas de proveedores o la recolección de stock (en caso de que este configurada para llevar… |
|  | `invoice_policy` | varchar | variable | Sí | Política de facturación — Cantidad ordenada: facturar la cantidad que el cliente ordenó. Cantidad entregada: facturar la cantidad que se le entregó al cliente. |
|  | `sale_line_warn_msg` | text | variable | Sí | Advertencia de la línea de la orden de venta |
|  | `service_to_purchase` | jsonb | variable | Sí | Servicio de subcontratación — Si se selecciona, cada vez que venda este producto a través de una orden de venta se creará una solicitud de cotización de forma automáti… |

### Tabla 4.2.8-7. `product_product`

**Variante del producto** · modelo `product.product` · módulo `product` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_tmpl_id` | integer | 4 B | No | Plantilla del producto → `product_template` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `default_code` | varchar | variable | Sí | Referencia interna |
|  | `barcode` | varchar | variable | Sí | Código de barras — Número de artículo internacional usado para identificar el producto. |
|  | `combination_indices` | varchar | variable | Sí | Índices de combinación |
|  | `standard_price` | jsonb | variable | Sí | Costo — El valor del producto (calculado de forma automática con AVCO). Se utiliza para valorar el producto cuando se desconoce el costo de compr… |
|  | `volume` | numeric | variable | Sí | Volumen |
|  | `weight` | numeric | variable | Sí | Peso |
|  | `active` | boolean | 1 B | Sí | Activo — Si no está marcado, permitirá ocultar el producto sin eliminarlo. |
|  | `can_image_variant_1024_be_zoomed` | boolean | 1 B | Sí | ¿Se puede ampliar la imagen 1024 de la variante? |
|  | `is_favorite` | boolean | 1 B | Sí | Favorito |
|  | `is_in_selected_section_of_order` | boolean | 1 B | Sí | Está en la sección seleccionada de la orden |
|  | `write_date` | timestamp | 8 B | Sí | Escribir la fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `lot_properties_definition` | jsonb | variable | Sí | Propiedades del lote |

### Tabla 4.2.8-8. `product_category`

**Categoría del producto** · modelo `product.category` · módulo `product` · 20 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_id` | integer | 4 B | Sí | Categoría principal → `product_category` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `complete_name` | varchar | variable | Sí | Nombre completo |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `product_properties_definition` | jsonb | variable | Sí | Propiedades del producto |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `property_account_income_categ_id` | jsonb | variable | Sí | Cuenta de ingresos — Esta cuenta se utilizará al validar una factura del cliente. |
|  | `property_account_expense_categ_id` | jsonb | variable | Sí | Cuenta de gastos — El gasto se contabiliza cuando se valida una factura del proveedor, excepto en la contabilidad anglosajona con valoración perpetua del in… |
| FK | `removal_strategy_id` | integer | 4 B | Sí | Estrategia de remoción forzada → `product_removal` — Establezca una estrategia de remoción específica que se utilizará sin importar la ubicación de origen para esta categoría de producto. PE… |
|  | `packaging_reserve_method` | varchar | variable | Sí | Reservar embalajes — Reservar solo empaquetados completos: no se reservarán empaquetados parciales. Si el cliente ordena 2 palés con 1000 unidades cada uno y… |
|  | `property_valuation` | jsonb | variable | Sí | Valuación de inventario — Periódico: Los asientos de contabilidad se sugieren de forma manual en el reporte de valuación de inventario. Perpetuo: Se crea un asient… |
|  | `property_cost_method` | jsonb | variable | Sí | Método de costo — Precio estándar: los productos se valoran según su costo estándar definido en el producto. Costo promedio (AVCO): los productos se valora… |
|  | `property_stock_journal` | jsonb | variable | Sí | Diario de existencias — Al realizar una valoración de inventario automatizada, las entradas se registrarán en automático en este diario contable al procesar los… |
|  | `property_stock_valuation_account_id` | jsonb | variable | Sí | Cuenta de valoración de existencias — Cuando la valoración de inventario automatizada está habilitada en un producto, esta cuenta mantendrá el valor actual de los productos. |
|  | `property_price_difference_account_id` | jsonb | variable | Sí | Cuenta de diferencia de precio — Con valuación perpetua, esta cuenta almacena la diferencia de precio entre el precio estándar y el precio de la factura. |
|  | `property_stock_account_production_cost_id` | jsonb | variable | Sí | Cuenta de producción — Esta cuenta se usará como una contrapartida de valuación tanto para los componentes como para los productos finales para las órdenes de f… |

### Tabla 4.2.8-9. `product_pricelist`

**Lista de precios** · modelo `product.pricelist` · módulo `product` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre de la lista de precios |
|  | `active` | boolean | 1 B | Sí | Activo — Si no está marcado, podrá ocultar la lista de precios sin eliminarla. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### Tabla 4.2.8-10. `product_pricelist_item`

**Regla de la lista de precios** · modelo `product.pricelist.item` · módulo `product` · 27 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `pricelist_id` | integer | 4 B | Sí | Lista de precios → `product_pricelist` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `categ_id` | integer | 4 B | Sí | Categoría → `product_category` — Especifique una categoría de producto si esta regla solo aplica a los productos pertenecientes a esa categoría o a también a sus subcateg… |
| FK | `product_tmpl_id` | integer | 4 B | Sí | Producto → `product_template` — Especifique una plantilla si esta regla solo aplica a una plantilla de producto. De no ser así, déjelo vacío. |
| FK | `product_id` | integer | 4 B | Sí | Variante → `product_product` — Especifique un producto si esta regla solo aplica a un producto. De no ser así, déjelo vacío. |
| FK | `base_pricelist_id` | integer | 4 B | Sí | Otra lista de precios → `product_pricelist` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `applied_on` | varchar | variable | No | Aplicar en — Elemento de la lista de precios aplicable a la opción seleccionada |
|  | `display_applied_on` | varchar | variable | No | Mostrar aplicado en — Elemento de la lista de precios aplicable a la opción seleccionada |
|  | `base` | varchar | variable | No | Según — Precio base para el cálculo. Precio de venta: el precio base será el precio de venta. Precio de costo: el precio base será el precio de c… |
|  | `compute_price` | varchar | variable | No | Calcular el precio — Utilice las reglas de descuento y active los ajustes de descuento para que el cliente pueda ver el descuento. |
|  | `min_quantity` | numeric | variable | Sí | Cantidad min. — Para que se aplique la regla, la cantidad comprada/vendida debe ser mayor o igual que la cantidad mínima que se especifica en este campo.… |
|  | `fixed_price` | numeric | variable | Sí | Precio fijo |
|  | `price_discount` | numeric | variable | Sí | Precio de descuento — Puede aplicar un aumento de precio para configurar un descuento negativo. |
|  | `price_round` | numeric | variable | Sí | Redondeo del precio — Establece el precio a un múltiplo de este valor. El redondeo se aplica después del descuento y antes del cargo adicional. Para que los pr… |
|  | `price_surcharge` | numeric | variable | Sí | Tarifa adicional — Especifique el importe fijo a agregar o a quitar (si es negativo) al importe calculado con el descuento. |
|  | `price_markup` | numeric | variable | Sí | Utilidad sobre el costo (%) — Puede aplicar el margen de ganancia en el costo. |
|  | `price_min_margin` | numeric | variable | Sí | Margen mín. de precio — Especifique el importe mínimo del margen sobre el precio base. |
|  | `price_max_margin` | numeric | variable | Sí | Margen máx. de precio — Especifique el importe máximo de margen sobre el precio base. |
|  | `date_start` | timestamp | 8 B | Sí | Fecha de inicio — Fecha y hora de inicio de la validación de la lista de precios. El valor que se muestra depende del huso horario indicado en sus preferen… |
|  | `date_end` | timestamp | 8 B | Sí | Fecha de finalización — Fecha y hora límite para la validación de la lista de precios. El valor que se muestra depende del huso horario indicado en sus preferenc… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `percent_price` | double precision | 8 B | Sí | Porcentaje de precio — Puede aplicar un aumento de precio para configurar un descuento negativo. |

### Tabla 4.2.8-11. `product_supplierinfo`

**Lista de precios del proveedor** · modelo `product.supplierinfo` · módulo `product` · 20 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | No | Proveedor → `res_partner` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Asigna la prioridad a la lista de proveedor de productos. |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
| FK | `product_id` | integer | 4 B | Sí | Variante del producto → `product_product` — Si no se establece, el precio de proveedor se aplicará a todas las variantes de este producto. |
| FK | `product_tmpl_id` | integer | 4 B | No | Plantilla del producto → `product_template` |
|  | `delay` | integer | 4 B | No | Plazo de entrega — Tiempo de espera en días entre la confirmación de la orden de compra y la recepción de los productos en su almacén. El planificador usa e… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_name` | varchar | variable | Sí | Nombre del producto del proveedor — El nombre de producto del proveedor se usará al imprimir una solicitud de cotización. Déjelo vacío para usar el nombre interno. |
|  | `product_code` | varchar | variable | Sí | Código de producto del proveedor — El código de producto de proveedor se usará al imprimir una solicitud de cotización. Déjelo vacío para usar el código interno. |
|  | `date_start` | date | 4 B | Sí | Fecha de inicio — Fecha inicial para este precio de proveedor |
|  | `date_end` | date | 4 B | Sí | Fecha de finalización — Fecha final para este precio de proveedor |
|  | `min_qty` | numeric | variable | No | Cantidad — La cantidad a comprar a este proveedor para beneficiarte del precio unitario. Si hay una unidad de proveedor definida, la cantidad debe e… |
|  | `price` | numeric | variable | Sí | Precio unitario — El precio al que se compra un producto |
|  | `discount` | numeric | variable | Sí | Descuento (%) |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### Tabla 4.2.8-12. `hr_employee`

**Empleado** · modelo `hr.employee` · módulo `hr` · 50 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `resource_id` | integer | 4 B | No | Recurso → `resource_resource` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `message_main_attachment_id` | integer | 4 B | Sí | Archivo adjunto principal → `ir_attachment` |
| FK | `current_version_id` | integer | 4 B | Sí | Versión actual → `hr_version` |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` — Nombre de usuario relacionado con el recurso para gestionar su acceso. |
| FK | `work_contact_id` | integer | 4 B | Sí | Contacto de trabajo → `res_partner` |
| FK | `country_of_birth` | integer | 4 B | Sí | País de nacimiento → `res_country` |
| FK | `parent_id` | integer | 4 B | Sí | Gerente → `hr_employee` |
| FK | `coach_id` | integer | 4 B | Sí | Instructor → `hr_employee` — Seleccione el "empleado" que instruirá a este empleado. El “instructor” no tiene derechos o responsabilidades específicos predeterminados. |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre del empleado |
|  | `work_phone` | varchar | variable | Sí | Teléfono laboral |
|  | `mobile_phone` | varchar | variable | Sí | Celular de trabajo |
|  | `work_email` | varchar | variable | Sí | Correo de trabajo |
|  | `legal_name` | varchar | variable | Sí | Nombre legal |
|  | `private_phone` | varchar | variable | Sí | Teléfono privado |
|  | `private_email` | varchar | variable | Sí | Correo electrónico privado |
|  | `lang` | varchar | variable | Sí | Idioma |
|  | `place_of_birth` | varchar | variable | Sí | Lugar de nacimiento |
|  | `permit_no` | varchar | variable | Sí | Número de permiso de trabajo |
|  | `visa_no` | varchar | variable | Sí | Número de visa |
|  | `certificate` | varchar | variable | Sí | Nivel de estudios |
|  | `study_field` | varchar | variable | Sí | Campo de estudio |
|  | `study_school` | varchar | variable | Sí | Escuela |
|  | `emergency_contact` | varchar | variable | Sí | Contacto de emergencia |
|  | `emergency_phone` | varchar | variable | Sí | Teléfono de emergencia |
|  | `barcode` | varchar | variable | Sí | ID de credencial — ID usado para identificar al empleado. |
|  | `pin` | varchar | variable | Sí | NIP — NIP que se utiliza para el registro de entrada/salida en el modo quiosco de la aplicación Asistencias (si se habilita en Configuración) y… |
|  | `private_car_plate` | varchar | variable | Sí | Placa del vehículo privado — Separe las placas con un espacio si tiene más de un vehículo. |
|  | `birthday` | date | 4 B | Sí | Fecha de nacimiento |
|  | `visa_expire` | date | 4 B | Sí | Fecha de vencimiento de la visa |
|  | `work_permit_expiration_date` | date | 4 B | Sí | Fecha de vencimiento del permiso de trabajo |
|  | `salary_distribution` | jsonb | variable | Sí | Distribución salarial |
|  | `employee_properties` | jsonb | variable | Sí | Propiedades |
|  | `active` | boolean | 1 B | Sí | Activo — Si desmarca el campo activo podrá ocultar el registro del recurso sin eliminarlo. |
|  | `birthday_public_display` | boolean | 1 B | Sí | Mostrar a todos los empleados |
|  | `work_permit_scheduled_activity` | boolean | 1 B | Sí | Actividad programada del permiso de trabajo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `monday_location_id` | integer | 4 B | Sí | Lunes → `hr_work_location` |
| FK | `tuesday_location_id` | integer | 4 B | Sí | Martes → `hr_work_location` |
| FK | `wednesday_location_id` | integer | 4 B | Sí | Miércoles → `hr_work_location` |
| FK | `thursday_location_id` | integer | 4 B | Sí | Jueves → `hr_work_location` |
| FK | `friday_location_id` | integer | 4 B | Sí | Viernes → `hr_work_location` |
| FK | `saturday_location_id` | integer | 4 B | Sí | Sábado → `hr_work_location` |
| FK | `sunday_location_id` | integer | 4 B | Sí | Domingo → `hr_work_location` |
|  | `today_location_name` | varchar | variable | Sí | Nombre de la ubicación de hoy |

## Inventario

### Tabla 4.2.8-13. `stock_warehouse`

**Almacén** · modelo `stock.warehouse` · módulo `stock` · 43 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` — La empresa se establece automáticamente de acuerdo a sus preferencias de usuario. |
| FK | `partner_id` | integer | 4 B | Sí | Dirección → `res_partner` |
| FK | `view_location_id` | integer | 4 B | No | Ver ubicación → `stock_location` |
| FK | `lot_stock_id` | integer | 4 B | No | Ubicación de existencias → `stock_location` |
| FK | `wh_input_stock_loc_id` | integer | 4 B | Sí | Ubicación de entrada → `stock_location` |
| FK | `wh_qc_stock_loc_id` | integer | 4 B | Sí | Ubicación del control de calidad → `stock_location` |
| FK | `wh_output_stock_loc_id` | integer | 4 B | Sí | Ubicación de salida → `stock_location` |
| FK | `wh_pack_stock_loc_id` | integer | 4 B | Sí | Ubicación de empaquetado → `stock_location` |
| FK | `mto_pull_id` | integer | 4 B | Sí | Regla MTO → `stock_rule` |
| FK | `pick_type_id` | integer | 4 B | Sí | Tipo de recolección → `stock_picking_type` |
| FK | `pack_type_id` | integer | 4 B | Sí | Tipo de empaquetado → `stock_picking_type` |
| FK | `out_type_id` | integer | 4 B | Sí | Tipo de salida → `stock_picking_type` |
| FK | `in_type_id` | integer | 4 B | Sí | En tipo → `stock_picking_type` |
| FK | `int_type_id` | integer | 4 B | Sí | Tipo interno → `stock_picking_type` |
| FK | `qc_type_id` | integer | 4 B | Sí | Tipo de control de calidad → `stock_picking_type` |
| FK | `store_type_id` | integer | 4 B | Sí | Tipo de almacenamiento → `stock_picking_type` |
| FK | `xdock_type_id` | integer | 4 B | Sí | Tipo de almacenaje intermedio → `stock_picking_type` |
| FK | `reception_route_id` | integer | 4 B | Sí | Ruta de recepción → `stock_route` |
| FK | `delivery_route_id` | integer | 4 B | Sí | Ruta de entrega → `stock_route` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Proporciona la secuencia de esta línea al mostrar los almacenes. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Almacén |
|  | `code` | varchar | 5 | No | Nombre corto — Nombre corto que se utiliza para identificar su almacén |
|  | `reception_steps` | varchar | variable | No | Envíos entrantes — Ruta de entrada a seguir predeterminada |
|  | `delivery_steps` | varchar | variable | No | Envíos salientes — Ruta de salida a seguir predeterminada |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `manufacture_pull_id` | integer | 4 B | Sí | Regla de fabricación → `stock_rule` |
| FK | `manufacture_mto_pull_id` | integer | 4 B | Sí | Regla de fabricación sobre pedido → `stock_rule` |
| FK | `pbm_mto_pull_id` | integer | 4 B | Sí | Regla de recolección antes de fabricación sobre pedido → `stock_rule` |
| FK | `sam_rule_id` | integer | 4 B | Sí | Regla de existencias después de la producción → `stock_rule` |
| FK | `manu_type_id` | integer | 4 B | Sí | Tipo de operación de fabricación → `stock_picking_type` |
| FK | `pbm_type_id` | integer | 4 B | Sí | Tipo de operación de recolección antes de fabricación → `stock_picking_type` |
| FK | `sam_type_id` | integer | 4 B | Sí | Tipo de existencias después de la operación de fabricación → `stock_picking_type` |
| FK | `pbm_route_id` | integer | 4 B | Sí | Ruta de recolección antes de fabricación → `stock_route` |
| FK | `pbm_loc_id` | integer | 4 B | Sí | Ubicación de recolección antes de fabricación → `stock_location` |
| FK | `sam_loc_id` | integer | 4 B | Sí | Ubicación de existencias después de la fabricación → `stock_location` |
|  | `manufacture_steps` | varchar | variable | No | Manufactura — 1 paso: Consumir los componentes del stock y fabricar. 2 pasos: Elegir los componentes del stock y luego fabricar. 3 pasos: Elegir los co… |
| FK | `pos_type_id` | integer | 4 B | Sí | Tipo de operación de Punto de venta → `stock_picking_type` |
| FK | `buy_pull_id` | integer | 4 B | Sí | Regla de compra → `stock_rule` |

### Tabla 4.2.8-14. `stock_location`

**Ubicaciones de inventario** · modelo `stock.location` · módulo `stock` · 24 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `location_id` | integer | 4 B | Sí | Ubicación principal → `stock_location` — La ubicación principal que incluye esta ubicación. Por ejemplo, "Zona de despacho" es la ubicación principal de "Puerta 1". |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — Deje vacío este campo si la ubicación se compartirá entre las empresas |
| FK | `removal_strategy_id` | integer | 4 B | Sí | Estrategia de remoción → `product_removal` — Define el método predeterminado que se utiliza para sugerir la ubicación específica (estante) de la que se tomarán los productos, los lot… |
|  | `cyclic_inventory_frequency` | integer | 4 B | Sí | Frecuencia de inventario — Cuando no es 0, la fecha de recuento de inventario para los productos almacenados en esta ubicación se establecerá de forma automática co… |
| FK | `warehouse_id` | integer | 4 B | Sí | Almacén → `stock_warehouse` |
| FK | `storage_category_id` | integer | 4 B | Sí | Categoría de almacenamiento → `stock_storage_category` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de la ubicación |
|  | `complete_name` | varchar | variable | Sí | Nombre completo de la ubicación |
|  | `usage` | varchar | variable | No | Tipo de ubicación — * Proveedor: Ubicación virtual que representa la ubicación de origen de los productos de tus proveedores. * Virtual: Ubicación virtual us… |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `barcode` | varchar | variable | Sí | Código de barras |
|  | `last_inventory_date` | date | 4 B | Sí | Último inventario — Fecha del último inventario en esta ubicación. |
|  | `next_inventory_date` | date | 4 B | Sí | Siguiente esperado — Fecha para el próximo inventario planeado según un programa cíclico. |
|  | `active` | boolean | 1 B | Sí | Activo — Si el campo activo se desmarca, permite ocultar la ubicación sin eliminarla. |
|  | `replenish_location` | boolean | 1 B | Sí | Reabastecimientos — Activar sugerencias de reabastecimiento para esta ubicación cuando se requiera |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `valuation_account_id` | integer | 4 B | Sí | Cuenta de valoración de existencias → `account_account` — Cuenta de gastos usada para reclasificar productos retirados del inventario y enviados a esta ubicación |
|  | `control_temperatura` | boolean | 1 B | Sí | **[donofrio_calidad]** Controlar temperatura — Si está marcado, las lecturas de temperatura de esta ubicación se comparan con su rango. |
|  | `temp_min` | double precision | 8 B | Sí | **[donofrio_calidad]** Temperatura mínima (°C) |
|  | `temp_max` | double precision | 8 B | Sí | **[donofrio_calidad]** Temperatura máxima (°C) |

### Tabla 4.2.8-15. `stock_picking_type`

**Tipo de recolección** · modelo `stock.picking.type` · módulo `stock` · 53 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Color |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Se utiliza para ordenar la vista de kanban de "Todas las operaciones" |
| FK | `sequence_id` | integer | 4 B | Sí | Secuencia de la referencia → `ir_sequence` |
| FK | `default_location_src_id` | integer | 4 B | No | Ubicación de origen → `stock_location` — Esta es la ubicación de origen predeterminada al crear la operación manualmente. Puede cambiarla después o las rutas también pueden usar… |
| FK | `default_location_dest_id` | integer | 4 B | No | Ubicación de destino → `stock_location` — Esta es la ubicación de destino predeterminada al crear la operación manualmente. Puede cambiarla después o las rutas también pueden usar… |
| FK | `return_picking_type_id` | integer | 4 B | Sí | Tipo de operación para devoluciones → `stock_picking_type` |
| FK | `warehouse_id` | integer | 4 B | Sí | Almacén → `stock_warehouse` |
|  | `reservation_days_before` | integer | 4 B | Sí | Días — Número máximo de días antes de la fecha programada en la que se reservarán los productos. |
|  | `reservation_days_before_priority` | integer | 4 B | Sí | Días cuando se destacó — Número máximo de días antes de la fecha programada en la que se reservarán los productos con recolección con prioridad. |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `sequence_code` | varchar | variable | No | Prefijo de secuencia |
|  | `code` | varchar | variable | No | Tipo de operación |
|  | `reservation_method` | varchar | variable | No | Método de reservación — Cómo se deben reservar los productos en traslados para este tipo de operación. |
|  | `product_label_format` | varchar | variable | Sí | Formato de etiqueta de producto para impresión automática |
|  | `lot_label_format` | varchar | variable | Sí | Formato de etiqueta de lote para autoimpresión |
|  | `package_label_to_print` | varchar | variable | Sí | Etiqueta de paquete para imprimir |
|  | `barcode` | varchar | variable | Sí | Código de barras |
|  | `create_backorder` | varchar | variable | No | Crear orden parcial — Al validar un traslado: * Preguntar: se le pide a los usuarios elegir si desean crear una orden parcial para los productos restantes * Si… |
|  | `move_type` | varchar | variable | No | Política de envío — Especifica si los bienes se trasladan parcialmente o todos a la vez. |
|  | `name` | jsonb | variable | No | Tipo de operación |
|  | `picking_properties_definition` | jsonb | variable | Sí | Propiedades de la recolección |
|  | `show_entire_packs` | boolean | 1 B | Sí | Mover paquetes completos — Si está seleccionada, los paquetes a mover aparecerán directamente en Código de barras en lugar de los productos que contienen |
|  | `set_package_type` | boolean | 1 B | Sí | Definir tipo de paquete — Si está seleccionada podrás seleccionar qué paquete o tipo de paquete usar al incluir en uno |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `use_create_lots` | boolean | 1 B | Sí | Crear nuevos números de lote o serie — Solamente si está seleccionado, supondrá que desea crear nuevos números de lote/de serie para que pueda proporcionarlos en un campo de te… |
|  | `use_existing_lots` | boolean | 1 B | Sí | Utilizar números de lotes/de serie existentes — Si esto se encuentra seleccionado, podrá elegir los números de serie o lote. También puede decidir no incluir lotes en este tipo de opera… |
|  | `print_label` | boolean | 1 B | Sí | Generar etiquetas de envío — Seleccione esta casilla si desea crear una etiqueta de envío en esta operación. |
|  | `show_operations` | boolean | 1 B | Sí | Mostrar operaciones detalladas — Si selecciona esta casilla, las líneas de recolección representarán operaciones detalladas de existencias. De lo contrario, las líneas de… |
|  | `auto_show_reception_report` | boolean | 1 B | Sí | Mostrar reporte de recepción en la validación — Si esta casilla está seleccionada, Odoo mostrará el reporte de recepción de forma automática (si hay movimientos por asignar) al validar. |
|  | `auto_print_delivery_slip` | boolean | 1 B | Sí | Imprimir el recibo de entrega de forma automática — Si selecciona esta casilla, Odoo imprimirá en automático el recibo de entrega de una recolección al validarla. |
|  | `auto_print_return_slip` | boolean | 1 B | Sí | Imprimir el recibo de devolución de forma automática — Si selecciona esta casilla, Odoo imprimirá en automático el recibo de devolución de una recolección al validarla. |
|  | `auto_print_product_labels` | boolean | 1 B | Sí | Imprimir las etiquetas del producto de forma automática — Si selecciona esta casilla, Odoo imprimirá en automático las etiquetas del producto de una recolección al validarla. |
|  | `auto_print_lot_labels` | boolean | 1 B | Sí | Imprimir las etiquetas de los números de lote y serie de forma automática — Si selecciona esta casilla, Odoo imprimirá en automático las etiquetas de número de lote o serie de una recolección al validarla. |
|  | `auto_print_reception_report` | boolean | 1 B | Sí | Imprimir el reporte de entrega de forma automática — Si selecciona esta casilla, Odoo imprimirá de forma automática el reporte de una recolección cuando se valide y tenga movimientos asignados. |
|  | `auto_print_reception_report_labels` | boolean | 1 B | Sí | Imprimir las etiquetas del reporte de entrega de forma automática — Si selecciona esta casilla, Odoo imprimirá en automático las etiquetas de reporte de una recepción al validarla. |
|  | `auto_print_packages` | boolean | 1 B | Sí | Imprimir de forma automática los paquetes — Si selecciona esta casilla, Odoo imprimirá en automático los paquetes y el contenido de una recolección al validarla. |
|  | `auto_print_package_label` | boolean | 1 B | Sí | Imprimir la etiqueta del paquete de forma automática — Si selecciona esta casilla, Odoo imprimirá la etiqueta del paquete en automático cuando se use el botón "Incluir en el paquete". |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `mrp_product_label_to_print` | varchar | variable | Sí | Etiqueta de producto para imprimir |
|  | `done_mrp_lot_label_to_print` | varchar | variable | Sí | Etiqueta de número de lote o serie a imprimir |
|  | `generated_mrp_lot_label_to_print` | varchar | variable | Sí | Etiqueta de número de serie o lote generada para imprimir |
|  | `use_create_components_lots` | boolean | 1 B | Sí | Crear nuevos números de lotes o de serie para componentes — Permita crear nuevos números de lote/de serie para los componentes |
|  | `auto_print_done_production_order` | boolean | 1 B | Sí | Orden de fabricación con impresión automática — Si esta casilla está marcada, Odoo imprimirá en automático la orden de producción de una orden de fabricación cuando esté lista. |
|  | `auto_print_done_mrp_product_labels` | boolean | 1 B | Sí | Etiquetas de productos producidas por impresión automática — Si esta casilla está marcada, Odoo imprimirá en automático las etiquetas de los productos de una orden de fabricación cuando esté lista. |
|  | `auto_print_done_mrp_lot` | boolean | 1 B | Sí | Etiqueta de lote producida por impresión automática — Si esta casilla está marcada, Odoo imprimirá en automático la etiqueta de número de lote o serie de una orden de fabricación cuando esté… |
|  | `auto_print_mrp_reception_report` | boolean | 1 B | Sí | Reporte de asignación de impresión automática — Si esta casilla está marcada, Odoo imprimirá en automático el reporte de asignación de una orden de fabricación cuando se haya realizado… |
|  | `auto_print_mrp_reception_report_labels` | boolean | 1 B | Sí | Etiquetas de reporte de asignación de impresión automática — Si esta casilla está marcada, Odoo imprimirá en automático las etiquetas del reporte de asignación de una orden de fabricación cuando est… |
|  | `auto_print_generated_mrp_lot` | boolean | 1 B | Sí | Impresión automática de la etiqueta de número de lote o serie — Imprimir de forma automática la etiqueta de número de lote o serie al utilizar el botón "Crear un nuevo número de serie o lote". |
|  | `analytic_costs` | boolean | 1 B | Sí | Costos analíticos — La validación de los productos seleccionados generará asientos analíticos para el proyecto seleccionado. También se facturarán al cliente… |

### Tabla 4.2.8-16. `stock_picking`

**Transferir** · modelo `stock.picking` · módulo `stock` · 32 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `backorder_id` | integer | 4 B | Sí | Orden parcial de → `stock_picking` — Si se dividió el envío, entonces este campo enlaza con el envío que contenga la parte ya procesada. |
| FK | `return_id` | integer | 4 B | Sí | Devolución de → `stock_picking` — Si esta recolección se creo como una devolución de otra recolección, este campo se vinculará a la recolección original. |
| FK | `location_id` | integer | 4 B | No | Ubicación de origen → `stock_location` |
| FK | `location_dest_id` | integer | 4 B | No | Ubicación de destino → `stock_location` |
| FK | `picking_type_id` | integer | 4 B | No | Tipo de operación → `stock_picking_type` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `user_id` | integer | 4 B | Sí | Responsable → `res_users` |
| FK | `owner_id` | integer | 4 B | Sí | Asignar propietario → `res_partner` — Al validar el traslado, los productos se asignarán a este propietario. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Referencia |
|  | `origin` | varchar | variable | Sí | Documento origen — Referencia del documento |
|  | `move_type` | varchar | variable | No | Política de envío — Especifica si los artículos se entregan parcialmente o todos a la vez |
|  | `state` | varchar | variable | Sí | Estado — * Borrador: no se ha confirmado el traslado. No se realizan reservas. * En espera de otra operación: el traslado espera otra operación an… |
|  | `priority` | varchar | variable | Sí | Prioridad — Los productos se reservarán primero para los traslados con mayor prioridad. |
|  | `picking_properties` | jsonb | variable | Sí | Propiedades |
|  | `note` | text | variable | Sí | Notas |
|  | `shipping_weight` | numeric | variable | Sí | Peso para envío — El paquete no contiene el peso y productos totales. Los paquetes que no especifican el peso del envío se les pondrá el peso total de los… |
|  | `has_deadline_issue` | boolean | 1 B | Sí | Atrasado — Llega tarde o llegará tarde según la fecha límite y la fecha programada |
|  | `printed` | boolean | 1 B | Sí | Impreso |
|  | `is_locked` | boolean | 1 B | Sí | Está bloqueado — Cuando la recolección no está hecha, esto permite cambiar la demanda inicial. Cuando se realiza la operación, esto permite cambiar las ca… |
|  | `scheduled_date` | timestamp | 8 B | Sí | Fecha programada — Fecha programada para la primera parte del envío que se procesará. Establecer manualmente un valor aquí significará la fecha esperada par… |
|  | `date_deadline` | timestamp | 8 B | Sí | Fecha límite — En caso de que se trate de un flujo de salida, valide el traslado antes de esta fecha para permitir la entrega en la fecha prometida al c… |
|  | `date_done` | timestamp | 8 B | Sí | Fecha de traslado — Fecha en la que se procesó o canceló el traslado. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `project_id` | integer | 4 B | Sí | Proyectos → `project_project` |
| FK | `pos_session_id` | integer | 4 B | Sí | Sesión de PdV → `pos_session` |
| FK | `pos_order_id` | integer | 4 B | Sí | Orden del PdV → `pos_order` |
| FK | `sale_id` | integer | 4 B | Sí | Orden de venta → `sale_order` |

### Tabla 4.2.8-17. `stock_move`

**Movimiento de stock** · modelo `stock.move` · módulo `stock` · 65 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `product_uom` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `location_id` | integer | 4 B | No | Ubicación de origen → `stock_location` — La operación toma y sugiere productos de esta ubicación. |
| FK | `location_dest_id` | integer | 4 B | No | Ubicación intermedia → `stock_location` — La operación trae el producto a esta ubicación |
| FK | `location_final_id` | integer | 4 B | Sí | Ubicación final → `stock_location` — La operación trae los productos a una ubicación intermedia. Esta operación es parte de una cadena de operaciones cuyo objetivo es la ubic… |
| FK | `partner_id` | integer | 4 B | Sí | Dirección de destino → `res_partner` — Dirección opcional donde se deben entregar los productos, se utiliza específicamente para lotes. |
| FK | `picking_id` | integer | 4 B | Sí | Transferir → `stock_picking` |
| FK | `scrap_id` | integer | 4 B | Sí | Operación de desecho → `stock_scrap` |
| FK | `rule_id` | integer | 4 B | Sí | Regla de inventario → `stock_rule` — La regla de existencias que creó este movimiento de existencias |
| FK | `picking_type_id` | integer | 4 B | Sí | Tipo de operación → `stock_picking_type` |
| FK | `origin_returned_move_id` | integer | 4 B | Sí | Origen del movimiento de devolución → `stock_move` — Movimiento que creó el movimiento de devolución |
| FK | `restrict_partner_id` | integer | 4 B | Sí | Propietario → `res_partner` |
| FK | `warehouse_id` | integer | 4 B | Sí | Almacén → `stock_warehouse` — el almacén a considerar para la selección de la ruta en el próximo aprovisionamiento (si lo hay). |
|  | `next_serial_count` | integer | 4 B | Sí | Cantidad de números de serie o lote |
| FK | `orderpoint_id` | integer | 4 B | Sí | Regla de reordenamiento original → `stock_warehouse_orderpoint` |
| FK | `packaging_uom_id` | integer | 4 B | Sí | Embalaje → `uom_uom` — Unidad de embalaje para órdenes de venta o compra |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `priority` | varchar | variable | Sí | Prioridad |
|  | `state` | varchar | variable | Sí | Estado — * Nuevo: Se creó el movimiento de existencias pero no está confirmado. * En espera de otro movimiento: Es necesario realizar el movimient… |
|  | `origin` | varchar | variable | Sí | Documento origen |
|  | `procure_method` | varchar | variable | No | Método de suministro — De forma predeterminada, el sistema tomará las unidades desde las existencias en la ubicación fuente y esperará pasivamente a su disponib… |
|  | `inventory_name` | varchar | variable | Sí | Nombre del inventario |
|  | `reference` | varchar | variable | Sí | Referencia |
|  | `next_serial` | varchar | variable | Sí | Primer número de serie/lote |
|  | `reservation_date` | date | 4 B | Sí | Fecha para reservar — Calcula cuándo se debe reservar un movimiento |
|  | `description_picking_manual` | text | variable | Sí | Descripción de la recolección manual |
|  | `product_qty` | numeric | variable | Sí | Cantidad real — Cantidad en la UdM predeterminada del producto |
|  | `product_uom_qty` | numeric | variable | No | Demanda — Esta es la cantidad de producto que se planea mover. Reducir esta cantidad no genera una orden pendiente. Modificar esta cantidad en movi… |
|  | `quantity` | numeric | variable | Sí | Cantidad |
|  | `picked` | boolean | 1 B | Sí | Recolección — Esta casilla solo es informativa, no valida ni genera ningún movimiento del producto. |
|  | `propagate_cancel` | boolean | 1 B | Sí | Propagar cancelación y división — Si se encuentra seleccionado, cuando este movimiento se cancela, también cancela el movimiento relacionado. |
|  | `is_inventory` | boolean | 1 B | Sí | Inventario |
|  | `additional` | boolean | 1 B | Sí | Si el movimiento se agregó después de la confirmación de la recolección |
|  | `date` | timestamp | 8 B | No | Fecha programada — Fecha programada hasta que el movimiento esté hecho, después la fecha real en la que se procesó el movimiento |
|  | `date_deadline` | timestamp | 8 B | Sí | Fecha límite — En caso de que se trate de un flujo de salida, valide el traslado antes de esta fecha para permitir la entrega en la fecha prometida al c… |
|  | `delay_alert_date` | timestamp | 8 B | Sí | Fecha de alerta de atraso — Procesar en esta fecha para que llegue a tiempo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `price_unit` | double precision | 8 B | Sí | Unidad de precio |
|  | `packaging_uom_qty` | double precision | 8 B | Sí | Cantidad de embalaje — Cantidad en la unidad de embalaje |
|  | `unit_factor` | double precision | 8 B | Sí | Factor unitario |
|  | `manual_consumption` | boolean | 1 B | Sí | Consumo manual — Cuando se activa, el registro de consumo para ese componente se registra solo de forma manual. Si no se activa y el consumo de cualquier… |
| FK | `created_production_id` | integer | 4 B | Sí | Orden de producción creada → `mrp_production` |
| FK | `production_id` | integer | 4 B | Sí | Orden de producción para productos terminados → `mrp_production` |
| FK | `raw_material_production_id` | integer | 4 B | Sí | Orden de producción para componentes → `mrp_production` |
| FK | `production_group_id` | integer | 4 B | Sí | Usado para producciones → `mrp_production_group` |
| FK | `unbuild_id` | integer | 4 B | Sí | Orden de desmantelamiento → `mrp_unbuild` |
| FK | `consume_unbuild_id` | integer | 4 B | Sí | Orden de desmantelamiento consumida → `mrp_unbuild` |
| FK | `operation_id` | integer | 4 B | Sí | Operación por consumir → `mrp_routing_workcenter` |
| FK | `workorder_id` | integer | 4 B | Sí | Orden de trabajo por consumir → `mrp_workorder` |
| FK | `bom_line_id` | integer | 4 B | Sí | Línea de la lista de materiales → `mrp_bom_line` |
| FK | `byproduct_id` | integer | 4 B | Sí | Subproductos → `mrp_bom_byproduct` — Línea de subproductos que generó el movimiento en una orden de fabricación |
|  | `cost_share` | numeric | variable | Sí | Reparto de costos (%) — El porcentaje del costo de producción final para este subproducto. El total de reparto de costos de subproductos debe ser menor o igual a… |
| FK | `account_move_id` | integer | 4 B | Sí | stock_move_id → `account_move` |
|  | `value` | numeric | variable | Sí | Valor — El valor actual del movimiento. Es cero si el movimiento no tiene una valuación. |
|  | `to_refund` | boolean | 1 B | Sí | Actualizar cantidades en órdenes de venta o compra — Activar una disminución de la cantidad entregada/recibida en la orden de venta/compra asociada |
|  | `is_in` | boolean | 1 B | Sí | Es una entrada (valuada) |
|  | `is_out` | boolean | 1 B | Sí | Es una salida (valuada) |
|  | `is_dropship` | boolean | 1 B | Sí | Es un envío directo |
| FK | `purchase_line_id` | integer | 4 B | Sí | Línea de la orden de compra → `purchase_order_line` |
| FK | `sale_line_id` | integer | 4 B | Sí | Línea de venta → `sale_order_line` |

### Tabla 4.2.8-18. `stock_move_line`

**Movimientos de producto (línea de movimiento de stock)** · modelo `stock.move.line` · módulo `stock` · 28 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `picking_id` | integer | 4 B | Sí | Transferir → `stock_picking` — La operación de existencias en la que se creó el paquete |
| FK | `move_id` | integer | 4 B | Sí | Operación de existencias → `stock_move` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `package_id` | integer | 4 B | Sí | Paquete de origen → `stock_package` |
| FK | `lot_id` | integer | 4 B | Sí | Número de serie/lote → `stock_lot` |
| FK | `result_package_id` | integer | 4 B | Sí | Paquete de destino → `stock_package` — Si se establece, las operaciones se empaquetan en este paquete |
| FK | `package_history_id` | integer | 4 B | Sí | Historial del paquete → `stock_package_history` |
| FK | `owner_id` | integer | 4 B | Sí | Del propietario → `res_partner` — Al validar el traslado, los productos se tomarán de este propietario. |
| FK | `location_id` | integer | 4 B | No | Desde → `stock_location` |
| FK | `location_dest_id` | integer | 4 B | No | A → `stock_location` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lot_name` | varchar | variable | Sí | Nombre del número de serie o lote |
|  | `state` | varchar | variable | Sí | Estado — * Nuevo: Se creó el movimiento de existencias pero no está confirmado. * En espera de otro movimiento: Es necesario realizar el movimient… |
|  | `quantity` | numeric | variable | Sí | Cantidad |
|  | `quantity_product_uom` | numeric | variable | Sí | Cantidad en la unidad de medida del producto |
|  | `picked` | boolean | 1 B | Sí | Recolección |
|  | `is_entire_pack` | boolean | 1 B | Sí | Se agrega a través del paquete completo |
|  | `date` | timestamp | 8 B | No | Fecha — La fecha de creación de esta línea de movimiento se actualizará si la cantidad aumenta, el estado cambia a "recolectado" o realiza la lín… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `workorder_id` | integer | 4 B | Sí | Orden de trabajo → `mrp_workorder` |
| FK | `production_id` | integer | 4 B | Sí | Orden de producción → `mrp_production` |
|  | `expiration_date` | timestamp | 8 B | Sí | Fecha de caducidad — Esta fecha indica que los bienes con este número de serie pueden representar un riesgo y no se deben consumir. |
|  | `removal_date` | timestamp | 8 B | Sí | Fecha de remoción |

### Tabla 4.2.8-19. `stock_lot`

**Número de serie/lote** · modelo `stock.lot` · módulo `stock` · 19 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `location_id` | integer | 4 B | Sí | Ubicación → `stock_location` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Número de serie/lote — Número de lote o de serie único |
|  | `ref` | varchar | variable | Sí | Referencia interna — Número de referencia interno en caso de que difiera del número de lote/serie del fabricante |
|  | `lot_properties` | jsonb | variable | Sí | Propiedades |
|  | `note` | text | variable | Sí | Descripción |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `product_expiry_reminded` | boolean | 1 B | Sí | Se recordó la fecha de caducidad |
|  | `expiration_date` | timestamp | 8 B | Sí | Fecha de caducidad — Esta fecha indica que los bienes con este número de serie pueden representar un riesgo y no se deben consumir. |
|  | `use_date` | timestamp | 8 B | Sí | Consumir preferentemente antes de — Esta fecha indica que los bienes con este número de serie empiezan a deteriorarse, pero todavía no representan un peligro. |
|  | `removal_date` | timestamp | 8 B | Sí | Fecha de remoción — Esta es la fecha en que los productos con este número de serie deben retirarse del inventario y dejar de contarse como existencias a la m… |
|  | `alert_date` | timestamp | 8 B | Sí | Fecha de alerta — Fecha que determina la caducidad de los números de lote y serie con el filtro "Alertas de caducidad". |
|  | `standard_price` | jsonb | variable | Sí | Costo — El valor del lote (calculado de forma automática con AVCO) Se utiliza para valorar el producto cuando se desconoce el costo de compra (po… |
|  | `alerta_vencimiento_fecha` | timestamp | 8 B | Sí | **[donofrio_calidad]** Alerta de vencimiento enviada — Cuándo se avisó que el lote estaba por vencer; evita repetir la alerta del cron diario. |

### Tabla 4.2.8-20. `stock_quant`

**Quants** · modelo `stock.quant` · módulo `stock` · 22 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — Deje vacío este campo si la ubicación se compartirá entre las empresas |
| FK | `location_id` | integer | 4 B | No | Ubicación → `stock_location` |
| FK | `lot_id` | integer | 4 B | Sí | Número de serie/lote → `stock_lot` |
| FK | `package_id` | integer | 4 B | Sí | Paquete → `stock_package` — El paquete que contiene esta cantidad |
| FK | `owner_id` | integer | 4 B | Sí | Propietario → `res_partner` — Este es el propietario del quant |
| FK | `user_id` | integer | 4 B | Sí | Asignado a → `res_users` — Usuario asignado para realizar un recuento de productos. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `inventory_date` | date | 4 B | Sí | Planeado — La próxima fecha en la que se contará la cantidad a la mano. |
|  | `quantity` | numeric | variable | Sí | Cantidad — Cantidad de productos en este quant, en la unidad de medida predeterminada del producto |
|  | `reserved_quantity` | numeric | variable | No | Cantidad reservada — Cantidad de productos reservados en este quant, en la unidad de medida predeterminada del producto |
|  | `inventory_quantity` | numeric | variable | Sí | Contado — La cantidad contada del producto. |
|  | `inventory_diff_quantity` | numeric | variable | Sí | Diferencia — Indica la diferencia entre la cantidad teórica del producto y su cantidad contada. |
|  | `inventory_quantity_set` | boolean | 1 B | Sí | Conjunto de cantidades de inventario |
|  | `in_date` | timestamp | 8 B | No | Fecha de entrada |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `expiration_date` | timestamp | 8 B | Sí | Fecha de caducidad — Esta fecha indica que los bienes con este número de serie pueden representar un riesgo y no se deben consumir. |
|  | `removal_date` | timestamp | 8 B | Sí | Fecha de remoción — Esta es la fecha en que los productos con este número de serie deben retirarse del inventario y dejar de contarse como existencias a la m… |
|  | `accounting_date` | date | 4 B | Sí | Fecha contable — Fecha en la que se crearán los asientos contables en caso de valoración de inventario automatizada. Si está vacío, se usará la fecha de i… |

### Tabla 4.2.8-21. `stock_warehouse_orderpoint`

**Regla de inventario mínimo** · modelo `stock.warehouse.orderpoint` · módulo `stock` · 22 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `warehouse_id` | integer | 4 B | No | Almacén → `stock_warehouse` |
| FK | `location_id` | integer | 4 B | No | Ubicación → `stock_location` |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `replenishment_uom_id` | integer | 4 B | Sí | Múltiple → `uom_uom` — La cantidad de aprovisionamiento se redondeará hacia arriba a un múltiplo de esta unidad o embalaje. Si no está definido, no se redondea. |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `route_id` | integer | 4 B | Sí | Ruta → `stock_route` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `trigger` | varchar | variable | No | Activar |
|  | `snoozed_until` | date | 4 B | Sí | Pospuesto — Oculto hasta el próximo planificador. |
|  | `deadline_date` | date | 4 B | Sí | Fecha límite — Fecha antes de la cual debes ordenar para evitar que las existencias estén por debajo del mínimo. Si no tienes nada que ordenar mientras… |
|  | `product_min_qty` | numeric | variable | No | Cantidad mínima — El nivel de stock mínimo que activará un reabastecimiento. |
|  | `product_max_qty` | numeric | variable | No | Cantidad máxima — Nivel de stock que se debe alcanzar durante el reabastecimiento. |
|  | `qty_to_order_computed` | numeric | variable | Sí | Por ordenar calculado |
|  | `qty_to_order_manual` | numeric | variable | Sí | Por ordenar manual |
|  | `active` | boolean | 1 B | Sí | Activo — Si el campo activo se establece a False, permite ocultar la regla de existencias mínimas sin eliminarla. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `bom_id` | integer | 4 B | Sí | Lista de materiales → `mrp_bom` |
| FK | `supplier_id` | integer | 4 B | Sí | Listas de precios de proveedores → `product_supplierinfo` |

## Producción

### Tabla 4.2.8-22. `mrp_bom`

**Lista de materiales** · modelo `mrp.bom` · módulo `mrp` · 23 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_tmpl_id` | integer | 4 B | No | Producto → `product_template` |
| FK | `product_id` | integer | 4 B | Sí | Variante del producto → `product_product` — Si define una variante de producto, la LdM sólo estará disponible para ese producto. |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` — La unidad de medida (UdM) es la unidad de medición para el control de inventario |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `picking_type_id` | integer | 4 B | Sí | Tipo de operación → `stock_picking_type` — Cuando un aprovisionamiento tiene una ruta de "producción" con un tipo de operación establecido, intentará crear una orden de fabricación… |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `produce_delay` | integer | 4 B | Sí | Plazo de fabricación — Tiempo promedio de entrega en días para fabricar este producto. En el caso de una lista de materiales de varios niveles se agregarán los… |
|  | `days_to_prepare_mo` | integer | 4 B | Sí | Días para preparar la orden de fabricación — Crea y confirma órdenes de fabricación con este número de días de anticipación para tener suficiente tiempo para reabastecer los componen… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | Sí | Referencia |
|  | `type` | varchar | variable | No | Tipo de lista de materiales |
|  | `ready_to_produce` | varchar | variable | No | Preparación para la fabricación |
|  | `consumption` | varchar | variable | No | Consumo flexible — Define si puede consumir más o menos componentes que la cantidad definida en la lista de materiales: * Permitido: se permite para todos l… |
|  | `product_qty` | numeric | variable | No | Cantidad — Esta debe ser la cantidad más pequeña que se puede producir de este producto. Si la LdM contiene operaciones, asegúrese de que la capacid… |
|  | `batch_size` | numeric | variable | Sí | Tamaño del lote — Todas las órdenes de fabricación generadas de forma automática para este producto tendrán este tamaño. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `allow_operation_dependencies` | boolean | 1 B | Sí | Dependencias de las operaciones — Cree dependencias de nivel de operación que influyan tanto en la planeación como en el estado de las órdenes de trabajo tras confirmar la… |
|  | `enable_batch_size` | boolean | 1 B | Sí | Activar tamaño de lote |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `project_id` | integer | 4 B | Sí | Proyectos → `project_project` |

### Tabla 4.2.8-23. `mrp_bom_line`

**Línea de lista de materiales** · modelo `mrp.bom.line` · módulo `mrp` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Componente → `product_product` |
| FK | `product_tmpl_id` | integer | 4 B | Sí | Plantilla del producto → `product_template` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Indica el orden de secuencia cuando se visualiza. |
| FK | `bom_id` | integer | 4 B | No | LdM principal → `mrp_bom` |
| FK | `operation_id` | integer | 4 B | Sí | Consumido en la operación → `mrp_routing_workcenter` — La operación en la que se consumen los componentes o los productos terminados creados. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_qty` | numeric | variable | No | Cantidad |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `cost_share` | numeric | variable | Sí | Reparto de costos (%) — El porcentaje del costo de repartición del componente cuando se compra un kit. El total del costo de todos los componentes debe ser igual… |

### Tabla 4.2.8-24. `mrp_production`

**Orden de fabricación** · modelo `mrp.production` · módulo `mrp` · 39 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `backorder_sequence` | integer | 4 B | Sí | Secuencia de orden parcial — Secuencia de orden parcial, si es igual a 0 significa que no está relacionada a una orden parcial. |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `production_group_id` | integer | 4 B | Sí | Grupo de producción → `mrp_production_group` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `picking_type_id` | integer | 4 B | No | Tipo de operación → `stock_picking_type` |
| FK | `location_src_id` | integer | 4 B | No | Ubicación de los componentes → `stock_location` — Ubicación donde el sistema buscará los componentes. |
| FK | `location_dest_id` | integer | 4 B | No | Ubicación de productos terminados → `stock_location` — Ubicación donde el sistema almacenará los productos terminados. |
| FK | `location_final_id` | integer | 4 B | Sí | Ubicación final del aprovisionamiento → `stock_location` |
| FK | `bom_id` | integer | 4 B | Sí | Lista de materiales → `mrp_bom` — Las listas de materiales, también conocidas como recetas de producción, se utilizan para autocompletar los componentes y las instruccione… |
| FK | `user_id` | integer | 4 B | Sí | Responsable → `res_users` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `orderpoint_id` | integer | 4 B | Sí | Punto de la orden → `stock_warehouse_orderpoint` |
| FK | `production_location_id` | integer | 4 B | Sí | Ubicación de producción → `stock_location` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Referencia |
|  | `priority` | varchar | variable | Sí | Prioridad — Primero se reservarán los componentes para la orden de fabricación con mayor prioridad. |
|  | `origin` | varchar | variable | Sí | Origen — Referencia al documento que generó esta solicitud de orden de producción. |
|  | `state` | varchar | variable | Sí | Estado — * Borrador: la orden de fabricación aún no está confirmada. * Confirmada: la orden de fabricación está confirmada, las reglas de existenc… |
|  | `reservation_state` | varchar | variable | Sí | Preparación de la orden de fabricación — La preparación de fabricación para esta orden, según la configuración de la lista de materiales: * Listo: el material está disponible par… |
|  | `product_description_variants` | varchar | variable | Sí | Descripción personalizada |
|  | `consumption` | varchar | variable | No | Consumo |
|  | `product_qty` | numeric | variable | No | Cantidad a producir |
|  | `qty_producing` | numeric | variable | Sí | Cantidad en producción |
|  | `propagate_cancel` | boolean | 1 B | Sí | Cancelar propagación y dividir — Si se encuentra seleccionado, cuando el movimiento previo a este (generado por un siguiente aprovisionamiento) se cancele o divida, el mo… |
|  | `is_locked` | boolean | 1 B | Sí | Está bloqueado |
|  | `is_planned` | boolean | 1 B | Sí | Sus operaciones están planeadas |
|  | `allow_workorder_dependencies` | boolean | 1 B | Sí | Permitir dependencias de orden de trabajo |
|  | `is_outdated_bom` | boolean | 1 B | Sí | LdM obsoleta — La lista de materiales se actualizó después de que se creó la orden de fabricación |
|  | `date_deadline` | timestamp | 8 B | Sí | Fecha límite — Fecha informativa que permite definir cuándo se debe procesar la orden de fabricación a más tardar para cumplir con la entrega a tiempo. |
|  | `date_start` | timestamp | 8 B | No | Inicio — Fecha prevista de inicio de la producción o fecha de inicio efectivo de la producción. |
|  | `date_finished` | timestamp | 8 B | Sí | Fin — La fecha prevista para terminar la producción o la fecha real de cierre de producción. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `product_uom_qty` | double precision | 8 B | Sí | Cantidad total |
|  | `extra_cost` | double precision | 8 B | Sí | Costo unitario adicional |
| FK | `project_id` | integer | 4 B | Sí | Proyectos → `project_project` |
| FK | `sale_line_id` | integer | 4 B | Sí | Línea de la orden de venta de origen → `sale_order_line` |

### Tabla 4.2.8-25. `mrp_workorder`

**Orden de trabajo** · modelo `mrp.workorder` · módulo `mrp` · 25 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `workcenter_id` | integer | 4 B | No | Centro de trabajo → `mrp_workcenter` |
| FK | `production_id` | integer | 4 B | No | Orden de fabricación → `mrp_production` |
| FK | `leave_id` | integer | 4 B | Sí | Abandonar → `resource_calendar_leaves` — Espacio en el calendario del espacio de trabajo una vez planeado |
|  | `duration_percent` | integer | 4 B | Sí | Desviación de duración (%) |
| FK | `operation_id` | integer | 4 B | Sí | Operación → `mrp_routing_workcenter` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Orden de trabajo |
|  | `barcode` | varchar | variable | Sí | Código de barras |
|  | `production_availability` | varchar | variable | Sí | Disponibilidad de existencias — La preparación de fabricación para esta orden, según la configuración de la lista de materiales: * Listo: el material está disponible par… |
|  | `state` | varchar | variable | Sí | Estado |
|  | `cost_mode` | varchar | variable | Sí | Modo de costo |
|  | `qty_produced` | numeric | variable | Sí | Cantidad hecha — El número de productos ya gestionados en esta orden de trabajo |
|  | `duration_expected` | numeric | variable | Sí | Duración esperada |
|  | `qty_reported_from_previous_wo` | numeric | variable | Sí | Cantidad llevada — La cantidad ya producida está en espera de asignación en la cadena de órdenes parciales. |
|  | `date_start` | timestamp | 8 B | Sí | Inicio |
|  | `date_finished` | timestamp | 8 B | Sí | Fin |
|  | `production_date` | timestamp | 8 B | Sí | Fecha de producción |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `duration` | double precision | 8 B | Sí | Duración real |
|  | `duration_unit` | double precision | 8 B | Sí | Duración por unidad |
|  | `costs_hour` | double precision | 8 B | Sí | Costo por hora |

### Tabla 4.2.8-26. `mrp_workcenter`

**Centro de trabajo** · modelo `mrp.workcenter` · módulo `mrp` · 22 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `resource_id` | integer | 4 B | No | Recurso → `resource_resource` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `resource_calendar_id` | integer | 4 B | Sí | Horas de trabajo → `resource_calendar` — Define el horario de trabajo del recurso. Si no configuras uno, su horario será completamente flexible. |
|  | `sequence` | integer | 4 B | No | Secuencia — Indica el orden de secuencia al mostrar una lista de centros de trabajo. |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Centro de trabajo |
|  | `code` | varchar | variable | Sí | Código |
|  | `working_state` | varchar | variable | Sí | Estado del centro de trabajo |
|  | `note` | text | variable | Sí | Descripción |
|  | `active` | boolean | 1 B | Sí | Activo — Si desmarca el campo activo podrá ocultar el registro del recurso sin eliminarlo. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `time_efficiency` | double precision | 8 B | Sí | Eficiencia de tiempo — Este campo se utiliza para calcular la duración esperada de una orden de trabajo en este centro de trabajo. Por ejemplo, si una orden de… |
|  | `costs_hour` | double precision | 8 B | Sí | Costo por hora — Costo de procesamiento por hora. |
|  | `time_start` | double precision | 8 B | Sí | Tiempo de preparación |
|  | `time_stop` | double precision | 8 B | Sí | Tiempo de limpieza |
|  | `oee_target` | double precision | 8 B | Sí | Objetivo de eficiencia general de los equipos — Objetivo de eficiencia efectiva general en porcentaje |
| FK | `expense_account_id` | integer | 4 B | Sí | Cuenta de gastos → `account_account` — El gasto se contabiliza al marcar la orden de fabricación como hecha. Si no se establece, se utilizará la cuenta de gastos del producto f… |
|  | `analytic_distribution` | jsonb | variable | Sí | Distribución analítica |

### Tabla 4.2.8-27. `mrp_routing_workcenter`

**Uso del centro de trabajo** · modelo `mrp.routing.workcenter` · módulo `mrp` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `workcenter_id` | integer | 4 B | No | Centro de trabajo → `mrp_workcenter` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Indica el orden de secuencia al mostrar una lista de enrutamientos de centros de trabajo. |
| FK | `bom_id` | integer | 4 B | No | Lista de materiales → `mrp_bom` |
|  | `time_mode_batch` | integer | 4 B | Sí | Según |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Operación |
|  | `time_mode` | varchar | variable | Sí | Cálculo de duración |
|  | `cost_mode` | varchar | variable | Sí | Costo basado en — Determina la forma en la que Odoo calcula el costo de la operación: - Basado en el tiempo real: El costo se calcula según el tiempo regis… |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `time_cycle_manual` | double precision | 8 B | Sí | Duración manual — Tiempo en minutos:- En modo fijo, el tiempo usado- En modo calculado, el supuesto primer momento cuando todavía no hay órdenes de trabajo |

## Compras

### Tabla 4.2.8-28. `purchase_order`

**Orden de compra** · modelo `purchase.order` · módulo `purchase` · 40 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | No | Proveedor → `res_partner` — Puede encontrar un proveedor por su nombre, NIF, correo electrónico o referencia interna. |
| FK | `dest_address_id` | integer | 4 B | Sí | Dirección de entrega → `res_partner` — Proporcione una dirección si desea entregar directamente desde el proveedor al cliente. De lo contrario, se entregará en su propia empresa. |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
|  | `invoice_count` | integer | 4 B | Sí | Número de facturas |
| FK | `fiscal_position_id` | integer | 4 B | Sí | Posición fiscal → `account_fiscal_position` |
| FK | `payment_term_id` | integer | 4 B | Sí | Términos de pago → `account_payment_term` |
| FK | `incoterm_id` | integer | 4 B | Sí | Incoterm → `account_incoterms` — Los términos de comercio internacional son una serie de condiciones comerciales usadas en las transacciones internacionales. |
| FK | `user_id` | integer | 4 B | Sí | Comprador → `res_users` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
|  | `reminder_date_before_receipt` | integer | 4 B | Sí | Días antes de la recepción |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `name` | varchar | variable | No | Referencia de la orden |
|  | `priority` | varchar | variable | Sí | Prioridad |
|  | `origin` | varchar | variable | Sí | Origen — Referencia del documento que generó esta solicitud de orden de compra (por ejemplo, una orden de venta) |
|  | `partner_ref` | varchar | variable | Sí | Referencia de proveedor — Referencia de la orden de venta o la oferta que envió el proveedor. Se utiliza para conciliar inventario al recibir los productos, ya que… |
|  | `state` | varchar | variable | Sí | Estado |
|  | `invoice_status` | varchar | variable | Sí | Estado de facturación |
|  | `note` | text | variable | Sí | Términos y condiciones |
|  | `amount_untaxed` | numeric | variable | Sí | Subtotal |
|  | `amount_tax` | numeric | variable | Sí | Impuestos |
|  | `amount_total` | numeric | variable | Sí | Total |
|  | `amount_total_cc` | numeric | variable | Sí | Total en moneda |
|  | `currency_rate` | numeric | variable | Sí | Tasa de cambio |
|  | `locked` | boolean | 1 B | Sí | Bloqueado — No puede modificar las órdenes de compra bloqueadas. |
|  | `acknowledged` | boolean | 1 B | Sí | Reconocido — Indica que el proveedor confirmó la recepción de la orden de compra. |
|  | `receipt_reminder_email` | boolean | 1 B | Sí | Correo electrónico del recordatorio de la entrega |
|  | `date_order` | timestamp | 8 B | No | Fecha límite de la orden — Representa la fecha en la que la solicitud de cotización debe validarse y convertirse en una orden de compra. |
|  | `date_approve` | timestamp | 8 B | Sí | Fecha de confirmación |
|  | `date_planned` | timestamp | 8 B | Sí | Entrega esperada — Fecha de entrega prometida por el proveedor. Se utiliza para determinar la llegada esperada de los productos. |
|  | `date_calendar_start` | timestamp | 8 B | Sí | Fecha de inicio del calendario |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `project_id` | integer | 4 B | Sí | Proyectos → `project_project` |
| FK | `picking_type_id` | integer | 4 B | No | Entregar a → `stock_picking_type` — Esto determinará el tipo de operación del envío entrante |
|  | `incoterm_location` | varchar | variable | Sí | Ubicación del incoterm |
|  | `receipt_status` | varchar | variable | Sí | Estado de entrega — Rojo: con demora Naranja: por procesar hoy Verde: a tiempo |
|  | `effective_date` | timestamp | 8 B | Sí | Llegada — Fecha de finalización de la primera orden de entrega. |

### Tabla 4.2.8-29. `purchase_order_line`

**Línea de la orden de compra** · modelo `purchase.order.line` · módulo `purchase` · 34 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `product_uom_id` | integer | 4 B | Sí | Unidad → `uom_uom` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `order_id` | integer | 4 B | No | Referencia de la orden → `purchase_order` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` — Puede encontrar un proveedor por su nombre, NIF, correo electrónico o referencia interna. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `qty_received_method` | varchar | variable | Sí | Método de cantidad recibida — La cantidad recibida se puede calcular en automático con el mecanismo según la configuración del producto: - Manual: la cantidad se estab… |
|  | `display_type` | varchar | variable | Sí | Tipo de visualización — Campo técnico para propósitos de usabilidad. |
|  | `analytic_distribution` | jsonb | variable | Sí | Distribución analítica |
|  | `name` | text | variable | No | Descripción |
|  | `product_qty` | numeric | variable | No | Cantidad |
|  | `discount` | numeric | variable | Sí | Descuento (%) |
|  | `price_unit` | numeric | variable | No | Precio unitario |
|  | `price_subtotal` | numeric | variable | Sí | Subtotal |
|  | `price_total` | numeric | variable | Sí | Total |
|  | `qty_invoiced` | numeric | variable | Sí | Cant. facturada |
|  | `qty_received` | numeric | variable | Sí | Cantidad recibida |
|  | `qty_received_manual` | numeric | variable | Sí | Cantidad manual recibida |
|  | `qty_to_invoice` | numeric | variable | Sí | Cantidad a facturar |
|  | `is_downpayment` | boolean | 1 B | Sí | Es un anticipo |
|  | `date_planned` | timestamp | 8 B | Sí | Entrega esperada — Fecha de entrega estimada del proveedor. Esta fecha tiene como valor predeterminado el plazo de entrega de la lista de precios del provee… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `product_uom_qty` | double precision | 8 B | Sí | Cantidad total |
|  | `price_tax` | double precision | 8 B | Sí | Impuesto |
|  | `technical_price_unit` | double precision | 8 B | Sí | Precio unitario técnico — Campo técnico para el cálculo del precio |
| FK | `orderpoint_id` | integer | 4 B | Sí | Punto de la orden → `stock_warehouse_orderpoint` |
| FK | `location_final_id` | integer | 4 B | Sí | Ubicación del aprovisionamiento → `stock_location` |
|  | `product_description_variants` | varchar | variable | Sí | Descripción personalizada |
|  | `propagate_cancel` | boolean | 1 B | Sí | Propagar cancelación |
| FK | `sale_line_id` | integer | 4 B | Sí | Artículo de la venta de origen → `sale_order_line` |

## Facturación

### Tabla 4.2.8-30. `account_move`

**Asiento contable** · modelo `account.move` · módulo `account` · 75 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence_number` | integer | 4 B | Sí | Número de secuencia |
| FK | `message_main_attachment_id` | integer | 4 B | Sí | Archivo adjunto principal → `ir_attachment` |
| FK | `journal_id` | integer | 4 B | No | Diario → `account_journal` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `origin_payment_id` | integer | 4 B | Sí | Pago → `account_payment` |
| FK | `statement_line_id` | integer | 4 B | Sí | Línea de estado de cuenta → `account_bank_statement_line` |
| FK | `tax_cash_basis_rec_id` | integer | 4 B | Sí | Asiento de base de impuesto en efectivo de → `account_partial_reconcile` |
| FK | `tax_cash_basis_origin_move_id` | integer | 4 B | Sí | Origen de base de efectivo → `account_move` — El asiento contable a partir del cual se creó este asiento de base fiscal. |
| FK | `auto_post_origin_id` | integer | 4 B | Sí | Primer asiento recurrente → `account_move` |
|  | `secure_sequence_number` | integer | 4 B | Sí | Secuencia inalterable sin espacios # |
| FK | `invoice_payment_term_id` | integer | 4 B | Sí | Términos de pago → `account_payment_term` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `commercial_partner_id` | integer | 4 B | Sí | Entidad comercial → `res_partner` |
| FK | `partner_shipping_id` | integer | 4 B | Sí | Dirección de entrega → `res_partner` — La dirección de envío se usará para calcular la posición fiscal. |
| FK | `partner_bank_id` | integer | 4 B | Sí | Banco receptor → `res_partner_bank` — Número de cuenta bancaria a la que se pagará la factura. Una cuenta bancaria de la empresa si esta es una factura de cliente o una nota d… |
| FK | `fiscal_position_id` | integer | 4 B | Sí | Posición fiscal → `account_fiscal_position` — Las posiciones fiscales se utilizan para adaptar impuestos y cuentas para determinados clientes u ordenes de venta/facturas. El valor pre… |
| FK | `preferred_payment_method_line_id` | integer | 4 B | Sí | Línea de método de pago preferido → `account_payment_method_line` |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
| FK | `reversed_entry_id` | integer | 4 B | Sí | Reversión de → `account_move` |
| FK | `invoice_user_id` | integer | 4 B | Sí | Vendedor → `res_users` |
| FK | `invoice_incoterm_id` | integer | 4 B | Sí | Incoterm → `account_incoterms` — Los términos de comercio internacional son una serie de términos comerciales usados en las transacciones internacionales. |
| FK | `invoice_cash_rounding_id` | integer | 4 B | Sí | Método de redondeo de efectivo → `account_cash_rounding` — Define la moneda más pequeña que se puede usar para pagar en efectivo. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `sequence_prefix` | varchar | variable | Sí | Prefijo de secuencia |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `name` | varchar | variable | Sí | Número |
|  | `ref` | varchar | variable | Sí | Referencia |
|  | `state` | varchar | variable | No | Estado |
|  | `move_type` | varchar | variable | No | Tipo |
|  | `auto_post` | varchar | variable | No | Publicar automáticamente — Especificar si este asiento se publica de forma automática en su fecha contable, y cualquier factura recurrente similar. |
|  | `inalterable_hash` | varchar | variable | Sí | Hash de inalterabilidad |
|  | `payment_reference` | varchar | variable | Sí | Referencia de pago — La referencia de pago para establecer en apuntes contables. |
|  | `qr_code_method` | varchar | variable | Sí | Código QR de pago — Tipo de código QR que se generará para el pago de esta factura al imprimirla. Si se deja en blanco, se utilizará el primer método disponi… |
|  | `payment_state` | varchar | variable | Sí | Estado del pago |
|  | `invoice_source_email` | varchar | variable | Sí | Correo electrónico de origen |
|  | `invoice_partner_display_name` | varchar | variable | Sí | Nombre del contacto a mostrar en la factura |
|  | `invoice_origin` | varchar | variable | Sí | Origen — El documento o documentos que generaron esta factura |
|  | `incoterm_location` | varchar | variable | Sí | Ubicación del Incoterm |
|  | `date` | date | 4 B | No | Fecha |
|  | `auto_post_until` | date | 4 B | Sí | Publicar automáticamente hasta — Este movimiento recurrente se publicará hasta e incluida esta fecha. |
|  | `invoice_date` | date | 4 B | Sí | Fecha de la factura |
|  | `invoice_date_due` | date | 4 B | Sí | Fecha de vencimiento |
|  | `delivery_date` | date | 4 B | Sí | Fecha de entrega |
|  | `taxable_supply_date` | date | 4 B | Sí | Fecha de suministro gravable |
|  | `sending_data` | jsonb | variable | Sí | Enviando datos |
|  | `narration` | text | variable | Sí | Términos y condiciones |
|  | `invoice_currency_rate` | numeric | variable | Sí | Tasa de cambio — Tasa de cambio de la moneda de la empresa a la del documento. |
|  | `amount_untaxed` | numeric | variable | Sí | Subtotal |
|  | `amount_tax` | numeric | variable | Sí | Impuesto |
|  | `amount_total` | numeric | variable | Sí | Total |
|  | `amount_residual` | numeric | variable | Sí | Cantidad por pagar |
|  | `amount_untaxed_signed` | numeric | variable | Sí | Importe sin impuestos firmado |
|  | `amount_untaxed_in_currency_signed` | numeric | variable | Sí | Importe sin impuestos en la moneda firmada |
|  | `amount_tax_signed` | numeric | variable | Sí | Impuesto firmado |
|  | `amount_total_signed` | numeric | variable | Sí | Total firmado |
|  | `amount_total_in_currency_signed` | numeric | variable | Sí | Total en moneda firmado |
|  | `amount_residual_signed` | numeric | variable | Sí | Importe pendiente firmado |
|  | `quick_edit_total_amount` | numeric | variable | Sí | Total (impuestos incluidos) — Utilice este campo para codificar el importe total de la factura. Odoo creará de forma automática una línea de factura con valores predet… |
|  | `always_tax_exigible` | boolean | 1 B | Sí | Siempre elegible para impuestos |
|  | `checked` | boolean | 1 B | Sí | Revisado |
|  | `posted_before` | boolean | 1 B | Sí | Registrado antes |
|  | `made_sequence_gap` | boolean | 1 B | Sí | Causó un espacio en la secuencia |
|  | `is_manually_modified` | boolean | 1 B | Sí | Modificado de forma manual |
|  | `is_move_sent` | boolean | 1 B | Sí | Es un movimiento enviado — Indica que se envió la factura o pago o que se generó el PDF. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `debit_origin_id` | integer | 4 B | Sí | Factura original debitada → `account_move` |
| FK | `l10n_latam_document_type_id` | integer | 4 B | Sí | Tipo de Documento → `l10n_latam_document_type` |
| FK | `reversed_pos_order_id` | integer | 4 B | Sí | Orden del PdV revertida → `pos_order` — La orden del PdV que se revirtió después de cerrar la sesión para crear una factura para ella. |
| FK | `campaign_id` | integer | 4 B | Sí | Campaña → `utm_campaign` — Este es el nombre que te ayuda a identificar tus campañas, por ejemplo: descuentos_octubre, rebajas_de_navidad |
| FK | `source_id` | integer | 4 B | Sí | Origen → `utm_source` — Esta es la fuente del enlace. Por ejemplo: motor de búsqueda, otro dominio o nombre de lista de correos electrónicos |
| FK | `medium_id` | integer | 4 B | Sí | Medio → `utm_medium` — Este es el método de entrega. Por ejemplo: correo postal, correo electrónico, publicidad web |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |

### Tabla 4.2.8-31. `account_move_line`

**Apunte contable** · modelo `account.move.line` · módulo `account` · 61 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `move_id` | integer | 4 B | No | Asiento contable → `account_move` |
| FK | `journal_id` | integer | 4 B | Sí | Diario → `account_journal` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `company_currency_id` | integer | 4 B | Sí | Moneda de la empresa → `res_currency` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `account_id` | integer | 4 B | Sí | Cuenta → `account_account` |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `reconcile_model_id` | integer | 4 B | Sí | Modelo de conciliación → `account_reconcile_model` |
| FK | `payment_id` | integer | 4 B | Sí | Emisor de pago → `account_payment` — El pago que creó este asiento |
| FK | `statement_line_id` | integer | 4 B | Sí | Línea de estado de cuenta del emisor → `account_bank_statement_line` — La línea del estado de cuenta que creó este asiento |
| FK | `statement_id` | integer | 4 B | Sí | Estado de cuenta → `account_bank_statement` — El estado de cuenta bancario que se utiliza para la conciliación bancaria |
| FK | `group_tax_id` | integer | 4 B | Sí | Grupo de impuestos originador → `account_tax` |
| FK | `tax_line_id` | integer | 4 B | Sí | Impuesto del emisor → `account_tax` — Indica que este apunte contable es una línea de impuesto |
| FK | `tax_group_id` | integer | 4 B | Sí | Grupo de impuestos del emisor → `account_tax_group` |
| FK | `tax_repartition_line_id` | integer | 4 B | Sí | Línea de distribución de impuestos de emisor → `account_tax_repartition_line` — Línea de distribución de impuestos que provocó la creación de esta línea de movimiento, en su caso |
| FK | `full_reconcile_id` | integer | 4 B | Sí | Conciliación → `account_full_reconcile` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `product_uom_id` | integer | 4 B | Sí | Unidad → `uom_uom` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `move_name` | varchar | variable | Sí | Número |
|  | `parent_state` | varchar | variable | Sí | Estado |
|  | `ref` | varchar | variable | Sí | Referencia |
|  | `name` | varchar | variable | Sí | Etiqueta |
|  | `matching_number` | varchar | variable | Sí | Conciliación # — Número coincidente para esta línea, "P" si solo se concilia parcialmente, o el nombre de la conciliación completa si existe. |
|  | `display_type` | varchar | variable | No | Mostrar como |
|  | `date` | date | 4 B | Sí | Fecha |
|  | `invoice_date` | date | 4 B | Sí | Fecha de la factura |
|  | `date_maturity` | date | 4 B | Sí | Fecha de vencimiento — Este campo se utiliza en asientos contables por pagar y por cobrar. Puede establecer la fecha límite para el pago de esta línea. |
|  | `discount_date` | date | 4 B | Sí | Fecha de descuento — La última fecha en la que se debe pagar el importe descontado para que se conceda el descuento de pago anticipado |
|  | `analytic_distribution` | jsonb | variable | Sí | Distribución analítica |
|  | `extra_tax_data` | jsonb | variable | Sí | Datos adicionales sobre impuestos |
|  | `debit` | numeric | variable | Sí | Débito |
|  | `credit` | numeric | variable | Sí | Crédito |
|  | `balance` | numeric | variable | Sí | Balance |
|  | `amount_currency` | numeric | variable | Sí | Importe en moneda — La cantidad que se expresa en una moneda alternativa si se trata de un asiento multimoneda. |
|  | `tax_base_amount` | numeric | variable | Sí | Importe base |
|  | `amount_residual` | numeric | variable | Sí | Importe residual — El importe residual en un apunte contable expresado en la moneda de la empresa. |
|  | `amount_residual_currency` | numeric | variable | Sí | Importe residual en moneda — El importe residual en un apunte contable en su moneda (es probable que no sea la que usa la empresa). |
|  | `quantity` | numeric | variable | Sí | Cantidad — La cantidad opcional expresada en el apunte, por ejemplo: número de productos vendidos. Esta cantidad no supone un requisito legal pero e… |
|  | `price_unit` | numeric | variable | Sí | Precio unitario |
|  | `price_subtotal` | numeric | variable | Sí | Subtotal |
|  | `price_total` | numeric | variable | Sí | Total |
|  | `discount` | numeric | variable | Sí | Descuento (%) |
|  | `discount_amount_currency` | numeric | variable | Sí | Importe de descuento en moneda |
|  | `discount_balance` | numeric | variable | Sí | Balance de descuento |
|  | `is_storno` | boolean | 1 B | Sí | Contabilidad Storno de la empresa — Campo de utilidad para expresar si el apunte contable se somete a la contabilidad Storno |
|  | `is_imported` | boolean | 1 B | Sí | Importado |
|  | `reconciled` | boolean | 1 B | Sí | Conciliado |
|  | `collapse_composition` | boolean | 1 B | Sí | Ocultar composición — Si se marca, las líneas después de esta sección no se mostrarán en los reportes ni en el portal. |
|  | `collapse_prices` | boolean | 1 B | Sí | Ocultar precios — Si se marca, los precios de las lineas después de esta sección no se mostrarán en los reportes ni el portal. |
|  | `no_followup` | boolean | 1 B | Sí | Sin seguimiento — Excluir este asiento de diario de reportes de seguimiento. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `deductible_amount` | double precision | 8 B | Sí | Deducibilidad |
| FK | `purchase_line_id` | integer | 4 B | Sí | Línea de la orden de compra → `purchase_order_line` |
|  | `is_downpayment` | boolean | 1 B | Sí | Es un anticipo |
| FK | `cogs_origin_id` | integer | 4 B | Sí | Origen del costo de los bienes vendidos → `account_move_line` |
| FK | `l10n_latam_document_type_id` | integer | 4 B | Sí | Tipo de Documento → `l10n_latam_document_type` |

### Tabla 4.2.8-32. `account_journal`

**Diario** · modelo `account.journal` · módulo `account` · 34 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `alias_id` | integer | 4 B | Sí | Alias → `mail_alias` |
| FK | `default_account_id` | integer | 4 B | Sí | Cuenta predeterminada → `account_account` |
| FK | `suspense_account_id` | integer | 4 B | Sí | Cuenta transitoria → `account_account` — Las transacciones de estados de cuenta bancarios se contabilizarán en la cuenta transitoria hasta la conciliación final que permita encon… |
| FK | `non_deductible_account_id` | integer | 4 B | Sí | Cuenta miscelánea privada → `account_account` — Cuenta que se utiliza para registrar la parte privada de los gastos mixtos. |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Se utiliza para ordenar los diarios en la vista de tablero |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` — La moneda utilizada para introducir estados de cuenta |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` — Empresa relacionada con este diario |
| FK | `invoice_template_pdf_report_id` | integer | 4 B | Sí | Reporte de la factura → `ir_act_report_xml` |
| FK | `profit_account_id` | integer | 4 B | Sí | Cuenta de ganancias → `account_account` — Se utiliza para registrar una ganancia cuando el balance final de una caja registradora difiere de lo calculado por el sistema |
| FK | `loss_account_id` | integer | 4 B | Sí | Cuenta de pérdidas → `account_account` — Se utiliza para registrar una pérdida cuando el balance final de una caja registradora difiere de lo calculado por el sistema |
| FK | `bank_account_id` | integer | 4 B | Sí | Cuenta bancaria → `res_partner_bank` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `color` | integer | 4 B | Sí | Índice de color |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `code` | varchar | 5 | No | Prefijo de secuencia — Nombre corto que se utiliza para mostrar. Los asientos de este diario también se nombrarán con este prefijo de forma predeterminada. |
|  | `type` | varchar | variable | No | Tipo — Selecciona "Ventas" para ver los diarios con las facturas de clientes. Selecciona "Compras" para ver los diarios con las facturas de prov… |
|  | `invoice_reference_type` | varchar | variable | No | Tipo de comunicación — Puede establecer aquí la comunicación predeterminada que aparecerá en las facturas del cliente, una vez validada, para ayudar al cliente… |
|  | `invoice_reference_model` | varchar | variable | No | Estándar de comunicación — Puede elegir diferentes modelos para cada tipo de referencia. El predeterminado es la referencia de Odoo. |
|  | `bank_statements_source` | varchar | variable | Sí | Conexiones bancarias — Define cómo se registrarán los estados de cuenta bancarios |
|  | `incoming_einvoice_notification_email` | varchar | variable | Sí | Enviar copia a — Email addresses that should receive invoices copy/return reminders. Separate entries with ';'. |
|  | `name` | jsonb | variable | No | Nombre del diario |
|  | `sequence_override_regex` | text | variable | Sí | Regex de anulación de secuencia — Campo técnico que se utiliza para imponer una composición de secuencia compleja que el sistema normalmente malinterpretaría. Esta es una… |
|  | `active` | boolean | 1 B | Sí | Activo — Establezca el activo como false para ocultar el diario sin eliminarlo. |
|  | `is_self_billing` | boolean | 1 B | Sí | Autofactura — Este diario es para auto facturas. Las facturas se crearán usando una secuencia diferente por contacto. |
|  | `restrict_mode_hash_table` | boolean | 1 B | Sí | Proteger asientos registrados con hash — Si está seleccionada, al registrar un asiento se genera un hash retroactivo en todos los movimientos de la secuencia desde el primer hast… |
|  | `refund_sequence` | boolean | 1 B | Sí | Secuencia de notas de crédito dedicada — Selecciona esta casilla si no deseas compartir la misma secuencia de facturas y notas de crédito de este diario |
|  | `payment_sequence` | boolean | 1 B | Sí | Secuencia de pago dedicada — Selecciona esta casilla si no deseas compartir la misma secuencia en pagos y transacciones bancarias publicadas en este diario |
|  | `show_on_dashboard` | boolean | 1 B | Sí | Mostrar diario en el tablero — Si este diario debe mostrarse en el tablero o no |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `debit_sequence` | boolean | 1 B | Sí | Secuencia de notas de débito dedicada — Seleccione esta casilla si no desea compartir la misma secuencia de facturas y notas de débito de este diario |
|  | `l10n_latam_use_documents` | boolean | 1 B | Sí | Usa Documentos? — Si está activo: se usará para la facturación (facturas, notas de débito y notas de crédito). Si no se configura, se usará para registrar… |

## Seguridad y mesa de servicios

### Tabla 4.2.8-33. `res_users`

**Usuario** · modelo `res.users` · módulo `base` · 25 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` — La empresa predeterminada para este usuario. |
| FK | `partner_id` | integer | 4 B | No | Contacto relacionado → `res_partner` — Datos relacionados al contacto del usuario |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |
|  | `login` | varchar | variable | No | Usuario — Se utiliza para conectarse al sistema. |
|  | `password` | varchar | variable | Sí | Contraseña — Déjelo vacío si no quiere que el usuario se pueda conectar al sistema. |
|  | `action_id` | integer | 4 B | Sí | Acción de inicio — Si se especifica, esta acción se ejecutará cuando este usuario entre en el sistema, en adición al menú estándar. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `signature` | text | variable | Sí | Firma de correo electrónico |
|  | `share` | boolean | 1 B | Sí | Compartir usuario — Usuario externo con acceso limitado, creado solo con el propósito de compartir datos. |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `totp_last_counter` | integer | 4 B | Sí | Último contador TOTP |
|  | `totp_secret` | varchar | variable | Sí | Secreto TOTP |
|  | `tour_enabled` | boolean | 1 B | Sí | Integración |
|  | `notification_type` | varchar | variable | No | Notificación — Política sobre cómo gestionar las notificaciones del chatter: - Por correo electrónico: las notificaciones se envían a su dirección de co… |
|  | `manual_im_status` | varchar | variable | Sí | Estado de mensajería instantánea establecido de forma manual por el usuario |
|  | `out_of_office_message` | text | variable | Sí | Mensaje de respuesta cuando estés de vacaciones |
|  | `out_of_office_from` | timestamp | 8 B | Sí | Fuera de la oficina de |
|  | `out_of_office_to` | timestamp | 8 B | Sí | Fuera de la oficina hasta |
|  | `odoobot_state` | varchar | variable | Sí | Estado de OdooBot |
|  | `odoobot_failed` | boolean | 1 B | Sí | Error de OdooBot |
| FK | `sale_team_id` | integer | 4 B | Sí | Equipo de ventas del usuario → `crm_team` — Usuario principal del equipo de ventas. En particular, se utiliza para el flujo de trabajo y para establecer el equipo de ventas en factu… |
|  | `property_warehouse_id` | jsonb | variable | Sí | Almacén predeterminado |

### Tabla 4.2.8-34. `res_groups`

**Grupos de acceso** · modelo `res.groups` · módulo `base` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `name` | jsonb | variable | No | Nombre |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `privilege_id` | integer | 4 B | Sí | Privilegio → `res_groups_privilege` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `comment` | jsonb | variable | Sí | Comentario |
|  | `share` | boolean | 1 B | Sí | Compartir grupo — Grupo creado para configurar permisos de acceso para compartir información con algunos usuarios. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `api_key_duration` | double precision | 8 B | Sí | Duración máxima de claves API en días — Determina la duración máxima de una clave API creada por un usuario que pertenece a este grupo. |

### Tabla 4.2.8-35. `auditlog_rule`

**Auditlog - Regla** · modelo `auditlog.rule` · módulo `auditlog` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | Sí | Modelo → `ir_model` — Seleccione el modelo al que quiere generar un registro. |
| FK | `action_id` | integer | 4 B | Sí | Acción → `ir_act_window` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Actualizado última vez por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `model_name` | varchar | variable | Sí | Nombre del modelo |
|  | `model_model` | varchar | variable | Sí | Nombre técnico del modelo |
|  | `log_type` | varchar | variable | No | Tipo — Full log: the previous values of updated fields are retrieved and stored on the log lines. This includes stored computed fields on the up… |
|  | `state` | varchar | variable | No | Estado |
|  | `log_read` | boolean | 1 B | Sí | Registrar lecturas — Marque esta casilla si desea hacer seguimiento de lectura/apertura de cualquier registro del modelo de esta regla |
|  | `log_write` | boolean | 1 B | Sí | Registrar modificaciones — Marque esta casilla si desea hacer un seguimiento de las modificaciones de cualquier registro del modelo de esta regla |
|  | `log_unlink` | boolean | 1 B | Sí | Borrar registros — Marque esta casilla si desea hacer un seguimiento del borrado de los registros del modelo de esta regla |
|  | `log_create` | boolean | 1 B | Sí | Crear registros — Marque esta casilla si desea hacer un seguimiento de la creacion de cualquier registro del modelo de esta regla |
|  | `log_export_data` | boolean | 1 B | Sí | Log Exports — Select this if you want to keep track of exports of the model of this rule |
|  | `capture_record` | boolean | 1 B | Sí | Log values on deletion — In case of full logging, also log all values of records at the time of deletion. |
|  | `create_date` | timestamp | 8 B | Sí | Creado en |
|  | `write_date` | timestamp | 8 B | Sí | Ultima Actualización |

### Tabla 4.2.8-36. `project_task`

**Tarea** · modelo `project.task` · módulo `project` · 41 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Sequence |
| FK | `stage_id` | integer | 4 B | Sí | Etapa → `project_task_type` |
| FK | `project_id` | integer | 4 B | Sí | Proyectos → `project_project` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `color` | integer | 4 B | Sí | Color Index |
| FK | `displayed_image_id` | integer | 4 B | Sí | Imagen de portada → `ir_attachment` |
| FK | `parent_id` | integer | 4 B | Sí | Tarea principal → `project_task` |
| FK | `milestone_id` | integer | 4 B | Sí | Objetivo → `project_milestone` — Ofrezca sus servicios de forma automática cada vez que se alcance un objetivo, se puede hacer vinculándolo a un artículo de la orden de v… |
| FK | `recurrence_id` | integer | 4 B | Sí | Recurrencia → `project_task_recurrence` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email_cc` | varchar | variable | Sí | CC del correo electrónico — Correos electrónicos en el campo con copia de los correos recibidos de esta tarea que no están vinculados a un cliente existente. |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `name` | varchar | variable | No | Título |
|  | `priority` | varchar | variable | Sí | Prioridad |
|  | `state` | varchar | variable | No | Estado |
|  | `partner_phone` | varchar | variable | Sí | Número de contacto |
|  | `email_from` | varchar | variable | Sí | Correo electrónico de |
|  | `html_field_history` | jsonb | variable | Sí | Datos del historial |
|  | `task_properties` | jsonb | variable | Sí | Propiedades |
|  | `description` | text | variable | Sí | Descripción |
|  | `working_hours_open` | numeric | variable | Sí | Horas laborables por asignar |
|  | `working_hours_close` | numeric | variable | Sí | Horas laborables para cerrar |
|  | `active` | boolean | 1 B | Sí | Active |
|  | `display_in_project` | boolean | 1 B | Sí | Display In Project |
|  | `recurring_task` | boolean | 1 B | Sí | Recurrente |
|  | `is_template` | boolean | 1 B | Sí | Is Template |
|  | `has_template_ancestor` | boolean | 1 B | Sí | Has Template Ancestor |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `date_end` | timestamp | 8 B | Sí | Fecha de finalización |
|  | `date_assign` | timestamp | 8 B | Sí | Fecha de asignación — Fecha en la que se asignó (o desasignó) esta tarea por última vez. Gracias a esta información podrá obtener estadísticas sobre cuánto tar… |
|  | `date_deadline` | timestamp | 8 B | Sí | Fecha límite |
|  | `date_last_stage_update` | timestamp | 8 B | Sí | Última actualización de la etapa — Fecha en la que se modificó por última vez el estado de su tarea. Gracias a esta información podrá identificar qué tareas están en pausa… |
|  | `rating_last_value` | double precision | 8 B | Sí | Último valor de la calificación |
|  | `allocated_hours` | double precision | 8 B | Sí | Tiempo asignado |
|  | `working_days_open` | double precision | 8 B | Sí | Días laborables por asignar |
|  | `working_days_close` | double precision | 8 B | Sí | Días laborables por cerrar |
|  | `sla_estado` | varchar | variable | Sí | **[donofrio_base]** Cumplimiento del SLA — Cumplido si el ticket se cerró antes de su fecha límite; incumplido si se cerró después. Solo se calcula en los tickets con fecha límite. |

## Calidad (M1)

### Tabla 4.2.8-37. `donofrio_calidad_punto`

**Punto de control de calidad** · modelo `donofrio.calidad.punto` · módulo `donofrio_calidad` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `categ_id` | integer | 4 B | Sí | Categoría de producto → `product_category` — Si se deja vacío, el punto se mide en todos los productos. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `tipo` | varchar | variable | No | Tipo |
|  | `unidad` | varchar | variable | Sí | Unidad — Por ejemplo: °C, g, %. |
|  | `name` | jsonb | variable | No | Punto de control |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `valor_min` | double precision | 8 B | Sí | Mínimo |
|  | `valor_max` | double precision | 8 B | Sí | Máximo |

### Tabla 4.2.8-38. `donofrio_calidad_inspeccion`

**Inspección de calidad del lote** · modelo `donofrio.calidad.inspeccion` · módulo `donofrio_calidad` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `production_id` | integer | 4 B | No | Orden de producción → `mrp_production` |
| FK | `lot_id` | integer | 4 B | No | Lote → `stock_lot` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `company_id` | integer | 4 B | No | Compañía → `res_company` |
| FK | `inspector_id` | integer | 4 B | Sí | Inspector → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Número |
|  | `state` | varchar | variable | No | Estado |
|  | `motivo_rechazo` | text | variable | Sí | Motivo del rechazo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### Tabla 4.2.8-39. `donofrio_calidad_linea`

**Medición de la inspección de calidad** · modelo `donofrio.calidad.linea` · módulo `donofrio_calidad` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `inspeccion_id` | integer | 4 B | No | Inspeccion → `donofrio_calidad_inspeccion` |
| FK | `punto_id` | integer | 4 B | No | Punto de control → `donofrio_calidad_punto` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `resultado` | varchar | variable | Sí | Resultado |
|  | `medido` | boolean | 1 B | Sí | Medido |
|  | `cumple_manual` | boolean | 1 B | Sí | Cumple |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `medicion` | double precision | 8 B | Sí | Medición |

## Heladeros (M2)

### Tabla 4.2.8-40. `donofrio_liquidacion`

**Liquidación diaria del heladero** · modelo `donofrio.liquidacion` · módulo `donofrio_heladeros` · 19 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | No | Heladero → `res_partner` |
| FK | `pricelist_id` | integer | 4 B | No | Lista de precios → `product_pricelist` |
| FK | `company_id` | integer | 4 B | No | Company → `res_company` |
| FK | `order_id` | integer | 4 B | Sí | Pedido de venta → `sale_order` |
| FK | `liquidador_id` | integer | 4 B | No | Liquidador → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Created by → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Last Updated by → `res_users` |
|  | `name` | varchar | variable | Sí | Número |
|  | `state` | varchar | variable | No | Estado |
|  | `fecha` | date | 4 B | No | Fecha |
|  | `total_importe` | numeric | variable | Sí | Importe vendido |
|  | `total_comision` | numeric | variable | Sí | Comisión |
|  | `diferencia_efectivo` | numeric | variable | Sí | Diferencia de efectivo — Efectivo entregado menos el importe vendido. Positivo: el heladero entregó de más (a su favor). Negativo: entregó de menos y debe la dife… |
|  | `create_date` | timestamp | 8 B | Sí | Created on |
|  | `write_date` | timestamp | 8 B | Sí | Last Updated on |
|  | `porcentaje_comision` | double precision | 8 B | Sí | Comisión (%) — Porcentaje del importe vendido que se queda el heladero. Valor supuesto del caso. |
|  | `efectivo_entregado` | double precision | 8 B | Sí | Efectivo entregado |
|  | `total_vendido` | double precision | 8 B | Sí | Unidades vendidas |

### Tabla 4.2.8-41. `donofrio_liquidacion_linea`

**Línea de la liquidación del heladero** · modelo `donofrio.liquidacion.linea` · módulo `donofrio_heladeros` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `liquidacion_id` | integer | 4 B | No | Liquidacion → `donofrio_liquidacion` |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `create_uid` | integer | 4 B | Sí | Created by → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Last Updated by → `res_users` |
|  | `precio_unitario` | numeric | variable | Sí | Precio |
|  | `importe` | numeric | variable | Sí | Importe |
|  | `create_date` | timestamp | 8 B | Sí | Created on |
|  | `write_date` | timestamp | 8 B | Sí | Last Updated on |
|  | `despachado` | double precision | 8 B | Sí | Despachado |
|  | `devuelto` | double precision | 8 B | Sí | Devuelto |
|  | `merma` | double precision | 8 B | Sí | Merma |
|  | `vendido` | double precision | 8 B | Sí | Vendido |

## Cadena de frío (M3)

### Tabla 4.2.8-42. `donofrio_temperatura`

**Lectura de temperatura** · modelo `donofrio.temperatura` · módulo `donofrio_calidad` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `location_id` | integer | 4 B | No | Ubicación → `stock_location` |
| FK | `user_id` | integer | 4 B | No | Registrado por → `res_users` |
| FK | `company_id` | integer | 4 B | Sí | Compañía → `res_company` — Deje vacío este campo si la ubicación se compartirá entre las empresas |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `observaciones` | text | variable | Sí | Observaciones |
|  | `fuera_de_rango` | boolean | 1 B | Sí | Fuera de rango |
|  | `fecha` | timestamp | 8 B | No | Fecha y hora |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `temperatura` | double precision | 8 B | No | Temperatura (°C) |
