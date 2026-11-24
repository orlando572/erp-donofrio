# 5.5e Documentación del módulo `donofrio_tablero` (M4)

> **Estado:** borrador del Sprint 4 · **Autora:** Evelyn (dueña del módulo) · **Revisa:** Orlando · **Fuente:** `addons/donofrio_tablero/` en la rama de M4 (HU-22 y HU-24), la base de desarrollo `donofrio` y las capturas de [`docs/capturas/sprint-4/`](../capturas/sprint-4/)
>
> Complementa 5.5 (`donofrio_base`), 5.5b (M1), 5.5c (M2) y 5.5d (M3). **M4 no crea tablas:** su servicio de datos es un modelo abstracto, así que el ER general (42 tablas) y el diccionario de datos no cambian.

## 5.5e.1 Qué hace

Gerencia ya tenía en la Fase 1 los dashboards estándar de Community (solo lectura, sin tarjetas propias). M4 (HU-22 y HU-24; RF013; CU009) agrega:

1. **Tablero gerencial** (Tablero › Gerencia): una acción de cliente OWL con **hasta seis tarjetas de KPI**, un **gráfico de ventas de los últimos seis meses** (Chart.js, que ya trae Odoo), una tabla de ventas del mes por canal y un **filtro por almacén**.
2. **Marca visual del backend:** barra superior en el amarillo de la marca, color primario de botones y enlaces en amarillo oscuro, y el favicon del helado.

## 5.5e.2 Las tarjetas

| Tarjeta | Qué cuenta | Sale si… |
|---|---|---|
| Ventas del mes | Pedidos confirmados o hechos del mes calendario (`amount_total`, con IGV), la variación contra el mes anterior y el desglose por canal (equipo de ventas) | Siempre |
| Cumplimiento de producción | OP del mes (por fecha de inicio) hechas entre las confirmadas, en curso, por cerrar y hechas | Siempre |
| Stock por vencer (30 d) | Lotes con existencias en ubicaciones internas cuyo vencimiento cae entre hoy y 30 días; valor = cantidad × costo estándar; además cuenta los lotes ya vencidos | Siempre |
| Lotes aprobados (M1) | Inspecciones terminadas: aprobadas entre aprobadas y rechazadas | `donofrio_calidad` instalado y el usuario puede leer las inspecciones |
| Liquidaciones pendientes (M2) | Liquidaciones de heladeros que no están en «Liquidado» | `donofrio_heladeros` instalado y el usuario puede leer las liquidaciones |
| Alertas de temperatura (M3) | Lecturas fuera de rango de los últimos 7 días | `donofrio_calidad` con la cadena de frío y el usuario puede leer las lecturas |

El gráfico y la tabla por canal siguen el mismo filtro. Los datos salen de `donofrio.tablero.get_kpis(warehouse_id)`.

## 5.5e.3 Archivos

| Ruta (`addons/donofrio_tablero/`) | Contenido |
|---|---|
| `__manifest__.py` | Depende de `donofrio_base`, `web`, `sale`, `stock`, `mrp` y `product_expiry`; **no** depende de calidad ni de heladeros (por eso sus tarjetas son opcionales) |
| `models/tablero.py` | Modelo abstracto `donofrio.tablero` con `get_kpis()`; usa `_read_group`, respeta los permisos de quien lo abre (sin `sudo`) |
| `static/src/tablero/tablero.js`, `.xml`, `.scss` | Componente OWL registrado como acción de cliente `donofrio_tablero.tablero`; gráfico con Chart.js |
| `views/tablero_views.xml` | Acción de cliente y menú «Tablero › Gerencia» (grupos de ventas con todos los leads y de gerencia de ventas) |
| `static/src/scss/primary_variables.scss` | Variables de la marca (HU-24) |
| `views/layout_templates.xml`, `static/img/favicon.png` | Favicon en `web.layout` (HU-24); el icono sale del logo de `donofrio_base` |
| `tests/test_tablero.py` | 17 pruebas |

## 5.5e.4 Marca (HU-24)

| Elemento | Valor | Por qué |
|---|---|---|
| Barra superior | Fondo `#F7C60A`, texto `#2B2B2B` | El amarillo solo como fondo, con texto oscuro (contraste 8.79, [4.6](04_06_prototipos_web_y_reportes.md)) |
| Color primario (`$o-brand-primary`) | `#9A6B00` | Amarillo oscuro: con texto blanco da contraste 4.69 |
| Favicon | `/donofrio_tablero/static/img/favicon.png` (64 × 64, recortado del logo) | Reemplaza el de Odoo en `web.layout` |

