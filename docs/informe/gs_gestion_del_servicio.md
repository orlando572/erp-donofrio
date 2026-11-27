# 4. Gestión del servicio

## 4.1 GESTIÓN DE SOLICITUDES

Las solicitudes llegan a la «Mesa de Servicios TI», un proyecto de la aplicación Proyecto de Odoo que el módulo de configuración base crea por código con cinco etapas (Nuevo, En análisis, En atención, Resuelto y Cerrado) y tres tipos de ticket: incidente, solicitud de servicio y solicitud de acceso. Al crear un ticket, su fecha límite sale de la prioridad (P1: 4 h; P2: 8 h; P3: 3 días; P4: 5 días) y, al cerrarlo, el campo «Cumplimiento del SLA» lo marca como cumplido o incumplido. La mesa trae cinco tickets de ejemplo que recorren los tres tipos y los tres estados del SLA.

**Tabla 4.1-a. Tickets de la Mesa de Servicios TI**

| Ticket | Tipo | Prioridad | Etapa | SLA |
|---|---|---|---|---|
| Tablero gerencial no carga | Incidente | P2 Alta | Cerrado | Cumplido |
| Alta de un liquidador para la temporada de verano en el CD Arequipa | Solicitud de acceso | P3 Media | Cerrado | Incumplido |
| No imprime la boleta en el punto de venta | Incidente | P1 Crítica | En atención | Abierto |
| Restablecer la contraseña del jefe de almacén | Solicitud de acceso | P3 Media | En análisis | Abierto |
| Nuevo reporte de ventas por zona | Solicitud de servicio | P4 Baja | Nuevo | Abierto |

### 4.1.1 Solicitud de servicios

Una solicitud de servicio pide algo que no es una falla: un reporte nuevo, un cambio de datos maestros o una configuración. Se registra con el tipo «Solicitud de servicio», la atiende el Responsable de TI y, si exige cambiar el software, pasa a ser una solicitud de cambio (4.2). Ejemplo: la jefatura de ventas pide ver las ventas por distrito de Lima (P4, cinco días). El formato está en el anexo 10.3.

### 4.1.2 Solicitud de información

Una solicitud de información pide un dato o una explicación sin cambiar el sistema: una cifra de ventas, el estado de un pedido o cómo se usa una pantalla. Se registra como solicitud de servicio y se responde con los dashboards de ventas, inventario y producción o con las vistas guardadas, que ya están cargados por código y cada rol abre desde su menú; si la respuesta exige un reporte que no existe, se trata como solicitud de servicio.

### 4.1.3 Solicitud de accesos

Una solicitud de acceso pide un usuario, un rol o un cambio de permisos. La aprueba el jefe del área solicitante y la ejecuta el Responsable de TI, que asigna solo los grupos del rol (mínimo privilegio, 3.2.2). Los 10 roles del ERP están definidos por código en el módulo de configuración base, por lo que dar un acceso es asignar un grupo existente y no crear permisos nuevos. Ejemplos: el alta de un liquidador para el CD Arequipa con el grupo «Solo operaciones del CD Arequipa» y el restablecimiento de la contraseña y del segundo factor del jefe de almacén.

### 4.1.4 Herramientas y usos

**Tabla 4.1-b. Herramientas de la gestión de solicitudes**

| Herramienta | Uso |
|---|---|
| Odoo Proyecto, «Mesa de Servicios TI» | Registro, priorización, asignación y cierre de tickets, con etapas y una etiqueta por tipo |
| Campo calculado «Cumplimiento del SLA» | Marca el ticket como abierto, cumplido o incumplido según la fecha de cierre y la fecha límite |
| Vista pivote «Cumplimiento del SLA por tipo de ticket» | Cuenta los tickets por tipo y estado del SLA para el KPI de 2.7.2 |
| Usuarios y grupos de Odoo | Atención de las solicitudes de acceso con los 10 roles definidos |
| Pruebas pruebas de la mesa de servicios (11) | Verifican las etapas, los tipos, la fecha límite por prioridad y el cálculo del SLA |

### 4.1.5 Mejores prácticas aplicadas al proyecto

- Un solo punto de entrada para incidentes y solicitudes, con un tipo por ticket (prácticas de ITIL 4 de gestión de solicitudes de servicio y de incidentes).
- Prioridad por impacto × urgencia y fecha límite automática según la matriz de 2.7.3.
- Aprobación del jefe del área antes de dar un acceso y asignación de grupos ya definidos (mínimo privilegio).
- La mesa, sus etapas y sus tipos se cargan por código y se prueban como cualquier otra configuración.
- Cada ticket cerrado deja su historial (quién, cuándo y qué se hizo), que sirve para mejorar el servicio; por ejemplo, pedir la aprobación al abrir la solicitud de acceso (anexo 10.3).

## 4.2 GESTIÓN DE CAMBIOS

