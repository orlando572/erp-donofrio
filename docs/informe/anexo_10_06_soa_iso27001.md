# Anexo 10.6 Declaración de Aplicabilidad (SoA) ISO/IEC 27001:2022 y política de seguridad

> **Estado:** borrador del Sprint 3 · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [09 §9.2, §9.8 y §9.9](../plan/09_normas_marcos.md), [02 §2.2](../plan/02_mapeo_plantilla.md) (fila 10.6), [5.10 a 5.12](05_10_a_05_12_seguridad.md), [5.13 y 5.14](05_13_a_05_14_pruebas.md), [6.4 a 6.6](06_04_a_06_06_repositorio.md), [6.9 a 6.13](06_09_a_06_13_pruebas.md)
>
> Mide el **estado real de `develop` al 23/11/2026** (`1e303ed`). Los riesgos (RSI-xx) y los controles (C-xx) de [5.10 a 5.12](05_10_a_05_12_seguridad.md) **no se repiten**: aquí se les asigna el control del Anexo A que cubren y se usan sus resultados como evidencia.
>
> *El proyecto se **alinea** con las normas y marcos citados como buenas prácticas de referencia. No constituye una implementación certificada ni auditada de ninguno de ellos; la Declaración de Aplicabilidad y las evidencias tienen fines académicos.*

---

# Parte A. Política de seguridad de la información (1 página)

**Documento ficticio pero coherente con el proyecto** · Organización: equipo del ERP académico «D'Onofrio» (UTP Arequipa) · Versión 1.0 · 23/11/2026 · Aprueban: Orlando (Scrum Master) y Evelyn (Product Owner)

**1. Objetivo y alcance.** Proteger la confidencialidad, la integridad y la disponibilidad de la información del ERP de D'Onofrio (Odoo 19.0 Community y PostgreSQL 16 en Docker), de su código y de su infraestructura como código en GitHub. Alcance: el sistema desplegado (Nginx, Odoo, PostgreSQL y su réplica), el repositorio `orlando572/erp-donofrio`, el CI y los respaldos. **Fuera del alcance:** instalaciones físicas, equipos personales de los integrantes, redes de la universidad y datos reales de D'Onofrio (todos los datos son ficticios).

**2. Activos que se protegen.** Datos del negocio (pedidos, clientes, lotes, precios, facturas), cuentas de usuario y permisos, base de datos y *filestore*, servicio web, código e imágenes (activos y riesgos en [5.10](05_10_a_05_12_seguridad.md)).

**3. Roles.**

| Rol | Persona | Responsabilidad de seguridad |
|---|---|---|
| **Responsable de seguridad y de TI** | Orlando (Scrum Master) | Mantiene los controles técnicos (acceso, TLS, respaldos, CI), la SoA y la gestión de cambios; es el único con rol de administrador del repositorio |
| **Responsable de la información** | Evelyn (Product Owner) | Decide quién accede a qué (por área y rol), acepta los riesgos residuales y revisa los cambios del otro integrante |
| **Usuarios** | Los 10 roles del ERP | Usan la información para su función y no comparten su contraseña |

**4. Principios.**
1. **Mínimo privilegio:** cada usuario tiene solo los grupos de su rol; ningún usuario por rol es administrador del ERP; los registros se limitan por almacén.
2. **Defensa en profundidad:** TLS, cabeceras, 2FA, bloqueo de intentos, gestor de BD cerrado y base sin superusuario.
3. **Todo por código y revisado:** la configuración se carga desde `donofrio_base`; los cambios entran por un PR revisado por el **otro** integrante y con el CI en verde; el RFC es el PR ([10.4](anexo_10_04_rfc.md)).
4. **Rastro:** los cambios en precios, pedidos y compras se auditan; los PR y el historial de Git son el registro de cambios.
5. **Recuperabilidad:** respaldo diario (RPO 24 h), réplica en caliente y restauración probada (RTO objetivo ≤ 2 h; medido 31 s).
6. **Privacidad:** solo datos ficticios y mínimos (Ley 29733).
7. **Uso aceptable:** las credenciales y los secretos no se suben al repositorio (`.env` fuera de Git, *secret scanning* activo); las cuentas son personales.

**5. Controles clave** (detalle en la Parte B): contraseñas de 12 o más caracteres; 2FA para el administrador y el gerente; bloqueo tras 5 intentos; TLS 1.2/1.3 con HSTS; `list_db = False`; respaldo con suma SHA-256 y retención de 7 días; auditoría con `auditlog`; ramas protegidas; pruebas automáticas (136) y de seguridad (ZAP, `verificar_despliegue.sh`).

