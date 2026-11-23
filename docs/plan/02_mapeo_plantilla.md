# 2. Mapeo de los lineamientos y la plantilla al trabajo

[← Índice](PLAN_PROYECTO.md)

**Responsables:** E = Evelyn · O = Orlando · E+O = compartido (el primero que aparece redacta y el otro revisa).
**Sprints y fases** (ver [04_scrum_pmbok.md](04_scrum_pmbok.md)):
- S0 = Inicio.
- S1-S3 = **Fase 1** (núcleo).
- S4 = **Fase 2** (módulos propios, uno a uno).
- Cierre = bloque reservado al final.
- Un solo plan: los sprints van en orden, con un *timebox* de ~1 día cada uno y sin fechas. Único límite: **entrega de todo el viernes 27 de noviembre, 14:30**.

**Toda sección tiene un borrador completo con contenido de la Fase 1 antes del Gate 0.** "S3 → Cierre" significa borrador en S3 y versión final en el Cierre. Las secciones que cambian si se llega a la Fase 2 están en la §2.3.

## 2.1 Los 12 puntos de "Información a entregar" del PDF de lineamientos

| # | Punto del lineamiento | Dónde se cubre en la plantilla | Responsable |
|---|---|---|---|
| 1 | Análisis empresarial y del negocio | 3 y 4.1 | E |
| 2 | Planificación de proyectos PMBOK con enfoque ágil | 4.2 (calendarización, Scrum) y 6.1 a 6.3 | E |
| 3 | Gestión de desarrollo de software, infraestructura y plataforma | 4.3 | O |
| 4 | Diseño de prototipos | 4.4 y 4.6 | E |
| 5 | Gestión de riesgos | 4.5 | E+O |
| 6 | Desarrollo front-end y rendimiento WPO | 4.6 | E |
| 7 | Acuerdos de nivel de servicio | 4.7 | E |
| 8 | Integración con base de datos, administración y buenas prácticas | 5.1 a 5.9 | O |
| 9 | Gestión de seguridad de información y controles | 5.10 y 5.11 | O |
| 10 | Seguridad y defensa ante ataques basada en riesgos | 5.12 | O |
| 11 | Validación de servicios, pruebas RF y RNF | 5.13, 5.14 y 6.9 a 6.13 | E+O |
| 12 | Despliegue: herramientas, procedimiento y resultados | 5.15 | O |

Entregables a-f del lineamiento: ver el checklist en [07_riesgos_entrega.md](07_riesgos_entrega.md).

## 2.2 Sección por sección de la plantilla

La plantilla no trae números visibles en los títulos. Esta numeración sigue su orden real y se fija para todo el equipo. La sección 6.4 corresponde a "Resumen del GitHub".