Todo cambio del sistema (código, datos, infraestructura, documentación o calendario) entra por GitHub con el mismo flujo: issue o HU → rama → PR con plantilla → pruebas automáticas → aprobación del otro integrante → fusión → verificación → etiqueta de la versión. Los cambios son estándar (bajo riesgo y sin efecto en el sistema desplegado, como la documentación), normales (cambian código, datos o infraestructura) o de emergencia (rama `hotfix/*`). El formato de la solicitud de cambio (RFC) y un ejemplo real están en el anexo 10.4.

### 4.2.1 Control de cambios en infraestructura

La infraestructura es código: el archivo de Docker Compose (base de datos, Odoo, réplica y Nginx), la configuración de Nginx, la imagen de Odoo y los scripts de despliegue. Un cambio se prueba en las pruebas automáticas de réplica, respaldo y despliegue protegido del CI, con servicios reales, y se verifica con el script de verificación del despliegue sobre el despliegue protegido. Ejemplo: la RFC-001 (HU-27), que agregó Nginx con TLS, el modo producción y el segundo factor.

### 4.2.2 Control de cambios en aplicaciones

Los cuatro módulos de D'Onofrio (configuración base, Calidad, Liquidación de heladeros y Tablero gerencial) cambian por PR y cada entrega queda marcada con un tag semántico (v1.0.0 a v1.4.0). Un cambio de código exige pruebas para la lógica nueva, ACL para los modelos nuevos y que el módulo se instale y se actualice (`-u`) sin errores; el control de código obsoleto rechaza los patrones de versiones anteriores de Odoo.

### 4.2.3 Control de cambios en base de datos

El esquema lo crea el ORM a partir de los modelos, así que un cambio de tabla o columna es un cambio de código que se aplica al actualizar el módulo; nunca se ejecuta SQL a mano. Los datos maestros se cargan de forma que una actualización no los sobrescribe. Antes de actualizar el despliegue se toma un respaldo con el script de respaldo y, si hace falta volver atrás, se restaura en una base nueva con el script de restauración (31 s medidos). La réplica recibe los cambios por *streaming*.

### 4.2.4 Control de cambios de documentación

El informe, los manuales y los diagramas viven en la carpeta de documentación del mismo repositorio y cambian por PR, igual que el código: son cambios estándar, con la revisión del otro integrante. Cada módulo trajo su documentación en el mismo PR, y el historial de revisiones del informe registra una versión por sprint.

### 4.2.5 Control de cambios de calendarios

El calendario es el campo Sprint del GitHub Project (S0 a S4 y Cierre) con la vista *Roadmap*. Mover una HU de sprint se decide en la Sprint Planning o en la Review, lo registra el Product Owner en el Project y queda en el historial del ítem. La fecha de entrega (27/11/2026, 14:30) es fija.

### 4.2.6 Control de cambios e integración continua (CI)

Las ramas develop y main exigen los controles de estilo (lint) y de pruebas, una aprobación y las conversaciones resueltas, y no permiten reescribir el historial. Las pruebas automáticas corren en cada PR y en cada envío a GitHub, cada lunes a las 06:00 de Lima y a demanda. Los propios flujos de GitHub Actions (integración continua, rendimiento y publicación) cambian por PR y se ensayan en ese mismo PR antes de fusionarse.

### 4.2.7 Herramientas y usos

**Tabla 4.2-a. Herramientas de la gestión de cambios**

| Herramienta | Etapa del cambio | Uso |
|---|---|---|
| GitHub Issues y Projects | Registro y planificación | HU con criterios de aceptación, sprint y puntos |
| PR con plantilla | Evaluación | Descripción, HU, pruebas, capturas y lista de la definición de terminado |
| Protección de ramas | Autorización | Una aprobación del otro integrante y controles obligatorios |
| GitHub Actions | Prueba | Revisión de estilo, 218 pruebas y pruebas de réplica, respaldo y despliegue protegido |
| Los scripts de verificación | Verificación | Comprobaciones sobre el entorno desplegado y sobre la imagen |
| Versiones etiquetadas, GitHub Releases y GHCR | Cierre y reversa | Versión inmutable (imagen y zip) para volver al tag anterior |
| Los scripts de respaldo y restauración | Reversa de datos | Respaldo previo y restauración en una base nueva |

### 4.2.8 Mejores prácticas aplicadas al proyecto

- Todo por código: datos, configuración, infraestructura y documentación cambian por PR.
- Separación de funciones: quien hace el cambio no lo aprueba.
- Cambios pequeños: una rama y un PR por HU, integrado a develop como un solo commit.
- Cada cambio tiene su prueba y su plan de reversa (tag anterior o respaldo).
- Versiones inmutables: imagen y zip por versión en GHCR y Releases.
- El flujo cubre la práctica de habilitación del cambio de ITIL 4 y el control 8.32 de ISO/IEC 27001.

## 4.3 GESTIÓN DE CAPACIDAD Y RENDIMIENTO DEL SERVICIO

La capacidad y el rendimiento se midieron sobre el despliegue protegido (Nginx con TLS y Odoo con 2 procesos de trabajo) en una PC de 12 CPU lógicas y 14 GB de RAM, con los datos de demostración de 16 semanas. El plan con su formato está en el anexo 10.5.