**6. Incidentes y cambios.** Los incidentes y solicitudes se registran en la «Mesa de Servicios TI» del Project (HU-32) con su SLA; los cambios, como PR con la plantilla de la DoD. Un evento de seguridad se informa al responsable el mismo día.

**7. Cumplimiento y revisión.** Esta política se revisa al **cierre de cada sprint** y en el **Gate 0**, y cuando cambie un riesgo de 5.10. El incumplimiento en el proyecto académico se trata como un impedimento del Scrum Master. Las limitaciones conocidas están declaradas en la Parte B (estados *Parcial*, *No implementado* y *Trabajo futuro*).

---

# Parte B. Declaración de Aplicabilidad

## Cómo leer la tabla

- **Aplica:** *Sí*, *Parcial* (se aplica con alcance reducido) o *No*.
- **Estado:** **Implementado** (existe en `develop` y se verificó, con evidencia en el repositorio), **Parcial** (existe con una limitación importante), **No implementado** (aplica y no existe), **Trabajo futuro** (aplica, se diseñó o se pospone) o **Excluido** (no aplica; se justifica).
- Los 93 controles del Anexo A de ISO/IEC 27001:2022 están en 4 temas: **5 Organizacionales** (37), **6 Personas** (8), **7 Físicos** (14) y **8 Tecnológicos** (34). Los nombres siguen ISO/IEC 27002:2022.
- La columna **Evidencia** cita un archivo del repositorio, un PR o una evidencia de `docs/capturas/sprint-3/`. Donde dice «5.11 C-xx» o «5.10 RSI-xx» se refiere a las tablas 16 y 17 de [5.10 y 5.11](05_10_a_05_12_seguridad.md).
- Los estados son **coherentes con 5.11**: donde el plan de 09 §9.8 decía «Implementado» y la realidad es menor (p. ej. 8.16, 8.31, 8.32), se documenta la realidad.

### Temas que no aplican (justificación en bloque, según 09 §9.8)

- **7.x Físicos (14 controles): No aplican.** Proyecto académico **sin instalaciones propias**: el sistema corre en las PC de los integrantes o en un contenedor de la nube; la seguridad física depende del *host* y queda fuera del alcance.
- **6.1, 6.2, 6.4, 6.5 (RR. HH. de contratación): No aplican.** El equipo son **dos estudiantes** sin contratación, selección, régimen disciplinario ni cese. **6.3, 6.6, 6.7 y 6.8 sí se evalúan.**
- **5.5, 5.11, 5.12, 5.13, 8.1, 8.11, 8.12, 8.17, 8.23 y 8.30 no aplican** por la misma causa: datos ficticios, sin empleados ni desarrollo externalizado, sin equipos de usuario final en el alcance y con el reloj heredado del *host* (se explica en cada fila). Con los 14 de 7.x y los 4 de 6.x suman **28 controles excluidos**.

## Resumen por estado

| Tema | Controles | Implementado | Parcial | No implementado | Trabajo futuro | Excluido |
|---|---|---|---|---|---|---|
| 5 Organizacionales | 37 | 6 | 22 | 3 | 2 | 4 |
| 6 Personas | 8 | 0 | 3 | 1 | 0 | 4 |
| 7 Físicos | 14 | 0 | 0 | 0 | 0 | 14 |
| 8 Tecnológicos | 34 | 15 | 12 | 0 | 1 | 6 |
| **Total** | **93** | **21** | **37** | **4** | **3** | **28** |

## Tema 5. Controles organizacionales (5.1 a 5.37)

