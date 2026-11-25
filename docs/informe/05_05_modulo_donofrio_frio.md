# 5.5d Documentación de la cadena de frío (M3, incremento de `donofrio_calidad`)

En la Fase 1 el rango de temperatura de una cámara iba solo en el nombre de la ubicación y las lecturas se anotaban en papel. M3 (HU-19; RF008; CU006) lo lleva al sistema como un incremento de `donofrio_calidad`, sin carpeta propia, y cubre el punto crítico de control de temperatura de HACCP. Se publicó en la release `v1.3.0`.

**Qué hace.** Cada ubicación interna puede tener un rango de temperatura (mínimo y máximo, en °C) y la casilla «Controlar temperatura». El almacén registra lecturas por ubicación; la lectura queda marcada como «Fuera de rango» si el valor sale del rango (los extremos cuentan como dentro) y entonces el sistema crea una actividad para el jefe de almacén con la ubicación, el valor y el rango, una sola vez por lectura. Un *cron* diario avisa además de los lotes con stock que vencen en los próximos 7 días (parámetro configurable), una sola vez por lote. El sistema no mueve ni bloquea lotes: la actividad pide revisarlos y decidir su destino.

| Elemento | Descripción |
|---|---|
| `donofrio.temperatura` | La lectura, con `mail.thread` y actividades: ubicación, temperatura, fecha, quién la tomó, observaciones y `fuera_de_rango` (calculado y almacenado) |
| `stock.location` y `stock.lot` (extendidos) | `control_temperatura`, `temp_min` y `temp_max` (el mínimo no puede superar al máximo); `alerta_vencimiento_fecha` y el *cron* «Calidad: lotes por vencer» |
| Rangos de las cámaras | Congelación (Lima y Arequipa) de −30 a −18 °C y refrigerados de 2 a 6 °C, cargados por una función idempotente que no pisa lo editado a mano |
| Historial y seguridad | Una lectura se juzga con el rango que tenía al registrarse. Sin grupo nuevo: el operario de inventario lee, crea y modifica pero no borra; el jefe de almacén también borra; el usuario interno solo lee |

![Lectura de temperatura fuera de rango con su actividad](../capturas/sprint-4/HU-19_lectura_fuera_de_rango.png)

*Figura 5.5d-a. Lectura fuera de rango: cinta «Fuera de rango» y actividad para el jefe de almacén (datos de demostración).*

**Pruebas y límites.** Las 29 pruebas de la cadena de frío pasan sin errores: rangos, lecturas dentro y fuera de rango, una sola actividad por lectura, correcciones, destinatario, permisos y las nueve del *cron*. En la pantalla se verificaron la lista de lecturas, una lectura dentro y otra fuera de rango, el rango en la ubicación y la actividad del *cron* sobre un lote que vence en 4 días, junto a la alerta estándar de `product_expiry`, que puede coincidir sobre el mismo lote. Las lecturas se registran a mano, sin sensores, y el sistema no avisa si falta una lectura; solo las cuatro cámaras de `donofrio_base` traen rango.
