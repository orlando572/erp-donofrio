# 9. Normas y marcos de referencia

[← Índice](PLAN_PROYECTO.md)

> **Frase obligatoria en el informe** (sección 4.3 o 5.10): *"El proyecto se **alinea** con las normas y marcos citados como buenas prácticas de referencia. No constituye una implementación certificada ni auditada de ninguno de ellos; la Declaración de Aplicabilidad y las evidencias tienen fines académicos."*

**Principio:** pocas normas bien demostradas.
- **Núcleo** (las del curso), demostradas a fondo con evidencia: **ISO/IEC 27001:2022 + 27002**, **ITIL 4** y **COBIT 2019**.
- **De apoyo**, cada una con una sola tabla o párrafo y su evidencia: ISO 31000, ISO 20000-1, ISO/IEC 25010, OWASP Top 10, ISO 22301, ISO 9001 + HACCP/ISO 22000 y la Ley 29733.
- **No se agregan** NIST CSF, PCI DSS, ISO 27701 ni CMMI. TOGAF es opcional y solo aporta las capas de la arquitectura.

**Numeración:** se usa la de [02_mapeo_plantilla.md](02_mapeo_plantilla.md), en la que la sección 6.4 es "Resumen del GitHub". Equivalencias aproximadas con la numeración corta que usa el pedido de esta sección:

| Pedido | Plan |
|---|---|
| 1 | 3 Aspectos generales |
| 2.x | 4.x Planificación y Front-end |
| 3.x | 5.x Back-end y Despliegue |

Para evitar ambigüedades, cada fila lleva también el **nombre** de la sección.

## 9.1 Mapeo de cada norma o marco a la plantilla

