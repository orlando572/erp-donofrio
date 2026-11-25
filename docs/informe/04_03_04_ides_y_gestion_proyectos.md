# 4.3.4 y 4.3.9 IDEs y lenguajes de programación; plataforma de gestión de proyectos

## 4.3.4 Aplicación de herramientas: IDEs y lenguajes de programación

El entorno de desarrollo es **Visual Studio Code** (con la extensión WSL en Windows), **Git** y la CLI **`gh`**, **Docker y Compose**, **DBeaver** para leer PostgreSQL y un asistente de IA (Claude Code) como herramienta de los *Developers*, con un *hook* que rechaza patrones de Odoo anteriores a la 19.

**Tabla 4.10. Lenguajes y formatos del proyecto**

| Lenguaje o formato | Dónde se usa |
|---|---|
| **Python** 3.12 | Los cuatro módulos (modelos, *hooks* y 218 pruebas con `TransactionCase`), los scripts de datos y medición y los generadores de diagramas |
| **XML y CSV** | Datos y configuración del ERP, vistas, reportes QWeb, permisos de acceso y diagramas BPMN |
| **JavaScript (OWL) y SCSS** | Tablero de M4 (componente OWL con Chart.js, que trae Odoo) y la marca visual (color primario `#9A6B00`, barra superior amarilla) |
| **Bash, YAML, PlantUML y Markdown** | Scripts de pruebas, respaldo y despliegue; Compose y GitHub Actions; diagramas; informe y manuales |

La calidad del código se verifica en el CI con `ruff`, con `check_legacy.sh` (patrones de Odoo 16 o anteriores) y con la instalación del módulo con `--test-enable`. No hay pruebas de JavaScript del componente OWL: el tablero se verificó en pantalla y con las pruebas de Python de `get_kpis()`.

## 4.3.9 Plataformas de gestión de proyectos

Se usó **GitHub Projects** porque es gratuito, está integrado con issues, PR y *commits*, y el docente lo ve sin invitación. Es un único Project, «Scrum ERP D'Onofrio», con 22 ítems (15 épicas y 7 de gestión). Las HU van como lista dentro de un issue de épica, una por área y dueño en cada sprint; cada HU tiene su rama `feature/HU-xx-*`, `[HU-xx]` en cada commit y `Parte de #n` en cada PR. Los campos son Status, Sprint (S0 a S4 y Cierre), Puntos, Responsable, Fase, Tipo y Prioridad, y las vistas son *Product Backlog* (tabla agrupada por fase), *Sprint actual* (tablero por estado) y *Roadmap* (línea de tiempo). En el Planning se asignan sprint y puntos; la Daily es un comentario en el issue «Dailies»; en la Review se marca la lista de cada épica con el enlace al PR.

El Project tiene seis *workflows* integrados y solo uno activo, por lo que el estado de las tarjetas se cambia a mano; el burndown por puntos se calcula con un script que lee el Project, porque Insights cuenta ítems y no puntos.
