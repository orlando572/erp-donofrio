# Pruebas no funcionales: carga (k6) y seguridad (ZAP) — HU-28

Cubren **RNF002** (rendimiento: p95 < 2 s en listas y formularios con 20 usuarios concurrentes) y **RNF009** (seguridad: HTTPS, cabeceras, gestor de BD oculto, cookies; los roles y el 2FA los cubren los tests de acceso de `donofrio_base`, `test_seguridad.py` y `test_hardening.py`). Normas: ISO 27001 A.8.29 y OWASP Top 10 A05 (mala configuración) y A07 (autenticación). El Lighthouse antes/después (RNF008) es de otra tarea de la misma HU.

Las dos pruebas corren **contra el despliegue protegido** (Nginx con TLS en `https://localhost:8443`, Odoo con `workers = 2` y `proxy_mode`), no contra el modo desarrollo (`workers = 0`, que no sirve para medir). Cada herramienta usa su imagen de Docker con versión fija: no se instala nada en el equipo.

## Cómo correrlas

```bash
# 1. Base con datos de demostración y despliegue protegido (ver el manual de instalación, §4.4, §4.5 y §6.2)
scripts/init_db.sh                      # donofrio_base
docker compose run --rm -T odoo odoo shell -d donofrio --no-http < scripts/cargar_transacciones.py
scripts/levantar_prod.sh                # en .env: ODOO_ADMIN_PASSWD de 16+ caracteres

# 2. Carga con k6 (20 usuarios virtuales, 3 minutos con todos activos)
scripts/perf/k6.sh

# 3. Seguridad con ZAP baseline
scripts/perf/zap.sh
```

Los reportes quedan en `scripts/perf/resultados/` (carpeta ignorada por git; se cambia con `SALIDA=`). Si falta algún umbral, k6 termina con código distinto de 0; ZAP termina con 1 si hay una alerta de riesgo **alto**. Para volver a desarrollo al terminar: `docker compose --profile proxy rm -sf nginx && docker compose up -d odoo`.

Dónde está cada cosa: `scripts/perf/carga.js` (escenario y umbrales de k6), `scripts/perf/k6.sh` (lanza k6 y mide `docker stats` cada 10 s), `scripts/perf/zap.sh` y `scripts/perf/zap-reglas.conf` (alertas aceptadas con su motivo). También hay un flujo manual en GitHub (Actions → «Pruebas no funcionales», `perf.yml`, solo `workflow_dispatch`) que arma todo en un runner y sube los reportes como artefactos; **no** es un check requerido del PR porque tarda.

## k6 (RNF002)

**Escenario.** 20 usuarios virtuales (subida de 20 s, 3 min con los 20 activos, bajada de 10 s). Cada uno inicia sesión **una sola vez** (`/web/session/authenticate`) con un usuario sin 2FA, repartidos por turno entre vendedor, jefe de ventas y jefe de almacén (el administrador y el gerente piden segundo factor en este modo). Las contraseñas salen de `DONOFRIO_USER_PASSWORD` del `.env` y no se escriben en el código ni en los reportes. Nunca se hacen intentos fallidos, para no activar el bloqueo de login de Odoo. Después, en bucle y con pausas de 1 a 3 s entre pantallas (lo que tarda una persona en leer), cada usuario:

| Paso | Llamada (JSON-RPC de Odoo 19, como el cliente web) | Etiqueta |
|---|---|---|
| Abrir la aplicación | `GET /odoo` y `GET /web/webclient/load_menus` | `app` |
| Listas (80 filas) | `web_search_read` de pedidos de venta, clientes, productos, facturas (jefe de ventas) o transferencias, lotes, órdenes de producción (jefe de almacén) | `lista` |
| Abrir un formulario | `web_read` de un pedido de venta (con sus líneas) o de una transferencia (con sus movimientos) elegidos al azar | `formulario` |
| Tablero | `web_read_group` de `sale.report` por mes (ventas) o de `stock.lot` por vencimiento (almacén) | `tablero` |

**Umbrales** (si no se cumplen, k6 falla): `http_req_failed < 1 %`, errores de JSON-RPC (un `200` con `error`, p. ej. `AccessError`, que `http_req_failed` no ve) `< 1 %`, `checks > 99 %`, y `p(95) < 2000 ms` en `lista`, `formulario` (RNF002), `tablero`, `app` y `login`.

