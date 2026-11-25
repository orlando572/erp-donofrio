# 5.5b Documentación del módulo `donofrio_calidad` (M1)

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn · **Revisa:** Orlando (dueño del módulo) · **Fuente:** `addons/donofrio_calidad/` en `develop` (PR #219, #220, #221 y #224; release [`v1.1.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.1.0), mini gate en [el mini gate de M1](../scrum/gates/gate-m1-calidad.md)), una base de desarrollo con el módulo instalado y las capturas de [`docs/capturas/sprint-4/`](../capturas/sprint-4/)
>
> Complementa la sección 5.5 (`donofrio_base`). **No** sustituye al ER general del núcleo (4.2.6): las tres tablas de este módulo se listan aquí, extraídas de la base real con `information_schema`, y **sí están** en el ER general (4.2.6, área «Calidad (M1)») y en el diccionario del núcleo (Tablas 4.2.8-37 a 4.2.8-39), regenerados con `scripts/diagrama_er.py` y `scripts/diccionario_datos.py` sobre una base con el módulo instalado.

## 5.5b.1 Qué hace

La Calidad estándar de Odoo es Enterprise, así que M1 la construye como módulo propio (HU-17 y HU-18; RF011 y RF012; CU008):

1. Define **puntos de control** (qué se mide y su norma).
2. Al **terminar una orden de producción** crea una **inspección pendiente por cada lote** producido.
3. El inspector mide los puntos, y el lote se **aprueba** (solo si todo cumple) o se **rechaza** (con motivo).
4. Un lote **rechazado no se despacha** a un cliente (RNF005).
5. De una inspección aprobada se emite el **certificado de calidad del lote en PDF** con las mediciones, el responsable y el logo.

## 5.5b.2 Archivos

| Ruta (`addons/donofrio_calidad/`) | Contenido |
|---|---|
| `__manifest__.py` | Depende de `donofrio_base`, `mrp`, `stock` y `product_expiry`; módulo con aplicación (menú «Calidad») |
| `models/calidad_punto.py` | `donofrio.calidad.punto`: punto de control, con rango o cumple / no cumple |
| `models/calidad_inspeccion.py` | `donofrio.calidad.inspeccion` y `donofrio.calidad.linea`: estados, aprobar, rechazar y certificado |
| `models/mrp_production.py` | Extiende `mrp.production.button_mark_done`: crea las inspecciones pendientes |
| `models/stock_lot.py` | `calidad_estado` del lote (sin inspección, pendiente, aprobado, rechazado) |
| `models/stock_move_line.py` | Bloquea la salida a cliente de un lote rechazado |
| `models/report_certificado.py`, `report/calidad_report.xml` | Reporte QWeb del certificado; error si la inspección no está aprobada |
| `security/` | Grupos `Calidad: inspector` y `Calidad: jefatura` y `ir.model.access.csv` |
| `data/calidad_data.xml` | Secuencia `INS/` y cinco puntos de control; asigna el grupo al usuario Inspector de Calidad |
| `views/calidad_views.xml` | Lista, formulario, búsqueda, acciones y menú |
| `tests/test_inspeccion.py` | 13 pruebas (y `test_pdv.py`, 2, y `test_idioma.py`, 1) |

## 5.5b.3 Estados y reglas

| Estado | Cómo se llega | Qué permite |
|---|---|---|
| Pendiente (`borrador`) | Se crea sola al terminar la OP | Iniciar la medición (genera una línea por cada punto que aplica al producto) |
| En medición (`en_curso`) | Botón «Iniciar medición» | Registrar mediciones; aprobar o rechazar |
| Aprobado (`aprobada`) | «Aprobar lote»: **todos** los puntos deben cumplir | Emitir el certificado PDF |
| Rechazado (`rechazada`) | «Rechazar lote» con **motivo** | Deja un mensaje y una actividad al responsable de la orden (reproceso o descarte); el lote no sale a un cliente |

Un punto con rango cumple si el valor medido está entre el mínimo y el máximo; un punto «cumple / no cumple» se marca a mano. Un punto sin medir queda «Pendiente» y **no deja aprobar**. Hay una sola inspección por orden y lote (restricción `UNIQUE`). Un lote sin inspección **no** se bloquea, para no romper los flujos de la Fase 1.

## 5.5b.4 Puntos de control cargados

| Punto | Norma | Aplica a |
|---|---|---|
| Pasteurización | 80 a 85 °C | Helados |
| Endurecimiento | −40 a −18 °C | Helados |
| Peso neto por unidad (±2 %) | 0.98 a 1.02 × peso nominal | Todos |
| Análisis microbiológico | Cumple / no cumple | Todos |
| Humedad del panetón | 22 a 28 % | Panetón |

Las normas son **supuestos del caso** (datos ficticios, S2): el mínimo y el máximo del endurecimiento (−40 y −18) y el rango de humedad no vienen de una norma real.

## 5.5b.5 Seguridad

| Grupo | Puede |
|---|---|
| Usuarios de inventario (`stock.group_stock_user`) | Solo leer inspecciones y mediciones |
| `Calidad: inspector` (incluye inventario y fabricación) | Crear y modificar inspecciones; leer los puntos de control |
| `Calidad: jefatura` | Todo lo anterior, más crear, modificar y borrar puntos de control y borrar inspecciones |

Un usuario sin ninguno de esos grupos recibe `AccessError` (prueba `test_permisos_del_inspector_y_de_un_usuario_sin_grupo`). El usuario de prueba «Inspector de Calidad» de `donofrio_base` recibe el grupo de inspector al instalar el módulo.

## 5.5b.6 Diccionario de datos

Extraído de la base `donofrio` con el módulo instalado (`information_schema`). Las tres tablas llevan los campos de auditoría de Odoo (`create_uid`, `write_uid`, `create_date`, `write_date`), que no se repiten abajo.

**`donofrio_calidad_punto`**

| Clave | Campo | Tipo | Nulo | Descripción |
|---|---|---|---|---|
| PK | `id` | integer | No | |
| FK | `categ_id` | integer | Sí | Categoría de producto → `product_category` (vacío = todos) |
| | `name` | jsonb | No | Punto de control (traducible) |
| | `sequence` | integer | Sí | Orden |
| | `active` | boolean | Sí | |
| | `tipo` | varchar | No | `rango` o `aprobacion` |
| | `valor_min`, `valor_max` | double precision | Sí | Norma del rango (restricción: mínimo ≤ máximo) |
| | `unidad` | varchar | Sí | °C, %, etc. |

**`donofrio_calidad_inspeccion`**

| Clave | Campo | Tipo | Nulo | Descripción |
|---|---|---|---|---|
| PK | `id` | integer | No | |
| FK | `production_id` | integer | No | Orden de producción → `mrp_production` |
| FK | `lot_id` | integer | No | Lote → `stock_lot` (`UNIQUE` con `production_id`) |
| FK | `product_id` | integer | Sí | Producto del lote (relacionado, almacenado) → `product_product` |
| FK | `company_id` | integer | No | Compañía → `res_company` |
| FK | `inspector_id` | integer | Sí | Inspector → `res_users` |
| | `name` | varchar | Sí | Número `INS/00001` |
| | `state` | varchar | No | `borrador`, `en_curso`, `aprobada` o `rechazada` |
| | `motivo_rechazo` | text | Sí | |

**`donofrio_calidad_linea`**

| Clave | Campo | Tipo | Nulo | Descripción |
|---|---|---|---|---|
| PK | `id` | integer | No | |
| FK | `inspeccion_id` | integer | No | Inspección → `donofrio_calidad_inspeccion` (borrado en cascada) |
| FK | `punto_id` | integer | No | Punto de control → `donofrio_calidad_punto` |
| | `sequence` | integer | Sí | Del punto de control |
| | `medicion` | double precision | Sí | Valor medido |
| | `medido` | boolean | Sí | Se marca al registrar un valor |
| | `cumple_manual` | boolean | Sí | Para los puntos «cumple / no cumple» |
| | `resultado` | varchar | Sí | `pendiente`, `cumple` o `no_cumple` (calculado) |

```text
mrp_production 1───* donofrio_calidad_inspeccion *───1 stock_lot
                              1
                              │
                              *
                    donofrio_calidad_linea *───1 donofrio_calidad_punto
```

## 5.5b.7 Pruebas y evidencia

`scripts/test.sh donofrio_calidad`: **45 pruebas, sin errores** (13 de inspección, 2 del punto de venta, 1 de idioma y 29 de la cadena de frío de [5.5d](05_05_modulo_donofrio_frio.md)). Las de inspección cubren la creación al terminar la OP y sin duplicados, líneas según el producto, aprobar con y sin cumplir, rechazar con motivo, despacho de lote rechazado y aprobado, unicidad, permisos, certificado de aprobada y error en las demás.

| Qué se verificó en la pantalla de Odoo (base `donofrio`, usuario Inspector de Calidad, con los datos de demostración de la HU-16; PNG de 1600 × 900, tomados el 25/11/2026) | Captura |
|---|---|
| Lista de inspecciones por medir | [`HU-17_lista_inspecciones.png`](../capturas/sprint-4/HU-17_lista_inspecciones.png) |
| Medir los cuatro puntos desde la pantalla y aprobar (INS/00180, aprobada, con las cuatro mediciones dentro de su norma) | [`HU-17_inspeccion_aprobada.png`](../capturas/sprint-4/HU-17_inspeccion_aprobada.png) |
| Inspección rechazada por pasteurización a 79.46 °C (INS/00177), con su motivo | [`HU-17_inspeccion_rechazada.png`](../capturas/sprint-4/HU-17_inspeccion_rechazada.png) |
| Certificado PDF de INS/00180 con logo, mediciones y responsable | [`HU-18_certificado_pdf.png`](../capturas/sprint-4/HU-18_certificado_pdf.png) |

## 5.5b.8 Límites

- **El bloqueo del despacho se probó con pruebas automáticas, no en la pantalla.** Cubre la salida a cliente por una transferencia y, desde el PR #224, el punto de venta (`test_pdv.py`, 2 pruebas); el bloqueo en el PdV no se vio en la pantalla.
- **Las inspecciones de las capturas son datos de demostración** (HU-16, 188 inspecciones en la base de desarrollo, no en el repositorio); se tomaron solo con lectura, sin crear ni editar registros. En un despliegue nuevo solo se crean al terminar una orden de fabricación.
- En las capturas, el historial de cada inspección figura a nombre de «OdooBot», porque la demostración se cargó por script; al crearla un usuario en la pantalla, queda su nombre.
- El módulo se instaló (`-i`) y se actualizó (`-u`) sobre la base `donofrio`, que tiene datos, sin errores ni avisos. No se probó una actualización entre dos versiones distintas del módulo, porque solo existe una.
- El mensaje de creación del historial de cambios sale en español: el módulo trae `i18n/es.po` desde el PR #224 (`test_idioma.py`); los otros módulos propios no traen `.po` y sus textos están en español en el código.
- El aviso del rechazo al **jefe de producción** (CU008, A1) se resuelve con una actividad al responsable de la orden; si la orden no tiene responsable, la actividad queda para quien rechaza.
