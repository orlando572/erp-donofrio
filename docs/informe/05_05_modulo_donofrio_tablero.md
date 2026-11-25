# 5.5e Documentación del módulo `donofrio_tablero` (M4)

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn (dueña del módulo) · **Revisa:** Orlando · **Fuente:** `addons/donofrio_tablero/` (HU-22 y HU-24, con las dos correcciones del 24/11), una instancia local con datos de demostración y las capturas y mediciones de [`docs/capturas/sprint-4/`](../capturas/sprint-4/) ([la verificación de M4](../capturas/sprint-4/S4_evidencia_verificacion_m4.txt))
>
> Complementa 5.5 (`donofrio_base`), 5.5b (M1), 5.5c (M2) y 5.5d (M3). **M4 no crea tablas:** su servicio de datos es un modelo abstracto, así que el ER general (42 tablas) y el diccionario de datos no cambian.

## 5.5e.1 Qué hace

Gerencia ya tenía en la Fase 1 los dashboards estándar de Community (solo lectura, sin tarjetas propias). M4 (HU-22 y HU-24; RF013; CU009) agrega:

1. **Tablero gerencial** (Tablero › Gerencia): una acción de cliente OWL con **hasta seis tarjetas de KPI**, un **gráfico de ventas de los últimos seis meses** (Chart.js, que ya trae Odoo), una tabla de ventas del mes por canal y un **filtro por almacén**.
2. **Marca visual:** barra superior del backend en el amarillo de la marca, color primario de botones y enlaces en amarillo oscuro, el mismo color en la pantalla de inicio de sesión y las ilustraciones de «sin datos», y el favicon del helado.

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
| `models/tablero.py` | Modelo abstracto `donofrio.tablero` con `get_kpis()`; usa `_read_group`, respeta los permisos de quien lo abre (sin `sudo`) y, si no puede leer los datos base, devuelve `sin_permiso` con un mensaje en vez de un error |
| `static/src/tablero/tablero.js`, `.xml`, `.scss` | Componente OWL registrado como acción de cliente `donofrio_tablero.tablero`; gráfico con Chart.js |
| `views/tablero_views.xml` | Acción de cliente y menú «Tablero › Gerencia» (grupos de ventas con todos los leads y de gerencia de ventas) |
| `static/src/scss/primary_variables.scss` | Variables de la marca (HU-24): backend (`$o-brand-primary`, barra) y paleta `base-1` del editor para las páginas públicas |
| `static/src/scss/sin_datos.scss`, `static/img/smiling_face.svg`, `neutral_face.svg` | Ilustraciones de «sin datos» con el degradado de la marca (HU-24) |
| `views/layout_templates.xml`, `static/img/favicon.png` | Favicon en `web.layout` (HU-24); el icono sale del logo de `donofrio_base` |
| `tests/test_tablero.py` | 21 pruebas |

## 5.5e.4 Marca (HU-24)

| Elemento | Valor | Por qué |
|---|---|---|
| Barra superior | Fondo `#F7C60A`, texto `#2B2B2B` | El amarillo solo como fondo, con texto oscuro (contraste 8.79, [4.6](04_06_prototipos_web_y_reportes.md)) |
| Color primario (`$o-brand-primary`) | `#9A6B00` | Amarillo oscuro: con texto blanco da contraste 4.69 |
| Favicon | `/donofrio_tablero/static/img/favicon.png` (64 × 64, recortado del logo) | Reemplaza el de Odoo en `web.layout` |

Las variables van antes de las de Odoo (que usan `!default`).

**Inicio de sesión y «sin datos» (corrección del 24/11).** El frontend de Odoo no usa `$o-brand-primary`: su color primario sale de la paleta `base-1` del editor (`o-color-1`). `primary_variables.scss` la redefine con `#9A6B00` (solo cambia `o-color-1`) y el archivo entra al frontend porque `web._assets_primary_variables` también forma parte de `web.assets_frontend`. Las caritas de «sin datos» son SVG con degradado morado: se incluyen copias con el degradado de la marca y `sin_datos.scss` las apunta. Resultado: el botón «Iniciar sesión» y los enlaces del login son marrón `#9A6B00` ([`HU-24_login_marca.png`](../capturas/sprint-4/HU-24_login_marca.png); antes, [`HU-24_limite_login_morado.jpg`](../capturas/sprint-4/HU-24_limite_login_morado.jpg)) y la ilustración de «sin datos» sale marrón ([`HU-24_marca_sin_datos_fabricacion.png`](../capturas/sprint-4/HU-24_marca_sin_datos_fabricacion.png)).

