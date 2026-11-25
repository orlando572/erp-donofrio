# 5.5d Documentación de la cadena de frío (M3, incremento de `donofrio_calidad`)

> **Estado:** versión final del Cierre (25/11/2026) · **Autor:** Orlando (dueño del módulo) · **Revisa:** Evelyn · **Fuente:** `addons/donofrio_calidad/` en `develop` (PR #226, HU-19, commit `98263c9`; release [`v1.3.0`](https://github.com/orlando572/erp-donofrio/releases/tag/v1.3.0), mini gate en [el mini gate de M3](../scrum/gates/gate-m3-cadena-frio.md)), una base nueva con el módulo instalado y las capturas de [`docs/capturas/sprint-4/`](../capturas/sprint-4/)
>
> Complementa 5.5 (`donofrio_base`), 5.5b (`donofrio_calidad`, M1) y 5.5c (`donofrio_heladeros`, M2). La cadena de frío **no es un módulo aparte**: es un incremento de `donofrio_calidad`, así que no tiene carpeta propia. Su tabla nueva ya está en el ER general ([4.2.6](04_02_modelo_de_datos.md), 42 tablas) y en el diccionario ([4.2.8, Tabla 42](04_02_diccionario_datos.md)); aquí solo se explica cómo funciona y qué se verificó.

## 5.5d.1 Qué hace

En la Fase 1 el rango de temperatura de una cámara iba solo en el **nombre** de la ubicación («Cámara de congelación (-25 °C)») y las lecturas se anotaban en papel. M3 (HU-19; RF008; CU006) lo lleva al sistema:

1. Cada **ubicación interna** puede tener un **rango de temperatura** (mínimo y máximo, en °C) y la casilla «Controlar temperatura».
2. El almacén registra **lecturas** de temperatura por ubicación (valor, fecha y hora, quién la tomó y observaciones).
3. La lectura queda **marcada como «Fuera de rango»** si la ubicación se controla y el valor sale de su rango (los extremos cuentan como dentro).
4. Si queda fuera de rango, el sistema crea una **actividad para el jefe de almacén** con la ubicación, el valor y el rango. Una lectura nunca genera dos veces la misma actividad.
5. Un **cron diario** avisa al jefe de almacén de los **lotes con stock que vencen en los próximos N días** (7 por defecto), **una sola vez por lote**.

El sistema **no mueve ni bloquea lotes**: la actividad pide revisar los lotes almacenados y decidir su destino (CU006, A1). Es el punto crítico de control de temperatura de HACCP ([9.7](../plan/09_normas_marcos.md)).

## 5.5d.2 Archivos

Todo vive en `addons/donofrio_calidad/` (el commit de código tocó 12 archivos; el resto del módulo es de M1).

| Ruta | Contenido |
|---|---|
| `models/calidad_temperatura.py` | `donofrio.temperatura`: la lectura, `fuera_de_rango`, destinatarios (`_usuarios_alerta`) y la actividad (`_alertar`) |
| `models/stock_location.py` | Extiende `stock.location` con `control_temperatura`, `temp_min` y `temp_max`, la restricción del rango y `_cargar_rangos_frio` |
| `models/stock_lot.py` | Extiende `stock.lot` con `alerta_vencimiento_fecha`, `_dias_alerta_vencimiento` y el cron `_cron_lotes_por_vencer` |
| `data/calidad_data.xml` | Función que carga los rangos de las cámaras, el parámetro `donofrio_calidad.dias_alerta_vencimiento` (`noupdate`) y el cron «Calidad: lotes por vencer» |
| `security/ir.model.access.csv` | Tres líneas para `donofrio.temperatura` (ver 5.5d.5) |
| `views/calidad_views.xml` | Grupo «Cadena de frío» en el formulario de la ubicación; lista, formulario y búsqueda de lecturas; menú |
| `i18n/es.po` y `donofrio_calidad.pot` | Traducción de los textos nuevos |
| `tests/test_frio.py` | 29 pruebas |

Menú: **Calidad › Cadena de frío › Lecturas de temperatura** (visible para quien tiene inventario o es inspector de calidad). El rango se edita en **Inventario › Configuración › Ubicaciones**, grupo «Cadena de frío» (solo ubicaciones internas).

## 5.5d.3 Modelos, campos y reglas

**`donofrio.temperatura`** (hereda `mail.thread` y `mail.activity.mixin`; orden: fecha descendente)

| Campo | Tipo | Detalle |
|---|---|---|
| `location_id` | Many2one `stock.location` | Obligatorio; solo ubicaciones internas; `ondelete='restrict'` |
| `temperatura` | Float | °C, obligatorio |
| `fecha` | Datetime | Obligatorio; por defecto, ahora |
| `user_id` | Many2one `res.users` | «Registrado por»; por defecto, el usuario actual |
| `observaciones` | Text | Opcional |
| `fuera_de_rango` | Boolean | **Calculado y almacenado**; depende solo de `location_id` y `temperatura` |
| `rango`, `temp_min`, `temp_max`, `control_temperatura` | Relacionados con la ubicación | Solo se muestran; no se guardan (`rango` dice «2 a 6 °C» o «Sin rango definido») |
| `company_id` | Many2one | Relacionado con la ubicación y almacenado |

**Campos nuevos de `stock.location`:** `control_temperatura` (Boolean), `temp_min` y `temp_max` (Float, °C). Restricción: con el control activo, el mínimo no puede ser mayor que el máximo (igual sí se permite). **Campo nuevo de `stock.lot`:** `alerta_vencimiento_fecha` (cuándo se avisó; solo lectura, no se copia).

Reglas que el código cumple y las pruebas verifican:

| Regla | Comportamiento |
|---|---|
| Dentro o fuera | Fuera de rango si `control_temperatura` y la lectura no está entre `temp_min` y `temp_max`, extremos incluidos. Una ubicación sin control nunca queda fuera de rango |
| Una actividad por lectura | La actividad (tipo «Por hacer») se crea al crear la lectura fuera de rango, o al **corregirla** de dentro a fuera. Editar una lectura ya alertada, o cuya actividad ya se atendió, **no** la repite; corregirla de fuera a dentro la desmarca |
| Historial | `fuera_de_rango` **no se reevalúa** si luego cambia el rango de la ubicación: la lectura se juzga con el rango que tenía al registrarla |
| Destinatario | El jefe de almacén de demostración (`donofrio_base.user_jefe_almacen`) si está activo; si no, los usuarios activos internos del grupo `stock.group_stock_manager`, **sin** OdooBot |
| Rangos de las cámaras | `_cargar_rangos_frio` pone el rango en las cuatro cámaras de `donofrio_base`: congelación (Lima y Arequipa) de −30 a −18 °C y refrigerados (Lima y Arequipa) de 2 a 6 °C (supuesto S5). Es idempotente y **no pisa** una ubicación que ya tiene el control activo; hace falta una función porque esas ubicaciones son `noupdate` y un `<record>` no se aplicaría al actualizar |
| Historial de cambios | `location_id`, `temperatura` y `fuera_de_rango` quedan en el chatter de la lectura |

## 5.5d.4 Cron de lotes por vencer

| Dato | Valor |
|---|---|
| Nombre | «Calidad: lotes por vencer» (`donofrio_calidad.ir_cron_lotes_por_vencer`) |
| Frecuencia | Una vez al día; corre como OdooBot (`base.user_root`) |
| Parámetro | `donofrio_calidad.dias_alerta_vencimiento` (Ajustes › Técnico › Parámetros del sistema), **7** por defecto; `noupdate`, así que una actualización no lo pisa. Si falta, no es un entero o es ≤ 0, se usan 7 |
| Qué busca | Lotes de **todas las compañías** con `expiration_date` entre ahora y ahora + N días, **con stock** (`product_qty > 0`) y sin `alerta_vencimiento_fecha` |
| Qué hace | Crea una actividad «Lote por vencer: *lote*» para el jefe de almacén (con la fecha de vencimiento como plazo y el producto, la fecha y la cantidad en el texto) y marca `alerta_vencimiento_fecha` |
| Qué no hace | No vuelve a avisar un lote ya alertado (aunque se atienda la actividad), ni avisa lotes sin stock, ya vencidos o más lejos que N días |

Odoo ya trae su propia alerta de lotes (`product_expiry`: «Fecha de alerta alcanzada», según el plazo de alerta de cada producto). **M3 no la reemplaza ni la desactiva:** son dos avisos distintos que pueden coincidir sobre el mismo lote (se ve en la última captura).

## 5.5d.5 Seguridad

| Grupo | Sobre `donofrio.temperatura` |
|---|---|
| Usuarios de inventario (`stock.group_stock_user`) | Leer, crear y modificar; **no** borrar |
| Jefe de almacén (`stock.group_stock_manager`) | Leer, crear, modificar y borrar |
| Usuario interno (`base.group_user`) | Solo leer |

No se creó un grupo nuevo: se usan los de Inventario. Las pruebas cubren que el operario de almacén registra y edita pero no borra (y su alerta llega al jefe), que el jefe borra y que un usuario interno solo lee (`AccessError` al crear, modificar o borrar).

## 5.5d.6 Diccionario de datos

La tabla nueva (`donofrio_temperatura`, 12 columnas) y las columnas que M3 agrega a otras tablas están en el [diccionario general](04_02_diccionario_datos.md), extraídas de una base limpia con el módulo instalado: Tabla 4.2.8-42, `stock_location` (+3 columnas: `control_temperatura`, `temp_min`, `temp_max`) y `stock_lot` (+1: `alerta_vencimiento_fecha`). El ER las muestra en el área «Cadena de frío (M3)» ([4.2.6](04_02_modelo_de_datos.md)).

```text
stock_location 1───* donofrio_temperatura *───1 res_users
(rango: control_temperatura, temp_min, temp_max)
```

## 5.5d.7 Pruebas y evidencia

`scripts/test.sh donofrio_calidad` (corrido con `docker run` sobre la misma imagen y red, porque desde un *worktree* el `docker compose` recrearía los contenedores): **45 pruebas, 0 fallos, 0 errores** (13 de inspecciones, 2 del punto de venta, 1 de idioma y las **29 de `tests/test_frio.py`**; el 24/11 eran 44 y la de inspección que se agregó después, con el PR #224, subió el total a 45). Las 29 de la cadena de frío:

| Clase | Pruebas | Qué cubren |
|---|---|---|
| `TestTemperatura` | 14 | Rangos de las cámaras de la base y que `_cargar_rangos_frio` no pisa lo editado a mano; dentro de rango (extremos incluidos) sin alerta; fuera de rango marcada y con actividad al jefe; ubicación sin rango; editar o atender sin duplicar; corregir de dentro a fuera (una actividad) y de fuera a dentro (se desmarca); cambiar el rango no reevalúa el historial; crear varias lecturas a la vez; sin el jefe de demostración avisa al grupo; el operario registra y la alerta llega al jefe; filtro de lecturas fuera de rango |
| `TestRangoUbicacion` | 3 | Mínimo mayor que máximo se rechaza; igual o sin control se permite; rango que incluye el cero |
| `TestSeguridadFrio` | 3 | Operario crea y edita pero no borra; jefe borra; usuario interno solo lee |
| `TestCronLotesPorVencer` | 9 | Parámetro por defecto (7); sin lotes por vencer no crea nada; una actividad por lote con stock; no repite aunque se atienda; ignora lotes sin stock, vencidos o fuera de la ventana; el parámetro cambia la ventana y uno inválido vuelve a 7; varios lotes, cada uno una vez; el cron existe, activo y diario |

Corrida del 24/11/2026 sobre una base nueva con el código de la rama: `44 post-tests`, `0 failed, 0 error(s) of 44 tests`, sin `ERROR`, `CRITICAL` ni `WARNING` en el registro. `scripts/check_legacy.sh`: «sin patrones legacy». **Actualización (`-u`):** se instaló M1 (código del commit anterior) sobre una base nueva con los datos de `donofrio_base` y se actualizó con el código de M3, sin `ERROR` ni `WARNING`; las cuatro cámaras quedaron con su rango y el cron y el parámetro (7) existen. No se probó sobre la base de desarrollo `donofrio`.

Capturas (base nueva con `donofrio_base`, `donofrio_calidad` y `donofrio_heladeros`, más datos ficticios cargados por script; usuario «Jefe de Almacén»; capturas rehechas el 25/11/2026 con los datos de demostración de la HU-16; PNG de 1600 × 900):

| Qué se verificó en la pantalla de Odoo | Captura |
|---|---|
| Lista de lecturas: una fuera de rango (7.3 °C en la cámara de insumos de 2 a 6 °C, el 21/11), en rojo y con la casilla marcada | [`HU-19_lista_lecturas.png`](../capturas/sprint-4/HU-19_lista_lecturas.png) |
| Lectura **dentro** de rango (3.9 °C): sin cinta y sin actividades | [`HU-19_lectura_dentro_de_rango.png`](../capturas/sprint-4/HU-19_lectura_dentro_de_rango.png) |
| Lectura **fuera** de rango: cinta «Fuera de rango» y la actividad «Temperatura fuera de rango» para el jefe de almacén | [`HU-19_lectura_fuera_de_rango.png`](../capturas/sprint-4/HU-19_lectura_fuera_de_rango.png) |
| Rango de temperatura en la ubicación (grupo «Cadena de frío»: 2.00 a 6.00 °C) | [`HU-19_rango_en_ubicacion.png`](../capturas/sprint-4/HU-19_rango_en_ubicacion.png) |
| Actividad del cron en un lote que vence en 4 días (INI-P02-A, vence el 29/11), junto a la alerta estándar de Odoo | [`HU-19_cron_lote_por_vencer.png`](../capturas/sprint-4/HU-19_cron_lote_por_vencer.png) |

## 5.5d.8 Límites

- **Las lecturas se registran a mano.** No hay sensores ni importación; el valor y la hora los escribe una persona (la fecha por defecto es ahora, pero se puede cambiar).
- **La alerta no actúa sobre los lotes:** no los lista, no los bloquea ni los pone en cuarentena. Pide al jefe de almacén que los revise y decida (CU006, A1).
- **Un solo destinatario.** Con el jefe de almacén de demostración activo, nadie más recibe la actividad; sin él, la reciben todos los jefes de almacén activos.
- **No avisa lecturas que faltan:** si nadie registra la temperatura de una cámara, el sistema no genera alerta.
- **Cambiar el rango no reevalúa lecturas anteriores** (decisión de diseño, probada). Una ubicación sin «Controlar temperatura» nunca queda fuera de rango.
- **Solo las cuatro cámaras de `donofrio_base` traen rango.** El de congelación es de −30 a −18 °C aunque su nombre diga −25 °C (supuesto S5: se exige −18 °C o menos en el producto); los demás almacenes no tienen rango hasta que alguien lo configure.
- **El cron avisa una sola vez por lote.** Si después se acerca más la fecha de vencimiento o se amplía el parámetro, no se vuelve a avisar un lote ya alertado; los vencidos y los sin stock no se avisan.
- **Dos avisos por el mismo lote:** la alerta estándar de `product_expiry` («Fecha de alerta alcanzada») y la de M3 («Lote por vencer») pueden coincidir. No se unificaron.
- **El cron se ejecutó a mano en la verificación** (`method_direct_trigger`, equivalente a «Ejecutar manualmente»): no se esperó a su disparo diario. Su definición (diario, activo) la comprueba una prueba.
- **Las capturas salen de una base de pruebas, no de `donofrio`**, con lecturas y lotes ficticios; la lectura fuera de rango la creó un script, no el formulario, y todas figuran a nombre del jefe de almacén (que también recibe la alerta). El caso del operario de almacén solo se verificó con pruebas automáticas.
- **No hay reglas de registro por compañía ni por almacén** para las lecturas: quien tiene el grupo ve todas.