| Norma / marco | Qué se toma (y solo eso) | Sección de la plantilla donde se demuestra | Resp. |
|---|---|---|---|
| **ISO/IEC 27001:2022 Anexo A + ISO/IEC 27002:2022** | Unos 20 controles del Anexo A (93 controles en 4 temas: organizacionales 5.x, personas 6.x, físicos 7.x y tecnológicos 8.x); SoA reducida (9.4) | **5.10** Identificación de riesgos de seguridad · **5.11** Controles de seguridad (+ SoA) · **5.12** Ataques y defensa · Anexo **10.6** SoA completa | O |
| **ISO 31000:2018** | Proceso: contexto → identificación → análisis (probabilidad × impacto) → evaluación → tratamiento → seguimiento, con comunicación y consulta | **4.5** Gestión de riesgos (plan, escalas 1-3, matrices por etapa) · también da el método de 5.10 | E |
| **ITIL 4** (5 prácticas) | **Gestión de solicitudes de servicio**, **habilitación del cambio**, **gestión de capacidad y desempeño**, **gestión de niveles de servicio** y **gestión de incidentes** | **4.3.3** Configuración de herramientas: despliegue, mantenimiento y monitoreo · **4.7** ANS (métricas, KPIs, SLA) · **5.15/5.16** Despliegue y gestión de servicios (cubre las entradas huérfanas del índice: BPMN de solicitudes, control de cambios y capacidad; tablas 26-38) · **6.8** Resumen de issues · Anexos **10.3-10.5** (formatos) | E (SLA, solicitudes, incidentes), O (cambios, capacidad) |
| **ISO/IEC 20000-1:2018** (complemento de ITIL) | Requisitos que respaldan las 5 prácticas: gestión de niveles de servicio, cambios, incidentes, solicitudes, capacidad y disponibilidad/continuidad (cláusulas 8.3-8.7; **verificar la numeración exacta con el texto de la norma**) | Columna "Requisito ISO 20000-1" en las tablas de 4.7 y 5.16 | E |
| **COBIT 2019** | Cascada de metas (necesidades de los interesados → metas empresariales EG → metas de alineamiento AG → objetivos de gestión) y 11 objetivos: APO09, APO12, APO13, BAI03, BAI06, DSS01, DSS02, DSS03, DSS04, DSS05 y MEA01 | **3.6** Estrategia empresarial y **3.7** Planificación empresarial (cascada) · **4.1.3** Análisis de arquitectura empresarial (objetivos que soporta el ERP) · **6.2** Cuadro de sprints (MEA01: seguimiento del desempeño) | E (cascada), O (arquitectura) |
| TOGAF 10 (opcional) | Solo las 4 capas (negocio, datos, aplicación, tecnología) para ordenar la arquitectura AS-IS y TO-BE | **4.1.3** | O |
| **ISO/IEC 25010:2023** | Modelo de calidad del producto (9 características) como **clasificación de los RNF** y de sus pruebas | **4.2.3** RNF (columna "Característica 25010") · **5.14** Pruebas no funcionales · Anexo **10.2** fichas RNF | O |
| **OWASP Top 10** (edición 2021; usar la 2025 si ya es versión final a la fecha de entrega) | Las 10 categorías como lista de ataques a defender | **5.12** Identificación de ataques y defensa · **6.13** Pruebas de seguridad (ZAP) | O |
| **ISO 22301:2019** | BIA mínimo (procesos críticos, RPO y RTO), estrategia de continuidad (réplica + respaldos) y ejercicio (restauración y promoción de la réplica) | **5.9** Gestión de replicación · **5.9b** Administración de BD (respaldos) · **4.7.3** SLA (RPO/RTO) | O |
| **ISO 9001:2015 + HACCP (Codex) / ISO 22000:2018** | ISO 9001: identificación y trazabilidad, liberación de productos, control de salidas no conformes. HACCP: puntos críticos de control (PCC), límites críticos, monitoreo, acciones correctivas, registros | **3.2** Descripción del problema (contexto de inocuidad) · **4.1.2** BPMN de producción y calidad · **5.5** Documentación del módulo `donofrio_calidad` · justificación de RF008, RF011, RF012 y RNF005 | O |
| **Ley 29733** (Protección de Datos Personales, Perú) y su reglamento vigente (verificar si es el **D.S. 016-2024-JUS**, que reemplazó al D.S. 003-2013-JUS) | Principios de finalidad, proporcionalidad y seguridad; datos de clientes (DNI/RUC) y empleados | **3.2** Supuestos (datos ficticios) · **4.2.3** RNF013 · **5.11** control 5.34 de la SoA | E |

## 9.2 Cómo se demuestra cada control en Odoo 19 Community

Todo lo que aparece aquí se **verificó en la rama 19.0** de `github.com/odoo/odoo` el 22/11/2026: los módulos existen y tienen licencia **LGPL-3** (Community). La configuración se carga **por código** en `donofrio_base`, con `ir.config_parameter` y datos XML, y no a mano.