| Sección de la plantilla | Qué se entrega | Herramienta / origen | Resp. | Sprint |
|---|---|---|---|---|
| **Portada** | Título "ERP para D'Onofrio con Odoo 19", enlace de GitHub, ciclo, tabla de integrantes ordenada por apellidos con CUI | Word | E | S3 → Cierre |
| **Historial de revisiones** | Una fila por sprint (v0.1 S1 … v1.0 entrega). Solo se llenan las 4 primeras columnas | Word | E | S1-S3, Cierre |
| **Índices** de contenidos, figuras y tablas | Índices automáticos de Word (títulos y leyendas) | Word: Referencias → Insertar índice | E | S3 → Cierre |
| **1. Resumen** | Organización, problemas, solución (Odoo 19 + PostgreSQL, web) y módulos principales | Texto | E | S3 → Cierre |
| **2. Abstract** | Traducción del resumen | Texto | O | S3 → Cierre |
| **3. Aspectos generales**: 3.1 Definición del problema, 3.2 Descripción del problema | Situación actual, datos de la empresa, giro, áreas, problemas, trabajadores y responsabilidades, organigrama, tabla de supuestos | Fuentes de [01](01_alcance_escenario.md); organigrama exportado de Odoo RR. HH. o draw.io | E | S1 |
| 3.3 Visión, 3.4 Misión | Visión y misión de la unidad (redacción propia, inspirada en la pública de Nestlé, citada) | Texto | E | S1 |
| 3.5 Entorno | PESTEL + 5 fuerzas (competencia: Alicorp/Lamborgini, Gloria, panaderías artesanales; caso Froneri) | Tabla PESTEL | E | S1 |
| 3.6 Estrategia empresarial | FODA y estrategias FO/DO; estacionalidad complementaria | Tabla FODA | E | S1 |
| 3.7 Planificación empresarial | Objetivos estratégicos ligados a los KPIs del ERP (BSC sencillo) | Tabla | E | S1 |
| **4. Planificación y front-end** | | | | |
| 4.1.1 Análisis de sistemas | Sistemas actuales por área (AS-IS supuesto) y sus brechas | Tabla | E | S1 |
| 4.1.2 Procesos AS-IS | 5 diagramas BPMN: venta B2B, liquidación de heladero, producción y calidad, compras de insumos, recepción y despacho con cadena de frío. También los TO-BE (en Odoo) para contrastar | bpmn.io / Camunda Modeler (gratis), exportado a PNG | E (ventas, heladeros, compras), O (producción y calidad, almacén y cadena de frío) | S1 (AS-IS), S2 (TO-BE) |
| 4.1.3 Arquitectura empresarial | Arquitectura actual y propuesta: software, datos y tecnología | draw.io (capas TOGAF simplificadas) | O | S1 |
| 4.1.4 Identificación de oportunidades de innovación tecnológica | Tabla 1 (problema → oportunidad → tecnología), ya redactada en [01 §1.6](01_alcance_escenario.md) | Tabla | E | S1 |
| 4.2.1 Gestión de requerimientos | Proceso: HU → RF/RNF → épica (issue) → prueba; matriz de trazabilidad | Tabla | E | S1 |
| 4.2.2 Requerimientos funcionales | Tabla 2: RF001 a RF018 por área, con columna de fase (ver [04 §4.2](04_scrum_pmbok.md)); el detalle en ficha va en el Anexo 10.1 | Tabla | E | S1 |
| 4.2.3 Requerimientos no funcionales | Tabla 3: RNF001 a RNF013 por área; el detalle en ficha va en el Anexo 10.2 | Tabla | O | S1 |
| 4.2.4 Diagramas de casos de uso | Diagrama general por área + CU001 a CU010, cada uno con su ficha (tabla 4) | PlantUML (en el repo, `docs/diagramas/*.puml`) | E (CU de ventas, heladeros, gerencia), O (CU de logística, producción, calidad) | S2 |
| 4.2.5 Diagrama de clases | **F1:** clases del dominio de D'Onofrio sobre los modelos de Odoo que se usan (`sale.order`, `stock.lot`, `mrp.production`, `mrp.bom`, `res.partner`, `product.template`, `hr.employee`) + lo que agrega `donofrio_base`. **F2:** + clases propias, marcadas como "implementado" o "propuesto" | PlantUML | O | S3 (+F2) |
| 4.2.6 Diseño de base de datos: modelo ER | ER **extraído de la BD real** después de instalar, filtrado a unas 30 tablas relevantes (F1: núcleo; con cada módulo de la F2 se vuelve a extraer y se agregan las tablas `donofrio_*`) | SchemaSpy (Docker) + DBeaver | O | S3 (+F2) |
| 4.2.7 Diseño lógico | **F1:** diagrama físico de las tablas centrales del negocio (pedidos, movimientos, lotes, OP, BoM). **F2:** + tablas `donofrio_*` y sus FK | DBeaver (diagrama ER) | O | S3 (+F2) |
| 4.2.8 Diccionario de datos | Tabla 5 por entidad: PK/FK, nombre, campo, tipo, tamaño, descripción. Se genera con un script desde `information_schema` + `ir_model_fields`; en el informe van las tablas propias y el resto como anexo o archivo | `scripts/diccionario_datos.py` → XLSX/MD | O | S3 |
| 4.2.9 Gestión de calendarización | Tabla 6 (cronograma de hitos en orden, ver [04 §4.10](04_scrum_pmbok.md)) + ilustración 6 (Gantt armado con las fechas reales de ejecución que registra el Project, no con fechas planificadas) | GitHub Projects (vista Roadmap) o diagrama Mermaid gantt | E | S0, se actualiza en cada sprint |
| 4.2.10 Desarrollo ágil Scrum: roles | Tabla 7 | Texto | E | S0 |
| 4.2.11 Artefactos | Product Backlog (tabla 8) y Sprint Backlog (tabla 9), con capturas de las vistas "Product Backlog" y "Sprint actual" | GitHub Projects | E | S0-S4 |
| 4.2.12 Eventos | Sprint, Planning, Daily, Review y Retro, con evidencias (ilustración 7) | GitHub Projects (issue "Dailies") + actas `docs/scrum/` | E | S0-S4 |
| 4.3.1 Infraestructura tecnológica | Diagrama: PC de desarrollo, Docker, contenedores Odoo/PostgreSQL/réplica/Nginx, GitHub, runner de Actions y (opcional) VM en la nube | draw.io | O | S1 |
| 4.3.2 Plataforma tecnológica | Odoo como MVC (ORM = DAO/Active Record, vistas XML/OWL, controladores), DTO (diccionarios JSON-RPC), SOLID aplicado a módulos y herencia | draw.io + texto | O | S2 |
| 4.3.3 Configuración de herramientas: desarrollo, despliegue, mantenimiento y monitoreo | Lineamientos breves; el detalle va al **Manual de herramientas** | Texto | O | S2 |
| 4.3.4 Aplicación de herramientas: IDEs y lenguajes de programación | VS Code (+ extensiones Python, XML, Odoo), Python 3.12, XML, JavaScript/OWL, SCSS, SQL | Texto | E | S2 |
| 4.3.5 Librerías, frameworks y otros: organización de paquetes, librerías y dependencias de comunicación | Árbol `addons/` (captura de VS Code); inventario de librerías (Odoo 19, OWL, Chart.js incluido en Odoo, psycopg2, OCA `auditlog`); dependencias de comunicación (HTTP/JSON-RPC, WebSocket del bus en el puerto 8072, protocolo PostgreSQL 5432, replicación) | `tree`, capturas | O | S3 |
| 4.3.6 Controles de versionamiento | Git + GitHub, ramas y responsables (resumen; el detalle va en 6.4 a 6.8) | Captura de GitHub | O | S1 |
| 4.3.7 Máquinas virtuales y contenedores | Docker Compose: servicios, volúmenes, perfiles y redes | `docker compose ps` + captura | O | S1 |
| 4.3.8 Plataformas cloud | GitHub (repo, Actions, GHCR) + VM en la nube opcional (decisión abierta) | Capturas | O | S3 → Cierre |
| 4.3.9 Plataformas de gestión de proyectos | GitHub Projects: issues, campos, vistas y uso (ilustración 16), según [04 §4.11](04_scrum_pmbok.md) | GitHub Projects + CLI `gh` | E | S1 |
| 4.4.1 Wireframes | Uno por caso de uso; detalle completo para las pantallas propias de la F2 (liquidación, inspección, temperatura, tablero), **que se diseñan en la F1 aunque no se implementen**, y versión simple para las estándar de Odoo | Excalidraw o Figma (gratis) | E | S2 |
| 4.4.2 Mockups | Mockups en alta fidelidad con la paleta de marca (amarillo de los carritos) | Figma | E | S2 |
| 4.5.1 Plan de gestión de riesgos | Tabla 10 + estrategias (evitar, mitigar, transferir, aceptar) + escalas 1-3 | Tabla en `docs/pm/plan_riesgos.md` + issue "Registro de riesgos" | E | S0 |
| 4.5.2 a 4.5.4 Riesgos por etapa: desarrollo, despliegue, mantenimiento | Tablas 11 a 13 con nivel = impacto × probabilidad, prioridad, seguimiento, frecuencia, herramienta y validación | Tabla (ver [07](07_riesgos_entrega.md)) | E (desarrollo), O (despliegue, mantenimiento) | S1, se actualiza en cada sprint |
| 4.6.1 Buenas prácticas de conversión de prototipos a web UI/UX | Heurísticas de Nielsen, consistencia con el diseño de Odoo, accesibilidad (contraste), responsive, etiquetas en español | Texto | E | S3 |
| 4.6.2 Propuesta de prototipos web | Pantallas reales implementadas, con capturas por caso de uso (F1: pantallas estándar configuradas; F2: + pantallas propias) | Odoo + navegador | E | S3 (+F2) |
| 4.6.3 Prototipos de informes y reportes | Diseño y vista de: **F1:** factura/boleta `l10n_pe`, guía de despacho y orden de producción con el layout de la compañía. **F2:** + Certificado de calidad por lote (M1) y Liquidación de heladero (M2), en QWeb. La plantilla dice JasperReports; se usa **QWeb**, el motor nativo de Odoo, y se justifica | QWeb → PDF | E (liquidación), O (certificado) | S3 |
| 4.6.4 Optimización de rendimiento web (WPO) | Lighthouse antes/después (modo `debug=assets` contra producción + Nginx con gzip y caché); métricas LCP, TBT, CLS; tabla por vista | Lighthouse CLI / DevTools | E | S3 → Cierre |
| 4.7 Acuerdos de niveles de servicio: 4.7.1 Identificación de métricas clave | Tabla 14: métricas técnicas, de usuario, de negocio y otras | Tabla | E | S3 |
| 4.7.2 Definición de KPIs | Definición, fórmula, meta y fuente (F1: dashboards estándar y pivotes; F2: tablero OWL) | Tabla | E | S3 |
| 4.7.3 Definición y clasificación de acuerdos de servicio SLA | Tabla 15: disponibilidad, tiempo de respuesta, tiempo de resolución, RPO/RTO y soporte | Tabla | E | S3 |
| **5. Back-end y despliegue** | | | | |
| 5.1 Integración con la base de datos (intro) | Cómo Odoo mapea modelos a tablas (ORM) | Texto | O | S3 |
| 5.2 Organización de paquetes | Estructura de `donofrio_base` (`data/` por área, `security/`, `tests/`, hooks) y, en la F2, de cada módulo propio (`models/`, `views/`, `report/`, `static/src/`) | Captura del árbol | O | S3 (+F2) |
| 5.3 Organización de librerías | Inventario de dependencias del `__manifest__.py` | Captura | O | S3 |
| 5.4 Gestión de dependencias de comunicación | Gráfico de dependencias entre módulos | Script → Graphviz (`depends` de los manifests) | O | S3 |
| 5.5 Documentación de módulos backend (un "Módulo XXXXX" por módulo propio) | **F1: "Módulo donofrio_base"**: `post_init_hook` (localización), datos por área, `ir.rule`, script de transacciones, tests. **F2:** un apartado por módulo terminado (modelos, métodos clave: aprobar, liquidar, `get_kpis`) | Capturas de código | O (base, calidad), E (datos de su área, heladeros, tablero) | S3 (+F2) |
| 5.6 Arquitectura de desarrollo impulsado por patrones | MVC, TDD (tests escritos antes de la lógica de los compute), DAO (ORM), DTO, SOLID | Texto | O | S3 |
| 5.7 Diagramas de arquitectura del sistema | Diagramas C4 de contexto y de contenedores + diagrama de componentes | draw.io / PlantUML C4 | O | S3 |
| 5.8 Integración sistema - base de datos | Componentes front-end (OWL, QWeb), backend (ORM, workers) y BD (PostgreSQL primario y réplica) | draw.io | O | S3 |
| 5.9 Gestión de replicación | Primario y standby en *streaming* (física, asíncrona); scripts y evidencias: `pg_stat_replication`, `pg_is_in_recovery()`, dato escrito en el primario y leído en la réplica, escritura rechazada en la réplica | Docker + psql | O | S3 |
| 5.9b Gestión de administración de BD | Backups (`pg_dump -Fc` + filestore, retención de 7 días), restauración probada, VACUUM/ANALYZE, `pg_stat_statements`, roles (Odoo no corre como superusuario), índices de los modelos propios, cifrado en tránsito (TLS en Nginx) | Scripts + DBeaver | O | S3 → Cierre |
| 5.10 Gestión de seguridad de información: identificación de riesgos de seguridad | Tabla 16 | Tabla | O | S3 → Cierre |
| 5.11 Identificación de controles de seguridad | Tabla 17 + escalas | Tabla | O | S3 → Cierre |
| 5.12 Identificación de ataques y defensa | Tabla 18 (SQLi, XSS, fuerza bruta, gestor de BD expuesto, robo de sesión, pérdida de datos, caída) | Tabla + prueba con OWASP ZAP | O | S3 → Cierre |
| 5.13 Validación del servicio: validación y verificación de requerimientos de software, pruebas funcionales | Tablas 19, 20 (casos TC con estado) y 21 | Tests de Odoo + pruebas manuales | E (ventas, heladeros, gerencia), O (logística, producción, calidad) | S3 → Cierre |
| 5.14 Validación y verificación de requerimientos de software, pruebas no funcionales | Tablas 22, 23 y 24: carga (k6), seguridad (ZAP), WPO (Lighthouse), disponibilidad, respaldo | k6, ZAP, Lighthouse | O (carga, seguridad), E (WPO, usabilidad) | S3 → Cierre |
| 5.15 Despliegue: enfoque y herramientas utilizadas, mejores prácticas | URLs de publicación; enfoque *rolling* con un solo nodo + rollback por imagen etiquetada; ilustración 32 (pipeline CI/CD); tabla 25; mejores prácticas (monitoreo, backups, secretos) | GitHub Actions, Docker, GHCR | O | S3 → Cierre |
| 5.16 **Entradas huérfanas del índice** → **Gestión de servicios (ITIL 4 / ISO 20000-1)** | El índice de figuras y tablas lista BPMN de solicitudes de servicios, información y accesos, control de cambios de CI y capacidad (ilustraciones 33-37) y las tablas 26-38 (herramientas de control de cambios, capacidad, rendimiento, proyección de usuarios), pero **esas secciones no existen en el cuerpo**. Plan: un subapartado breve "Gestión de servicios" dentro de Despliegue, con 2 BPMN (control de cambios vía PR/CI y solicitud de acceso) y una tabla resumen de herramientas y capacidad. Antes, **consultar al docente** si las espera | bpmn.io + tablas | O | S3 → Cierre |
| **6. Documentación de la solución** | | | | |
| 6.1 Descripción del Scrum Team | Integrantes, roles y responsabilidades | Texto | E | S3 → Cierre |
| 6.2 Resumen del cuadro de sprints | Tabla por sprint: objetivo, HU, puntos planificados y completados, fechas, incremento, burndown | GitHub Projects (Insights) + `scripts/burndown.py` (lee `gh project item-list --format json`, por puntos) | E | S3 → Cierre |
| 6.3 Resumen del Monday | La sección se desarrolla con **GitHub Projects**, la herramienta de gestión del equipo, y lo dice en una línea bajo el título: es gratuita, está integrada con los issues, los PR y los commits, y el docente la ve sin invitación ([04 §4.11](04_scrum_pmbok.md)). Capturas de cada vista (Product Backlog, Sprint actual, Roadmap) y de Insights al cierre de cada sprint, y el issue "Dailies" | GitHub Projects | E | S3 → Cierre |
| 6.4 Resumen del GitHub o GitLab | URLs del repo, releases, Actions y paquete GHCR; capturas (ver [06 §6.6](06_github_ci_infra.md)) | GitHub | O | S3 → Cierre |
| 6.5 Ramificación o branching | Flujograma de ramas, esquema y listado de ramas | Mermaid gitGraph + capturas | O | S3 → Cierre |
| 6.6 Merge strategy | PR → revisión cruzada → *squash merge* a `develop`; *merge commit* de `develop` a `main` con tag | Capturas de PR | O | S3 → Cierre |
| 6.7 Resumen de commits | Convención, estadísticas por autor y capturas | GitHub Insights | E | S3 → Cierre |
| 6.8 Resumen de issues | Unos 25 issues: épicas por área con su checklist de HU, issues de gestión y bugs; etiquetas, milestones, cierre con `Closes #n` y prevención | GitHub Issues | E | S3 → Cierre |
| 6.9 Resumen de pruebas | Tabla consolidada: unitarias, integrales, usabilidad y seguridad × desarrollo, despliegue y mantenimiento | Tabla | E+O | S3 → Cierre |
| 6.10 Pruebas unitarias (desarrollo, despliegue, mantenimiento) | `TransactionCase` de `donofrio_base` (datos, seguridad) y de los módulos de la F2 que se terminen; en CI; *smoke test* post-despliegue; ejecución programada semanal | Odoo test runner + Actions | O | S3 (+F2) |
| 6.11 Pruebas integrales | **F1** (HU-33): pedido → entrega FEFO → factura; compra → recepción; OP → lote. **F2:** OP → inspección → bloqueo de despacho; liquidación → pedido | Odoo + Actions | O | S3 → Cierre |
| 6.12 Pruebas de usabilidad | Tareas cronometradas con 5 usuarios + cuestionario SUS | Google Forms | E | S3 → Cierre |
| 6.13 Pruebas de seguridad | ZAP baseline, pruebas de permisos (`AccessError`), política de contraseñas, `list_db=False` | ZAP, tests | O | S3 → Cierre |
| **7. Conclusiones** | Una por objetivo y por área | Texto | E+O | S3 → Cierre |
| **8. Recomendaciones** | Trabajo futuro: los módulos de la F2 que no se hayan terminado (con su diseño), EDI SUNAT vía OSE, app móvil para heladeros, plan para la transición a Froneri (migración de compañía) | Texto | E+O | S3 → Cierre |
| **9. Referencias y bibliografía** | APA 7: fuentes de [01](01_alcance_escenario.md), documentación de Odoo 19, Scrum Guide 2020, PMBOK/PMI, OWASP | Gestor de referencias de Word o Zotero | E | S3 → Cierre |
| **10. Anexos**: 10.1 RF (fichas como la tabla 39), 10.2 RNF (fichas como la tabla 40) | Una ficha por RF y RNF (las de RNF con su característica ISO 25010); anexos extra: actas Scrum, diccionario completo y manuales referenciados | Tablas | E (RF), O (RNF) | S2-S3 (+F2) |
| 10.3 a 10.5 Formatos ITIL | Solicitud de servicio o acceso, solicitud de cambio (RFC) y registro de incidente, cada uno con un ejemplo lleno ([09 §9.3](09_normas_marcos.md)) | Tablas | E (10.3, 10.5), O (10.4) | S3 → Cierre |
| 10.6 SoA ISO 27001 | Declaración de Aplicabilidad completa + política de seguridad de 1 página ([09 §9.8](09_normas_marcos.md)) | Tabla | O | S3 → Cierre |

