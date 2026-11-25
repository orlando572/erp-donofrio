# Anexo 10.4 Solicitud de cambio (RFC)

Este anexo trae el formato de la solicitud de cambio y un ejemplo lleno con un cambio real: la HU-27, el endurecimiento del despliegue (PR #189). La habilitación del cambio de ITIL 4 (y el control 8.32 de ISO/IEC 27001) se cubre con el flujo PR → CI → revisión → fusión → verificación → cierre: el registro es el PR con su plantilla, la evaluación es la lista de la definición de terminado y el CI, la autorización es la aprobación del otro integrante, la implementación es la fusión con *squash* a `develop`, la verificación son el CI y los `verificar_*.sh`, y el cierre es el tag de la release. Los cambios son estándar (bajo riesgo y sin efecto en el sistema desplegado, como la documentación), normales (cambian código, datos o infraestructura, como la HU-27) o de emergencia (una rama `hotfix/*`, que no se usó).

## Formato y ejemplo lleno: RFC-001, endurecimiento del despliegue (HU-27)

| Campo | Contenido |
|---|---|
| ID, fecha y solicitante | **RFC-001** · PR #189 · 23/11/2026 · Orlando |
| Descripción y motivo | Poner Odoo detrás de Nginx con TLS 1.2 y 1.3 y HSTS; modo producción (`workers = 2`, `proxy_mode`, `list_db = False`); 2FA para administrador y gerente; contraseña mínima de 12 caracteres y bloqueo tras 5 intentos por 60 s; `auditlog` en precios, pedidos y compras. Origen: HU-27, RNF009 y RNF010, y los riesgos RSI-02 a 05, 07, 08, 11 y 15 de 5.10 |
| Tipo y componentes | **Normal.** Servicio `nginx` nuevo, imagen de Odoo con `auditlog`, módulo `donofrio_base` (grupo 2FA, política de contraseñas, auditoría), scripts de despliegue y verificación, job `proxy` del CI y manual: 23 archivos, +659 y −8 líneas |
| Impacto | Solo en el despliegue protegido, administrador y gerente piden un código TOTP o por correo; el resto inicia sesión igual. No modifica datos de negocio; en desarrollo no cambia |
| Riesgo | Bloquear a todos los usuarios por el 2FA (2 × 3 = 6, Alta). Se materializó en la primera versión (`_mfa_type` devolvía 403 durante el login), se detectó al probar en el despliegue real y se corrigió con una prueba de regresión; el parámetro `donofrio.2fa_privilegiados` permite apagarlo sin tocar el código |
| Plan de implementación y pruebas | Fusionar `develop` en la rama, construir la imagen, `-u donofrio_base`, `levantar_prod.sh` y `verificar_despliegue.sh`. Pruebas: 12 nuevas de endurecimiento, el job `proxy` y la verificación manual de la redirección a `/web/login/totp` |
| Plan de reversa | Revertir el commit de fusión con un PR (sin *force push*); `docker compose --profile proxy down` y `up -d` vuelven al modo de desarrollo; respaldo previo con `backup.sh` y restauración en una base nueva (31 s). No fue necesario |
| Resultado | **Exitoso, con observaciones.** El job `proxy` falló 2 veces antes de la fusión (el chequeo de TLS y del bloqueo contaba mal) y se corrigió en el mismo PR. Después, ZAP dio 0 alertas altas y k6 un p95 de 12 ms. Lección: probar la autenticación contra el despliegue real y no solo con el ORM |