**Revisión en pantalla (24/11/2026, Gerente General, instancia local de esta rama):** se recorrieron Ventas (lista y formulario de un pedido; al Gerente le sale dentro de «CRM › Ventas»), Inventario (entregas), Fabricación (órdenes), el tablero y el inicio de sesión. En todas, la barra superior es amarilla con texto oscuro legible, los botones primarios y los enlaces son marrón con texto blanco, y no hay texto ilegible. Capturas PNG (1600 × 900): [`HU-24_marca_barra_superior`](../capturas/sprint-4/HU-24_marca_barra_superior.png), [`_ventas_lista`](../capturas/sprint-4/HU-24_marca_ventas_lista.png), [`_ventas_formulario`](../capturas/sprint-4/HU-24_marca_ventas_formulario.png), [`_fabricacion`](../capturas/sprint-4/HU-24_marca_fabricacion.png) y [`_traslados`](../capturas/sprint-4/HU-24_marca_traslados.png). **No se revisaron** los informes PDF (usan el color de la compañía, `#C77D00`, de `donofrio_base`), el punto de venta ni el resto de aplicaciones de Odoo.

## 5.5e.5 Permisos

El tablero **no tiene ACL propios**: es un modelo abstracto sin tabla y lee con los permisos de quien lo abre. El menú se muestra a quien tiene el grupo de ventas con todos los leads o el de gerencia de ventas (el Gerente General de prueba entra por el primero). Las tarjetas de los módulos opcionales se ocultan cuando el usuario no puede leer su modelo.

**Sin permiso (corrección del 24/11).** Si el usuario no puede leer pedidos de venta, almacenes, existencias, lotes u órdenes de fabricación, `get_kpis` devuelve `sin_permiso`, las áreas que faltan y un mensaje en español, y el componente lo muestra como una alerta amarilla en vez del «Error de acceso» de Odoo. Con los usuarios de prueba (instancia local, 24/11): el **Gerente General** ve el tablero completo; el **Jefe de Ventas** ve el menú y, al abrirlo, el aviso «falta acceso a Inventario» (no lee lotes ni existencias), y el **Vendedor**, que no tiene el menú, recibe el mismo aviso si abre la acción por su dirección; el Jefe de Almacén, el Jefe de Producción, el Inspector y el Liquidador pueden leer todo, pero no tienen el menú. Captura: [`HU-22_tablero_sin_permiso_vendedor.png`](../capturas/sprint-4/HU-22_tablero_sin_permiso_vendedor.png).

## 5.5e.6 Pruebas y evidencia

`scripts/test.sh donofrio_tablero`: **21 pruebas, sin errores** (24/11/2026, rama con las dos correcciones). `scripts/test.sh donofrio_calidad donofrio_heladeros donofrio_tablero`: **81 pruebas, sin errores** (79 el 24/11; una prueba más en `donofrio_calidad` y otra en `donofrio_heladeros`, agregadas después, suman 81) (también pasan las 21 con M4 solo, donde las tarjetas opcionales no están y sus pruebas se omiten). `scripts/check_legacy.sh`: sin patrones legacy. Las pruebas cubren la estructura, las ventas contra un pedido real y el filtro de almacén, las producciones, el stock por vencer y vencido, las tres tarjetas opcionales (con y sin su módulo), el permiso de lectura (4 pruebas del aviso de «sin permiso» y del menú) y que `get_kpis` tarde menos de 3 s.