La norma o marco que se demuestra en cada sección (ISO 27001, ITIL 4, COBIT, ISO 31000, ISO 25010, OWASP, ISO 22301, ISO 9001/HACCP, Ley 29733) está en [09_normas_marcos.md §9.1](09_normas_marcos.md).

### Criterio de "sección completa"

Una sección está completa cuando cumple todo esto:
- Tiene texto propio, no el texto de ejemplo de la plantilla.
- Cada figura y tabla tiene leyenda numerada.
- Las fuentes están citadas.
- Al menos una evidencia real del proyecto (captura, diagrama o tabla con datos reales).
- La revisó el otro integrante.

## 2.3 Secciones del informe que cambian según se llegue o no a la Fase 2

**Regla:** el informe siempre está completo con la Fase 1. Cada módulo de la F2 que se termina (y pasa su mini gate) **actualiza** las filas de esta tabla. Lo que no llega se marca como "Diseñado – trabajo futuro" y nunca se presenta como implementado. Con el plazo actual, el escenario más probable es **Fase 1 + M1**: conviene redactar primero las columnas "Solo Fase 1" y "M1".

| Sección | Solo Fase 1 (núcleo) | Si se termina M1 `donofrio_calidad` (+M3 frío) | Si se termina M2 `donofrio_heladeros` | Si se termina M4 `donofrio_tablero` |
|---|---|---|---|---|
| 3.2 / 4.1.4 Problemas y oportunidades (tabla 1) | Problemas 2, 5, 6 y 7: "resuelto"; 1, 3 y 4: "propuesta" | 4 (y 3 con M3): "resuelto" | 1: "resuelto" | 5: se refuerza |
| 4.1.2 BPMN TO-BE | Producción con controles en las instrucciones de las operaciones; heladeros con pedido + devolución estándar | TO-BE con inspección (y registro de temperatura) | TO-BE con liquidación | — |
| 4.2.2 RF (tabla 2) y anexo 10.1 | RF004, RF008, RF011 y RF012 en estado "Diseñado – trabajo futuro"; RF013 "Implementado (estándar)" | RF011 y RF012 (y RF008) "Implementado" | RF004 "Implementado" | RF013 "Implementado (propio)" |
| 4.2.4 Casos de uso | Todos los CU con su ficha; los de la F2 marcados como "propuesto" | CU de inspección (y temperatura) → implementado | CU de liquidación → implementado | CU del tablero → implementado |
| 4.2.5 Diagrama de clases | Dominio sobre los modelos de Odoo + `donofrio_base`; clases de la F2 como "propuesto" (estereotipo `<<propuesto>>`) | `donofrio.calidad.*` (y `donofrio.temperatura`) implementadas | `donofrio.liquidacion*` implementadas | Clase de servicio de KPIs |
| 4.2.6-4.2.8 ER, diseño lógico, diccionario | Tablas del núcleo (unas 30) | + tablas `donofrio_calidad_*` (+ temperatura) | + `donofrio_liquidacion*` | Sin tablas nuevas |
| 4.4 Wireframes y mockups | **Iguales en los dos casos**: se diseñan en S2 para todas las pantallas | — | — | — |
| 4.6.2 Prototipos web | Pantallas estándar configuradas | + inspección y temperatura | + liquidación (incluida la vista móvil) | + tablero |
| 4.6.3 Reportes | Factura/boleta, guía, OP con el layout de la compañía | + Certificado de calidad | + Liquidación del heladero | — |
| 4.6.4 WPO | Login, backend y dashboard estándar | — | — | + tablero OWL (antes/después) |
| 4.7 KPIs / SLA | KPIs desde dashboards y pivotes | + % de lotes aprobados (+ alertas de temperatura) | + merma de heladeros, liquidaciones pendientes | KPIs centralizados en el tablero |
| 5.2-5.4 Paquetes, librerías, dependencias | `donofrio_base` + OCA + dependencias del core | + módulo | + módulo | + módulo (OWL, Chart.js) |
| **5.5 Documentación de módulos backend** | **"Módulo donofrio_base"** (hook de localización, datos por área, `ir.rule`, script, tests) | + "Módulo donofrio_calidad" | + "Módulo donofrio_heladeros" | + "Módulo donofrio_tablero" |
| 5.6-5.8 Patrones, arquitectura, integración | MVC sobre el ORM, herencia de `donofrio_base`, TDD en los tests de integración | + TDD de los cálculos y estados | + idem | + componente OWL (front-end) |
| 5.13 Pruebas funcionales (tablas 19-21) | Casos TC de los RF de la F1; RF de la F2 con estado "No ejecutado – fuera del alcance entregado" | + TC de RF011, RF012 (RF008) | + TC de RF004 | + TC de RF013 propio |
| 6.10-6.11 Pruebas unitarias e integrales | Tests de `donofrio_base` (HU-04, HU-33) | + tests del módulo | + tests del módulo | + test de `get_kpis` |
| 6.2 Cuadro de sprints y 6.4-6.8 GitHub | Tag `v1.0.0` + Gate 0 | + `v1.1.0` (+ `v1.3.0` con M3) + mini gate | + `v1.2.0` | + `v1.4.0` |
| 9 normas ([09](09_normas_marcos.md)): ISO 9001 / HACCP | Trazabilidad por lote, FEFO, fecha de retiro, PCC documentados en las operaciones | + liberación y no conformes; + monitoreo de PCC de temperatura | — | — |
| 7-8 Conclusiones y recomendaciones | Los módulos de la F2 no hechos pasan a trabajo futuro | Se quita de trabajo futuro | Idem | Idem |
| Presentación | Variante "Solo Fase 1" ([05 §5.4](05_reparto_equipo.md)) | Demo 2 con inspección | Demo 1 con liquidación | Demo 1 con tablero |