| # | Control (ISO 27001 Anexo A) | Mecanismo en Odoo 19 / infraestructura | Cómo se configura (por código) | Evidencia concreta |
|---|---|---|---|---|
| 1 | **5.15** Control de acceso · **5.18** Derechos de acceso · **8.3** Restricción de acceso a la información (**mínimo privilegio**) | `res.groups` (en 19, con `privilege_id` → `res.groups.privilege`), `ir.model.access` (CRUD por modelo y grupo), `ir.rule` (filtro por registro) | `security/donofrio_security.xml` en cada módulo propio: grupos "Calidad / Inspector" y "Calidad / Jefe", "Heladeros / Liquidador" y "Heladeros / Supervisor"; `ir.model.access.csv`; `ir.rule`: el liquidador solo ve sus liquidaciones y solo el jefe de calidad aprueba. 10 usuarios por rol con `group_ids` | **Test** `tests/test_seguridad.py`: `with_user(vendedor)` → `AccessError` al leer inspecciones (corre en CI). **Captura** de la pantalla de permisos de un usuario y del mensaje de acceso denegado. **Archivo** `ir.model.access.csv` |
| 2 | **8.5** Autenticación segura · **8.2** Accesos privilegiados | `auth_totp` (2FA TOTP con app de autenticación); `auth_totp_mail` (invitación y política `auth_totp.policy` = `employee_required` / `all_required`); bloqueo por intentos fallidos nativo de `base`: `base.login_cooldown_after` (5 por defecto) y `base.login_cooldown_duration` (60 s por defecto) | `depends: ['auth_totp', 'auth_totp_mail']`; 2FA activado para el administrador y la gerencia; los parámetros de *cooldown* se fijan por XML | **Captura** del enrolamiento con QR y del login que pide el código. **Log** de Odoo con el bloqueo después de 5 intentos fallidos. **Test** del parámetro configurado |
| 3 | **5.17** Información de autenticación | `auth_password_policy` (parámetro `auth_password_policy.minlength`; Odoo guarda las contraseñas con *hash* PBKDF2) | `ir.config_parameter` `auth_password_policy.minlength = 12` | **Captura** del cambio de contraseña rechazado ("debe tener al menos 12 caracteres"). **Test**: `_check_password_policy` lanza error con una contraseña corta. **Consulta SQL** que muestra que `res_users.password` está *hasheada* |
| 4 | **8.15** Registro (*logging*) · **8.16** Monitoreo | `mail.thread` + `tracking=True` (chatter con el historial de cambios: quién, cuándo, valor anterior y nuevo); `res.users.log` (registro de inicios de sesión, en `base`); opcional: OCA `auditlog` 19.0 para modelos del core como precios y productos; `/web/health` + Uptime Kuma | Los modelos propios heredan `['mail.thread', 'mail.activity.mixin']` con `tracking=True` en estado, resultado, cantidades e importes | **Captura** del chatter de una inspección (rechazada → aprobada, con usuario y hora). **Consulta** a `res_users_log`. **Captura** de Uptime Kuma |
| 5 | **8.13** Respaldo · **8.14** Redundancia (+ **ISO 22301**) | `scripts/backup.sh`: `pg_dump -Fc` + tar del *filestore*, retención de 7 días, programado con cron (host o contenedor); réplica *streaming* (`db-replica`) | Cron diario a las 02:00; copia fuera del servidor (carpeta sincronizada o artefacto) | **Listado** de respaldos con fecha y tamaño. **Log** de `restore.sh` restaurando en una BD nueva, con el **RTO medido**. **Captura** de `pg_stat_replication` y `pg_is_in_recovery()` |
| 6 | **8.24** Uso de criptografía · **8.20** Seguridad de redes | Nginx con TLS 1.2/1.3, redirección 80 → 443 y HSTS; `proxy_mode = True`; PostgreSQL no expuesto fuera de la red de Docker en "prod" | `docker/nginx/odoo.conf` + perfil `proxy` | **Captura** del candado del navegador y del certificado. **Salida** de `curl -I https://…` (cabecera HSTS) y `openssl s_client` (versión TLS). **Archivo** de configuración de Nginx |
| 7 | **8.31** Separación de entornos · **8.32** Gestión de cambios · **8.25** Ciclo de desarrollo seguro · **8.9** Gestión de configuración | Entornos **dev** (PC, `workers=0`, cinta "DESARROLLO" con OCA `web_environment_ribbon`), **test** (CI efímero en Actions) y **prod** (perfil `proxy`, `list_db=False`, `admin_passwd` desde un secreto, sin modo debug); cambios solo por PR revisado + CI en verde; infraestructura como código (Compose y Dockerfile versionados) | `.env.dev` / `.env.prod` (no versionados; `.env.example` sí); protección de ramas en GitHub | **Captura** de la cinta en dev frente a prod sin cinta. **Captura** de las reglas de protección de rama. **PR** con revisión y checks en verde. **Commit** del Dockerfile y el Compose |
| 8 | **8.8** Vulnerabilidades técnicas · **8.29** Pruebas de seguridad | Dependabot (Actions y Docker), imagen de Odoo fijada, OWASP ZAP baseline | `.github/dependabot.yml`; `scripts/perf/zap.sh` | **Reporte HTML** de ZAP. **PR** de Dependabot |
| 9 | **5.34** Privacidad y protección de datos personales (**Ley 29733**) | Campos privados de empleados restringidos al grupo de RR. HH. (Odoo los protege con `groups`); datos ficticios y mínimos; sin datos sensibles | Datos de `donofrio_base` revisados; ningún campo extra de datos sensibles | **Captura**: un vendedor no ve los datos privados de un empleado. **Párrafo** de cumplimiento en 3.2 |