| Control | Aplica | Justificación | Mecanismo real | Evidencia | Estado |
|---|---|---|---|---|---|
| 5.1 Políticas de seguridad de la información | Sí | Se necesita un marco mínimo | Política de 1 página (Parte A de este anexo) | Este anexo | Implementado |
| 5.2 Roles y responsabilidades de seguridad | Sí | Alguien debe responder por cada control | Roles de seguridad en la política (§3) y roles Scrum en `docs/pm/roles.md` | `docs/pm/roles.md`; este anexo | Parcial |
| 5.3 Segregación de funciones | Parcial | Equipo de 2 personas | El autor de un PR **no** lo aprueba (regla de aprobación del otro integrante en `develop`); permisos por rol de negocio (`ir.model.access.csv`). **Límite:** con `enforce_admins = false` el administrador puede saltarse la regla | 6.6; `gh api …/protection` en `S3-informe6_evidencia_github.txt` | Parcial |
| 5.4 Responsabilidades de la dirección | Parcial | La «dirección» son el SM y la PO | Aprobación de la política y revisión al cierre de cada sprint | Parte A; `docs/scrum/` | Parcial |
| 5.5 Contacto con las autoridades | No | Proyecto académico con datos ficticios: no hay incidentes reportables a una autoridad | — | — | Excluido |
| 5.6 Contacto con grupos de interés especial | Sí | Se depende de Odoo, OCA y GitHub | No hay suscripción formal a boletines de seguridad. **Límite:** Dependabot sin configurar | 5.11 C-15 | No implementado |
| 5.7 Inteligencia de amenazas | Sí | Odoo 19 y OCA reciben avisos de seguridad | Solo se usa OWASP Top 10 como lista de ataques de referencia; no hay fuente de amenazas vigilada | 5.12 | Trabajo futuro |
| 5.8 Seguridad en la gestión de proyectos | Sí | Hay un proyecto Scrum con entregas | Plan y registro de riesgos (`docs/pm/plan_riesgos.md`), tabla de riesgos de seguridad y checklist de la DoD del PR (ACL, tests, sin patrones legacy) | `docs/pm/plan_riesgos.md`; `.github/pull_request_template.md`; 5.10 | Implementado |
| 5.9 Inventario de información y otros activos | Sí | Hay que saber qué se protege | Activos listados en 5.10; inventario de módulos con `scripts/grafo_dependencias.py` (62 módulos en el árbol de `depends`); diccionario de datos de las tablas. **Límite:** no hay un registro formal de activos con propietario | 5.10; `S3-informe5_evidencia_tests_y_dependencias.txt`; `04_02_diccionario_datos.md` | Parcial |
| 5.10 Uso aceptable de la información y los activos | Sí | Evitar la publicación de secretos y el uso de cuentas ajenas | Principio 7 de la política; `.env` en `.gitignore`; *secret scanning* con *push protection*. **Límite:** sin un documento de uso aceptable aparte | Parte A §4; 5.11 C-16 | Parcial |
| 5.11 Devolución de activos | No | Sin empleados ni activos entregados | — | — | Excluido |
| 5.12 Clasificación de la información | No | Todos los datos son ficticios y de un solo nivel | La política los trata como un único nivel | Parte A | Excluido |
| 5.13 Etiquetado de la información | No | Sin clasificación no hay etiquetas | — | — | Excluido |
| 5.14 Transferencia de información | Parcial | El código y los datos se mueven entre PC y GitHub; los usuarios acceden por web | TLS 1.2/1.3 con HSTS en el despliegue protegido; GitHub por HTTPS. **Límite:** el repositorio es **público** y la copia de respaldo no se cifra | `verificar_despliegue.sh`; 5.11 C-05, C-10 | Parcial |
| 5.15 Control de acceso | Sí | Datos de varias áreas | Grupos de Odoo 19 (`res.groups`), ACL e `ir.rule` por almacén | `addons/donofrio_base/security/`; `test_seguridad.py` (9 pruebas); 5.11 C-01 | Implementado |
| 5.16 Gestión de identidades | Sí | Cada usuario debe ser identificable | 10 usuarios por rol creados por código, ninguno administrador; empleados vinculados a su usuario. **Límite:** sin proceso de baja de usuarios | `usuarios_data.xml`; `test_seguridad.py`; `test_rrhh.py`; PR #157 | Parcial |
| 5.17 Información de autenticación | Sí | Hay usuarios internos | `auth_password_policy.minlength = 12`; contraseñas con PBKDF2-SHA512; `admin_passwd` de 16 o más caracteres y no la de ejemplo en producción; secretos en `.env` o archivo | `seguridad_data.xml`; `test_hardening.py`; `docker/odoo/entrypoint.sh`; 5.11 C-02, C-09 | Implementado |
| 5.18 Derechos de acceso | Sí | Mínimo privilegio | Un usuario por rol con sus grupos; las solicitudes de acceso se registran en la mesa de servicios (tipo «Solicitud de acceso») | `test_seguridad.py`; `mesa_servicios_data.xml`; PR #157 y #193 | Implementado |
| 5.19 Seguridad en las relaciones con proveedores | Parcial | Se depende de GitHub, Docker Hub y OCA | Proveedores identificados (Odoo, OCA, GitHub, Docker Hub, PostgreSQL, Nginx). **Límite:** sin evaluación ni acuerdos | 5.11 C-15; `docker/odoo/Dockerfile` | Parcial |
| 5.20 Seguridad en los acuerdos con proveedores | Sí | Condiciones de uso de GitHub y licencias | Solo los términos públicos de cada proveedor y las licencias (LGPL-3, AGPL-3 de OCA); no hay acuerdos propios | `LICENSE`; `Dockerfile` | No implementado |
| 5.21 Cadena de suministro de las TIC | Sí | Imagen, módulos y acciones de terceros | Imagen `odoo:19.0-20261112` y `postgres:16` fijadas; `auditlog` de OCA por **commit** (`13e504f…`); `ruff` 0.8.4; imágenes de k6, ZAP y PlantUML con versión. **Límite:** las acciones de GitHub se llaman por versión mayor (`@v4`, `@v6`), no por commit; sin escaneo de dependencias | `docker/odoo/Dockerfile`; `.github/workflows/`; 5.11 C-15 | Parcial |
| 5.22 Seguimiento y cambio de los servicios de proveedores | Sí | Detectar versiones vulnerables | **No** hay Dependabot (no existe `.github/dependabot.yml`) ni revisión periódica; la corrida semanal del CI solo detecta roturas | `S3-informe6_evidencia_github.txt` §1 y §7 | Trabajo futuro |
| 5.23 Seguridad en el uso de servicios en la nube | Parcial | GitHub (repositorio, Actions y GHCR) | *Secret scanning* y *push protection* activos; permisos de Actions limitados (`contents: read`); solo `GITHUB_TOKEN`. **Límite:** el paquete GHCR aún no existe | `ci.yml`; `S3-informe6_evidencia_github.txt` §1 | Parcial |
| 5.24 Planificación y preparación de la gestión de incidentes | Sí | Continuidad operativa | Mesa de Servicios TI en Project con tipos ITIL, etapas y SLA por prioridad (30 min/4 h a 1 día/5 días). **Límite:** el formato de registro de incidente (anexo 10.5) lo escribe Evelyn y aún no está | `mesa_servicios_data.xml`; `test_mesa_servicios.py` (11); PR #193 | Parcial |
| 5.25 Evaluación y decisión sobre eventos | Sí | Priorizar | Matriz impacto × urgencia → prioridad P1 a P4 y la fecha límite sale de la prioridad | `test_mesa_servicios.py`; 09 §9.3 | Parcial |
| 5.26 Respuesta a incidentes | Sí | Resolver dentro del SLA | Etapas Nuevo → En análisis → En atención → Resuelto → Cerrado; pivote de cumplimiento del SLA. **Límite:** solo tickets de ejemplo, ningún incidente real | `HU-32_pivote_cumplimiento_sla.png` | Parcial |
| 5.27 Aprendizaje de los incidentes | Sí | Evitar repetirlos | Retrospectivas por sprint y el registro de riesgos se actualizan tras cada hallazgo (p. ej. las 2 corridas rojas de HU-27 se corrigieron en el PR). **Límite:** sin análisis de causa raíz formal | `docs/scrum/sprint-*/`; `docs/pm/plan_riesgos.md` | Parcial |
| 5.28 Recopilación de evidencias | Sí | Auditoría | Historial de Git y de PR (inalterable salvo *force push*, prohibido), `auditlog`, `res_users_log`, registros del CI. **Límite:** sin procedimiento forense | 6.6; 5.11 C-12 | Parcial |
| 5.29 Seguridad de la información durante una interrupción | Sí | Temporada alta crítica | Respaldos con `backup.sh`/`restore.sh` (RTO 31 s) y réplica en *streaming*. **Límites:** el *cron* diario está documentado y no instalado; sin cifrado; la promoción de la réplica no se probó | `HU-26_evidencia_respaldo.txt`; `HU-25_evidencia_replica.txt`; 5.11 C-10, C-11 | Parcial |
| 5.30 Preparación de las TIC para la continuidad | Sí | Disponibilidad ≥ 99 % | `restart: unless-stopped` y *healthchecks*; RPO 24 h y RTO ≤ 2 h. **Límite:** sin medición de disponibilidad (Uptime Kuma no se implementó) y sin *failover* automático | 5.14 Tabla 24 c y d; 5.11 C-13 | Parcial |
| 5.31 Requisitos legales y contractuales | Sí | Ley 29733 y licencias | Datos ficticios y mínimos (RNF013); licencia LGPL-3 del código propio. **Límite:** el reglamento vigente de la Ley 29733 no se citó con texto verificado | `LICENSE`; 4.2.3 RNF013; 09 §9.1 | Parcial |
| 5.32 Derechos de propiedad intelectual | Sí | Se reutiliza código de terceros | Código propio bajo **LGPL-3**; Odoo (LGPL-3) y `auditlog` de OCA (AGPL-3) se usan sin modificar y se declaran en el `Dockerfile`. **Límite:** sin inventario de licencias de las 109 dependencias instaladas | `LICENSE`; `docker/odoo/Dockerfile` | Parcial |
| 5.33 Protección de registros | Sí | Evitar pérdida o alteración | Respaldo con suma SHA-256 (un respaldo alterado se rechaza), retención de 7 días y auditoría de cambios | `verificar_backup.sh`; 5.11 C-10, C-12 | Parcial |
| 5.34 Privacidad y protección de datos personales | Sí | Ley 29733 | Datos ficticios (RUC `20999999990`, correos `.example.com`); campos privados de empleados protegidos por el grupo de RR. HH. de Odoo. **Límite:** sin política de privacidad ni consentimiento (no aplican con datos ficticios) | 5.11 C-18; RNF013 | Parcial |
| 5.35 Revisión independiente de la seguridad | Sí | Verificar los controles con alguien ajeno | La revisión es **entre los dos integrantes**, no independiente; ZAP es una herramienta automática | 6.6 | No implementado |
| 5.36 Cumplimiento de políticas y normas | Sí | Comprobar que se cumple lo escrito | El CI hace cumplir `check_legacy.sh`, `ruff` y los tests; la DoD del PR. **Límite:** `enforce_admins` desactivado | `ci.yml`; 6.6 | Parcial |
| 5.37 Procedimientos operativos documentados | Sí | Reproducibilidad | Manual de instalación (§2 a §8), `docs/dev/release.md`, `docs/dev/pruebas_no_funcionales.md` y `docs/dev/odoo19_cambios.md` | `docs/manuales/manual_instalacion.md`; `docs/dev/` | Implementado |

