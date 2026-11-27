# Anexo 10.5 Registro de incidente

Este anexo trae el formato del registro de incidente (ITIL 4), la matriz de prioridad y un ejemplo ficticio de D'Onofrio que coincide con uno de los tickets de la «Mesa de Servicios TI». Un incidente es una interrupción o falla del servicio: algo que antes funcionaba y ya no. Si lo pedido no es una falla, se usa el anexo 10.3.

La prioridad sale de la matriz impacto × urgencia, con los plazos de 4.7.3 (respuesta y resolución): P1, 30 min y 4 h; P2, 2 h y 8 h; P3, 8 h y 3 días; P4, 1 día y 5 días.

## Formato y ejemplo lleno: el tablero gerencial no carga

| Campo | Contenido |
|---|---|
| ID, fecha y reportante | `INC-001` · 20/11/2026, 07:00 (hora de Lima) · Gerente General, Dirección |
| Servicio y síntoma | Tableros de Odoo. Al abrir el panel de ventas la pantalla queda en blanco; afecta solo al gerente |
| Prioridad y SLA | Impacto medio × urgencia alta (lo necesita para una reunión del día) → **P2 Alta**: resolución en 8 h, fecha límite 20/11/2026, 15:00 |
| Diagnóstico | Otros usuarios abren el mismo panel sin problema, así que el servidor funciona; el navegador del gerente guardó una versión vieja de los archivos de la página |
| Solución | Se limpió la caché del navegador y el Responsable de TI confirmó con el gerente que se veía bien |
| Tiempo frente al SLA | Cerrado el 20/11/2026 a las 12:30: 5 h 30 min, dentro de las 8 h. **SLA cumplido** |
| Causa raíz y prevención | Caché con archivos antiguos tras una actualización; no es un defecto del sistema. Se avisa a los usuarios de dirección que, tras una actualización, recarguen con Ctrl + F5; no se abre un problema porque no hay un defecto que corregir |

Odoo Project no registra la primera respuesta, así que solo se mide la resolución.
