# Anexo 10.7 Declaración de Aplicabilidad (SoA) ISO/IEC 27001:2022 y política de seguridad

El proyecto se alinea con ISO/IEC 27001:2022 (ISO/IEC, 2022). Este anexo resume la política de seguridad y la declaración de aplicabilidad por tema; los riesgos y los controles técnicos que la sustentan están en 3.2.1 a 3.2.3.

## Parte A. Política de seguridad de la información

Organización: equipo del ERP académico «D'Onofrio» · Versión 1.0 · 23/11/2026 · Aprueban Orlando (Scrum Master) y Evelyn (Product Owner).

Objetivo y alcance. Proteger la confidencialidad, integridad y disponibilidad de la información del ERP (Odoo 19.0 Community y PostgreSQL 16 en Docker), de su código y de su infraestructura como código en GitHub. Quedan fuera las instalaciones físicas, los equipos personales y los datos reales de D'Onofrio.

Roles. Orlando es el responsable de seguridad y de TI: mantiene los controles técnicos, la declaración de aplicabilidad y la gestión de cambios, y es el único administrador del repositorio. Evelyn es la responsable de la información: decide quién accede a qué, acepta los riesgos residuales y revisa los cambios del otro integrante. Los usuarios (10 roles) usan la información para su función y no comparten su contraseña.

Principios. Mínimo privilegio; defensa en profundidad (TLS, cabeceras, 2FA, bloqueo de intentos, gestor de BD cerrado); todo por código y revisado por el otro integrante con el CI en verde; rastro de los cambios en precios, pedidos y compras; recuperabilidad (respaldo diario, réplica y restauración en 31 s); privacidad con datos ficticios (Ley 29733); y sin credenciales en el repositorio. Los incidentes y solicitudes se registran en la mesa de servicios con su SLA, los cambios como PR, y la política se revisa al cierre de cada sprint.

## Parte B. Declaración de Aplicabilidad

Los 93 controles del Anexo A de ISO/IEC 27001:2022 están en cuatro temas. Cada control aplica (con su mecanismo y su evidencia) o está excluido (no aplica, con su justificación). Los controles que aplican son coherentes con 3.2.2.

### Resumen por tema

| Tema | Controles | Aplican | Excluidos |
|---|---|---|---|
| 5 Organizacionales | 37 | 33 | 4 |
| 6 Personas | 8 | 4 | 4 |
| 7 Físicos | 14 | 0 | 14 |
| 8 Tecnológicos | 34 | 28 | 6 |
| Total | 93 | 65 | 28 |

Controles excluidos (28). Los 14 físicos (7.x) no aplican porque el proyecto no tiene instalaciones propias: el sistema corre en las PC de los integrantes y la seguridad física depende del *host*. De personas no aplican 6.1, 6.2, 6.4 y 6.5 (contratación y cese) porque el equipo son dos estudiantes. Tampoco aplican 5.5, 5.11, 5.12, 5.13, 8.1, 8.11, 8.12, 8.17, 8.23 y 8.30, por tener datos ficticios, sin empleados, sin desarrollo externalizado y sin equipos de usuario final en el alcance.

### Controles clave por tema

| Tema | Controles implementados | Mecanismo y evidencia |
|---|---|---|
| 5 Organizacionales | 5.1 políticas, 5.8 seguridad en la gestión de proyectos, 5.15 control de acceso, 5.17 información de autenticación, 5.18 derechos de acceso, 5.37 procedimientos documentados | Política de una página; 10 roles con grupos, ACL y 4 reglas de acceso por registro; contraseña de 12 caracteres; PR con la definición de terminado y revisión cruzada; pruebas de permisos |
| 8 Tecnológicos (acceso y autenticación) | 8.2 acceso privilegiado, 8.3 restricción de acceso, 8.5 autenticación segura | 2FA obligatorio para administrador y gerente, bloqueo tras 5 intentos, sin usuarios por rol con administración; pruebas de endurecimiento y el script de verificación del despliegue |
| 8 Tecnológicos (operación) | 8.9 configuración, 8.13 copia de seguridad, 8.14 redundancia, 8.15 registro, 8.19 instalación de software, 8.20 seguridad de redes | Configuración por código; respaldo con SHA-256 y retención de 7 días (RTO de 31 s); réplica en *streaming*; el registro de auditoría; imagen con versiones fijas; Nginx con TLS 1.2 y 1.3, HSTS y puertos solo dentro del propio equipo |
| 8 Tecnológicos (desarrollo) | 8.25 ciclo de desarrollo seguro, 8.26 requisitos de seguridad, 8.28 codificación segura, 8.29 pruebas de seguridad, 8.33 información de prueba, 8.34 protección en las pruebas | CI obligatorio (estilo (lint) y pruebas); solo ORM, sin SQL crudo; 21 pruebas de acceso y endurecimiento, ZAP y verificación del despliegue; datos ficticios con semilla fija; pruebas de carga sobre una base aparte |