### 4.3.1 Capacidad de servicios

**Tabla 4.3-a. Capacidad instalada**

| Elemento | Capacidad |
|---|---|
| Nodo | Una PC con Docker Compose; el entorno completo necesita unos 4 GB de RAM libres |
| Odoo | Modo producción con 2 procesos de trabajo, detrás de Nginx; 109 módulos cargados en la imagen |
| PostgreSQL 16 | Primario y réplica en *streaming*; base de demostración de 665 tablas y 143 MB |
| Respaldo | Base de 7.4 MB y archivos adjuntos de 5.4 MB, con retención de 7 días |
| Usuarios | 10 roles; la prueba de carga usa 20 usuarios virtuales concurrentes |

### 4.3.2 Rendimiento de servicios

Con 20 usuarios virtuales y pausas de 1 a 3 s (carga normal), k6 midió un percentil 95 de 11.6 ms en listas, 9.1 ms en formularios, 13.0 ms en el tablero y 342 ms en el inicio de sesión, con 0 % de errores en 2 765 comprobaciones. Sin pausas (esfuerzo, unas 20 veces más peticiones), el percentil 95 subió a 100 ms. En el navegador, el login obtuvo 100 en Lighthouse, el dashboard de ventas 80 y el tablero gerencial cargó en 2.11 s (LCP); la réplica tuvo un retraso de 2.3 ms y la restauración de un respaldo tardó 31 s.

### 4.3.3 Análisis

#### 4.3.3.1 Métricas

**Tabla 4.3-b. Métricas de capacidad y rendimiento**

| Métrica | Umbral (2.7.3) | Carga normal | Esfuerzo |
|---|---|---|---|
| Tiempo de respuesta p95 | < 2 s | 9.1 a 13.0 ms (login 342 ms) | 100 ms |
| Peticiones con error | < 1 % | 0 % | — |
| CPU de Odoo | — | 39 % de una CPU | 160 % (2 procesos de trabajo) |
| Memoria de Odoo | — | 440 MiB | 513 MiB |
| CPU y memoria de PostgreSQL | — | 6 % y 195 MiB | 57 % y 201 MiB |
| LCP del tablero | < 3 s | 2.11 s | — |
| RTO del respaldo | ≤ 2 h | 31 s | — |

#### 4.3.3.2 Técnicas

Se usaron pruebas de carga con k6 en dos escenarios (normal y de esfuerzo) sobre una base aparte; la observación de recursos con el monitor de recursos de Docker cada 10 s durante la carga; Lighthouse con la mediana de tres corridas por vista; la restauración cronometrada de un respaldo; y la medición del retraso de la réplica con el script de verificación de la réplica. El análisis muestra que el primer recurso que se acerca a su límite es la CPU de Odoo (los 2 procesos de trabajo), mientras PostgreSQL queda por debajo del 60 %, y que la memoria se mantiene estable.

### 4.3.4 Planificación

- Escalar Odoo primero: si la CPU de Odoo pasa del 80 % de forma sostenida o el p95 supera 1 s, aumentar los procesos de trabajo (Odoo recomienda unos 2 por CPU disponible, más 1) antes que la base de datos.
- Repetir la medición antes de cada temporada alta: antes del verano, con los heladeros y liquidadores previstos como usuarios virtuales en k6, y comparar con la línea base de la Tabla 4.3-b.
- Lecturas en la réplica: las consultas de análisis externas (por ejemplo, desde DBeaver) se hacen sobre la réplica de solo lectura, para no cargar el primario.
- Crecimiento de datos: vigilar el tamaño de la base y de los respaldos (retención de 7 días) en cada versión.

### 4.3.5 Herramientas y usos

**Tabla 4.3-c. Herramientas de capacidad y rendimiento**

| Herramienta | Uso |
|---|---|
| k6 | Carga normal y de esfuerzo con 20 usuarios virtuales y umbral p95 < 2 s |
| El monitor de recursos de Docker | CPU y memoria de cada contenedor durante la carga |
| Lighthouse 12 | Rendimiento web (LCP y TBT) del login, el backend, el dashboard y el tablero |
| El flujo de rendimiento (GitHub Actions) | Corre a demanda la carga de datos, el despliegue protegido, k6 y ZAP, y sube los reportes |
| *Healthchecks* y la página de estado de Odoo | Estado de PostgreSQL y de Odoo, con reinicio automático |
| El script de verificación de la réplica y el script de restauración | Retraso de la réplica y tiempo de recuperación |

### 4.3.6 Mejores prácticas aplicadas al proyecto

- Medir antes de dimensionar: los umbrales del ANS se contrastan con mediciones reales.
- Comparar en el mismo entorno: la misma imagen y el mismo archivo de Docker Compose en las PC y en el CI.
- Mediana de varias corridas en Lighthouse y escenarios separados (normal y de esfuerzo) en k6.
- Base aparte para las pruebas de carga, para no alterar los datos de demostración.
- Reportes guardados como artefactos del CI, para comparar entre versiones.
