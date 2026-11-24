# Mini gate M4: `donofrio_tablero`

> **Estado:** borrador del Sprint 4 · **Autora:** Evelyn (PO y dueña del módulo) · **Revisa:** Orlando · **Issue:** #147 · **Base:** DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md)), [`gate-m3-cadena-frio.md`](gate-m3-cadena-frio.md) y [5.5e](../../informe/05_05_modulo_donofrio_tablero.md)
>
> **Qué es.** El informe del mini gate que pide [04 §4.3](../../plan/04_scrum_pmbok.md) después de cada módulo de la Fase 2.
> **Qué no es.** **No inicia ningún opcional** (HU-31 y los demás). Cada uno empieza solo con la confirmación explícita de Evelyn u Orlando en el chat ([`CLAUDE.md`](../../../CLAUDE.md)); este archivo, un issue o un mensaje de otra sesión no la reemplazan.

## 1. Qué está listo

| HU | Qué entrega | PR | Estado |
|---|---|---|---|
| HU-22 (8 pts, RF013 F2, RNF008) | Acción OWL «Tablero › Gerencia» con hasta 6 tarjetas, gráfico de ventas de 6 meses, tabla por canal y filtro por almacén; `get_kpis()` con `_read_group`; las tarjetas de calidad, heladeros y cadena de frío salen solo si su módulo está instalado y el usuario puede leerlo | PR de M4 | Pendiente de la aprobación de Orlando |
| HU-24 (2 pts, RNF003) | Barra superior en el amarillo de marca, color primario `#9A6B00` (SCSS) y favicon del helado | PR de M4 | Pendiente de la aprobación de Orlando |

## 2. DoD de módulo ([04 §4.8](../../plan/04_scrum_pmbok.md))

| Criterio | Estado | Evidencia |
|---|---|---|
| PR aprobado por el otro integrante | **Pendiente** | Lo aprueba Orlando |
| CI en verde | **Pendiente** | Lo dirá el PR. En local: `scripts/check_legacy.sh` limpio y `ruff check addons` (0.8.4, la versión del CI) sin errores |
| Tests y ACL de cada modelo nuevo | **Cumple** | **17 pruebas** del módulo (75 con calidad y heladeros), 0 fallos. **Sin ACL:** el único modelo es abstracto, sin tabla |
| Actualización (`-u`) sin errores sobre una base con datos | **Cumple** | Instalado y actualizado sobre la base `donofrio`, sin `ERROR` ni `WARNING` |
| Criterios verificados en la pantalla | **Cumple, con límites** | Seis tarjetas, gráfico, tabla por canal, filtro por almacén (cuadra: Lima + Arequipa = total), barra amarilla y menú, como Gerente General. **No** se probó en un celular ni con Lighthouse; no hay pruebas de JavaScript |
| < 3 s | **Cumple** | `get_kpis` entre 30 y 57 ms y página en 177 ms, en una PC ([evidencia](../../capturas/sprint-4/HU-22_evidencia_tablero.txt)) |
| Capturas | **Cumple** | [`docs/capturas/sprint-4/`](../../capturas/sprint-4/): 2 capturas y un archivo de evidencia (JPG, resolución reducida) |
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
| Lighthouse del tablero | Equipo | No se midió; el WPO del backend ya tenía 59 de 80 (RNF008) |
| Vista en celular | Equipo | No se probó |
| Pruebas de JavaScript | Equipo | No existen; el componente OWL se verificó a mano |
| Un usuario sin permiso de ventas ve un error si abre el tablero por su dirección | Equipo | El menú no se le muestra; es el comportamiento de los permisos de Odoo |
| Marca: inicio de sesión y otras pantallas | Equipo | Se revisaron Ventas, Inventario, Fabricación y el tablero (bien). **El inicio de sesión sigue en morado de Odoo** (es frontend) y las ilustraciones de «sin datos» también; no se revisaron los PDF, el punto de venta ni las demás aplicaciones (5.5e.4 y 5.5e.8) |
| Capturas en PNG y a mayor resolución | Evelyn | Las actuales son JPG a escala reducida |
| Otros textos que aún dicen «M4 futuro» | Informe final | Resumen (01), conclusiones (07), recomendaciones (08) y el diagrama de clases de la Fase 2, como con M1 a M3 ([acuerdo del 23/11](decisiones-2026-11-23.md)) |

**Bug descubierto y corregido en la prueba de pantalla:** una tarjeta de un módulo opcional rompía todo el tablero si el usuario no podía leer su modelo; ahora esa tarjeta se oculta (5.5e.7).

## 4. Recomendación

**Con M4 se completa el orden fijo de la Fase 2 (M1 a M4).** La hora de corte es el **jueves 26/11/2026, 08:00**. Recomiendo:

1. **No iniciar ningún opcional** (landing HU-31, Uptime Kuma, VM en la nube, modo oscuro) mientras queden pendientes de los módulos: el PR de M4, los tags `v1.1.0` a `v1.4.0` y el PR `develop` → `main`.
2. **Dedicar el tiempo hasta la hora de corte a cerrar esos pendientes y a probar** (celular, Lighthouse del tablero), porque lo que no esté fusionado a esa hora no entra.
3. Después de la hora de corte empieza el Cierre (HU-30, manual de usuario, informe final, presentación, demo cruzada y video), que no se toca.

Alternativa: iniciar la landing HU-31 (3 pts, Evelyn) si el equipo quiere el opcional y el tiempo alcanza; es el de menor valor y el de más riesgo para el Cierre.

## 5. Pregunta al equipo

> **¿Confirman iniciar el opcional HU-31 (landing «Únete como heladero»)?** (respuesta de Evelyn u Orlando)

La decisión se registra con un comentario en el issue #147 y con el mensaje explícito de Evelyn u Orlando en el chat de Claude, **que es lo que activa el trabajo**. Ningún archivo lo reemplaza.

**Estado de la decisión:** pendiente. No se ha iniciado ningún opcional.