Las variables van antes de las de Odoo (que usan `!default`).

## 5.5e.5 Permisos

El tablero **no tiene ACL propios**: es un modelo abstracto sin tabla y lee con los permisos de quien lo abre. El menú se muestra a quien tiene el grupo de ventas con todos los leads o el de gerencia de ventas (el Gerente General de prueba entra por el primero). Si un usuario sin permiso de ventas abre la acción por su dirección, Odoo le da «Error de acceso» por los pedidos de venta (se vio con el Inspector de Calidad). Las tarjetas de los módulos opcionales se ocultan cuando el usuario no puede leer su modelo.

## 5.5e.6 Pruebas y evidencia

`scripts/test.sh donofrio_calidad donofrio_heladeros donofrio_tablero`: **75 pruebas, sin errores** (17 de M4; también pasan las 17 con M4 solo, donde las tarjetas opcionales no están y las pruebas de esas tarjetas se omiten). Cubren la estructura, las ventas contra un pedido real y el filtro de almacén, las producciones, el stock por vencer y vencido, las tres tarjetas opcionales (con y sin su módulo), el permiso de lectura y que `get_kpis` tarde menos de 3 s.

| Qué se verificó en la pantalla (base `donofrio`, usuario Gerente General, 24/11/2026) | Evidencia |
|---|---|
| Tablero con las seis tarjetas, el gráfico de seis meses, la tabla por canal y la barra amarilla | [`HU-22_tablero_todos_los_almacenes.jpg`](../capturas/sprint-4/HU-22_tablero_todos_los_almacenes.jpg) |
| Filtro «Almacén: WH-AQP CD Arequipa»: las tarjetas y el gráfico cambian | [`HU-22_tablero_filtro_arequipa.jpg`](../capturas/sprint-4/HU-22_tablero_filtro_arequipa.jpg) |
| Tiempos, cifras de control y favicon | [`HU-22_evidencia_tablero.txt`](../capturas/sprint-4/HU-22_evidencia_tablero.txt) |

Cifras de control: las ventas de noviembre del tablero (S/ 2,844,525.83) coinciden con la suma de los pedidos confirmados en la base, y Lima (S/ 2,525,180.71) más Arequipa (S/ 319,345.12) dan el total. `get_kpis` tardó entre 30 y 57 ms y la página 177 ms (meta de RNF008: menos de 3 s).

## 5.5e.7 Un fallo que apareció en la prueba de pantalla

La primera vez, el tablero se abrió con el Inspector de Calidad y falló con «Error de acceso» por las liquidaciones. No era un error del Gerente (se había entrado con otro usuario por un clic en la lista de cuentas), pero mostró que una tarjeta de un módulo opcional podía romper todo el tablero. Se corrigió: una tarjeta opcional solo sale si el usuario puede leer su modelo (`has_access('read')`), con una prueba.

## 5.5e.8 Límites

- **El tablero no se midió con Lighthouse** ni en un celular: se midió la consulta y la carga de la página en una PC de desarrollo. Los 177 ms no sustituyen una prueba en el servidor definitivo.
- **No hay pruebas de JavaScript** (por ejemplo de Hoot): el componente OWL se verificó a mano en la pantalla (tarjetas, gráfico y cambio de almacén).
- **Cumplimiento de producción:** cuenta las OP del mes que ya empezaron (no las que siguen en borrador); no es un plan contra lo ejecutado.
- **El filtro de almacén no aplica a las liquidaciones pendientes** (la liquidación no tiene almacén); las demás tarjetas sí. En Lotes aprobados el almacén es el de la orden de producción.
- **Valor del stock por vencer:** cantidad × costo estándar del producto; no usa la valoración FIFO de contabilidad.
- **Los títulos del gráfico y los meses** están en español en el código (sin traducciones `.po`).
- **Marca:** se verificó la barra superior y los botones (por ejemplo el del diálogo); no se revisaron todas las pantallas de Odoo con el nuevo color. En la pestaña de pruebas el icono lo reemplaza la extensión del navegador, así que el favicon se verificó en el HTML de la página y en la respuesta del archivo.
- **Un usuario sin permiso de ventas** que abra la acción por su dirección recibe un error de acceso, no un tablero reducido.
- **Datos de prueba:** las cifras de las capturas salen de la base de desarrollo, con las transacciones de demostración (supuesto S2) y las inspecciones que se crearon a mano para M1.