**Con qué datos se midió.** Base `donofrio_perf` = `donofrio_base` + `scripts/cargar_transacciones.py` completo (16 semanas): 437 pedidos de venta (1 454 líneas), 939 pedidos del PdV, 1 647 transferencias, 6 063 movimientos de stock, 488 lotes, 3 369 asientos y facturas, 188 órdenes de producción, 101 órdenes de compra, 63 contactos, 48 productos; 143 MB. Equipo: 12 CPU lógicas y 14 GB de RAM; k6, Nginx, Odoo y PostgreSQL corren en la **misma** PC, sin límites de recursos y sin latencia de red.

### Resultados (corrida del 23/11/2026)

| | Prueba normal (pausas de 1 a 3 s) | Prueba de esfuerzo (`PAUSA=0`, 1 min) |
|---|---|---|
| Usuarios virtuales | 20 | 20 |
| Iteraciones / peticiones | 332 / 2 765 (12.5 por s) | 2 516 / 20 888 (232 por s) |
| `http_req_failed` | 0 de 2 765 (0 %) | 1 de 20 888 (0.005 %) |
| Errores de JSON-RPC | 0 de 2 101 | 0 de 15 856 |
| Umbrales | todos se cumplen | todos se cumplen |

| Tipo | Normal p50 | Normal p95 | Normal p99 | Esfuerzo p50 | Esfuerzo p95 | Esfuerzo p99 |
|---|---|---|---|---|---|---|
| Listas | 7.8 ms | **11.6 ms** | 13.3 ms | 71 ms | **98.7 ms** | 121 ms |
| Formularios | 7.5 ms | **9.1 ms** | 11.4 ms | 72 ms | **100 ms** | 121 ms |
| Tablero | 9.3 ms | 13.0 ms | 14.1 ms | 73 ms | 101 ms | 119 ms |
| App (`/odoo` y menús) | 10.1 ms | 17.8 ms | 21.0 ms | 73 ms | 103 ms | 125 ms |
| Inicio de sesión | 330 ms | 342 ms | 345 ms | 356 ms | 566 ms | 2.89 s |

**RNF002 se cumple con mucho margen**: p95 de 12 ms en listas y de 9 ms en formularios frente al límite de 2 s. Incluso sin pausas (un ritmo unas 20 veces mayor que el de una persona) el p95 es de unos 100 ms.

CPU y memoria (`docker stats`, máximo de las muestras): en la prueba normal Odoo llegó a 39 % de una CPU y 440 MiB, PostgreSQL a 9 % y 195 MiB, Nginx a menos de 1 % y 19 MiB. En la de esfuerzo Odoo llegó a 160 % (los dos workers casi saturados) y 513 MiB, PostgreSQL a 57 % y 201 MiB y Nginx a 67 % y 24 MiB. El inicio de sesión cuesta unos 330 ms por el hash de la contraseña (PBKDF2).

**Limitaciones y lo que no se sabe.**
- En la prueba de esfuerzo falló **una** petición (`load_menus`, tardó 30 s) de 20 888; no se investigó la causa y no apareció en la prueba normal. Está dentro del umbral (< 1 %) pero se informa tal cual.
- Los datos son los de demostración (437 pedidos): con años de datos las listas y los tableros tardarán más. Las listas se leen de a 80 filas, como el cliente web.
- k6 y el servidor comparten la PC y no hay red de por medio: es una medida del servidor, no de lo que verá un usuario en Arequipa. La percepción en el navegador (LCP, CLS) la mide Lighthouse.
- Solo hay lecturas (listas, formularios, tableros). No se miden escrituras concurrentes (confirmar pedidos, entregas) ni el PdV.
- El administrador y el gerente (2FA) no se pueden probar con un script sin su segundo factor.

## ZAP baseline (RNF009)

`zap-baseline.py` (ZAP 2.17.0) hace una araña de hasta 5 minutos sobre `https://localhost:8443/web/login` y aplica las reglas **pasivas** sobre lo que ve; no ataca. Corre **sin sesión**: ve la pantalla de acceso, las páginas públicas y los assets, no el backend (Odoo es una aplicación de una sola página y la araña tradicional ve poco de ella). El backend autenticado se cubre con los tests de acceso por rol de `donofrio_base`, y k6 comprueba que los tres roles de la prueba pueden leer sus pantallas por HTTPS. Pasó con **0 alertas de riesgo alto**.