## Tema 6. Controles de personas (6.1 a 6.8)

| Control | Aplica | Justificación | Mecanismo real | Evidencia | Estado |
|---|---|---|---|---|---|
| 6.1 Selección | No | Equipo de dos estudiantes, sin contratación | — | — | Excluido |
| 6.2 Términos y condiciones de contratación | No | Sin contratos laborales | — | — | Excluido |
| 6.3 Concienciación, educación y formación | Parcial | Equipo pequeño | Sección de seguridad del manual (§6.2) con los controles y la regla de conocimiento cruzado de `docs/pm/roles.md`. **Límite:** sin capacitación formal | `docs/manuales/manual_instalacion.md` §6.2; `docs/pm/roles.md` | Parcial |
| 6.4 Proceso disciplinario | No | Sin relación laboral | — | — | Excluido |
| 6.5 Responsabilidades tras el cese o cambio de empleo | No | Sin altas ni bajas de personal | — | — | Excluido |
| 6.6 Acuerdos de confidencialidad | Parcial | Los datos son ficticios, pero hay material del docente | Los PDF de los lineamientos y la plantilla del docente **no se suben** al repositorio público (`.gitignore`) | `.gitignore` | Parcial |
| 6.7 Trabajo remoto | Sí | Cada integrante trabaja en su PC | Todo el trabajo pasa por GitHub con PR revisado. **No** hay política de teletrabajo ni se verifica el 2FA de las cuentas de GitHub | Parte A | No implementado |
| 6.8 Notificación de eventos de seguridad | Sí | Detectar y reportar | Plantilla de *issue* `bug.yml` y la mesa de servicios; la política pide informar al responsable el mismo día | `.github/ISSUE_TEMPLATE/bug.yml`; PR #193 | Parcial |

