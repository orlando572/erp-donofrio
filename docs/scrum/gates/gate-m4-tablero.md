# Mini gate M4: `donofrio_tablero`

> **Estado:** borrador del Sprint 4 · **Autora:** Evelyn (PO y dueña del módulo) · **Revisa:** Orlando · **Issue:** #147 · **Base:** DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md)), [`gate-m3-cadena-frio.md`](gate-m3-cadena-frio.md) y [5.5e](../../informe/05_05_modulo_donofrio_tablero.md)
>
> **Qué es.** El informe del mini gate que pide [04 §4.3](../../plan/04_scrum_pmbok.md) después de cada módulo de la Fase 2.
> **Qué no es.** **No inicia ningún opcional** (HU-31 y los demás). Cada uno empieza solo con la confirmación explícita de Evelyn u Orlando en el chat ([`CLAUDE.md`](../../../CLAUDE.md)); este archivo, un issue o un mensaje de otra sesión no la reemplazan.

## 1. Qué está listo

| HU | Qué entrega | PR | Estado |
|---|---|---|---|
| HU-22 (8 pts, RF013 F2, RNF008) | Acción OWL «Tablero › Gerencia» con hasta 6 tarjetas, gráfico de ventas de 6 meses, tabla por canal y filtro por almacén; `get_kpis()` con `_read_group`; las tarjetas de calidad, heladeros y cadena de frío salen solo si su módulo está instalado y el usuario puede leerlo; **sin permiso de lectura, un aviso en español en vez del «Error de acceso»** (corrección del 24/11) | PR de M4 | Pendiente de la aprobación de Orlando |
| HU-24 (2 pts, RNF003) | Barra superior en el amarillo de marca, color primario `#9A6B00` (SCSS), favicon del helado, **inicio de sesión y caritas de «sin datos» con la marca** (corrección del 24/11) | PR de M4 | Pendiente de la aprobación de Orlando |

## 2. DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md))

| Criterio | Estado | Evidencia |
|---|---|---|
| PR aprobado por el otro integrante | **Pendiente** | Lo aprueba Orlando |
| CI en verde | **Pendiente** | Lo dirá el PR. En local: `scripts/check_legacy.sh` limpio y `ruff check addons` (0.8.4, la versión del CI) sin errores |
| Tests y ACL de cada modelo nuevo | **Cumple** | **21 pruebas** del módulo (79 con calidad y heladeros), 0 fallos ni errores (corridas del 24/11 en la rama con las dos correcciones; `scripts/check_legacy.sh` sin patrones legacy). **Sin ACL:** el único modelo es abstracto, sin tabla |
| Actualización (`-u`) sin errores sobre una base con datos | **Cumple** | Instalado y actualizado sobre la base `donofrio`, sin `ERROR` ni `WARNING` (primera entrega). El 24/11 se instaló además desde cero en una base nueva con los datos de demostración (los cuatro módulos), sin errores; la actualización de las dos correcciones sobre la base del equipo no se repitió |
| Criterios verificados en la pantalla | **Cumple, con límites** | Seis tarjetas, gráfico, tabla por canal, filtro por almacén (cuadra: Lima + Arequipa = total y el total coincide con SQL), barra amarilla y menú, como Gerente General; aviso de «sin permiso» con el Vendedor; login con la marca. **Celular:** probado en un emulador, sin desplazamiento horizontal y legible ([5.5e.6.1](../../informe/05_05_modulo_donofrio_tablero.md)); no en un teléfono real. **Lighthouse del tablero: 76 en escritorio, bajo la meta de 80** (ver §3). No hay pruebas de JavaScript |
| < 3 s | **Cumple** | `get_kpis` entre 30 y 57 ms y página en 177 ms, en una PC ([evidencia](../../capturas/sprint-4/HU-22_evidencia_tablero.txt)); Lighthouse en el despliegue protegido: **LCP del tablero 2.11 s** ([evidencia](../../capturas/sprint-4/S4_evidencia_verificacion_m4.txt)) |
| Capturas | **Cumple** (las de M4) | [`docs/capturas/sprint-4/`](../../capturas/sprint-4/): PNG de 1600 × 900 del tablero (todos los almacenes, filtro Arequipa, sin permiso), de la marca (barra, ventas, fabricación, entregas, «sin datos», login) y del celular, más la [evidencia](../../capturas/sprint-4/S4_evidencia_verificacion_m4.txt) y el CSV de Lighthouse. Las de M1 y M2 (HU-17, 18, 20 y 21) se rehicieron el 25/11 en PNG de 1600 × 900 (ver los gates de M1 y M2), igual que las del tablero con las tarjetas llenas |
| Checklist de la épica #147 | **Parcial** | Con el PR; el criterio de la carga se marca con la medición de una PC |
| Sección del informe | **Cumple** | [5.5e](../../informe/05_05_modulo_donofrio_tablero.md); RF013 en 4.2.2 y 10.1; CU009; 4.4; 4.2.5 |
| ER y diccionario extraídos de nuevo | **No aplica** | M4 no crea tablas: el ER (42 tablas) y el diccionario no cambian |
| **Tag de release de M4** | **Falta** | `v1.4.0`, según el esquema de los módulos anteriores (v1.1.0 a v1.3.0); lo crea Orlando desde `main`, tras el PR `develop` → `main` |
| Mini gate escrito | **Cumple** | Este archivo |