## 9.3 ITIL 4: tickets en Community

**El problema:** la app **Helpdesk es Enterprise**. Se verificó que `addons/helpdesk` no existe en la 19.0 de Community.

**La solución** usa dos herramientas, sin código nuevo:

| Uso | Herramienta | Configuración (por código en `donofrio_base`) | Práctica ITIL |
|---|---|---|---|
| **Mesa de servicios TI** para los usuarios del ERP (personal de D'Onofrio) | App **Project** de Odoo (Community, LGPL-3): proyecto "Mesa de Servicios TI" | Etapas (`project.task.type`): Nuevo → En análisis → En atención → Resuelto → Cerrado (plegada). Etiquetas por tipo: *Incidente*, *Solicitud de servicio*, *Solicitud de acceso*. Prioridad (estrellas). Fecha límite = objetivo del SLA según prioridad. Asignado = resolutor. Actividades para escalar | Gestión de incidentes, gestión de solicitudes de servicio y gestión de niveles de servicio (la vista pivote de tareas por etapa y prioridad mide el cumplimiento del SLA) |
| **Gestión de cambios y problemas** del software | **GitHub Issues** con plantillas: `solicitud_cambio.yml` (RFC: motivo, impacto, riesgo, plan de *rollback*, aprobador), `bug.yml` (incidente técnico o problema) | Etiquetas `tipo:cambio-normal`, `tipo:cambio-estandar`, `tipo:cambio-emergencia`; el PR enlazado es la implementación; el CI y la revisión hacen de **autoridad de cambio** | Habilitación del cambio: RFC → evaluación (revisión del PR) → autorización (aprobación) → implementación (merge) → verificación (CI y *smoke test*) → cierre (release) |
| **Capacidad y desempeño** | k6 + `pg_stat_statements` + `docker stats` + Uptime Kuma | `scripts/perf/` | Gestión de capacidad y desempeño: tabla de proyección de usuarios (heladeros en verano frente a invierno) y umbrales |

**Anexos nuevos** (los formatos que pide el pedido). Cada uno trae el formulario y un ejemplo lleno con un caso de D'Onofrio:

| Anexo | Formato | Ejemplo lleno |
|---|---|---|
| **10.3** | Solicitud de servicio o de acceso: solicitante, área, tipo, justificación, aprobador, rol solicitado, fecha y SLA | "Alta de un liquidador para la temporada de verano en el CD Arequipa" |
| **10.4** | Solicitud de cambio (RFC): ID, descripción, motivo, tipo (estándar, normal o emergencia), impacto, riesgo, plan de pruebas, plan de *rollback*, aprobación, PR y release | "Agregar el campo de merma por zona a la liquidación" |
| **10.5** | Registro de incidente: ID, fecha y hora, reportante, servicio afectado, impacto × urgencia → prioridad, diagnóstico, solución, tiempo de resolución frente al SLA y causa raíz (→ problema) | "Tablero gerencial no carga" |

Matriz de prioridad (impacto × urgencia) y SLA por prioridad. Es la misma tabla de 4.7.3, con la columna "Requisito ISO 20000-1":

| Prioridad | Respuesta | Resolución |
|---|---|---|
| P1 Crítica | 30 min | 4 h |
| P2 Alta | 2 h | 8 h |
| P3 Media | 8 h | 3 días |
| P4 Baja | 1 día | 5 días |

## 9.4 COBIT 2019: cascada de metas (para 3.6, 3.7 y 4.1.3)

| Necesidad del interesado (gerencia de D'Onofrio) | Meta empresarial (EG) | Meta de alineamiento (AG) | Objetivos de gestión | Cómo lo atiende el proyecto |
|---|---|---|---|---|
| Integrar ventas, almacén y producción, y liquidar heladeros sin errores | EG08 Optimización de la funcionalidad de los procesos internos | AG08 Habilitar y soportar los procesos integrando aplicaciones y tecnología | **BAI03** Gestionar la identificación y construcción de soluciones | Módulos estándar + 4 módulos propios, construidos con Scrum |
| Que el sistema esté disponible en temporada alta | EG06 Continuidad y disponibilidad del servicio | AG05 Entrega de servicios de I&T alineada con el negocio | **APO09** Acuerdos de servicio · **DSS01** Operaciones · **DSS04** Continuidad | SLA (4.7), monitoreo, réplica y respaldos |
| Proteger la información de clientes y la operación | EG02 Riesgo de negocio gestionado · EG03 Cumplimiento de leyes externas | AG02 Riesgo de I&T gestionado · AG07 Seguridad de la información y privacidad · AG01 Cumplimiento | **APO12** Riesgo · **APO13** Seguridad · **DSS05** Servicios de seguridad | ISO 31000 (4.5), ISO 27001 + SoA (5.10-5.12), Ley 29733 |
| Cambiar el sistema sin romper la operación | EG08 | AG06 Agilidad para convertir requerimientos en soluciones operativas | **BAI06** Cambios de TI · **DSS02** Solicitudes e incidentes · **DSS03** Problemas | PR + CI + releases; mesa de servicios en Project; issues |
| Decidir con datos | EG07 Calidad de la información de gestión | AG10 Calidad de la información de gestión de I&T | **MEA01** Supervisar el desempeño y la conformidad | Tablero gerencial de KPIs, burndown y métricas de SLA |

Se demuestra con dos tablas: la cascada (arriba) en 3.6-3.7 y un mapa "objetivo COBIT → componente del ERP o de la infraestructura" en 4.1.3. **No se hace** evaluación de capacidad ni de madurez: queda fuera de alcance.

## 9.5 ISO/IEC 25010:2023 aplicada a los RNF (columna nueva en 4.2.3 y 5.14)

| Característica 25010:2023 | RNF | Prueba |
|---|---|---|
| Adecuación funcional | (los RF) | Pruebas funcionales (5.13) |
| Eficiencia de desempeño | RNF002, RNF008 | k6, Lighthouse |
| Compatibilidad | RNF001 | 3 navegadores |
| Capacidad de interacción (antes "usabilidad") | RNF003 | SUS + tareas |
| Fiabilidad | RNF006, RNF011 | Restauración, réplica, *uptime* |
| Seguridad | RNF009, RNF010, RNF013 | ZAP, tests de acceso |
| Mantenibilidad | RNF007 | CI, lint, cobertura de tests |
| Flexibilidad (antes "portabilidad") | RNF012 | Instalación limpia con un comando |
| Protección (*safety*, nueva en 2023) | RNF004, RNF005 | Un lote rechazado o vencido no se despacha (inocuidad del consumidor) |

## 9.6 OWASP Top 10 → tabla 18 "Ataque y defensa" (5.12)

| Id | Categoría (2021) | Defensa en el proyecto | Prueba |
|---|---|---|---|
| A01 | Control de acceso roto | Grupos + ACL + `ir.rule`; ningún método público sin `check_access` o `@api.private` | `test_seguridad.py` |
| A02 | Fallas criptográficas | HTTPS/HSTS; contraseñas con *hash* PBKDF2 (nativo) | `curl -I`, consulta SQL |
| A03 | Inyección (SQL, XSS) | Solo el ORM (sin SQL crudo; si hace falta, `odoo.tools.SQL`); QWeb `t-out` escapa el contenido | ZAP + intento de `' OR '1'='1` en la búsqueda |
| A04 | Diseño inseguro | Matriz de riesgos y revisión de PR | Revisión |
| A05 | Mala configuración | `list_db=False`, `admin_passwd` fuerte desde un secreto, sin debug en prod, cabeceras en Nginx | ZAP, captura de `/web/database/manager` bloqueado |
| A06 | Componentes vulnerables | Imagen y commits de OCA fijados; Dependabot | PR de Dependabot |
| A07 | Fallas de autenticación | 2FA, política de contraseñas, *cooldown* después de 5 intentos | Log y captura |
| A08 | Integridad de software y datos | CI obligatorio, ramas protegidas, imágenes en GHCR por tag | Actions |
| A09 | Fallas de registro y monitoreo | Chatter/tracking, `res_users_log`, Uptime Kuma | Capturas |
| A10 | SSRF | No aplica: los módulos propios no hacen peticiones salientes a URLs del usuario (se justifica) | — |

## 9.7 ISO 9001 + HACCP / ISO 22000: justificación del módulo de calidad y la cadena de frío

| Requisito | Dónde se ve en el ERP |
|---|---|
| ISO 9001: identificación y trazabilidad | Lote por OP (`stock.lot`) con vencimiento; trazabilidad de la OP al cliente (RNF004) |
| ISO 9001: liberación de productos | Inspección **aprobada** = lote liberado; certificado QWeb del lote (RF012) |
| ISO 9001: control de salidas no conformes | Lote **rechazado** → no se puede despachar (RNF005) |
| HACCP: PCC y límites críticos | **F1:** PCC documentados en las instrucciones de las operaciones de la BoM. **F2-M1/M3:** puntos de control de `donofrio_calidad`: **pasteurización 80-85 °C** y **almacenamiento ≤ −18 °C** como PCC (supuesto S5) |
| HACCP: monitoreo, acción correctiva y registros | `donofrio.temperatura` (registro) → fuera de rango → actividad para el jefe de almacén (acción correctiva) → historial en el chatter (registro) |
| ISO 22000: trazabilidad y retiro | FEFO + búsqueda de lotes por vencimiento; el *cron* avisa de los lotes por vencer |

En Perú, la vigilancia sanitaria de alimentos la ejerce DIGESA y existe una norma sanitaria para aplicar HACCP (citar con la referencia exacta después de verificarla; se cree que es la R.M. 449-2006/MINSA).

## 9.8 Declaración de Aplicabilidad (SoA) reducida: ISO/IEC 27001:2022 Anexo A

En 5.11 va un resumen de unos 20 controles; la SoA completa va en el Anexo 10.6. Los temas que **no aplican** se justifican en bloque:
- **7.x Físicos:** proyecto académico sin instalaciones propias; se depende del host o la nube.
- **6.x Personas:** equipo de 2 personas, salvo 6.3 en forma de "inducción en el manual".

| Control | Aplica | Justificación | Implementación (§9.2 #) | Estado |
|---|---|---|---|---|
| 5.1 Políticas de seguridad | Parcial | Se necesita un marco mínimo | Política de seguridad de 1 página (anexo) | Implementado |
| 5.15 Control de acceso | Sí | Datos de varias áreas | #1 | Implementado |
| 5.17 Información de autenticación | Sí | Hay usuarios internos | #3 | Implementado |
| 5.18 Derechos de acceso | Sí | Mínimo privilegio | #1 + mesa de servicios (solicitud de acceso) | Implementado |
| 5.19-5.22 Proveedores | Parcial | Se depende de GitHub, Docker Hub y OCA | Versiones fijadas; listado de proveedores | Parcial |
| 5.24-5.26 Gestión de incidentes | Sí | Continuidad operativa | Mesa de servicios en Project + Anexo 10.5 | Implementado |
| 5.29 / 5.30 Continuidad / preparación de las TIC | Sí | Temporada alta crítica | #5 (ISO 22301) | Implementado |
| 5.34 Privacidad y datos personales | Sí | Ley 29733 | #9 | Implementado |
| 5.37 Procedimientos operativos documentados | Sí | Reproducibilidad | Manual de instalación y de herramientas | Implementado |
| 6.3 Concienciación y formación | Parcial | Equipo pequeño | Sección de seguridad en el manual | Parcial |
| 7.1-7.14 Físicos | No | Sin instalaciones propias (académico) | — | Excluido |
| 8.2 Derechos de acceso privilegiado | Sí | Administrador de Odoo y de PostgreSQL | #2; Odoo no corre como superusuario de PostgreSQL | Implementado |
| 8.3 Restricción de acceso a la información | Sí | Liquidaciones y calidad | #1 (`ir.rule`) | Implementado |
| 8.5 Autenticación segura | Sí | Acceso web | #2 | Implementado |
| 8.8 Vulnerabilidades técnicas | Sí | Dependencias de terceros | #8 | Implementado |
| 8.9 Gestión de configuración | Sí | Infraestructura como código | #7 | Implementado |
| 8.13 Respaldo de información | Sí | Pérdida de datos | #5 | Implementado |
| 8.14 Redundancia | Sí | Disponibilidad | #5 (réplica) | Implementado |
| 8.15 Registro (*logging*) | Sí | Auditoría | #4 | Implementado |
| 8.16 Actividades de monitoreo | Sí | SLA | #4 (Uptime Kuma) | Implementado si se hace la opcional 17; si no, Parcial |
| 8.20 / 8.24 Redes / criptografía | Sí | Credenciales en tránsito | #6 | Implementado |
| 8.25 / 8.28 Desarrollo y codificación seguros | Sí | Hay código propio | CI, lint, ORM, revisión de PR | Implementado |
| 8.29 Pruebas de seguridad | Sí | Validar los controles | #8 (ZAP) + tests | Implementado |
| 8.31 Separación de entornos | Sí | Evitar cambios directos en prod | #7 | Implementado |
| 8.32 Gestión de cambios | Sí | Estabilidad | #7 + RFC (Anexo 10.4) | Implementado |

## 9.9 Trazabilidad: norma → control → evidencia

Esta tabla va en el informe, en 5.11 o como anexo. Cada evidencia se guarda en `docs/capturas/normas/` con el nombre `<norma>_<control>_<descripcion>.png`, o se enlaza al archivo o commit.

| Norma / marco | Requisito o práctica | Control implementado | Evidencia (tipo: ubicación) |
|---|---|---|---|
| ISO 27001 A.5.15 / A.8.3 | Control de acceso y mínimo privilegio | Grupos + `ir.model.access` + `ir.rule` | Archivo: `addons/*/security/`; test: `test_seguridad.py` (log del CI); captura: acceso denegado |
| ISO 27001 A.8.5 | Autenticación segura | `auth_totp` + `auth_totp_mail` + *cooldown* | Captura: QR y pantalla del código; log: bloqueo |
| ISO 27001 A.5.17 | Información de autenticación | `auth_password_policy` (minlength 12) | Captura: rechazo; archivo: `data/ir_config_parameter.xml` |
| ISO 27001 A.8.15 | Registro | Chatter `tracking=True`, `res.users.log` | Captura: chatter de inspección y liquidación; consulta SQL |
| ISO 27001 A.8.13 + ISO 22301 | Respaldo y continuidad | `backup.sh` / `restore.sh` + cron | Archivo: scripts; captura: listado de respaldos; log: restauración con RTO |
| ISO 27001 A.8.14 + ISO 22301 | Redundancia | Réplica *streaming* | Captura: `pg_stat_replication`, `pg_is_in_recovery()` |
| ISO 27001 A.8.24 | Criptografía | Nginx TLS + HSTS | Archivo: `docker/nginx/odoo.conf`; captura: certificado; salida de `curl -I` |
| ISO 27001 A.8.31 / A.8.32 · ITIL habilitación del cambio · COBIT BAI06 | Separación de entornos y gestión de cambios | Perfiles dev/prod, cinta de entorno, PR + CI, plantilla de RFC | Captura: protección de rama, PR aprobado con checks; commit: merge de la release; Anexo 10.4 |
| ISO 27001 A.8.29 · OWASP Top 10 | Pruebas de seguridad | ZAP baseline + tests de acceso | Archivo: reporte HTML de ZAP; Actions |
| ITIL incidentes y solicitudes · COBIT DSS02 · ISO 20000-1 | Registrar y resolver dentro del SLA | Mesa de servicios en Project | Captura: Kanban de tickets por etapa; pivote de cumplimiento del SLA; Anexos 10.3 y 10.5 |
| ITIL niveles de servicio · COBIT APO09 | SLA definidos y medidos | Tabla de SLA + Uptime Kuma | Tabla 15; captura: *uptime* |
| ITIL capacidad y desempeño | Capacidad para la temporada alta | k6 + proyección de usuarios | Archivo: reporte de k6; tabla de proyección |
| ISO 31000 · COBIT APO12 | Riesgos evaluados y tratados | Matriz I × P + vista "Riesgos" del GitHub Project | Tablas 10-13; captura de la vista |
| ISO 25010 | Calidad del producto | RNF clasificados y probados | Tablas 22-24 con la columna 25010 |
| ISO 9001 / HACCP / ISO 22000 | Trazabilidad (F1); liberación, no conformes, PCC, registros (F2) | F1: lotes, FEFO, fecha de retiro. F2: `donofrio_calidad` (inspecciones, temperaturas, bloqueo de despacho) | Test: lote rechazado no despacha; captura: certificado QWeb, alerta de temperatura |
| Ley 29733 · ISO 27001 A.5.34 | Protección de datos personales | Datos ficticios, campos privados restringidos | Captura: vendedor sin acceso a datos privados; párrafo en 3.2 |
| COBIT MEA01 | Supervisión del desempeño | Tablero de KPIs + burndown | Captura del tablero; gráfico de burndown |

## 9.10 Impacto en el backlog y el reparto

Se mantiene la simplicidad: solo se agrega **una** HU de configuración y se precisan dos existentes.

| Cambio | Detalle | Pts | Sprint | Resp. |
|---|---|---|---|---|
| **HU-32 (nueva, Fase 1)** | Como **responsable de TI**, quiero una mesa de servicios en Project (etapas, tipos de ticket ITIL, prioridad con fecha límite de SLA) para registrar incidentes y solicitudes. Criterios: proyecto y etapas cargados por código; 5 tickets de ejemplo; pivote de cumplimiento del SLA | 2 | S3 | E |
| HU-27 (precisión) | Se agregan `auth_password_policy` (minlength 12), parámetros de *cooldown*, `auth_totp_mail` con política para el administrador y la gerencia, y `test_seguridad.py` | (sin cambio: 5) | S3 (Fase 1) | O |
| HU-04 (precisión) | Grupos de 19.0 con `privilege_id` + `ir.rule` del CD Arequipa (F1); las `ir.rule` del liquidador y del inspector llegan con M1 y M2 (F2) | (sin cambio: 3) | S1 | O |
| DOC (nuevas tareas) | Cascada COBIT (3.6-3.7) y prácticas ITIL + anexos 10.3-10.5 → **E**; SoA, trazabilidad, OWASP, columna 25010, ISO 22301 y HACCP → **O** | — | S3 (Fase 1) | E / O |

Todos los controles de seguridad de §9.2 son de la **Fase 1**: no dependen de módulos propios. Los grupos "Calidad / …" y "Heladeros / …" de la fila #1 se agregan solo si llegan M1 y M2. Total del backlog: ver [04 §4.4](04_scrum_pmbok.md) (F1 = 83 puntos, F2 = 37).
