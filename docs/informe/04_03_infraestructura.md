# 2.3 Gestión de desarrollo de software, infraestructura y plataforma

## 2.3.1 Infraestructura tecnológica

El ERP corre en contenedores de Docker en la PC de cada integrante (Ubuntu o Windows con WSL2). Las dos PC y el servidor de pruebas automáticas de GitHub usan la misma configuración y la misma versión de Odoo (imagen del 12/11/2026), de modo que el sistema completo se levanta con un solo comando (RNF012).

![Infraestructura tecnológica](../diagramas/arquitectura/infraestructura.png)

*Figura 4.7. Infraestructura tecnológica: PC de desarrollo, contenedores, GitHub, Actions y GHCR.*

La infraestructura tiene cuatro contenedores:

- **Odoo:** el ERP, al que se entra con el navegador; solo acepta conexiones desde el propio equipo.
- **Base de datos (PostgreSQL 16):** guarda toda la información, con un usuario que no tiene permisos de administrador.
- **Réplica:** una segunda base de datos de solo lectura que copia a la principal en tiempo real, para no perder datos si la principal falla.
- **Nginx:** la puerta de entrada segura; cifra la conexión (HTTPS), comprime las páginas y guarda en caché los archivos de la interfaz.

En la nube, GitHub guarda el código con las ramas protegidas, GitHub Actions ejecuta las pruebas en cada cambio y GHCR guarda una copia instalable de cada versión (v1.0.0 a v1.4.0). Las contraseñas están en un archivo de configuración que nunca se sube al repositorio.

## 2.3.2 Plataforma tecnológica

El ERP usa **Odoo 19.0 Community**, escrito en Python, con la base de datos **PostgreSQL 16**. Odoo separa los datos, las pantallas y la lógica (patrón Modelo-Vista-Controlador) y se encarga él mismo de leer y escribir en la base de datos.

**Tabla 4.8. Patrones de la plataforma y su uso en el proyecto**

| Concepto | Cómo lo hace Odoo | Ejemplo en el proyecto |
|---|---|---|
| **Modelo (datos)** | Cada tipo de dato (producto, lote, pedido) es una clase de Python que Odoo convierte en una tabla; el código nunca escribe consultas SQL a mano | Lotes de producto y órdenes de producción |
| **Vista (pantallas)** | Listas, formularios, tableros kanban y tablas dinámicas descritos en XML, y componentes de interfaz en OWL | Pantallas de Inventario y Fabricación; Tablero gerencial |
| **Controlador (acciones)** | Los botones y menús llaman a funciones del modelo | Validar una recepción de mercadería |

**Principios de diseño (SOLID).** Cada módulo tiene una sola responsabilidad (el módulo de configuración base solo configura y carga datos), los módulos estándar de Odoo se amplían sin modificarlos y cada usuario recibe solo los permisos de su rol.

## 2.3.3 Configuración de herramientas

### 2.3.3.1 Desarrollo de software

Se usan Ubuntu o WSL2, el editor VS Code, Docker Compose, DBeaver (para consultar la base de datos) y Git, más un control automático que rechaza instrucciones de versiones antiguas de Odoo. Los datos y la configuración se cargan siempre por código y la interfaz solo se usa para verificar.

### 2.3.3.2 Despliegue de software

El despliegue usa una versión fija de Odoo, la configuración se genera desde un archivo de parámetros, las pruebas corren en cada cambio y el código pasa por tres ramas (trabajo → integración → entrega) con revisión del otro integrante, más Nginx con HTTPS y la réplica de la base de datos (3.4).

### 2.3.3.3 Mantenimiento y monitoreo de software

El mantenimiento actualiza los módulos sobre una base con datos y las pruebas automáticas se repiten cada semana. El monitoreo usa los chequeos de salud de la base de datos y de Odoo, el reinicio automático de los contenedores y respaldos cuya restauración se midió en 31 s.

## 2.3.4.3 Controles de versionamiento

Todo el trabajo (código, datos, scripts, documentación e informe) está en un solo repositorio de Git en GitHub, público y con licencia LGPL-3.0.

**Tabla 4.9. Controles de versionamiento**

| Control | Implementación y qué previene |
|---|---|
| Ramas con propósito | main (lo entregado, una versión por entrega), develop (integración) y una rama corta por historia de usuario; evita mezclar trabajos |
| Convención de commits | Mensajes con un formato común en español y el código de la historia de usuario; deja un historial legible |
| Revisión cruzada | Cada cambio se propone como *pull request* (PR) con pruebas y capturas, y lo aprueba el otro integrante; si el código cambia, se aprueba de nuevo |
| Protección de ramas | Las pruebas automáticas deben pasar y las observaciones deben estar resueltas; no se puede reescribir el historial |
| Freno al código obsoleto | Un control automático con 17 instrucciones de Odoo 16 o anteriores que no se aceptan |

El paso de develop a main se hizo dos veces: al cerrar el núcleo (v1.0.0) y al completar los módulos de D'Onofrio (v1.4.0).

## 2.3.4.4 Máquinas virtuales y contenedores

No se usan máquinas virtuales: todo corre en contenedores de Docker Compose. Odoo y la base de datos se reinician solos si fallan; la réplica y Nginx se activan solo cuando se necesitan (Nginx atiende en los puertos 8080 y 8443). Los datos se guardan en volúmenes de Docker, que sobreviven aunque se borre un contenedor, y los contenedores se comunican por una red interna.

## 2.3.4.5 Plataformas cloud

El ERP se ejecuta en la PC de cada integrante y la demostración protegida se abre en `https://localhost:8443`. Las plataformas en la nube son las de GitHub: el repositorio, GitHub Projects para el backlog, GitHub Actions para las pruebas automáticas (tres flujos: integración continua, rendimiento y publicación), Releases para las versiones v1.0.0 a v1.4.0 (un zip de unos 25 MiB cada una) y GHCR para la imagen instalable de cada versión (unos 3.25 GB).