## 3. Qué falta o falló

| Pendiente | Quién | Nota |
|---|---|---|
| Aprobación y CI del PR de M4 | Orlando | Ruff 0.8.4 pasó en local; falta el resultado del CI |
| Tag `v1.4.0` | Orlando | Con el merge `develop` → `main`; el primero fue *squash* y el siguiente PR a `main` puede dar conflictos |
| Marcar la tarjeta de #147 en el Project | Orlando | Evelyn solo tiene lectura |
| **Lighthouse del tablero: 76, la meta es 80** | Equipo | Medido el 24/11 (3 corridas: 76, 76 y 81). Escritorio: **76** (LCP 2.11 s); móvil: **39** (CPU 4× más lento). El login sí cumple (100 y 95). RNF008 queda **Parcial**; falta decidir si se mejora (p. ej. el *Speed Index*) o se declara como límite, como el backend (59). El tablero «después» se midió con el Jefe de Almacén porque el Gerente pide 2FA en el despliegue protegido ([5.5e.6.2](../../informe/05_05_modulo_donofrio_tablero.md)) |
| Vista en celular | Equipo | **Hecha en emulador (375 × 812):** sin desplazamiento horizontal, tarjetas en una columna, gráfico legible. **Falta** probarla en un teléfono real y el cambio de almacén en el celular |
| Pruebas de JavaScript | Equipo | No existen; el componente OWL se verificó a mano |
| ~~Un usuario sin permiso de ventas ve un error si abre el tablero~~ | **Resuelto** (24/11) | Recibe un aviso en español; 4 pruebas nuevas y captura con el Vendedor. Queda como límite que no hay una versión parcial del tablero por áreas |
| Marca: otras pantallas | Equipo | **Resuelto:** el inicio de sesión y las ilustraciones de «sin datos» ya usan la marca (capturas PNG). **Pendiente:** no se revisaron los PDF, el punto de venta, otras páginas públicas (portal, restablecer contraseña) ni las demás aplicaciones (5.5e.4 y 5.5e.8) |
| ~~Capturas en PNG y a mayor resolución~~ de M4 | **Resuelto** (24/11) | PNG de 1600 × 900. ~~**Pendiente:** las de M1 y M2 (HU-17, 18, 20 y 21) siguen en JPG reducido~~ **Resuelto** (25/11): rehechas en PNG de 1600 × 900 con los datos de demostración; quedan solo dos JPG históricos que no se pueden reproducir sin crear datos (`HU-20_error_devuelto_mas_merma`, `HU-24_limite_login_morado`) |
| Otros textos que aún dicen «M4 futuro» | Informe final | Resumen (01), conclusiones (07), recomendaciones (08) y el diagrama de clases de la Fase 2, como con M1 a M3 ([acuerdo del 23/11](decisiones-2026-11-23.md)) |

**Bugs descubiertos y corregidos en la prueba de pantalla:** (1) una tarjeta de un módulo opcional rompía todo el tablero si el usuario no podía leer su modelo; ahora esa tarjeta se oculta (5.5e.7). (2) El Jefe de Ventas (que ve el menú) y el Vendedor (si abre la dirección) recibían «Error de acceso» porque no leen lotes ni existencias; ahora reciben el aviso de «sin permiso» (5.5e.5). Esta verificación no encontró ningún error nuevo del módulo; no se tocó código.

## 4. Recomendación

**Con M4 se completa el orden fijo de la Fase 2 (M1 a M4).** La hora de corte es el **jueves 26/11/2026, 08:00**. Recomiendo:

1. **No iniciar ningún opcional** (landing HU-31, Uptime Kuma, VM en la nube, modo oscuro) mientras queden pendientes de los módulos: el PR de M4, los tags `v1.1.0` a `v1.4.0` y el PR `develop` → `main`.
2. **Dedicar el tiempo hasta la hora de corte a cerrar esos pendientes**, porque lo que no esté fusionado a esa hora no entra. Las pruebas del celular y de Lighthouse ya se hicieron (el tablero sale en 76, bajo la meta de 80): queda decidir si se mejora o se declara el límite.
3. Después de la hora de corte empieza el Cierre (HU-30, manual de usuario, informe final, presentación, demo cruzada y video), que no se toca.

Alternativa: iniciar la landing HU-31 (3 pts, Evelyn) si el equipo quiere el opcional y el tiempo alcanza; es el de menor valor y el de más riesgo para el Cierre.

## 5. Pregunta al equipo

> **¿Confirman iniciar el opcional HU-31 (landing «Únete como heladero»)?** (respuesta de Evelyn u Orlando)

La decisión se registra con un comentario en el issue #147 y con el mensaje explícito de Evelyn u Orlando en el chat de Claude, **que es lo que activa el trabajo**. Ningún archivo lo reemplaza.

**Decisión de Evelyn en el chat (24/11/2026):** no iniciar ningún opcional, conforme a la recomendación de este mini gate. HU-31, Uptime Kuma, la VM en la nube y el modo oscuro quedan como trabajo futuro. **Falta** el comentario con esta decisión en #147 y la respuesta de Orlando; no se ha iniciado ningún opcional.