| Corrida | Alto | Medio | Bajo | Informativo |
|---|---|---|---|---|
| 1.ª: Nginx de HU-27, sin reglas aceptadas | 0 | 6 | 7 | 8 |
| Final: Nginx corregido + `zap-reglas.conf` | **0** | 4 (aceptadas) | 3 (aceptadas) | 8 (aceptadas) |

Con la corrida final ZAP informa `FAIL 0 · WARN 0 · IGNORE 10 · PASS 58`: lo que sigue listado en el reporte (`HU-28_zap_reporte.html` y `.json` en `docs/capturas/sprint-3/`) es lo aceptado en `scripts/perf/zap-reglas.conf`; una alerta nueva saldría como aviso.

### Corregido en `docker/nginx/` (malas configuraciones reales)

| Alerta de ZAP | Cambio |
|---|---|
| CSP no definida; CSP sin `base-uri` ni `form-action`; CSP con comodines (Medio) | `Content-Security-Policy` propia en `seguridad.conf`: `default-src 'self'`, `object-src`, `base-uri`, `form-action` y `frame-ancestors` cerrados al propio origen, imágenes y fuentes solo propias o `data:`/`blob:`. Odoo solo mandaba `frame-ancestors 'self'` |
| Cookie sin `Secure` y sin `SameSite` (Bajo) | `proxy_cookie_flags ~ secure samesite=lax;` en el servidor HTTPS: `session_id` sale con `HttpOnly; Secure; SameSite=Lax` |
| `Permissions-Policy` ausente (Bajo) | `geolocation`, `camera` y `microphone` solo del propio sitio; `payment` y `usb` desactivados |
| `Cross-Origin-Opener-Policy` ausente (Bajo) | `same-origin` (el ERP no abre popups de terceros) |

La CSP se probó con Chrome (Playwright, fuera del repo) en el despliegue protegido: login, listas y formularios de ventas e inventario, el pivote de ventas y el PdV (`/pos/ui`) cargan sin ninguna violación de la CSP, salvo las fuentes de respaldo `fonts.odoocdn.com` (Noto, para escrituras poco comunes), que Odoo pide a un CDN externo y quedan bloqueadas a propósito: el ERP no debe depender de un tercero. `scripts/verificar_despliegue.sh` sigue en verde (la política de CSP y de cookies no cambia ninguna de sus comprobaciones).

### Aceptado, con su motivo (`scripts/perf/zap-reglas.conf`)

| Regla | Riesgo | Por qué se acepta |
|---|---|---|
| 10055 CSP `script-src` y `style-src` con `unsafe-inline` / `unsafe-eval` | Medio | Limitación de Odoo 19: el cliente web (OWL) compila sus plantillas con `new Function` y usa scripts y estilos en línea; quitarlos rompe la aplicación. El resto de la CSP sí está cerrada |
| 10098 `Access-Control-Allow-Origin: *` en `/logo.png` y `/web/binary/company_logo` | Medio | Odoo lo hace a propósito: el logo es público y se incrusta en correos y reportes de otros orígenes. No expone datos ni sesión |
| 90004 `Cross-Origin-Embedder-Policy` y `Cross-Origin-Resource-Policy` ausentes | Bajo | Estrictos, bloquean las imágenes y el logo que los correos y otros sitios cargan de este servidor |
| 10010 cookie `frontend_lang` sin `HttpOnly` | Bajo | Es el idioma del sitio público y el JavaScript de Odoo la lee; no guarda sesión (`session_id` sí es `HttpOnly`) |
| 10031 atributo controlable por el usuario (parámetro `redirect` del login) | Informativo | Se comprobó con `redirect="><script>`: Odoo lo escapa. Falso positivo |
| 10015, 10049, 10109, 10111, 10112 | Informativo | Solo informan (caché, aplicación de una sola página, formulario de login, cookie de sesión) |

**Limitaciones.** El certificado es autofirmado (la demo; en una VM real va Let's Encrypt), por eso ZAP corre con la verificación TLS desactivada; el análisis es pasivo y sin sesión (ver arriba); el sitio web público de Odoo (`/web/signup`, `/contactus`, `sitemap.xml`) responde, algo que hay que revisar antes de publicarlo en Internet.

## Evidencias

`docs/capturas/sprint-3/`: `HU-28_evidencia_k6_zap.txt` (salida real de las corridas, el volumen de datos, `docker stats` y la verificación del despliegue), `HU-28_k6_resumen.json`, `HU-28_k6_esfuerzo_resumen.json` y `HU-28_zap_reporte.html` / `.json`.
