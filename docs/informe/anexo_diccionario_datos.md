# Anexo: diccionario de datos del resto del esquema

> **Archivo generado** por [`scripts/diccionario_datos.py`](../../scripts/diccionario_datos.py); no se edita a mano. Origen: BD limpia con `donofrio_base`, `donofrio_calidad` y `donofrio_heladeros` instalados desde `develop` (Odoo 19.0, PostgreSQL 16).
>
> Complementa el [diccionario del núcleo](04_02_diccionario_datos.md) (4.2.8) con las otras 661 tablas del esquema, agrupadas por el módulo de Odoo que define cada modelo. El esquema completo tiene 703 tablas (42 en el núcleo). Mismo formato y mismas fuentes que el diccionario del núcleo.

## Índice por módulo

| Módulo | Tablas |
|---|---|
| `account` | 76 |
| `account_debit_note` | 2 |
| `account_payment` | 1 |
| `analytic` | 8 |
| `auditlog` | 8 |
| `auth_passkey` | 2 |
| `auth_totp` | 3 |
| `barcodes` | 2 |
| `base` | 102 |
| `base_address_extended` | 1 |
| `base_import` | 2 |
| `base_import_module` | 1 |
| `base_install_request` | 2 |
| `bus` | 1 |
| `calendar` | 11 |
| `crm` | 19 |
| `crm_iap_mine` | 10 |
| `digest` | 4 |
| `hr` | 17 |
| `hr_homeworking` | 1 |
| `hr_homeworking_calendar` | 1 |
| `hr_skills` | 9 |
| `html_editor` | 2 |
| `iap` | 4 |
| `l10n_latam_base` | 1 |
| `l10n_latam_invoice_document` | 1 |
| `l10n_pe` | 1 |
| `mail` | 65 |
| `mrp` | 33 |
| `mrp_account` | 3 |
| `onboarding` | 6 |
| `payment` | 13 |
| `phone_validation` | 2 |
| `point_of_sale` | 35 |
| `portal` | 5 |
| `privacy_lookup` | 3 |
| `product` | 33 |
| `product_expiry` | 4 |
| `project` | 29 |
| `project_todo` | 1 |
| `purchase` | 6 |
| `rating` | 1 |
| `resource` | 4 |
| `sale` | 10 |
| `sale_crm` | 1 |
| `sales_team` | 4 |
| `sms` | 10 |
| `snailmail` | 1 |
| `spreadsheet_dashboard` | 7 |
| `stock` | 64 |
| `stock_account` | 1 |
| `stock_sms` | 2 |
| `uom` | 1 |
| `utm` | 6 |
| `web` | 2 |
| `web_tour` | 3 |
| `sin módulo` | 14 |

## Módulo `account`

### `account_account`

**Cuenta** · modelo `account.account` · módulo `account` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `currency_id` | integer | 4 B | Sí | Moneda de la cuenta → `res_currency` — Obliga a que todos los apuntes contables en esta cuenta tengan una moneda específica (por ejemplo, los diarios bancarios). Los asientos p… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `account_type` | varchar | variable | No | Tipo — Usamos el tipo de cuenta para proporcionar información, generar reportes legales específicos para cada país, establecer las reglas para c… |
|  | `name` | jsonb | variable | No | Nombre de la cuenta |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `code_store` | jsonb | variable | Sí | Código de tienda |
|  | `note` | text | variable | Sí | Notas internas |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `reconcile` | boolean | 1 B | Sí | Permitir conciliación — Selecciona esta casilla si la cuenta permite vincular facturas y pagos con apuntes contables. |
|  | `non_trade` | boolean | 1 B | Sí | No comercial — Si se establece, esta cuenta pertenecerá a los reportes y filtros de cuentas por cobrar o por pagar no comerciales. En caso contrario, es… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `account_stock_variation_id` | integer | 4 B | Sí | Cuenta de variación → `account_account` — Al cierre, registra la variación del inventario del periodo en una cuenta específica |
| FK | `account_stock_expense_id` | integer | 4 B | Sí | Cuenta de gastos → `account_account` — Contrapartida usada al cierre para los ajustes contables de la valuación del inventario. |

### `account_account_account_merge_wizard_rel`

**Relación muchos a muchos entre «account.merge.wizard» y «account.account»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_merge_wizard_id` | integer | 4 B | No | Referencia a account_merge_wizard |
| PK, FK | `account_account_id` | integer | 4 B | No | Referencia a account_account |

### `account_account_account_tag`

**Relación muchos a muchos entre «account.account» y «account.account.tag»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_account_id` | integer | 4 B | No | Referencia a account_account |
| PK, FK | `account_account_tag_id` | integer | 4 B | No | Referencia a account_account_tag |

### `account_account_res_company_rel`

**Relación muchos a muchos entre «account.account» y «res.company»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_account_id` | integer | 4 B | No | Referencia a account_account |
| PK, FK | `res_company_id` | integer | 4 B | No | Referencia a res_company |

### `account_account_tag`

**Etiqueta de cuenta** · modelo `account.account.tag` · módulo `account` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` — País para el que está disponible esta etiqueta, cuando se aplica en los impuestos. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `applicability` | varchar | variable | No | Aplicabilidad |
|  | `name` | jsonb | variable | No | Nombre de la etiqueta |
|  | `active` | boolean | 1 B | Sí | Activo — Establezca el activo como false para ocultar la etiqueta de cuenta sin eliminarla. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_account_tag_account_move_line_rel`

**Relación muchos a muchos entre «account.move.line» y «account.account.tag»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_move_line_id` | integer | 4 B | No | Referencia a account_move_line |
| PK, FK | `account_account_tag_id` | integer | 4 B | No | Referencia a account_account_tag |

### `account_account_tag_account_tax_repartition_line_rel`

**Relación muchos a muchos entre «account.tax.repartition.line» y «account.account.tag»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_tax_repartition_line_id` | integer | 4 B | No | Referencia a account_tax_repartition_line |
| PK, FK | `account_account_tag_id` | integer | 4 B | No | Referencia a account_account_tag |

### `account_account_tax_default_rel`

**Relación muchos a muchos entre «account.account» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_id` | integer | 4 B | No | Referencia a account_account |
| PK, FK | `tax_id` | integer | 4 B | No | Referencia a account_tax |

### `account_accrued_orders_wizard`

**Asistente de órdenes devengadas** · modelo `account.accrued.orders.wizard` · módulo `account` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `journal_id` | integer | 4 B | No | Diario → `account_journal` |
| FK | `currency_id` | integer | 4 B | Sí | Moneda de la empresa → `res_currency` — Campo de utilidad para expresar la moneda del importe. |
| FK | `account_id` | integer | 4 B | No | Cuenta devengada → `account_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `date` | date | 4 B | No | Fecha |
|  | `reversal_date` | date | 4 B | No | Fecha de reversión |
|  | `amount` | numeric | variable | Sí | Importe — Especifique un valor arbitrario que se acumulará en una cuenta predeterminada para toda la orden, independientemente de los productos en… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_automatic_entry_wizard`

**Crear asientos automáticos** · modelo `account.automatic.entry.wizard` · módulo `account` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `destination_account_id` | integer | 4 B | Sí | A → `account_account` — Cuenta a la cual transferir. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `action` | varchar | variable | No | Acción |
|  | `account_type` | varchar | variable | Sí | Tipo de cuenta |
|  | `date` | date | 4 B | No | Fecha |
|  | `total_amount` | numeric | variable | Sí | Importe total — Importe total impactado por el asiento automático. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `percentage` | double precision | 8 B | Sí | Porcentaje — Porcentaje de cada línea sobre la que ejecutar la acción. |

### `account_automatic_entry_wizard_account_move_line_rel`

**Relación muchos a muchos entre «account.automatic.entry.wizard» y «account.move.line»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_automatic_entry_wizard_id` | integer | 4 B | No | Referencia a account_automatic_entry_wizard |
| PK, FK | `account_move_line_id` | integer | 4 B | No | Referencia a account_move_line |

### `account_autopost_bills_wizard`

**Asistente de registro automático de facturas** · modelo `account.autopost.bills.wizard` · módulo `account` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
|  | `nb_unmodified_bills` | integer | 4 B | Sí | Número de facturas sin modificar con anterioridad de este contacto |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_bank_statement`

**Estado de cuenta bancario** · modelo `account.bank.statement` · módulo `account` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — Empresa relacionada con este diario |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `journal_id` | integer | 4 B | Sí | Diario → `account_journal` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Referencia |
|  | `reference` | varchar | variable | Sí | Referencia externa |
|  | `first_line_index` | varchar | variable | Sí | Índice de primera línea |
|  | `date` | date | 4 B | Sí | Fecha |
|  | `balance_start` | numeric | variable | Sí | Balance inicial |
|  | `balance_end` | numeric | variable | Sí | Balance calculado |
|  | `balance_end_real` | numeric | variable | Sí | Saldo final |
|  | `is_complete` | boolean | 1 B | Sí | Completo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_bank_statement_ir_attachment_rel`

**Relación muchos a muchos entre «account.bank.statement» y «ir.attachment»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_bank_statement_id` | integer | 4 B | No | Referencia a account_bank_statement |
| PK, FK | `ir_attachment_id` | integer | 4 B | No | Referencia a ir_attachment |

### `account_bank_statement_line`

**Línea de estado de cuenta bancario** · modelo `account.bank.statement.line` · módulo `account` · 25 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `move_id` | integer | 4 B | No | Asiento contable → `account_move` |
| FK | `journal_id` | integer | 4 B | No | Diario → `account_journal` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `statement_id` | integer | 4 B | Sí | Estado de cuenta → `account_bank_statement` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `currency_id` | integer | 4 B | Sí | Moneda del diario → `res_currency` |
| FK | `foreign_currency_id` | integer | 4 B | Sí | Moneda extranjera → `res_currency` — La moneda alterna si se trata de un asiento multimoneda. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `account_number` | varchar | variable | Sí | Número de cuenta bancaria |
|  | `partner_name` | varchar | variable | Sí | Nombre del contacto |
|  | `transaction_type` | varchar | variable | Sí | Tipo de transacción |
|  | `payment_ref` | varchar | variable | Sí | Etiqueta |
|  | `internal_index` | varchar | variable | Sí | Referencia interna |
|  | `transaction_details` | jsonb | variable | Sí | Detalles de la transacción |
|  | `amount` | numeric | variable | Sí | Importe |
|  | `amount_currency` | numeric | variable | Sí | Importe en moneda — La cantidad que se expresa en una moneda alternativa si se trata de un asiento multimoneda. |
|  | `is_reconciled` | boolean | 1 B | Sí | Conciliado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `amount_residual` | double precision | 8 B | Sí | Importe residual |
| FK | `pos_session_id` | integer | 4 B | Sí | Sesión → `pos_session` |
| FK | `employee_id` | integer | 4 B | Sí | Empleado → `hr_employee` — El empleado que hizo el movimiento de efectivo. |

### `account_cash_rounding`

**Redondeo de efectivo de la cuenta** · modelo `account.cash.rounding` · módulo `account` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `strategy` | varchar | variable | No | Estrategia de redondeo — Especifique la manera en que se redondeará el importe de la factura a la precisión de redondeo |
|  | `rounding_method` | varchar | variable | No | Método de redondeo — La regla de desempate que se utiliza para las operaciones de redondeo de decimales |
|  | `name` | jsonb | variable | No | Nombre |
|  | `profit_account_id` | jsonb | variable | Sí | Cuenta de ganancias |
|  | `loss_account_id` | jsonb | variable | Sí | Cuenta de pérdidas |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `rounding` | double precision | 8 B | No | Precisión de redondeo — Representa la moneda más pequeña con valor distinto de cero (por ejemplo, 0.05). |

### `account_financial_year_op`

**Balance de apertura del año financiero** · modelo `account.financial.year.op` · módulo `account` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_fiscal_position`

**Posición fiscal** · modelo `account.fiscal.position` · módulo `account` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` — Aplicar solo si el país de entrega coincide. |
| FK | `country_group_id` | integer | 4 B | Sí | Grupo de países → `res_country_group` — Aplicar solo si el país de entrega coincide con el grupo. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `zip_from` | varchar | variable | Sí | Rango postal desde |
|  | `zip_to` | varchar | variable | Sí | Rango postal hasta |
|  | `foreign_vat` | varchar | variable | Sí | Identificación fiscal extranjera — La identificación fiscal de su empresa en la región mapeada por esta posición fiscal. |
|  | `name` | jsonb | variable | No | Posición fiscal |
|  | `note` | jsonb | variable | Sí | Notas — Menciones legales que se tienen que imprimir en las facturas. |
|  | `active` | boolean | 1 B | Sí | Activo — Al deseleccionar el campo actual se ocultará la posición fiscal sin eliminarla. |
|  | `auto_apply` | boolean | 1 B | Sí | Detectar de forma automática — Aplicar automáticamente el mapeo de impuestos y cuentas en las facturas cuando se cumplan los criterios de correspondencia (Número de ide… |
|  | `vat_required` | boolean | 1 B | Sí | Requiere número de identificación tributaria — Aplicar solo si el contacto tiene un número fiscal. |
|  | `is_domestic` | boolean | 1 B | Sí | Es local |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_fiscal_position_account`

**Mapeo de cuentas de posición fiscal** · modelo `account.fiscal.position.account` · módulo `account` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `position_id` | integer | 4 B | No | Posición fiscal → `account_fiscal_position` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `account_src_id` | integer | 4 B | No | Cuenta de producto → `account_account` |
| FK | `account_dest_id` | integer | 4 B | No | Cuenta alternativa → `account_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_fiscal_position_account_tax_rel`

**Relación muchos a muchos entre «account.fiscal.position» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_fiscal_position_id` | integer | 4 B | No | Referencia a account_fiscal_position |
| PK, FK | `account_tax_id` | integer | 4 B | No | Referencia a account_tax |

### `account_fiscal_position_res_country_state_rel`

**Relación muchos a muchos entre «account.fiscal.position» y «res.country.state»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_fiscal_position_id` | integer | 4 B | No | Referencia a account_fiscal_position |
| PK, FK | `res_country_state_id` | integer | 4 B | No | Referencia a res_country_state |

### `account_full_reconcile`

**Conciliación completa** · modelo `account.full.reconcile` · módulo `account` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_group`

**Grupo de cuentas** · modelo `account.group` · módulo `account` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_id` | integer | 4 B | Sí | Principal → `account_group` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code_prefix_start` | varchar | variable | Sí | Inicio de prefijo de código |
|  | `code_prefix_end` | varchar | variable | Sí | Fin de prefijo de código |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_incoterms`

**Incoterms** · modelo `account.incoterms` · módulo `account` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | 3 | No | Código — Código estándar del Incoterm |
|  | `name` | jsonb | variable | No | Nombre — Los Incoterms son una serie de términos de venta. Se usan para dividir los costos de la transacción y determinar las obligaciones entre e… |
|  | `active` | boolean | 1 B | Sí | Activo — Al deseleccionar el campo activo ocultará un INCOTERM que no use. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_invoice_transaction_rel`

**Relación muchos a muchos entre «account.move» y «payment.transaction»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `invoice_id` | integer | 4 B | No | Referencia a account_move |
| PK, FK | `transaction_id` | integer | 4 B | No | Referencia a payment_transaction |

### `account_journal_account_journal_group_rel`

**Relación muchos a muchos entre «account.journal» y «account.journal.group»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_journal_group_id` | integer | 4 B | No | Referencia a account_journal_group |
| PK, FK | `account_journal_id` | integer | 4 B | No | Referencia a account_journal |

### `account_journal_account_reconcile_model_rel`

**Relación muchos a muchos entre «account.reconcile.model» y «account.journal»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_reconcile_model_id` | integer | 4 B | No | Referencia a account_reconcile_model |
| PK, FK | `account_journal_id` | integer | 4 B | No | Referencia a account_journal |

### `account_journal_group`

**Grupo de diario contable** · modelo `account.journal.group` · módulo `account` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — Define qué empresa puede seleccionar varios libros mayores en los filtros de reporte. Si no seleccionas ninguna estará disponible para to… |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Grupo de libros mayores |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_lock_exception`

**Excepción de bloqueo de la cuenta** · modelo `account.lock_exception` · módulo `account` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reason` | varchar | variable | Sí | Motivo |
|  | `lock_date_field` | varchar | variable | No | Campo de fecha de bloqueo — Campo técnico que identifica la fecha de bloqueo modificada |
|  | `lock_date` | date | 4 B | Sí | Fecha de bloqueo modificada — Campo técnico que proporciona la fecha en la que se cambió la fecha de bloqueo. |
|  | `company_lock_date` | date | 4 B | Sí | Fecha de bloqueo original — Campo técnico que proporciona la fecha de la fecha de bloqueo de la empresa al momento de crear la excepción. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `end_datetime` | timestamp | 8 B | Sí | Fecha de finalización |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_merge_wizard`

**Asistente de fusión de cuenta** · modelo `account.merge.wizard` · módulo `account` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `is_group_by_name` | boolean | 1 B | Sí | ¿Agrupar por nombre? — Seleccione esta casilla si desea agrupar cuentas por nombre para fusionarlas. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_merge_wizard_line`

**Línea del asistente de fusión de cuentas** · modelo `account.merge.wizard.line` · módulo `account` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `wizard_id` | integer | 4 B | No | Asistente → `account_merge_wizard` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `account_id` | integer | 4 B | Sí | Cuenta → `account_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `grouping_key` | varchar | variable | Sí | Clave de agrupación |
|  | `display_type` | varchar | variable | No | Mostrar como |
|  | `is_selected` | boolean | 1 B | Sí | Está seleccionado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_move__account_payment`

**Relación muchos a muchos entre «account.move» y «account.payment»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `invoice_id` | integer | 4 B | No | Referencia a account_move |
| PK, FK | `payment_id` | integer | 4 B | No | Referencia a account_payment |

### `account_move_account_move_send_batch_wizard_rel`

**Relación muchos a muchos entre «account.move.send.batch.wizard» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_move_send_batch_wizard_id` | integer | 4 B | No | Referencia a account_move_send_batch_wizard |
| PK, FK | `account_move_id` | integer | 4 B | No | Referencia a account_move |

### `account_move_account_resequence_wizard_rel`

**Relación muchos a muchos entre «account.resequence.wizard» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_resequence_wizard_id` | integer | 4 B | No | Referencia a account_resequence_wizard |
| PK, FK | `account_move_id` | integer | 4 B | No | Referencia a account_move |

### `account_move_line_account_tax_rel`

**Relación muchos a muchos entre «account.move.line» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_tax_id` | integer | 4 B | No | Referencia a account_tax |
| PK, FK | `account_move_line_id` | integer | 4 B | No | Referencia a account_move_line |

### `account_move_reversal`

**Reversión de movimiento de cuenta** · modelo `account.move.reversal` · módulo `account` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `journal_id` | integer | 4 B | No | Diario → `account_journal` — Si está vacío, utiliza el diario del asiento que se revertirá. |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reason` | varchar | variable | Sí | Motivo que aparece en la nota de crédito |
|  | `date` | date | 4 B | Sí | Fecha de reversión |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `l10n_latam_document_type_id` | integer | 4 B | Sí | Tipo de Documento → `l10n_latam_document_type` |
|  | `l10n_latam_document_number` | varchar | variable | Sí | Número de Documento |

### `account_move_reversal_move`

**Relación muchos a muchos entre «account.move.reversal» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `reversal_id` | integer | 4 B | No | Referencia a account_move_reversal |
| PK, FK | `move_id` | integer | 4 B | No | Referencia a account_move |

### `account_move_reversal_new_move`

**Relación muchos a muchos entre «account.move.reversal» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `reversal_id` | integer | 4 B | No | Referencia a account_move_reversal |
| PK, FK | `new_move_id` | integer | 4 B | No | Referencia a account_move |

### `account_move_send_batch_wizard`

**Asistente de envío de lotes y movimientos de cuenta** · modelo `account.move.send.batch.wizard` · módulo `account` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_move_send_wizard`

**Asistente de envío de movimientos de cuenta** · modelo `account.move.send.wizard` · módulo `account` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `template_id` | integer | 4 B | Sí | Plantilla de correo electrónico → `mail_template` |
| FK | `move_id` | integer | 4 B | No | Movimiento → `account_move` |
| FK | `pdf_report_id` | integer | 4 B | Sí | Reporte de la factura → `ir_act_report_xml` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lang` | varchar | variable | Sí | Idioma — Idioma de traducción opcional (código ISO) a seleccionar al enviar un correo. Si no lo defines, el sistema usará el idioma principal del… |
|  | `subject` | varchar | variable | Sí | Asunto |
|  | `model` | varchar | variable | Sí | Modelo de documento relacionado |
|  | `template_name` | varchar | variable | Sí | Nombre de la plantilla |
|  | `sending_method_checkboxes` | jsonb | variable | Sí | Casillas del método de envío |
|  | `extra_edi_checkboxes` | jsonb | variable | Sí | Casillas adicionales EDI |
|  | `mail_attachments_widget` | jsonb | variable | Sí | Widget de archivos adjuntos del correo |
|  | `body` | text | variable | Sí | Contenidos |
|  | `res_ids` | text | variable | Sí | IDs de los documentos relacionados |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_move_send_wizard_res_partner_rel`

**Relación muchos a muchos entre «account.move.send.wizard» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_move_send_wizard_id` | integer | 4 B | No | Referencia a account_move_send_wizard |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `account_move_validate_account_move_rel`

**Relación muchos a muchos entre «validate.account.move» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `validate_account_move_id` | integer | 4 B | No | Referencia a validate_account_move |
| PK, FK | `account_move_id` | integer | 4 B | No | Referencia a account_move |

### `account_partial_reconcile`

**Conciliación parcial** · modelo `account.partial.reconcile` · módulo `account` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `debit_move_id` | integer | 4 B | No | Movimiento de débito → `account_move_line` |
| FK | `credit_move_id` | integer | 4 B | No | Movimiento de crédito → `account_move_line` |
| FK | `full_reconcile_id` | integer | 4 B | Sí | Conciliación completa → `account_full_reconcile` |
| FK | `exchange_move_id` | integer | 4 B | Sí | Movimiento de intercambio → `account_move` |
| FK | `debit_currency_id` | integer | 4 B | Sí | Moneda del apunte contable de débito. → `res_currency` |
| FK | `credit_currency_id` | integer | 4 B | Sí | Moneda del apunte contable de crédito. → `res_currency` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `max_date` | date | 4 B | Sí | Fecha máxima de lineas asociadas |
|  | `draft_caba_move_vals` | jsonb | variable | Sí | Valores que crearon el asiento de ingreso en efectivo |
|  | `amount` | numeric | variable | Sí | Importe — Importe siempre positivo que el emparejamiento expresado en la moneda de la empresa está afectando. |
|  | `debit_amount_currency` | numeric | variable | Sí | Moneda del monto de débito — Importe siempre positivo que este emparejamiento está afectando expresado en moneda extranjera de la línea de débito. |
|  | `credit_amount_currency` | numeric | variable | Sí | Moneda del monto del crédito — Importe siempre positivo afectado por este emparejamiento expresado en moneda extranjera de la línea de crédito. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_payment`

**Pagos** · modelo `account.payment` · módulo `account` · 36 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `message_main_attachment_id` | integer | 4 B | Sí | Archivo adjunto principal → `ir_attachment` |
| FK | `move_id` | integer | 4 B | Sí | Asiento contable → `account_move` |
| FK | `journal_id` | integer | 4 B | No | Diario → `account_journal` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `partner_bank_id` | integer | 4 B | Sí | Cuenta bancaria receptora → `res_partner_bank` |
| FK | `paired_internal_transfer_payment_id` | integer | 4 B | Sí | Pago por transferencia interna emparejada → `account_payment` — Se crea un pago emparejado cuando se publica una transferencia interna. Se referencian de forma cruzada en este campo |
| FK | `payment_method_line_id` | integer | 4 B | Sí | Método de pago → `account_payment_method_line` — Manual: Paga o cobra con cualquier método externo a Odoo. Proveedores de pago: Cada proveedor de pago tiene su propio método de pago. Sol… |
| FK | `payment_method_id` | integer | 4 B | Sí | Método → `account_payment_method` |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` — La moneda del pago. |
| FK | `partner_id` | integer | 4 B | Sí | Cliente/proveedor → `res_partner` |
| FK | `outstanding_account_id` | integer | 4 B | Sí | Cuenta pendiente → `account_account` |
| FK | `destination_account_id` | integer | 4 B | Sí | Cuenta de destino → `account_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Número |
|  | `state` | varchar | variable | No | Estado |
|  | `payment_type` | varchar | variable | No | Tipo de pago |
|  | `partner_type` | varchar | variable | No | Tipo de contacto |
|  | `memo` | varchar | variable | Sí | Memo |
|  | `payment_reference` | varchar | variable | Sí | Referencia de pago — Referencia del documento que se utiliza para emitir este pago. Por ejemplo: número de cheque, nombre de archivo, etc. |
|  | `date` | date | 4 B | No | Fecha |
|  | `amount` | numeric | variable | Sí | Importe |
|  | `amount_company_currency_signed` | numeric | variable | Sí | Importe firmado en la moneda de la empresa |
|  | `is_reconciled` | boolean | 1 B | Sí | Conciliado |
|  | `is_matched` | boolean | 1 B | Sí | Corresponde con un estado de cuenta bancario |
|  | `is_sent` | boolean | 1 B | Sí | Enviado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `payment_transaction_id` | integer | 4 B | Sí | Transacción de pago → `payment_transaction` |
| FK | `payment_token_id` | integer | 4 B | Sí | Token de pago guardado → `payment_token` — Tenga en cuenta que solo están disponibles los tokens de los proveedores que permiten captar el importe. |
| FK | `source_payment_id` | integer | 4 B | Sí | Origen del pago → `account_payment` — El pago de origen de los pagos de reembolsos correspondientes |
| FK | `pos_payment_method_id` | integer | 4 B | Sí | Método de pago de PdV → `pos_payment_method` |
| FK | `force_outstanding_account_id` | integer | 4 B | Sí | Cuenta pendiente forzada → `account_account` |
| FK | `pos_session_id` | integer | 4 B | Sí | Sesión de PdV → `pos_session` |
| FK | `pos_order_id` | integer | 4 B | Sí | Orden del PdV → `pos_order` — La orden de punto de venta vinculada a este pago |

### `account_payment_account_bank_statement_line_rel`

**Relación muchos a muchos entre «account.bank.statement.line» y «account.payment»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_bank_statement_line_id` | integer | 4 B | No | Referencia a account_bank_statement_line |
| PK, FK | `account_payment_id` | integer | 4 B | No | Referencia a account_payment |

### `account_payment_method`

**Métodos de pago** · modelo `account.payment.method` · módulo `account` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | No | Código |
|  | `payment_type` | varchar | variable | No | Tipo de pago |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_payment_method_line`

**Métodos de pago** · modelo `account.payment.method.line` · módulo `account` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `payment_method_id` | integer | 4 B | No | Método de pago → `account_payment_method` |
| FK | `payment_account_id` | integer | 4 B | Sí | Cuenta del pago → `account_account` |
| FK | `journal_id` | integer | 4 B | Sí | Diario → `account_journal` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `payment_provider_id` | integer | 4 B | Sí | Proveedor de pago → `payment_provider` |

### `account_payment_register`

**Pagar** · modelo `account.payment.register` · módulo `account` · 29 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` — La moneda del pago. |
| FK | `journal_id` | integer | 4 B | Sí | Diario → `account_journal` |
| FK | `partner_bank_id` | integer | 4 B | Sí | Cuenta bancaria receptora → `res_partner_bank` |
| FK | `custom_user_currency_id` | integer | 4 B | Sí | Moneda de usuario personalizada → `res_currency` |
| FK | `source_currency_id` | integer | 4 B | Sí | Moneda de origen → `res_currency` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente/proveedor → `res_partner` |
| FK | `payment_method_line_id` | integer | 4 B | Sí | Método de pago → `account_payment_method_line` — Manual: Paga o cobra con cualquier método externo a Odoo. Proveedores de pago: Cada proveedor de pago tiene su propio método de pago. Sol… |
| FK | `writeoff_account_id` | integer | 4 B | Sí | Cuenta diferencial → `account_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `communication` | varchar | variable | Sí | Memo |
|  | `installments_mode` | varchar | variable | Sí | Installments Mode |
|  | `payment_type` | varchar | variable | Sí | Tipo de pago |
|  | `partner_type` | varchar | variable | Sí | Tipo de contacto |
|  | `payment_difference_handling` | varchar | variable | Sí | Manejo de diferencias de pago |
|  | `writeoff_label` | varchar | variable | Sí | Etiqueta de apunte contable — Cambiar la etiqueta de la contrapartida que mantendrá la diferencia de pago |
|  | `payment_date` | date | 4 B | No | Fecha de pago |
|  | `amount` | numeric | variable | Sí | Importe |
|  | `custom_user_amount` | numeric | variable | Sí | Importe de usuario personalizado |
|  | `source_amount` | numeric | variable | Sí | Importe por pagar (moneda de la empresa) |
|  | `source_amount_currency` | numeric | variable | Sí | Importe por pagar (moneda extranjera) |
|  | `group_payment` | boolean | 1 B | Sí | Agrupar pagos — Solo se creará un pago por contacto (banco), en lugar de uno por factura de proveedor. |
|  | `can_edit_wizard` | boolean | 1 B | Sí | Puede editar el asistente |
|  | `can_group_payments` | boolean | 1 B | Sí | Puede agrupar pagos |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `payment_token_id` | integer | 4 B | Sí | Token de pago guardado → `payment_token` — Tenga en cuenta que los tokens de los proveedores configurados para solo autorizar las transacciones (en lugar de capturar el importe) no… |

### `account_payment_register_move_line_rel`

**Relación muchos a muchos entre «account.payment.register» y «account.move.line»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `wizard_id` | integer | 4 B | No | Referencia a account_payment_register |
| PK, FK | `line_id` | integer | 4 B | No | Referencia a account_move_line |

### `account_payment_term`

**Términos de pago** · modelo `account.payment.term` · módulo `account` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `sequence` | integer | 4 B | No | Secuencia |
|  | `discount_days` | integer | 4 B | Sí | Días de descuento — Número de días antes de que expire la propuesta de pago anticipado |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `early_pay_discount_computation` | varchar | variable | Sí | Reducción de impuestos por diferencia de efectivo |
|  | `name` | jsonb | variable | No | Términos de pago |
|  | `note` | jsonb | variable | Sí | Descripción de la factura |
|  | `active` | boolean | 1 B | Sí | Activo — Si el campo activo se configura como falso, podrás ocultar los términos de pago sin eliminarlo. |
|  | `display_on_invoice` | boolean | 1 B | Sí | Mostrar fechas de las cuotas |
|  | `early_discount` | boolean | 1 B | Sí | Descuento por pago anticipado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `discount_percentage` | double precision | 8 B | Sí | Descuento % — Descuento por pago anticipado otorgado para este término de pago |

### `account_payment_term_line`

**Línea de términos de pago** · modelo `account.payment.term.line` · módulo `account` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `nb_days` | integer | 4 B | Sí | Días |
| FK | `payment_id` | integer | 4 B | No | Términos de pago → `account_payment_term` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `value` | varchar | variable | No | Valor — Seleccione aquí el tipo de valoración relacionada con esta línea de términos de pago. |
|  | `delay_type` | varchar | variable | No | Tipo de atraso |
|  | `days_next_month` | varchar | 2 | Sí | Días en el siguiente mes |
|  | `value_amount` | numeric | variable | Sí | Debido — Para el porcentaje, introduzca una razón entre 0-100. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_reconcile_model`

**Preajuste para crear asientos durante la conciliación de facturas y pagos** · modelo `account.reconcile.model` · módulo `account` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | No | Secuencia |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `next_activity_type_id` | integer | 4 B | Sí | Siguiente actividad → `mail_activity_type` |
| FK | `mapped_partner_id` | integer | 4 B | Sí | Contacto mapeado → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `trigger` | varchar | variable | No | Activar — Valide la línea de la declaración automáticamente (conciliación basada en su regla). |
|  | `match_amount` | varchar | variable | Sí | Importe — El modelo de conciliación solo se aplicará cuando el importe sea menor que, mayor que o entre las cantidades especificadas. |
|  | `match_label` | varchar | variable | Sí | Etiqueta — El modelo de conciliación solo se aplicará cuando la etiqueta de la línea del estado de cuenta, los detalles de la transacción o la nota… |
|  | `match_label_param` | varchar | variable | Sí | Parámetro de la etiqueta |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `can_be_proposed` | boolean | 1 B | Sí | Se puede proponer |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `match_amount_min` | double precision | 8 B | Sí | Parámetro de importe mínimo |
|  | `match_amount_max` | double precision | 8 B | Sí | Parámetro de importe máximo |

### `account_reconcile_model_line`

**Reglas para el modelo de conciliación** · modelo `account.reconcile.model.line` · módulo `account` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | Sí | Modelo → `account_reconcile_model` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `sequence` | integer | 4 B | No | Secuencia |
| FK | `account_id` | integer | 4 B | Sí | Cuenta → `account_account` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `amount_type` | varchar | variable | No | Tipo de importe |
|  | `amount_string` | varchar | variable | No | Importe — Valor para el importe de la línea de cancelación Porcentaje: El porcentaje del saldo, entre 0 y 100. Fijo: El valor fijo de la cancelació… |
|  | `analytic_distribution` | jsonb | variable | Sí | Distribución analítica |
|  | `label` | jsonb | variable | Sí | Etiqueta |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `amount` | double precision | 8 B | Sí | Importe flotante |

### `account_reconcile_model_line_account_tax_rel`

**Relación muchos a muchos entre «account.reconcile.model.line» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_tax_id` | integer | 4 B | No | Referencia a account_tax |
| PK, FK | `account_reconcile_model_line_id` | integer | 4 B | No | Referencia a account_reconcile_model_line |

### `account_reconcile_model_res_partner_rel`

**Relación muchos a muchos entre «account.reconcile.model» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_reconcile_model_id` | integer | 4 B | No | Referencia a account_reconcile_model |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `account_report`

**Reporte contable** · modelo `account.report` · módulo `account` · 36 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `root_report_id` | integer | 4 B | Sí | Reporte principal → `account_report` — El reporte del que este reporte es una variante. |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
|  | `load_more_limit` | integer | 4 B | Sí | Cargar más límite |
|  | `prefix_groups_threshold` | integer | 4 B | Sí | Límite de grupos de prefijos |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `chart_template` | varchar | variable | Sí | Plan de cuentas |
|  | `availability_condition` | varchar | variable | Sí | Disponibilidad |
|  | `integer_rounding` | varchar | variable | Sí | Redondeo de enteros |
|  | `default_opening_date_filter` | varchar | variable | Sí | Apertura predeterminada |
|  | `currency_translation` | varchar | variable | Sí | Ajuste de moneda |
|  | `filter_multi_company` | varchar | variable | Sí | Multiempresa |
|  | `filter_hide_0_lines` | varchar | variable | Sí | Oculta las líneas en 0 |
|  | `filter_hierarchy` | varchar | variable | Sí | Grupos de cuentas |
|  | `filter_account_type` | varchar | variable | Sí | Tipos de cuenta |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `use_sections` | boolean | 1 B | Sí | Reporte compuesto — Cree un reporte estructurado con varias secciones para facilitar la navegación y poder imprimirlo de manera simultánea. |
|  | `only_tax_exigible` | boolean | 1 B | Sí | Solo líneas de impuesto exigible |
|  | `search_bar` | boolean | 1 B | Sí | Barra de búsqueda |
|  | `allow_foreign_vat` | boolean | 1 B | Sí | Permitir número de identificación fiscal extranjero |
|  | `filter_date_range` | boolean | 1 B | Sí | Rango de fecha |
|  | `filter_show_draft` | boolean | 1 B | Sí | Borradores de asientos |
|  | `filter_unreconciled` | boolean | 1 B | Sí | Asientos sin conciliar |
|  | `filter_unfold_all` | boolean | 1 B | Sí | Desplegar todo |
|  | `filter_period_comparison` | boolean | 1 B | Sí | Comparación de periodo |
|  | `filter_growth_comparison` | boolean | 1 B | Sí | Comparación de crecimiento |
|  | `filter_journals` | boolean | 1 B | Sí | Diarios |
|  | `filter_analytic` | boolean | 1 B | Sí | Filtro analítico |
|  | `filter_partner` | boolean | 1 B | Sí | Contactos |
|  | `filter_aml_ir_filters` | boolean | 1 B | Sí | Filtros favoritos — Si se activa, será posible seleccionar los filtros definidos por el usuario en los apuntes contables en este reporte |
|  | `filter_budgets` | boolean | 1 B | Sí | Presupuestos |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_report_column`

**Columna de reporte contable** · modelo `account.report.column` · módulo `account` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `report_id` | integer | 4 B | Sí | Reporte → `account_report` |
| FK | `custom_audit_action_id` | integer | 4 B | Sí | Acción personalizada de auditar → `ir_act_window` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `expression_label` | varchar | variable | No | Etiqueta de expresión |
|  | `figure_type` | varchar | variable | No | Tipo de cifra |
|  | `name` | jsonb | variable | No | Nombre |
|  | `sortable` | boolean | 1 B | Sí | Clasificable |
|  | `blank_if_zero` | boolean | 1 B | Sí | Dejar en blanco si es cero — Cuando se seleccione, los valores 0 no se mostrarán en esta columna. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_report_expression`

**Expresión de reporte contable** · modelo `account.report.expression` · módulo `account` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `report_line_id` | integer | 4 B | No | Línea de reporte → `account_report_line` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `label` | varchar | variable | No | Etiqueta |
|  | `engine` | varchar | variable | No | Motor de cálculo |
|  | `formula` | varchar | variable | No | Fórmula |
|  | `subformula` | varchar | variable | Sí | Subfórmula |
|  | `date_scope` | varchar | variable | No | Alcance de la fecha |
|  | `figure_type` | varchar | variable | Sí | Tipo de cifra |
|  | `carryover_target` | varchar | variable | Sí | Traspasar a — La fórmula en el formulario line_code.expression_label. Permite establecer el objetivo del traspaso para esta expresión (en una expresión… |
|  | `green_on_positive` | boolean | 1 B | Sí | El crecimiento es positivo |
|  | `blank_if_zero` | boolean | 1 B | Sí | Dejar en blanco si es cero — Cuando se selecciona, los valores 0 no se aparecerán cuando se muestre el valor de esta expresión. |
|  | `auditable` | boolean | 1 B | Sí | Auditable |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_report_external_value`

**Valor externo de reporte contable** · modelo `account.report.external.value` · módulo `account` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `target_report_expression_id` | integer | 4 B | No | Expresión objetivo → `account_report_expression` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `carryover_origin_report_line_id` | integer | 4 B | Sí | Línea origen → `account_report_line` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `text_value` | varchar | variable | Sí | Valor del texto |
|  | `carryover_origin_expression_label` | varchar | variable | Sí | Etiqueta de expresión de origen |
|  | `date` | date | 4 B | No | Fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `value` | double precision | 8 B | Sí | Valor númerico |

### `account_report_line`

**Línea del reporte contable** · modelo `account.report.line` · módulo `account` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `report_id` | integer | 4 B | No | Reporte principal → `account_report` |
|  | `hierarchy_level` | integer | 4 B | No | Nivel |
| FK | `parent_id` | integer | 4 B | Sí | Línea principal → `account_report_line` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
|  | `action_id` | integer | 4 B | Sí | Acción — Establecer este campo convertirá la línea en un enlace y ejecutará la acción cuando se haga clic en él. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `groupby` | varchar | variable | Sí | Agrupar por — Lista de campos de account.move.line (apunte contable) separados por comas. Cuando la configures, esta línea generará sublíneas agrupadas… |
|  | `user_groupby` | varchar | variable | Sí | Agrupar usuario por — Lista de campos de account.move.line (apunte contable) separados por comas. Cuando la configures, esta línea generará sublíneas agrupadas… |
|  | `code` | varchar | variable | Sí | Código — Identificador único para esta línea. |
|  | `horizontal_split_side` | varchar | variable | Sí | División lateral horizontal |
|  | `name` | jsonb | variable | No | Nombre |
|  | `foldable` | boolean | 1 B | Sí | Plegable — Siempre desplegamos las líneas que podemos de forma automática. Si esto se selecciona, la línea no se desplegará en automático y se mostr… |
|  | `print_on_new_page` | boolean | 1 B | Sí | Imprimir en una nueva página — Cuando se selecciona, esta línea y todo lo que siga se imprimirá en una nueva página. |
|  | `hide_if_zero` | boolean | 1 B | Sí | Ocultar si es cero — Esta línea y sus líneas dependientes se ocultarán cuando todas sus columnas sean 0. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_report_section_rel`

**Relación muchos a muchos entre «account.report» y «account.report»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `main_report_id` | integer | 4 B | No | Referencia a account_report |
| PK, FK | `sub_report_id` | integer | 4 B | No | Referencia a account_report |

### `account_resequence_wizard`

**Rehaga la secuencia de los asientos contables.** · modelo `account.resequence.wizard` · módulo `account` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `first_name` | varchar | variable | No | Primera secuencia nueva |
|  | `ordering` | varchar | variable | No | Orden |
|  | `first_date` | date | 4 B | Sí | Primera fecha — Fecha (inclusiva) a la cual se vuelven a secuenciar los números. |
|  | `end_date` | date | 4 B | Sí | Fecha de finalización — Fecha (inclusiva) a la que se vuelven a secuenciar los números. Si no se establece, se vuelven a secuenciar todos los asientos contables… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_secure_entries_wizard`

**Proteger asientos contables** · modelo `account.secure.entries.wizard` · módulo `account` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `hash_date` | date | 4 B | No | Hashear todos los asientos — La fecha seleccionada |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_setup_bank_manual_config`

**Configuración manual de datos bancarios** · modelo `account.setup.bank.manual.config` · módulo `account` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `res_partner_bank_id` | integer | 4 B | No | Banco del contacto → `res_partner_bank` |
|  | `num_journals_without_account_bank` | integer | 4 B | Sí | Número de diarios sin cuenta bancaria |
|  | `num_journals_without_account_credit` | integer | 4 B | Sí | Número de diarios sin cuenta de crédito |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `new_journal_name` | varchar | variable | No | Nuevo nombre de diario — Se usará para nombrar el diario relacionado con esta cuenta bancaria. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_tax`

**Impuesto** · modelo `account.tax` · módulo `account` · 30 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
|  | `sequence` | integer | 4 B | No | Secuencia — El campo de secuencia se utiliza para definir el orden en que se aplican los apuntes de impuestos. |
| FK | `tax_group_id` | integer | 4 B | No | Grupo de impuestos → `account_tax_group` |
| FK | `cash_basis_transition_account_id` | integer | 4 B | Sí | Cuenta transitoria de base de efectivo → `account_account` — Cuenta que se utiliza para la transición del importe del impuesto para impuestos de base de efectivo. Contendrá el importe del impuesto m… |
| FK | `country_id` | integer | 4 B | No | País → `res_country` — El país al que aplica este impuesto. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `type_tax_use` | varchar | variable | No | Tipo de impuesto — Determina en dónde se puede seleccionar un impuesto. Nota: 'Ninguno' significa que un impuesto no se puede usar por sí mismo, pero sí se… |
|  | `tax_scope` | varchar | variable | Sí | Ámbito del impuesto |
|  | `amount_type` | varchar | variable | No | Cálculo de impuestos — - Grupo de impuestos: El impuesto es un conjunto de subimpuestos. - Fijo: El importe del impuesto se mantiene igual sin importar el preci… |
|  | `price_include_override` | varchar | variable | Sí | Incluido en el precio — Sobrescribe la configuración predeterminada de la empresa si el precio que utiliza en el producto y en las facturas incluye este impuesto. |
|  | `tax_exigibility` | varchar | variable | Sí | Exigencia de impuestos — Con base en la factura: el impuesto vence tan pronto como la factura se valide. Con base en el pago: el impuesto vence tan pronto como se… |
|  | `name` | jsonb | variable | No | Nombre del impuesto |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `invoice_label` | jsonb | variable | Sí | Etiqueta en facturas |
|  | `invoice_legal_notes` | jsonb | variable | Sí | Notas legales — Menciones legales que se tienen que imprimir en las facturas. |
|  | `amount` | numeric | variable | No | Importe |
|  | `is_domestic` | boolean | 1 B | Sí | Es local |
|  | `active` | boolean | 1 B | Sí | Activo — Establezca el activo como false para ocultar el impuesto sin eliminarlo. |
|  | `include_base_amount` | boolean | 1 B | Sí | Afecta la base de los impuestos subsecuentes — Si se establece, los impuestos con una secuencia mayor que esta serán afectados por ello, en caso de que lo acepten. |
|  | `is_base_affected` | boolean | 1 B | Sí | Base afectada por impuestos previos — Si se establece, los impuestos con una secuencia menor que esta serán afectados por ello, en caso de que traten de hacerlo. |
|  | `analytic` | boolean | 1 B | Sí | Incluir en el costo analítico — Si se establece, el importe calculado por este impuesto se asignará a la misma cuenta analítica de la línea de factura (si la hay) |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `ubl_cii_tax_category_code` | varchar | variable | Sí | Código de categoría del impuesto — El código de la categoría del IVA que se usa para fines de facturación electrónica. |
|  | `ubl_cii_tax_exemption_reason_code` | varchar | variable | Sí | Código del motivo de la exención fiscal — El motivo por el que la cantidad está exenta de IVA o por qué no se está cobrando el IVA, se usa para fines de facturación electrónica. |
|  | `l10n_pe_edi_tax_code` | varchar | variable | Sí | Código — Perú: Código tributario de la SUNAT |
|  | `l10n_pe_edi_unece_category` | varchar | variable | Sí | Código UNECE — Revisa la norma UN/ECE 5305 de la Comisión Económica de las Naciones Unidas para Europa para obtener más información: http://www.unece.or… |
|  | `l10n_pe_edi_isc_type` | varchar | variable | Sí | Tipo de Impuesto Selectivo al Consumo — Utilizado en el Impuesto Selectivo al Consumo para indicar el tipo de cálculo del mismo. |

### `account_tax_alternatives`

**Relación muchos a muchos entre «account.tax» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `dest_tax_id` | integer | 4 B | No | Referencia a account_tax |
| PK, FK | `src_tax_id` | integer | 4 B | No | Referencia a account_tax |

### `account_tax_filiation_rel`

**Relación muchos a muchos entre «account.tax» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `parent_tax` | integer | 4 B | No | Referencia a account_tax |
| PK, FK | `child_tax` | integer | 4 B | No | Referencia a account_tax |

### `account_tax_group`

**Grupo de impuestos** · modelo `account.tax.group` · módulo `account` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `tax_payable_account_id` | integer | 4 B | Sí | Cuenta por pagar de impuestos → `account_account` — Cuenta corriente de impuestos que se utiliza como contrapartida del asiento de cierre de impuestos cuando está a favor de las autoridades. |
| FK | `tax_receivable_account_id` | integer | 4 B | Sí | Cuenta por cobrar de impuestos → `account_account` — Cuenta corriente de impuestos que se utiliza como contrapartida del asiento de cierre de impuestos cuando está a favor de la empresa. |
| FK | `advance_tax_payment_account_id` | integer | 4 B | Sí | Cuenta avanzada de impuestos → `account_account` — Los anticipos registrados en esta cuenta se considerarán en el asiento de cierre fiscal. |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` — El país al que aplica este grupo de impuestos. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `pos_receipt_label` | varchar | variable | Sí | Imprimir etiqueta |
|  | `name` | jsonb | variable | No | Nombre |
|  | `preceding_subtotal` | jsonb | variable | Sí | Subtotal precedente — Si se establece, este valor se utilizará como la etiqueta de un subtotal sin incluir este grupo de impuestos antes de mostrarlo. Si no se… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_tax_pos_order_line_rel`

**Relación muchos a muchos entre «account.tax» y «pos.order.line»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_tax_id` | integer | 4 B | No | Referencia a account_tax |
| PK, FK | `pos_order_line_id` | integer | 4 B | No | Referencia a pos_order_line |

### `account_tax_purchase_order_line_rel`

**Relación muchos a muchos entre «account.tax» y «purchase.order.line»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_tax_id` | integer | 4 B | No | Referencia a account_tax |
| PK, FK | `purchase_order_line_id` | integer | 4 B | No | Referencia a purchase_order_line |

### `account_tax_repartition_line`

**Línea de partición de impuestos** · modelo `account.tax.repartition.line` · módulo `account` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | Sí | Cuenta → `account_account` — Cuenta en la que se publicará el importe del impuesto. |
| FK | `tax_id` | integer | 4 B | Sí | Impuesto → `account_tax` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — La empresa a la que pertenece esta línea de distribución. |
|  | `sequence` | integer | 4 B | Sí | Secuencia — El orden en que se muestran y coinciden las líneas de distribución. Para que los reembolsos funcionen correctamente, las líneas de repart… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `repartition_type` | varchar | variable | No | Con base en — Base sobre la que se aplicará el factor. |
|  | `document_type` | varchar | variable | No | Relacionado a |
|  | `factor_percent` | numeric | variable | No | % — Factor por aplicar en las líneas de movimiento de cuenta generadas desde esta línea de distribución, en porcentajes |
|  | `use_in_tax_closing` | boolean | 1 B | Sí | Asiento de cierre de impuestos |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `adjusting_entries__account_move`

**Relación muchos a muchos entre «account.move» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `move_id` | integer | 4 B | No | Referencia a account_move |
| PK, FK | `adjusting_entry_move_id` | integer | 4 B | No | Referencia a account_move |

### `refunded_invoices`

**Relación muchos a muchos entre «account.move» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `refund_account_move` | integer | 4 B | No | Referencia a account_move |
| PK, FK | `original_account_move` | integer | 4 B | No | Referencia a account_move |

### `sale_order_line_invoice_rel`

**Relación muchos a muchos entre «account.move.line» y «sale.order.line»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `invoice_line_id` | integer | 4 B | No | Referencia a account_move_line |
| PK, FK | `order_line_id` | integer | 4 B | No | Referencia a sale_order_line |

### `validate_account_move`

**Validar movimiento contable** · modelo `validate.account.move` · módulo `account` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `force_post` | boolean | 1 B | Sí | Forzar — Los asientos en el futuro están configurados para que se publiquen automáticamente de forma predeterminada. Selecciona esta casilla para… |
|  | `force_hash` | boolean | 1 B | Sí | Forzar hash |
|  | `ignore_abnormal_date` | boolean | 1 B | Sí | Ignorar fecha anormal |
|  | `ignore_abnormal_amount` | boolean | 1 B | Sí | Ignorar importe anormal |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `wip_move_production_rel`

**Relación muchos a muchos entre «account.move» y «mrp.production»** · tabla intermedia, sin modelo propio · módulo `account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `production_id` | integer | 4 B | No | Referencia a mrp_production |
| PK, FK | `move_id` | integer | 4 B | No | Referencia a account_move |

## Módulo `account_debit_note`

### `account_debit_note`

**Asistente para agregar nota de débito** · modelo `account.debit.note` · módulo `account_debit_note` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `journal_id` | integer | 4 B | Sí | Utilizar diario específico → `account_journal` — Si está vacío, se utiliza el asiento contable del diario para realizar el cargo. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reason` | varchar | variable | Sí | Motivo |
|  | `date` | date | 4 B | No | Fecha de nota de débito |
|  | `copy_lines` | boolean | 1 B | Sí | Copiar líneas — Puede ser útil copiarlas en caso de que haga correcciones para cada línea. No las copiaremos para las notas de débito desde las notas de… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_move_debit_move`

**Relación muchos a muchos entre «account.debit.note» y «account.move»** · tabla intermedia, sin modelo propio · módulo `account_debit_note` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `debit_id` | integer | 4 B | No | Referencia a account_debit_note |
| PK, FK | `move_id` | integer | 4 B | No | Referencia a account_move |

## Módulo `account_payment`

### `payment_refund_wizard`

**Asistente de reembolso de pago** · modelo `payment.refund.wizard` · módulo `account_payment` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `payment_id` | integer | 4 B | Sí | Pago → `account_payment` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `amount_to_refund` | numeric | variable | Sí | Reembolsar importe |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `analytic`

### `account_analytic_account`

**Cuenta analítica** · modelo `account.analytic.account` · módulo `analytic` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `plan_id` | integer | 4 B | No | Plan → `account_analytic_plan` |
| FK | `root_plan_id` | integer | 4 B | Sí | Plan raíz → `account_analytic_plan` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | Sí | Referencia |
|  | `name` | jsonb | variable | No | Cuenta analítica |
|  | `active` | boolean | 1 B | Sí | Activo — Desactivar cuenta. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `account_analytic_account_mrp_bom_rel`

**Relación muchos a muchos entre «account.analytic.account» y «mrp.bom»** · tabla intermedia, sin modelo propio · módulo `analytic` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_analytic_account_id` | integer | 4 B | No | Referencia a account_analytic_account |
| PK, FK | `mrp_bom_id` | integer | 4 B | No | Referencia a mrp_bom |

### `account_analytic_account_mrp_production_rel`

**Relación muchos a muchos entre «account.analytic.account» y «mrp.production»** · tabla intermedia, sin modelo propio · módulo `analytic` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_analytic_account_id` | integer | 4 B | No | Referencia a account_analytic_account |
| PK, FK | `mrp_production_id` | integer | 4 B | No | Referencia a mrp_production |

### `account_analytic_account_mrp_workcenter_rel`

**Relación muchos a muchos entre «account.analytic.account» y «mrp.workcenter»** · tabla intermedia, sin modelo propio · módulo `analytic` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `account_analytic_account_id` | integer | 4 B | No | Referencia a account_analytic_account |
| PK, FK | `mrp_workcenter_id` | integer | 4 B | No | Referencia a mrp_workcenter |

### `account_analytic_applicability`

**Aplicabilidades del plan analítico** · modelo `account.analytic.applicability` · módulo `analytic` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `analytic_plan_id` | integer | 4 B | Sí | Plan analítico → `account_analytic_plan` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `business_domain` | varchar | variable | No | Dominio |
|  | `applicability` | varchar | variable | No | Aplicabilidad |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `product_categ_id` | integer | 4 B | Sí | Categoría del producto → `product_category` |
|  | `account_prefix` | varchar | variable | Sí | Prefijos de las cuentas financieras — Prefijo que define a qué cuentas de la contabilidad financiera se debe aplicar esta aplicabilidad |

### `account_analytic_distribution_model`

**Modelo de distribución analítica** · modelo `account.analytic.distribution.model` · módulo `analytic` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` — Seleccionar un contacto para el que se utilizará la distribución analítica (por ejemplo, crear una nueva factura de cliente u orden de ve… |
| FK | `partner_category_id` | integer | 4 B | Sí | Categoría del contacto → `res_partner_category` — Seleccionar una categoría de contacto para la que se utilizará la distribución analítica (por ejemplo, crear una nueva factura de cliente… |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — Seleccione la empresa para la que se utilizará la distribución analítica (por ejemplo, al crear una nueva factura de cliente o una orden… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `analytic_distribution` | jsonb | variable | Sí | Distribución analítica |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` — Seleccione un producto para el que se utilizará la distribución analítica (por ejemplo, al crear una nueva factura de cliente o una orden… |
| FK | `product_categ_id` | integer | 4 B | Sí | Categoría del producto → `product_category` — Seleccione una categoría de producto que utilizará la cuenta analítica que se especifica en el análisis predeterminado (por ejemplo, al c… |
|  | `account_prefix` | varchar | variable | Sí | Prefijo de cuentas — Esta distribución analítica se aplicará a todas las cuentas financieras que compartan el prefijo especificado. |

### `account_analytic_line`

**Línea analítica** · modelo `account.analytic.line` · módulo `analytic` · 23 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | Sí | Project Account → `account_analytic_account` |
| FK | `product_uom_id` | integer | 4 B | Sí | Unidad → `uom_uom` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Descripción |
|  | `category` | varchar | variable | Sí | Categoría |
|  | `date` | date | 4 B | No | Fecha |
|  | `amount` | numeric | variable | No | Importe |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `unit_amount` | double precision | 8 B | Sí | Cantidad |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `general_account_id` | integer | 4 B | Sí | Cuenta financiera → `account_account` |
| FK | `journal_id` | integer | 4 B | Sí | Diario financiero → `account_journal` |
| FK | `move_line_id` | integer | 4 B | Sí | Apunte contable → `account_move_line` |
|  | `code` | varchar | 8 | Sí | Código |
|  | `ref` | varchar | variable | Sí | Ref. |
| FK | `so_line` | integer | 4 B | Sí | Artículo de la orden de venta → `sale_order_line` |

### `account_analytic_plan`

**Planes analíticos** · modelo `account.analytic.plan` · módulo `analytic` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_id` | integer | 4 B | Sí | Principal → `account_analytic_plan` |
|  | `color` | integer | 4 B | Sí | Color |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `complete_name` | varchar | variable | Sí | Nombre completo |
|  | `name` | jsonb | variable | No | Nombre |
|  | `default_applicability` | jsonb | variable | Sí | Aplicabilidad predeterminada |
|  | `description` | text | variable | Sí | Descripción |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `auditlog`

### `auditlog_autovacuum`

**Auditlog - Borrar registros antiguos** · modelo `auditlog.autovacuum` · módulo `auditlog` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Actualizado última vez por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado en |
|  | `write_date` | timestamp | 8 B | Sí | Ultima Actualización |

### `auditlog_http_request`

**Auditlog - Reigstro de peticiones HTTP** · modelo `auditlog.http.request` · módulo `auditlog` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
| FK | `http_session_id` | integer | 4 B | Sí | Sesión → `auditlog_http_session` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Actualizado última vez por → `res_users` |
|  | `display_name` | varchar | variable | Sí | Nombre |
|  | `name` | varchar | variable | Sí | Ruta |
|  | `root_url` | varchar | variable | Sí | URL raíz |
|  | `user_context` | varchar | variable | Sí | Contexto |
|  | `create_date` | timestamp | 8 B | Sí | Creado en |
|  | `write_date` | timestamp | 8 B | Sí | Ultima Actualización |

### `auditlog_http_session`

**Auditlog - Registro de sesión de usuario HTTP** · modelo `auditlog.http.session` · módulo `auditlog` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Actualizado última vez por → `res_users` |
|  | `display_name` | varchar | variable | Sí | Nombre |
|  | `name` | varchar | variable | Sí | ID de sesión |
|  | `create_date` | timestamp | 8 B | Sí | Creado en |
|  | `write_date` | timestamp | 8 B | Sí | Ultima Actualización |

### `auditlog_log`

**Auditlog - Registro** · modelo `auditlog.log` · módulo `auditlog` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | Sí | Modelo → `ir_model` |
|  | `res_id` | integer | 4 B | Sí | ID del recurso |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
| FK | `http_session_id` | integer | 4 B | Sí | Sesión → `auditlog_http_session` |
| FK | `http_request_id` | integer | 4 B | Sí | Petición HTTP → `auditlog_http_request` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Actualizado última vez por → `res_users` |
|  | `name` | varchar | 64 | Sí | Nombre del recurso |
|  | `model_name` | varchar | variable | Sí | Nombre del modelo |
|  | `model_model` | varchar | variable | Sí | Nombre técnico del modelo |
|  | `res_ids` | varchar | variable | Sí | Resource IDs |
|  | `method` | varchar | 64 | Sí | Método |
|  | `log_type` | varchar | variable | Sí | Tipo |
|  | `create_date` | timestamp | 8 B | Sí | Creado en |
|  | `write_date` | timestamp | 8 B | Sí | Ultima Actualización |

### `auditlog_log_line`

**Auditlog - Detalles de registro (campos actualizados)** · modelo `auditlog.log.line` · módulo `auditlog` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `field_id` | integer | 4 B | Sí | Campo → `ir_model_fields` |
| FK | `log_id` | integer | 4 B | Sí | Registro → `auditlog_log` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Actualizado última vez por → `res_users` |
|  | `field_name` | varchar | variable | Sí | Nombre técnico |
|  | `field_description` | varchar | variable | Sí | Descripción |
|  | `old_value` | text | variable | Sí | Valor anterior |
|  | `new_value` | text | variable | Sí | Valor nuevo |
|  | `old_value_text` | text | variable | Sí | Texto del valor anterior |
|  | `new_value_text` | text | variable | Sí | Texto del valor nuevo |
|  | `create_date` | timestamp | 8 B | Sí | Creado en |
|  | `write_date` | timestamp | 8 B | Sí | Ultima Actualización |

### `auditlog_rule_ir_model_fields_rel`

**Relación muchos a muchos entre «auditlog.rule» y «ir.model.fields»** · tabla intermedia, sin modelo propio · módulo `auditlog` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `auditlog_rule_id` | integer | 4 B | No | Referencia a auditlog_rule |
| PK, FK | `ir_model_fields_id` | integer | 4 B | No | Referencia a ir_model_fields |

### `auditlog_rule_res_users_rel`

**Relación muchos a muchos entre «auditlog.rule» y «res.users»** · tabla intermedia, sin modelo propio · módulo `auditlog` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `auditlog_rule_id` | integer | 4 B | No | Referencia a auditlog_rule |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `audittail_rules_users`

**Relación muchos a muchos entre «auditlog.rule» y «res.users»** · tabla intermedia, sin modelo propio · módulo `auditlog` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `user_id` | integer | 4 B | No | Referencia a auditlog_rule |
| PK, FK | `rule_id` | integer | 4 B | No | Referencia a res_users |

## Módulo `auth_passkey`

### `auth_passkey_key`

**Llave de acceso** · modelo `auth.passkey.key` · módulo `auth_passkey` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sign_count` | integer | 4 B | Sí | Número de sesiones iniciadas |
| FK | `create_uid` | integer | 4 B | Sí | Crear UID → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `credential_identifier` | varchar | variable | No | Identificador de credenciales |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `public_key` | varchar | variable | Sí | Clave pública |

### `auth_passkey_key_create`

**Crear una llave de acceso** · modelo `auth.passkey.key.create` · módulo `auth_passkey` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `auth_totp`

### `auth_totp_device`

**Dispositivo de autenticación** · modelo `auth_totp.device` · módulo `auth_totp` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `name` | varchar | variable | No | Descripción |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
|  | `scope` | varchar | variable | Sí | Alcance |
|  | `expiration_date` | timestamp | 8 B | Sí | Fecha de vencimiento |
|  | `index` | varchar | 8 | Sí | — |
|  | `key` | varchar | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |

### `auth_totp_rate_limit_log`

**Cantidad límite de registros de TOTP** · modelo `auth.totp.rate.limit.log` · módulo `auth_totp` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `ip` | varchar | variable | Sí | IP |
|  | `limit_type` | varchar | variable | Sí | Tipo de límite |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `auth_totp_wizard`

**Asistente de la configuración de la autenticación de dos factores** · modelo `auth_totp.wizard` · módulo `auth_totp` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `secret` | varchar | variable | No | Secreto |
|  | `url` | varchar | variable | Sí | URL |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `qrcode` | bytea | variable | Sí | Código QR |

## Módulo `barcodes`

### `barcode_nomenclature`

**Nomenclatura del código de barras** · modelo `barcode.nomenclature` · módulo `barcodes` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nomenclatura del código de barras — Un identificador interno para la nomenclatura del código de barras |
|  | `upc_ean_conv` | varchar | variable | No | Conversión UPC/EAN — Los códigos UPC se pueden convertir a EAN al agregar un cero al inicio. Esta opción define si un código de barras UPC/EAN debe convertirs… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `gs1_separator_fnc1` | varchar | variable | Sí | Separador FNC1 — Delimitador alternativo en la expresión regular para el FNC1. El separador no debe coincidir con el inicio o final del patrón de ninguna… |
|  | `is_gs1_nomenclature` | boolean | 1 B | Sí | Es nomenclatura GS1 — Esta nomenclatura usa la especificación GS1 y solo acepta las reglas de codificación GS1-128. |

### `barcode_rule`

**Regla del código de barras** · modelo `barcode.rule` · módulo `barcodes` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `barcode_nomenclature_id` | integer | 4 B | Sí | Nomenclatura del código de barras → `barcode_nomenclature` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Se utiliza para ordenar reglas de modo que las que tienen una secuencia menor se evalúen primero |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de la regla — Un identificador interno para esta regla de nomenclatura del código de barras |
|  | `encoding` | varchar | variable | No | Codificación — Esta regla solo aplicará si el código de barras tiene la codificación especificada |
|  | `type` | varchar | variable | No | Tipo |
|  | `pattern` | varchar | variable | No | Patrón del código de barras — El patrón de concordancia para el código de barras |
|  | `alias` | varchar | variable | No | Alias — El patrón coincidente se asignará a este código de barras. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `associated_uom_id` | integer | 4 B | Sí | UdM asociada → `uom_uom` |
|  | `gs1_content_type` | varchar | variable | Sí | Tipo de contenido GS1 — El tipo de contenido GS1 define el tipo de datos que procesará la regla para el código de barras: * Fecha: El código de barras se convert… |
|  | `gs1_decimal_usage` | boolean | 1 B | Sí | Decimal — Si es "true", use el último dígito de AI para determinar dónde está el primer decimal |

## Módulo `base`

### `account_fiscal_position_res_config_settings_rel`

**Relación muchos a muchos entre «res.config.settings» y «account.fiscal.position»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `res_config_settings_id` | integer | 4 B | No | Referencia a res_config_settings |
| PK, FK | `account_fiscal_position_id` | integer | 4 B | No | Referencia a account_fiscal_position |

### `base_enable_profiling_wizard`

**Habilitar análisis de rendimiento por cierto tiempo** · modelo `base.enable.profiling.wizard` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `duration` | varchar | variable | Sí | Habilitar análisis de rendimiento para |
|  | `expiration` | timestamp | 8 B | Sí | Habilitar análisis de rendimiento hasta |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `base_language_export`

**Exportar idioma** · modelo `base.language.export` · módulo `base` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | Sí | Modelo a exportar → `ir_model` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre del archivo |
|  | `lang` | varchar | variable | No | Idioma |
|  | `format` | varchar | variable | No | Formato del archivo |
|  | `export_type` | varchar | variable | No | Tipo de exportación |
|  | `domain` | varchar | variable | Sí | Dominio del modelo |
|  | `state` | varchar | variable | Sí | Estado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `data` | bytea | variable | Sí | Archivo |

### `base_language_import`

**Importar idioma** · modelo `base.language.import` · módulo `base` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre del idioma |
|  | `code` | varchar | variable | No | Código ISO — Código ISO de idioma y país, por ejemplo, es_ES |
|  | `filename` | varchar | variable | No | Nombre del archivo |
|  | `overwrite` | boolean | 1 B | Sí | Sobrescribir términos existentes — Si habilita esta opción, las traducciones existentes (incluidas las personalizadas) serán sobrescritas y reemplazadas por las traduccione… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `data` | bytea | variable | No | Archivo |

### `base_language_install`

**Instalar idioma** · modelo `base.language.install` · módulo `base` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `overwrite` | boolean | 1 B | Sí | Sobrescribir términos existentes — Si selecciona esta casilla, las traducciones personalizadas serán sobrescritas y reemplazadas por las oficiales. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `base_module_uninstall`

**Desinstalar módulo** · modelo `base.module.uninstall` · módulo `base` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `show_all` | boolean | 1 B | Sí | Mostrar todo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `base_module_uninstall_ir_module_module_rel`

**Relación muchos a muchos entre «base.module.uninstall» y «ir.module.module»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `base_module_uninstall_id` | integer | 4 B | No | Referencia a base_module_uninstall |
| PK, FK | `ir_module_module_id` | integer | 4 B | No | Referencia a ir_module_module |

### `base_module_update`

**Actualizar módulo** · modelo `base.module.update` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `updated` | integer | 4 B | Sí | Número de módulos actualizados |
|  | `added` | integer | 4 B | Sí | Número de módulos agregados |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `state` | varchar | variable | Sí | Estado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `base_module_upgrade`

**Actualizar módulo** · modelo `base.module.upgrade` · módulo `base` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `module_info` | text | variable | Sí | Aplicaciones a actualizar |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `base_partner_merge_automatic_wizard`

**Asistente de fusión de contactos** · modelo `base.partner.merge.automatic.wizard` · módulo `base` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `number_group` | integer | 4 B | Sí | Grupo de contactos |
| FK | `current_line_id` | integer | 4 B | Sí | Línea actual → `base_partner_merge_line` |
| FK | `dst_partner_id` | integer | 4 B | Sí | Contacto de destino → `res_partner` |
|  | `maximum_group` | integer | 4 B | Sí | Máximo de grupos de contactos |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `state` | varchar | variable | No | Estado |
|  | `group_by_email` | boolean | 1 B | Sí | Correo electrónico |
|  | `group_by_name` | boolean | 1 B | Sí | Nombre |
|  | `group_by_is_company` | boolean | 1 B | Sí | Es una empresa |
|  | `group_by_vat` | boolean | 1 B | Sí | Número de identificación fiscal |
|  | `group_by_parent_id` | boolean | 1 B | Sí | Empresa matriz |
|  | `exclude_contact` | boolean | 1 B | Sí | Un usuario asociado al contacto |
|  | `exclude_journal_item` | boolean | 1 B | Sí | Asientos contables relacionados al contacto |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `base_partner_merge_automatic_wizard_res_partner_rel`

**Relación muchos a muchos entre «base.partner.merge.automatic.wizard» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `base_partner_merge_automatic_wizard_id` | integer | 4 B | No | Referencia a base_partner_merge_automatic_wizard |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `base_partner_merge_line`

**Fusionar línea de contacto** · modelo `base.partner.merge.line` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `wizard_id` | integer | 4 B | Sí | Asistente → `base_partner_merge_automatic_wizard` |
|  | `min_id` | integer | 4 B | Sí | MinID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `aggr_ids` | varchar | variable | No | ID |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `change_password_own`

**Usuario, asistente de cambio de contraseña propia** · modelo `change.password.own` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `new_password` | varchar | variable | Sí | Contraseña nueva |
|  | `confirm_password` | varchar | variable | Sí | Contraseña nueva (confirmación) |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `change_password_user`

**Usuario, asistente de cambio de contraseña** · modelo `change.password.user` · módulo `base` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `wizard_id` | integer | 4 B | No | Asistente → `change_password_wizard` |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `user_login` | varchar | variable | Sí | Inicio de sesión del usuario |
|  | `new_passwd` | varchar | variable | Sí | Contraseña nueva |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `change_password_wizard`

**Asistente para cambiar contraseña** · modelo `change.password.wizard` · módulo `base` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `decimal_precision`

**Precisión decimal** · modelo `decimal.precision` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `digits` | integer | 4 B | No | Dígitos |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Uso |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_act_server_group_rel`

**Relación muchos a muchos entre «ir.actions.server» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `act_id` | integer | 4 B | No | Referencia a ir_act_server |
| PK, FK | `gid` | integer | 4 B | No | Referencia a res_groups |

### `ir_act_server_res_partner_rel`

**Relación muchos a muchos entre «ir.actions.server» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `ir_act_server_id` | integer | 4 B | No | Referencia a ir_act_server |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `ir_act_server_webhook_field_rel`

**Relación muchos a muchos entre «ir.actions.server» y «ir.model.fields»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `server_id` | integer | 4 B | No | Referencia a ir_act_server |
| PK, FK | `field_id` | integer | 4 B | No | Referencia a ir_model_fields |

### `ir_act_window_group_rel`

**Relación muchos a muchos entre «ir.actions.act_window» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `act_id` | integer | 4 B | No | Referencia a ir_act_window |
| PK, FK | `gid` | integer | 4 B | No | Referencia a res_groups |

### `ir_actions_server_history`

**Historial de acciones del servidor** · modelo `ir.actions.server.history` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `action_id` | integer | 4 B | No | Acción → `ir_act_server` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | text | variable | Sí | Código |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_actions_todo`

**Asistentes de configuración** · modelo `ir.actions.todo` · módulo `base` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `action_id` | integer | 4 B | No | Acción |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `state` | varchar | variable | No | Estado |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_asset`

**Activo** · modelo `ir.asset` · módulo `base` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | No | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `bundle` | varchar | variable | No | Nombre del paquete |
|  | `directive` | varchar | variable | Sí | Directiva |
|  | `path` | varchar | variable | No | Ruta (o patrón glob) |
|  | `target` | varchar | variable | Sí | Objetivo |
|  | `active` | boolean | 1 B | Sí | activa |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_attachment`

**Archivos adjuntos** · modelo `ir.attachment` · módulo `base` · 22 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | Sí | ID del recurso |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `file_size` | integer | 4 B | Sí | Tamaño del archivo |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `res_model` | varchar | variable | Sí | Modelo del recurso |
|  | `res_field` | varchar | variable | Sí | Campo de recurso |
|  | `type` | varchar | variable | No | Tipo — Puede subir un archivo desde su computadora o copiar y pegar un enlace de internet a su archivo. |
|  | `url` | varchar | 1024 | Sí | URL |
|  | `access_token` | varchar | variable | Sí | Token de acceso |
|  | `store_fname` | varchar | variable | Sí | Nombre del archivo almacenado |
|  | `checksum` | varchar | 40 | Sí | Suma de verificación/SHA1 |
|  | `mimetype` | varchar | variable | Sí | Tipo MIME |
|  | `description` | text | variable | Sí | Descripción |
|  | `index_content` | text | variable | Sí | Contenido indexado |
|  | `public` | boolean | 1 B | Sí | Es un documento público |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `db_datas` | bytea | variable | Sí | Datos de la base de datos |
| FK | `original_id` | integer | 4 B | Sí | Archivo adjunto original (no optimizado, sin tamaño ajustado) → `ir_attachment` |

### `ir_config_parameter`

**Parámetro del sistema** · modelo `ir.config_parameter` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `key` | varchar | variable | No | Clave |
|  | `value` | text | variable | No | Valor |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_cron`

**Acciones planificadas** · modelo `ir.cron` · módulo `base` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `ir_actions_server_id` | integer | 4 B | No | Acción del servidor → `ir_act_server` |
| FK | `user_id` | integer | 4 B | No | Usuario encargado de la planificación → `res_users` |
|  | `interval_number` | integer | 4 B | No | Número de intervalo — Repetir cada x. |
|  | `priority` | integer | 4 B | Sí | Prioridad — Prioridad del trabajo, expresada con un entero: 0 es la prioridad máxima y 10 es la más baja. |
|  | `failure_count` | integer | 4 B | Sí | Cuenta de fallos — El número de fallas consecutivas de este trabajo. Se resetea de forma automática al tener éxito. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `cron_name` | varchar | variable | Sí | Nombre |
|  | `interval_type` | varchar | variable | No | Unidad de intervalo |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `nextcall` | timestamp | 8 B | No | Siguiente fecha de ejecución — Siguiente fecha de ejecución programada para esta acción. |
|  | `lastcall` | timestamp | 8 B | Sí | Última fecha de ejecución — La última vez que se ejecutó el cron con éxito. Se le proporciona al trabajo a través del contexto en la clave `lastcall`. |
|  | `first_failure_date` | timestamp | 8 B | Sí | Fecha del primer fallo — La primera vez que el cron falló. Se resetea de forma automática al tener éxito. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_cron_progress`

**Progreso de acciones programadas** · modelo `ir.cron.progress` · módulo `base` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `cron_id` | integer | 4 B | No | Cron → `ir_cron` |
|  | `remaining` | integer | 4 B | Sí | Restantes |
|  | `done` | integer | 4 B | Sí | Hecho |
|  | `timed_out_counter` | integer | 4 B | Sí | Contador de tiempo fuera |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `deactivate` | boolean | 1 B | Sí | Desactivar |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_cron_trigger`

**Acciones activadas** · modelo `ir.cron.trigger` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `cron_id` | integer | 4 B | No | Cron → `ir_cron` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `call_at` | timestamp | 8 B | No | Llamar a |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_default`

**Valores predeterminados** · modelo `ir.default` · módulo `base` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `field_id` | integer | 4 B | No | Campo → `ir_model_fields` |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` — Si se establece, la acción vinculada sólo se aplica a este usuario |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — Si se establece, la acción vinculada sólo se aplica a esta empresa |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `condition` | varchar | variable | Sí | Condición — Si se establece, se aplica el valor predeterminado. |
|  | `json_value` | varchar | variable | No | Valor predeterminado (formato JSON) |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_demo`

**Demostración** · modelo `ir.demo` · módulo `base` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_demo_failure`

**Error en la demostración** · modelo `ir.demo_failure` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `module_id` | integer | 4 B | No | Módulo → `ir_module_module` |
| FK | `wizard_id` | integer | 4 B | Sí | Asistente → `ir_demo_failure_wizard` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `error` | varchar | variable | Sí | Error |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_demo_failure_wizard`

**Asistente para error de datos de demostración** · modelo `ir.demo_failure.wizard` · módulo `base` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_embedded_actions`

**Acciones incrustadas** · modelo `ir.embedded.actions` · módulo `base` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `parent_action_id` | integer | 4 B | No | Acción principal → `ir_act_window` |
|  | `parent_res_id` | integer | 4 B | Sí | ID principal activa |
|  | `action_id` | integer | 4 B | Sí | Acción |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` — Acción incrustada específica para el usuario. Si se deja en blanco, la acción incrustada es compartida. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `parent_res_model` | varchar | variable | No | Modelo principal activo |
|  | `python_method` | varchar | variable | Sí | Método Python — Método Python que regresa una acción |
|  | `default_view_mode` | varchar | variable | Sí | Vista predeterminada — Vista predeterminada (si no, se toma la vista predeterminada de la acción) |
|  | `domain` | varchar | variable | Sí | Dominio — Dominio que se aplica al ID activo del modelo principal |
|  | `context` | varchar | variable | Sí | Contexto — Diccionario que representa el contexto como una expresión Python, está vacío de forma predeterminada (Predeterminado: {}). |
|  | `name` | jsonb | variable | Sí | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_embedded_actions_res_groups_rel`

**Relación muchos a muchos entre «ir.embedded.actions» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `ir_embedded_actions_id` | integer | 4 B | No | Referencia a ir_embedded_actions |
| PK, FK | `res_groups_id` | integer | 4 B | No | Referencia a res_groups |

### `ir_exports`

**Exportaciones** · modelo `ir.exports` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Exportar nombre |
|  | `resource` | varchar | variable | Sí | Recurso |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_exports_line`

**Línea de exportaciones** · modelo `ir.exports.line` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `export_id` | integer | 4 B | Sí | Exportar → `ir_exports` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre del campo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_filters`

**Filtros** · modelo `ir.filters` · módulo `base` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `action_id` | integer | 4 B | Sí | Acción — La acción de menú a la que se aplica este filtro. Si está vacía, el filtro se aplica a todos los menús de este modelo. |
| FK | `embedded_action_id` | integer | 4 B | Sí | Acción incrustada → `ir_embedded_actions` — La acción insertada a la que se aplica este filtro |
|  | `embedded_parent_res_id` | integer | 4 B | Sí | Res. principal incrustada — ID del registro al que se le debe aplicar el filtro. Solo se usa en combinación con acciones incrustadas |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre del filtro |
|  | `sort` | varchar | variable | No | Ordenar |
|  | `model_id` | varchar | variable | No | Modelo |
|  | `domain` | text | variable | No | Dominio |
|  | `context` | text | variable | No | Contexto |
|  | `is_default` | boolean | 1 B | Sí | Filtro predeterminado |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_filters_res_users_rel`

**Relación muchos a muchos entre «ir.filters» y «res.users»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `ir_filters_id` | integer | 4 B | No | Referencia a ir_filters |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `ir_logging`

**Registro** · modelo `ir.logging` · módulo `base` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `create_uid` | integer | 4 B | Sí | Creado por |
|  | `write_uid` | integer | 4 B | Sí | Última actualización por |
|  | `name` | varchar | variable | No | Nombre |
|  | `type` | varchar | variable | No | Tipo |
|  | `dbname` | varchar | variable | Sí | Nombre de la base de datos |
|  | `level` | varchar | variable | Sí | Nivel |
|  | `path` | varchar | variable | No | Ruta |
|  | `func` | varchar | variable | No | Función |
|  | `line` | varchar | variable | No | Línea |
|  | `message` | text | variable | No | Mensaje |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_mail_server`

**Servidor de correo** · modelo `ir.mail_server` · módulo `base` · 28 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `smtp_port` | integer | 4 B | Sí | Puerto SMTP — Puerto SMTP. Por lo general 465 para SSL y 25 o 587 para otros casos. |
|  | `sequence` | integer | 4 B | Sí | Prioridad — Cuando no se solicita un servidor de correo específico para un correo, se usa la prioridad más alta. La prioridad predeterminada es 10 (n… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `from_filter` | varchar | variable | Sí | Filtro DE — Lista separada por comas de direcciones o dominios para los cuáles se puede usar este servidor. Por ejemplo: "notificacion@odoo.com" o "o… |
|  | `smtp_host` | varchar | variable | Sí | Servidor SMTP — Nombre de host o dirección IP del servidor SMTP |
|  | `smtp_authentication` | varchar | variable | No | Autenticar con |
|  | `smtp_user` | varchar | variable | Sí | Nombre de usuario — Nombre de usuario opcional para autenticación SMTP |
|  | `smtp_pass` | varchar | variable | Sí | Contraseña — Contraseña opcional para la autenticación SMTP |
|  | `smtp_encryption` | varchar | variable | No | Cifrado de la conexión — Elija el esquema de cifrado de la conexión: - Ninguno: Las sesiones SMTP se realizan en texto plano. - TLS (STARTTLS): Se solicita encrip… |
|  | `smtp_debug` | boolean | 1 B | Sí | Depuración — Si está habilitado, la salida completa de las sesiones SMTP se escribirá en el registro del servidor al nivel de DEBUG (tome en cuenta qu… |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `max_email_size` | double precision | 8 B | Sí | Tamaño máximo de correo |
|  | `smtp_ssl_certificate` | bytea | variable | Sí | Certificado SSL — Certificado SSL que se usa para la autenticación |
|  | `smtp_ssl_private_key` | bytea | variable | Sí | Clave privada SSL — Clave privada SSL que se usa para la autenticación |
| FK | `owner_user_id` | integer | 4 B | Sí | Propietario → `res_users` |
|  | `owner_limit_count` | integer | 4 B | Sí | Limitar la cantidad de propietarios |
|  | `owner_limit_time` | timestamp | 8 B | Sí | Límite de tiempo del propietario |
|  | `google_gmail_access_token_expiration` | integer | 4 B | Sí | Marca de tiempo de vencimiento del token de acceso |
|  | `google_gmail_refresh_token` | varchar | variable | Sí | Actualizar token |
|  | `google_gmail_access_token` | varchar | variable | Sí | Token de acceso |
|  | `microsoft_outlook_access_token_expiration` | integer | 4 B | Sí | Marca de tiempo de vencimiento del token de acceso de Outlook |
|  | `microsoft_outlook_refresh_token` | varchar | variable | Sí | Token de actualización de Outlook |
|  | `microsoft_outlook_access_token` | varchar | variable | Sí | Token de acceso de Outlook |

### `ir_model`

**Modelos** · modelo `ir.model` · módulo `base` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `model` | varchar | variable | No | Modelo |
|  | `order` | varchar | variable | No | Orden — Expresión SQL para ordenar registros en el modelo; por ejemplo, "x_sequence asc, id desc" |
|  | `state` | varchar | variable | Sí | Tipo |
|  | `fold_name` | varchar | variable | Sí | Plegar campo — En la vista kanban donde las columnas son registros de este modelo, el valor de este campo (booleano) determina qué columna se debe plega… |
|  | `name` | jsonb | variable | No | Descripción del modelo |
|  | `info` | text | variable | Sí | Información |
|  | `abstract` | boolean | 1 B | Sí | Modelo abstracto |
|  | `transient` | boolean | 1 B | Sí | Modelo transitorio |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `is_mail_thread` | boolean | 1 B | Sí | Tiene hilo de correo |
|  | `is_mail_activity` | boolean | 1 B | Sí | Tiene actividad de correo |
|  | `is_mail_blacklist` | boolean | 1 B | Sí | Tiene exclusión de correo |

### `ir_model_access`

**Acceso al modelo** · modelo `ir.model.access` · módulo `base` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | No | Modelo → `ir_model` |
| FK | `group_id` | integer | 4 B | Sí | Grupo → `res_groups` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Activo — Si desmarca el campo activo, deshabilitará el ACL sin eliminarlo (si elimina un ACL nativo, se volverá a crear cuando cargue el módulo). |
|  | `perm_read` | boolean | 1 B | Sí | Acceso de lectura |
|  | `perm_write` | boolean | 1 B | Sí | Permiso de escritura |
|  | `perm_create` | boolean | 1 B | Sí | Acceso de creación |
|  | `perm_unlink` | boolean | 1 B | Sí | Acceso de eliminación |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_model_constraint`

**Restricción del modelo** · modelo `ir.model.constraint` · módulo `base` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model` | integer | 4 B | No | Modelo → `ir_model` |
| FK | `module` | integer | 4 B | No | Módulo → `ir_module_module` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Restricción — Restricción de PostgreSQL o nombre de la clave externa. |
|  | `definition` | varchar | variable | Sí | Definición — Definición de restricciones de PostgreSQL |
|  | `type` | varchar | 1 | No | Tipo de restricción — Tipo de restricción: 'f' para una clave externa, 'u' para otras restricciones. |
|  | `message` | jsonb | variable | Sí | Mensaje — Mensaje de error que aparece al incumplir la restricción. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_model_data`

**Datos del modelo** · modelo `ir.model.data` · módulo `base` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_id` | integer | 4 B | Sí | ID de registro — ID del registro objetivo en la base de datos |
|  | `noupdate` | boolean | 1 B | Sí | No se puede actualizar |
|  | `name` | varchar | variable | No | Identificador externo — Clave/identificador externo que puede usarse para la integración de datos con sistemas externos |
|  | `module` | varchar | variable | No | Módulo |
|  | `model` | varchar | variable | No | Nombre del modelo |

### `ir_model_fields`

**Campos** · modelo `ir.model.fields` · módulo `base` · 44 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `relation_field_id` | integer | 4 B | Sí | Campo de relación → `ir_model_fields` |
| FK | `model_id` | integer | 4 B | No | Modelo → `ir_model` — El modelo al que pertenece este campo. |
| FK | `related_field_id` | integer | 4 B | Sí | Campo relacionado → `ir_model_fields` |
|  | `size` | integer | 4 B | Sí | Tamaño |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre del campo |
|  | `model` | varchar | variable | No | Nombre del modelo — El nombre técnico del modelo al que pertenece este campo. |
|  | `relation` | varchar | variable | Sí | Modelo relacionado — Para los campos de relación, el nombre técnico del modelo destino |
|  | `relation_field` | varchar | variable | Sí | Campo de relación — Para campos one2many, el campo del modelo destino que implementa la relación inversa many2one. |
|  | `ttype` | varchar | variable | No | Tipo de campo |
|  | `related` | varchar | variable | Sí | Definición del campo relacionado — El campo relacionado correspondiente, si lo hay. Debe ser una lista de nombres de campos separados por puntos. |
|  | `translate` | varchar | variable | Sí | Traducible — Si los valores de este campo se pueden traducir (activa el mecanismo de traducción para ese campo). |
|  | `state` | varchar | variable | No | Tipo |
|  | `on_delete` | varchar | variable | Sí | Al eliminar — Propiedad 'Al eliminar' para campos many2one |
|  | `domain` | varchar | variable | Sí | Dominio — El dominio opcional para restringir los posibles valores para los campos relacionales se especifica como una expresión de Python compuest… |
|  | `relation_table` | varchar | variable | Sí | Tabla de relación — Utilizado para personalizar campos many2many para definir un nombre de tabla de relación personalizada |
|  | `column1` | varchar | variable | Sí | Columna 1 — Columna referente al registro en la tabla del modelo |
|  | `column2` | varchar | variable | Sí | Columna 2 — Columna referente al registro en la tabla del comodelo |
|  | `depends` | varchar | variable | Sí | Dependencias — Dependencias del método de cálculo; una lista de nombres de campos separados por comas, como name, partner_id.name |
|  | `currency_field` | varchar | variable | Sí | Campo de moneda — Nombre del campo many2one que contiene la res.currency |
|  | `field_description` | jsonb | variable | No | Etiqueta de campo |
|  | `help` | jsonb | variable | Sí | Campo de ayuda |
|  | `compute` | text | variable | Sí | Calcular — Código para calcular el valor del campo. Itera sobre el conjunto de registros 'self' y asigna el valor del campo: for record in self: rec… |
|  | `copied` | boolean | 1 B | Sí | Copiado — Si el valor se copiará o no al duplicar un registro. |
|  | `required` | boolean | 1 B | Sí | Requerido |
|  | `readonly` | boolean | 1 B | Sí | Solo lectura |
|  | `index` | boolean | 1 B | Sí | Indexado |
|  | `company_dependent` | boolean | 1 B | Sí | Dependiente de la empresa — Si los valores de este campo dependen de la empresa |
|  | `group_expand` | boolean | 1 B | Sí | Expandir grupos — Si está seleccionado, todos los registros del modelo objetivo se incluirán en un resultado agrupado (por ejemplo, los filtros "Agrupar po… |
|  | `selectable` | boolean | 1 B | Sí | Se puede seleccionar |
|  | `store` | boolean | 1 B | Sí | Almacenado — Si el valor se almacena en la base de datos. |
|  | `sanitize` | boolean | 1 B | Sí | Depurar HTML |
|  | `sanitize_overridable` | boolean | 1 B | Sí | Depurar HTML anulable |
|  | `sanitize_tags` | boolean | 1 B | Sí | Depurar etiquetas HTML |
|  | `sanitize_attributes` | boolean | 1 B | Sí | Depurar atributos HTML |
|  | `sanitize_style` | boolean | 1 B | Sí | Depurar estilo HTML |
|  | `sanitize_form` | boolean | 1 B | Sí | Depurar formulario HTML |
|  | `strip_style` | boolean | 1 B | Sí | Quitar atributo de estilo |
|  | `strip_classes` | boolean | 1 B | Sí | Quitar atributo de clase |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `tracking` | integer | 4 B | Sí | Activar el seguimiento de órdenes — Si se establece, se realiza un seguimiento de cada modificación realizada en este campo. El valor se utiliza para ordenar los valores de… |

### `ir_model_fields_group_rel`

**Relación muchos a muchos entre «ir.model.fields» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `field_id` | integer | 4 B | No | Referencia a ir_model_fields |
| PK, FK | `group_id` | integer | 4 B | No | Referencia a res_groups |

### `ir_model_fields_selection`

**Selección de campos** · modelo `ir.model.fields.selection` · módulo `base` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `field_id` | integer | 4 B | No | Campo → `ir_model_fields` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `value` | varchar | variable | No | Valor |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_model_inherit`

**Modelo de árbol de la herencia** · modelo `ir.model.inherit` · módulo `base` · 4 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | No | Modelo → `ir_model` |
| FK | `parent_id` | integer | 4 B | No | Principal → `ir_model` |
| FK | `parent_field_id` | integer | 4 B | Sí | Campo principal → `ir_model_fields` |

### `ir_model_relation`

**Modelo relacional** · modelo `ir.model.relation` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model` | integer | 4 B | No | Modelo → `ir_model` |
| FK | `module` | integer | 4 B | No | Módulo → `ir_module_module` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de relación — Nombre de la tabla de PostgreSQL que implementa una relación many2many. |
|  | `write_date` | timestamp | 8 B | Sí | Escribir la fecha |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |

### `ir_module_category`

**Aplicación** · modelo `ir.module.category` · módulo `base` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
| FK | `parent_id` | integer | 4 B | Sí | Aplicación principal → `ir_module_category` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `visible` | boolean | 1 B | Sí | Visible |
|  | `exclusive` | boolean | 1 B | Sí | Exclusivo |

### `ir_module_module`

**Módulo** · modelo `ir.module.module` · módulo `base` · 31 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `website` | varchar | variable | Sí | Sitio web |
|  | `summary` | jsonb | variable | Sí | Resumen |
|  | `name` | varchar | variable | No | Nombre técnico |
|  | `author` | varchar | variable | Sí | Autor |
|  | `icon` | varchar | variable | Sí | URL del icono |
|  | `state` | varchar | 16 | Sí | Estado |
|  | `latest_version` | varchar | variable | Sí | Versión instalada |
|  | `shortdesc` | jsonb | variable | Sí | Nombre de módulo |
| FK | `category_id` | integer | 4 B | Sí | Categoría → `ir_module_category` |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `application` | boolean | 1 B | Sí | Aplicación |
|  | `demo` | boolean | 1 B | Sí | Datos de demostración |
|  | `web` | boolean | 1 B | Sí | — |
|  | `license` | varchar | 32 | Sí | Licencia |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
|  | `auto_install` | boolean | 1 B | Sí | Instalación automática — El sistema instala un módulo autoinstalable cuando se satisfacen todas sus dependencias. Si el módulo no tiene dependencias, siempre se i… |
|  | `to_buy` | boolean | 1 B | Sí | Módulo de Odoo Enterprise |
|  | `maintainer` | varchar | variable | Sí | Encargado del mantenimiento |
|  | `published_version` | varchar | variable | Sí | Versión publicada |
|  | `url` | varchar | variable | Sí | URL |
|  | `contributors` | text | variable | Sí | Contribuidores |
|  | `menus_by_module` | text | variable | Sí | Menús |
|  | `reports_by_module` | text | variable | Sí | Reportes |
|  | `views_by_module` | text | variable | Sí | Vistas |
|  | `module_type` | varchar | variable | Sí | Tipo de módulo |
|  | `imported` | boolean | 1 B | Sí | Módulo importado |

### `ir_module_module_dependency`

**Dependencia del módulo** · modelo `ir.module.module.dependency` · módulo `base` · 4 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `name` | varchar | variable | Sí | Nombre |
| FK | `module_id` | integer | 4 B | Sí | Módulo → `ir_module_module` |
|  | `auto_install_required` | boolean | 1 B | Sí | Instalación automática necesaria — Si esta dependencia bloquea la instalación automática del dependiente |

### `ir_module_module_exclusion`

**Exclusión del módulo** · modelo `ir.module.module.exclusion` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `module_id` | integer | 4 B | Sí | Módulo → `ir_module_module` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_profile`

**Resultados del análisis de rendimiento de software** · modelo `ir.profile` · módulo `base` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sql_count` | integer | 4 B | Sí | Número de consultas |
|  | `entry_count` | integer | 4 B | Sí | Número de asientos |
|  | `session` | varchar | variable | Sí | Sesión |
|  | `name` | varchar | variable | Sí | Descripción |
|  | `init_stack_trace` | text | variable | Sí | Seguimiento de pila inicial |
|  | `sql` | text | variable | Sí | SQL |
|  | `traces_async` | text | variable | Sí | Rastrea asincronización |
|  | `traces_sync` | text | variable | Sí | Rastrea sincronización |
|  | `others` | text | variable | Sí | otros |
|  | `qweb` | text | variable | Sí | Qweb |
|  | `duration` | numeric | variable | Sí | Duración — Tiempo real transcurrido |
|  | `cpu_duration` | numeric | variable | Sí | Tiempo de CPU — Frecuencia de reloj (sin incluir otros procesos o SQL) |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |

### `ir_rule`

**Regla** · modelo `ir.rule` · módulo `base` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | No | Modelo → `ir_model` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `domain_force` | text | variable | Sí | Dominio |
|  | `active` | boolean | 1 B | Sí | Activo — Si desmarca el campo activo, deshabilitará la regla de registro sin eliminarla (si elimina una regla de registro nativa, se recreará cuan… |
|  | `perm_read` | boolean | 1 B | Sí | Leer |
|  | `perm_write` | boolean | 1 B | Sí | Editar |
|  | `perm_create` | boolean | 1 B | Sí | Crear |
|  | `perm_unlink` | boolean | 1 B | Sí | Eliminar |
|  | `global` | boolean | 1 B | Sí | Global — Si no se especifica un grupo, la regla se considerará global y se aplicará a todos |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_sequence`

**Secuencia** · modelo `ir.sequence` · módulo `base` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `number_next` | integer | 4 B | No | Siguiente número — Siguiente número de esta secuencia |
|  | `number_increment` | integer | 4 B | No | Paso — El siguiente número de la secuencia se incrementará por este número. |
|  | `padding` | integer | 4 B | No | Tamaño de la secuencia — Odoo agregará algunos '0' a la izquierda del 'número siguiente' en automático para obtener el tamaño del espacio necesario. |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `code` | varchar | variable | Sí | Código de la secuencia |
|  | `implementation` | varchar | variable | No | Implementación — Al asignar un número de secuencia a un registro, la implementación de secuencia "sin espacios" garantiza que cada número anterior ya haya… |
|  | `prefix` | varchar | variable | Sí | Prefijo — Valor del prefijo del registro para la secuencia |
|  | `suffix` | varchar | variable | Sí | Sufijo — Valor del sufijo del registro para la secuencia |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `use_date_range` | boolean | 1 B | Sí | Usar subsecuencias por date_range |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_sequence_date_range`

**Rango de fechas de la secuencia** · modelo `ir.sequence.date_range` · módulo `base` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `sequence_id` | integer | 4 B | No | Secuencia principal → `ir_sequence` |
|  | `number_next` | integer | 4 B | No | Siguiente número — Siguiente número de esta secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `date_from` | date | 4 B | No | Desde |
|  | `date_to` | date | 4 B | No | Para |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_ui_menu`

**Menú** · modelo `ir.ui.menu` · módulo `base` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `parent_id` | integer | 4 B | Sí | Menú principal → `ir_ui_menu` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `web_icon` | varchar | variable | Sí | Archivo del icono web |
|  | `action` | varchar | variable | Sí | Acción |
|  | `name` | jsonb | variable | No | Menú |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_ui_menu_group_rel`

**Relación muchos a muchos entre «ir.ui.menu» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `menu_id` | integer | 4 B | No | Referencia a ir_ui_menu |
| PK, FK | `gid` | integer | 4 B | No | Referencia a res_groups |

### `ir_ui_view`

**Vista** · modelo `ir.ui.view` · módulo `base` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `priority` | integer | 4 B | No | Secuencia |
| FK | `inherit_id` | integer | 4 B | Sí | Vista heredada → `ir_ui_view` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Ver nombre |
|  | `model` | varchar | variable | Sí | Modelo |
|  | `key` | varchar | variable | Sí | Clave |
|  | `type` | varchar | variable | Sí | Ver tipo |
|  | `arch_fs` | varchar | variable | Sí | Nombre del archivo de la arquitectura — Archivo desde el que se origina la vista. Útil para restablecer (por completo) vistas dañadas o para leer la arquitectura del archivo en… |
|  | `mode` | varchar | variable | No | Modo de herencia de la vista — Solo aplica si esta vista hereda de otra (inherit_id no es False/Null). * Si tiene extensión (predeterminada), cuando se solicita esta vi… |
|  | `arch_db` | jsonb | variable | Sí | Blob de la arquitectura — Este campo almacena la arquitectura de la vista. |
|  | `arch_prev` | text | variable | Sí | Arquitectura de la vista previa — Este campo almacenará la `arch_db` actual antes de escribir en ella. Es útil para restablecer (de forma parcial) una vista con errores. |
|  | `arch_updated` | boolean | 1 B | Sí | Arquitectura modificada |
|  | `active` | boolean | 1 B | Sí | Activo — Si se hereda esta vista, * Si es "TRUE", la vista siempre extiende a la vista principal * Si es "FALSE", la vista actual no extiende la v… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `customize_show` | boolean | 1 B | Sí | Mostrar como herencia opcional |

### `ir_ui_view_custom`

**Vista personalizada** · modelo `ir.ui.view.custom` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `ref_id` | integer | 4 B | No | Vista original → `ir_ui_view` |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `arch` | text | variable | No | Ver arquitectura |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `ir_ui_view_group_rel`

**Relación muchos a muchos entre «ir.ui.view» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `view_id` | integer | 4 B | No | Referencia a ir_ui_view |
| PK, FK | `group_id` | integer | 4 B | No | Referencia a res_groups |

### `module_country`

**Relación muchos a muchos entre «ir.module.module» y «res.country»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `module_id` | integer | 4 B | No | Referencia a ir_module_module |
| PK, FK | `country_id` | integer | 4 B | No | Referencia a res_country |

### `pos_category_res_config_settings_rel`

**Relación muchos a muchos entre «res.config.settings» y «pos.category»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `res_config_settings_id` | integer | 4 B | No | Referencia a res_config_settings |
| PK, FK | `pos_category_id` | integer | 4 B | No | Referencia a pos_category |

### `product_pricelist_res_config_settings_rel`

**Relación muchos a muchos entre «res.config.settings» y «product.pricelist»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `res_config_settings_id` | integer | 4 B | No | Referencia a res_config_settings |
| PK, FK | `product_pricelist_id` | integer | 4 B | No | Referencia a product_pricelist |

### `properties_base_definition`

**Definición base de las propiedades** · modelo `properties.base.definition` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `properties_field_id` | integer | 4 B | No | Campo de propiedades → `ir_model_fields` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `properties_definition` | jsonb | variable | Sí | Definición de las propiedades |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `rel_modules_langexport`

**Relación muchos a muchos entre «base.language.export» y «ir.module.module»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `wiz_id` | integer | 4 B | No | Referencia a base_language_export |
| PK, FK | `module_id` | integer | 4 B | No | Referencia a ir_module_module |

### `report_layout`

**Diseño del reporte** · modelo `report.layout` · módulo `base` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `view_id` | integer | 4 B | No | Plantilla del documento → `ir_ui_view` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `image` | varchar | variable | Sí | Visualizar fuente de la imagen |
|  | `pdf` | varchar | variable | Sí | Previsualizar fuente del pdf |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `report_paperformat`

**Configuración del formato de papel** · modelo `report.paperformat` · módulo `base` · 20 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `page_height` | integer | 4 B | Sí | Altura de la página (mm) |
|  | `page_width` | integer | 4 B | Sí | Ancho de la página (mm) |
|  | `header_spacing` | integer | 4 B | Sí | Espaciado del encabezado |
|  | `dpi` | integer | 4 B | No | DPI de salida |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `format` | varchar | variable | Sí | Tamaño del papel — Seleccione el tamaño del papel correcto |
|  | `orientation` | varchar | variable | Sí | Orientación |
|  | `default` | boolean | 1 B | Sí | ¿Formato de papel predeterminado? |
|  | `header_line` | boolean | 1 B | Sí | Mostrar una línea de encabezado |
|  | `disable_shrinking` | boolean | 1 B | Sí | Deshabilitar el encogimiento inteligente |
|  | `css_margins` | boolean | 1 B | Sí | Use los márgenes CSS |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `margin_top` | double precision | 8 B | Sí | Margen superior (mm) |
|  | `margin_bottom` | double precision | 8 B | Sí | Margen inferior (mm) |
|  | `margin_left` | double precision | 8 B | Sí | Margen izquierdo (mm) |
|  | `margin_right` | double precision | 8 B | Sí | Margen derecho (mm) |

### `res_bank`

**Banco** · modelo `res.bank` · módulo `base` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `state` | integer | 4 B | Sí | Estado federal → `res_country_state` |
| FK | `country` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `street` | varchar | variable | Sí | Calle |
|  | `street2` | varchar | variable | Sí | Calle2 |
|  | `zip` | varchar | variable | Sí | Código postal |
|  | `city` | varchar | variable | Sí | Ciudad |
|  | `email` | varchar | variable | Sí | Correo electrónico |
|  | `phone` | varchar | variable | Sí | Teléfono |
|  | `bic` | varchar | variable | Sí | Código de identificación bancaria — También se le conoce como BIC o Swift. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `l10n_pe_edi_code` | varchar | variable | Sí | Código (PE) — Código bancario asignado por la SUNAT para identificar a las instituciones bancarias. |

### `res_company`

**Empresas** · modelo `res.company` · módulo `base` · 134 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `name` | varchar | variable | No | Nombre de la empresa |
| FK | `partner_id` | integer | 4 B | No | Contacto → `res_partner` |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Se usa para ordenar las empresas en menú de cambio de empresas |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
| FK | `parent_id` | integer | 4 B | Sí | Empresa matriz → `res_company` |
| FK | `paperformat_id` | integer | 4 B | Sí | Formato de papel → `report_paperformat` |
| FK | `external_report_layout_id` | integer | 4 B | Sí | Plantilla del documento → `ir_ui_view` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email` | varchar | variable | Sí | Correo electrónico |
|  | `phone` | varchar | variable | Sí | Teléfono |
|  | `font` | varchar | variable | Sí | Fuente |
|  | `primary_color` | varchar | variable | Sí | Color primario |
|  | `secondary_color` | varchar | variable | Sí | Color secundario |
|  | `layout_background` | varchar | variable | No | Diseño del fondo |
|  | `report_header` | jsonb | variable | Sí | Lema de la empresa — Lema de la empresa. Aparece en el encabezado o pie de página de los documentos impresos (según el diseño seleccionado). |
|  | `report_footer` | jsonb | variable | Sí | Pie de página del reporte — Texto del pie de página que se muestra en la parte inferior de todos los reportes. |
|  | `company_details` | jsonb | variable | Sí | Detalles de la empresa — Texto de encabezado en la parte superior de todos los reportes. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `uses_default_logo` | boolean | 1 B | Sí | Usa el logotipo predeterminado |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `logo_web` | bytea | variable | Sí | Logo web |
| FK | `nomenclature_id` | integer | 4 B | Sí | Nomenclatura → `barcode_nomenclature` |
| FK | `resource_calendar_id` | integer | 4 B | Sí | Horas laborables predeterminadas → `resource_calendar` |
| FK | `alias_domain_id` | integer | 4 B | Sí | Dominio de correo electrónico → `mail_alias_domain` |
|  | `email_primary_color` | varchar | variable | Sí | Texto del botón de correo |
|  | `email_secondary_color` | varchar | variable | Sí | Color del botón del correo electrónico |
|  | `iap_enrich_auto_done` | boolean | 1 B | Sí | Enriquecimiento listo |
|  | `snailmail_color` | boolean | 1 B | Sí | Color del correo postal |
|  | `snailmail_cover` | boolean | 1 B | Sí | Agregar una portada |
|  | `snailmail_duplex` | boolean | 1 B | Sí | Ambos lados |
|  | `fiscalyear_last_day` | integer | 4 B | No | Último día del año fiscal |
| FK | `transfer_account_id` | integer | 4 B | Sí | Cuenta de transferencias interbancarias → `account_account` — Cuenta intermediaria que se utiliza al mover dinero desde una cuenta de liquidez a otra |
| FK | `default_cash_difference_income_account_id` | integer | 4 B | Sí | Ingreso por diferencia de efectivo → `account_account` |
| FK | `default_cash_difference_expense_account_id` | integer | 4 B | Sí | Gasto por diferencia de efectivo → `account_account` |
| FK | `account_journal_suspense_account_id` | integer | 4 B | Sí | Cuenta transitoria del diario → `account_account` |
| FK | `account_journal_early_pay_discount_gain_account_id` | integer | 4 B | Sí | Cuenta de ganancia por cancelación por diferencia de efectivo → `account_account` |
| FK | `account_journal_early_pay_discount_loss_account_id` | integer | 4 B | Sí | Cuenta de pérdida por cancelación por diferencia de efectivo → `account_account` |
| FK | `account_sale_tax_id` | integer | 4 B | Sí | Impuesto de venta predeterminado → `account_tax` |
| FK | `account_purchase_tax_id` | integer | 4 B | Sí | Impuesto de compra predeterminado → `account_tax` |
| FK | `account_purchase_receipt_fiscal_position_id` | integer | 4 B | Sí | Posición fiscal predeterminada del recibo de compra → `account_fiscal_position` |
| FK | `currency_exchange_journal_id` | integer | 4 B | Sí | Diario de pérdidas y ganancias por cambio de moneda → `account_journal` |
| FK | `income_currency_exchange_account_id` | integer | 4 B | Sí | Cuenta de ganancias por diferencia de cambio → `account_account` |
| FK | `expense_currency_exchange_account_id` | integer | 4 B | Sí | Cuenta de pérdida por diferencia de cambio → `account_account` |
| FK | `incoterm_id` | integer | 4 B | Sí | Incoterm predeterminado → `account_incoterms` — Los términos de comercio internacional son una serie de términos comerciales usados en las transacciones internacionales. |
| FK | `batch_payment_sequence_id` | integer | 4 B | Sí | Secuencia de pagos por lote → `ir_sequence` |
| FK | `account_opening_move_id` | integer | 4 B | Sí | Asiento contable de apertura → `account_move` — El asiento contable que contiene el balance inicial de todas las cuentas de esta empresa. |
| FK | `account_default_pos_receivable_account_id` | integer | 4 B | Sí | Cuenta por cobrar predeterminada del PdV → `account_account` |
| FK | `expense_accrual_account_id` | integer | 4 B | Sí | Cuenta acumulada de gastos → `account_account` — Cuenta que se utiliza para mover el periodo de un gasto |
| FK | `revenue_accrual_account_id` | integer | 4 B | Sí | Cuenta acumulada de ingresos → `account_account` — Cuenta que se utiliza para mover el periodo de un ingreso |
| FK | `automatic_entry_default_journal_id` | integer | 4 B | Sí | Diario predeterminado de asiento automático → `account_journal` — Diario que se utiliza de forma predeterminada para mover el periodo de un asiento |
| FK | `domestic_fiscal_position_id` | integer | 4 B | Sí | Posición fiscal doméstica → `account_fiscal_position` |
| FK | `account_fiscal_country_id` | integer | 4 B | Sí | País fiscal → `res_country` — El país que se utilizará en los reportes fiscales de esta empresa |
| FK | `tax_cash_basis_journal_id` | integer | 4 B | Sí | Diario de base de efectivo → `account_journal` |
| FK | `account_cash_basis_base_account_id` | integer | 4 B | Sí | Cuenta de base de impuestos recibidos → `account_account` — Cuenta que se establecerá en las líneas de asientos contables en el diario de base de efectivo y que se utilizarán para llevar un seguimi… |
| FK | `account_discount_income_allocation_id` | integer | 4 B | Sí | Cuenta separada para el descuento de ingreso → `account_account` |
| FK | `account_discount_expense_allocation_id` | integer | 4 B | Sí | Cuenta separada para el descuento del gasto → `account_account` |
| FK | `income_account_id` | integer | 4 B | Sí | Cuenta de ingresos → `account_account` — Esta cuenta se utilizará al validar una factura del cliente. |
| FK | `expense_account_id` | integer | 4 B | Sí | Cuenta de gastos → `account_account` — El gasto se contabiliza cuando se valida una factura del proveedor, excepto en la contabilidad anglosajona con valoración perpetua del in… |
| FK | `price_difference_account_id` | integer | 4 B | Sí | Cuenta de diferencia de precio → `account_account` — Durante la valuación perpetua esta cuenta retendrá la diferencia de precio entre el precio estándar y el precio de la factura de proveedor. |
|  | `fiscalyear_last_month` | varchar | variable | No | Último mes del año fiscal |
|  | `chart_template` | varchar | variable | Sí | Plantilla de plan |
|  | `bank_account_code_prefix` | varchar | variable | Sí | Prefijo de las cuentas bancarias |
|  | `cash_account_code_prefix` | varchar | variable | Sí | Prefijo de las cuentas de efectivo |
|  | `transfer_account_code_prefix` | varchar | variable | Sí | Prefijo de las cuentas de transferencias |
|  | `tax_calculation_rounding_method` | varchar | variable | Sí | Método de redondeo del cálculo de impuestos |
|  | `terms_type` | varchar | variable | Sí | Formato de los términos y condiciones |
|  | `quick_edit_mode` | varchar | variable | Sí | Codificación rápida |
|  | `account_price_include` | varchar | variable | No | Precio de venta predeterminado incluido — Se predetermina según si el precio de venta que utiliza en el producto y en las facturas de esta empresa incluye sus impuestos. |
|  | `fiscalyear_lock_date` | date | 4 B | Sí | Fecha de bloqueo global — Cualquier asiento anterior o hasta esa fecha se pospondrá para una fecha posterior, según la secuencia de su diario. |
|  | `tax_lock_date` | date | 4 B | Sí | Fecha de bloqueo de la declaración de impuestos — Cualquier asiento con impuestos anterior o hasta esa fecha se pospondrá para una fecha posterior, según la secuencia de su diario. La fec… |
|  | `sale_lock_date` | date | 4 B | Sí | Fecha de bloqueo de las ventas — Cualquier asiento de venta anterior o hasta esta fecha se pospondrá para una fecha posterior de acuerdo con la secuencia de su diario. |
|  | `purchase_lock_date` | date | 4 B | Sí | Fecha de bloqueo de compras — Cualquier asiento de compra anterior o hasta esta fecha se pospondrá para una fecha posterior de acuerdo con la secuencia de su diario. |
|  | `hard_lock_date` | date | 4 B | Sí | Fecha de bloqueo permanente — Cualquier asiento anterior o hasta esa fecha se pospondrá para una fecha posterior, según la secuencia de su diario. Esta fecha de bloque… |
|  | `account_opening_date` | date | 4 B | Sí | Asiento de apertura — Esa es la fecha del asiento de apertura. |
|  | `invoice_terms` | jsonb | variable | Sí | Términos y condiciones predeterminados |
|  | `invoice_terms_html` | jsonb | variable | Sí | Términos y condiciones predeterminados como una página web |
|  | `expects_chart_of_accounts` | boolean | 1 B | Sí | Se espera un plan de cuentas |
|  | `anglo_saxon_accounting` | boolean | 1 B | Sí | Utilizar contabilidad anglosajona |
|  | `qr_code` | boolean | 1 B | Sí | Mostrar código QR en facturas |
|  | `link_qr_code` | boolean | 1 B | Sí | Mostrar el enlace del código QR |
|  | `display_invoice_amount_total_words` | boolean | 1 B | Sí | Importe total de una factura con letra |
|  | `display_invoice_tax_company_currency` | boolean | 1 B | Sí | Impuestos en la moneda de la empresa |
|  | `account_use_credit_limit` | boolean | 1 B | Sí | Límite de crédito de ventas — Habilitar el uso de límite de crédito en los partners. |
|  | `tax_exigibility` | boolean | 1 B | Sí | Utilizar base de efectivo |
|  | `account_storno` | boolean | 1 B | Sí | Contabilidad Storno |
|  | `restrictive_audit_trail` | boolean | 1 B | Sí | Pista de auditoría restrictiva — Habilitar esta opción para evitar que se eliminen registros relacionados al asiento de diario. |
|  | `autopost_bills` | boolean | 1 B | Sí | Validar facturas en automático |
|  | `hr_presence_control_email_amount` | integer | 4 B | Sí | Número de correos electrónicos por enviar |
|  | `contract_expiration_notice_period` | integer | 4 B | Sí | Plazo de notificación de contrato vencido |
|  | `work_permit_expiration_notice_period` | integer | 4 B | Sí | Plazo de notificación del permiso de trabajo vencido |
|  | `hr_presence_control_ip_list` | varchar | variable | Sí | Direcciones IP válidas |
|  | `employee_properties_definition` | jsonb | variable | Sí | Propiedades del empleado |
|  | `hr_presence_control_login` | boolean | 1 B | Sí | Según el estado del usuario en el sistema |
|  | `hr_presence_control_email` | boolean | 1 B | Sí | Según la cantidad de correos electrónicos enviados |
|  | `hr_presence_control_ip` | boolean | 1 B | Sí | Según la dirección IP |
|  | `hr_presence_control_attendance` | boolean | 1 B | Sí | Según las asistencias |
| FK | `internal_transit_location_id` | integer | 4 B | Sí | Ubicación del tránsito interno → `stock_location` |
| FK | `stock_mail_confirmation_template_id` | integer | 4 B | Sí | Plantilla de correo electrónico para la confirmación de recolección → `mail_template` — Correo electrónico enviado al cliente una vez que se realiza la orden. |
|  | `annual_inventory_day` | integer | 4 B | Sí | Día del mes — Día del mes en el que se debe realizar el inventario anual. Si es cero o negativo, se seleccionará el primer día del mes. Si es mayor que… |
|  | `annual_inventory_month` | varchar | variable | Sí | Mes del inventario anual — Mes del inventario anual para productos que no están en una ubicación con una fecha de inventario cíclica. Establézcalo como "sin mes" si… |
|  | `stock_confirmation_type` | varchar | variable | Sí | Tipo de confirmación de existencias |
|  | `stock_move_email_validation` | boolean | 1 B | Sí | Confirmación por correo electrónico de recolección |
|  | `stock_text_confirmation` | boolean | 1 B | Sí | Texto de confirmación de stock |
|  | `horizon_days` | double precision | 8 B | No | Horizonte de reabastecimiento — Configura tu horizonte para activar las reglas de reordenamiento antes y evitar atrasos o actívalas justo a tiempo ("0 días") para evitar… |
|  | `vat_check_vies` | boolean | 1 B | Sí | Verificar números tributarios |
|  | `po_lock` | varchar | variable | Sí | Modificación de la orden de compra — Modificación de la orden de compra que se usa cuando quiere editar una orden de compra después de confirmarla |
|  | `po_double_validation` | varchar | variable | Sí | Niveles de aprobación — Proporcione un mecanismo de doble validación para las compras |
|  | `po_double_validation_amount` | numeric | variable | Sí | Importe para doble validación — Importe mínimo que necesita doble validación |
| FK | `account_stock_journal_id` | integer | 4 B | Sí | Diario de existencias → `account_journal` |
| FK | `account_stock_valuation_id` | integer | 4 B | Sí | Cuenta de valoración de existencias → `account_account` |
| FK | `account_production_wip_account_id` | integer | 4 B | Sí | Cuenta de producción en curso → `account_account` |
| FK | `account_production_wip_overhead_account_id` | integer | 4 B | Sí | Cuenta de gastos generales de producción en curso → `account_account` |
|  | `inventory_period` | varchar | variable | No | Periodo de inventario |
|  | `inventory_valuation` | varchar | variable | Sí | Valoración |
|  | `cost_method` | varchar | variable | No | Método de costo |
| FK | `stock_sms_confirmation_template_id` | integer | 4 B | Sí | Plantilla de SMS → `sms_template` — SMS que se envía al cliente una vez que se entrega la orden. |
|  | `has_received_warning_stock_sms` | boolean | 1 B | Sí | Ha recibido un SMS de advertencia de existencias |
|  | `point_of_sale_update_stock_quantities` | varchar | variable | Sí | Actualizar cantidades en existencias. — Al cierre de la sesión: El sistema crea una recolección para la sesión entera al cerrarla En tiempo real: Cada orden enviada al servidor… |
|  | `point_of_sale_ticket_portal_url_display_mode` | varchar | variable | No | Imprimir — Elija cómo se imprimirá la URL del portal en el recibo. |
|  | `point_of_sale_use_ticket_qr_code` | boolean | 1 B | Sí | Autofacturación — Imprimir información en el recibo para que el cliente pueda acceder a la factura en cualquier momento desde el portal de Odoo. |
|  | `point_of_sale_ticket_unique_code` | boolean | 1 B | Sí | Generar un código en el ticket — Agregar un código de 5 dígitos en el recibo con el que el usuario pueda solicitar una factura desde el portal. |
|  | `days_to_purchase` | double precision | 8 B | Sí | Días para la compra — Días que se necesitan para confirmar una orden de compra, define cuándo se debería de validar la orden de compra |
|  | `quotation_validity_days` | integer | 4 B | Sí | Validez predeterminada de la cotización — Días entre la propuesta de cotización y el vencimiento, 0 días significa que el vencimiento automático está deshabilitado |
| FK | `sale_discount_product_id` | integer | 4 B | Sí | Producto de descuento → `product_product` — Producto predeterminado que se utiliza para los descuentos |
| FK | `downpayment_account_id` | integer | 4 B | Sí | Cuenta de anticipos → `account_account` — Esta cuenta se usará en las facturas de anticipo. |
|  | `sale_onboarding_payment_method` | varchar | variable | Sí | Venta incorporando el método de pago seleccionado |
|  | `portal_confirmation_sign` | boolean | 1 B | Sí | Firma en línea |
|  | `portal_confirmation_pay` | boolean | 1 B | Sí | Pago en línea |
|  | `prepayment_percent` | double precision | 8 B | Sí | Porcentaje de pago anticipado — El porcentaje del importe que se debe pagar para confirmar las cotizaciones. |
|  | `security_lead` | double precision | 8 B | No | Días de seguridad para las ventas — Margen de error en las fechas prometidas a los clientes. Se programará el aprovisionamiento y la entrega de los productos unos días antes… |

### `res_company_users_rel`

**Relación muchos a muchos entre «res.company» y «res.users»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `cid` | integer | 4 B | No | Referencia a res_company |
| PK, FK | `user_id` | integer | 4 B | No | Referencia a res_users |

### `res_config`

**Configuración** · modelo `res.config` · módulo `base` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_config_settings`

**Ajustes de configuración** · modelo `res.config.settings` · módulo `base` · 191 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `web_app_name` | varchar | variable | Sí | Nombre de la aplicación web |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
|  | `module_base_import` | boolean | 1 B | Sí | Permita a los usuarios importar datos desde archivos CSV/XLS/XLSX/ODS |
|  | `module_google_calendar` | boolean | 1 B | Sí | Permita a los usuarios sincronizar su calendario con el calendario de Google |
|  | `module_microsoft_calendar` | boolean | 1 B | Sí | Permita a los usuarios sincronizar su calendario con el calendario de Outlook |
|  | `module_mail_plugin` | boolean | 1 B | Sí | Permita la integración con los complementos de correo |
|  | `module_auth_oauth` | boolean | 1 B | Sí | Use proveedores de autenticación externos (OAuth) |
|  | `module_auth_ldap` | boolean | 1 B | Sí | Autenticación LDAP |
|  | `module_account_inter_company_rules` | boolean | 1 B | Sí | Administrar operaciones entre empresas |
|  | `module_voip` | boolean | 1 B | Sí | Teléfono |
|  | `module_web_unsplash` | boolean | 1 B | Sí | Biblioteca de imágenes de Unsplash |
|  | `module_sms` | boolean | 1 B | Sí | SMS |
|  | `module_partner_autocomplete` | boolean | 1 B | Sí | Autocompletar contacto |
|  | `module_base_geolocalize` | boolean | 1 B | Sí | Geoposicionar |
|  | `module_google_recaptcha` | boolean | 1 B | Sí | reCAPTCHA |
|  | `module_website_cf_turnstile` | boolean | 1 B | Sí | Cloudflare Turnstile |
|  | `module_google_address_autocomplete` | boolean | 1 B | Sí | Autocompletado de direcciones de Google |
|  | `group_multi_currency` | boolean | 1 B | Sí | Multimoneda — Permita trabajar en un entorno multimoneda |
|  | `show_effect` | boolean | 1 B | Sí | Mostrar efecto |
|  | `profiling_enabled_until` | timestamp | 8 B | Sí | El análisis de rendimiento estará habilitado hasta |
|  | `google_places_api_key` | varchar | variable | Sí | Clave API de Google Places |
|  | `minlength` | integer | 4 B | Sí | Longitud mínima de la contraseña — El mínimo de caracteres que deben tener las contraseñas. Usa 0 para deshabilitar esta función. |
|  | `twilio_account_sid` | varchar | variable | Sí | SID de la cuenta |
|  | `twilio_account_token` | varchar | variable | Sí | Token de autenticación de la cuenta |
|  | `sfu_server_url` | varchar | variable | Sí | URL del servidor SFU |
|  | `sfu_server_key` | varchar | variable | Sí | Clave del servidor SFU — Clave con codificación Base64 |
|  | `tenor_api_key` | varchar | variable | Sí | Clave API de Klipy — Agrega una clave API de GIF de Klipy para activar la compatibilidad con los archivos GIF. https://docs.klipy.com/getting-started Si usaba… |
|  | `google_translate_api_key` | varchar | variable | Sí | Clave API de traducción del mensaje — Necesita una clave API de Google válida para habilitar la traducción de mensajes. https://cloud.google.com/translate/docs/setup?hl=es-419 |
|  | `external_email_server_default` | boolean | 1 B | Sí | Utilizar servidores de correo electrónico personalizados |
|  | `module_google_gmail` | boolean | 1 B | Sí | Soporte para la autenticación de Gmail |
|  | `module_microsoft_outlook` | boolean | 1 B | Sí | Soporte para la autenticación de Outlook |
|  | `restrict_template_rendering` | boolean | 1 B | Sí | Restringir la creación de plantillas — Los usuarios aún podrán visualizar las plantillas. Sin embargo, solo los editores de plantillas de correo podrán crear nuevas plantillas… |
|  | `use_twilio_rtc_servers` | boolean | 1 B | Sí | Usar los servidores ICE de Twilio — Si desea utilizar twilio como proveedor de servidores TURN/STUN |
|  | `use_sfu_server` | boolean | 1 B | Sí | Usar servidor SFU — Si quieres configurar un servidor SFU para llamadas grupales grandes. |
|  | `unsplash_access_key` | varchar | variable | Sí | Clave de acceso |
|  | `unsplash_app_id` | varchar | variable | Sí | ID de aplicación |
|  | `group_analytic_accounting` | boolean | 1 B | Sí | Contabilidad analítica |
| FK | `auth_signup_template_user_id` | integer | 4 B | Sí | Plantilla de usuario para los nuevos usuarios creados a través del inicio de sesión → `res_users` |
|  | `auth_signup_uninvited` | varchar | variable | Sí | Cuenta de cliente |
|  | `auth_signup_reset_password` | boolean | 1 B | Sí | Habilite el restablecimiento de contraseñas desde la página de inicio de sesión |
|  | `auth_totp_policy` | varchar | variable | Sí | Política de cumplimiento de la autenticación de dos factores |
|  | `auth_totp_enforce` | boolean | 1 B | Sí | Habilita la autenticación de dos factores |
|  | `google_gmail_client_identifier` | varchar | variable | Sí | ID de cliente de Gmail |
|  | `google_gmail_client_secret` | varchar | variable | Sí | Secreto de cliente de Gmail |
|  | `microsoft_outlook_client_identifier` | varchar | variable | Sí | ID de cliente de Outlook |
|  | `microsoft_outlook_client_secret` | varchar | variable | Sí | Secreto de cliente de Outlook |
|  | `product_weight_in_lbs` | varchar | variable | Sí | Unidad de medida de peso |
|  | `product_volume_volume_in_cubic_feet` | varchar | variable | Sí | Unidad de medida de volumen |
|  | `group_uom` | boolean | 1 B | Sí | Unidades de medida y embalajes |
|  | `group_product_variant` | boolean | 1 B | Sí | Variantes |
|  | `module_loyalty` | boolean | 1 B | Sí | Promociones, cupones, tarjetas de regalo y programas de lealtad |
|  | `group_product_pricelist` | boolean | 1 B | Sí | Listas de precios |
| FK | `digest_id` | integer | 4 B | Sí | Correo electrónico de resumen → `digest_digest` |
|  | `digest_emails` | boolean | 1 B | Sí | Correos electrónicos de resumen |
|  | `chart_template` | varchar | variable | Sí | Plantilla de plan |
|  | `module_account_accountant` | boolean | 1 B | Sí | Contabilidad |
|  | `group_cash_rounding` | boolean | 1 B | Sí | Redondeo de efectivo |
|  | `show_sale_receipts` | boolean | 1 B | Sí | Recibo de venta |
|  | `module_account_budget` | boolean | 1 B | Sí | Gestión de presupuesto |
|  | `module_account_payment` | boolean | 1 B | Sí | Pago de facturas en línea |
|  | `module_account_reports` | boolean | 1 B | Sí | Reportes dinámicos |
|  | `module_account_check_printing` | boolean | 1 B | Sí | Permitir la impresión de cheques y depósitos |
|  | `module_account_batch_payment` | boolean | 1 B | Sí | Utilizar pagos por lotes — Esto le permite agrupar pagos en un solo lote y facilita el proceso de conciliación. -Esto instala el módulo account_batch_payment. |
|  | `module_account_iso20022` | boolean | 1 B | Sí | Transferencia de crédito SEPA / ISO20022 |
|  | `module_account_sepa_direct_debit` | boolean | 1 B | Sí | Utilizar domiciliación bancaria SEPA |
|  | `module_account_bank_statement_import_qif` | boolean | 1 B | Sí | Importar archivos .qif |
|  | `module_currency_rate_live` | boolean | 1 B | Sí | Tasas de cambio automáticas |
|  | `module_account_intrastat` | boolean | 1 B | Sí | Intrastat |
|  | `module_product_margin` | boolean | 1 B | Sí | Permitir márgenes de producto |
|  | `module_account_extract` | boolean | 1 B | Sí | Digitalización de documento |
|  | `module_account_invoice_extract` | boolean | 1 B | Sí | Digitalización de facturas |
|  | `module_account_bank_statement_extract` | boolean | 1 B | Sí | Digitalización de estados de cuenta bancarios |
|  | `module_snailmail_account` | boolean | 1 B | Sí | Correo postal |
|  | `module_account_peppol` | boolean | 1 B | Sí | Facturación PEPPOL |
|  | `use_invoice_terms` | boolean | 1 B | Sí | Términos y condiciones predeterminados |
|  | `group_sale_delivery_address` | boolean | 1 B | Sí | Direcciones del cliente |
|  | `crm_auto_assignment_interval_number` | integer | 4 B | Sí | Repetir cada — Tipo de número de intervalos entre cada ejecución del cron (por ejemplo, cada 2 días o cada 4 días) |
|  | `crm_auto_assignment_action` | varchar | variable | Sí | Acción de autoasignación — La asignación manual permite activar la asignación desde la vista de formulario del equipo con un botón de acción. En automático se confi… |
|  | `crm_auto_assignment_interval_type` | varchar | variable | Sí | Unidad de intervalo de autoasignación — Tipo de intervalo entre cada ejecución del cron (por ejemplo, cada 2 días o cada 2 horas) |
|  | `lead_enrich_auto` | varchar | variable | Sí | Enriquecer el lead en automático |
|  | `predictive_lead_scoring_start_date_str` | varchar | variable | Sí | Fecha de inicio de la puntuación de leads en cadena |
|  | `predictive_lead_scoring_fields_str` | varchar | variable | Sí | Campos de frecuencia de puntuación de leads en cadena |
|  | `group_use_lead` | boolean | 1 B | Sí | Leads |
|  | `group_use_recurring_revenues` | boolean | 1 B | Sí | Ingresos recurrentes |
|  | `is_membership_multi` | boolean | 1 B | Sí | Varios equipos |
|  | `module_partnership` | boolean | 1 B | Sí | Membresía / Asociación |
|  | `crm_use_auto_assignment` | boolean | 1 B | Sí | Asignación por reglas |
|  | `module_crm_iap_mine` | boolean | 1 B | Sí | Genere nuevos leads en función de su país, sector, tamaño, etc. |
|  | `module_crm_iap_enrich` | boolean | 1 B | Sí | Enriquezca automáticamente sus leads con datos de la empresa según su dirección de correo electrónico. |
|  | `module_website_crm_iap_reveal` | boolean | 1 B | Sí | Cree leads/oportunidades desde el tráfico de su sitio web |
|  | `lead_mining_in_pipeline` | boolean | 1 B | Sí | Cree una solicitud de minado de leads directamente desde el flujo de oportunidades. |
|  | `crm_auto_assignment_run_datetime` | timestamp | 8 B | Sí | Siguiente fecha de ejecución de autoasignación |
|  | `module_hr_presence` | boolean | 1 B | Sí | Control de asistencia avanzado |
|  | `module_hr_skills` | boolean | 1 B | Sí | Gestión de habilidades |
|  | `module_hr_timesheet` | boolean | 1 B | Sí | Registros de la tarea |
|  | `group_project_stages` | boolean | 1 B | Sí | Etapas del proyecto |
|  | `barcode_separator` | varchar | variable | Sí | Separador — Caracteres utilizados para separar los datos contenidos en un código de barras agregado (es decir, un código de barras que contiene varia… |
|  | `module_product_expiry` | boolean | 1 B | Sí | Fechas de vencimiento — Haga un seguimiento de las fechas de seguimiento de los números de lote y serie: consúmase antes de, remoción, fin de vida, alerta. Dicha… |
|  | `group_stock_production_lot` | boolean | 1 B | Sí | Números de serie y lote |
|  | `group_stock_lot_print_gs1` | boolean | 1 B | Sí | Imprimir códigos de barra GS1 para números de serie y de lotes |
|  | `group_lot_on_delivery_slip` | boolean | 1 B | Sí | Mostrar números de lote y de serie en recibos de entrega |
|  | `group_stock_tracking_lot` | boolean | 1 B | Sí | Paquetes |
|  | `group_stock_tracking_owner` | boolean | 1 B | Sí | Consigna |
|  | `group_stock_adv_location` | boolean | 1 B | Sí | Rutas multietapa — Agregue y personalice las operaciones de ruta para procesar movimientos de productos en sus almacenes. Por ejemplo, descarga > control de… |
|  | `group_warning_stock` | boolean | 1 B | Sí | Advertencias para existencias |
|  | `group_stock_sign_delivery` | boolean | 1 B | Sí | Firma |
|  | `module_stock_picking_batch` | boolean | 1 B | Sí | Traslados por lote, olas y por preparación de varias órdenes |
|  | `module_stock_barcode` | boolean | 1 B | Sí | Lector de códigos de barras |
|  | `module_stock_barcode_barcodelookup` | boolean | 1 B | Sí | Base de datos de códigos de barras en existencia |
|  | `module_stock_sms` | boolean | 1 B | Sí | Confirmación por SMS |
|  | `module_delivery` | boolean | 1 B | Sí | Métodos de entrega |
|  | `module_delivery_dhl` | boolean | 1 B | Sí | Conector de DHL Express |
|  | `module_delivery_fedex_rest` | boolean | 1 B | Sí | Conector de FedEx |
|  | `module_delivery_ups_rest` | boolean | 1 B | Sí | Conector de UPS |
|  | `module_delivery_usps_rest` | boolean | 1 B | Sí | Conector de USPS |
|  | `module_delivery_bpost` | boolean | 1 B | Sí | Conector de bpost |
|  | `module_delivery_easypost` | boolean | 1 B | Sí | Conector de Easypost |
|  | `module_delivery_sendcloud` | boolean | 1 B | Sí | Conector de Sendcloud |
|  | `module_delivery_shiprocket` | boolean | 1 B | Sí | Conector de Shiprocket |
|  | `module_delivery_starshipit` | boolean | 1 B | Sí | Conector de Starshipit |
|  | `module_delivery_envia` | boolean | 1 B | Sí | Conector de Envia.com |
|  | `module_quality_control` | boolean | 1 B | Sí | Calidad |
|  | `module_quality_control_worksheet` | boolean | 1 B | Sí | Hoja de trabajo de calidad |
|  | `group_stock_multi_locations` | boolean | 1 B | Sí | Ubicaciones de almacenamiento — Almacene productos en ubicaciones específicas de su almacén (por ejemplo, contenedores, bastidores) y lleve un seguimiento del inventario… |
|  | `group_stock_reception_report` | boolean | 1 B | Sí | Reporte de recepción |
|  | `module_stock_dropshipping` | boolean | 1 B | Sí | Triangulación |
|  | `module_stock_fleet` | boolean | 1 B | Sí | Sistema de gestión de despacho |
|  | `pay_invoices_online` | boolean | 1 B | Sí | Pagar facturas en línea |
|  | `group_mrp_byproducts` | boolean | 1 B | Sí | Subproductos |
|  | `module_mrp_mps` | boolean | 1 B | Sí | Programa maestro de producción |
|  | `module_mrp_plm` | boolean | 1 B | Sí | Gestión del ciclo de vida del producto (PLM) |
|  | `module_mrp_subcontracting` | boolean | 1 B | Sí | Subcontratación |
|  | `group_mrp_routings` | boolean | 1 B | Sí | Órdenes de trabajo de planeación de recursos de fabricación |
|  | `group_unlocked_by_default` | boolean | 1 B | Sí | Desbloquear órdenes de fabricación |
|  | `group_mrp_reception_report` | boolean | 1 B | Sí | Reporte de asignación para órdenes de fabricación |
|  | `group_mrp_workorder_dependencies` | boolean | 1 B | Sí | Dependencias de la orden de trabajo |
|  | `group_expiry_date_on_delivery_slip` | boolean | 1 B | Sí | Mostrar la fecha de caducidad en los recibos de entrega |
|  | `lock_confirmed_po` | boolean | 1 B | Sí | Bloquear órdenes confirmadas |
|  | `po_order_approval` | boolean | 1 B | Sí | Aprobación de la orden de compra |
|  | `group_warning_purchase` | boolean | 1 B | Sí | Advertencias de compra |
|  | `module_account_3way_match` | boolean | 1 B | Sí | Conciliación de tres vías: compras, recepciones y facturas. |
|  | `module_purchase_requisition` | boolean | 1 B | Sí | Contratos de compra |
|  | `module_purchase_product_matrix` | boolean | 1 B | Sí | Entrada de tabla de compra |
|  | `group_send_reminder` | boolean | 1 B | Sí | Recordatorio de entrega — Permita el envío automático de correos electrónicos para recordarle la fecha de recepción a su proveedor |
|  | `module_stock_landed_costs` | boolean | 1 B | Sí | Costos en destino — Afecte los costos en destino en las operaciones de recepción y divídalos entre productos para actualizar su precio de costo. |
|  | `group_lot_on_invoice` | boolean | 1 B | Sí | Mostrar números de lote y de serie en las facturas |
| FK | `pos_config_id` | integer | 4 B | Sí | Punto de venta → `pos_config` |
| FK | `pos_default_fiscal_position_id` | integer | 4 B | Sí | Posición fiscal predeterminada → `account_fiscal_position` |
| FK | `pos_pricelist_id` | integer | 4 B | Sí | Lista de precios predeterminada → `product_pricelist` |
| FK | `pos_tip_product_id` | integer | 4 B | Sí | Producto de propina → `product_product` |
|  | `pos_receipt_footer` | text | variable | Sí | Pie del recibo |
|  | `pos_receipt_header` | text | variable | Sí | Encabezado del recibo |
|  | `module_pos_adyen` | boolean | 1 B | Sí | Terminal de pago Adyen — Adyen procesa las transacciones. Establezca sus credenciales de Adyen en el método de pago relacionado. |
|  | `module_pos_stripe` | boolean | 1 B | Sí | Terminal de pago de Stripe — Stripe procesa las transacciones. Establezca sus credenciales de Stripe en el método de pago relacionado. |
|  | `module_pos_viva_com` | boolean | 1 B | Sí | Terminal de pago de Viva.com — Viva.com procesa las transacciones en la terminal o al acercar la tarjeta o el dispositivo para pagar. |
|  | `module_pos_razorpay` | boolean | 1 B | Sí | Terminal de pago de Razorpay — Razorpay procesa las transacciones. Establezca sus credenciales de Razorpay en el método de pago relacionado. |
|  | `module_pos_mercado_pago` | boolean | 1 B | Sí | Terminal de pago de Mercado Pago — Mercado Pago procesa las transacciones. Establezca sus credenciales de Mercado Pago en el método de pago relacionado. |
|  | `module_pos_pine_labs` | boolean | 1 B | Sí | Terminal de pagos de Pine Labs — Pine Labs procesa las transacciones. Establece tus credenciales de Pine Labs en el método de pago relacionado. |
|  | `module_pos_qfpay` | boolean | 1 B | Sí | Terminal de pago QFPay — QFPay procesa las transacciones. Configura tus credenciales de QFPay en el método de pago asociado. |
|  | `module_pos_pricer` | boolean | 1 B | Sí | Etiquetas electrónicas de Pricer — Muestre los precios de sus productos a través de etiquetas de precio electrónicas |
|  | `is_kiosk_mode` | boolean | 1 B | Sí | ¿Es el modo quiosco? |
|  | `pos_is_order_printer` | boolean | 1 B | Sí | Es una impresora de pedidos del PdV |
|  | `pos_iface_cashdrawer` | boolean | 1 B | Sí | Caja registradora |
|  | `pos_iface_electronic_scale` | boolean | 1 B | Sí | Báscula electrónica |
|  | `pos_iface_print_via_proxy` | boolean | 1 B | Sí | Imprimir vía proxy |
|  | `pos_iface_scan_via_proxy` | boolean | 1 B | Sí | Escanear vía proxy |
|  | `group_pos_preset` | boolean | 1 B | Sí | Ajustes preestablecidos — Ocultar o mostrar el menú de valores preestablecidos en la configuración de Punto de venta. |
|  | `is_installed_sale` | boolean | 1 B | Sí | ¿El módulo Ventas está instalado? |
| FK | `invoice_mail_template_id` | integer | 4 B | Sí | Plantilla de correo electrónico → `mail_template` — Correo electrónico enviado al cliente una vez que esté disponible la factura. |
|  | `default_invoice_policy` | varchar | variable | Sí | Política de facturación |
|  | `group_auto_done_setting` | boolean | 1 B | Sí | Bloquear órdenes confirmadas |
|  | `group_discount_per_so_line` | boolean | 1 B | Sí | Descuentos |
|  | `group_proforma_sales` | boolean | 1 B | Sí | Factura proforma — Le permite enviar una factura proforma. |
|  | `group_warning_sale` | boolean | 1 B | Sí | Advertencias de órdenes de venta |
|  | `automatic_invoice` | boolean | 1 B | Sí | Factura automática — La factura se genera de forma automática y está disponible en el portal del cliente cuando el proveedor de pago confirma la transacción.… |
|  | `module_product_email_template` | boolean | 1 B | Sí | Correo electrónico específico |
|  | `module_sale_amazon` | boolean | 1 B | Sí | Sincronización con Amazon |
|  | `module_sale_commission` | boolean | 1 B | Sí | Comisiones |
|  | `module_sale_gelato` | boolean | 1 B | Sí | Gelato |
|  | `module_sale_loyalty` | boolean | 1 B | Sí | Cupones y lealtad |
|  | `module_sale_margin` | boolean | 1 B | Sí | Márgenes |
|  | `module_sale_pdf_quote_builder` | boolean | 1 B | Sí | Creador de cotizaciones en PDF |
|  | `module_sale_product_matrix` | boolean | 1 B | Sí | Entrada en la tabla de ventas |
|  | `module_sale_shopee` | boolean | 1 B | Sí | Sincronización con Shopee |
|  | `default_picking_policy` | varchar | variable | No | Política de recolección |
|  | `use_security_lead` | boolean | 1 B | Sí | Plazo de seguridad para ventas — Margen de error en la fecha de entrega que se le prometió al cliente. Se programará la entrega de los productos unos días antes de la fec… |

### `res_country`

**País** · modelo `res.country` · módulo `base` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `address_view_id` | integer | 4 B | Sí | Ingresar vista → `ir_ui_view` — Use este campo si quiere sustituir la forma habitual de codificar una dirección completa. Tenga en cuenta que el campo address_format se… |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
|  | `phone_code` | integer | 4 B | Sí | Código de llamada del país |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | 2 | No | Código del país — El código ISO del país en dos caracteres. Puedes utilizar este campo para realizar una búsqueda rápida. |
|  | `name_position` | varchar | variable | Sí | Posición del nombre del cliente — Determina dónde se debe colocar el nombre del cliente/empresa; es decir, antes o después de la dirección. |
|  | `name` | jsonb | variable | No | Nombre del país |
|  | `vat_label` | jsonb | variable | Sí | Etiqueta IVA — Use este campo si desea cambiar la etiqueta del IVA. |
|  | `address_format` | text | variable | Sí | Diseño en los reportes — Formato de visualización a utilizar en las direcciones pertenecientes a este país. Puede utilizar un patrón de cadena de estilo de Python… |
|  | `state_required` | boolean | 1 B | Sí | Estado obligatorio |
|  | `zip_required` | boolean | 1 B | Sí | Código postal obligatorio |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `enforce_cities` | boolean | 1 B | Sí | Establecer ciudades — Selecciona esta casilla para asegurarte de que cada dirección creada en ese país tenga una "Ciudad" elegida en la lista de ciudades del p… |

### `res_country_group`

**Grupo del país** · modelo `res.country.group` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | Sí | Código |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_country_group_res_country_state_rel`

**Relación muchos a muchos entre «res.country.group» y «res.country.state»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `res_country_group_id` | integer | 4 B | No | Referencia a res_country_group |
| PK, FK | `res_country_state_id` | integer | 4 B | No | Referencia a res_country_state |

### `res_country_res_country_group_rel`

**Relación muchos a muchos entre «res.country» y «res.country.group»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `res_country_id` | integer | 4 B | No | Referencia a res_country |
| PK, FK | `res_country_group_id` | integer | 4 B | No | Referencia a res_country_group |

### `res_country_state`

**Estado** · modelo `res.country.state` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `country_id` | integer | 4 B | No | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de estado — División administrativa de un país. Por ejemplo: entidad federativa, provincia, ayuntamiento |
|  | `code` | varchar | variable | No | Código de estado — El código del estado. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_currency`

**Moneda** · modelo `res.currency` · módulo `base` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `name` | varchar | variable | No | Moneda — Código de divisa (ISO 4217) |
|  | `symbol` | varchar | variable | No | Símbolo — Símbolo de la moneda, se utiliza al imprimir importes. |
|  | `iso_numeric` | integer | 4 B | Sí | Código numérico de la moneda. — Código numérico de divisa (ISO 4217). |
|  | `decimal_places` | integer | 4 B | Sí | Dígitos decimales — Los lugares decimales que se toman en cuenta para las operaciones en cantidades de esta moneda. Se determina por el factor de redondeo. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `full_name` | varchar | variable | Sí | Nombre |
|  | `position` | varchar | variable | Sí | Posición del símbolo — Determina si el símbolo de la moneda debe estar antes o después del importe. |
|  | `currency_unit_label` | jsonb | variable | Sí | Unidad de moneda |
|  | `currency_subunit_label` | jsonb | variable | Sí | Subunidad de moneda |
|  | `rounding` | numeric | variable | Sí | Factor de redondeo — Los importes en esta moneda se redondean al múltiplo más cercano del factor de redondeo. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_currency_rate`

**Tasa de cambio** · modelo `res.currency.rate` · módulo `base` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | date | 4 B | No | Fecha |
|  | `rate` | numeric | variable | Sí | Tasa técnica — La tasa de la divisa a la divisa de la tasa 1 |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_device_log`

**Registro del dispositivo** · modelo `res.device.log` · módulo `base` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `session_identifier` | varchar | variable | No | Identificador de la sesión |
|  | `platform` | varchar | variable | Sí | Plataforma |
|  | `browser` | varchar | variable | Sí | Navegador |
|  | `ip_address` | varchar | variable | Sí | Dirección IP |
|  | `country` | varchar | variable | Sí | País |
|  | `city` | varchar | variable | Sí | Ciudad |
|  | `device_type` | varchar | variable | Sí | Tipo de dispositivo |
|  | `revoked` | boolean | 1 B | Sí | Revocado — Si Verdadero, el archivo de la sesión correspondiente a este dispositivo ya no existe en el archivo del sistema. |
|  | `first_activity` | timestamp | 8 B | Sí | Primera actividad |
|  | `last_activity` | timestamp | 8 B | Sí | Última actividad |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_groups_implied_rel`

**Relación muchos a muchos entre «res.groups» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `gid` | integer | 4 B | No | Referencia a res_groups |
| PK, FK | `hid` | integer | 4 B | No | Referencia a res_groups |

### `res_groups_privilege`

**Privilegios** · modelo `res.groups.privilege` · módulo `base` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `category_id` | integer | 4 B | Sí | Categoría → `ir_module_category` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `placeholder` | varchar | variable | Sí | Marcador de posición — El texto que se mostrará como marcador de posición en el campo de selección del formulario de usuario |
|  | `name` | jsonb | variable | No | Nombre |
|  | `description` | text | variable | Sí | Descripción |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_groups_report_rel`

**Relación muchos a muchos entre «ir.actions.report» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `uid` | integer | 4 B | No | Referencia a ir_act_report_xml |
| PK, FK | `gid` | integer | 4 B | No | Referencia a res_groups |

### `res_groups_users_rel`

**Relación muchos a muchos entre «res.groups» y «res.users»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `gid` | integer | 4 B | No | Referencia a res_groups |
| PK, FK | `uid` | integer | 4 B | No | Referencia a res_users |

### `res_lang`

**Idiomas** · modelo `res.lang` · módulo `base` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `code` | varchar | variable | No | Código de idioma — Este campo se utiliza para establecer y obtener la configuración regional del usuario |
|  | `iso_code` | varchar | variable | Sí | Código ISO — Este código ISO es el nombre de los archivos .po que se utilizan para las traducciones |
|  | `url_code` | varchar | variable | No | Código URL — El código de idioma que aparece en la URL |
|  | `direction` | varchar | variable | No | Dirección |
|  | `date_format` | varchar | variable | No | Formato de fecha |
|  | `time_format` | varchar | variable | No | Formato de hora |
|  | `week_start` | varchar | variable | No | Primer día de la semana |
|  | `grouping` | varchar | variable | No | Formato del separador — El formato internacional representará 123456789 como 123,456,789.00 y el formato indio representará 123456789 como 12,34,56,789.00 |
|  | `decimal_point` | varchar | variable | No | Separador decimal |
|  | `thousands_sep` | varchar | variable | Sí | Separador de miles |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_lang_install_rel`

**Relación muchos a muchos entre «base.language.install» y «res.lang»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `language_wizard_id` | integer | 4 B | No | Referencia a base_language_install |
| PK, FK | `lang_id` | integer | 4 B | No | Referencia a res_lang |

### `res_partner_bank`

**Cuentas bancarias** · modelo `res.partner.bank` · módulo `base` · 19 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | No | Titular de la cuenta → `res_partner` |
| FK | `bank_id` | integer | 4 B | Sí | Banco → `res_bank` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `acc_number` | varchar | variable | No | Número de cuenta |
|  | `clearing_number` | varchar | variable | Sí | Número de compensación |
|  | `sanitized_acc_number` | varchar | variable | Sí | Número de cuenta depurado |
|  | `acc_holder_name` | varchar | variable | Sí | Nombre del titular de la cuenta — Nombre del titular de la cuenta, en caso de que sea diferente al nombre del titular de la cuenta |
|  | `note` | text | variable | Sí | Notas |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `allow_out_payment` | boolean | 1 B | Sí | Enviar dinero — Enviar facturas falsas con un número de cuenta fraudulento es una práctica común de phishing. Para protegerte, es importante que siempre… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `has_iban_warning` | boolean | 1 B | Sí | Tiene advertencia IBAN — El campo técnico se usa para mostrar una advertencia si el país IBAN es diferente al IBAN necesario |
|  | `has_money_transfer_warning` | boolean | 1 B | Sí | Tiene advertencia de transferencia de dinero — El campo técnico usado para mostrar una advertencia si la cuenta es una cuenta de servicio de transferencia. |

### `res_partner_category`

**Etiquetas del contacto** · modelo `res.partner.category` · módulo `base` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `parent_id` | integer | 4 B | Sí | Categoría → `res_partner_category` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Activo — El campo activo le permite ocultar la categoría sin tener que eliminarla. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_partner_industry`

**Industria** · modelo `res.partner.industry` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | Sí | Nombre |
|  | `full_name` | jsonb | variable | Sí | Nombre completo |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_partner_res_partner_category_rel`

**Relación muchos a muchos entre «res.partner» y «res.partner.category»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `category_id` | integer | 4 B | No | Referencia a res_partner_category |
| PK, FK | `partner_id` | integer | 4 B | No | Referencia a res_partner |

### `res_users_apikeys`

**Claves API de los usuarios** · modelo `res.users.apikeys` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `name` | varchar | variable | No | Descripción |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
|  | `scope` | varchar | variable | Sí | Alcance |
|  | `expiration_date` | timestamp | 8 B | Sí | Fecha de vencimiento |
|  | `index` | varchar | 8 | Sí | — |
|  | `key` | varchar | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |

### `res_users_apikeys_description`

**Descripción de la clave API** · modelo `res.users.apikeys.description` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Descripción |
|  | `duration` | varchar | variable | No | Duración |
|  | `expiration_date` | timestamp | 8 B | Sí | Fecha de vencimiento |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_users_deletion`

**Solicitud de eliminación de usuario** · modelo `res.users.deletion` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
|  | `user_id_int` | integer | 4 B | Sí | ID del usuario |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `state` | varchar | variable | No | Estado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_users_identitycheck`

**Asistente de verificación de contraseñas** · modelo `res.users.identitycheck` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `request` | varchar | variable | Sí | Solicitud |
|  | `auth_method` | varchar | variable | Sí | Método de autenticación |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_users_log`

**Registro de usuarios** · modelo `res.users.log` · módulo `base` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_users_settings`

**Ajustes de usuario** · modelo `res.users.settings` · módulo `base` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `voice_active_duration` | integer | 4 B | Sí | Duración de la actividad vocal en ms — Cuánto tiempo permanecerá activa la emisión de audio tras superar el límite de volumen |
|  | `push_to_talk_key` | varchar | variable | Sí | Atajo de la función pulsar para hablar — Cadena con formato que representa una tecla con modificadores que siguen este patrón: shift.ctrl.alt.key, por ejemplo: truthy.1.true.b |
|  | `channel_notifications` | varchar | variable | Sí | Notificaciones del canal — Este ajuste solo se aplicará a los canales. A las menciones solo si no se especifica. |
|  | `is_discuss_sidebar_category_channel_open` | boolean | 1 B | Sí | ¿Está abierto el canal de la categoría de la barra lateral de conversaciones? |
|  | `is_discuss_sidebar_category_chat_open` | boolean | 1 B | Sí | ¿Está abierto el chat de la categoría de la barra lateral de conversaciones? |
|  | `use_push_to_talk` | boolean | 1 B | Sí | Usar la función pulsar para hablar |
|  | `calendar_default_privacy` | varchar | variable | No | Privacidad predeterminada del calendario — Ajuste de privacidad predeterminado para la que los eventos del calendario serán visibles. |

### `reset_view_arch_wizard`

**Asistente para restablecer la arquitectura de la vista** · modelo `reset.view.arch.wizard` · módulo `base` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `view_id` | integer | 4 B | Sí | Vista → `ir_ui_view` |
| FK | `compare_view_id` | integer | 4 B | Sí | Comparar la vista → `ir_ui_view` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reset_mode` | varchar | variable | No | Restablecer modo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `rule_group_rel`

**Relación muchos a muchos entre «ir.rule» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `base` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `rule_group_id` | integer | 4 B | No | Referencia a ir_rule |
| PK, FK | `group_id` | integer | 4 B | No | Referencia a res_groups |

### `server_action_history_wizard`

**Asistente de historial de acciones del servidor** · modelo `server.action.history.wizard` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `action_id` | integer | 4 B | Sí | Acción → `ir_act_server` |
| FK | `revision` | integer | 4 B | No | Revisión → `ir_actions_server_history` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `wizard_ir_model_menu_create`

**Asistente para crear menú** · modelo `wizard.ir.model.menu.create` · módulo `base` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `menu_id` | integer | 4 B | No | Menú principal → `ir_ui_menu` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre del menú |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `base_address_extended`

### `res_city`

**Ciudad** · modelo `res.city` · módulo `base_address_extended` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `country_id` | integer | 4 B | No | País → `res_country` |
| FK | `state_id` | integer | 4 B | Sí | Estado → `res_country_state` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `zipcode` | varchar | variable | Sí | Código postal |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `l10n_pe_code` | varchar | variable | Sí | Código — Este código ayudará con la identificación de cada ciudad en Perú. |

## Módulo `base_import`

### `base_import_import`

**Importación base** · modelo `base_import.import` · módulo `base_import` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | Sí | Modelo |
|  | `file_name` | varchar | variable | Sí | Nombre del archivo |
|  | `file_type` | varchar | variable | Sí | Tipo del archivo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `file` | bytea | variable | Sí | Archivo — Archivo a comprobar o importar, binario sin procesar (no base64) |

### `base_import_mapping`

**Mapeo de la importación de base** · modelo `base_import.mapping` · módulo `base_import` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | Sí | Modelo res |
|  | `column_name` | varchar | variable | Sí | Nombre de la columna |
|  | `field_name` | varchar | variable | Sí | Nombre del campo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `base_import_module`

### `base_import_module`

**Importar módulo** · modelo `base.import.module` · módulo `base_import_module` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `state` | varchar | variable | Sí | Estado |
|  | `import_message` | text | variable | Sí | Importar mensaje |
|  | `modules_dependencies` | text | variable | Sí | Dependencias del módulo |
|  | `force` | boolean | 1 B | Sí | Forzar inicio — Forzar el modo de inicio incluso si está instalado (actualizará los registros de `noupdate='1'`) |
|  | `with_demo` | boolean | 1 B | Sí | Importar datos de demostración del módulo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `module_file` | bytea | variable | No | Archivo .ZIP del módulo |

## Módulo `base_install_request`

### `base_module_install_request`

**Solicitud de activación de módulo** · modelo `base.module.install.request` · módulo `base_install_request` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `module_id` | integer | 4 B | No | Módulo → `ir_module_module` |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `body_html` | text | variable | Sí | Contenido |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `base_module_install_review`

**Revisión de la activación del módulo** · modelo `base.module.install.review` · módulo `base_install_request` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `module_id` | integer | 4 B | No | Módulo → `ir_module_module` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `bus`

### `bus_bus`

**Bus de comunicación** · modelo `bus.bus` · módulo `bus` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `channel` | varchar | variable | Sí | Canal |
|  | `message` | varchar | variable | Sí | Mensaje |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `calendar`

### `calendar_alarm`

**Alerta de evento** · modelo `calendar.alarm` · módulo `calendar` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `duration` | integer | 4 B | No | Recordar antes de |
|  | `duration_minutes` | integer | 4 B | Sí | Duración en minutos |
| FK | `mail_template_id` | integer | 4 B | Sí | Plantilla de correo electrónico → `mail_template` — Plantilla que se utiliza para visualizar el contenido del correo de recordatorio. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `alarm_type` | varchar | variable | No | Tipo |
|  | `interval` | varchar | variable | No | Unidad |
|  | `name` | jsonb | variable | No | Nombre |
|  | `body` | text | variable | Sí | Mensaje adicional — Mensaje adicional que se enviará con la notificación para el recordatorio |
|  | `notify_responsible` | boolean | 1 B | Sí | Notificar al responsable |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `sms_template_id` | integer | 4 B | Sí | Plantilla de SMS → `sms_template` — Plantilla que se utiliza para visualizar el contenido de los recordatorios por SMS. |

### `calendar_alarm_calendar_event_rel`

**Relación muchos a muchos entre «calendar.event» y «calendar.alarm»** · tabla intermedia, sin modelo propio · módulo `calendar` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `calendar_event_id` | integer | 4 B | No | Referencia a calendar_event |
| PK, FK | `calendar_alarm_id` | integer | 4 B | No | Referencia a calendar_alarm |

### `calendar_attendee`

**Información en el calendario de los asistentes** · modelo `calendar.attendee` · módulo `calendar` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `event_id` | integer | 4 B | No | Reunión vinculada → `calendar_event` |
| FK | `partner_id` | integer | 4 B | No | Asistente → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `common_name` | varchar | variable | Sí | Nombre común |
|  | `access_token` | varchar | variable | Sí | Token de invitación |
|  | `state` | varchar | variable | Sí | Estado |
|  | `availability` | varchar | variable | Sí | Disponible/Ocupado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `calendar_event`

**Evento del calendario** · modelo `calendar.event` · módulo `calendar` · 29 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Organizador → `res_users` |
| FK | `videocall_channel_id` | integer | 4 B | Sí | Canal de conversaciones → `discuss_channel` |
|  | `res_id` | integer | 4 B | Sí | ID del documento |
| FK | `res_model_id` | integer | 4 B | Sí | Modelo de documento → `ir_model` |
| FK | `recurrence_id` | integer | 4 B | Sí | Regla de recurrencia → `calendar_recurrence` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Asunto de la reunión |
|  | `location` | varchar | variable | Sí | Ubicación |
|  | `videocall_location` | varchar | variable | Sí | URL de la reunión |
|  | `access_token` | varchar | variable | Sí | Token de invitación |
|  | `privacy` | varchar | variable | Sí | Privacidad — Gente que podrá ver este evento. |
|  | `show_as` | varchar | variable | No | Mostrar como — Si el horario aparece como "ocupado", puede que otras personas puedan ver la información completa del evento o solo se mostrará el texto… |
|  | `res_model` | varchar | variable | Sí | Nombre del modelo del documento |
|  | `start_date` | date | 4 B | Sí | Fecha de inicio |
|  | `stop_date` | date | 4 B | Sí | Fecha de finalización |
|  | `description` | text | variable | Sí | Descripción — Cuando la sincronización con un calendario externo está activa, esta descripción se sincroniza with the one of the associated meeting in… |
|  | `notes` | text | variable | Sí | Notas |
|  | `active` | boolean | 1 B | Sí | Activo — Si el campo activo se establece como False, le permitirá ocultar la notificación de aviso del evento sin eliminarlo. |
|  | `allday` | boolean | 1 B | Sí | Todo el día |
|  | `recurrency` | boolean | 1 B | Sí | Recurrente |
|  | `follow_recurrence` | boolean | 1 B | Sí | Seguir la recurrencia |
|  | `start` | timestamp | 8 B | No | Iniciar — Fecha de inicio del evento. Los eventos que duran todo el día no incluyen la hora. |
|  | `stop` | timestamp | 8 B | No | Detener — Fecha de finalización del evento, no muestra la hora para eventos que duran todo el día. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `duration` | double precision | 8 B | Sí | Duración |
| FK | `opportunity_id` | integer | 4 B | Sí | Oportunidad → `crm_lead` |

### `calendar_event_res_partner_rel`

**Relación muchos a muchos entre «calendar.event» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `calendar` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |
| PK, FK | `calendar_event_id` | integer | 4 B | No | Referencia a calendar_event |

### `calendar_event_type`

**Tipo de reunión** · modelo `calendar.event.type` · módulo `calendar` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `calendar_filters`

**Filtros de calendario** · modelo `calendar.filters` · módulo `calendar` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | No | Yo → `res_users` |
| FK | `partner_id` | integer | 4 B | No | Empleado → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `partner_checked` | boolean | 1 B | Sí | Comprobado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `calendar_popover_delete_wizard`

**Asistente para eliminar ventana emergente del calendario** · modelo `calendar.popover.delete.wizard` · módulo `calendar` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `template_id` | integer | 4 B | Sí | Plantilla de correo electrónico → `mail_template` |
| FK | `calendar_event_id` | integer | 4 B | Sí | Evento del calendario → `calendar_event` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lang` | varchar | variable | Sí | Idioma — Idioma de traducción opcional (código ISO) a seleccionar al enviar un correo. Si no lo defines, el sistema usará el idioma principal del… |
|  | `subject` | varchar | variable | Sí | Asunto |
|  | `delete` | varchar | variable | Sí | Eliminar |
|  | `body` | text | variable | Sí | Contenidos |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `calendar_provider_config`

**Asistente de configuración de proveedor de calendario** · modelo `calendar.provider.config` · módulo `calendar` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `external_calendar_provider` | varchar | variable | Sí | Elija un calendario externo para configurar |
|  | `cal_client_id` | varchar | variable | Sí | Client_id de Google |
|  | `cal_client_secret` | varchar | variable | Sí | Client_key de Google |
|  | `microsoft_outlook_client_identifier` | varchar | variable | Sí | ID de cliente de Outlook |
|  | `microsoft_outlook_client_secret` | varchar | variable | Sí | Secreto de cliente de Outlook |
|  | `cal_sync_paused` | boolean | 1 B | Sí | La sincronización con Google está en pausa |
|  | `microsoft_outlook_sync_paused` | boolean | 1 B | Sí | La sincronización con Outlook está en pausa |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `calendar_recurrence`

**Regla de recurrencia de evento** · modelo `calendar.recurrence` · módulo `calendar` · 26 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `base_event_id` | integer | 4 B | Sí | Evento base → `calendar_event` |
|  | `interval` | integer | 4 B | Sí | Intervalo |
|  | `count` | integer | 4 B | Sí | Número |
|  | `day` | integer | 4 B | Sí | Día |
| FK | `trigger_id` | integer | 4 B | Sí | Activar → `ir_cron_trigger` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `event_tz` | varchar | variable | Sí | Zona horaria |
|  | `rrule` | varchar | variable | Sí | Rrule |
|  | `rrule_type` | varchar | variable | Sí | Tipo de rrule |
|  | `end_type` | varchar | variable | Sí | Tipo de finalización |
|  | `month_by` | varchar | variable | Sí | Mes por |
|  | `weekday` | varchar | variable | Sí | Día de la semana |
|  | `byday` | varchar | variable | Sí | Por día |
|  | `until` | date | 4 B | Sí | Repetir hasta |
|  | `mon` | boolean | 1 B | Sí | lun. |
|  | `tue` | boolean | 1 B | Sí | mar |
|  | `wed` | boolean | 1 B | Sí | mié |
|  | `thu` | boolean | 1 B | Sí | jue |
|  | `fri` | boolean | 1 B | Sí | vie. |
|  | `sat` | boolean | 1 B | Sí | sáb |
|  | `sun` | boolean | 1 B | Sí | dom |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `meeting_category_rel`

**Relación muchos a muchos entre «calendar.event» y «calendar.event.type»** · tabla intermedia, sin modelo propio · módulo `calendar` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `event_id` | integer | 4 B | No | Referencia a calendar_event |
| PK, FK | `type_id` | integer | 4 B | No | Referencia a calendar_event_type |

## Módulo `crm`

### `crm_convert_lead_mass_lead_rel`

**Relación muchos a muchos entre «crm.lead2opportunity.partner.mass» y «crm.lead»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_lead2opportunity_partner_mass_id` | integer | 4 B | No | Referencia a crm_lead2opportunity_partner_mass |
| PK, FK | `crm_lead_id` | integer | 4 B | No | Referencia a crm_lead |

### `crm_lead2opportunity_partner`

**Convertir lead en oportunidad (no en masa)** · modelo `crm.lead2opportunity.partner` · módulo `crm` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `lead_id` | integer | 4 B | No | Lead asociado → `crm_lead` |
| FK | `commercial_partner_id` | integer | 4 B | Sí | Empresa → `res_partner` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `user_id` | integer | 4 B | Sí | Vendedor → `res_users` |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Acciones de conversión |
|  | `action` | varchar | variable | No | Cliente relacionado |
|  | `force_assignment` | boolean | 1 B | Sí | Forzar asignación — Si está seleccionado, obliga al vendedor a mantenerse actualizado sobre las oportunidades actualizadas, incluso si ya están configuradas. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_lead2opportunity_partner_mass`

**Convertir lead en oportunidad (en masa)** · modelo `crm.lead2opportunity.partner.mass` · módulo `crm` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `lead_id` | integer | 4 B | Sí | Lead asociado → `crm_lead` |
| FK | `commercial_partner_id` | integer | 4 B | Sí | Empresa → `res_partner` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `user_id` | integer | 4 B | Sí | Vendedor → `res_users` |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Acciones de conversión |
|  | `action` | varchar | variable | No | Cliente relacionado |
|  | `force_assignment` | boolean | 1 B | Sí | Forzar asignación — Si está seleccionado, obliga al vendedor a mantenerse actualizado sobre las oportunidades actualizadas, incluso si ya están configuradas. |
|  | `deduplicate` | boolean | 1 B | Sí | Aplicar la deduplicación — Combinar con leads/oportunidades existentes de cada contacto |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_lead2opportunity_partner_mass_res_users_rel`

**Relación muchos a muchos entre «crm.lead2opportunity.partner.mass» y «res.users»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_lead2opportunity_partner_mass_id` | integer | 4 B | No | Referencia a crm_lead2opportunity_partner_mass |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `crm_lead_crm_lead2opportunity_partner_mass_rel`

**Relación muchos a muchos entre «crm.lead2opportunity.partner.mass» y «crm.lead»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_lead2opportunity_partner_mass_id` | integer | 4 B | No | Referencia a crm_lead2opportunity_partner_mass |
| PK, FK | `crm_lead_id` | integer | 4 B | No | Referencia a crm_lead |

### `crm_lead_crm_lead2opportunity_partner_rel`

**Relación muchos a muchos entre «crm.lead2opportunity.partner» y «crm.lead»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_lead2opportunity_partner_id` | integer | 4 B | No | Referencia a crm_lead2opportunity_partner |
| PK, FK | `crm_lead_id` | integer | 4 B | No | Referencia a crm_lead |

### `crm_lead_crm_lead_lost_rel`

**Relación muchos a muchos entre «crm.lead.lost» y «crm.lead»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_lead_lost_id` | integer | 4 B | No | Referencia a crm_lead_lost |
| PK, FK | `crm_lead_id` | integer | 4 B | No | Referencia a crm_lead |

### `crm_lead_lost`

**Obtener motivo de la pérdida** · modelo `crm.lead.lost` · módulo `crm` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `lost_reason_id` | integer | 4 B | Sí | Motivo de pérdida → `crm_lost_reason` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lost_feedback` | text | variable | Sí | Nota de cierre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_lead_pls_update`

**Actualizar las probabilidades** · modelo `crm.lead.pls.update` · módulo `crm` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `pls_start_date` | date | 4 B | No | Fecha de inicio de la puntuación predictiva de leads |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_lead_pls_update_crm_lead_scoring_frequency_field_rel`

**Relación muchos a muchos entre «crm.lead.pls.update» y «crm.lead.scoring.frequency.field»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_lead_pls_update_id` | integer | 4 B | No | Referencia a crm_lead_pls_update |
| PK, FK | `crm_lead_scoring_frequency_field_id` | integer | 4 B | No | Referencia a crm_lead_scoring_frequency_field |

### `crm_lead_scoring_frequency`

**Frecuencia de puntuación de leads** · modelo `crm.lead.scoring.frequency` · módulo `crm` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `variable` | varchar | variable | Sí | Variable |
|  | `value` | varchar | variable | Sí | Valor |
|  | `won_count` | numeric | variable | Sí | Número de ganados |
|  | `lost_count` | numeric | variable | Sí | Número de pérdidas |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_lead_scoring_frequency_field`

**Campos que se pueden utilizar para predecir la puntuación de los leads** · modelo `crm.lead.scoring.frequency.field` · módulo `crm` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `field_id` | integer | 4 B | No | Campo → `ir_model_fields` |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_lost_reason`

**Motivo de pérdida de la oportunidad** · modelo `crm.lost.reason` · módulo `crm` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Descripción |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_merge_opportunity`

**Fusionar oportunidades** · modelo `crm.merge.opportunity` · módulo `crm` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Vendedor → `res_users` |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_recurring_plan`

**Planes de ingresos recurrentes de CRM** · modelo `crm.recurring.plan` · módulo `crm` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `number_of_months` | integer | 4 B | No | Número de meses |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre del plan |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_stage`

**Etapas del CRM** · modelo `crm.stage` · módulo `crm` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Se utiliza para ordenar etapas. Entre más bajo, mejor. |
|  | `rotting_threshold_days` | integer | 4 B | Sí | Días para deteriorarse — Destaca las oportunidades que no han sido actualizadas en este número de días. Utiliza 0 para desactivar la función. Cambiar este parámet… |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre de la etapa |
|  | `requirements` | text | variable | Sí | Requisitos — Ingrese aquí los requisitos internos para esta etapa (por ejemplo, oferta enviada al cliente). Aparecerá como una descripción emergente s… |
|  | `is_won` | boolean | 1 B | Sí | ¿Está en la etapa ganada? |
|  | `fold` | boolean | 1 B | Sí | Plegado en el flujo — Esta etapa está oculta en la vista de kanban cuando no tiene registros para mostrar. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_stage_crm_team_rel`

**Relación muchos a muchos entre «crm.stage» y «crm.team»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_stage_id` | integer | 4 B | No | Referencia a crm_stage |
| PK, FK | `crm_team_id` | integer | 4 B | No | Referencia a crm_team |

### `crm_tag_rel`

**Relación muchos a muchos entre «crm.lead» y «crm.tag»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `lead_id` | integer | 4 B | No | Referencia a crm_lead |
| PK, FK | `tag_id` | integer | 4 B | No | Referencia a crm_tag |

### `merge_opportunity_rel`

**Relación muchos a muchos entre «crm.merge.opportunity» y «crm.lead»** · tabla intermedia, sin modelo propio · módulo `crm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `merge_id` | integer | 4 B | No | Referencia a crm_merge_opportunity |
| PK, FK | `opportunity_id` | integer | 4 B | No | Referencia a crm_lead |

## Módulo `crm_iap_mine`

### `crm_iap_lead_helpers`

**Métodos de soporte para los módulos crm_iap_lead** · modelo `crm.iap.lead.helpers` · módulo `crm_iap_mine` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_iap_lead_industry`

**CRM IAP Industria líder** · modelo `crm.iap.lead.industry` · módulo `crm_iap_mine` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Índice de color |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reveal_ids` | varchar | variable | No | Revelar |
|  | `name` | jsonb | variable | No | Industria |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_iap_lead_industry_crm_iap_lead_mining_request_rel`

**Relación muchos a muchos entre «crm.iap.lead.mining.request» y «crm.iap.lead.industry»** · tabla intermedia, sin modelo propio · módulo `crm_iap_mine` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_iap_lead_mining_request_id` | integer | 4 B | No | Referencia a crm_iap_lead_mining_request |
| PK, FK | `crm_iap_lead_industry_id` | integer | 4 B | No | Referencia a crm_iap_lead_industry |

### `crm_iap_lead_mining_request`

**Solicitud de minado de leads de CRM** · modelo `crm.iap.lead.mining.request` · módulo `crm_iap_mine` · 20 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `lead_number` | integer | 4 B | No | Número de leads |
| FK | `team_id` | integer | 4 B | Sí | Equipo de ventas → `crm_team` |
| FK | `user_id` | integer | 4 B | Sí | Vendedor → `res_users` |
|  | `company_size_min` | integer | 4 B | Sí | Tamaño |
|  | `company_size_max` | integer | 4 B | Sí | Tamaño máximo de la empresa |
|  | `contact_number` | integer | 4 B | Sí | Número de contactos |
| FK | `preferred_role_id` | integer | 4 B | Sí | Función preferida → `crm_iap_lead_role` |
| FK | `seniority_id` | integer | 4 B | Sí | Antigüedad → `crm_iap_lead_seniority` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Número de solicitud |
|  | `state` | varchar | variable | No | Estado |
|  | `search_type` | varchar | variable | No | Objetivo |
|  | `error_type` | varchar | variable | Sí | Tipo de error |
|  | `lead_type` | varchar | variable | No | Tipo |
|  | `contact_filter_type` | varchar | variable | Sí | Filtrar por |
|  | `filter_on_size` | boolean | 1 B | Sí | Filtrar por tamaño |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_iap_lead_mining_request_crm_iap_lead_role_rel`

**Relación muchos a muchos entre «crm.iap.lead.mining.request» y «crm.iap.lead.role»** · tabla intermedia, sin modelo propio · módulo `crm_iap_mine` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_iap_lead_mining_request_id` | integer | 4 B | No | Referencia a crm_iap_lead_mining_request |
| PK, FK | `crm_iap_lead_role_id` | integer | 4 B | No | Referencia a crm_iap_lead_role |

### `crm_iap_lead_mining_request_crm_tag_rel`

**Relación muchos a muchos entre «crm.iap.lead.mining.request» y «crm.tag»** · tabla intermedia, sin modelo propio · módulo `crm_iap_mine` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_iap_lead_mining_request_id` | integer | 4 B | No | Referencia a crm_iap_lead_mining_request |
| PK, FK | `crm_tag_id` | integer | 4 B | No | Referencia a crm_tag |

### `crm_iap_lead_mining_request_res_country_rel`

**Relación muchos a muchos entre «crm.iap.lead.mining.request» y «res.country»** · tabla intermedia, sin modelo propio · módulo `crm_iap_mine` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_iap_lead_mining_request_id` | integer | 4 B | No | Referencia a crm_iap_lead_mining_request |
| PK, FK | `res_country_id` | integer | 4 B | No | Referencia a res_country |

### `crm_iap_lead_mining_request_res_country_state_rel`

**Relación muchos a muchos entre «crm.iap.lead.mining.request» y «res.country.state»** · tabla intermedia, sin modelo propio · módulo `crm_iap_mine` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `crm_iap_lead_mining_request_id` | integer | 4 B | No | Referencia a crm_iap_lead_mining_request |
| PK, FK | `res_country_state_id` | integer | 4 B | No | Referencia a res_country_state |

### `crm_iap_lead_role`

**Función de las personas** · modelo `crm.iap.lead.role` · módulo `crm_iap_mine` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reveal_id` | varchar | variable | No | Revelar |
|  | `name` | jsonb | variable | No | Nombre de la función |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_iap_lead_seniority`

**Antigüedad de las personas** · modelo `crm.iap.lead.seniority` · módulo `crm_iap_mine` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reveal_id` | varchar | variable | No | Revelar |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `digest`

### `digest_digest`

**Resumen** · modelo `digest.digest` · módulo `digest` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `periodicity` | varchar | variable | No | Periodicidad |
|  | `state` | varchar | variable | Sí | Estado |
|  | `next_run_date` | date | 4 B | Sí | Fecha del próximo envío de correo |
|  | `name` | jsonb | variable | No | Nombre |
|  | `kpi_res_users_connected` | boolean | 1 B | Sí | Usuarios conectados |
|  | `kpi_mail_message_total` | boolean | 1 B | Sí | Mensajes enviados |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `kpi_account_total_revenue` | boolean | 1 B | Sí | Ingreso |
|  | `kpi_crm_lead_created` | boolean | 1 B | Sí | Nuevos leads |
|  | `kpi_crm_opportunities_won` | boolean | 1 B | Sí | Oportunidades ganadas |
|  | `kpi_project_task_opened` | boolean | 1 B | Sí | Tareas abiertas |
|  | `kpi_pos_total` | boolean | 1 B | Sí | Ventas de PdV |

### `digest_digest_res_users_rel`

**Relación muchos a muchos entre «digest.digest» y «res.users»** · tabla intermedia, sin modelo propio · módulo `digest` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `digest_digest_id` | integer | 4 B | No | Referencia a digest_digest |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `digest_tip`

**Consejos del resumen** · modelo `digest.tip` · módulo `digest` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Se utiliza para mostrar un consejo del resumen en la plantilla de correo según la orden |
| FK | `group_id` | integer | 4 B | Sí | Grupo autorizado → `res_groups` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | Sí | Nombre |
|  | `tip_description` | jsonb | variable | Sí | Descripción del consejo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `digest_tip_res_users_rel`

**Relación muchos a muchos entre «digest.tip» y «res.users»** · tabla intermedia, sin modelo propio · módulo `digest` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `digest_tip_id` | integer | 4 B | No | Referencia a digest_tip |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

## Módulo `hr`

### `employee_bank_account_rel`

**Relación muchos a muchos entre «hr.employee» y «res.partner.bank»** · tabla intermedia, sin modelo propio · módulo `hr` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `employee_id` | integer | 4 B | No | Referencia a hr_employee |
| PK, FK | `bank_account_id` | integer | 4 B | No | Referencia a res_partner_bank |

### `employee_category_rel`

**Relación muchos a muchos entre «hr.employee» y «hr.employee.category»** · tabla intermedia, sin modelo propio · módulo `hr` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `employee_id` | integer | 4 B | No | Referencia a hr_employee |
| PK, FK | `category_id` | integer | 4 B | No | Referencia a hr_employee_category |

### `hr_bank_account_allocation_wizard`

**Asistente de asignación de cuenta bancaria** · modelo `hr.bank.account.allocation.wizard` · módulo `hr` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `employee_id` | integer | 4 B | No | Empleado → `hr_employee` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_bank_account_allocation_wizard_line`

**Línea de asignación de cuenta bancaria (asistente)** · modelo `hr.bank.account.allocation.wizard.line` · módulo `hr` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `wizard_id` | integer | 4 B | No | Asistente → `hr_bank_account_allocation_wizard` |
| FK | `bank_account_id` | integer | 4 B | No | Cuenta bancaria → `res_partner_bank` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `amount_type` | varchar | variable | Sí | Tipo de importe |
|  | `amount` | numeric | variable | Sí | Importe |
|  | `trusted` | boolean | 1 B | Sí | Confiable |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_contract_type`

**Tipo de contrato** · modelo `hr.contract.type` · módulo `hr` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | Sí | Código |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_department`

**Departamento** · modelo `hr.department` · módulo `hr` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `parent_id` | integer | 4 B | Sí | Departamento principal → `hr_department` |
| FK | `manager_id` | integer | 4 B | Sí | Gerente → `hr_employee` |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `master_department_id` | integer | 4 B | Sí | Departamento maestro → `hr_department` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `name` | jsonb | variable | No | Nombre del departamento |
|  | `note` | text | variable | Sí | Nota |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_departure_reason`

**Motivo de salida** · modelo `hr.departure.reason` · módulo `hr` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Motivo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_departure_wizard`

**Asistente de salida** · modelo `hr.departure.wizard` · módulo `hr` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `departure_reason_id` | integer | 4 B | No | Motivo de salida → `hr_departure_reason` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `departure_date` | date | 4 B | No | Fecha de finalización del contrato |
|  | `departure_description` | text | variable | Sí | Información adicional |
|  | `remove_related_user` | boolean | 1 B | Sí | Usuario relacionado — Si está seleccionada, el usuario relacionado será eliminado del sistema. |
|  | `set_date_end` | boolean | 1 B | Sí | Establecer fecha de finalización de contrato — Establecer la fecha de finalización en el contrato actual. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_departure_wizard_hr_employee_rel`

**Relación muchos a muchos entre «hr.departure.wizard» y «hr.employee»** · tabla intermedia, sin modelo propio · módulo `hr` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `hr_departure_wizard_id` | integer | 4 B | No | Referencia a hr_departure_wizard |
| PK, FK | `hr_employee_id` | integer | 4 B | No | Referencia a hr_employee |

### `hr_employee_category`

**Categoría de empleado** · modelo `hr.employee.category` · módulo `hr` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de la etiqueta |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_employee_hr_skill_rel`

**Relación muchos a muchos entre «hr.employee» y «hr.skill»** · tabla intermedia, sin modelo propio · módulo `hr` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `hr_employee_id` | integer | 4 B | No | Referencia a hr_employee |
| PK, FK | `hr_skill_id` | integer | 4 B | No | Referencia a hr_skill |

### `hr_job`

**Puesto de trabajo** · modelo `hr.job` · módulo `hr` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
|  | `no_of_recruitment` | integer | 4 B | Sí | Objetivo — Número de empleados que espera contratar. |
| FK | `user_id` | integer | 4 B | Sí | Reclutador → `res_users` — El reclutador será el valor predeterminado para todos los postulantes de este puesto. El reclutador se agrega de forma automática a todas… |
| FK | `department_id` | integer | 4 B | Sí | Departamento → `hr_department` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `contract_type_id` | integer | 4 B | Sí | Tipo de empleo → `hr_contract_type` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Puesto de trabajo |
|  | `description` | text | variable | Sí | Descripción del trabajo |
|  | `requirements` | text | variable | Sí | Requisitos |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_job_hr_skill_rel`

**Relación muchos a muchos entre «hr.job» y «hr.skill»** · tabla intermedia, sin modelo propio · módulo `hr` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `hr_job_id` | integer | 4 B | No | Referencia a hr_job |
| PK, FK | `hr_skill_id` | integer | 4 B | No | Referencia a hr_skill |

### `hr_payroll_structure_type`

**Tipo de estructura salarial** · modelo `hr.payroll.structure.type` · módulo `hr` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `default_resource_calendar_id` | integer | 4 B | Sí | Horas laborables → `resource_calendar` |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Tipo de estructura salarial |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_version`

**Contrato del empleado** · modelo `hr.version` · módulo `hr` · 53 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `employee_id` | integer | 4 B | Sí | Empleado → `hr_employee` |
| FK | `last_modified_uid` | integer | 4 B | No | Última modificación de → `res_users` |
| FK | `country_id` | integer | 4 B | Sí | Nacionalidad (país) → `res_country` |
| FK | `private_state_id` | integer | 4 B | Sí | Estado privado → `res_country_state` |
| FK | `private_country_id` | integer | 4 B | Sí | País privado → `res_country` |
|  | `distance_home_work` | integer | 4 B | Sí | Distancia de la casa al trabajo |
|  | `km_home_work` | integer | 4 B | Sí | Distancia de la casa al trabajo en kilómetros |
|  | `children` | integer | 4 B | Sí | Hijos dependientes |
| FK | `department_id` | integer | 4 B | Sí | Departamento → `hr_department` |
| FK | `job_id` | integer | 4 B | Sí | Puesto → `hr_job` |
| FK | `address_id` | integer | 4 B | Sí | Dirección laboral → `res_partner` |
| FK | `work_location_id` | integer | 4 B | Sí | Ubicación de trabajo → `hr_work_location` |
| FK | `departure_reason_id` | integer | 4 B | Sí | Motivo de salida → `hr_departure_reason` |
| FK | `resource_calendar_id` | integer | 4 B | Sí | Horas laborables → `resource_calendar` |
| FK | `contract_template_id` | integer | 4 B | Sí | Plantilla de contrato → `hr_version` — Seleccione una plantilla de contrato para completar el formulario de contrato con los valores predefinidos de forma automática. Luego de… |
| FK | `structure_type_id` | integer | 4 B | Sí | Tipo de estructura salarial → `hr_payroll_structure_type` |
| FK | `contract_type_id` | integer | 4 B | Sí | Tipo de contrato → `hr_contract_type` |
| FK | `hr_responsible_id` | integer | 4 B | No | Responsable de RR. HH. → `res_users` — Persona responsable de validar los contratos del empleado. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `identification_id` | varchar | variable | Sí | Número de identificación — Ingresa el número de identificación nacional del empleado emitido por el gobierno (por ejemplo, Aadhaar, SIN, NIN). Este se usa para regi… |
|  | `ssnid` | varchar | variable | Sí | Número de seguridad social — Número de seguridad social |
|  | `passport_id` | varchar | variable | Sí | Número de pasaporte |
|  | `sex` | varchar | variable | Sí | Género — Este es el sexo legal reconocido por el estado. |
|  | `private_street` | varchar | variable | Sí | Calle privada |
|  | `private_street2` | varchar | variable | Sí | Calle2 privada |
|  | `private_city` | varchar | variable | Sí | Ciudad privada |
|  | `private_zip` | varchar | variable | Sí | C.P. privado |
|  | `distance_home_work_unit` | varchar | variable | No | Unidad de la distancia entre la casa y el trabajo |
|  | `marital` | varchar | variable | No | Estado civil |
|  | `spouse_complete_name` | varchar | variable | Sí | Nombre legal del cónyuge |
|  | `employee_type` | varchar | variable | No | Tipo de empleado |
|  | `job_title` | varchar | variable | Sí | Nombre del puesto |
|  | `date_version` | date | 4 B | No | Fecha de la versión |
|  | `passport_expiration_date` | date | 4 B | Sí | Fecha de vencimiento del pasaporte |
|  | `spouse_birthdate` | date | 4 B | Sí | Fecha de nacimiento del cónyuge |
|  | `departure_date` | date | 4 B | Sí | Fecha de salida |
|  | `contract_date_start` | date | 4 B | Sí | Fecha de inicio del contrato |
|  | `contract_date_end` | date | 4 B | Sí | Fecha de finalización del contrato — Fecha de finalización del contrato (si es un contrato por tiempo determinado). |
|  | `trial_date_end` | date | 4 B | Sí | Fin del periodo de prueba — Fecha de finalización del periodo de prueba (si existe). |
|  | `departure_description` | text | variable | Sí | Información adicional |
|  | `additional_note` | text | variable | Sí | Nota adicional |
|  | `wage` | numeric | variable | Sí | Salario — Salario bruto mensual del empleado. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `is_custom_job_title` | boolean | 1 B | Sí | Es un título de trabajo personalizado |
|  | `is_flexible` | boolean | 1 B | Sí | Es flexible |
|  | `is_fully_flexible` | boolean | 1 B | Sí | Es completamente flexible |
|  | `last_modified_date` | timestamp | 8 B | No | Última modificación el |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_version_wizard`

**Asistente de plantilla de contrato** · modelo `hr.version.wizard` · módulo `hr` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `contract_template_id` | integer | 4 B | No | Plantilla de contrato → `hr_version` — Seleccione una plantilla de contrato para completar el formulario de contrato con los valores predefinidos de forma automática. Luego de… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_work_location`

**Ubicación de trabajo** · modelo `hr.work.location` · módulo `hr` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `address_id` | integer | 4 B | No | Dirección laboral → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Ubicación de trabajo |
|  | `location_type` | varchar | variable | No | Imagen de portada |
|  | `location_number` | varchar | variable | Sí | Número de ubicación |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `hr_homeworking`

### `hr_employee_location`

**Ubicación del empleado** · modelo `hr.employee.location` · módulo `hr_homeworking` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `work_location_id` | integer | 4 B | No | Ubicación → `hr_work_location` |
| FK | `employee_id` | integer | 4 B | No | Empleado → `hr_employee` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `date` | date | 4 B | Sí | Fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `hr_homeworking_calendar`

### `homework_location_wizard`

**Asistente para establecer una ubicación de trabajo remoto** · modelo `homework.location.wizard` · módulo `hr_homeworking_calendar` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `work_location_id` | integer | 4 B | No | Ubicación → `hr_work_location` |
| FK | `employee_id` | integer | 4 B | No | Empleado → `hr_employee` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `date` | date | 4 B | Sí | Fecha |
|  | `weekly` | boolean | 1 B | Sí | Semanal |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `hr_skills`

### `hr_employee_cv_wizard`

**Currículo impreso** · modelo `hr.employee.cv.wizard` · módulo `hr_skills` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `color_primary` | varchar | variable | No | Color primario |
|  | `color_secondary` | varchar | variable | No | Color secundario |
|  | `show_skills` | boolean | 1 B | Sí | Habilidades |
|  | `show_contact` | boolean | 1 B | Sí | Información de contacto |
|  | `show_others` | boolean | 1 B | Sí | Otros |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_employee_hr_employee_cv_wizard_rel`

**Relación muchos a muchos entre «hr.employee.cv.wizard» y «hr.employee»** · tabla intermedia, sin modelo propio · módulo `hr_skills` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `hr_employee_cv_wizard_id` | integer | 4 B | No | Referencia a hr_employee_cv_wizard |
| PK, FK | `hr_employee_id` | integer | 4 B | No | Referencia a hr_employee |

### `hr_employee_skill`

**Nivel de habilidad del empleado** · modelo `hr.employee.skill` · módulo `hr_skills` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `skill_id` | integer | 4 B | No | Habilidad → `hr_skill` |
| FK | `skill_level_id` | integer | 4 B | No | Nivel de habilidad → `hr_skill_level` |
| FK | `skill_type_id` | integer | 4 B | No | Tipo de habilidad → `hr_skill_type` |
| FK | `employee_id` | integer | 4 B | No | Empleado → `hr_employee` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `valid_from` | date | 4 B | Sí | Inicio de la validez |
|  | `valid_to` | date | 4 B | Sí | Detener validez |
|  | `display_warning_message` | boolean | 1 B | Sí | Mostrar mensaje de advertencia |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_job_skill`

**Habilidades para los puestos de trabajo** · modelo `hr.job.skill` · módulo `hr_skills` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `skill_id` | integer | 4 B | No | Habilidad → `hr_skill` |
| FK | `skill_level_id` | integer | 4 B | No | Nivel de habilidad → `hr_skill_level` |
| FK | `skill_type_id` | integer | 4 B | No | Tipo de habilidad → `hr_skill_type` |
| FK | `job_id` | integer | 4 B | No | Puesto → `hr_job` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `valid_from` | date | 4 B | Sí | Inicio de la validez |
|  | `valid_to` | date | 4 B | Sí | Detener validez |
|  | `display_warning_message` | boolean | 1 B | Sí | Mostrar mensaje de advertencia |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_resume_line`

**Línea de currículum de un empleado** · modelo `hr.resume.line` · módulo `hr_skills` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `employee_id` | integer | 4 B | No | Empleado → `hr_employee` |
|  | `duration` | integer | 4 B | Sí | Duración |
| FK | `line_type_id` | integer | 4 B | Sí | Tipo → `hr_resume_line_type` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `course_type` | varchar | variable | No | Tipo de curso |
|  | `external_url` | varchar | variable | Sí | URL externa |
|  | `certificate_filename` | varchar | variable | Sí | Nombre del archivo del certificado |
|  | `date_start` | date | 4 B | No | Fecha de inicio |
|  | `date_end` | date | 4 B | Sí | Fecha de finalización |
|  | `name` | jsonb | variable | No | Nombre |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `resume_line_properties` | jsonb | variable | Sí | Propiedades |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_resume_line_type`

**Tipo de línea en el currículum** · modelo `hr.resume.line.type` · módulo `hr_skills` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `resume_line_type_properties_definition` | jsonb | variable | Sí | Propiedades de las secciones |
|  | `is_course` | boolean | 1 B | Sí | Curso |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_skill`

**Habilidad** · modelo `hr.skill` · módulo `hr_skills` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `skill_type_id` | integer | 4 B | No | Tipo de habilidad → `hr_skill_type` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_skill_level`

**Nivel de habilidad** · modelo `hr.skill.level` · módulo `hr_skills` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `skill_type_id` | integer | 4 B | Sí | Tipo de habilidad → `hr_skill_type` |
|  | `level_progress` | integer | 4 B | Sí | Progreso — Progreso desde cero (0%) a dominio total (100%). |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `default_level` | boolean | 1 B | Sí | Nivel predeterminado — Si se encuentra seleccionado, este nivel será el que se seleccione de forma predeterminada al elegir esta habilidad. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `hr_skill_type`

**Tipo de habilidad** · modelo `hr.skill.type` · módulo `hr_skills` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
|  | `color` | integer | 4 B | Sí | Color |
|  | `levels_count` | integer | 4 B | Sí | Número de niveles — Número de niveles vinculados a este tipo de habilidad |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `is_certification` | boolean | 1 B | Sí | Certificación — Si está seleccionada, el tipo de habilidad se convierte en un tipo de certificación. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `html_editor`

### `html_editor_converter_test`

**Prueba del convertidor de editor HTML** · modelo `html_editor.converter.test` · módulo `html_editor` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `integer` | integer | 4 B | Sí | Integer |
| FK | `many2one` | integer | 4 B | Sí | Many2One → `html_editor_converter_test_sub` |
| FK | `create_uid` | integer | 4 B | Sí | Created by → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Last Updated by → `res_users` |
|  | `char` | varchar | variable | Sí | Char |
|  | `selection_str` | varchar | variable | Sí | Lorsqu'un pancake prend l'avion à destination de Toronto et qu'il fait une escale technique à St Claude, on dit: |
|  | `date` | date | 4 B | Sí | Date |
|  | `html` | text | variable | Sí | Html |
|  | `text` | text | variable | Sí | Text |
|  | `numeric` | numeric | variable | Sí | Numeric |
|  | `datetime` | timestamp | 8 B | Sí | Datetime |
|  | `create_date` | timestamp | 8 B | Sí | Created on |
|  | `write_date` | timestamp | 8 B | Sí | Last Updated on |
|  | `float` | double precision | 8 B | Sí | Float |
|  | `binary` | bytea | variable | Sí | Binary |

### `html_editor_converter_test_sub`

**Subprueba del convertidor de editor HTML** · modelo `html_editor.converter.test.sub` · módulo `html_editor` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `iap`

### `iap_account`

**Cuenta para compras dentro de la aplicación** · modelo `iap.account` · módulo `iap` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `service_id` | integer | 4 B | No | Servicio → `iap_service` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `account_token` | varchar | 43 | Sí | Token de la cuenta — El token de su cuenta es su clave de autenticación para este servicio. No lo comparta. |
|  | `balance` | varchar | variable | Sí | Balance |
|  | `state` | varchar | variable | Sí | Estado |
|  | `service_locked` | boolean | 1 B | Sí | Servicio bloqueado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `warning_threshold` | double precision | 8 B | Sí | Límite de alerta por correo electrónico |
|  | `sender_name` | varchar | variable | Sí | Nombre del remitente — Este es el nombre que aparecerá como el remitente del SMS. |

### `iap_account_res_company_rel`

**Relación muchos a muchos entre «iap.account» y «res.company»** · tabla intermedia, sin modelo propio · módulo `iap` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `iap_account_id` | integer | 4 B | No | Referencia a iap_account |
| PK, FK | `res_company_id` | integer | 4 B | No | Referencia a res_company |

### `iap_account_res_users_rel`

**Relación muchos a muchos entre «iap.account» y «res.users»** · tabla intermedia, sin modelo propio · módulo `iap` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `iap_account_id` | integer | 4 B | No | Referencia a iap_account |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `iap_service`

**Servicio de compras dentro de la aplicación** · modelo `iap.service` · módulo `iap` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `technical_name` | varchar | variable | No | Nombre técnico |
|  | `description` | jsonb | variable | No | Descripción |
|  | `unit_name` | jsonb | variable | No | Nombre de la unidad |
|  | `integer_balance` | boolean | 1 B | No | Saldo integro |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `l10n_latam_base`

### `l10n_latam_identification_type`

**Tipos de identificación** · modelo `l10n_latam.identification.type` · módulo `l10n_latam_base` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `is_vat` | boolean | 1 B | Sí | Es Identificación Fiscal? |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `l10n_pe_vat_code` | varchar | variable | Sí | Código de tipo de documento de identidad |

## Módulo `l10n_latam_invoice_document`

### `l10n_latam_document_type`

**Tipo de Documento Latam** · modelo `l10n_latam.document.type` · módulo `l10n_latam_invoice_document` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID (identificación) |
|  | `sequence` | integer | 4 B | No | Secuencia — Para establecer el orden en que se muestran los tipos de documento, de modo que los más usados aparezcan primero |
| FK | `country_id` | integer | 4 B | No | País → `res_country` — País donde este tipo de documento es válido |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `doc_code_prefix` | varchar | variable | Sí | Prefijo del código de documento — Prefijo para los códigos de documentos en facturas y asientos. Por ejemplo, 'FA' generará el número de documento 'FA 0001-0000001' |
|  | `code` | varchar | variable | Sí | Código — Código usando por diferentes localizaciones |
|  | `internal_type` | varchar | variable | Sí | Tipo interno — Análogo a account.move.move_type de Odoo, pero con más opciones que te permiten identificar el tipo de documento con el que trabajas. (No… |
|  | `name` | jsonb | variable | No | Nombre — El nombre del documento |
|  | `report_name` | jsonb | variable | Sí | Nombre en Reportes — Nombre que será impreso en los reportes, por ejemplo "NOTA DE CREDITO" |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `l10n_pe`

### `l10n_pe_res_city_district`

**Distrito** · modelo `l10n_pe.res.city.district` · módulo `l10n_pe` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `city_id` | integer | 4 B | Sí | Ciudad → `res_city` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | Sí | Código — Este código ayudará con la identificación de cada distrito en Perú. |
|  | `name` | jsonb | variable | Sí | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `mail`

### `activity_attachment_rel`

**Relación muchos a muchos entre «mail.activity» y «ir.attachment»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `activity_id` | integer | 4 B | No | Referencia a mail_activity |
| PK, FK | `attachment_id` | integer | 4 B | No | Referencia a ir_attachment |

### `discuss_call_history`

**Mantener el historial de la llamada** · modelo `discuss.call.history` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `channel_id` | integer | 4 B | No | Canal → `discuss_channel` |
| FK | `start_call_message_id` | integer | 4 B | Sí | Mensaje de iniciar llamada → `mail_message` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `start_dt` | timestamp | 8 B | No | Fecha de inicio |
|  | `end_dt` | timestamp | 8 B | Sí | Fecha de finalización |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `discuss_channel`

**Canal de conversaciones** · modelo `discuss.channel` · módulo `mail` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_channel_id` | integer | 4 B | Sí | Canal principal → `discuss_channel` — Canal principal |
| FK | `from_message_id` | integer | 4 B | Sí | Mensaje de → `mail_message` — El mensaje desde el que se creó el canal. |
| FK | `group_public_id` | integer | 4 B | Sí | Grupo autorizado → `res_groups` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `channel_type` | varchar | variable | No | Tipo de canal — Un chat es privado y único entre 2 personas. Un grupo es privado entre las personas invitadas. Un canal es abierto y cualquier persona pu… |
|  | `default_display_mode` | varchar | variable | Sí | Modo de visualización predeterminado — Determina cómo se mostrará el canal de forma predeterminada al abrirlo desde el enlace de invitación. Ningún valor significa que se muest… |
|  | `sfu_channel_uuid` | varchar | variable | Sí | Uuid del canal Sfu |
|  | `sfu_server_url` | varchar | variable | Sí | URL del servidor SFU |
|  | `uuid` | varchar | 50 | Sí | UUID |
|  | `description` | text | variable | Sí | Descripción |
|  | `active` | boolean | 1 B | Sí | Activo — Cambie la opción de activo a falso para ocultar el canal sin eliminarlo. |
|  | `last_interest_dt` | timestamp | 8 B | Sí | Último interés — Incluye la fecha y hora del último evento interesante que ocurrió en este canal. Esto se actualiza cuando se publica un nuevo mensaje. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `discuss_channel_hr_department_rel`

**Relación muchos a muchos entre «discuss.channel» y «hr.department»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `discuss_channel_id` | integer | 4 B | No | Referencia a discuss_channel |
| PK, FK | `hr_department_id` | integer | 4 B | No | Referencia a hr_department |

### `discuss_channel_member`

**Miembro del canal** · modelo `discuss.channel.member` · módulo `mail` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `guest_id` | integer | 4 B | Sí | Invitado → `mail_guest` |
| FK | `channel_id` | integer | 4 B | No | Canal → `discuss_channel` |
| FK | `fetched_message_id` | integer | 4 B | Sí | Recuperado por última vez → `mail_message` |
| FK | `seen_message_id` | integer | 4 B | Sí | Visto por última vez → `mail_message` |
|  | `new_message_separator` | integer | 4 B | No | Separador para nuevos mensajes — ID del mensaje ante el cual debe aparecer el separador |
| FK | `rtc_inviting_session_id` | integer | 4 B | Sí | Sesión de llamadas → `discuss_channel_rtc_session` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `custom_channel_name` | varchar | variable | Sí | Nombre personalizado del canal |
|  | `custom_notifications` | varchar | variable | Sí | Notificaciones personalizadas — Use el valor predeterminado de los ajustes del usuario si no se especifica. Este ajuste solo se aplicará a los canales. |
|  | `mute_until_dt` | timestamp | 8 B | Sí | Silenciar las notificaciones hasta que — Si se establece, el miembro no recibirá notificaciones del canal hasta esa fecha. |
|  | `unpin_dt` | timestamp | 8 B | Sí | Fecha en que se desfijó — Incluye la fecha y hora en que el usuario desfijó el canal. |
|  | `last_interest_dt` | timestamp | 8 B | Sí | Último interés — Incluye la fecha y hora del último evento interesante que ocurrió en este canal para este usuario. Esto incluye: crear, unir y fijar. |
|  | `last_seen_dt` | timestamp | 8 B | Sí | Fecha de la última visita |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `discuss_channel_res_groups_rel`

**Relación muchos a muchos entre «discuss.channel» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `discuss_channel_id` | integer | 4 B | No | Referencia a discuss_channel |
| PK, FK | `res_groups_id` | integer | 4 B | No | Referencia a res_groups |

### `discuss_channel_rtc_session`

**Sesión de comunicación en tiempo real por correo** · modelo `discuss.channel.rtc.session` · módulo `mail` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `channel_member_id` | integer | 4 B | No | Miembro del canal → `discuss_channel_member` |
| FK | `channel_id` | integer | 4 B | Sí | Canal → `discuss_channel` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `is_screen_sharing_on` | boolean | 1 B | Sí | Está compartiendo pantalla |
|  | `is_camera_on` | boolean | 1 B | Sí | Está enviando un video de usuario |
|  | `is_muted` | boolean | 1 B | Sí | El micrófono está silenciado |
|  | `is_deaf` | boolean | 1 B | Sí | Ha desactivado el sonido de entrada |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |

### `discuss_gif_favorite`

**Marcar un GIF de Tenor API como favorito** · modelo `discuss.gif.favorite` · módulo `mail` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `tenor_gif_id` | varchar | variable | No | ID de GIF de Tenor |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `discuss_voice_metadata`

**Metadatos para los archivos adjuntos de voz** · modelo `discuss.voice.metadata` · módulo `mail` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `attachment_id` | integer | 4 B | Sí | Archivo adjunto → `ir_attachment` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `email_template_attachment_rel`

**Relación muchos a muchos entre «mail.template» y «ir.attachment»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `email_template_id` | integer | 4 B | No | Referencia a mail_template |
| PK, FK | `attachment_id` | integer | 4 B | No | Referencia a ir_attachment |

### `fetchmail_server`

**Servidor de correos entrantes** · modelo `fetchmail.server` · módulo `mail` · 29 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `port` | integer | 4 B | Sí | Puerto |
| FK | `object_id` | integer | 4 B | Sí | Crear un nuevo registro → `ir_model` — Procese cada correo entrante como parte de una conversación correspondiente a este tipo de documento. Esto creará nuevos documentos para… |
|  | `priority` | integer | 4 B | Sí | Prioridad del servidor — Define el orden de procesamiento. Los valores más bajos significan una mayor prioridad. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `state` | varchar | variable | Sí | Estado |
|  | `server` | varchar | variable | Sí | Nombre del servidor — Nombre del host o IP del servidor de correo |
|  | `server_type` | varchar | variable | No | Tipo de servidor |
|  | `user` | varchar | variable | Sí | Nombre de usuario |
|  | `password` | varchar | variable | Sí | Contraseña |
|  | `script` | varchar | variable | Sí | Script |
|  | `error_message` | text | variable | Sí | Último mensaje de error |
|  | `configuration` | text | variable | Sí | Configuración |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `is_ssl` | boolean | 1 B | Sí | SSL/TLS — Las conexiones se cifran con SSL/TLS a través de un puerto específico (predeterminado: IMAPS = 993, POP3S = 995) |
|  | `attach` | boolean | 1 B | Sí | Guardar archivos adjuntos — Si se deben descargar los archivos adjuntos. Si no se habilita, se eliminará cualquier archivo adjunto de los correos entrantes antes de… |
|  | `original` | boolean | 1 B | Sí | Mantener el original — Si se debe guardar una copia original completa de cada correo electrónico como referencia adjunta a cada mensaje procesado. Esto usualmen… |
|  | `date` | timestamp | 8 B | Sí | Última fecha de búsqueda |
|  | `error_date` | timestamp | 8 B | Sí | Fecha del último error — Fecha de la última falla, se restablecerá si se tiene éxito. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `google_gmail_access_token_expiration` | integer | 4 B | Sí | Marca de tiempo de vencimiento del token de acceso |
|  | `google_gmail_refresh_token` | varchar | variable | Sí | Actualizar token |
|  | `google_gmail_access_token` | varchar | variable | Sí | Token de acceso |
|  | `microsoft_outlook_access_token_expiration` | integer | 4 B | Sí | Marca de tiempo de vencimiento del token de acceso de Outlook |
|  | `microsoft_outlook_refresh_token` | varchar | variable | Sí | Token de actualización de Outlook |
|  | `microsoft_outlook_access_token` | varchar | variable | Sí | Token de acceso de Outlook |

### `mail_activity`

**Actividad** · modelo `mail.activity` · módulo `mail` · 22 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `res_model_id` | integer | 4 B | Sí | Modelo de documento → `ir_model` |
|  | `res_id` | integer | 4 B | Sí | ID del documento relacionado |
| FK | `activity_type_id` | integer | 4 B | Sí | Tipo de actividad → `mail_activity_type` |
| FK | `user_id` | integer | 4 B | Sí | Asignada a → `res_users` |
| FK | `recommended_activity_type_id` | integer | 4 B | Sí | Tipo de actividad recomendada → `mail_activity_type` |
| FK | `previous_activity_type_id` | integer | 4 B | Sí | Tipo de actividad previa → `mail_activity_type` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | Sí | Modelo de documento relacionado |
|  | `res_name` | varchar | variable | Sí | Nombre del documento |
|  | `summary` | varchar | variable | Sí | Resumen |
|  | `user_tz` | varchar | variable | Sí | Zona horaria — Al imprimir documentos y exportar e importar datos, los valores de fechas y horas se calculan con base en esta zona horaria. Si no ha con… |
|  | `date_deadline` | date | 4 B | No | Fecha límite |
|  | `date_done` | date | 4 B | Sí | Fecha de finalización |
|  | `note` | text | variable | Sí | Nota |
|  | `feedback` | text | variable | Sí | Retroalimentación |
|  | `automated` | boolean | 1 B | Sí | Actividad automatizada — Indica que esta actividad se creó automáticamente y no la creó un usuario. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `calendar_event_id` | integer | 4 B | Sí | Reunión de calendario → `calendar_event` |

### `mail_activity_plan`

**Plan de actividad** · modelo `mail.activity.plan` · módulo `mail` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `res_model_id` | integer | 4 B | No | Aplica a → `ir_model` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `res_model` | varchar | variable | No | Modelo — Especificar un modelo si la actividad debería ser específica para un modelo y no estar disponible cuando se gestionan actividades para ot… |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `department_id` | integer | 4 B | Sí | Departamento → `hr_department` |

### `mail_activity_plan_mail_activity_schedule_rel`

**Relación muchos a muchos entre «mail.activity.schedule» y «mail.activity.plan»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_activity_schedule_id` | integer | 4 B | No | Referencia a mail_activity_schedule |
| PK, FK | `mail_activity_plan_id` | integer | 4 B | No | Referencia a mail_activity_plan |

### `mail_activity_plan_template`

**Plantilla del plan de actividad** · modelo `mail.activity.plan.template` · módulo `mail` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `plan_id` | integer | 4 B | No | Plan → `mail_activity_plan` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `activity_type_id` | integer | 4 B | No | Tipo de actividad → `mail_activity_type` |
|  | `delay_count` | integer | 4 B | Sí | Intervalo — Número de días, semanas o meses antes de realizar la acción después o antes de la fecha del plan programado. |
| FK | `responsible_id` | integer | 4 B | Sí | Asignada a → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `delay_unit` | varchar | variable | No | Unidades atrasadas — Unidad de retraso |
|  | `delay_from` | varchar | variable | No | Activar |
|  | `summary` | varchar | variable | Sí | Resumen |
|  | `responsible_type` | varchar | variable | No | Asignación |
|  | `note` | text | variable | Sí | Nota |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_activity_plan_template_mail_activity_type_rel`

**Relación muchos a muchos entre «mail.activity.plan.template» y «mail.activity.type»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_activity_plan_template_id` | integer | 4 B | No | Referencia a mail_activity_plan_template |
| PK, FK | `mail_activity_type_id` | integer | 4 B | No | Referencia a mail_activity_type |

### `mail_activity_rel`

**Relación muchos a muchos entre «mail.activity.type» y «mail.activity.type»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `activity_id` | integer | 4 B | No | Referencia a mail_activity_type |
| PK, FK | `recommended_id` | integer | 4 B | No | Referencia a mail_activity_type |

### `mail_activity_schedule`

**Asistente para planificar actividades** · modelo `mail.activity.schedule` · módulo `mail` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `res_model_id` | integer | 4 B | Sí | Aplica a → `ir_model` |
| FK | `plan_id` | integer | 4 B | Sí | Plan → `mail_activity_plan` |
| FK | `plan_on_demand_user_id` | integer | 4 B | Sí | Asignado a → `res_users` — Seleccione la asignación para actividades con asignación a petición. |
| FK | `activity_type_id` | integer | 4 B | Sí | Tipo de actividad → `mail_activity_type` |
| FK | `activity_user_id` | integer | 4 B | Sí | Asignada a → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | Sí | Modelo |
|  | `summary` | varchar | variable | Sí | Resumen |
|  | `plan_date` | date | 4 B | Sí | Fecha del plan |
|  | `date_deadline` | date | 4 B | Sí | Fecha límite |
|  | `res_ids` | text | variable | Sí | ID del documento |
|  | `note` | text | variable | Sí | Nota |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_activity_schedule_line`

**Línea de programar la actividad de correo** · modelo `mail.activity.schedule.line` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `activity_schedule_id` | integer | 4 B | No | Horario de la actividad → `mail_activity_schedule` |
| FK | `responsible_user_id` | integer | 4 B | Sí | Usuario responsable → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `line_description` | varchar | variable | Sí | Descripción de la línea |
|  | `line_date_deadline` | date | 4 B | Sí | Fecha límite |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_activity_type`

**Tipo de actividad** · modelo `mail.activity.type` · módulo `mail` · 20 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Crear UID → `res_users` |
|  | `delay_count` | integer | 4 B | Sí | Programar — Número de días/semanas/meses antes de realizar la acción. Permite planear la fecha límite de la acción. |
| FK | `triggered_next_type_id` | integer | 4 B | Sí | Activar → `mail_activity_type` — Programar automáticamente esta actividad una vez que la actual se marque como hecha. |
| FK | `default_user_id` | integer | 4 B | Sí | Usuario predeterminado → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `delay_unit` | varchar | variable | No | Unidades atrasadas — Unidad de retraso |
|  | `delay_from` | varchar | variable | No | Tipo de atraso — Tipo de retraso |
|  | `icon` | varchar | variable | Sí | Icono — Icono de Font Awesome, por ejemplo, fa-tasks |
|  | `decoration_type` | varchar | variable | Sí | Tipo de decoración — Cambia el color de fondo de las actividades relacionadas de este tipo. |
|  | `res_model` | varchar | variable | Sí | Modelo — Especificar un modelo si la actividad debería ser específica para un modelo y no estar disponible cuando se gestionan actividades para ot… |
|  | `chaining_type` | varchar | variable | No | Tipo de encadenamiento |
|  | `category` | varchar | variable | Sí | Acción — Las acciones pueden activar comportamientos específicos, como abrir la vista de calendario o marcar la actividad como hecha de forma auto… |
|  | `name` | jsonb | variable | No | Nombre |
|  | `summary` | jsonb | variable | Sí | Resumen predeterminado |
|  | `default_note` | jsonb | variable | Sí | Nota predeterminada |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_activity_type_mail_template_rel`

**Relación muchos a muchos entre «mail.activity.type» y «mail.template»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_activity_type_id` | integer | 4 B | No | Referencia a mail_activity_type |
| PK, FK | `mail_template_id` | integer | 4 B | No | Referencia a mail_template |

### `mail_alias`

**Alias de correo** · modelo `mail.alias` · módulo `mail` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `alias_domain_id` | integer | 4 B | Sí | Dominio del alias → `mail_alias_domain` |
| FK | `alias_model_id` | integer | 4 B | No | Modelo con alias → `ir_model` — El modelo (tipo de documento de Odoo) al que corresponde este alias. Cualquier correo entrante que no sea respuesta a un registro existen… |
|  | `alias_force_thread_id` | integer | 4 B | Sí | ID del hilo de registro — ID opcional de un hilo (registro) al que se adjuntarán todos los mensajes entrantes, incluso si no fueron respuestas del mismo. Si se est… |
| FK | `alias_parent_model_id` | integer | 4 B | Sí | Modelo principal → `ir_model` — Modelo principal que posee el seudónimo. El modelo que contiene la referencia del seudónimo no es necesariamente el modelo dado por alias… |
|  | `alias_parent_thread_id` | integer | 4 B | Sí | ID del hilo del registro principal — ID del registro principal que tiene el alias (por ejemplo, el proyecto que contiene el alias para la creación de tareas) |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `alias_name` | varchar | variable | Sí | Nombre del alias — El nombre del alias del correo, por ejemplo, "vacantes" para recibir los mensajes de <vacantes@ejemplo.odoo.com>. |
|  | `alias_full_name` | varchar | variable | Sí | Correo electrónico del alias |
|  | `alias_contact` | varchar | variable | No | Seguridad del contacto del alias — La política sobre cómo publicar un mensaje en el documento con el servidor de correo. - Todos: todos pueden publicar - Contactos: solo lo… |
|  | `alias_status` | varchar | variable | Sí | Estado del alias — Estado del alias evaluado en el último mensaje recibido. |
|  | `alias_bounced_content` | jsonb | variable | Sí | Mensaje personalizado en caso de devolución — Si se establece, este contenido se enviará en automático a los usuarios no autorizados en vez del mensaje predeterminado. |
|  | `alias_defaults` | text | variable | No | Valores predeterminados — Un diccionario de Python que se evaluará con el fin de proporcionar los valores predeterminados al crear nuevos registros para este alias. |
|  | `alias_incoming_local` | boolean | 1 B | Sí | Detección entrante basada en la parte local |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_alias_domain`

**Dominio de correo electrónico** · modelo `mail.alias.domain` · módulo `mail` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre — Dominio del correo electrónico, por ejemplo, "ejemplo.com" en "odoo@ejemplo.com" |
|  | `bounce_alias` | varchar | variable | No | Alias de devolución — Parte local del correo electrónico que se utiliza como "ruta de retorno" en caso de que los correos se devuelvan, por ejemplo, "devolucio… |
|  | `catchall_alias` | varchar | variable | No | Alias de catchall — Parte local del correo electrónico que se utiliza como "responder a" para recibir respuestas, por ejemplo, "catchall" en "catchall@ejempl… |
|  | `default_from` | varchar | variable | Sí | Alias de origen predeterminado — Predeterminado cuando no coincide con los filtros de servidor saliente. Puede ser una parte local, por ejemplo, "notificaciones" o una di… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_blacklist`

**Exclusión del correo** · modelo `mail.blacklist` · módulo `mail` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email` | varchar | variable | No | Dirección de correo electrónico — Este campo no distingue entre mayúsculas y minúsculas. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_blacklist_remove`

**Asistente para eliminar los correos electrónicos de la lista de exclusión** · modelo `mail.blacklist.remove` · módulo `mail` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email` | varchar | variable | No | Correo electrónico |
|  | `reason` | varchar | variable | Sí | Motivo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_canned_response`

**Respuesta predefinida** · modelo `mail.canned.response` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `source` | varchar | variable | No | Acceso directo — Respuesta predefinida que se sustituirá en automático por un contenido más largo en tus mensajes. Escribe '::' seguido del nombre de tu a… |
|  | `substitution` | text | variable | No | Sustitución — Contenido que sustituirá automáticamente el acceso directo que usted elija. Aún se puede cambiar este contenido antes de enviar su mensaje. |
|  | `is_shared` | boolean | 1 B | Sí | Determina si la canned_response se comparte con otros usuarios en este momento |
|  | `last_used` | timestamp | 8 B | Sí | Último uso — Última vez que se utilizó esta canned_response |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_canned_response_res_groups_rel`

**Relación muchos a muchos entre «mail.canned.response» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_canned_response_id` | integer | 4 B | No | Referencia a mail_canned_response |
| PK, FK | `res_groups_id` | integer | 4 B | No | Referencia a res_groups |

### `mail_compose_message`

**Asistente de redacción de correo electrónico** · modelo `mail.compose.message` · módulo `mail` · 37 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `template_id` | integer | 4 B | Sí | Utilizar plantilla → `mail_template` |
| FK | `parent_id` | integer | 4 B | Sí | Mensaje principal → `mail_message` |
| FK | `author_id` | integer | 4 B | Sí | Autor → `res_partner` — Autor del mensaje. Si no se establece, email_from puede contener una dirección de correo que no coincida con la de ningún contacto. |
| FK | `res_domain_user_id` | integer | 4 B | Sí | Responsable → `res_users` — Se utiliza como contexto para evaluar el dominio del redactor |
| FK | `record_alias_domain_id` | integer | 4 B | Sí | Dominio del alias → `mail_alias_domain` |
| FK | `record_company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `subtype_id` | integer | 4 B | Sí | Subtipo → `mail_message_subtype` |
| FK | `mail_activity_type_id` | integer | 4 B | Sí | Tipo de actividad del correo electrónico → `mail_activity_type` |
| FK | `mail_server_id` | integer | 4 B | Sí | Servidor de correo saliente → `ir_mail_server` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lang` | varchar | variable | Sí | Idioma — Idioma de traducción opcional (código ISO) a seleccionar al enviar un correo. Si no lo defines, el sistema usará el idioma principal del… |
|  | `subject` | varchar | variable | Sí | Asunto |
|  | `email_layout_xmlid` | varchar | variable | Sí | Diseño de notificación de correo electrónico |
|  | `email_from` | varchar | variable | Sí | Desde — Dirección de correo del remitente. Este campo se establece cuando no se encuentra ningún contacto coincidente y reemplaza el campo author… |
|  | `composition_mode` | varchar | variable | Sí | Modo de redacción |
|  | `composition_comment_option` | varchar | variable | Sí | Opciones de comentario |
|  | `model` | varchar | variable | Sí | Modelo de documento relacionado |
|  | `message_type` | varchar | variable | No | Tipo — Tipo de mensaje: correo electrónico para mensajes de correo electrónico, notificación para mensajes del sistema, comentario para otros ti… |
|  | `reply_to` | varchar | variable | Sí | Responder a — Dirección de correo electrónico de respuesta. Al configurar reply_to se anula la creación automática de hilos. |
|  | `scheduled_date` | varchar | variable | Sí | Fecha programada — En la modalidad de agregar comentarios: puede posponer el envío de notificaciones. En el modo de envíos masivos de correos: puede configu… |
|  | `template_name` | varchar | variable | Sí | Nombre de la plantilla |
|  | `body` | text | variable | Sí | Contenidos |
|  | `res_ids` | text | variable | Sí | IDs de los documentos relacionados |
|  | `res_domain` | text | variable | Sí | Dominio activo |
|  | `email_add_signature` | boolean | 1 B | Sí | Agregar firma |
|  | `reply_to_force_new` | boolean | 1 B | Sí | Considera las respuestas como un nuevo hilo — Gestione respuestas como correos electrónicos entrantes nuevos en lugar de respuestas al mismo hilo. |
|  | `auto_delete` | boolean | 1 B | Sí | Eliminar correos electrónicos — Esta opción elimina de forma permanente cualquier rastro del envío del correo, incluso del menú técnico en los ajustes, para preservar el… |
|  | `auto_delete_keep_log` | boolean | 1 B | Sí | Conservar copia del mensaje — Conservar una copia del contenido del correo electrónico si estos son eliminados (sólo envíos masivos) |
|  | `force_send` | boolean | 1 B | Sí | Enviar correo electrónico o notificaciones de forma directa |
|  | `notify_author` | boolean | 1 B | Sí | Notificar al autor |
|  | `notify_author_mention` | boolean | 1 B | Sí | Notificar mención del autor |
|  | `notify_skip_followers` | boolean | 1 B | Sí | Omitir notificación a seguidores |
|  | `use_exclusion_list` | boolean | 1 B | Sí | Usar lista de exclusión — Evitar enviar mensajes a contactos en la lista de exclusión. Desactívalo solo cuando sea absolutamente necesario. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_compose_message_ir_attachments_rel`

**Relación muchos a muchos entre «mail.compose.message» y «ir.attachment»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `wizard_id` | integer | 4 B | No | Referencia a mail_compose_message |
| PK, FK | `attachment_id` | integer | 4 B | No | Referencia a ir_attachment |

### `mail_compose_message_res_partner_rel`

**Relación muchos a muchos entre «mail.compose.message» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `wizard_id` | integer | 4 B | No | Referencia a mail_compose_message |
| PK, FK | `partner_id` | integer | 4 B | No | Referencia a res_partner |

### `mail_followers`

**Seguidores del documento** · modelo `mail.followers` · módulo `mail` · 4 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | Sí | ID del documento relacionado — ID del recurso seguido |
| FK | `partner_id` | integer | 4 B | No | Contacto relacionado → `res_partner` |
|  | `res_model` | varchar | variable | No | Nombre del modelo del documento relacionado |

### `mail_followers_edit`

**Asistente para editar seguidores** · modelo `mail.followers.edit` · módulo `mail` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | No | Modelo de documento relacionado — Modelo del recurso seguido |
|  | `res_ids` | varchar | variable | Sí | IDs de los documentos relacionados — ID de los recursos seguidos |
|  | `operation` | varchar | variable | No | Operación |
|  | `message` | text | variable | Sí | Mensaje |
|  | `notify` | boolean | 1 B | Sí | Notificar a los destinatarios |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_followers_edit_res_partner_rel`

**Relación muchos a muchos entre «mail.followers.edit» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_followers_edit_id` | integer | 4 B | No | Referencia a mail_followers_edit |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `mail_followers_mail_message_subtype_rel`

**Relación muchos a muchos entre «mail.followers» y «mail.message.subtype»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_followers_id` | integer | 4 B | No | Referencia a mail_followers |
| PK, FK | `mail_message_subtype_id` | integer | 4 B | No | Referencia a mail_message_subtype |

### `mail_gateway_allowed`

**Puerta de enlace de correo permitida** · modelo `mail.gateway.allowed` · módulo `mail` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email` | varchar | variable | No | Dirección de correo electrónico |
|  | `email_normalized` | varchar | variable | Sí | Correo electrónico normalizado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_guest`

**Invitado** · modelo `mail.guest` · módulo `mail` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `access_token` | varchar | variable | No | Token de acceso |
|  | `email` | varchar | variable | Sí | Correo electrónico |
|  | `lang` | varchar | variable | Sí | Idioma |
|  | `timezone` | varchar | variable | Sí | Zona horaria |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_ice_server`

**Servidor ICE** · modelo `mail.ice.server` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `server_type` | varchar | variable | No | Tipo |
|  | `uri` | varchar | variable | No | URI |
|  | `username` | varchar | variable | Sí | Nombre de usuario |
|  | `credential` | varchar | variable | Sí | Credencial |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_link_preview`

**Almacenar los datos de la vista previa del enlace** · modelo `mail.link.preview` · módulo `mail` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `source_url` | varchar | variable | No | URL |
|  | `og_type` | varchar | variable | Sí | Tipo |
|  | `og_title` | varchar | variable | Sí | Título |
|  | `og_site_name` | varchar | variable | Sí | Nombre del sitio |
|  | `og_image` | varchar | variable | Sí | Imagen |
|  | `og_mimetype` | varchar | variable | Sí | Tipo de MIME |
|  | `image_mimetype` | varchar | variable | Sí | Imagen tipo MIME |
|  | `og_description` | text | variable | Sí | Descripción |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_mail`

**Correos salientes** · modelo `mail.mail` · módulo `mail` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mail_message_id` | integer | 4 B | No | Mensaje → `mail_message` |
| FK | `fetchmail_server_id` | integer | 4 B | Sí | Servidor de correo entrante → `fetchmail_server` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email_cc` | varchar | variable | Sí | Cc — Destinatarios de la copia de carbón de los mensajes |
|  | `state` | varchar | variable | Sí | Estado |
|  | `failure_type` | varchar | variable | Sí | Tipo de error |
|  | `body_html` | text | variable | Sí | Contenidos del texto — Mensaje de texto enriquecido/HTML |
|  | `references` | text | variable | Sí | Referencias — Referencia de mensajes, como los identificadores de los mensajes anteriores |
|  | `headers` | text | variable | Sí | Cabeceras |
|  | `email_to` | text | variable | Sí | Para — Destinatarios del mensaje (correos electrónicos) |
|  | `failure_reason` | text | variable | Sí | Motivo del error — Motivo del error. Por lo general es la excepción lanzada por el servidor de correo electrónico y se almacena para facilitar la eliminació… |
|  | `is_notification` | boolean | 1 B | Sí | Correo electrónico de notificación — Se creó un correo para notificar a la gente de un mail.message existente |
|  | `auto_delete` | boolean | 1 B | Sí | Eliminar automáticamente — Esta opción elimina de forma permanente cualquier rastro del envío del correo, incluso del menú técnico en los ajustes, para preservar el… |
|  | `scheduled_date` | timestamp | 8 B | Sí | Fecha de envío programada — Si esta opción está activada, el administrador de tareas enviará el correo electrónico después de la fecha. Si no se activada, el correo… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_mail_res_partner_rel`

**Relación muchos a muchos entre «mail.mail» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_mail_id` | integer | 4 B | No | Referencia a mail_mail |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `mail_message`

**Mensaje** · modelo `mail.message` · módulo `mail` · 30 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_id` | integer | 4 B | Sí | Mensaje principal → `mail_message` |
|  | `res_id` | integer | 4 B | Sí | ID del documento relacionado |
| FK | `record_alias_domain_id` | integer | 4 B | Sí | Dominio del alias → `mail_alias_domain` |
| FK | `record_company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `subtype_id` | integer | 4 B | Sí | Subtipo → `mail_message_subtype` |
| FK | `mail_activity_type_id` | integer | 4 B | Sí | Tipo de actividad del correo electrónico → `mail_activity_type` |
| FK | `author_id` | integer | 4 B | Sí | Autor → `res_partner` — Autor del mensaje. Si no se establece, email_from puede contener una dirección de correo que no coincida con la de ningún contacto. |
| FK | `author_guest_id` | integer | 4 B | Sí | Invitado → `mail_guest` |
| FK | `mail_server_id` | integer | 4 B | Sí | Servidor de correo saliente → `ir_mail_server` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `subject` | varchar | variable | Sí | Asunto |
|  | `model` | varchar | variable | Sí | Modelo de documento relacionado |
|  | `message_type` | varchar | variable | No | Tipo — Se utiliza para categorizar el generador de mensajes. 'email': lo genera un correo electrónico entrante, por ejemplo, con una pasarela de… |
|  | `email_from` | varchar | variable | Sí | Desde — Dirección de correo del remitente. Este campo se establece cuando no se encuentra ningún contacto coincidente y reemplaza el campo author… |
|  | `incoming_email_cc` | varchar | variable | Sí | CC a los correos |
|  | `outgoing_email_to` | varchar | variable | Sí | Correos para |
|  | `message_id` | varchar | variable | Sí | Message-Id — Identificador único del mensaje |
|  | `reply_to` | varchar | variable | Sí | Responder a — Dirección de correo electrónico de respuesta. Al configurar reply_to se anula la creación automática de hilos. |
|  | `email_layout_xmlid` | varchar | variable | Sí | Diseño |
|  | `body` | text | variable | Sí | Contenidos |
|  | `incoming_email_to` | text | variable | Sí | Correos para |
|  | `is_internal` | boolean | 1 B | Sí | Solo para empleados — Ocultar a los usuarios públicos / del portal, independientemente de la configuración del subtipo. |
|  | `reply_to_force_new` | boolean | 1 B | Sí | No hay un hilo de respuestas — Si está marcado como verdadero, no se mostrarán las respuestas en el hilo de conversación del documento original. En su lugar, se comprob… |
|  | `email_add_signature` | boolean | 1 B | Sí | Agregar firma de correo electrónico |
|  | `date` | timestamp | 8 B | Sí | Fecha |
|  | `pinned_at` | timestamp | 8 B | Sí | Fijado — Fecha y hora en la que se ancló el mensaje |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_message_link_preview`

**Enlace entre la previsualización de enlaces y mensajes** · modelo `mail.message.link.preview` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `message_id` | integer | 4 B | No | Mensaje → `mail_message` |
| FK | `link_preview_id` | integer | 4 B | No | Previsualización del enlace → `mail_link_preview` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `is_hidden` | boolean | 1 B | Sí | Está oculto |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_message_reaction`

**Reacción de mensaje** · modelo `mail.message.reaction` · módulo `mail` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `message_id` | integer | 4 B | No | Mensaje → `mail_message` |
| FK | `partner_id` | integer | 4 B | Sí | Reacción del contacto → `res_partner` |
| FK | `guest_id` | integer | 4 B | Sí | Reacción del invitado → `mail_guest` |
|  | `content` | varchar | variable | No | Contenido |

### `mail_message_res_partner_rel`

**Relación muchos a muchos entre «mail.message» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_message_id` | integer | 4 B | No | Referencia a mail_message |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `mail_message_res_partner_starred_rel`

**Relación muchos a muchos entre «mail.message» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_message_id` | integer | 4 B | No | Referencia a mail_message |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `mail_message_schedule`

**Mensajes programados** · modelo `mail.message.schedule` · módulo `mail` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mail_message_id` | integer | 4 B | No | Mensaje → `mail_message` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `notification_parameters` | text | variable | Sí | Parámetro de notificación |
|  | `scheduled_datetime` | timestamp | 8 B | No | Fecha de envío programada — Fecha y hora en la que se debe enviar la notificación. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_message_subtype`

**Subtipos de mensaje** · modelo `mail.message.subtype` · módulo `mail` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_id` | integer | 4 B | Sí | Principal → `mail_message_subtype` — Subtipo principal, se utiliza para la suscripción automática. El nombre de este campo no es correcto. Por ejemplo, en un proyecto, el par… |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Se utiliza para ordenar los subtipos. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `relation_field` | varchar | variable | Sí | Campo de relación — Campo utilizado para vincular el modelo relacionado con el modelo de subtipo cuando se utiliza la suscripción automática en un documento… |
|  | `res_model` | varchar | variable | Sí | Modelo — Modelo al que aplica el subtipo. Si no está establecido, este subtipo aplica a todos los modelos. |
|  | `name` | jsonb | variable | No | Tipo de mensaje — El subtipo del mensaje indica con mayor precisión su tipo, en especial para las notificaciones del sistema. Por ejemplo, si es una notifi… |
|  | `description` | jsonb | variable | Sí | Descripción — Descripción que se agregará al mensaje mandado para este subtipo. Si no se llena, se pondrá el nombre en su lugar. |
|  | `internal` | boolean | 1 B | Sí | Solo para uso interno — Los mensajes con subtipos internos solo serán visibles para los empleados, es decir, los miembros del grupo base_user |
|  | `default` | boolean | 1 B | Sí | Predeterminado — Se activa automáticamente al suscribirse. |
|  | `hidden` | boolean | 1 B | Sí | Oculto — Ocultar el subtipo en las opciones del seguidor |
|  | `track_recipients` | boolean | 1 B | Sí | Rastrear destinatarios — Si desea mostrar todos los destinatarios o solo los importantes. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_message_translation`

**Traducción de mensajes** · modelo `mail.message.translation` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `message_id` | integer | 4 B | No | Mensaje → `mail_message` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `source_lang` | varchar | variable | No | Idioma de origen — Resultado de la detección del idioma según su contenido. |
|  | `target_lang` | varchar | variable | No | Idioma de destino — Language code used as the target for the translation request. |
|  | `body` | text | variable | No | Traducción del contenido — Cadena recibida de la solicitud de traducción. |
|  | `create_date` | timestamp | 8 B | Sí | Fecha de creación |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_notification`

**Notificaciones de mensajes** · modelo `mail.notification` · módulo `mail` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `author_id` | integer | 4 B | Sí | Autor → `res_partner` |
| FK | `mail_message_id` | integer | 4 B | No | Mensaje → `mail_message` |
| FK | `mail_mail_id` | integer | 4 B | Sí | Correo → `mail_mail` — ID de mail_mail opcional. Se utiliza principalmente para optimizar búsquedas. |
| FK | `res_partner_id` | integer | 4 B | Sí | Destinatario → `res_partner` |
|  | `mail_email_address` | varchar | variable | Sí | Enviar a dirección de correo — Dirección de correo del destinatario |
|  | `notification_type` | varchar | variable | No | Tipo de notificación |
|  | `notification_status` | varchar | variable | Sí | Estado |
|  | `failure_type` | varchar | variable | Sí | Tipo de error |
|  | `failure_reason` | text | variable | Sí | Motivo del error |
|  | `is_read` | boolean | 1 B | Sí | Se leyó |
|  | `read_date` | timestamp | 8 B | Sí | Fecha de lectura |
|  | `sms_id_int` | integer | 4 B | Sí | ID de SMS |
|  | `sms_number` | varchar | variable | Sí | Número SMS |
| FK | `letter_id` | integer | 4 B | Sí | Carta de correo postal → `snailmail_letter` |

### `mail_presence`

**Conexión del usuario/invitado** · modelo `mail.presence` · módulo `mail` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Usuarios → `res_users` |
| FK | `guest_id` | integer | 4 B | Sí | Invitado → `mail_guest` |
|  | `status` | varchar | variable | Sí | Estado de mensajería instantánea |
|  | `last_poll` | timestamp | 8 B | Sí | Última encuesta |
|  | `last_presence` | timestamp | 8 B | Sí | Última conexión |

### `mail_push`

**Notificaciones push** · modelo `mail.push` · módulo `mail` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mail_push_device_id` | integer | 4 B | No | dispositivos → `mail_push_device` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `payload` | text | variable | Sí | Carga efectiva |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_push_device`

**Dispositivo de notificación push** · modelo `mail.push.device` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | No | Contacto → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `endpoint` | varchar | variable | No | Punto de conexión del navegador |
|  | `keys` | varchar | variable | No | Claves del navegador — Se refiere a las claves del navegador que usa la notificación: - p256dh: es la clave pública de suscripción que genera el navegador. El n… |
|  | `expiration_time` | timestamp | 8 B | Sí | Fecha de expiración del token |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_scheduled_message`

**Mensaje programado** · modelo `mail.scheduled.message` · módulo `mail` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | No | ID del documento relacionado |
| FK | `author_id` | integer | 4 B | No | Autor → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `subject` | varchar | variable | Sí | Asunto |
|  | `composition_comment_option` | varchar | variable | Sí | Opciones de comentario |
|  | `model` | varchar | variable | No | Modelo de documento relacionado |
|  | `send_context` | jsonb | variable | Sí | Contexto del envío |
|  | `body` | text | variable | Sí | Contenidos |
|  | `notification_parameters` | text | variable | Sí | Parámetros de notificación |
|  | `is_note` | boolean | 1 B | Sí | Es una nota — Si el mensaje se registrará como una nota. |
|  | `scheduled_date` | timestamp | 8 B | No | Fecha programada |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_scheduled_message_res_partner_rel`

**Relación muchos a muchos entre «mail.scheduled.message» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_scheduled_message_id` | integer | 4 B | No | Referencia a mail_scheduled_message |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `mail_template`

**Plantillas de correo electrónico** · modelo `mail.template` · módulo `mail` · 26 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | Sí | Aplica a → `ir_model` |
| FK | `user_id` | integer | 4 B | Sí | Propietario → `res_users` |
| FK | `mail_server_id` | integer | 4 B | Sí | Servidor de correo saliente → `ir_mail_server` — Servidor preferido opcional para los correos salientes. Si no se establece, se utilizará el de mayor prioridad. |
| FK | `ref_ir_act_window` | integer | 4 B | Sí | Acción de la barra lateral → `ir_act_window` — Acción de la barra lateral para hacer disponible esta plantilla en los registros del modelo de documento relacionado |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `template_fs` | varchar | variable | Sí | Nombre del archivo de la plantilla — Archivo desde el que se origina la plantilla. Se utiliza para restablecer la plantilla rota. |
|  | `lang` | varchar | variable | Sí | Idioma — Idioma de traducción opcional (código ISO) a seleccionar al enviar un correo. Si no lo defines, el sistema usará el idioma principal del… |
|  | `model` | varchar | variable | Sí | Modelo de documento relacionado |
|  | `email_from` | varchar | variable | Sí | Enviar desde — Dirección del remitente (puedes usar marcadores de posición aquí). Si no la configuras, el valor predeterminado será el alias del correo… |
|  | `email_to` | varchar | variable | Sí | Para (correos electrónicos) — Direcciones de destinatarios separadas por comas (se pueden utilizar marcadores de posición aquí) |
|  | `partner_to` | varchar | variable | Sí | Para (contactos) — IDs de destinatarios separados por comas (se pueden utilizar marcadores de posición aquí) |
|  | `email_cc` | varchar | variable | Sí | Cc — Destinatarios de copias de carbón (se pueden utilizar marcadores de posición aquí) |
|  | `reply_to` | varchar | variable | Sí | Responder a — Dirección de correo electrónico a la que se redireccionarán las respuestas al enviar correos electrónicos masivos. Solo se utiliza cuando… |
|  | `email_layout_xmlid` | varchar | variable | Sí | Diseño de notificación de correo electrónico |
|  | `scheduled_date` | varchar | variable | Sí | Fecha programada — Si esta opción está activa, el administrador de tareas enviará el correo electrónico después de la fecha. Si no, el correo electrónico se… |
|  | `name` | jsonb | variable | Sí | Nombre |
|  | `description` | jsonb | variable | Sí | Descripción de la plantilla — Este campo se utiliza para la descripción interna del uso de la plantilla. |
|  | `subject` | jsonb | variable | Sí | Asunto — Asunto (se pueden utilizar marcadores de posición aquí) |
|  | `body_html` | jsonb | variable | Sí | Contenido |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `use_default_to` | boolean | 1 B | Sí | Destinatarios predeterminados — Destinatarios predeterminados del registro: - contacto (usa el ID del contacto o partner_id) O - correo electrónico (usa email_from o el… |
|  | `auto_delete` | boolean | 1 B | Sí | Eliminar automáticamente — Esta opción elimina de forma permanente cualquier rastro del envío del correo, incluso del menú técnico en los ajustes, para preservar el… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_template_ir_actions_report_rel`

**Relación muchos a muchos entre «mail.template» y «ir.actions.report»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_template_id` | integer | 4 B | No | Referencia a mail_template |
| PK, FK | `ir_actions_report_id` | integer | 4 B | No | Referencia a ir_act_report_xml |

### `mail_template_mail_template_reset_rel`

**Relación muchos a muchos entre «mail.template.reset» y «mail.template»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mail_template_reset_id` | integer | 4 B | No | Referencia a mail_template_reset |
| PK, FK | `mail_template_id` | integer | 4 B | No | Referencia a mail_template |

### `mail_template_preview`

**Vista previa de la plantilla del correo electrónico** · modelo `mail.template.preview` · módulo `mail` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mail_template_id` | integer | 4 B | No | Plantilla del correo relacionado → `mail_template` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `resource_ref` | varchar | variable | Sí | Registro |
|  | `lang` | varchar | variable | Sí | Idioma de vista previa de la plantilla |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_template_reset`

**Restablecer plantilla de correo** · modelo `mail.template.reset` · módulo `mail` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mail_tracking_value`

**Valor de seguimiento de correo** · modelo `mail.tracking.value` · módulo `mail` · 19 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `field_id` | integer | 4 B | Sí | Campo → `ir_model_fields` |
|  | `old_value_integer` | integer | 4 B | Sí | Valor antiguo Integer |
|  | `new_value_integer` | integer | 4 B | Sí | Nuevo valor Integer |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` — Se utiliza para mostrar la moneda al llevar seguimiento de los valores monetarios |
| FK | `mail_message_id` | integer | 4 B | No | ID del mensaje → `mail_message` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `old_value_char` | varchar | variable | Sí | Valor antiguo Char |
|  | `new_value_char` | varchar | variable | Sí | Nuevo carácter de valor |
|  | `field_info` | jsonb | variable | Sí | Información de campo eliminada |
|  | `old_value_text` | text | variable | Sí | Valor antiguo de texto |
|  | `new_value_text` | text | variable | Sí | Nuevo valor de texto |
|  | `old_value_datetime` | timestamp | 8 B | Sí | Valor antiguo DateTime |
|  | `new_value_datetime` | timestamp | 8 B | Sí | Nuevo valor de fecha y hora |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `old_value_float` | double precision | 8 B | Sí | Valor antiguo Float |
|  | `new_value_float` | double precision | 8 B | Sí | Nuevo valor Float |

### `message_attachment_rel`

**Relación muchos a muchos entre «mail.message» y «ir.attachment»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `message_id` | integer | 4 B | No | Referencia a mail_message |
| PK, FK | `attachment_id` | integer | 4 B | No | Referencia a ir_attachment |

### `res_role`

**Representa un rol en el sistema utilizado para categorizar a los usuarios. Cada rol tiene un nombre único y puede estar asociado a varios usuarios. Puede mencionar a los roles en los mensajes para notificar a todos los usuarios asociados.** · modelo `res.role` · módulo `mail` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_role_res_users_rel`

**Relación muchos a muchos entre «res.role» y «res.users»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `res_role_id` | integer | 4 B | No | Referencia a res_role |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `res_users_settings_volumes`

**Ajustes de volumen del usuario** · modelo `res.users.settings.volumes` · módulo `mail` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_setting_id` | integer | 4 B | No | Ajustes de usuario → `res_users_settings` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `guest_id` | integer | 4 B | Sí | Invitado → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `volume` | double precision | 8 B | Sí | Volumen — Rango entre 0.0 y 1.0, la escala depende de la implementación del navegador. |

### `scheduled_message_attachment_rel`

**Relación muchos a muchos entre «mail.scheduled.message» y «ir.attachment»** · tabla intermedia, sin modelo propio · módulo `mail` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `scheduled_message_id` | integer | 4 B | No | Referencia a mail_scheduled_message |
| PK, FK | `attachment_id` | integer | 4 B | No | Referencia a ir_attachment |

## Módulo `mrp`

### `change_production_qty`

**Cambiar cantidad de producción** · modelo `change.production.qty` · módulo `mrp` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mo_id` | integer | 4 B | No | Orden de fabricación → `mrp_production` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_qty` | numeric | variable | No | Cantidad a producir |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_bom_byproduct`

**Subproducto** · modelo `mrp.bom.byproduct` · módulo `mrp` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Subproducto → `product_product` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `bom_id` | integer | 4 B | Sí | Lista de materiales → `mrp_bom` |
| FK | `operation_id` | integer | 4 B | Sí | Producido en la operación → `mrp_routing_workcenter` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_qty` | numeric | variable | No | Cantidad |
|  | `cost_share` | numeric | variable | Sí | Reparto de costos (%) — El porcentaje del costo de producción final para esta línea de subproducto (dividido entre la cantidad producida). El total de reparto de… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_bom_byproduct_product_template_attribute_value_rel`

**Relación muchos a muchos entre «mrp.bom.byproduct» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_bom_byproduct_id` | integer | 4 B | No | Referencia a mrp_bom_byproduct |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `mrp_bom_line_product_template_attribute_value_rel`

**Relación muchos a muchos entre «mrp.bom.line» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_bom_line_id` | integer | 4 B | No | Referencia a mrp_bom_line |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `mrp_consumption_warning`

**Asistente en caso de consumo en advertencia/estricto y una mayor cantidad de componentes se han utilizado para una orden de fabricación (relacionado con la lista de materiales)** · modelo `mrp.consumption.warning` · módulo `mrp` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_consumption_warning_line`

**Línea de error de consumo** · modelo `mrp.consumption.warning.line` · módulo `mrp` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mrp_consumption_warning_id` | integer | 4 B | No | Asistente principal → `mrp_consumption_warning` |
| FK | `mrp_production_id` | integer | 4 B | No | Orden de fabricación → `mrp_production` |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `product_consumed_qty_uom` | double precision | 8 B | Sí | Consumido |
|  | `product_expected_qty_uom` | double precision | 8 B | Sí | Por consumir |

### `mrp_consumption_warning_mrp_production_rel`

**Relación muchos a muchos entre «mrp.consumption.warning» y «mrp.production»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_consumption_warning_id` | integer | 4 B | No | Referencia a mrp_consumption_warning |
| PK, FK | `mrp_production_id` | integer | 4 B | No | Referencia a mrp_production |

### `mrp_production_backorder`

**Asistente para marcar como hecho o crear una orden parcial** · modelo `mrp.production.backorder` · módulo `mrp` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_production_backorder_line`

**Línea de confirmación de órdenes parciales** · modelo `mrp.production.backorder.line` · módulo `mrp` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mrp_production_backorder_id` | integer | 4 B | No | Orden de fabricación pendiente → `mrp_production_backorder` |
| FK | `mrp_production_id` | integer | 4 B | No | Orden de fabricación → `mrp_production` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `to_backorder` | boolean | 1 B | Sí | Para hacer una orden parcial |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_production_group`

**Grupo de producción** · modelo `mrp.production.group` · módulo `mrp` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_production_group_rel`

**Relación muchos a muchos entre «mrp.production.group» y «mrp.production.group»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `parent_group_id` | integer | 4 B | No | Referencia a mrp_production_group |
| PK, FK | `child_group_id` | integer | 4 B | No | Referencia a mrp_production_group |

### `mrp_production_mrp_production_backorder_rel`

**Relación muchos a muchos entre «mrp.production.backorder» y «mrp.production»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_production_backorder_id` | integer | 4 B | No | Referencia a mrp_production_backorder |
| PK, FK | `mrp_production_id` | integer | 4 B | No | Referencia a mrp_production |

### `mrp_production_serials`

**Asigna números de serie a la orden de producción** · modelo `mrp.production.serials` · módulo `mrp` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `production_id` | integer | 4 B | Sí | Producción → `mrp_production` |
| FK | `workorder_id` | integer | 4 B | Sí | Orden de trabajo → `mrp_workorder` |
|  | `lot_quantity` | integer | 4 B | Sí | Cantidad de números de serie |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lot_name` | varchar | variable | Sí | Primer número de serie |
|  | `serial_numbers` | text | variable | Sí | Números de serie producidos |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_production_split`

**Asistente para dividir una producción** · modelo `mrp.production.split` · módulo `mrp` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `production_split_multi_id` | integer | 4 B | Sí | Dividir producciones → `mrp_production_split_multi` |
| FK | `production_id` | integer | 4 B | Sí | Orden de fabricación → `mrp_production` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_production_split_line`

**Detalle de división de producción** · modelo `mrp.production.split.line` · módulo `mrp` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mrp_production_split_id` | integer | 4 B | No | Dividir producción → `mrp_production_split` |
| FK | `user_id` | integer | 4 B | Sí | Responsable → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `quantity` | numeric | variable | No | Cantidad a producir |
|  | `date` | timestamp | 8 B | Sí | Fecha planificada |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_production_split_multi`

**Asistente para dividir varias producciones** · modelo `mrp.production.split.multi` · módulo `mrp` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_production_stock_lot_rel`

**Relación muchos a muchos entre «mrp.production» y «stock.lot»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_production_id` | integer | 4 B | No | Referencia a mrp_production |
| PK, FK | `stock_lot_id` | integer | 4 B | No | Referencia a stock_lot |

### `mrp_routing_workcenter_dependencies_rel`

**Relación muchos a muchos entre «mrp.routing.workcenter» y «mrp.routing.workcenter»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `operation_id` | integer | 4 B | No | Referencia a mrp_routing_workcenter |
| PK, FK | `blocked_by_id` | integer | 4 B | No | Referencia a mrp_routing_workcenter |

### `mrp_routing_workcenter_product_template_attribute_value_rel`

**Relación muchos a muchos entre «mrp.routing.workcenter» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_routing_workcenter_id` | integer | 4 B | No | Referencia a mrp_routing_workcenter |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `mrp_unbuild`

**Orden de desmontaje** · modelo `mrp.unbuild` · módulo `mrp` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `bom_id` | integer | 4 B | Sí | Lista de materiales → `mrp_bom` |
| FK | `mo_id` | integer | 4 B | Sí | Orden de fabricación → `mrp_production` |
| FK | `lot_id` | integer | 4 B | Sí | Número de serie/lote → `stock_lot` |
| FK | `location_id` | integer | 4 B | No | Ubicación de origen → `stock_location` — Ubicación del producto que desea desmantelar. |
| FK | `location_dest_id` | integer | 4 B | No | Ubicación de destino → `stock_location` — Ubicación donde desea enviar los componentes resultantes de la orden desensamblada. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Referencia |
|  | `state` | varchar | variable | Sí | Estado |
|  | `product_qty` | numeric | variable | No | Cantidad |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_workcenter_alternative_rel`

**Relación muchos a muchos entre «mrp.workcenter» y «mrp.workcenter»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `workcenter_id` | integer | 4 B | No | Referencia a mrp_workcenter |
| PK, FK | `alternative_workcenter_id` | integer | 4 B | No | Referencia a mrp_workcenter |

### `mrp_workcenter_capacity`

**Capacidad del centro de trabajo** · modelo `mrp.workcenter.capacity` · módulo `mrp` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `workcenter_id` | integer | 4 B | No | Centro de trabajo → `mrp_workcenter` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `capacity` | double precision | 8 B | Sí | Capacidad — Número de piezas que se puede producir al mismo tiempo de este producto, según la unidad. |
|  | `time_start` | double precision | 8 B | Sí | Tiempo de configuración (minutos) — Tiempo en minutos para la configuración. |
|  | `time_stop` | double precision | 8 B | Sí | Tiempo de limpieza (minutos) — Tiempo en minutos para la limpieza. |

### `mrp_workcenter_mrp_workcenter_tag_rel`

**Relación muchos a muchos entre «mrp.workcenter» y «mrp.workcenter.tag»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_workcenter_id` | integer | 4 B | No | Referencia a mrp_workcenter |
| PK, FK | `mrp_workcenter_tag_id` | integer | 4 B | No | Referencia a mrp_workcenter_tag |

### `mrp_workcenter_productivity`

**Registro de productividad del centro de trabajo** · modelo `mrp.workcenter.productivity` · módulo `mrp` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `workcenter_id` | integer | 4 B | No | Centro de trabajo → `mrp_workcenter` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `workorder_id` | integer | 4 B | Sí | Orden de trabajo → `mrp_workorder` |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` |
| FK | `loss_id` | integer | 4 B | No | Motivo de pérdida → `mrp_workcenter_productivity_loss` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `description` | text | variable | Sí | Descripción |
|  | `date_start` | timestamp | 8 B | No | Fecha de inicio |
|  | `date_end` | timestamp | 8 B | Sí | Fecha de finalización |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `duration` | double precision | 8 B | Sí | Duración |
| FK | `account_move_line_id` | integer | 4 B | Sí | Línea de movimiento de la cuenta → `account_move_line` |

### `mrp_workcenter_productivity_loss`

**Pérdidas de productividad en el centro de trabajo** · modelo `mrp.workcenter.productivity.loss` · módulo `mrp` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `loss_id` | integer | 4 B | Sí | Categoría → `mrp_workcenter_productivity_loss_type` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Motivo de bloqueo |
|  | `manual` | boolean | 1 B | Sí | Es un motivo de bloqueo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_workcenter_productivity_loss_type`

**Pérdidas de productividad en la orden de trabajo de planeación de recursos de fabricación** · modelo `mrp.workcenter.productivity.loss.type` · módulo `mrp` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `loss_type` | varchar | variable | No | Categoría |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_workcenter_tag`

**Agregar etiqueta para el centro de trabajo** · modelo `mrp.workcenter.tag` · módulo `mrp` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de la etiqueta |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_workorder_dependencies_rel`

**Relación muchos a muchos entre «mrp.workorder» y «mrp.workorder»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `workorder_id` | integer | 4 B | No | Referencia a mrp_workorder |
| PK, FK | `blocked_by_id` | integer | 4 B | No | Referencia a mrp_workorder |

### `mrp_workorder_mo_analytic_rel`

**Relación muchos a muchos entre «mrp.workorder» y «account.analytic.line»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_workorder_id` | integer | 4 B | No | Referencia a mrp_workorder |
| PK, FK | `account_analytic_line_id` | integer | 4 B | No | Referencia a account_analytic_line |

### `mrp_workorder_wc_analytic_rel`

**Relación muchos a muchos entre «mrp.workorder» y «account.analytic.line»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_workorder_id` | integer | 4 B | No | Referencia a mrp_workorder |
| PK, FK | `account_analytic_line_id` | integer | 4 B | No | Referencia a account_analytic_line |

### `stock_reference_production_rel`

**Relación muchos a muchos entre «mrp.production» y «stock.reference»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `production_id` | integer | 4 B | No | Referencia a mrp_production |
| PK, FK | `reference_id` | integer | 4 B | No | Referencia a stock_reference |

### `stock_warn_insufficient_qty_unbuild`

**Advertir cantidad insuficiente de desmontaje** · modelo `stock.warn.insufficient.qty.unbuild` · módulo `mrp` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `location_id` | integer | 4 B | No | Ubicación → `stock_location` |
| FK | `unbuild_id` | integer | 4 B | Sí | Desmantelar → `mrp_unbuild` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_uom_name` | varchar | variable | No | Unidad |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `quantity` | double precision | 8 B | No | Cantidad |

### `template_attribute_value_mrp_production_rel`

**Relación muchos a muchos entre «mrp.production» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `mrp` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `production_id` | integer | 4 B | No | Referencia a mrp_production |
| PK, FK | `template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

## Módulo `mrp_account`

### `mrp_account_wip_accounting`

**Asistente para publicar el movimiento de cuenta del trabajo de fabricación en curso** · modelo `mrp.account.wip.accounting` · módulo `mrp_account` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `journal_id` | integer | 4 B | No | Diario → `account_journal` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reference` | varchar | variable | Sí | Referencia |
|  | `date` | date | 4 B | Sí | Fecha |
|  | `reversal_date` | date | 4 B | No | Fecha de reversión |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_account_wip_accounting_line`

**Línea de movimiento de la cuenta a crear al registrar el movimiento de la cuenta de trabajo en curso** · modelo `mrp.account.wip.accounting.line` · módulo `mrp_account` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | Sí | Cuenta → `account_account` |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `wip_accounting_id` | integer | 4 B | Sí | Asistente de contabilidad para el trabajo en curso → `mrp_account_wip_accounting` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `label` | varchar | variable | Sí | Etiqueta |
|  | `debit` | numeric | variable | Sí | Deber |
|  | `credit` | numeric | variable | Sí | Haber |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `mrp_account_wip_accounting_mrp_production_rel`

**Relación muchos a muchos entre «mrp.account.wip.accounting» y «mrp.production»** · tabla intermedia, sin modelo propio · módulo `mrp_account` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `mrp_account_wip_accounting_id` | integer | 4 B | No | Referencia a mrp_account_wip_accounting |
| PK, FK | `mrp_production_id` | integer | 4 B | No | Referencia a mrp_production |

## Módulo `onboarding`

### `onboarding_onboarding`

**Integración** · modelo `onboarding.onboarding` · módulo `onboarding` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `route_name` | varchar | variable | No | Nombre de una sola palabra |
|  | `text_completed` | varchar | variable | Sí | Mensaje al terminar — Texto que aparece en la integración cuando se completa |
|  | `panel_close_action_name` | varchar | variable | Sí | Acción de cierre — Nombre de la acción del modelo de integración que se ejecutará al cerrar el panel. |
|  | `name` | jsonb | variable | Sí | Nombre de la integración |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `onboarding_onboarding_onboarding_onboarding_step_rel`

**Relación muchos a muchos entre «onboarding.onboarding» y «onboarding.onboarding.step»** · tabla intermedia, sin modelo propio · módulo `onboarding` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `onboarding_onboarding_id` | integer | 4 B | No | Referencia a onboarding_onboarding |
| PK, FK | `onboarding_onboarding_step_id` | integer | 4 B | No | Referencia a onboarding_onboarding_step |

### `onboarding_onboarding_step`

**Paso de integración** · modelo `onboarding.onboarding.step` · módulo `onboarding` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `done_icon` | varchar | variable | Sí | Icono de Font Awesome cuando se completa |
|  | `step_image_filename` | varchar | variable | Sí | Nombre del archivo de la imagen del paso |
|  | `panel_step_open_action_name` | varchar | variable | Sí | Acción de apertura — Nombre de la acción del modelo de paso de integración que se ejecutará al abrir el paso, por ejemplo, action_open_onboarding_1_step_1 |
|  | `title` | jsonb | variable | Sí | Título |
|  | `description` | jsonb | variable | Sí | Descripción |
|  | `button_text` | jsonb | variable | No | Texto del botón — Texto en el botón del panel para iniciar este paso |
|  | `done_text` | jsonb | variable | Sí | Texto a mostrar al completar el paso |
|  | `step_image_alt` | jsonb | variable | Sí | Texto alternativo para la imagen del paso — Mostrar cuando no es posible cargar la imagen |
|  | `is_per_company` | boolean | 1 B | Sí | Por empresa |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `onboarding_progress`

**Rastreador de progreso de integración** · modelo `onboarding.progress` · módulo `onboarding` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `onboarding_id` | integer | 4 B | No | Rastreador de integración relacionado → `onboarding_onboarding` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `onboarding_state` | varchar | variable | Sí | Progreso de integración |
|  | `is_onboarding_closed` | boolean | 1 B | Sí | ¿Se cerró el panel? |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `onboarding_progress_onboarding_progress_step_rel`

**Relación muchos a muchos entre «onboarding.progress» y «onboarding.progress.step»** · tabla intermedia, sin modelo propio · módulo `onboarding` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `onboarding_progress_id` | integer | 4 B | No | Referencia a onboarding_progress |
| PK, FK | `onboarding_progress_step_id` | integer | 4 B | No | Referencia a onboarding_progress_step |

### `onboarding_progress_step`

**Rastreador de los pasos del progreso de integración** · modelo `onboarding.progress.step` · módulo `onboarding` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `step_id` | integer | 4 B | No | Paso de integración → `onboarding_onboarding_step` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `step_state` | varchar | variable | Sí | Progreso del paso de integración |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `payment`

### `payment_capture_wizard`

**Asistente de captura de pagos** · modelo `payment.capture.wizard` · módulo `payment` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `amount_to_capture` | numeric | variable | Sí | Importe a capturar |
|  | `void_remaining_amount` | boolean | 1 B | Sí | Importe restante nulo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `payment_capture_wizard_payment_transaction_rel`

**Relación muchos a muchos entre «payment.capture.wizard» y «payment.transaction»** · tabla intermedia, sin modelo propio · módulo `payment` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `payment_capture_wizard_id` | integer | 4 B | No | Referencia a payment_capture_wizard |
| PK, FK | `payment_transaction_id` | integer | 4 B | No | Referencia a payment_transaction |

### `payment_country_rel`

**Relación muchos a muchos entre «payment.provider» y «res.country»** · tabla intermedia, sin modelo propio · módulo `payment` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `payment_id` | integer | 4 B | No | Referencia a payment_provider |
| PK, FK | `country_id` | integer | 4 B | No | Referencia a res_country |

### `payment_currency_rel`

**Relación muchos a muchos entre «payment.provider» y «res.currency»** · tabla intermedia, sin modelo propio · módulo `payment` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `payment_provider_id` | integer | 4 B | No | Referencia a payment_provider |
| PK, FK | `currency_id` | integer | 4 B | No | Referencia a res_currency |

### `payment_link_wizard`

**Generar enlace de pago de ventas** · modelo `payment.link.wizard` · módulo `payment` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | No | ID del documento relacionado |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | No | Modelo de documento relacionado |
|  | `amount` | numeric | variable | No | Importe |
|  | `amount_max` | numeric | variable | Sí | Cantidad máxima |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `discount_date` | date | 4 B | Sí | Fecha de descuento |
|  | `open_installments` | jsonb | variable | Sí | Open Installments |
|  | `has_eligible_epd` | boolean | 1 B | Sí | Tiene un descuento elegible por pago anticipado |
|  | `amount_paid` | numeric | variable | Sí | Pagado |
|  | `prepayment_amount` | numeric | variable | Sí | Importe de pago anticipado |

### `payment_method`

**Método de pago** · modelo `payment.method` · módulo `payment` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `primary_payment_method_id` | integer | 4 B | Sí | Método de pago primario → `payment_method` — El método de pago primario del método de pago actual, si el último es una marca. Por ejemplo, "Tarjeta" es el método de pago primario par… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | No | Código — El código técnico para este método de pago. |
|  | `support_manual_capture` | varchar | variable | No | Captura manual — El pago se autoriza y captura en dos pasos en lugar de solo en uno. |
|  | `support_refund` | varchar | variable | No | Reembolso — El reembolso es una función que le permite hacerle un reembolso al cliente directamente desde el pago en Odoo. |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `support_tokenization` | boolean | 1 B | Sí | Tokenización — La tokenización es el proceso en el que guarda los detalles de pago como un token que luego puede usar varias veces sin tener que escribi… |
|  | `support_express_checkout` | boolean | 1 B | Sí | Pago exprés — El pago exprés le permite a los clientes pagar más rápido usando un método de pago que proporciona toda la información necesaria para la… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `payment_method_payment_provider_rel`

**Relación muchos a muchos entre «payment.method» y «payment.provider»** · tabla intermedia, sin modelo propio · módulo `payment` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `payment_method_id` | integer | 4 B | No | Referencia a payment_method |
| PK, FK | `payment_provider_id` | integer | 4 B | No | Referencia a payment_provider |

### `payment_method_res_country_rel`

**Relación muchos a muchos entre «payment.method» y «res.country»** · tabla intermedia, sin modelo propio · módulo `payment` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `payment_method_id` | integer | 4 B | No | Referencia a payment_method |
| PK, FK | `res_country_id` | integer | 4 B | No | Referencia a res_country |

### `payment_method_res_currency_rel`

**Relación muchos a muchos entre «payment.method» y «res.currency»** · tabla intermedia, sin modelo propio · módulo `payment` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `payment_method_id` | integer | 4 B | No | Referencia a payment_method |
| PK, FK | `res_currency_id` | integer | 4 B | No | Referencia a res_currency |

### `payment_provider`

**Proveedor de pago** · modelo `payment.provider` · módulo `payment` · 27 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Defina el orden de visualización |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `redirect_form_view_id` | integer | 4 B | Sí | Plantilla de formulario de redirección → `ir_ui_view` — La plantilla que representa un formulario enviado para redireccionar al usuario al realizar un pago |
| FK | `inline_form_view_id` | integer | 4 B | Sí | Plantilla de formulario en línea → `ir_ui_view` — La plantilla que muestra el formulario de pago en línea cuando se realiza un pago directo |
| FK | `token_inline_form_view_id` | integer | 4 B | Sí | Plantilla de formulario en línea de token → `ir_ui_view` — La plantilla que muestra el formulario de pago en línea cuando se realiza un pago con token. |
| FK | `express_checkout_form_view_id` | integer | 4 B | Sí | Plantilla de formulario de pago rápido → `ir_ui_view` — La plantilla que representa el formulario de los métodos de pago rápido. |
|  | `color` | integer | 4 B | Sí | Color — El color de la tarjeta en la vista de kanban |
| FK | `module_id` | integer | 4 B | Sí | Módulo correspondiente → `ir_module_module` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `code` | varchar | variable | No | Código — El código técnico de este proveedor de pagos. |
|  | `state` | varchar | variable | No | Estado — En el modo de prueba, se procesa un pago falso a través de una interfaz de pago de prueba. Este modo se recomienda al establecer el métod… |
|  | `name` | jsonb | variable | No | Nombre |
|  | `pre_msg` | jsonb | variable | Sí | Mensaje de ayuda — El mensaje que aparece para explicar y ayudar al proceso de pago |
|  | `pending_msg` | jsonb | variable | Sí | Mensaje pendiente — El mensaje que aparece si la orden esta pendiente después del proceso de pago |
|  | `auth_msg` | jsonb | variable | Sí | Mensaje de autorización — El mensaje que aparece si se autoriza el pago |
|  | `done_msg` | jsonb | variable | Sí | Mensaje de finalización — El mensaje que aparece si la orden se realiza con éxito después del proceso de pago |
|  | `cancel_msg` | jsonb | variable | Sí | Mensaje cancelado — El mensaje mostrado si la orden se cancela durante el proceso de pago |
|  | `maximum_amount` | numeric | variable | Sí | Monto máximo — El importe máximo de pago para el que está disponible este proveedor de pagos. Si desea que esté disponible para cualquier importe, deje… |
|  | `is_published` | boolean | 1 B | Sí | Publicado — Si el proveedor se encuentra visible en el sitio web o no. Los tokens siguen funcionando pero solo son visibles en los formularios. |
|  | `allow_tokenization` | boolean | 1 B | Sí | Permitir guardar métodos de pago — Controla si los clientes pueden guardar sus métodos de pago como tokens de pago. Un token de pago es un enlace anónimo a los detalles de… |
|  | `capture_manually` | boolean | 1 B | Sí | Capturar el importe de forma manual — Capturar el importe de Odoo cuando se complete la entrega. Utilícelo si desea hacer el cargo a la tarjeta de sus clientes solo cuando est… |
|  | `allow_express_checkout` | boolean | 1 B | Sí | Permitir pago exprés — Determina si los clientes pueden utilizar métodos de pago rápido. El pago rápido permite que los clientes paguen con Google Pay y Apple P… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `so_reference_type` | varchar | variable | Sí | Comunicación — Puede establecer aquí el tipo de comunicación que aparecerá en las órdenes de venta. El cliente recibirá esta comunicación cuando selecci… |

### `payment_token`

**Token de pago** · modelo `payment.token` · módulo `payment` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `provider_id` | integer | 4 B | No | Proveedor → `payment_provider` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `payment_method_id` | integer | 4 B | No | Método de pago → `payment_method` |
| FK | `partner_id` | integer | 4 B | No | Contacto → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `payment_details` | varchar | variable | Sí | Detalles de pago — La parte clara de los datos de pago del método de pago. |
|  | `provider_ref` | varchar | variable | No | Referencia del proveedor — La referencia del proveedor del token de la transacción. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `payment_transaction`

**Transacción de pago** · modelo `payment.transaction` · módulo `payment` · 34 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `provider_id` | integer | 4 B | No | Proveedor → `payment_provider` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `payment_method_id` | integer | 4 B | No | Método de pago → `payment_method` |
| FK | `currency_id` | integer | 4 B | No | Moneda → `res_currency` |
| FK | `token_id` | integer | 4 B | Sí | Token de pago → `payment_token` |
| FK | `source_transaction_id` | integer | 4 B | Sí | Origen de la transacción → `payment_transaction` — La transacción fuente de la transacción hija |
| FK | `partner_id` | integer | 4 B | No | Cliente → `res_partner` |
| FK | `partner_state_id` | integer | 4 B | Sí | Estado → `res_country_state` |
| FK | `partner_country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `reference` | varchar | variable | No | Referencia — La referencia interna de la transacción |
|  | `provider_reference` | varchar | variable | Sí | Referencia del proveedor — La referencia de proveedor de pago de la transacción |
|  | `state` | varchar | variable | No | Estado |
|  | `operation` | varchar | variable | Sí | Operación |
|  | `landing_route` | varchar | variable | Sí | Ruta de destino — La ruta del usuario se redirecciona a después de la transacción |
|  | `partner_name` | varchar | variable | Sí | Nombre del contacto |
|  | `partner_lang` | varchar | variable | Sí | Idioma |
|  | `partner_email` | varchar | variable | Sí | Correo electrónico |
|  | `partner_address` | varchar | variable | Sí | Dirección |
|  | `partner_zip` | varchar | variable | Sí | Zip Code |
|  | `partner_city` | varchar | variable | Sí | Ciudad |
|  | `partner_phone` | varchar | variable | Sí | Teléfono |
|  | `state_message` | text | variable | Sí | Mensaje — El mensaje de información complementaria sobre el estado |
|  | `amount` | numeric | variable | No | Importe |
|  | `is_live` | boolean | 1 B | Sí | Entorno de producción — Indica si la transacción ocurrió en un entorno de producción. Su estado será falso para las transacciones creadas antes de implementar es… |
|  | `is_post_processed` | boolean | 1 B | Sí | Posprocesado — ¿Se posproceso el pago? |
|  | `tokenize` | boolean | 1 B | Sí | Crear token — Si se debe crear un token de pago al posprocesar la transacción |
|  | `last_state_change` | timestamp | 8 B | Sí | Última fecha de cambio de estado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `payment_id` | integer | 4 B | Sí | Pago → `account_payment` |
| FK | `pos_order_id` | integer | 4 B | Sí | Orden del PdV → `pos_order` — La orden del punto de venta que está vinculada a la transacción de pago |

### `sale_order_transaction_rel`

**Relación muchos a muchos entre «payment.transaction» y «sale.order»** · tabla intermedia, sin modelo propio · módulo `payment` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `transaction_id` | integer | 4 B | No | Referencia a payment_transaction |
| PK, FK | `sale_order_id` | integer | 4 B | No | Referencia a sale_order |

## Módulo `phone_validation`

### `phone_blacklist`

**Lista de exclusión de números telefónicos** · modelo `phone.blacklist` · módulo `phone_validation` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `number` | varchar | variable | No | Número de teléfono — El número debe tener formato E164 |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `phone_blacklist_remove`

**Eliminar teléfono de la lista de exclusión** · modelo `phone.blacklist.remove` · módulo `phone_validation` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `phone` | varchar | variable | No | Número de teléfono |
|  | `reason` | varchar | variable | Sí | Motivo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `point_of_sale`

### `account_fiscal_position_pos_config_rel`

**Relación muchos a muchos entre «pos.config» y «account.fiscal.position»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `account_fiscal_position_id` | integer | 4 B | No | Referencia a account_fiscal_position |

### `payment_provider_pos_payment_method_rel`

**Relación muchos a muchos entre «pos.payment.method» y «payment.provider»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_payment_method_id` | integer | 4 B | No | Referencia a pos_payment_method |
| PK, FK | `payment_provider_id` | integer | 4 B | No | Referencia a payment_provider |

### `pos_bill`

**Monedas/billetes** · modelo `pos.bill` · módulo `point_of_sale` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Nombre |
|  | `value` | numeric | variable | No | Valor |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_bill_pos_config_rel`

**Relación muchos a muchos entre «pos.bill» y «pos.config»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `pos_bill_id` | integer | 4 B | No | Referencia a pos_bill |

### `pos_category`

**Categoría de Punto de venta** · modelo `pos.category` · módulo `point_of_sale` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_id` | integer | 4 B | Sí | Categoría principal → `pos_category` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Indica el orden de secuencia cuando se muestra una lista de categorías de producto. |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre de la categoría |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `hour_until` | double precision | 8 B | Sí | Disponible hasta — El producto estará disponible hasta esta hora para las órdenes en línea y de autopedido. |
|  | `hour_after` | double precision | 8 B | Sí | Disponible después de — El producto estará disponible después de esta hora para las órdenes en línea y de autopedido. |

### `pos_category_pos_config_rel`

**Relación muchos a muchos entre «pos.config» y «pos.category»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `pos_category_id` | integer | 4 B | No | Referencia a pos_category |

### `pos_close_session_wizard`

**Asistente para cerrar sesión** · modelo `pos.close.session.wizard` · módulo `point_of_sale` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | Sí | Cuenta destino → `account_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `message` | text | variable | Sí | Mensaje de información |
|  | `account_readonly` | boolean | 1 B | Sí | La cuenta destino es de solo lectura |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `amount_to_balance` | double precision | 8 B | Sí | Importe por balancear |

### `pos_config`

**Configuración del punto de venta** · modelo `pos.config` · módulo `point_of_sale` · 74 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `picking_type_id` | integer | 4 B | No | Tipo de operación → `stock_picking_type` |
| FK | `journal_id` | integer | 4 B | Sí | Diario del Punto de venta → `account_journal` — Diario contable que se utiliza para registrar asientos contables de sesiones de PdV y pagos de factura de PdV. |
| FK | `invoice_journal_id` | integer | 4 B | Sí | Diario de factura → `account_journal` — Diario contable que se utiliza para crear facturas. |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `order_seq_id` | integer | 4 B | Sí | Secuencia de la orden → `ir_sequence` |
| FK | `order_backend_seq_id` | integer | 4 B | Sí | Secuencia del backend de la orden → `ir_sequence` |
| FK | `order_line_seq_id` | integer | 4 B | Sí | Secuencia de la línea de la orden → `ir_sequence` |
| FK | `device_seq_id` | integer | 4 B | Sí | Secuencia del dispositivo → `ir_sequence` |
| FK | `pricelist_id` | integer | 4 B | Sí | Lista de precios predeterminada → `product_pricelist` — La lista de precios que se utiliza si no se selecciona un cliente o si los clientes no tienen una lista de precios de venta configurada. |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `group_pos_manager_id` | integer | 4 B | Sí | Grupo de gerente de Punto de venta → `res_groups` — Este campo se encuentra aquí para pasar el identificador del grupo de gerentes del PdV al cliente del punto de venta. |
| FK | `group_pos_user_id` | integer | 4 B | Sí | Grupo de usuario del Punto de venta → `res_groups` — Este campo se encuentra aquí para pasar el identificador del grupo de usuarios del punto de venta al cliente del punto de venta. |
| FK | `tip_product_id` | integer | 4 B | Sí | Producto de propina → `product_product` — Este producto se utiliza como referencia en los recibos del cliente. |
| FK | `default_fiscal_position_id` | integer | 4 B | Sí | Posición fiscal predeterminada → `account_fiscal_position` |
| FK | `default_preset_id` | integer | 4 B | Sí | Ajuste preestablecido predeterminado → `pos_preset` |
| FK | `rounding_method` | integer | 4 B | Sí | Redondeo de efectivo → `account_cash_rounding` |
| FK | `warehouse_id` | integer | 4 B | Sí | Almacén → `stock_warehouse` |
| FK | `route_id` | integer | 4 B | Sí | Especifique la ruta para entregar los productos más tarde. → `stock_route` |
| FK | `fallback_nomenclature_id` | integer | 4 B | Sí | Nomenclatura alternativa → `barcode_nomenclature` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_token` | varchar | variable | Sí | Token de acceso |
|  | `name` | varchar | variable | No | Punto de venta — Una identificación interna del punto de venta. |
|  | `iface_tax_included` | varchar | variable | No | Mostrar impuestos |
|  | `customer_display_bg_img_name` | varchar | variable | Sí | Nombre de la imagen de fondo |
|  | `proxy_ip` | varchar | 45 | Sí | Dirección IP — El nombre de host o la dirección IP del proxy de hardware. Se detectarán en automático si los campos están vacíos. |
|  | `uuid` | varchar | variable | Sí | UUID — Un identificador único global para esta configuración del PdV, se usa para prevenir conflictos en datos que el cliente genere. |
|  | `picking_policy` | varchar | variable | No | Política de envío — Si entregas todos los productos al mismo tiempo, la orden de entrega se programará según el mayor plazo de entrega del producto. De lo co… |
|  | `epson_printer_ip` | varchar | variable | Sí | Dirección IP de la impresora Epson — Dirección IP local de una impresora de recibos Epson o su número de serie si la opción "Actualización automática de certificados" está ac… |
|  | `receipt_header` | text | variable | Sí | Encabezado del recibo — Un texto corto que se insertará como encabezado de página en el recibo impreso. |
|  | `receipt_footer` | text | variable | Sí | Pie del recibo — Un texto corto que se insertará como pie de página en el recibo impreso. |
|  | `is_order_printer` | boolean | 1 B | Sí | Impresora de pedidos |
|  | `iface_cashdrawer` | boolean | 1 B | Sí | Caja registradora — Abrir la caja registradora de forma automática. |
|  | `iface_electronic_scale` | boolean | 1 B | Sí | Báscula electrónica — Habilita la integración de una báscula electrónica. |
|  | `iface_print_via_proxy` | boolean | 1 B | Sí | Imprimir vía proxy — Evite la impresión con el navegador e imprima mediante el proxy de hardware. |
|  | `iface_scan_via_proxy` | boolean | 1 B | Sí | Escanear vía proxy — Habilite el escaneo de código de barras con un lector de código de barras remoto y lea las tarjetas con un lector de tarjetas de Vantiv. |
|  | `iface_big_scrollbars` | boolean | 1 B | Sí | Barras de desplazamiento grandes — Para pantallas táctiles industriales imprecisas |
|  | `iface_group_by_categ` | boolean | 1 B | Sí | Agrupar productos por categorías — Muestra los productos agrupados por categorías. |
|  | `iface_print_auto` | boolean | 1 B | Sí | Impresión automática de recibos — El recibo se imprimirá automáticamente al final de cada orden. |
|  | `iface_print_skip_screen` | boolean | 1 B | Sí | Saltar pantalla de vista previa — Se omitirá la pantalla de recibo si el recibo se puede imprimir de forma automática. |
|  | `restrict_price_control` | boolean | 1 B | Sí | Restringir las modificaciones de los precios a los gerentes — Solo los usuarios con permisos de acceso de gerente en la aplicación Punto de Venta pueden modificar los precios de los productos en las… |
|  | `is_margins_costs_accessible_to_every_user` | boolean | 1 B | Sí | Márgenes y costos — Cuando se deshabilita, solo el gerente de PdV puede ver el margen y el costo del producto entre la información del producto. |
|  | `set_maximum_difference` | boolean | 1 B | Sí | Establecer la diferencia máxima — Defina la diferencia máxima permitida entre el dinero esperado y el dinero contado al cierre de la sesión |
|  | `basic_receipt` | boolean | 1 B | Sí | Recibo básico — Imprima un recibo básico sin precios. Es útil para regalos. |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `iface_tipproduct` | boolean | 1 B | Sí | Propinas de productos |
|  | `use_pricelist` | boolean | 1 B | Sí | Utilice una lista de precios. |
|  | `use_presets` | boolean | 1 B | Sí | Usar ajustes preestablecidos |
|  | `tax_regime_selection` | boolean | 1 B | Sí | Valor de la selección del régimen fiscal |
|  | `limit_categories` | boolean | 1 B | Sí | Restringir categorías |
|  | `module_pos_restaurant` | boolean | 1 B | Sí | Es un bar/restaurante |
|  | `module_pos_avatax` | boolean | 1 B | Sí | Integración entre AvaTax y PdV — Use el mapeo automático de impuestos con AvaTax en PdV |
|  | `module_pos_discount` | boolean | 1 B | Sí | Descuentos globales |
|  | `module_pos_appointment` | boolean | 1 B | Sí | Reservas en línea |
|  | `is_posbox` | boolean | 1 B | Sí | PosBox |
|  | `is_header_or_footer` | boolean | 1 B | Sí | Encabezado y pie de página personalizados |
|  | `module_pos_hr` | boolean | 1 B | Sí | Módulo PdV RR. HH. — Mostrar pantalla de inicio de sesión de empleado |
|  | `other_devices` | boolean | 1 B | Sí | Otros dispositivos — Conectar dispositivos a su PdV sin una caja IoT. |
|  | `cash_rounding` | boolean | 1 B | Sí | Redondeo de efectivo |
|  | `only_round_cash_method` | boolean | 1 B | Sí | Aplicar redondeo solamente en efectivo |
|  | `manual_discount` | boolean | 1 B | Sí | Descuentos por línea |
|  | `ship_later` | boolean | 1 B | Sí | Enviar después |
|  | `auto_validate_terminal_payment` | boolean | 1 B | Sí | Validar automáticamente el pago por terminal — Valide las órdenes pagadas con una terminal de pago en automático |
|  | `show_product_images` | boolean | 1 B | Sí | Mostrar imágenes del producto — Mostrar imágenes del producto en la interfaz del punto de venta. |
|  | `show_category_images` | boolean | 1 B | Sí | Mostrar imágenes de la categoría — Mostrar imágenes de la categoría en la interfaz del punto de venta. |
|  | `module_pos_sms` | boolean | 1 B | Sí | Envío por SMS — Active la función de SMS para point_of_sale |
|  | `is_closing_entry_by_product` | boolean | 1 B | Sí | Asiento de cierre por producto — Muestre el desglose de las líneas de venta por producto en la entrada de cierre que se genera en automático. |
|  | `order_edit_tracking` | boolean | 1 B | Sí | Llevar seguimiento de la edición de las órdenes — Almacene las órdenes editadas en el backend |
|  | `use_fast_payment` | boolean | 1 B | Sí | Validación rápida de pagos — Activa métodos de pago rápido para validar las órdenes en la pantalla de productos. |
|  | `last_data_change` | timestamp | 8 B | Sí | Fecha de la última edición |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `amount_authorized_diff` | double precision | 8 B | Sí | Importe de la diferencia permitida — Este campo representa la diferencia máxima permitida entre el saldo final y el efectivo teórico al cerrar una sesión, para usuarios no ad… |

### `pos_config_pos_note_rel`

**Relación muchos a muchos entre «pos.config» y «pos.note»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `pos_note_id` | integer | 4 B | No | Referencia a pos_note |

### `pos_config_pos_payment_method_rel`

**Relación muchos a muchos entre «pos.config» y «pos.payment.method»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `pos_payment_method_id` | integer | 4 B | No | Referencia a pos_payment_method |

### `pos_config_pos_preset_rel`

**Relación muchos a muchos entre «pos.config» y «pos.preset»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `pos_preset_id` | integer | 4 B | No | Referencia a pos_preset |

### `pos_config_printer_rel`

**Relación muchos a muchos entre «pos.config» y «pos.printer»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `printer_id` | integer | 4 B | No | Referencia a pos_printer |
| PK, FK | `config_id` | integer | 4 B | No | Referencia a pos_config |

### `pos_config_product_pricelist_rel`

**Relación muchos a muchos entre «pos.config» y «product.pricelist»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `product_pricelist_id` | integer | 4 B | No | Referencia a product_pricelist |

### `pos_config_trust_relation`

**Relación muchos a muchos entre «pos.config» y «pos.config»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `is_trusting` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `is_trusted` | integer | 4 B | No | Referencia a pos_config |

### `pos_confirmation_wizard`

**Asistente de confirmación** · modelo `pos.confirmation.wizard` · módulo `point_of_sale` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `message` | text | variable | Sí | Mensaje |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_daily_sales_reports_wizard`

**Reporte diario del Punto de venta** · modelo `pos.daily.sales.reports.wizard` · módulo `point_of_sale` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `pos_session_id` | integer | 4 B | No | Sesión de PdV → `pos_session` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `add_report_per_employee` | boolean | 1 B | Sí | Agregue un reporte para cada empleado |

### `pos_detail_configs`

**Relación muchos a muchos entre «pos.details.wizard» y «pos.config»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_details_wizard_id` | integer | 4 B | No | Referencia a pos_details_wizard |
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |

### `pos_details_wizard`

**Reporte de detalles de Punto de venta** · modelo `pos.details.wizard` · módulo `point_of_sale` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `start_date` | timestamp | 8 B | No | Fecha de inicio |
|  | `end_date` | timestamp | 8 B | No | Fecha de finalización |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_hr_advanced_employee_hr_employee`

**Relación muchos a muchos entre «pos.config» y «hr.employee»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `hr_employee_id` | integer | 4 B | No | Referencia a hr_employee |

### `pos_hr_basic_employee_hr_employee`

**Relación muchos a muchos entre «pos.config» y «hr.employee»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `hr_employee_id` | integer | 4 B | No | Referencia a hr_employee |

### `pos_hr_minimal_employee_hr_employee`

**Relación muchos a muchos entre «pos.config» y «hr.employee»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `hr_employee_id` | integer | 4 B | No | Referencia a hr_employee |

### `pos_make_invoice`

**Creación de factura para varias órdenes** · modelo `pos.make.invoice` · módulo `point_of_sale` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `consolidated_billing` | boolean | 1 B | Sí | Facturación consolidada — Crea una factura para todas las órdenes relacionadas con el mismo cliente y la misma dirección de facturación |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_make_payment`

**Asistente de pago de Punto de venta** · modelo `pos.make.payment` · módulo `point_of_sale` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `config_id` | integer | 4 B | No | Configuración del punto de venta → `pos_config` |
| FK | `payment_method_id` | integer | 4 B | No | Método de pago → `pos_payment_method` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `payment_name` | varchar | variable | Sí | Referencia de pago |
|  | `amount` | numeric | variable | No | Importe |
|  | `payment_date` | timestamp | 8 B | No | Fecha de pago |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_note`

**Nota del PdV** · modelo `pos.note` · módulo `point_of_sale` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_order_line`

**Líneas de orden del Punto de venta** · modelo `pos.order.line` · módulo `point_of_sale` · 28 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `order_id` | integer | 4 B | No | Ref. de la orden → `pos_order` |
| FK | `refunded_orderline_id` | integer | 4 B | Sí | Línea de orden reembolsada → `pos_order_line` — Si esta línea de orden es un reembolso entonces se especifica la línea de orden reembolsada en este campo. |
| FK | `combo_parent_id` | integer | 4 B | Sí | Combo principal → `pos_order_line` |
| FK | `combo_item_id` | integer | 4 B | Sí | Artículo del combo → `product_combo_item` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Número de línea |
|  | `notice` | varchar | variable | Sí | Nota de descuento |
|  | `price_type` | varchar | variable | Sí | Tipo de precio |
|  | `full_product_name` | varchar | variable | Sí | Nombre completo del producto |
|  | `customer_note` | varchar | variable | Sí | Nota para el cliente |
|  | `uuid` | varchar | variable | Sí | UUID |
|  | `note` | varchar | variable | Sí | Nota del producto |
|  | `extra_tax_data` | jsonb | variable | Sí | Datos adicionales sobre impuestos |
|  | `price_unit` | numeric | variable | Sí | Precio unitario |
|  | `qty` | numeric | variable | Sí | Cantidad |
|  | `price_subtotal` | numeric | variable | No | Impuestos excl. |
|  | `price_subtotal_incl` | numeric | variable | No | Impuestos incl. |
|  | `total_cost` | numeric | variable | Sí | Costo total |
|  | `discount` | numeric | variable | Sí | Descuento (%) |
|  | `is_total_cost_computed` | boolean | 1 B | Sí | Costo total calculado — Permite saber si ya se calculó el costo total |
|  | `is_edited` | boolean | 1 B | Sí | Editado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `price_extra` | double precision | 8 B | Sí | Precio adicional |

### `pos_order_line_product_template_attribute_value_rel`

**Relación muchos a muchos entre «pos.order.line» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_order_line_id` | integer | 4 B | No | Referencia a pos_order_line |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `pos_pack_operation_lot`

**Especifique el número de lote/de serie en la línea de la orden de PdV** · modelo `pos.pack.operation.lot` · módulo `point_of_sale` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `pos_order_line_id` | integer | 4 B | Sí | Línea de la orden del PdV → `pos_order_line` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lot_name` | varchar | variable | Sí | Nombre del lote |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_payment`

**Pagos en punto de venta** · modelo `pos.payment` · módulo `point_of_sale` · 28 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `pos_order_id` | integer | 4 B | No | Ordenar → `pos_order` |
| FK | `payment_method_id` | integer | 4 B | No | Método de pago → `pos_payment_method` |
| FK | `session_id` | integer | 4 B | Sí | Sesión → `pos_session` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `account_move_id` | integer | 4 B | Sí | Movimiento de cuenta → `account_move` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Etiqueta |
|  | `card_type` | varchar | variable | Sí | Tipo de tarjeta utilizada — El tipo de tarjeta de pago (por ejemplo, TARJETA DE CRÉDITO O DE DÉBITO) |
|  | `card_brand` | varchar | variable | Sí | Emisor de la tarjeta — El tipo de tarjeta de pago (Por ejemplo: Visa, AMEX, etc.) |
|  | `card_no` | varchar | variable | Sí | Número de tarjeta (últimos 4 dígitos) |
|  | `cardholder_name` | varchar | variable | Sí | Nombre del titular de la tarjeta |
|  | `payment_ref_no` | varchar | variable | Sí | Número de referencia de pago — Número de referencia del pago desde la terminal del proveedor de pagos |
|  | `payment_method_authcode` | varchar | variable | Sí | Código APPR de pago |
|  | `payment_method_issuer_bank` | varchar | variable | Sí | Banco emisor del pago |
|  | `payment_method_payment_mode` | varchar | variable | Sí | Modo de pago |
|  | `transaction_id` | varchar | variable | Sí | ID de transacción de pago |
|  | `payment_status` | varchar | variable | Sí | Estado del pago |
|  | `ticket` | varchar | variable | Sí | Información del recibo de pago |
|  | `uuid` | varchar | variable | Sí | UUID |
|  | `amount` | numeric | variable | No | Importe — Importe total del pago. |
|  | `is_change` | boolean | 1 B | Sí | ¿Se cambió este pago? |
|  | `payment_date` | timestamp | 8 B | No | Fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `employee_id` | integer | 4 B | Sí | Cajero → `hr_employee` — El empleado que usa la caja registradora. |
| FK | `online_account_payment_id` | integer | 4 B | Sí | Contabilidad de pago en línea → `account_payment` |

### `pos_payment_method`

**Métodos de pago del punto de venta** · modelo `pos.payment.method` · módulo `point_of_sale` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `outstanding_account_id` | integer | 4 B | Sí | Cuenta pendiente → `account_account` — La cuenta que se utiliza como cuenta pendiente al crear registros de pagos contables para los pagos bancarios. |
| FK | `receivable_account_id` | integer | 4 B | Sí | Cuenta intermediaria → `account_account` — Dejar vacío para utilizar la cuenta predeterminada de los ajustes de la empresa. Anula la cuenta por cobrar de la empresa (para el punto… |
| FK | `journal_id` | integer | 4 B | Sí | Diario → `account_journal` — Dejar vacío para utilizar la cuenta por cobrar del cliente. Define el diario en el que se anotan los pagos acumulados (o el pago individu… |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `use_payment_terminal` | varchar | variable | Sí | Usar una terminal de pago — Registre los pagos en este diario con una terminal. |
|  | `payment_method_type` | varchar | variable | No | Integración |
|  | `qr_code_method` | varchar | variable | Sí | Formato del código QR — Tipo de código QR a generar para este método de pago. |
|  | `name` | jsonb | variable | No | Método — Defina el nombre del método de pago que se mostrará en el Punto de venta al seleccionar el pago. |
|  | `is_cash_count` | boolean | 1 B | Sí | Efectivo |
|  | `split_transactions` | boolean | 1 B | Sí | Identificar cliente — Obliga a establecer un cliente al utilizar este método de pago y divide los asientos contables para cada cliente. Podría ralentizar el pr… |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `is_online_payment` | boolean | 1 B | Sí | Pago en línea — Use este método de pago para pagos en línea (pagos realizados en una página de internet con proveedores de pagos en línea). |

### `pos_payment_method_config_fast_validation_relation`

**Relación muchos a muchos entre «pos.config» y «pos.payment.method»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_config_id` | integer | 4 B | No | Referencia a pos_config |
| PK, FK | `pos_payment_method_id` | integer | 4 B | No | Referencia a pos_payment_method |

### `pos_preset`

**Cargue un conjunto de opciones de configuración de inmediato** · modelo `pos.preset` · módulo `point_of_sale` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `pricelist_id` | integer | 4 B | Sí | Lista de precios → `product_pricelist` |
| FK | `fiscal_position_id` | integer | 4 B | Sí | Posición fiscal → `account_fiscal_position` |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `resource_calendar_id` | integer | 4 B | Sí | Recurso → `resource_calendar` |
|  | `slots_per_interval` | integer | 4 B | Sí | Capacidad |
|  | `interval_time` | integer | 4 B | Sí | Intervalo de tiempo (en min) |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `identification` | varchar | variable | No | Identificación |
|  | `name` | jsonb | variable | No | Etiqueta |
|  | `is_return` | boolean | 1 B | Sí | Modo de devolución — Toda la cantidad en el carrito será negativa, lo cual es ideal para gestionar las devoluciones. |
|  | `use_timing` | boolean | 1 B | Sí | Gestionar órdenes por tiempo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_printer`

**Impresora del punto de venta** · modelo `pos.printer` · módulo `point_of_sale` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de la impresora — Un identificador interno de la impresora |
|  | `printer_type` | varchar | variable | Sí | Tipo de impresora |
|  | `proxy_ip` | varchar | variable | Sí | Dirección IP del proxy — La dirección IP o el nombre de host del proxy del hardware de la impresora |
|  | `epson_printer_ip` | varchar | variable | Sí | Dirección IP de la impresora Epson — Dirección IP local de una impresora de recibos Epson o su número de serie si la opción "Actualización automática de certificados" está ac… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `pos_session`

**Sesión del punto de venta** · modelo `pos.session` · módulo `point_of_sale` · 22 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `config_id` | integer | 4 B | No | Punto de venta → `pos_config` |
| FK | `user_id` | integer | 4 B | No | Abierta por → `res_users` |
| FK | `cash_journal_id` | integer | 4 B | Sí | Diario de efectivo → `account_journal` |
| FK | `move_id` | integer | 4 B | Sí | Asiento contable → `account_move` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `name` | varchar | variable | Sí | ID de sesión |
|  | `state` | varchar | variable | No | Estado |
|  | `opening_notes` | text | variable | Sí | Notas de apertura |
|  | `closing_notes` | text | variable | Sí | Notas de cierre |
|  | `cash_register_balance_end_real` | numeric | variable | Sí | Saldo final |
|  | `cash_register_balance_start` | numeric | variable | Sí | Saldo inicial |
|  | `cash_real_transaction` | numeric | variable | Sí | Transacción |
|  | `rescue` | boolean | 1 B | Sí | Sesión de recuperación — Sesión autogenerada para órdenes abandonadas, se ignora en las restricciones |
|  | `update_stock_at_closing` | boolean | 1 B | Sí | Las existencias se deben actualizar al cierre |
|  | `start_at` | timestamp | 8 B | Sí | Fecha de apertura |
|  | `stop_at` | timestamp | 8 B | Sí | Fecha de cierre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `employee_id` | integer | 4 B | Sí | Cajero → `hr_employee` — El empleado que utiliza la caja registradora en este momento |

### `printer_category_rel`

**Relación muchos a muchos entre «pos.printer» y «pos.category»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `printer_id` | integer | 4 B | No | Referencia a pos_printer |
| PK, FK | `category_id` | integer | 4 B | No | Referencia a pos_category |

### `stock_reference_pos_order_rel`

**Relación muchos a muchos entre «pos.order» y «stock.reference»** · tabla intermedia, sin modelo propio · módulo `point_of_sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pos_order_id` | integer | 4 B | No | Referencia a pos_order |
| PK, FK | `reference_id` | integer | 4 B | No | Referencia a stock_reference |

## Módulo `portal`

### `portal_share`

**Compartir portal** · modelo `portal.share` · módulo `portal` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | No | ID del documento relacionado |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | No | Modelo de documento relacionado |
|  | `note` | text | variable | Sí | Nota — Agrega contenido adicional para que aparezca en el correo electrónico |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `portal_share_res_partner_rel`

**Relación muchos a muchos entre «portal.share» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `portal` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `portal_share_id` | integer | 4 B | No | Referencia a portal_share |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `portal_wizard`

**Otorgar acceso al portal** · modelo `portal.wizard` · módulo `portal` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `welcome_message` | text | variable | Sí | Mensaje de invitación — Este texto aparece en el correo electrónico que reciben los nuevos usuarios del portal. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `portal_wizard_res_partner_rel`

**Relación muchos a muchos entre «portal.wizard» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `portal` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `portal_wizard_id` | integer | 4 B | No | Referencia a portal_wizard |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `portal_wizard_user`

**Configuración del portal del usuario** · modelo `portal.wizard.user` · módulo `portal` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `wizard_id` | integer | 4 B | No | Asistente → `portal_wizard` |
| FK | `partner_id` | integer | 4 B | No | Contacto → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email` | varchar | variable | Sí | Correo electrónico |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `privacy_lookup`

### `privacy_log`

**Registro de privacidad** · modelo `privacy.log` · módulo `privacy_lookup` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | No | Gestionado por → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `anonymized_name` | varchar | variable | No | Nombre anónimo |
|  | `anonymized_email` | varchar | variable | No | Correo electrónico anónimo |
|  | `execution_details` | text | variable | Sí | Detalles de ejecución |
|  | `records_description` | text | variable | Sí | Registros encontrados |
|  | `additional_note` | text | variable | Sí | Nota adicional |
|  | `date` | timestamp | 8 B | No | Fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `privacy_lookup_wizard`

**Asistente de búsqueda de privacidad** · modelo `privacy.lookup.wizard` · módulo `privacy_lookup` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `log_id` | integer | 4 B | Sí | Registro → `privacy_log` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `email` | varchar | variable | No | Correo electrónico |
|  | `execution_details` | text | variable | Sí | Detalles de ejecución |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `privacy_lookup_wizard_line`

**Línea de asistente de búsqueda de privacidad** · modelo `privacy.lookup.wizard.line` · módulo `privacy_lookup` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `wizard_id` | integer | 4 B | Sí | Asistente → `privacy_lookup_wizard` |
|  | `res_id` | integer | 4 B | No | ID del recurso |
| FK | `res_model_id` | integer | 4 B | Sí | Modelo de documento relacionado → `ir_model` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_name` | varchar | variable | Sí | Nombre del recurso |
|  | `res_model` | varchar | variable | Sí | Modelo de documento |
|  | `execution_details` | varchar | variable | Sí | Detalles de ejecución |
|  | `has_active` | boolean | 1 B | Sí | Activo |
|  | `is_active` | boolean | 1 B | Sí | Está activa |
|  | `is_unlinked` | boolean | 1 B | Sí | Se desvinculó |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `product`

### `account_account_tag_product_template_rel`

**Relación muchos a muchos entre «product.template» y «account.account.tag»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_template_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `account_account_tag_id` | integer | 4 B | No | Referencia a account_account_tag |

### `pos_category_product_template_rel`

**Relación muchos a muchos entre «product.template» y «pos.category»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_template_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `pos_category_id` | integer | 4 B | No | Referencia a pos_category |

### `pos_product_optional_rel`

**Relación muchos a muchos entre «product.template» y «product.template»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `src_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `dest_id` | integer | 4 B | No | Referencia a product_template |

### `product_attr_exclusion_value_ids_rel`

**Relación muchos a muchos entre «product.template.attribute.exclusion» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_template_attribute_exclusion_id` | integer | 4 B | No | Referencia a product_template_attribute_exclusion |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `product_attribute`

**Atributo de producto** · modelo `product.attribute` · módulo `product` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Determinar el orden de visualización |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_variant` | varchar | variable | No | Creación de variantes — - Instantáneo: todas las variantes posibles se crean tan pronto como agrega el atributo y sus valores a un producto. - Dinámico: cada var… |
|  | `display_type` | varchar | variable | No | Tipo de visualización — El tipo de visualización utilizado en el configurador del producto. |
|  | `name` | jsonb | variable | No | Atributo |
|  | `active` | boolean | 1 B | Sí | Activo — Si no se encuentra seleccionado, permite ocultar el atributo sin eliminarlo. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_attribute_custom_value`

**Valor personalizado del atributo del producto** · modelo `product.attribute.custom.value` · módulo `product` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `custom_product_template_attribute_value_id` | integer | 4 B | No | Valor del atributo → `product_template_attribute_value` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `custom_value` | varchar | variable | Sí | Valor personalizado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `pos_order_line_id` | integer | 4 B | Sí | Línea de la orden del PdV → `pos_order_line` |
| FK | `sale_order_line_id` | integer | 4 B | Sí | Línea de la orden de venta → `sale_order_line` |

### `product_attribute_product_template_rel`

**Relación muchos a muchos entre «product.attribute» y «product.template»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_attribute_id` | integer | 4 B | No | Referencia a product_attribute |
| PK, FK | `product_template_id` | integer | 4 B | No | Referencia a product_template |

### `product_attribute_value`

**Valor del atributo** · modelo `product.attribute.value` · módulo `product` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Determinar el orden de visualización |
| FK | `attribute_id` | integer | 4 B | No | Atributo → `product_attribute` — El atributo no puede modificarse una vez que el valor se utiliza en al menos un producto. |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `html_color` | varchar | variable | Sí | Color — Aquí puede establecer un índice de color HTML específico (por ejemplo, #ff0000) para mostrar el color si el tipo de atributo es 'Color'. |
|  | `name` | jsonb | variable | No | Valor |
|  | `is_custom` | boolean | 1 B | Sí | Texto libre — Permita que los clientes establezcan el valor |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `default_extra_price` | double precision | 8 B | Sí | Precio adicional predeterminado |

### `product_attribute_value_product_template_attribute_line_rel`

**Relación muchos a muchos entre «product.attribute.value» y «product.template.attribute.line»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_attribute_value_id` | integer | 4 B | No | Referencia a product_attribute_value |
| PK, FK | `product_template_attribute_line_id` | integer | 4 B | No | Referencia a product_template_attribute_line |

### `product_combo`

**Combo de productos** · modelo `product.combo` · módulo `product` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `qty_max` | integer | 4 B | Sí | Cantidad máxima — Número máximo de artículos a seleccionar en el combo. |
|  | `qty_free` | integer | 4 B | Sí | Cantidad gratuita — Número de artículos gratuitos incluidos en el combo. |

### `product_combo_item`

**Artículo del compro de productos** · modelo `product.combo.item` · módulo `product` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `combo_id` | integer | 4 B | No | Combo → `product_combo` |
| FK | `product_id` | integer | 4 B | No | Opciones → `product_product` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `extra_price` | numeric | variable | Sí | Precio extra |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_combo_product_template_rel`

**Relación muchos a muchos entre «product.template» y «product.combo»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_template_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `product_combo_id` | integer | 4 B | No | Referencia a product_combo |

### `product_document`

**Documento de producto** · modelo `product.document` · módulo `product` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `ir_attachment_id` | integer | 4 B | No | Archivo adjunto relacionado → `ir_attachment` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `attached_on_mrp` | varchar | variable | No | MRP: visible en — Déjelo oculto si solo es posible acceder al documento en el formulario de producto. Seleccione la lista de materiales para visualizar est… |
|  | `attached_on_sale` | varchar | variable | No | Ventas: visible en — Le permite compartir el documento con sus clientes dentro de una venta. Déjelo vacío si no desea compartir este documento con su cliente.… |

### `product_label_layout`

**Elige el diseño de la hoja para imprimir etiquetas** · modelo `product.label.layout` · módulo `product` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `custom_quantity` | integer | 4 B | No | Copias |
| FK | `pricelist_id` | integer | 4 B | Sí | Lista de precios → `product_pricelist` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `print_format` | varchar | variable | No | Formato |
|  | `extra_html` | text | variable | Sí | Contenido adicional |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `move_quantity` | varchar | variable | No | Cantidad a imprimir |
|  | `zpl_template` | varchar | variable | No | Plantilla ZPL |

### `product_label_layout_product_product_rel`

**Relación muchos a muchos entre «product.label.layout» y «product.product»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_label_layout_id` | integer | 4 B | No | Referencia a product_label_layout |
| PK, FK | `product_product_id` | integer | 4 B | No | Referencia a product_product |

### `product_label_layout_product_template_rel`

**Relación muchos a muchos entre «product.label.layout» y «product.template»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_label_layout_id` | integer | 4 B | No | Referencia a product_label_layout |
| PK, FK | `product_template_id` | integer | 4 B | No | Referencia a product_template |

### `product_label_layout_stock_move_rel`

**Relación muchos a muchos entre «product.label.layout» y «stock.move»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_label_layout_id` | integer | 4 B | No | Referencia a product_label_layout |
| PK, FK | `stock_move_id` | integer | 4 B | No | Referencia a stock_move |

### `product_optional_rel`

**Relación muchos a muchos entre «product.template» y «product.template»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `src_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `dest_id` | integer | 4 B | No | Referencia a product_template |

### `product_supplier_taxes_rel`

**Relación muchos a muchos entre «product.template» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `prod_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `tax_id` | integer | 4 B | No | Referencia a account_tax |

### `product_tag`

**Etiqueta del producto** · modelo `product.tag` · módulo `product` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `color` | varchar | variable | Sí | Color |
|  | `name` | jsonb | variable | No | Nombre |
|  | `visible_to_customers` | boolean | 1 B | Sí | Visible para los clientes — Si la etiqueta se muestra a los clientes. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `pos_description` | jsonb | variable | Sí | Descripción |

### `product_tag_product_product_rel`

**Relación muchos a muchos entre «product.product» y «product.tag»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_product_id` | integer | 4 B | No | Referencia a product_product |
| PK, FK | `product_tag_id` | integer | 4 B | No | Referencia a product_tag |

### `product_tag_product_template_rel`

**Relación muchos a muchos entre «product.tag» y «product.template»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_template_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `product_tag_id` | integer | 4 B | No | Referencia a product_tag |

### `product_taxes_rel`

**Relación muchos a muchos entre «product.template» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `prod_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `tax_id` | integer | 4 B | No | Referencia a account_tax |

### `product_template_attribute_exclusion`

**Exclusión de atributos del modelo del producto** · modelo `product.template.attribute.exclusion` · módulo `product` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_template_attribute_value_id` | integer | 4 B | Sí | Valor del atributo → `product_template_attribute_value` |
| FK | `product_tmpl_id` | integer | 4 B | No | Plantilla del producto → `product_template` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_template_attribute_line`

**Línea del atributo de la plantilla del producto** · modelo `product.template.attribute.line` · módulo `product` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_tmpl_id` | integer | 4 B | No | Plantilla del producto → `product_template` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `attribute_id` | integer | 4 B | No | Atributo → `product_attribute` |
|  | `value_count` | integer | 4 B | Sí | Conteo de valor |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_template_attribute_value`

**Valor del atributo de la plantilla del producto** · modelo `product.template.attribute.value` · módulo `product` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_attribute_value_id` | integer | 4 B | No | Valor del atributo → `product_attribute_value` |
| FK | `attribute_line_id` | integer | 4 B | No | Línea de atributo → `product_template_attribute_line` |
| FK | `product_tmpl_id` | integer | 4 B | Sí | Plantilla del producto → `product_template` |
| FK | `attribute_id` | integer | 4 B | Sí | Atributo → `product_attribute` |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `price_extra` | numeric | variable | Sí | Precio extra — Precio adicional para la variante con este valor de atributo en el precio de venta. Por ejemplo, 200 de precio adicional, 1000 + 200 = 1200. |
|  | `ptav_active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_template_uom_uom_rel`

**Relación muchos a muchos entre «product.template» y «uom.uom»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_template_id` | integer | 4 B | No | Referencia a product_template |
| PK, FK | `uom_uom_id` | integer | 4 B | No | Referencia a uom_uom |

### `product_uom`

**Relación entre los productos y sus unidades de medida** · modelo `product.uom` · módulo `product` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `barcode` | varchar | variable | No | Código de barras |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_variant_combination`

**Relación muchos a muchos entre «product.product» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `product_product_id` | integer | 4 B | No | Referencia a product_product |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `res_country_group_pricelist_rel`

**Relación muchos a muchos entre «product.pricelist» y «res.country.group»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `pricelist_id` | integer | 4 B | No | Referencia a product_pricelist |
| PK, FK | `res_country_group_id` | integer | 4 B | No | Referencia a res_country_group |

### `stock_route_categ`

**Relación muchos a muchos entre «product.category» y «stock.route»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `route_id` | integer | 4 B | No | Referencia a stock_route |
| PK, FK | `categ_id` | integer | 4 B | No | Referencia a product_category |

### `stock_route_product`

**Relación muchos a muchos entre «product.template» y «stock.route»** · tabla intermedia, sin modelo propio · módulo `product` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `route_id` | integer | 4 B | No | Referencia a stock_route |
| PK, FK | `product_id` | integer | 4 B | No | Referencia a product_template |

### `update_product_attribute_value`

**Actualizar el valor del atributo del producto** · modelo `update.product.attribute.value` · módulo `product` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `attribute_value_id` | integer | 4 B | No | Valor del atributo → `product_attribute_value` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `mode` | varchar | variable | Sí | Modo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `product_expiry`

### `expiry_picking_confirmation`

**Confirmar caducidad** · modelo `expiry.picking.confirmation` · módulo `product_expiry` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `workorder_id` | integer | 4 B | Sí | Orden de trabajo → `mrp_workorder` |

### `expiry_picking_confirmation_mrp_production_rel`

**Relación muchos a muchos entre «expiry.picking.confirmation» y «mrp.production»** · tabla intermedia, sin modelo propio · módulo `product_expiry` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `expiry_picking_confirmation_id` | integer | 4 B | No | Referencia a expiry_picking_confirmation |
| PK, FK | `mrp_production_id` | integer | 4 B | No | Referencia a mrp_production |

### `expiry_picking_confirmation_stock_lot_rel`

**Relación muchos a muchos entre «expiry.picking.confirmation» y «stock.lot»** · tabla intermedia, sin modelo propio · módulo `product_expiry` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `expiry_picking_confirmation_id` | integer | 4 B | No | Referencia a expiry_picking_confirmation |
| PK, FK | `stock_lot_id` | integer | 4 B | No | Referencia a stock_lot |

### `expiry_picking_confirmation_stock_picking_rel`

**Relación muchos a muchos entre «expiry.picking.confirmation» y «stock.picking»** · tabla intermedia, sin modelo propio · módulo `product_expiry` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `expiry_picking_confirmation_id` | integer | 4 B | No | Referencia a expiry_picking_confirmation |
| PK, FK | `stock_picking_id` | integer | 4 B | No | Referencia a stock_picking |

## Módulo `project`

### `project_collaborator`

**Colaboradores en proyectos compartidos** · modelo `project.collaborator` · módulo `project` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `project_id` | integer | 4 B | No | Project Shared → `project_project` |
| FK | `partner_id` | integer | 4 B | No | Collaborator → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `limited_access` | boolean | 1 B | Sí | Limited Access |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_favorite_user_rel`

**Relación muchos a muchos entre «project.project» y «res.users»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_id` | integer | 4 B | No | Referencia a project_project |
| PK, FK | `user_id` | integer | 4 B | No | Referencia a res_users |

### `project_milestone`

**Objetivo del proyecto** · modelo `project.milestone` · módulo `project` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `project_id` | integer | 4 B | No | Proyectos → `project_project` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `deadline` | date | 4 B | Sí | Fecha límite |
|  | `reached_date` | date | 4 B | Sí | Reached Date |
|  | `is_reached` | boolean | 1 B | Sí | Alcanzado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_project`

**Proyectos** · modelo `project.project` · módulo `project` · 28 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | Sí | Project Account → `account_analytic_account` |
| FK | `alias_id` | integer | 4 B | No | Alias → `mail_alias` — Correo electrónico interno asociado a este proyecto. Los correos electrónicos entrantes se sincronizan en automático con las tareas (o, s… |
|  | `sequence` | integer | 4 B | Sí | Sequence |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `color` | integer | 4 B | Sí | Color Index |
| FK | `user_id` | integer | 4 B | Sí | Gerente de proyecto → `res_users` |
| FK | `stage_id` | integer | 4 B | Sí | Etapa → `project_project_stage` |
| FK | `last_update_id` | integer | 4 B | Sí | Last Update → `project_update` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `privacy_visibility` | varchar | variable | No | Visibilidad — Visibilidad del proyecto y las tareas: - Usuarios internos invitados: Solo pueden acceder al proyecto o tareas que siguen. Los asignados… |
|  | `last_update_status` | varchar | variable | No | Last Update Status |
|  | `date_start` | date | 4 B | Sí | Fecha de inicio |
|  | `date` | date | 4 B | Sí | Fecha de vencimiento — Fecha en la que termina este proyecto. Se toma en cuenta el plazo definido en el proyecto al ver su planificación. |
|  | `name` | jsonb | variable | No | Nombre |
|  | `label_tasks` | jsonb | variable | Sí | Use tareas como — Nombre utilizado para referirse a las tareas de su proyecto, por ejemplo, tareas, tickets, sprints, etc. |
|  | `task_properties_definition` | jsonb | variable | Sí | Propiedades de la tarea |
|  | `description` | text | variable | Sí | Descripción — Descripción para proporcionar más información y contexto sobre este proyecto |
|  | `active` | boolean | 1 B | Sí | Active |
|  | `allow_task_dependencies` | boolean | 1 B | Sí | Dependencias de las tareas |
|  | `allow_milestones` | boolean | 1 B | Sí | Objetivos |
|  | `allow_recurring_tasks` | boolean | 1 B | Sí | Tareas recurrentes |
|  | `is_template` | boolean | 1 B | Sí | Is Template |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_project_project_tags_rel`

**Relación muchos a muchos entre «project.project» y «project.tags»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_project_id` | integer | 4 B | No | Referencia a project_project |
| PK, FK | `project_tags_id` | integer | 4 B | No | Referencia a project_tags |

### `project_project_project_task_type_delete_wizard_rel`

**Relación muchos a muchos entre «project.task.type.delete.wizard» y «project.project»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_task_type_delete_wizard_id` | integer | 4 B | No | Referencia a project_task_type_delete_wizard |
| PK, FK | `project_project_id` | integer | 4 B | No | Referencia a project_project |

### `project_project_stage`

**Etapa del proyecto** · modelo `project.project.stage` · módulo `project` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Sequence |
| FK | `mail_template_id` | integer | 4 B | Sí | Plantilla de correo electrónico → `mail_template` — Si esta opción está activada, se enviará automáticamente un correo electrónico al cliente cuando el proyecto llegue a esta etapa. |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Active |
|  | `fold` | boolean | 1 B | Sí | Plegada — Si está seleccionada, esta etapa aparecerá plegada en las vistas de kanban y de lista de tus proyectos. Los proyectos en una etapa plegad… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `sms_template_id` | integer | 4 B | Sí | Plantilla de SMS → `sms_template` — Si esta opción está activada, se enviará un mensaje SMS de forma automática al cliente cuando el proyecto llegue a esta etapa. |

### `project_project_stage_delete_wizard`

**Asistente para eliminar la etapa del proyecto** · modelo `project.project.stage.delete.wizard` · módulo `project` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_project_stage_project_project_stage_delete_wizard_rel`

**Relación muchos a muchos entre «project.project.stage.delete.wizard» y «project.project.stage»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_project_stage_delete_wizard_id` | integer | 4 B | No | Referencia a project_project_stage_delete_wizard |
| PK, FK | `project_project_stage_id` | integer | 4 B | No | Referencia a project_project_stage |

### `project_role`

**Rol del proyecto** · modelo `project.role` · módulo `project` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Color |
|  | `sequence` | integer | 4 B | Sí | Sequence |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_role_project_task_rel`

**Relación muchos a muchos entre «project.task» y «project.role»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_task_id` | integer | 4 B | No | Referencia a project_task |
| PK, FK | `project_role_id` | integer | 4 B | No | Referencia a project_role |

### `project_share_collaborator_wizard`

**Asistente de colaborador para compartir proyectos** · modelo `project.share.collaborator.wizard` · módulo `project` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `parent_wizard_id` | integer | 4 B | Sí | Parent Wizard → `project_share_wizard` |
| FK | `partner_id` | integer | 4 B | No | Colaborador → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_mode` | varchar | variable | No | Modo de acceso — Lectura: Los colaboradores pueden ver las tareas, pero no editarlas. Editar con acceso limitado: Los colaboradores pueden ver y editar la… |
|  | `send_invitation` | boolean | 1 B | Sí | Enviar invitación |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_share_wizard`

**Compartir proyectos** · modelo `project.share.wizard` · módulo `project` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | No | ID del documento relacionado |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | No | Modelo de documento relacionado |
|  | `note` | text | variable | Sí | Nota — Agrega contenido adicional para que aparezca en el correo electrónico |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_share_wizard_res_partner_rel`

**Relación muchos a muchos entre «project.share.wizard» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_share_wizard_id` | integer | 4 B | No | Referencia a project_share_wizard |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `project_tags`

**Etiquetas del proyecto** · modelo `project.tags` · módulo `project` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Color — Las etiquetas transparentes no son visibles desde la vista de kanban de sus proyectos y tareas. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_tags_project_task_rel`

**Relación muchos a muchos entre «project.tags» y «project.task»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_task_id` | integer | 4 B | No | Referencia a project_task |
| PK, FK | `project_tags_id` | integer | 4 B | No | Referencia a project_tags |

### `project_task_recurrence`

**Recurrencia de la tarea** · modelo `project.task.recurrence` · módulo `project` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `repeat_interval` | integer | 4 B | Sí | Repetir cada |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `repeat_unit` | varchar | variable | Sí | Repeat Unit |
|  | `repeat_type` | varchar | variable | Sí | Hasta |
|  | `repeat_until` | date | 4 B | Sí | Fecha de finalización |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_task_type`

**Etapa de la tarea** · modelo `project.task.type` · módulo `project` · 20 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `mail_template_id` | integer | 4 B | Sí | Plantilla de correo electrónico → `mail_template` — Si esta opción está activada, se enviará automáticamente un correo electrónico al cliente cuando la tarea llegue a esta etapa. |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `rating_template_id` | integer | 4 B | Sí | Plantilla del correo de calificación → `mail_template` — Si está seleccionada, el sistema enviará una solicitud de calificación por correo electrónico al cliente en automático cuando la tarea pa… |
|  | `rotting_threshold_days` | integer | 4 B | Sí | Días para deteriorarse — Número de días antes de que las tareas en esta etapa se consideren obsoletas. Defínelo con 0 para desactivar esta función. Cambiar este p… |
| FK | `user_id` | integer | 4 B | Sí | Propietario de la etapa → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `rating_status` | varchar | variable | No | Estado de las calificaciones del cliente — Envía una solicitud de calificación cuando una tarea entre en cierta etapa para que conozcas los comentarios de tus clientes. Para ello,… |
|  | `rating_status_period` | varchar | variable | No | Frecuencia de calificación |
|  | `name` | jsonb | variable | No | Nombre |
|  | `active` | boolean | 1 B | Sí | Active |
|  | `fold` | boolean | 1 B | Sí | Plegada |
|  | `auto_validation_state` | boolean | 1 B | Sí | Estado de kanban automático — Modifique el estado de forma automática cuando el cliente responda a los comentarios para esta etapa. * Los comentarios buenos del client… |
|  | `rating_active` | boolean | 1 B | Sí | Envía una solicitud de calificación al cliente |
|  | `rating_request_deadline` | timestamp | 8 B | Sí | Rating Request Deadline |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `sms_template_id` | integer | 4 B | Sí | Plantilla de SMS → `sms_template` — Si esta opción está activada, se enviará un mensaje SMS de forma automática al cliente cuando la tarea llegue a esta etapa. |

### `project_task_type_delete_wizard`

**Asistente para eliminar la etapa de la tarea del proyecto** · modelo `project.task.type.delete.wizard` · módulo `project` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_task_type_project_task_type_delete_wizard_rel`

**Relación muchos a muchos entre «project.task.type.delete.wizard» y «project.task.type»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_task_type_delete_wizard_id` | integer | 4 B | No | Referencia a project_task_type_delete_wizard |
| PK, FK | `project_task_type_id` | integer | 4 B | No | Referencia a project_task_type |

### `project_task_type_rel`

**Relación muchos a muchos entre «project.project» y «project.task.type»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_id` | integer | 4 B | No | Referencia a project_project |
| PK, FK | `type_id` | integer | 4 B | No | Referencia a project_task_type |

### `project_task_user_rel`

**Relación muchos a muchos entre «project.task» y «project.task.type»** · tabla intermedia, sin modelo propio · módulo `project` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
| FK | `task_id` | integer | 4 B | No | Referencia a project_task |
| FK | `user_id` | integer | 4 B | No | Referencia a res_users |
| FK | `stage_id` | integer | 4 B | Sí | Referencia a project_task_type |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |

### `project_template_create_wizard`

**Asistente de creación de plantillas de proyecto** · modelo `project.template.create.wizard` · módulo `project` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `alias_domain_id` | integer | 4 B | Sí | Dominio del alias → `mail_alias_domain` |
| FK | `template_id` | integer | 4 B | Sí | Plantilla → `project_project` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `alias_name` | varchar | variable | Sí | Nombre del alias |
|  | `date_start` | date | 4 B | Sí | Fecha de inicio |
|  | `date` | date | 4 B | Sí | Fecha de vencimiento |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_template_role_to_users_map`

**Rol de proyecto para usuarios para el mapeo** · modelo `project.template.role.to.users.map` · módulo `project` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `wizard_id` | integer | 4 B | Sí | Wizard → `project_template_create_wizard` |
| FK | `role_id` | integer | 4 B | No | Rol del proyecto → `project_role` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `project_template_role_to_users_map_res_users_rel`

**Relación muchos a muchos entre «project.template.role.to.users.map» y «res.users»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `project_template_role_to_users_map_id` | integer | 4 B | No | Referencia a project_template_role_to_users_map |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `project_update`

**Actualización del proyecto** · modelo `project.update` · módulo `project` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `progress` | integer | 4 B | Sí | Progreso |
| FK | `user_id` | integer | 4 B | No | Autor → `res_users` |
| FK | `project_id` | integer | 4 B | No | Project → `project_project` |
|  | `task_count` | integer | 4 B | Sí | Task Count |
|  | `closed_task_count` | integer | 4 B | Sí | Closed Task Count |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `email_cc` | varchar | variable | Sí | CC del correo electrónico |
|  | `name` | varchar | variable | No | Título |
|  | `status` | varchar | variable | No | Status |
|  | `date` | date | 4 B | Sí | Fecha |
|  | `description` | text | variable | Sí | Descripción |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `res_partner_task_share_wizard_rel`

**Relación muchos a muchos entre «task.share.wizard» y «res.partner»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `task_share_wizard_id` | integer | 4 B | No | Referencia a task_share_wizard |
| PK, FK | `res_partner_id` | integer | 4 B | No | Referencia a res_partner |

### `task_dependencies_rel`

**Relación muchos a muchos entre «project.task» y «project.task»** · tabla intermedia, sin modelo propio · módulo `project` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `task_id` | integer | 4 B | No | Referencia a project_task |
| PK, FK | `depends_on_id` | integer | 4 B | No | Referencia a project_task |

### `task_share_wizard`

**Compartir tarea** · modelo `task.share.wizard` · módulo `project` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | No | ID del documento relacionado |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
| FK | `task_id` | integer | 4 B | Sí | Tarea → `project_task` |
|  | `res_model` | varchar | variable | No | Modelo de documento relacionado |
|  | `note` | text | variable | Sí | Nota — Agrega contenido adicional para que aparezca en el correo electrónico |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `project_todo`

### `mail_activity_todo_create`

**Crear actividad y actividad pendiente al mismo tiempo** · modelo `mail.activity.todo.create` · módulo `project_todo` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | No | Asignada a → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `summary` | varchar | variable | Sí | Resumen |
|  | `date_deadline` | date | 4 B | No | Fecha límite |
|  | `note` | text | variable | Sí | Nota |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `purchase`

### `account_move_purchase_order_rel`

**Relación muchos a muchos entre «purchase.order» y «account.move»** · tabla intermedia, sin modelo propio · módulo `purchase` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `purchase_order_id` | integer | 4 B | No | Referencia a purchase_order |
| PK, FK | `account_move_id` | integer | 4 B | No | Referencia a account_move |

### `bill_to_po_wizard`

**Facturar a la orden de compra** · modelo `bill.to.po.wizard` · módulo `purchase` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `purchase_order_id` | integer | 4 B | Sí | Orden de compra → `purchase_order` |
| FK | `partner_id` | integer | 4 B | Sí | Contacto → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_template_attribute_value_purchase_order_line_rel`

**Relación muchos a muchos entre «purchase.order.line» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `purchase` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `purchase_order_line_id` | integer | 4 B | No | Referencia a purchase_order_line |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `purchase_order_stock_picking_rel`

**Relación muchos a muchos entre «purchase.order» y «stock.picking»** · tabla intermedia, sin modelo propio · módulo `purchase` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `purchase_order_id` | integer | 4 B | No | Referencia a purchase_order |
| PK, FK | `stock_picking_id` | integer | 4 B | No | Referencia a stock_picking |

### `stock_move_created_purchase_line_rel`

**Relación muchos a muchos entre «purchase.order.line» y «stock.move»** · tabla intermedia, sin modelo propio · módulo `purchase` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `created_purchase_line_id` | integer | 4 B | No | Referencia a purchase_order_line |
| PK, FK | `move_id` | integer | 4 B | No | Referencia a stock_move |

### `stock_reference_purchase_rel`

**Relación muchos a muchos entre «purchase.order» y «stock.reference»** · tabla intermedia, sin modelo propio · módulo `purchase` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `purchase_id` | integer | 4 B | No | Referencia a purchase_order |
| PK, FK | `reference_id` | integer | 4 B | No | Referencia a stock_reference |

## Módulo `rating`

### `rating_rating`

**Calificación** · modelo `rating.rating` · módulo `rating` · 26 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `res_model_id` | integer | 4 B | Sí | Modelo de documento relacionado → `ir_model` |
|  | `res_id` | integer | 4 B | No | Documento |
| FK | `parent_res_model_id` | integer | 4 B | Sí | Modelo de documento principal relacionado → `ir_model` |
|  | `parent_res_id` | integer | 4 B | Sí | Documento principal |
| FK | `rated_partner_id` | integer | 4 B | Sí | Operador valorado → `res_partner` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `message_id` | integer | 4 B | Sí | Mensaje → `mail_message` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_name` | varchar | variable | Sí | Nombre del recurso |
|  | `res_model` | varchar | variable | Sí | Modelo de documento |
|  | `parent_res_name` | varchar | variable | Sí | Nombre del documento principal |
|  | `parent_res_model` | varchar | variable | Sí | Modelo del documento principal |
|  | `rating_text` | varchar | variable | Sí | Calificación |
|  | `access_token` | varchar | variable | Sí | Token de seguridad |
|  | `feedback` | text | variable | Sí | Comentario |
|  | `is_internal` | boolean | 1 B | Sí | Visible solo de forma interna — Ocultar a los usuarios públicos o del portal, independientemente de la configuración del subtipo. |
|  | `consumed` | boolean | 1 B | Sí | Calificación otorgada |
|  | `create_date` | timestamp | 8 B | Sí | Enviado el |
|  | `rated_on` | timestamp | 8 B | Sí | Calificado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `rating` | double precision | 8 B | Sí | Valor de la calificación |
| FK | `publisher_id` | integer | 4 B | Sí | Comentario hecho por → `res_partner` |
|  | `publisher_comment` | text | variable | Sí | Comentario del editor |
|  | `publisher_datetime` | timestamp | 8 B | Sí | Comentario hecho el |

## Módulo `resource`

### `resource_calendar`

**Tiempo de trabajo de recursos** · modelo `resource.calendar` · módulo `resource` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `schedule_type` | varchar | variable | No | Tipo de horario — Elige el nivel de definición que quieres configurar en tu horario: - Flexible: Define una cantidad de horas para trabajar durante la sema… |
|  | `tz` | varchar | variable | No | Zona horaria — Este campo se utiliza para definir en qué zona horaria funcionarán los recursos. |
|  | `hours_per_day` | numeric | variable | Sí | Promedio de horas al día — El recurso de horas promedio al día debe trabajar con este calendario. |
|  | `active` | boolean | 1 B | Sí | Activo — Si el campo activo está configurado a "falso" le permitirá ocultar las "horas trabajadas" sin quitarlas. |
|  | `duration_based` | boolean | 1 B | Sí | Asistencia basada en la duración — Las horas se centrarán alrededor de las 12:00 para cubrir la duración del día |
|  | `flexible_hours` | boolean | 1 B | Sí | Horas flexibles — Cuando esta opción está habilitada los empleados pueden trabajar de forma flexible sin depender del horario de trabajo de la empresa (hor… |
|  | `two_weeks_calendar` | boolean | 1 B | Sí | Calendario en modo de 2 semanas |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `full_time_required_hours` | double precision | 8 B | Sí | Equivalente a tiempo completo — Número de horas a trabajar en el horario de la empresa para considerarse como tiempo completo. |
|  | `hours_per_week` | double precision | 8 B | Sí | Horas por semana |

### `resource_calendar_attendance`

**Detalle del trabajo** · modelo `resource.calendar.attendance` · módulo `resource` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `calendar_id` | integer | 4 B | No | Calendario del recurso → `resource_calendar` |
|  | `sequence` | integer | 4 B | Sí | Secuencia — Da la secuencia de esta línea cuando se muestra el calendario de recursos |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `dayofweek` | varchar | variable | No | Día de la semana |
|  | `day_period` | varchar | variable | No | Periodo del día |
|  | `week_type` | varchar | variable | Sí | Número de semana |
|  | `display_type` | varchar | variable | Sí | Mostrar tipo — Campo técnico para propósitos de usabilidad. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `hour_from` | double precision | 8 B | No | Trabajar desde — Inicio y fin del trabajo Un valor específico como 24:00 se interpretará como 23:59:59.999999. |
|  | `hour_to` | double precision | 8 B | No | Trabajar hasta |
|  | `duration_hours` | double precision | 8 B | Sí | Duración (horas) |
|  | `duration_days` | double precision | 8 B | Sí | Duración (días) |

### `resource_calendar_leaves`

**Detalle de la pausa del recurso** · modelo `resource.calendar.leaves` · módulo `resource` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `calendar_id` | integer | 4 B | Sí | Horas laborales → `resource_calendar` |
| FK | `resource_id` | integer | 4 B | Sí | Recurso → `resource_resource` — Si está vacío, son ausencias genéricas para la empresa. Si un recurso está configurado, la ausencia es solo para este recurso. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | Sí | Motivo |
|  | `time_type` | varchar | variable | Sí | Tipo de tiempo — Si esto debe calcularse como tiempo personal o como tiempo de trabajo (por ejemplo, formación) |
|  | `date_from` | timestamp | 8 B | No | Fecha de inicio |
|  | `date_to` | timestamp | 8 B | No | Fecha de finalización |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `resource_resource`

**Recursos** · modelo `resource.resource` · módulo `resource` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `user_id` | integer | 4 B | Sí | Usuario → `res_users` — Nombre de usuario relacionado con el recurso para gestionar su acceso. |
| FK | `calendar_id` | integer | 4 B | Sí | Horas laborables → `resource_calendar` — Define el horario de trabajo del recurso. Si no configuras uno, su horario será completamente flexible. |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `resource_type` | varchar | variable | No | Tipo |
|  | `tz` | varchar | variable | No | Zona horaria |
|  | `active` | boolean | 1 B | Sí | Activo — Si desmarca el campo activo podrá ocultar el registro del recurso sin eliminarlo. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `time_efficiency` | double precision | 8 B | No | Factor de eficiencia — Este campo se utiliza para calcular la duración esperada de una orden de trabajo en este centro de trabajo. Por ejemplo, si una orden de… |
|  | `color` | integer | 4 B | Sí | Color |

## Módulo `sale`

### `account_tax_sale_order_line_rel`

**Relación muchos a muchos entre «sale.order.line» y «account.tax»** · tabla intermedia, sin modelo propio · módulo `sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `sale_order_line_id` | integer | 4 B | No | Referencia a sale_order_line |
| PK, FK | `account_tax_id` | integer | 4 B | No | Referencia a account_tax |

### `product_template_attribute_value_sale_order_line_rel`

**Relación muchos a muchos entre «sale.order.line» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `sale_order_line_id` | integer | 4 B | No | Referencia a sale_order_line |
| PK, FK | `product_template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

### `sale_advance_payment_inv`

**Factura de anticipo de ventas** · modelo `sale.advance.payment.inv` · módulo `sale` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `currency_id` | integer | 4 B | Sí | Moneda → `res_currency` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `advance_payment_method` | varchar | variable | No | Crear factura — Se emite una factura estándar con todas las líneas de orden listas para la facturación, de acuerdo con su política de facturación (según… |
|  | `fixed_amount` | numeric | variable | Sí | Importe del anticipo (fijo) — El importe fijo que se facturará por adelantado. |
|  | `deduct_down_payments` | boolean | 1 B | Sí | Deducir anticipos |
|  | `consolidated_billing` | boolean | 1 B | Sí | Facturación consolidada — Crea una factura para todas las órdenes relacionadas con el mismo cliente, la misma dirección de facturación y la misma dirección de entr… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `amount` | double precision | 8 B | Sí | Anticipo — El porcentaje del importe a facturar por adelantado. |

### `sale_advance_payment_inv_sale_order_rel`

**Relación muchos a muchos entre «sale.advance.payment.inv» y «sale.order»** · tabla intermedia, sin modelo propio · módulo `sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `sale_advance_payment_inv_id` | integer | 4 B | No | Referencia a sale_advance_payment_inv |
| PK, FK | `sale_order_id` | integer | 4 B | No | Referencia a sale_order |

### `sale_mass_cancel_orders`

**Cancelar varias cotizaciones** · modelo `sale.mass.cancel.orders` · módulo `sale` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sale_order_discount`

**Asistente de descuentos** · modelo `sale.order.discount` · módulo `sale` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `sale_order_id` | integer | 4 B | No | Orden de venta → `sale_order` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `discount_type` | varchar | variable | Sí | Tipo de descuento |
|  | `discount_amount` | numeric | variable | Sí | Importe |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `discount_percentage` | double precision | 8 B | Sí | Porcentaje |

### `sale_order_line_stock_route_rel`

**Relación muchos a muchos entre «sale.order.line» y «stock.route»** · tabla intermedia, sin modelo propio · módulo `sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `sale_order_line_id` | integer | 4 B | No | Referencia a sale_order_line |
| PK, FK | `stock_route_id` | integer | 4 B | No | Referencia a stock_route |

### `sale_order_mass_cancel_wizard_rel`

**Relación muchos a muchos entre «sale.mass.cancel.orders» y «sale.order»** · tabla intermedia, sin modelo propio · módulo `sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `sale_mass_cancel_orders_id` | integer | 4 B | No | Referencia a sale_mass_cancel_orders |
| PK, FK | `sale_order_id` | integer | 4 B | No | Referencia a sale_order |

### `sale_order_tag_rel`

**Relación muchos a muchos entre «sale.order» y «crm.tag»** · tabla intermedia, sin modelo propio · módulo `sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `order_id` | integer | 4 B | No | Referencia a sale_order |
| PK, FK | `tag_id` | integer | 4 B | No | Referencia a crm_tag |

### `stock_reference_sale_rel`

**Relación muchos a muchos entre «sale.order» y «stock.reference»** · tabla intermedia, sin modelo propio · módulo `sale` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `sale_id` | integer | 4 B | No | Referencia a sale_order |
| PK, FK | `reference_id` | integer | 4 B | No | Referencia a stock_reference |

## Módulo `sale_crm`

### `crm_quotation_partner`

**Cree un nuevo cliente o utilice uno existente para una nueva cotización** · modelo `crm.quotation.partner` · módulo `sale_crm` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `lead_id` | integer | 4 B | No | Lead asociado → `crm_lead` |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `action` | varchar | variable | No | Cotización del cliente |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `sales_team`

### `crm_tag`

**Etiqueta CRM** · modelo `crm.tag` · módulo `sales_team` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre de la etiqueta |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `crm_team`

**Equipo de ventas** · modelo `crm.team` · módulo `sales_team` · 18 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `user_id` | integer | 4 B | Sí | Líder del equipo → `res_users` |
|  | `color` | integer | 4 B | Sí | Índice de color — Color del canal |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Equipo de ventas |
|  | `active` | boolean | 1 B | Sí | Activo — Si el campo activo se define como falso, podrá ocultar el equipo de ventas sin eliminarlo. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `alias_id` | integer | 4 B | No | Alias → `mail_alias` — La dirección de correo electrónico asociada con este canal. Los nuevos correos electrónicos recibidos crearán de forma automática nuevos… |
|  | `assignment_domain` | varchar | variable | Sí | Dominio de asignación — Dominio de filtro adicional cuando se buscan leads no asignados para asignarlos al equipo. |
|  | `lead_properties_definition` | jsonb | variable | Sí | Propiedades del lead |
|  | `use_leads` | boolean | 1 B | Sí | Leads — Seleccione esta casilla para filtrar y calificar las solicitudes entrantes como leads antes de convertirlas en oportunidades y asignarlas… |
|  | `use_opportunities` | boolean | 1 B | Sí | Flujo — Seleccione esta casilla para administrar un proceso de preventa con oportunidades. |
|  | `assignment_optout` | boolean | 1 B | Sí | Omitir la asignación automática |
|  | `invoiced_target` | double precision | 8 B | Sí | Objetivo de facturación — Objetivo de ingresos para el mes actual (total sin impuestos de las facturas pagadas). |

### `crm_team_member`

**Miembro del equipo de ventas** · modelo `crm.team.member` · módulo `sales_team` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `crm_team_id` | integer | 4 B | No | Equipo de ventas → `crm_team` |
| FK | `user_id` | integer | 4 B | No | Vendedor → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `assignment_max` | integer | 4 B | Sí | Capacidad promedio de leads (en 30 días) |
|  | `assignment_domain` | varchar | variable | Sí | Dominio de asignación |
|  | `assignment_domain_preferred` | varchar | variable | Sí | Dominio de asignación preferido |
|  | `assignment_optout` | boolean | 1 B | Sí | Pausar asignación |

### `team_favorite_user_rel`

**Relación muchos a muchos entre «crm.team» y «res.users»** · tabla intermedia, sin modelo propio · módulo `sales_team` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `team_id` | integer | 4 B | No | Referencia a crm_team |
| PK, FK | `user_id` | integer | 4 B | No | Referencia a res_users |

## Módulo `sms`

### `sms_account_code`

**Asistente para código de verificación para cuenta de SMS** · modelo `sms.account.code` · módulo `sms` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | No | Cuenta → `iap_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `verification_code` | varchar | variable | No | Código de verificación |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_account_phone`

**Asistente de registro de número de teléfono para cuenta de SMS** · modelo `sms.account.phone` · módulo `sms` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | No | Cuenta → `iap_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `phone_number` | varchar | variable | No | Número de teléfono |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_account_sender`

**Asistente para nombre de remitente para cuenta de SMS** · modelo `sms.account.sender` · módulo `sms` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `account_id` | integer | 4 B | No | Cuenta → `iap_account` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `sender_name` | varchar | variable | Sí | Nombre del remitente |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_composer`

**Asistente de envío de SMS** · modelo `sms.composer` · módulo `sms` · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `res_id` | integer | 4 B | Sí | ID del documento |
| FK | `template_id` | integer | 4 B | Sí | Usar plantilla → `sms_template` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `composition_mode` | varchar | variable | No | Modo de redacción |
|  | `res_model` | varchar | variable | Sí | Nombre del modelo del documento |
|  | `res_ids` | varchar | variable | Sí | Identificadores de documento |
|  | `recipient_single_number_itf` | varchar | variable | Sí | Número del destinatario — Número de teléfono del destinatario. Si se cambió, se registrará en el perfil del cliente. |
|  | `number_field_name` | varchar | variable | Sí | Campo de número |
|  | `numbers` | varchar | variable | Sí | Destinatarios (números) |
|  | `body` | text | variable | No | Mensaje |
|  | `mass_keep_log` | boolean | 1 B | Sí | Mantener una nota en el documento |
|  | `mass_force_send` | boolean | 1 B | Sí | Enviar directamente |
|  | `use_exclusion_list` | boolean | 1 B | Sí | Usar lista de exclusión — Evita enviar mensajes a los contactos en la lista de exclusión. Desactiva esta función solo cuando sea absolutamente necesario. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_sms`

**SMS salientes** · modelo `sms.sms` · módulo `sms` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `partner_id` | integer | 4 B | Sí | Cliente → `res_partner` |
| FK | `mail_message_id` | integer | 4 B | Sí | Mensaje de correo → `mail_message` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `uuid` | varchar | variable | Sí | UUID — Forma alternativa de identificar un registro de SMS. Se utiliza para los reportes de entrega. |
|  | `number` | varchar | variable | Sí | Número |
|  | `state` | varchar | variable | No | Estado de SMS |
|  | `failure_type` | varchar | variable | Sí | Tipo de error |
|  | `body` | text | variable | Sí | Contenido |
|  | `to_delete` | boolean | 1 B | Sí | Marcado para eliminación — Se eliminará de forma automática, mientras que las notificaciones no se eliminarán en ningún caso. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_template`

**Plantillas de SMS** · modelo `sms.template` · módulo `sms` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `model_id` | integer | 4 B | No | Aplica a → `ir_model` — Puede usar el tipo de plantilla de este documento con |
| FK | `sidebar_action_id` | integer | 4 B | Sí | Acción de la barra lateral → `ir_act_window` — Acción de la barra lateral para hacer disponible esta plantilla en los registros del modelo de documento relacionado |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `template_fs` | varchar | variable | Sí | Nombre del archivo de la plantilla — Archivo desde el que se origina la plantilla. Se utiliza para restablecer la plantilla dañada. |
|  | `lang` | varchar | variable | Sí | Idioma — Idioma de traducción opcional (código ISO) a seleccionar al enviar un correo. Si no lo defines, el sistema usará el idioma principal del… |
|  | `model` | varchar | variable | Sí | Modelo de documento relacionado |
|  | `name` | jsonb | variable | Sí | Nombre |
|  | `body` | jsonb | variable | No | Contenido |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_template_preview`

**Previsualización de la plantilla de SMS** · modelo `sms.template.preview` · módulo `sms` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `sms_template_id` | integer | 4 B | No | Plantilla de SMS → `sms_template` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `lang` | varchar | variable | Sí | Idioma de vista previa de la plantilla |
|  | `resource_ref` | varchar | variable | Sí | Registro de referencia |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_template_reset`

**Restablecer las plantillas de SMS** · modelo `sms.template.reset` · módulo `sms` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `sms_template_sms_template_reset_rel`

**Relación muchos a muchos entre «sms.template.reset» y «sms.template»** · tabla intermedia, sin modelo propio · módulo `sms` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `sms_template_reset_id` | integer | 4 B | No | Referencia a sms_template_reset |
| PK, FK | `sms_template_id` | integer | 4 B | No | Referencia a sms_template |

### `sms_tracker`

**Vincula SMS a los modelos de seguimiento de correo y mensajes de texto** · modelo `sms.tracker` · módulo `sms` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `mail_notification_id` | integer | 4 B | Sí | Notificación de correo → `mail_notification` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `sms_uuid` | varchar | variable | No | UUID del SMS |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `snailmail`

### `snailmail_letter`

**Carta de correo postal** · modelo `snailmail.letter` · módulo `snailmail` · 25 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Enviada por → `res_users` |
|  | `res_id` | integer | 4 B | No | ID del documento |
| FK | `partner_id` | integer | 4 B | No | Destinatario → `res_partner` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `report_template` | integer | 4 B | Sí | Reporte opcional para imprimir y adjuntar → `ir_act_report_xml` |
| FK | `attachment_id` | integer | 4 B | Sí | Archivo adjunto → `ir_attachment` |
| FK | `message_id` | integer | 4 B | Sí | Mensaje del estado de correo postal → `mail_message` |
| FK | `state_id` | integer | 4 B | Sí | Estado → `res_country_state` |
| FK | `country_id` | integer | 4 B | Sí | País → `res_country` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `model` | varchar | variable | No | Modelo |
|  | `state` | varchar | variable | No | Estado — Al crear una carta, su estado es "Pendiente". Si la carta se envía de forma correcta, el estado cambia a "Enviado". Si no, el estado será… |
|  | `error_code` | varchar | variable | Sí | Error |
|  | `street` | varchar | variable | Sí | Calle |
|  | `street2` | varchar | variable | Sí | Calle2 |
|  | `zip` | varchar | variable | Sí | Código postal |
|  | `city` | varchar | variable | Sí | Ciudad |
|  | `info_msg` | text | variable | Sí | Información |
|  | `color` | boolean | 1 B | Sí | Color |
|  | `cover` | boolean | 1 B | Sí | Portada |
|  | `duplex` | boolean | 1 B | Sí | Ambos lados |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `spreadsheet_dashboard`

### `ir_model_spreadsheet_dashboard_rel`

**Relación muchos a muchos entre «spreadsheet.dashboard» y «ir.model»** · tabla intermedia, sin modelo propio · módulo `spreadsheet_dashboard` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `spreadsheet_dashboard_id` | integer | 4 B | No | Referencia a spreadsheet_dashboard |
| PK, FK | `ir_model_id` | integer | 4 B | No | Referencia a ir_model |

### `res_company_spreadsheet_dashboard_rel`

**Relación muchos a muchos entre «spreadsheet.dashboard» y «res.company»** · tabla intermedia, sin modelo propio · módulo `spreadsheet_dashboard` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `spreadsheet_dashboard_id` | integer | 4 B | No | Referencia a spreadsheet_dashboard |
| PK, FK | `res_company_id` | integer | 4 B | No | Referencia a res_company |

### `res_groups_spreadsheet_dashboard_rel`

**Relación muchos a muchos entre «spreadsheet.dashboard» y «res.groups»** · tabla intermedia, sin modelo propio · módulo `spreadsheet_dashboard` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `spreadsheet_dashboard_id` | integer | 4 B | No | Referencia a spreadsheet_dashboard |
| PK, FK | `res_groups_id` | integer | 4 B | No | Referencia a res_groups |

### `res_users_spreadsheet_dashboard_rel`

**Relación muchos a muchos entre «spreadsheet.dashboard» y «res.users»** · tabla intermedia, sin modelo propio · módulo `spreadsheet_dashboard` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `spreadsheet_dashboard_id` | integer | 4 B | No | Referencia a spreadsheet_dashboard |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `spreadsheet_dashboard`

**Tablero de Hojas de cálculo** · modelo `spreadsheet.dashboard` · módulo `spreadsheet_dashboard` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `dashboard_group_id` | integer | 4 B | No | Grupo de tablero → `spreadsheet_dashboard_group` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `sample_dashboard_file_path` | varchar | variable | Sí | Sample Dashboard File Path |
|  | `name` | jsonb | variable | No | Nombre |
|  | `is_published` | boolean | 1 B | Sí | Está publicado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `spreadsheet_dashboard_group`

**Grupo de tableros** · modelo `spreadsheet.dashboard.group` · módulo `spreadsheet_dashboard` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `spreadsheet_dashboard_share`

**Copia de una hoja de cálculo compartida** · modelo `spreadsheet.dashboard.share` · módulo `spreadsheet_dashboard` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `dashboard_id` | integer | 4 B | No | Tablero → `spreadsheet_dashboard` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `access_token` | varchar | variable | No | Token de acceso |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `stock`

### `Products`

**Relación muchos a muchos entre «stock.package.destination» y «stock.move.line»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_package_destination_id` | integer | 4 B | No | Referencia a stock_package_destination |
| PK, FK | `stock_move_line_id` | integer | 4 B | No | Referencia a stock_move_line |

### `account_analytic_line_stock_move_rel`

**Relación muchos a muchos entre «stock.move» y «account.analytic.line»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_move_id` | integer | 4 B | No | Referencia a stock_move |
| PK, FK | `account_analytic_line_id` | integer | 4 B | No | Referencia a account_analytic_line |

### `lot_label_layout`

**Elija el diseño de la hoja para imprimir etiquetas de lotes** · modelo `lot.label.layout` · módulo `stock` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `label_quantity` | varchar | variable | No | Cantidad a imprimir — Si la UdM del lote no es "unidades", el lote se considerará una unidad y solo se imprimirá una etiqueta para este lote. |
|  | `print_format` | varchar | variable | No | Formato |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `lot_label_layout_stock_move_line_rel`

**Relación muchos a muchos entre «lot.label.layout» y «stock.move.line»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `lot_label_layout_id` | integer | 4 B | No | Referencia a lot_label_layout |
| PK, FK | `stock_move_line_id` | integer | 4 B | No | Referencia a stock_move_line |

### `mrp_bom_stock_replenishment_info_rel`

**Relación muchos a muchos entre «stock.replenishment.info» y «mrp.bom»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_replenishment_info_id` | integer | 4 B | No | Referencia a stock_replenishment_info |
| PK, FK | `mrp_bom_id` | integer | 4 B | No | Referencia a mrp_bom |

### `mrp_production_picking_label_type_rel`

**Relación muchos a muchos entre «picking.label.type» y «mrp.production»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `picking_label_type_id` | integer | 4 B | No | Referencia a picking_label_type |
| PK, FK | `mrp_production_id` | integer | 4 B | No | Referencia a mrp_production |

### `picking_label_type`

**Elija si se deben imprimir etiquetas de producto o de número de lote o de serie** · modelo `picking.label.type` · módulo `stock` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `label_type` | varchar | variable | No | Etiquetas para imprimir |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `picking_label_type_stock_picking_rel`

**Relación muchos a muchos entre «picking.label.type» y «stock.picking»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `picking_label_type_id` | integer | 4 B | No | Referencia a picking_label_type |
| PK, FK | `stock_picking_id` | integer | 4 B | No | Referencia a stock_picking |

### `picking_type_favorite_user_rel`

**Relación muchos a muchos entre «stock.picking.type» y «res.users»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `picking_type_id` | integer | 4 B | No | Referencia a stock_picking_type |
| PK, FK | `user_id` | integer | 4 B | No | Referencia a res_users |

### `product_removal`

**Estrategia de remoción** · modelo `product.removal` · módulo `stock` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `method` | jsonb | variable | No | Método — PEPS, UEPS... |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `product_replenish`

**Reabastecimiento de producto** · modelo `product.replenish` · módulo `stock` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `route_id` | integer | 4 B | Sí | Ruta preferida → `stock_route` — Aplique una ruta específica para el reabastecimiento en lugar de las rutas predeterminadas del producto. |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `product_tmpl_id` | integer | 4 B | No | Plantilla del producto → `product_template` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad de medida → `uom_uom` |
| FK | `warehouse_id` | integer | 4 B | No | Almacén → `stock_warehouse` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_has_variants` | boolean | 1 B | No | Tiene variantes |
|  | `date_planned` | timestamp | 8 B | No | Fecha programada — Fecha en la que el reabastecimiento debe ocurrir. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `quantity` | double precision | 8 B | No | Cantidad |
| FK | `bom_id` | integer | 4 B | Sí | Lista de materiales → `mrp_bom` |
| FK | `supplier_id` | integer | 4 B | Sí | Proveedor → `product_supplierinfo` |

### `product_supplierinfo_stock_replenishment_info_rel`

**Relación muchos a muchos entre «stock.replenishment.info» y «product.supplierinfo»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_replenishment_info_id` | integer | 4 B | No | Referencia a stock_replenishment_info |
| PK, FK | `product_supplierinfo_id` | integer | 4 B | No | Referencia a product_supplierinfo |

### `stock_backorder_confirmation`

**Confirmación de orden parcial** · modelo `stock.backorder.confirmation` · módulo `stock` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `show_transfers` | boolean | 1 B | Sí | Mostrar traslados |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_backorder_confirmation_line`

**Línea de confirmación de órdenes parciales** · modelo `stock.backorder.confirmation.line` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `backorder_confirmation_id` | integer | 4 B | Sí | Traslado inmediato → `stock_backorder_confirmation` |
| FK | `picking_id` | integer | 4 B | Sí | Transferir → `stock_picking` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `to_backorder` | boolean | 1 B | Sí | Para hacer una orden parcial |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_conflict_quant_rel`

**Relación muchos a muchos entre «stock.inventory.conflict» y «stock.quant»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_inventory_conflict_id` | integer | 4 B | No | Referencia a stock_inventory_conflict |
| PK, FK | `stock_quant_id` | integer | 4 B | No | Referencia a stock_quant |

### `stock_inventory_adjustment_name`

**Referencia/motivo del ajuste de inventario** · modelo `stock.inventory.adjustment.name` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `inventory_adjustment_name` | varchar | variable | Sí | Motivo del inventario |
|  | `counting_date` | timestamp | 8 B | Sí | Fecha del conteo — Fecha en la que se fecharán los movimientos resultantes. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `accounting_date` | date | 4 B | Sí | Fecha contable — Fecha en la que se crearán los asientos contables en caso de valoración de inventario automatizada. Si está vacío, se usará la fecha de i… |

### `stock_inventory_adjustment_name_stock_quant_rel`

**Relación muchos a muchos entre «stock.inventory.adjustment.name» y «stock.quant»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_inventory_adjustment_name_id` | integer | 4 B | No | Referencia a stock_inventory_adjustment_name |
| PK, FK | `stock_quant_id` | integer | 4 B | No | Referencia a stock_quant |

### `stock_inventory_conflict`

**Conflicto en el inventario** · modelo `stock.inventory.conflict` · módulo `stock` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_inventory_conflict_stock_quant_rel`

**Relación muchos a muchos entre «stock.inventory.conflict» y «stock.quant»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_inventory_conflict_id` | integer | 4 B | No | Referencia a stock_inventory_conflict |
| PK, FK | `stock_quant_id` | integer | 4 B | No | Referencia a stock_quant |

### `stock_inventory_warning`

**Advertencia del ajuste de inventario** · modelo `stock.inventory.warning` · módulo `stock` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_inventory_warning_stock_quant_rel`

**Relación muchos a muchos entre «stock.inventory.warning» y «stock.quant»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_inventory_warning_id` | integer | 4 B | No | Referencia a stock_inventory_warning |
| PK, FK | `stock_quant_id` | integer | 4 B | No | Referencia a stock_quant |

### `stock_move_line_consume_rel`

**Relación muchos a muchos entre «stock.move.line» y «stock.move.line»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `consume_line_id` | integer | 4 B | No | Referencia a stock_move_line |
| PK, FK | `produce_line_id` | integer | 4 B | No | Referencia a stock_move_line |

### `stock_move_line_stock_put_in_pack_rel`

**Relación muchos a muchos entre «stock.put.in.pack» y «stock.move.line»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_put_in_pack_id` | integer | 4 B | No | Referencia a stock_put_in_pack |
| PK, FK | `stock_move_line_id` | integer | 4 B | No | Referencia a stock_move_line |

### `stock_move_move_rel`

**Relación muchos a muchos entre «stock.move» y «stock.move»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `move_orig_id` | integer | 4 B | No | Referencia a stock_move |
| PK, FK | `move_dest_id` | integer | 4 B | No | Referencia a stock_move |

### `stock_orderpoint_snooze`

**Posponer punto de orden** · modelo `stock.orderpoint.snooze` · módulo `stock` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `predefined_date` | varchar | variable | Sí | Posponer para |
|  | `snoozed_until` | date | 4 B | Sí | Fecha pospuesta |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_orderpoint_snooze_stock_warehouse_orderpoint_rel`

**Relación muchos a muchos entre «stock.orderpoint.snooze» y «stock.warehouse.orderpoint»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_orderpoint_snooze_id` | integer | 4 B | No | Referencia a stock_orderpoint_snooze |
| PK, FK | `stock_warehouse_orderpoint_id` | integer | 4 B | No | Referencia a stock_warehouse_orderpoint |

### `stock_package`

**Paquete** · modelo `stock.package` · módulo `stock` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `package_type_id` | integer | 4 B | Sí | Tipo de paquete → `stock_package_type` |
| FK | `location_id` | integer | 4 B | Sí | Ubicación → `stock_location` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `parent_package_id` | integer | 4 B | Sí | Contenedor → `stock_package` |
| FK | `package_dest_id` | integer | 4 B | Sí | Contenedor del destino → `stock_package` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Referencia del paquete |
|  | `complete_name` | varchar | variable | Sí | Nombre completo del paquete |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `pack_date` | date | 4 B | Sí | Fecha de empaquetado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `shipping_weight` | double precision | 8 B | Sí | Peso de envío — Peso total del paquete. |

### `stock_package_destination`

**Destino del paquete de existencias** · modelo `stock.package.destination` · módulo `stock` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `location_dest_id` | integer | 4 B | No | Ubicación de destino → `stock_location` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_package_history`

**Historial del paquete en stock** · modelo `stock.package.history` · módulo `stock` · 15 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `location_id` | integer | 4 B | Sí | Ubicación de origen → `stock_location` |
| FK | `location_dest_id` | integer | 4 B | Sí | Ubicación de destino → `stock_location` |
| FK | `package_id` | integer | 4 B | No | Paquete → `stock_package` |
| FK | `parent_orig_id` | integer | 4 B | Sí | Contenedor de origen → `stock_package` |
| FK | `parent_dest_id` | integer | 4 B | Sí | Contenedor del destino → `stock_package` |
| FK | `outermost_dest_id` | integer | 4 B | Sí | Contenedor de destino más alejado → `stock_package` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `package_name` | varchar | variable | No | Nombre del paquete |
|  | `parent_orig_name` | varchar | variable | Sí | Nombre del contenedor de origen |
|  | `parent_dest_name` | varchar | variable | Sí | Nombre del contenedor del destino |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_package_history_stock_picking_rel`

**Relación muchos a muchos entre «stock.package.history» y «stock.picking»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_picking_id` | integer | 4 B | No | Referencia a stock_picking |
| PK, FK | `stock_package_history_id` | integer | 4 B | No | Referencia a stock_package_history |

### `stock_package_stock_put_in_pack_rel`

**Relación muchos a muchos entre «stock.put.in.pack» y «stock.package»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_put_in_pack_id` | integer | 4 B | No | Referencia a stock_put_in_pack |
| PK, FK | `stock_package_id` | integer | 4 B | No | Referencia a stock_package |

### `stock_package_type`

**Tipo de paquete de existencias** · modelo `stock.package.type` · módulo `stock` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia — El primero en la secuencia es el predeterminado. |
| FK | `sequence_id` | integer | 4 B | Sí | Secuencia de la referencia → `ir_sequence` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Tipo de paquete |
|  | `barcode` | varchar | variable | Sí | Código de barras |
|  | `package_use` | varchar | variable | No | Uso del paquete — Las cajas reutilizables se utilizan para preparar lotes y después se vacían para volver a utilizarse. Al escanear una caja reutilizable m… |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `height` | double precision | 8 B | Sí | Altura — Altura del empaquetado |
|  | `width` | double precision | 8 B | Sí | Ancho — Ancho del empaquetado |
|  | `packaging_length` | double precision | 8 B | Sí | Longitud — Longitud del empaquetado |
|  | `base_weight` | double precision | 8 B | Sí | Peso — Peso del tipo de paquete |
|  | `max_weight` | double precision | 8 B | Sí | Peso máximo — Peso máximo a enviar en este paquete |

### `stock_package_type_stock_putaway_rule_rel`

**Relación muchos a muchos entre «stock.putaway.rule» y «stock.package.type»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_putaway_rule_id` | integer | 4 B | No | Referencia a stock_putaway_rule |
| PK, FK | `stock_package_type_id` | integer | 4 B | No | Referencia a stock_package_type |

### `stock_package_type_stock_route_rel`

**Relación muchos a muchos entre «stock.package.type» y «stock.route»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_package_type_id` | integer | 4 B | No | Referencia a stock_package_type |
| PK, FK | `stock_route_id` | integer | 4 B | No | Referencia a stock_route |

### `stock_picking_backorder_rel`

**Relación muchos a muchos entre «stock.backorder.confirmation» y «stock.picking»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_backorder_confirmation_id` | integer | 4 B | No | Referencia a stock_backorder_confirmation |
| PK, FK | `stock_picking_id` | integer | 4 B | No | Referencia a stock_picking |

### `stock_put_in_pack`

**Asistente para incluir en el paquete** · modelo `stock.put.in.pack` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `location_dest_id` | integer | 4 B | Sí | Destino → `stock_location` |
| FK | `package_type_id` | integer | 4 B | Sí | Tipo de paquete → `stock_package_type` |
| FK | `result_package_id` | integer | 4 B | Sí | Paquete → `stock_package` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_putaway_rule`

**Regla de almacenamiento** · modelo `stock.putaway.rule` · módulo `stock` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `category_id` | integer | 4 B | Sí | Categoría del producto → `product_category` |
| FK | `location_in_id` | integer | 4 B | No | Cuando el producto llega a → `stock_location` |
| FK | `location_out_id` | integer | 4 B | No | Almacenar en sububicación → `stock_location` |
|  | `sequence` | integer | 4 B | Sí | Prioridad — Proporciónele mayor prioridad a la categoría más especializada para que aparezca en la parte superior de la lista. |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `storage_category_id` | integer | 4 B | Sí | Categoría de almacenamiento → `stock_storage_category` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `sublocation` | varchar | variable | Sí | Sububicación |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_quant_relocate`

**Traslado de las cantidades de existencias** · modelo `stock.quant.relocate` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `dest_location_id` | integer | 4 B | Sí | Ubicación de destino → `stock_location` |
| FK | `dest_package_id` | integer | 4 B | Sí | Destino del empaque → `stock_package` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `message` | text | variable | Sí | Motivo de la reubicación |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_quant_stock_quant_relocate_rel`

**Relación muchos a muchos entre «stock.quant.relocate» y «stock.quant»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_quant_relocate_id` | integer | 4 B | No | Referencia a stock_quant_relocate |
| PK, FK | `stock_quant_id` | integer | 4 B | No | Referencia a stock_quant |

### `stock_quant_stock_request_count_rel`

**Relación muchos a muchos entre «stock.request.count» y «stock.quant»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_request_count_id` | integer | 4 B | No | Referencia a stock_request_count |
| PK, FK | `stock_quant_id` | integer | 4 B | No | Referencia a stock_quant |

### `stock_quantity_history`

**Historial de cantidad de existencias** · modelo `stock.quantity.history` · módulo `stock` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `inventory_datetime` | timestamp | 8 B | Sí | Inventario a la fecha — Elija una fecha para obtener el inventario en esa fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_reference`

**Referencia entre documentos de inventario** · modelo `stock.reference` · módulo `stock` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Referencia |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_reference_move_rel`

**Relación muchos a muchos entre «stock.move» y «stock.reference»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `move_id` | integer | 4 B | No | Referencia a stock_move |
| PK, FK | `reference_id` | integer | 4 B | No | Referencia a stock_reference |

### `stock_replenishment_info`

**Información de reabastecimiento del proveedor de inventario** · modelo `stock.replenishment.info` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `orderpoint_id` | integer | 4 B | Sí | Punto de la orden → `stock_warehouse_orderpoint` |
|  | `percent_factor` | integer | 4 B | No | Factor de porcentaje |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `based_on` | varchar | variable | No | Basado en — Estima el volumen de ventas para el periodo basado en periodos anteriores u ordena la cantidad pronosticada para ese periodo. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_replenishment_option`

**Opción de reabastecimiento de almacén de existencias** · modelo `stock.replenishment.option` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `route_id` | integer | 4 B | Sí | Ruta → `stock_route` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `replenishment_info_id` | integer | 4 B | Sí | Información de reabastecimiento → `stock_replenishment_info` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_request_count`

**Solicitar un recuento de inventario** · modelo `stock.request.count` · módulo `stock` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | Sí | Asignar a → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `inventory_date` | date | 4 B | No | Programado el — Elija una fecha para obtener el inventario en esa fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_return_picking`

**Recolección de devolución** · modelo `stock.return.picking` · módulo `stock` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `picking_id` | integer | 4 B | Sí | Recolección → `stock_picking` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_return_picking_line`

**Línea de recolección de devolución** · modelo `stock.return.picking.line` · módulo `stock` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `wizard_id` | integer | 4 B | Sí | Asistente → `stock_return_picking` |
| FK | `move_id` | integer | 4 B | Sí | Movimiento → `stock_move` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `quantity` | numeric | variable | No | Cantidad |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `to_refund` | boolean | 1 B | Sí | Actualizar cantidades en órdenes de venta o compra — Activar una disminución de la cantidad entregada/recibida en la orden de venta/compra asociada |

### `stock_route`

**Rutas de inventario** · modelo `stock.route` · módulo `stock` · 16 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `supplied_wh_id` | integer | 4 B | Sí | Almacén suministrado → `stock_warehouse` |
| FK | `supplier_wh_id` | integer | 4 B | Sí | Almacén de suministros → `stock_warehouse` |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` — Deje este campo vacío si esta ruta se comparte entre todas las empresas |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Ruta |
|  | `active` | boolean | 1 B | Sí | Activo — Si el campo activo se establece a False, permitirá ocultar la ruta sin eliminarla. |
|  | `product_selectable` | boolean | 1 B | Sí | Aplicable en el producto — Cuando se selecciona, la ruta se podrá seleccionar en la pestaña de inventario del formulario de producto. |
|  | `product_categ_selectable` | boolean | 1 B | Sí | Aplicable en la categoría de productos — Cuando se selecciona, la ruta se podrá seleccionar en las categorías de producto. |
|  | `warehouse_selectable` | boolean | 1 B | Sí | Aplicable en el almacén — Cuando se selecciona un almacén para esta ruta, esta ruta debe considerarse como la ruta predeterminada cuando los productos pasan a trav… |
|  | `package_type_selectable` | boolean | 1 B | Sí | Aplicable en el tipo de paquete — Cuando está seleccionada, la ruta se podrá elegir en los tipos de paquete |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `sale_selectable` | boolean | 1 B | Sí | Se puede seleccionar en la línea de la orden de venta |

### `stock_route_move`

**Relación muchos a muchos entre «stock.move» y «stock.route»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `move_id` | integer | 4 B | No | Referencia a stock_move |
| PK, FK | `route_id` | integer | 4 B | No | Referencia a stock_route |

### `stock_route_stock_rules_report_rel`

**Relación muchos a muchos entre «stock.rules.report» y «stock.route»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_rules_report_id` | integer | 4 B | No | Referencia a stock_rules_report |
| PK, FK | `stock_route_id` | integer | 4 B | No | Referencia a stock_route |

### `stock_route_warehouse`

**Relación muchos a muchos entre «stock.route» y «stock.warehouse»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `route_id` | integer | 4 B | No | Referencia a stock_route |
| PK, FK | `warehouse_id` | integer | 4 B | No | Referencia a stock_warehouse |

### `stock_rule`

**Regla de inventario** · modelo `stock.rule` · módulo `stock` · 24 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `location_dest_id` | integer | 4 B | No | Ubicación de destino → `stock_location` |
| FK | `location_src_id` | integer | 4 B | Sí | Ubicación de origen → `stock_location` |
| FK | `route_id` | integer | 4 B | No | Ruta → `stock_route` |
|  | `route_sequence` | integer | 4 B | Sí | Secuencia de la ruta |
| FK | `picking_type_id` | integer | 4 B | No | Tipo de operación → `stock_picking_type` |
|  | `delay` | integer | 4 B | Sí | Plazo de entrega — La fecha esperada del traslado creado se calculará en función de este plazo de entrega. |
| FK | `partner_address_id` | integer | 4 B | Sí | Dirección del contacto → `res_partner` — Dirección a la que se deben entregar los productos. Opcional. |
| FK | `warehouse_id` | integer | 4 B | Sí | Almacén → `stock_warehouse` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `action` | varchar | variable | No | Acción |
|  | `procure_method` | varchar | variable | No | Método de suministro — Tomar de las existencias: los productos se tomarán de las existencias disponibles en la ubicación de origen. Activar otra regla: el siste… |
|  | `auto` | varchar | variable | No | Movimiento automático — El valor 'Operación manual' creará un movimiento de existencias después del actual. Con 'Automático sin paso agregado', la ubicación se r… |
|  | `push_domain` | varchar | variable | Sí | Aplicabilidad push |
|  | `name` | jsonb | variable | No | Nombre — Este campo completará el origen del paquete y el nombre de sus movimientos |
|  | `active` | boolean | 1 B | Sí | Activo — Si no se encuentra seleccionado, permite ocultar la regla sin eliminarla. |
|  | `location_dest_from_rule` | boolean | 1 B | Sí | Ubicación de destino obtenida desde la regla — Cuando está configurado como True la ubicación de destino del stock.move será la regla. De lo contrario, la ubicación de destino se tomar… |
|  | `propagate_cancel` | boolean | 1 B | Sí | Cancelar siguiente movimiento — Si está seleccionada, al cancelar el movimiento creado por esta regla también cancelará el siguiente. |
|  | `propagate_carrier` | boolean | 1 B | Sí | Propagación del transportista — Cuando se selecciona, se propagará el transportista de envío. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_rules_report`

**Reporte de reglas de existencias** · modelo `stock.rules.report` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `product_tmpl_id` | integer | 4 B | No | Plantilla del producto → `product_template` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_has_variants` | boolean | 1 B | No | Tiene variantes |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_rules_report_stock_warehouse_rel`

**Relación muchos a muchos entre «stock.rules.report» y «stock.warehouse»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_rules_report_id` | integer | 4 B | No | Referencia a stock_rules_report |
| PK, FK | `stock_warehouse_id` | integer | 4 B | No | Referencia a stock_warehouse |

### `stock_scrap`

**Desechar** · modelo `stock.scrap` · módulo `stock` · 23 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `product_uom_id` | integer | 4 B | No | Unidad → `uom_uom` |
| FK | `lot_id` | integer | 4 B | Sí | Número de serie/lote → `stock_lot` |
| FK | `package_id` | integer | 4 B | Sí | Paquete → `stock_package` |
| FK | `owner_id` | integer | 4 B | Sí | Propietario → `res_partner` |
| FK | `picking_id` | integer | 4 B | Sí | Recolección → `stock_picking` |
| FK | `location_id` | integer | 4 B | No | Ubicación de origen → `stock_location` |
| FK | `scrap_location_id` | integer | 4 B | No | Ubicación de desecho → `stock_location` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Referencia |
|  | `origin` | varchar | variable | Sí | Documento origen |
|  | `state` | varchar | variable | Sí | Estado |
|  | `scrap_qty` | numeric | variable | No | Cantidad |
|  | `should_replenish` | boolean | 1 B | Sí | Reabastecer cantidades — Esta opción habilita el reabastecimiento de los productos desechados |
|  | `date_done` | timestamp | 8 B | Sí | Fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `production_id` | integer | 4 B | Sí | Orden de fabricación → `mrp_production` |
| FK | `workorder_id` | integer | 4 B | Sí | Orden de trabajo → `mrp_workorder` |
| FK | `bom_id` | integer | 4 B | Sí | Kit → `mrp_bom` |

### `stock_scrap_reason_tag`

**Etiqueta del motivo de descarte** · modelo `stock.scrap.reason.tag` · módulo `stock` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `color` | varchar | variable | Sí | Color |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_scrap_stock_scrap_reason_tag_rel`

**Relación muchos a muchos entre «stock.scrap» y «stock.scrap.reason.tag»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `stock_scrap_id` | integer | 4 B | No | Referencia a stock_scrap |
| PK, FK | `stock_scrap_reason_tag_id` | integer | 4 B | No | Referencia a stock_scrap_reason_tag |

### `stock_storage_category`

**Categoría de almacenamiento** · modelo `stock.storage.category` · módulo `stock` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Categoría de almacenamiento |
|  | `allow_new_product` | varchar | variable | No | Permitir nuevo producto |
|  | `max_weight` | numeric | variable | Sí | Peso máximo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_storage_category_capacity`

**Capacidad de la categoría de almacenamiento** · modelo `stock.storage.category.capacity` · módulo `stock` · 9 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `storage_category_id` | integer | 4 B | No | Categoría de almacenamiento → `stock_storage_category` |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `package_type_id` | integer | 4 B | Sí | Tipo de paquete → `stock_package_type` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `quantity` | double precision | 8 B | No | Cantidad |

### `stock_traceability_report`

**Reporte de trazabilidad** · modelo `stock.traceability.report` · módulo `stock` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_warn_insufficient_qty_scrap`

**Advertir de cantidad de desecho insuficiente** · modelo `stock.warn.insufficient.qty.scrap` · módulo `stock` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | No | Producto → `product_product` |
| FK | `location_id` | integer | 4 B | No | Ubicación → `stock_location` |
| FK | `scrap_id` | integer | 4 B | Sí | Desechar → `stock_scrap` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `product_uom_name` | varchar | variable | No | Unidad |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `quantity` | double precision | 8 B | No | Cantidad |

### `stock_wh_resupply_table`

**Relación muchos a muchos entre «stock.warehouse» y «stock.warehouse»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `supplied_wh_id` | integer | 4 B | No | Referencia a stock_warehouse |
| PK, FK | `supplier_wh_id` | integer | 4 B | No | Referencia a stock_warehouse |

### `template_attribute_value_stock_move_rel`

**Relación muchos a muchos entre «stock.move» y «product.template.attribute.value»** · tabla intermedia, sin modelo propio · módulo `stock` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `move_id` | integer | 4 B | No | Referencia a stock_move |
| PK, FK | `template_attribute_value_id` | integer | 4 B | No | Referencia a product_template_attribute_value |

## Módulo `stock_account`

### `product_value`

**Valor del producto** · modelo `product.value` · módulo `stock_account` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `product_id` | integer | 4 B | Sí | Producto → `product_product` |
| FK | `lot_id` | integer | 4 B | Sí | Lote → `stock_lot` |
| FK | `move_id` | integer | 4 B | Sí | Movimiento → `stock_move` |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `user_id` | integer | 4 B | No | Usuario → `res_users` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `description` | varchar | variable | Sí | Descripción |
|  | `value` | numeric | variable | No | Valor |
|  | `date` | timestamp | 8 B | No | Fecha |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `stock_sms`

### `confirm_stock_sms`

**Confirmar existencias por SMS** · modelo `confirm.stock.sms` · módulo `stock_sms` · 5 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `stock_picking_sms_rel`

**Relación muchos a muchos entre «confirm.stock.sms» y «stock.picking»** · tabla intermedia, sin modelo propio · módulo `stock_sms` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `confirm_stock_sms_id` | integer | 4 B | No | Referencia a confirm_stock_sms |
| PK, FK | `stock_picking_id` | integer | 4 B | No | Referencia a stock_picking |

## Módulo `uom`

### `uom_uom`

**Unidad de medida del producto** · modelo `uom.uom` · módulo `uom` · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `relative_uom_id` | integer | 4 B | Sí | Unidad de referencia → `uom_uom` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `parent_path` | varchar | variable | Sí | Ruta principal |
|  | `name` | jsonb | variable | No | Nombre de la unidad |
|  | `relative_factor` | numeric | variable | No | Contiene — Qué tan mayor o menor es esta unidad en comparación con la unidad de medida de referencia |
|  | `factor` | numeric | variable | Sí | Cantidad absoluta |
|  | `active` | boolean | 1 B | Sí | Activo — Desactive el campo activo para desactivar la unidad de medida sin eliminarla. |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `package_type_id` | integer | 4 B | Sí | Tipo de paquete → `stock_package_type` |
|  | `is_pos_groupable` | boolean | 1 B | Sí | Agrupar productos en PdV — Indique si desea agrupar los productos de esta unidad en las órdenes del punto de venta |

## Módulo `utm`

### `utm_campaign`

**Campaña UTM** · modelo `utm.campaign` · módulo `utm` · 13 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_id` | integer | 4 B | No | Responsable → `res_users` |
| FK | `stage_id` | integer | 4 B | No | Etapa → `utm_stage` |
|  | `color` | integer | 4 B | Sí | Índice de color |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Identificador de la campaña |
|  | `title` | jsonb | variable | No | Nombre de la campaña |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `is_auto_campaign` | boolean | 1 B | Sí | Campaña generada de forma automática — Nos permite filtrar las campañas relevantes |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
| FK | `company_id` | integer | 4 B | Sí | Empresa → `res_company` |

### `utm_medium`

**Medio UTM** · modelo `utm.medium` · módulo `utm` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre del medio |
|  | `active` | boolean | 1 B | Sí | Activo |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `utm_source`

**Fuente UTM** · modelo `utm.source` · módulo `utm` · 6 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre de la fuente |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `utm_stage`

**Etapa de la campaña** · modelo `utm.stage` · módulo `utm` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `utm_tag`

**Etiquetas UTM** · modelo `utm.tag` · módulo `utm` · 7 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `color` | integer | 4 B | Sí | Índice de color — Color de etiqueta. Si no tiene color significa que no se puede visualizar en kanban para distinguir las etiquetas internas de las etiquet… |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | jsonb | variable | No | Nombre |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `utm_tag_rel`

**Relación muchos a muchos entre «utm.campaign» y «utm.tag»** · tabla intermedia, sin modelo propio · módulo `utm` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `tag_id` | integer | 4 B | No | Referencia a utm_campaign |
| PK, FK | `campaign_id` | integer | 4 B | No | Referencia a utm_tag |

## Módulo `web`

### `base_document_layout`

**Diseño de documentos de la empresa** · modelo `base.document.layout` · módulo `web` · 8 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `company_id` | integer | 4 B | No | Empresa → `res_company` |
| FK | `report_layout_id` | integer | 4 B | Sí | Diseño del reporte → `report_layout` |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |
|  | `from_invoice` | boolean | 1 B | Sí | De factura |

### `res_users_settings_embedded_action`

**Ajustes del usuario para acciones incrustadas** · modelo `res.users.settings.embedded.action` · módulo `web` · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `user_setting_id` | integer | 4 B | No | User Setting → `res_users_settings` |
| FK | `action_id` | integer | 4 B | No | Action → `ir_act_window` |
|  | `res_id` | integer | 4 B | Sí | Res |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `res_model` | varchar | variable | No | Res Model |
|  | `embedded_actions_order` | varchar | variable | Sí | List order of embedded action ids |
|  | `embedded_actions_visibility` | varchar | variable | Sí | List visibility of embedded actions ids |
|  | `embedded_visibility` | boolean | 1 B | Sí | Is top bar visible |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `web_tour`

### `res_users_web_tour_tour_rel`

**Relación muchos a muchos entre «web_tour.tour» y «res.users»** · tabla intermedia, sin modelo propio · módulo `web_tour` · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK, FK | `web_tour_tour_id` | integer | 4 B | No | Referencia a web_tour_tour |
| PK, FK | `res_users_id` | integer | 4 B | No | Referencia a res_users |

### `web_tour_tour`

**Recorridos** · modelo `web_tour.tour` · módulo `web_tour` · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `name` | varchar | variable | No | Nombre |
|  | `url` | varchar | variable | Sí | URL de inicio |
|  | `rainbow_man_message` | jsonb | variable | Sí | Mensaje del hombre arcoíris |
|  | `custom` | boolean | 1 B | Sí | Personalizado |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

### `web_tour_tour_step`

**Paso del recorrido** · modelo `web_tour.tour.step` · módulo `web_tour` · 11 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | ID |
| FK | `tour_id` | integer | 4 B | No | Recorrido → `web_tour_tour` |
|  | `sequence` | integer | 4 B | Sí | Secuencia |
| FK | `create_uid` | integer | 4 B | Sí | Creado por → `res_users` |
| FK | `write_uid` | integer | 4 B | Sí | Última actualización por → `res_users` |
|  | `trigger` | varchar | variable | No | Activar |
|  | `content` | varchar | variable | Sí | Contenido |
|  | `tooltip_position` | varchar | variable | Sí | Posición de la información sobre herramientas |
|  | `run` | varchar | variable | Sí | Ejecutar |
|  | `create_date` | timestamp | 8 B | Sí | Creado el |
|  | `write_date` | timestamp | 8 B | Sí | Última actualización el |

## Módulo `sin módulo`

### `ir_act_client`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 17 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
| FK | `binding_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `type` | varchar | variable | No | — |
|  | `path` | varchar | variable | Sí | — |
|  | `binding_type` | varchar | variable | No | — |
|  | `binding_view_types` | varchar | variable | Sí | — |
|  | `name` | jsonb | variable | No | — |
|  | `help` | jsonb | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |
|  | `tag` | varchar | variable | No | — |
|  | `target` | varchar | variable | Sí | — |
|  | `res_model` | varchar | variable | Sí | — |
|  | `context` | varchar | variable | No | — |
|  | `params_store` | bytea | variable | Sí | — |

### `ir_act_report_xml`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 23 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
| FK | `binding_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `type` | varchar | variable | No | — |
|  | `path` | varchar | variable | Sí | — |
|  | `binding_type` | varchar | variable | No | — |
|  | `binding_view_types` | varchar | variable | Sí | — |
|  | `name` | jsonb | variable | No | — |
|  | `help` | jsonb | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |
| FK | `paperformat_id` | integer | 4 B | Sí | Referencia a report_paperformat |
|  | `model` | varchar | variable | No | — |
|  | `report_type` | varchar | variable | No | — |
|  | `report_name` | varchar | variable | No | — |
|  | `report_file` | varchar | variable | Sí | — |
|  | `attachment` | varchar | variable | Sí | — |
|  | `domain` | varchar | variable | Sí | — |
|  | `print_report_name` | jsonb | variable | Sí | — |
|  | `multi` | boolean | 1 B | Sí | — |
|  | `attachment_use` | boolean | 1 B | Sí | — |
|  | `is_invoice_report` | boolean | 1 B | Sí | — |

### `ir_act_server`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 48 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
| FK | `binding_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `type` | varchar | variable | No | — |
|  | `path` | varchar | variable | Sí | — |
|  | `binding_type` | varchar | variable | No | — |
|  | `binding_view_types` | varchar | variable | Sí | — |
|  | `name` | jsonb | variable | No | — |
|  | `help` | jsonb | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |
|  | `sequence` | integer | 4 B | Sí | — |
| FK | `model_id` | integer | 4 B | No | Referencia a ir_model |
| FK | `parent_id` | integer | 4 B | Sí | Referencia a ir_act_server |
| FK | `crud_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `link_field_id` | integer | 4 B | Sí | Referencia a ir_model_fields |
| FK | `update_field_id` | integer | 4 B | Sí | Referencia a ir_model_fields |
| FK | `update_related_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `sequence_id` | integer | 4 B | Sí | Referencia a ir_sequence |
| FK | `selection_value` | integer | 4 B | Sí | Referencia a ir_model_fields_selection |
|  | `automated_name` | varchar | variable | Sí | — |
|  | `usage` | varchar | variable | No | — |
|  | `state` | varchar | variable | No | — |
|  | `update_path` | varchar | variable | Sí | — |
|  | `update_m2m_operation` | varchar | variable | Sí | — |
|  | `update_boolean_value` | varchar | variable | Sí | — |
|  | `evaluation_type` | varchar | variable | Sí | — |
|  | `resource_ref` | varchar | variable | Sí | — |
|  | `webhook_url` | varchar | variable | Sí | — |
|  | `code` | text | variable | Sí | — |
|  | `value` | text | variable | Sí | — |
|  | `html_value` | text | variable | Sí | — |
| FK | `activity_user_id` | integer | 4 B | Sí | Referencia a res_users |
| FK | `activity_type_id` | integer | 4 B | Sí | Referencia a mail_activity_type |
| FK | `template_id` | integer | 4 B | Sí | Referencia a mail_template |
|  | `activity_date_deadline_range` | integer | 4 B | Sí | — |
|  | `activity_summary` | varchar | variable | Sí | — |
|  | `followers_type` | varchar | variable | Sí | — |
|  | `followers_partner_field_name` | varchar | variable | Sí | — |
|  | `mail_post_method` | varchar | variable | Sí | — |
|  | `activity_date_deadline_range_type` | varchar | variable | Sí | — |
|  | `activity_user_type` | varchar | variable | Sí | — |
|  | `activity_user_field_name` | varchar | variable | Sí | — |
|  | `activity_note` | text | variable | Sí | — |
|  | `mail_post_autofollow` | boolean | 1 B | Sí | — |
| FK | `sms_template_id` | integer | 4 B | Sí | Referencia a sms_template |
|  | `sms_method` | varchar | variable | Sí | — |

### `ir_act_url`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 14 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
| FK | `binding_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `type` | varchar | variable | No | — |
|  | `path` | varchar | variable | Sí | — |
|  | `binding_type` | varchar | variable | No | — |
|  | `binding_view_types` | varchar | variable | Sí | — |
|  | `name` | jsonb | variable | No | — |
|  | `help` | jsonb | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |
|  | `target` | varchar | variable | No | — |
|  | `url` | text | variable | No | — |

### `ir_act_window`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 25 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
| FK | `binding_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `type` | varchar | variable | No | — |
|  | `path` | varchar | variable | Sí | — |
|  | `binding_type` | varchar | variable | No | — |
|  | `binding_view_types` | varchar | variable | Sí | — |
|  | `name` | jsonb | variable | No | — |
|  | `help` | jsonb | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |
| FK | `view_id` | integer | 4 B | Sí | Referencia a ir_ui_view |
|  | `res_id` | integer | 4 B | Sí | — |
|  | `limit` | integer | 4 B | Sí | — |
| FK | `search_view_id` | integer | 4 B | Sí | Referencia a ir_ui_view |
|  | `domain` | varchar | variable | Sí | — |
|  | `context` | varchar | variable | No | — |
|  | `res_model` | varchar | variable | No | — |
|  | `target` | varchar | variable | Sí | — |
|  | `view_mode` | varchar | variable | No | — |
|  | `mobile_view_mode` | varchar | variable | Sí | — |
|  | `usage` | varchar | variable | Sí | — |
|  | `filter` | boolean | 1 B | Sí | — |
|  | `cache` | boolean | 1 B | Sí | — |

### `ir_act_window_view`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 10 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `sequence` | integer | 4 B | Sí | — |
| FK | `view_id` | integer | 4 B | Sí | Referencia a ir_ui_view |
| FK | `act_window_id` | integer | 4 B | Sí | Referencia a ir_act_window |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `view_mode` | varchar | variable | No | — |
|  | `multi` | boolean | 1 B | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |

### `ir_actions`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 12 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
| FK | `binding_model_id` | integer | 4 B | Sí | Referencia a ir_model |
| FK | `create_uid` | integer | 4 B | Sí | Referencia a res_users |
| FK | `write_uid` | integer | 4 B | Sí | Referencia a res_users |
|  | `type` | varchar | variable | No | — |
|  | `path` | varchar | variable | Sí | — |
|  | `binding_type` | varchar | variable | No | — |
|  | `binding_view_types` | varchar | variable | Sí | — |
|  | `name` | jsonb | variable | No | — |
|  | `help` | jsonb | variable | Sí | — |
|  | `create_date` | timestamp | 8 B | Sí | — |
|  | `write_date` | timestamp | 8 B | Sí | — |

### `orm_signaling_assets`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `date` | timestamp | 8 B | Sí | — |

### `orm_signaling_default`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `date` | timestamp | 8 B | Sí | — |

### `orm_signaling_groups`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `date` | timestamp | 8 B | Sí | — |

### `orm_signaling_registry`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `date` | timestamp | 8 B | Sí | — |

### `orm_signaling_routing`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `date` | timestamp | 8 B | Sí | — |

### `orm_signaling_stable`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `date` | timestamp | 8 B | Sí | — |

### `orm_signaling_templates`

**Sin modelo de Odoo** · tabla intermedia, sin modelo propio · 2 columnas

| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |
|---|---|---|---|---|---|
| PK | `id` | integer | 4 B | No | — |
|  | `date` | timestamp | 8 B | Sí | — |
