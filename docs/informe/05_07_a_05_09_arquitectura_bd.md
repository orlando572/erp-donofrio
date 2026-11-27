# 5.7 a 5.9 Arquitectura del sistema, integración con la base de datos, replicación y administración de la BD

## 3.1.6 Diagramas de arquitectura del sistema (C4)

La arquitectura se describe con el modelo C4, que muestra el sistema en tres acercamientos: el contexto (quién lo usa y con qué se conecta), los contenedores (las piezas que se ejecutan) y los componentes (lo que hay dentro de Odoo). El sistema corre en Docker Compose sobre un solo nodo.

![C4 de contexto](../diagramas/c4/c4_contexto.png)

*Figura 5.7-a. Contexto del ERP de D'Onofrio: personas, sistema y sistemas externos.*

En el contexto participan los 10 usuarios por rol, el ERP (Odoo 19.0 Community sobre PostgreSQL 16) y GitHub (repositorio, Actions, GHCR y versiones).

Los contenedores son los de la tabla siguiente.

| Contenedor | Qué hace | Acceso |
|---|---|---|
| Nginx (solo en el despliegue protegido) | Entrada segura con HTTPS | Puertos 8080 y 8443 |
| Odoo 19.0 con la auditoría de OCA | El ERP | Solo desde el propio equipo (8069 y 8072) |
| PostgreSQL 16 principal y réplica | Base de datos y su copia en tiempo real | Solo desde el propio equipo (5432 y 5433) |

## 3.1.7 Diagramas de integración sistema y base de datos

![C4 de componentes](../diagramas/c4/c4_componentes.png)

*Figura 5.8-a. Componentes de Odoo y su integración con PostgreSQL.*

Las pantallas que ve el usuario (incluido el Tablero gerencial de 3.1.4.5) nunca llegan directo a la base de datos: piden los datos al servidor de Odoo. El servidor (con 2 procesos de trabajo en el despliegue protegido) aplica los permisos de cada usuario, ejecuta la lógica de los módulos y las tareas programadas, y guarda cada operación en una transacción. Odoo lee y escribe solo en la base principal; la réplica sirve para consultas de lectura y como copia en caliente. Los archivos adjuntos se guardan aparte de la base, por lo que el respaldo incluye ambos.

Los canales son: navegador → Nginx por HTTPS (cifrado TLS 1.2 y 1.3; una dirección HTTP se redirige a HTTPS), Nginx → Odoo por la red interna de Docker, y Odoo → PostgreSQL con contraseña cifrada y un usuario sin permisos de administrador.

## 3.1.8 Gestión de replicación

**Estrategia.** La base principal envía cada cambio a la réplica en tiempo real (replicación en *streaming*), sin esperar su confirmación (asíncrona), y la réplica queda disponible para consultas de solo lectura. Es la replicación propia de PostgreSQL y basta porque Odoo escribe en una sola base. La réplica se conecta con un usuario exclusivo para replicar, con contraseña cifrada, y la base principal limita a 1 GB los cambios que guarda para ella. Todo está en el repositorio y se verifica con un script y en las pruebas automáticas.

| Comprobación (23/11/2026) | Resultado |
|---|---|
| Estado de la replicación en la base principal | Activa, asíncrona, con un retraso de 0.002 s |
| La réplica funciona como copia | Sí |
| Dato escrito en el primario y leído en la réplica | Llegó; las tablas de control coinciden |
| Intento de escribir en la réplica | Rechazado: la réplica es de solo lectura |

**Operación.** La replicación es asíncrona (en la medición, el retraso fue de milisegundos) y la réplica se puede convertir en base principal con un solo comando de PostgreSQL.

## 3.1.9 Gestión de administración de la base de datos

**Respaldo y restauración (HU-26).** El script de respaldo genera en cada corrida una copia comprimida de la base, otra de los archivos adjuntos y un archivo de sumas de control (SHA-256) para detectar alteraciones, y borra los respaldos con más de 7 días. El script de restauración restaura en una base nueva (nunca sobrescribe), verifica las sumas y mide el tiempo de recuperación (RTO). El script de verificación del respaldo, que también corre en las pruebas automáticas, ejecuta el ciclo completo: respaldo, restauración, comparación, rechazo de un respaldo alterado y retención.

| Medida | Valor |
|---|---|
| Respaldo | Base de 7.4 MB y adjuntos de 5.4 MB, en 2 s |
| Restauración | RTO medido de 31 s (objetivo RNF006: 2 h); 105 módulos, 14 usuarios y 751 adjuntos |
| Pérdida máxima de datos (RPO) | Hasta 24 h con el respaldo diario; segundos con la réplica |

**Usuarios, cifrado y mantenimiento.** Odoo se conecta con un usuario sin permisos de administrador; la base principal y la réplica solo aceptan conexiones desde el propio equipo, y el gestor de bases de datos de Odoo está deshabilitado (Nginx responde «no encontrado» a esa dirección). El tráfico del navegador va cifrado y el de Odoo, PostgreSQL y la réplica circula por la red interna de Docker; los respaldos llevan su suma de control. La limpieza automática de PostgreSQL ya actuó sobre las tablas más escritas. Odoo crea los índices (1 651 sobre 665 tablas) y los módulos de D'Onofrio indexan los campos que más se buscan; con 143 MB no hizo falta ningún ajuste y las listas responden en 12 ms.