| Qué se verificó en la pantalla (instancia local de esta rama, Gerente General, 24/11/2026) | Evidencia |
|---|---|
| Tablero con las seis tarjetas, el gráfico de seis meses, la tabla por canal y la barra amarilla | [`HU-22_tablero_todos_los_almacenes.png`](../capturas/sprint-4/HU-22_tablero_todos_los_almacenes.png) |
| Filtro «Almacén: WH-AQP CD Arequipa»: las tarjetas y el gráfico cambian | [`HU-22_tablero_filtro_arequipa.png`](../capturas/sprint-4/HU-22_tablero_filtro_arequipa.png) |
| Vendedor sin acceso a Inventario: aviso en vez de error | [`HU-22_tablero_sin_permiso_vendedor.png`](../capturas/sprint-4/HU-22_tablero_sin_permiso_vendedor.png) |
| Tablero en una ventana de 375 × 812 | [`S4_movil_tablero.png`](../capturas/sprint-4/S4_movil_tablero.png), [`S4_movil_tablero_abajo.png`](../capturas/sprint-4/S4_movil_tablero_abajo.png), [`S4_movil_login.png`](../capturas/sprint-4/S4_movil_login.png) |
| Lighthouse del tablero y del login | [los resultados de Lighthouse de M4](../capturas/sprint-4/S4_lighthouse_m4_resultados.csv), [la verificación de M4](../capturas/sprint-4/S4_evidencia_verificacion_m4.txt) |
| Tiempos de `get_kpis`, cifras de control y favicon (base del 24/11 por la mañana) | [la evidencia del tablero](../capturas/sprint-4/HU-22_evidencia_tablero.txt) |

Cifras de control: en la instancia local nueva (las capturas HU-22 del 25/11 muestran S/ 2,844,413.33, S/ 2,525,068.21 de Lima y S/ 319,345.12 de Arequipa), las ventas de noviembre del tablero (S/ 2,844,413.33) coinciden con la suma de los pedidos confirmados en la base (consulta SQL), y Lima (S/ 2,525,068.21) más Arequipa (S/ 319,345.12) dan el total. La medición anterior, sobre la base `donofrio` del equipo, dio S/ 2,844,525.83 (Arequipa igual): la diferencia de S/ 112.50 está en Lima, no se investigó y proviene de que la base nueva se cargó de nuevo. En esa base `get_kpis` tardó entre 30 y 57 ms y la página 177 ms (meta de RNF008: menos de 3 s).

Las capturas son PNG de 1600 × 900 (la ventana angosta, 750 × 1624) tomadas con Chromium sin interfaz, porque el navegador integrado de la app no guarda las imágenes; las de la primera entrega eran JPG reducidos y se rehicieron en PNG el 25/11/2026 con los datos de demostración de la HU-16 (M1, M2, M3 y las dos del tablero con las tarjetas llenas). Quedan dos JPG de la primera entrega que no se pueden reproducir sin crear datos o sin la versión anterior de la pantalla: `HU-20_error_devuelto_mas_merma.jpg` y `HU-24_limite_login_morado.jpg`.

### 5.5e.6.1 Vista en una ventana angosta

Con un ancho de 375 px (en Chromium a factor 2 y en el navegador integrado con el preset móvil): **no hay desplazamiento horizontal**; las seis tarjetas pasan a una columna con 16 px de margen, el selector de almacén cabe junto a su etiqueta, el gráfico de seis meses se lee completo (309 px de ancho) y la tabla por canal cabe. **Lo que queda así:** la barra superior solo muestra el menú de hamburguesa (no el nombre de la aplicación, que es el diseño móvil de Odoo); el tablero mide unas dos pantallas y media, de modo que el gráfico queda abajo.

### 5.5e.6.2 Lighthouse (RNF008)

Lighthouse 12.2.1, solo *Performance*, mediana de 3 corridas, con el método de la HU-28 ([4.6.4](04_06_wpo.md)): «antes» es el desarrollo con `?debug=assets` y «después» el despliegue protegido (Nginx con TLS y gzip, 2 *workers*). Meta de RNF008: puntaje ≥ 80 y tablero en menos de 3 s.

| Página y perfil | Antes: puntaje | Después: puntaje | Después: LCP (s) | Después: TBT (ms) | Cumple ≥ 80 |
|---|---|---|---|---|---|
| Login, escritorio | 98 | **100** | 0.38 | 14 | Sí |
| Login, móvil (4G lenta, CPU 4× más lenta) | — | **95** | 1.68 | 238 | Sí |
| **Tablero, escritorio** | 50 | **76** | 2.11 | 92 | **No** (por 4 puntos) |
| Tablero, móvil (4G lenta, CPU 4× más lenta) | — | **39** | 12.16 | 680 | No |