## Tema 7. Controles físicos (7.1 a 7.14): no aplican

Justificación única (09 §9.8): el proyecto es **académico y no tiene instalaciones propias**; el sistema corre en las PC de los integrantes o en un contenedor de la nube y la seguridad física depende del *host*. Los 14 controles quedan **Excluidos**; si el ERP se llevara a un local real, se evaluarían de nuevo.

| Control | Aplica | Justificación | Estado |
|---|---|---|---|
| 7.1 Perímetros de seguridad física | No | Sin instalaciones propias | Excluido |
| 7.2 Controles físicos de entrada | No | Sin instalaciones propias | Excluido |
| 7.3 Seguridad de oficinas, despachos e instalaciones | No | Sin instalaciones propias | Excluido |
| 7.4 Monitoreo de la seguridad física | No | Sin instalaciones propias | Excluido |
| 7.5 Protección contra amenazas físicas y ambientales | No | Sin instalaciones propias; el servidor es una PC o un contenedor | Excluido |
| 7.6 Trabajo en áreas seguras | No | Sin áreas seguras | Excluido |
| 7.7 Puesto de trabajo despejado y pantalla limpia | No | Sin puestos de trabajo propios | Excluido |
| 7.8 Emplazamiento y protección de los equipos | No | Los equipos son personales | Excluido |
| 7.9 Seguridad de los activos fuera de las instalaciones | No | Los equipos son personales | Excluido |
| 7.10 Soportes de almacenamiento | No | Sin soportes extraíbles en el alcance; los respaldos van a una carpeta (`BACKUP_DIR`) | Excluido |
| 7.11 Servicios de suministro | No | Depende del *host* | Excluido |
| 7.12 Seguridad del cableado | No | Depende del *host* | Excluido |
| 7.13 Mantenimiento de los equipos | No | Depende del *host* | Excluido |
| 7.14 Eliminación o reutilización segura de equipos | No | Sin equipos propios | Excluido |

