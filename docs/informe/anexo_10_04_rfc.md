# Anexo 10.4 Documentos y formatos de control de cambios

Este anexo trae el formato de la solicitud de cambio y un ejemplo lleno con un cambio real: la HU-27, el endurecimiento del despliegue (PR #189). La habilitación del cambio de ITIL 4 (y el control 8.32 de ISO/IEC 27001) se cubre con el flujo PR → CI → revisión → fusión → verificación → cierre: el registro es el PR con su plantilla, la evaluación es la lista de la definición de terminado y el CI, la autorización es la aprobación del otro integrante, la implementación es la fusión integrado a develop como un solo commit, la verificación son el CI y los scripts de verificación, y el cierre es el etiqueta de la versión. Los cambios son estándar (bajo riesgo y sin efecto en el sistema desplegado, como la documentación), normales (cambian código, datos o infraestructura, como la HU-27) o de emergencia (una rama `hotfix/*`).

## Registro por tipo de cambio

Todos los tipos usan el mismo formato de RFC (el PR con su plantilla); cambian los componentes afectados y la forma de verificar y revertir.

| Tipo de cambio | Qué se cambia | Verificación | Reversa |
|---|---|---|---|
| Infraestructura | El archivo de Docker Compose, Nginx, imagen de Odoo, scripts de despliegue | Pruebas automáticas de réplica, respaldo y despliegue protegido; el script de verificación del despliegue | Revertir el PR y volver a levantar con el tag anterior |
| Aplicaciones | Módulos de D'Onofrio (datos, pantallas, seguridad y reportes) | 218 pruebas automáticas, actualización sobre una base con datos y revisión en pantalla | Imagen y zip del tag anterior |
| Base de datos | Modelos (esquema por el ORM) y datos XML | Instalación limpia y actualización en el CI; el script de verificación de la réplica | Respaldo previo con los scripts de respaldo y restauración en una base nueva |
| Documentación | Informe, manuales y diagramas | Revisión del otro integrante (cambio estándar) | Revertir el PR |
| Configuración | Archivo de parámetros, configuración de Odoo y parámetros del sistema cargados por código | El script de verificación del despliegue (modo producción y gestor de bases cerrado) | Revertir el PR y reiniciar el servicio |
| Calendario | Campo Sprint y *Roadmap* del GitHub Project | Acuerdo en la Sprint Planning o en la Review, registrado por el Product Owner | Historial del ítem en el Project |
| Integración continua | Flujos integración continua, rendimiento y publicación | Ensayo del flujo en el mismo PR | Revertir el PR |

## Formato y ejemplo lleno: RFC-001, endurecimiento del despliegue (HU-27)

| Campo | Contenido |
|---|---|
| ID, fecha y solicitante | **RFC-001** · PR #189 · 23/11/2026 · Orlando |
| Descripción y motivo | Poner Odoo detrás de Nginx con TLS 1.2 y 1.3 y HSTS; modo producción (2 procesos de trabajo y gestor de bases de datos cerrado); 2FA para administrador y gerente; contraseña mínima de 12 caracteres y bloqueo tras 5 intentos por 60 s; el registro de auditoría en precios, pedidos y compras. Origen: HU-27, RNF009 y RNF010, y los riesgos RSI-02 a 05, 07, 08, 11 y 15 de 3.2.1 |
| Tipo y componentes | **Normal.** Servicio Nginx nuevo, imagen de Odoo con el registro de auditoría, módulo de configuración base (grupo 2FA, política de contraseñas, auditoría), scripts de despliegue y verificación, prueba automática del despliegue protegido y manual: 23 archivos, +659 y −8 líneas |
| Impacto | Solo en el despliegue protegido, administrador y gerente piden un código TOTP o por correo; el resto inicia sesión igual. No modifica datos de negocio; en desarrollo no cambia |
| Riesgo | Bloquear a todos los usuarios por el 2FA (2 × 3 = 6, Alta). Se presentó en la primera versión (el inicio de sesión devolvía un error de acceso), se detectó al probar en el despliegue real y se corrigió con una prueba que evita que vuelva a pasar; un parámetro del sistema permite desactivar el segundo factor sin tocar el código |
| Plan de implementación y pruebas | Fusionar develop en la rama, construir la imagen, actualizar la configuración base, el script de arranque del despliegue protegido y el script de verificación del despliegue. Pruebas: 12 nuevas de endurecimiento, la prueba automática del despliegue protegido y la verificación manual de que se pide el segundo factor |
| Plan de reversa | Revertir el commit de fusión con un PR (sin reescribir el historial); apagar el despliegue protegido devuelve el modo de desarrollo; respaldo previo con el script de respaldo y restauración en una base nueva (31 s). No fue necesario |
| Resultado | **Exitoso, con observaciones.** La prueba automática del despliegue protegido falló 2 veces antes de la fusión (el chequeo de TLS y del bloqueo contaba mal) y se corrigió en el mismo PR. Después, ZAP dio 0 alertas altas y k6 un p95 de 12 ms. Lección: probar la autenticación contra el despliegue real y no solo con el ORM |

