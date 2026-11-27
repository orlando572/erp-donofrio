# 4.3.4 y 4.3.9 IDEs y lenguajes de programación; plataforma de gestión de proyectos

## 2.3.4 Aplicación de herramientas

## 2.3.4.1 IDEs y lenguajes de programación

El entorno de desarrollo es el editor **Visual Studio Code** (con la extensión WSL en Windows), **Git** y su herramienta de línea de comandos para GitHub, **Docker y Compose** para levantar el sistema y **DBeaver** para consultar la base de datos.

**Tabla 4.10. Lenguajes y formatos del proyecto**

| Lenguaje o formato | Dónde se usa |
|---|---|
| **Python** 3.12 | La lógica de los cuatro módulos y sus 218 pruebas automáticas, los scripts de carga de datos y de medición, y los generadores de diagramas |
| **XML y CSV** | Datos y configuración del ERP, pantallas, reportes impresos, permisos de acceso y diagramas de procesos |
| **JavaScript (OWL) y SCSS** | El Tablero gerencial (con los gráficos de Chart.js que trae Odoo) y la marca visual de D'Onofrio (barra superior amarilla) |
| **Bash, YAML, PlantUML y Markdown** | Scripts de pruebas, respaldo y despliegue; configuración de Docker y de GitHub Actions; diagramas; informe y manuales |

La calidad del código se verifica en cada cambio con tres controles automáticos: el revisor de estilo de Python (ruff), el control de instrucciones de Odoo 16 o anteriores y la instalación del módulo con sus pruebas. El tablero se verificó además en pantalla.

## 2.3.4.2 Librerías, frameworks y otros

El proyecto se apoya en el framework de Odoo y en componentes que la propia plataforma trae; no agrega librerías propias. La organización por capas de estas dependencias está en 3.1.2.

**Tabla 2.3.4-b. Librerías, frameworks y otros componentes**

| Componente | Uso en el proyecto |
|---|---|
| Odoo 19.0 Community (framework) | Acceso a la base de datos, pantallas, reportes impresos, permisos por rol, tareas programadas y servidor web |
| OWL y Chart.js (incluidos en Odoo) | Componente del tablero gerencial (M4) y su gráfico mensual |
| Auditoría de la comunidad OCA (auditlog 19.0.2.0.2) | Registro de cambios en precios, pedidos y compras |
| Librerías de Python que trae Odoo | Conexión a PostgreSQL (psycopg2), XML (lxml), servidor web (Werkzeug), PDF (reportlab), imágenes (Pillow), contraseñas (passlib) y validación de documentos como el RUC (python-stdnum) |
| Calidad y medición | ruff (estilo), control de código obsoleto, k6 (carga), OWASP ZAP (seguridad) y Lighthouse (rendimiento web) |
| Diagramas | PlantUML (C4), Mermaid y generadores propios en Python |

## 2.3.4.6 Plataformas de gestión de proyectos de software

Se usó **GitHub Projects** porque es gratuito, está integrado con issues, PR y *commits*, y el docente lo ve sin invitación. Es un único Project, «Scrum ERP D'Onofrio», con 22 ítems (15 épicas y 7 de gestión). Las historias de usuario (HU) se agrupan en épicas, una por área y responsable en cada sprint, y cada HU queda ligada a su rama, a sus commits y a su *pull request*. Cada tarjeta registra estado, sprint, puntos, responsable, fase, tipo y prioridad, y hay tres vistas: *Product Backlog* (tabla por fase), *Sprint actual* (tablero por estado) y *Roadmap* (línea de tiempo). En la Planning se asignan sprint y puntos; la Daily se registra como comentario; y en la Review se marca cada HU terminada con el enlace a su cambio.

El burndown por puntos se calcula con un script que lee el Project.