## Tema 8. Controles tecnológicos (8.1 a 8.34)

| Control | Aplica | Justificación | Mecanismo real | Evidencia | Estado |
|---|---|---|---|---|---|
| 8.1 Dispositivos de punto final de usuario | No | Los equipos de usuario final no forman parte del sistema (solo el servidor) | — | — | Excluido |
| 8.2 Derechos de acceso privilegiado | Sí | Administrador de Odoo y de PostgreSQL | Ningún usuario por rol es administrador del ERP; el administrador (`admin`) y el gerente tienen 2FA obligatoria; el rol de Odoo **no** es superusuario de PostgreSQL | `test_seguridad.py::test_nadie_es_administrador`; `test_hardening.py`; `verificar_replica.sh` paso 5; 5.11 C-04 | Implementado |
| 8.3 Restricción de acceso a la información | Sí | Datos de varias áreas | `ir.rule` por almacén; el vendedor y el cajero no ven compras; el vendedor no modifica almacenes. **Límite:** las reglas por registro cubren solo inventario | `test_seguridad.py` (`AccessError`); 5.11 C-01 | Implementado |
| 8.4 Acceso al código fuente | Sí | El código es el activo principal | Repositorio con 2 personas con acceso de escritura (Orlando con rol *admin* y Evelyn con rol *write*); ramas protegidas; *force push* prohibido. **Límite:** el repositorio es **público** (lectura abierta, por decisión del proyecto) y `enforce_admins` desactivado | `S3-informe6_evidencia_github.txt` §1 a §3 | Parcial |
| 8.5 Autenticación segura | Sí | Acceso web | Bloqueo tras 5 intentos por 60 s (por IP y *worker*); 2FA TOTP o por correo para los privilegiados con `proxy_mode`; contraseñas de 12 o más | `test_hardening.py` (12); `verificar_despliegue.sh` paso 7; 5.11 C-03, C-04 | Implementado |
| 8.6 Gestión de la capacidad | Sí | Temporada alta | k6 con 20 usuarios (p95 de 12 ms) y de esfuerzo (232 peticiones/s, CPU de Odoo hasta 160 %); `docker stats`. **Límite:** sin proyección de usuarios de la temporada alta | 5.14 Tabla 22; `HU-28_evidencia_k6_zap.txt` | Parcial |
| 8.7 Protección contra el malware | Sí | Los usuarios pueden subir adjuntos | Odoo no escanea archivos adjuntos y el proyecto no agrega un antivirus | — | Trabajo futuro |
| 8.8 Gestión de vulnerabilidades técnicas | Sí | Dependencias de terceros | Versiones fijadas y **ZAP baseline** (0 altas). **Límite:** sin Dependabot ni escaneo de imágenes; actualizaciones de seguridad de GitHub desactivadas | `HU-28_zap_reporte.html`; 5.11 C-15, C-17 | Parcial |
| 8.9 Gestión de la configuración | Sí | Infraestructura como código | `docker-compose.yml`, `Dockerfile`, `odoo.conf.template`, Nginx y `.env.example` en Git; configuración de seguridad por XML; `entrypoint.sh` rechaza una configuración insegura en producción | `docker/`; `docker-compose.yml`; `seguridad_data.xml`; 5.11 C-09 | Implementado |
| 8.10 Eliminación de información | Sí | Retención y borrado | `backup.sh` borra los respaldos de más de 7 días (se probó: borra el de 8 días y conserva el de 6). **Límite:** sin política de borrado de datos de negocio | `verificar_backup.sh` paso 6 | Parcial |
| 8.11 Enmascaramiento de datos | No | Todos los datos son ficticios | — | — | Excluido |
| 8.12 Prevención de fuga de datos | No | Datos ficticios; sin correo ni canales salientes configurados | — | — | Excluido |
| 8.13 Copia de seguridad | Sí | Pérdida de datos | `backup.sh` (`pg_dump -Fc` + *filestore* + SHA-256, retención de 7 días) y `restore.sh` (solo a una base nueva); **RTO 31 s**. **Límites:** *cron* diario documentado y no instalado; sin cifrado; copia en el mismo equipo salvo que `BACKUP_DIR` apunte a otro | `HU-26_evidencia_respaldo.txt`; `verificar_backup.sh`; job `backup`; PR #187 | Implementado |
| 8.14 Redundancia de las instalaciones | Sí | Disponibilidad | Réplica en *streaming* de solo lectura (retraso de 2.3 ms). **Límites:** asíncrona, sin *failover* automático, promoción no probada | `HU-25_evidencia_replica.txt`; `verificar_replica.sh`; job `replica`; PR #186 | Implementado |
| 8.15 Registro | Sí | Auditoría | `auditlog` sobre precios, pedidos de venta y de compra; *chatter* con `tracking`; `res_users_log` de los inicios de sesión | `seguridad_data.xml`; `test_hardening.py::test_cambio_de_precio_queda_auditado`; 5.11 C-12 | Implementado |
| 8.16 Actividades de seguimiento | Sí | Detectar fallos | *Healthchecks* de Docker (`/web/health` cada 15 s, `pg_isready`); registros de Odoo. **Límite:** sin monitoreo continuo ni alertas (Uptime Kuma no se implementó) | 5.11 C-13 | Parcial |
| 8.17 Sincronización del reloj | No | Los contenedores usan el reloj del *host* y no hay otros sistemas que correlacionar | — | — | Excluido |
| 8.18 Uso de programas de utilidad privilegiados | Sí | `odoo shell`, `psql` y `docker compose` | Requieren acceso al *host*; el rol de Odoo no es superusuario de PostgreSQL. **Límite:** sin registro del uso de estas utilidades | `verificar_replica.sh` paso 5 | Parcial |
| 8.19 Instalación de software en sistemas operativos | Sí | Evitar software no autorizado | Los módulos se instalan por código desde la imagen y los usuarios por rol no son administradores (no pueden instalar aplicaciones); la imagen solo cambia por PR | `docker/odoo/Dockerfile`; `test_seguridad.py::test_nadie_es_administrador` | Implementado |
| 8.20 Seguridad de redes | Sí | Credenciales en tránsito | Nginx con TLS 1.2/1.3, redirección 80 → 443 y HSTS; PostgreSQL y Odoo solo en `127.0.0.1`. **Límite:** Nginx publica 8080 y 8443 en todas las interfaces (lo pide la demo) | `docker/nginx/`; `verificar_despliegue.sh`; 5.11 C-05, C-08 | Implementado |
| 8.21 Seguridad de los servicios de red | Sí | Servicio web expuesto | Cabeceras de seguridad y cookies `Secure; HttpOnly; SameSite=Lax`; `/web/database/` → 404; ZAP baseline. **Límites:** CSP con `unsafe-inline`/`unsafe-eval` (OWL); PostgreSQL sin TLS dentro de Docker | `docker/nginx/seguridad.conf`; `HU-28_zap_reporte.html`; 5.11 C-06 | Parcial |
| 8.22 Segregación de redes | Sí | Aislar la base de datos | Red interna de Docker para PostgreSQL y la réplica; puertos al *host* solo en `127.0.0.1`. **Límite:** una sola red de Docker, sin zonas | `docker-compose.yml` | Parcial |
| 8.23 Filtrado web | No | Controla la navegación de usuarios finales, fuera del alcance | — | — | Excluido |
| 8.24 Uso de criptografía | Sí | Credenciales y datos en tránsito | TLS 1.2/1.3 y HSTS; hash PBKDF2-SHA512 de contraseñas; sumas SHA-256 de los respaldos. **Límites:** certificado **autofirmado**; sin cifrado en reposo ni de los respaldos; sin política de gestión de claves | `verificar_despliegue.sh`; `HU-27_evidencia_seguridad.txt`; 5.11 C-02, C-05 | Parcial |
| 8.25 Ciclo de vida de desarrollo seguro | Sí | Hay código propio | PR con plantilla de DoD, revisión del otro integrante, CI (`lint` y `test`) obligatorio en `develop`; sin patrones legacy; textos y commits en español con Conventional Commits | `.github/pull_request_template.md`; `ci.yml`; 6.6 | Implementado |
| 8.26 Requisitos de seguridad de las aplicaciones | Sí | Deben ser explícitos | RNF009 (RBAC, HTTPS, gestor de BD, 2FA), RNF010 (auditoría) y RNF013 (datos) con su prueba; riesgos RSI-01 a RSI-16 | `04_02_requerimientos_no_funcionales.md`; 5.10 | Implementado |
| 8.27 Principios de arquitectura segura | Sí | Arquitectura en capas | Nginx → Odoo → PostgreSQL (primario y réplica), mínimo privilegio en la base, configuración por código. **Límite:** sin revisión formal de arquitectura segura | `04_03_infraestructura.md`; 5.7 a 5.9 | Parcial |
| 8.28 Codificación segura | Sí | Evitar inyección y XSS | Solo ORM, **sin SQL crudo** (`grep` de `cr.execute` en `addons/`: 0 resultados), QWeb escapa; `ruff` y `check_legacy.sh` en el CI; el hook anti-legacy del agente | `S3-informe5_evidencia_inyeccion_xss.txt`; `ci.yml`; `.claude/hooks/` | Implementado |
| 8.29 Pruebas de seguridad en desarrollo y aceptación | Sí | Validar los controles | 21 pruebas de acceso y endurecimiento en el CI; `verificar_despliegue.sh`; ZAP baseline. **Límite:** ZAP pasivo y sin sesión; sin prueba de penetración | 6.13; `HU-28_zap_reporte.html` | Implementado |
| 8.30 Desarrollo externalizado | No | Todo el código lo escriben los dos integrantes | — | — | Excluido |
| 8.31 Separación de entornos | Sí | Evitar cambios directos en producción | Desarrollo (`workers = 0`), CI efímero y «producción» de demostración (perfil `proxy`, `workers = 2`, `list_db = False`). **Límites:** misma PC para los tres, **sin cinta de entorno** (`web_environment_ribbon` no se implementó) | `docker-compose.yml`; `ci.yml`; `docker/odoo/odoo.conf.template` | Parcial |
| 8.32 Gestión de cambios | Sí | Estabilidad | PR → CI → revisión → fusión; formato de RFC (anexo 10.4). **Límites:** `enforce_admins` desactivado, 3 PR del Sprint 1 se fusionaron sin aprobación vigente, `main` sin checks obligatorios | 6.6; [10.4](anexo_10_04_rfc.md); 5.11 C-14 | Parcial |
| 8.33 Información de prueba | Sí | No usar datos reales | Datos 100 % ficticios con semilla fija (`cargar_transacciones.py`); las pruebas usan una base temporal que se borra | `scripts/cargar_transacciones.py`; `scripts/test.sh` | Implementado |
| 8.34 Protección de los sistemas durante las pruebas de auditoría | Sí | Las pruebas de carga y ZAP pueden afectar al servicio | Se corrieron sobre el despliegue local con una base aparte (`donofrio_perf`), sin tocar las bases de desarrollo; ZAP es pasivo | 5.14; `docs/dev/pruebas_no_funcionales.md` | Implementado |

