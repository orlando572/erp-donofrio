# 2.2.1.5.3 Diccionario de datos de los módulos de D'Onofrio

Los módulos desarrollados para D'Onofrio crean seis tablas; cada una incluye además las columnas estándar de Odoo que registran quién creó y modificó el registro y cuándo. El Tablero gerencial no crea tablas. La cadena de frío agrega a las ubicaciones la casilla «Controlar temperatura» y el rango mínimo y máximo, y a los lotes la fecha de aviso de vencimiento. PK = clave primaria y FK = clave foránea. El diccionario completo del esquema de Odoo se genera con la herramienta del proyecto.

**Tabla 4.4. Módulos de D'Onofrio**

| Tabla | Campo | Tipo | Descripción |
|---|---|---|---|
| `donofrio_calidad_punto` | `id` (PK) | integer | ID |
|  | `sequence` | integer | Secuencia |
|  | `categ_id` (FK) | integer | Categoría de producto → `product_category` |
|  | `tipo` | varchar | Tipo |
|  | `unidad` | varchar | Unidad |
|  | `name` | jsonb | Punto de control |
|  | `active` | boolean | Activo |
|  | `valor_min` | double | Mínimo |
|  | `valor_max` | double | Máximo |
| `donofrio_calidad_inspeccion` | `---` (---) | --- | --- |
|  | `id` (PK) | integer | ID |
|  | `production_id` (FK) | integer | Orden de producción → `mrp_production` |
|  | `lot_id` (FK) | integer | Lote → `stock_lot` |
|  | `product_id` (FK) | integer | Producto → `product_product` |
|  | `company_id` (FK) | integer | Compañía → `res_company` |
|  | `inspector_id` (FK) | integer | Inspector → `res_users` |
|  | `name` | varchar | Número |
|  | `state` | varchar | Estado |
|  | `motivo_rechazo` | text | Motivo del rechazo |
| `donofrio_calidad_linea` | `---` (---) | --- | --- |
|  | `id` (PK) | integer | ID |
|  | `inspeccion_id` (FK) | integer | Inspección → `donofrio_calidad_inspeccion` |
|  | `punto_id` (FK) | integer | Punto de control → `donofrio_calidad_punto` |
|  | `sequence` | integer | Secuencia |
|  | `resultado` | varchar | Resultado |
|  | `medido` | boolean | Medido |
|  | `cumple_manual` | boolean | Cumple |
|  | `medicion` | double | Medición |
| `donofrio_liquidacion` | `---` (---) | --- | --- |
|  | `id` (PK) | integer | ID |
|  | `partner_id` (FK) | integer | Heladero → `res_partner` |
|  | `pricelist_id` (FK) | integer | Lista de precios → `product_pricelist` |
|  | `company_id` (FK) | integer | Compañía → `res_company` |
|  | `order_id` (FK) | integer | Pedido de venta → `sale_order` |
|  | `liquidador_id` (FK) | integer | Liquidador → `res_users` |
|  | `name` | varchar | Número |
|  | `state` | varchar | Estado |
|  | `fecha` | date | Fecha |
|  | `total_importe` | numeric | Importe vendido |
|  | `total_comision` | numeric | Comisión |
|  | `diferencia_efectivo` | numeric | Diferencia de efectivo |
|  | `porcentaje_comision` | double | Comisión (%) |
|  | `efectivo_entregado` | double | Efectivo entregado |
|  | `total_vendido` | double | Unidades vendidas |
| `donofrio_liquidacion_linea` | `---` (---) | --- | --- |
|  | `id` (PK) | integer | ID |
|  | `liquidacion_id` (FK) | integer | Liquidación → `donofrio_liquidacion` |
|  | `product_id` (FK) | integer | Producto → `product_product` |
|  | `precio_unitario` | numeric | Precio |
|  | `importe` | numeric | Importe |
|  | `despachado` | double | Despachado |
|  | `devuelto` | double | Devuelto |
|  | `merma` | double | Merma |
|  | `vendido` | double | Vendido |
| `donofrio_temperatura` | `---` (---) | --- | --- |
|  | `id` (PK) | integer | ID |
|  | `location_id` (FK) | integer | Ubicación → `stock_location` |
|  | `user_id` (FK) | integer | Registrado por → `res_users` |
|  | `company_id` (FK) | integer | Compañía → `res_company` |
|  | `observaciones` | text | Observaciones |
|  | `fuera_de_rango` | boolean | Fuera de rango |
|  | `fecha` | timestamp | Fecha y hora |
|  | `temperatura` | double | Temperatura (°C) |