- **El tablero no llega a 80:** las tres corridas dieron 76, 76 y 81; una sola pasó el umbral, así que no es estable. Sí cumple la parte de la **carga en menos de 3 s** (LCP de 2.11 s). El puntaje lo frena el *Speed Index* (2.97 s); no se hizo un análisis más fino.
- **El móvil queda en 39:** el perfil móvil de Lighthouse emula un CPU 4 veces más lento y el JavaScript del cliente web de Odoo bloquea el hilo 680 ms. RNF008 se definió para escritorio; se declara como **límite conocido** (lo explica el JavaScript de Odoo, igual que el 59 del backend), no se corrigió.
- **Con otro usuario en «después»:** el Gerente General (el único con el menú y todos los datos) pide 2FA en el despliegue protegido y un script no lo puede dar; el Jefe de Ventas ve el menú, pero recibe el aviso de «sin permiso». El tablero «después» se midió con el Jefe de Almacén, que no tiene 2FA y lee todos los datos (abre la acción por su dirección). «Antes» se midió con el Gerente. No se debilitó ningún control de seguridad. Una primera tanda midió por error la pantalla de login con el Gerente (la sesión no pasó el 2FA); se descartó y el script ahora se detiene si la página termina en el login.
- **Comparación con la HU-28:** ahí el backend dio 59 y el dashboard de Ventas 80; esta medición corrió en otra PC (Linux, `--network host`) y no es directamente comparable. El script de esta medición es [`S4_lighthouse_m4.py`](../capturas/sprint-4/S4_lighthouse_m4.py).

## 5.5e.7 Un fallo que apareció en la prueba de pantalla

La primera vez, el tablero se abrió con el Inspector de Calidad y falló con «Error de acceso» por las liquidaciones. No era un error del Gerente (se había entrado con otro usuario por un clic en la lista de cuentas), pero mostró que una tarjeta de un módulo opcional podía romper todo el tablero. Se corrigió: una tarjeta opcional solo sale si el usuario puede leer su modelo (`has_access('read')`), con una prueba.

## 5.5e.7b Otros hallazgos del 24/11 (corregidos antes de esta verificación)

- **El Jefe de Ventas veía el menú y el tablero fallaba con «Error de acceso»** (y lo mismo al Vendedor si abría la dirección), porque no leen lotes ni existencias; ahora reciben el aviso de «sin permiso» (5.5e.5).
- **El inicio de sesión y las ilustraciones de «sin datos» seguían en morado**; ahora usan la marca (5.5e.4).

## 5.5e.8 Límites

- **Lighthouse del tablero: 76 en escritorio (meta 80, no cumple; límite conocido) y 39 en móvil** (5.5e.6.2); el LCP de 2.11 s sí cumple los 3 s. Se midió en una PC de desarrollo con Docker, no en el servidor definitivo, y el tablero «después» con el Jefe de Almacén (el Gerente pide 2FA).
- **La vista angosta se revisó en Chromium y en el navegador integrado con el tamaño de una ventana de 375 × 812** (5.5e.6.1).
- **No hay pruebas de JavaScript** (por ejemplo de Hoot): el componente OWL se verificó a mano en la pantalla (tarjetas, gráfico y cambio de almacén).
- **Cumplimiento de producción:** cuenta las OP del mes que ya empezaron (no las que siguen en borrador); no es un plan contra lo ejecutado.
- **El filtro de almacén no aplica a las liquidaciones pendientes** (la liquidación no tiene almacén); las demás tarjetas sí. En Lotes aprobados el almacén es el de la orden de producción.
- **Valor del stock por vencer:** cantidad × costo estándar del producto; no usa la valoración FIFO de contabilidad.
- **Los títulos del gráfico y los meses** están en español en el código (sin traducciones `.po`).
- **Marca:** el color nuevo se aplica al backend (barra, botones y enlaces), al inicio de sesión y a las ilustraciones de «sin datos»; se revisaron 4 aplicaciones del backend y el login, no todas (ver 5.5e.4). En la pestaña de pruebas el icono lo reemplaza la extensión del navegador, así que el favicon se verificó en el HTML de la página y en la respuesta del archivo. Otras páginas públicas (portal, restablecer contraseña) no se revisaron.
- **Un usuario sin permiso** recibe un aviso en lugar de un tablero reducido: no hay una versión parcial del tablero por áreas.
- **Datos de prueba:** las cifras de las capturas salen de una instancia local con las transacciones de demostración (supuesto S2); las inspecciones (11 aprobadas y 1 rechazada), la liquidación sin liquidar y las dos lecturas de temperatura se agregaron a mano solo para ver las tarjetas, y no están en el repositorio.