## Trazabilidad norma → control → evidencia (09 §9.9)

| Norma / marco | Control implementado | Evidencia |
|---|---|---|
| ISO 27001 5.15, 8.3 | Grupos, ACL e `ir.rule` | `addons/donofrio_base/security/`; `test_seguridad.py` (corre en el CI) |
| ISO 27001 8.5, 8.2 | 2FA, bloqueo, contraseñas | `test_hardening.py`; `verificar_despliegue.sh`; `HU-27_evidencia_seguridad.txt` |
| ISO 27001 5.17 | Política de contraseñas | `seguridad_data.xml`; consulta SQL del hash en la evidencia de HU-27 |
| ISO 27001 8.15 | `auditlog` y *chatter* | `test_cambio_de_precio_queda_auditado` |
| ISO 27001 8.13, 8.14 + ISO 22301 | Respaldo, restauración y réplica | `HU-26_evidencia_respaldo.txt`, `HU-25_evidencia_replica.txt` |
| ISO 27001 8.24, 8.20 | Nginx con TLS y HSTS | `docker/nginx/`; `verificar_despliegue.sh` |
| ISO 27001 8.29 + OWASP | ZAP baseline y pruebas de acceso | `HU-28_zap_reporte.html`; 6.13 |
| ISO 27001 8.31, 8.32 + ITIL + COBIT BAI06 | PR + CI + RFC | 6.6; [10.4](anexo_10_04_rfc.md); `S3-informe6_evidencia_github.txt` |

> **Trazabilidad de requisitos y pruebas:** [`trazabilidad.md`](trazabilidad.md). **Normas de apoyo** (ISO 31000, ITIL 4, ISO 20000-1, COBIT 2019, ISO 25010, ISO 22301, ISO 9001/HACCP, Ley 29733): sección 09 del plan; sus formatos ITIL están en los anexos 10.3 a 10.5.
