# 8. Recomendaciones

> **Estado:** versión final del Cierre (25/11/2026) · **Autor de 8.2:** Orlando (SM) · **Autora de 8.1:** Evelyn (PO) · **Revisa:** el otro integrante · **Fuente:** [02 §2.2 y §2.3](../plan/02_mapeo_plantilla.md) (fila 8), [03 §3.4](../plan/03_modulos_odoo.md), [04 §4.5](../plan/04_scrum_pmbok.md), [5.9](05_07_a_05_09_arquitectura_bd.md), [5.14](05_13_a_05_14_pruebas.md), [5.15](05_15_despliegue.md), [4.2.3](04_02_requerimientos_no_funcionales.md), [4.3.8](04_03_infraestructura.md), [4.5.3 y 4.5.4](04_05_riesgos_despliegue_y_mantenimiento.md)
>
> Cada recomendación sale de **una limitación o un pendiente que el propio proyecto documentó** con su evidencia; no hay recomendaciones genéricas. Los números de las secciones enlazadas son los del informe al 25/11/2026. Con la Fase 2 completa (M1 a M4 en `main` y publicados en las releases `v1.1.0` a `v1.4.0`), **ya no hay módulos propios por construir**: la recomendación T10 de la versión anterior pasó a ser *implementada* y se reemplazó por mejoras de los módulos ya construidos.

## 8.1 Recomendaciones de negocio y gestión

Las redactó Evelyn en [`08_01_recomendaciones_negocio.md`](08_01_recomendaciones_negocio.md) (8 recomendaciones con plazo y esfuerzo). Esta sección 8.2 no las repite; las dos se ensamblan en un solo capítulo 8 al maquetar el informe.

## 8.2 Recomendaciones técnicas

Se ordenan por **prioridad para una puesta en producción real**, no por tamaño. Cada fila dice qué se recomienda, **qué evidencia del proyecto la respalda** (qué se midió o qué no existe) y cómo se haría con lo que ya hay en el repositorio. «Trabajo futuro» significa algo que el proyecto **no hizo**; lo que se hizo está en las secciones 4 y 5.

### Tabla 8.2-a. Resumen de recomendaciones técnicas

| # | Recomendación | Qué la respalda | Esfuerzo | Sección |
|---|---|---|---|---|
| T1 | Instalar el *cron* de respaldos y sacar los respaldos del equipo (con cifrado) | RNF006 y C-10: el *cron* está documentado y no instalado; los respaldos viven en el mismo equipo | Bajo | [8.2.1](#821-respaldos-programados-y-copia-fuera-del-equipo) |
| T2 | Medir la disponibilidad con un registro continuo (Uptime Kuma) | RNF011 «Parcial»: sin medición, el 99 % no se puede afirmar | Bajo | [8.2.2](#822-medición-de-la-disponibilidad) |
| T3 | Revisar en otros navegadores y en la ventana angosta (incluidos el tablero y la liquidación) | RNF001 «Parcial»: la revisión usó Chrome y una ventana de 375 × 812 | Bajo | [8.2.3](#823-compatibilidad-con-navegadores-y-móvil-rnf001) |
| T4 | Desplegar en una VM con dominio y Let's Encrypt, y un `cd.yml` por SSH | 4.3.8: no hay VM; el certificado es autofirmado | Medio | [8.2.4](#824-vm-en-la-nube-con-lets-encrypt-y-despliegue-automático) |
| T5 | Configurar un servidor de correo saliente | 5.7: `auth_totp_mail` lo necesita y no está configurado | Bajo | [8.2.5](#825-correo-saliente-para-el-2fa-por-correo) |
| T6 | Activar `pg_stat_statements` | 5.9b: no activado; no se midieron las consultas más lentas | Bajo | [8.2.6](#826-pg_stat_statements-y-consultas-lentas) |
| T7 | Reducir el JavaScript del backend y del tablero para subir Lighthouse (backend 59, tablero 76) a 80 | RNF008 «Parcial»: límite conocido por el TBT del JavaScript de Odoo | Medio | [8.2.7](#827-rendimiento-del-backend-lighthouse-59-frente-a-80) |
| T8 | Activar `enforce_admins` en `develop` y `main` | 6.6 y C-14: las reglas no aplican al administrador (los checks de `main` ya están) | Bajo | [8.2.8](#828-protección-de-ramas-enforce_admins-y-main) |
| T9 | Completar la seguridad: promoción de la réplica, ZAP activo y autenticado, Dependabot | 5.11 (C-11, C-15, C-17) y 5.14 | Medio | [8.2.9](#829-otras-mejoras-de-seguridad-y-calidad-con-evidencia) |
| T10 | Mejorar los módulos de la Fase 2: sensores y alertas por lecturas que faltan, auditoría `auditlog`, pruebas de JavaScript, vista móvil probada y app para el heladero | Límites declarados en 5.5b a 5.5e y en el anexo 10.1 | Medio a alto | [8.2.10](#8210-mejoras-de-los-módulos-de-la-fase-2-trabajo-futuro-real) |
| T11 | Envío electrónico de comprobantes a SUNAT/OSE | `l10n_pe_edi` es Enterprise: **fuera del alcance** | Alto | [8.2.11](#8211-envío-electrónico-a-sunat-edi-fuera-de-alcance) |

### 8.2.1 Respaldos programados y copia fuera del equipo

- **Recomendación.** Instalar el *cron* diario de `scripts/backup.sh`, definir `BACKUP_DIR` en una carpeta sincronizada o un disco externo, **cifrar** los respaldos (por ejemplo con `gpg` o `age`) y restaurar de forma periódica en **otra máquina**.
- **Por qué.** El RTO medido es de 31 s y el respaldo se verifica con SHA-256 (RNF006 «Cumple»), pero el RPO de 24 h solo existe si alguien instala el *cron* (`0 2 * * * cd /ruta && scripts/backup.sh >> backups/backup.log 2>&1`, documentado en el manual de instalación); hoy **no está instalado**, los respaldos **no se cifran** y están en el mismo equipo que la base (5.15.4, C-10, R8).
- **Cómo.** `backup.sh` ya admite `BACKUP_DIR`; falta la línea del `crontab` y un paso de cifrado y copia. `scripts/verificar_backup.sh` ya prueba la restauración y puede correr tras cada copia programada.

### 8.2.2 Medición de la disponibilidad

- **Recomendación.** Registrar `GET /web/health` de forma continua (Uptime Kuma como servicio del perfil `tools` de Compose o un *cron* con `curl`) y calcular la disponibilidad del horario laboral.
- **Por qué.** RNF011 está **«Parcial»**: hay reinicio automático y *healthchecks* en los tres contenedores, pero no hay ninguna medición en el tiempo y la meta del 99 % no se puede afirmar como cumplida (5.14, Tabla 24 c). El perfil `tools` del plan **no existe** en el `docker-compose.yml`.
- **Cómo.** Agregar el perfil, apuntar el monitor a `/web/health` por la red interna y exportar el registro como evidencia mensual. También cubre RS-06: el *healthcheck* actual no detecta un *cron* de Odoo detenido ([4.5.4](04_05_riesgos_despliegue_y_mantenimiento.md)).

### 8.2.3 Compatibilidad con navegadores y móvil (RNF001)

- **Recomendación.** Ejecutar y registrar una prueba manual de CU002 (pedido) y CU003 (punto de venta) en Chrome, Firefox y Edge y en vista móvil, con una tabla de pasos y capturas.
- **Por qué.** RNF001 está **«Parcial»**: la revisión usó Chrome y una ventana de 375 × 812 (4.2.3 y el anexo 10.2).
- **Cómo.** Una sola persona, con los datos de `cargar_transacciones.py` y `cargar_demo_completa.py`, en menos de una hora; además, el tablero (M4) y la liquidación (M2, HU-21) en otros tamaños de pantalla.

### 8.2.4 VM en la nube con Let's Encrypt y despliegue automático

- **Recomendación.** Si el sistema se va a usar fuera de una PC, desplegar en una VM (Oracle Free u otra) con Docker Compose y el perfil `proxy`, un dominio y **Let's Encrypt** en lugar del certificado autofirmado, y agregar `.github/workflows/cd.yml` que, al publicar una release, entre por SSH, ejecute `backup.sh`, `docker compose pull`, `up -d`, `odoo -u donofrio_*` y un *smoke test* (`/web/health` y login), con *rollback* a la imagen del tag anterior.
- **Por qué.** **No se hizo** (4.3.8): el sitio solo existe en la PC que lo levanta. Hoy el despliegue y el *rollback* son manuales y **el *rollback* por imagen de un tag anterior no se ensayó**, aunque ya hay cinco tags publicados (`v1.0.0` a `v1.4.0`, 5.15.1).
- **Cómo y con qué cuidado.** La imagen `ghcr.io/orlando572/erp-donofrio:vX.Y.Z` y el zip ya los publica `release.yml` (publicados `v1.0.0` a `v1.4.0`); la llave SSH iría a *GitHub Secrets*. Antes de exponer a Internet hay que **revisar el sitio web público de Odoo** (`/web/signup`, `/contactus`) y agregar `noindex`, que el plan prometía (R11) y no existe. Es una mejora de operación, no un requisito de los lineamientos.

### 8.2.5 Correo saliente para el 2FA por correo

- **Recomendación.** Configurar un servidor de correo saliente (`ir.mail_server`, por ejemplo SMTP con un relé autenticado) y probarlo con el código de `auth_totp_mail`.
- **Por qué.** El administrador y el gerente tienen 2FA obligatorio en el despliegue protegido (C-04, probado en `test_hardening.py`), pero el servidor de correo saliente **no está configurado** ([5.7](05_07_a_05_09_arquitectura_bd.md), nivel 1): el 2FA funciona con la app de autenticación (TOTP) y el código por correo necesitaría un servidor real. Sin él, un usuario que pierde su app no tiene un camino de recuperación.
- **Cómo.** Datos de conexión por variables de entorno (nunca en el repositorio, que es público) y una prueba de envío en el despliegue.

### 8.2.6 `pg_stat_statements` y consultas lentas

- **Recomendación.** Activar `pg_stat_statements` en el primario (`shared_preload_libraries = 'pg_stat_statements'` en el `command` del servicio `db`, `CREATE EXTENSION` en la base y reinicio) y revisar las consultas más lentas después de cada prueba de carga.
- **Por qué.** El plan lo contemplaba y **no está activado** (5.9b): la extensión está disponible en la imagen (versión 1.10) y `shared_preload_libraries` está vacío. k6 midió el tiempo de respuesta de la aplicación, no el de las consultas, y «Capacidad y desempeño» de ITIL pide medir ambos (5.15.6).
- **Cómo.** Es un cambio de dos líneas en `docker-compose.yml`; **exige reiniciar PostgreSQL**, por lo que conviene hacerlo con un respaldo reciente y con la réplica detenida.

### 8.2.7 Rendimiento del backend (Lighthouse 59 frente a 80)

- **Recomendación.** Reducir el JavaScript que carga el cliente web de Odoo (menos aplicaciones instaladas por usuario, desactivar widgets no usados, revisar el modo `debug=assets` fuera de las mediciones) y volver a medir con `scripts/perf/lighthouse.py`.
- **Por qué.** RNF008 está **«Parcial»**: login 100 y dashboard 80 con LCP de 1.9 s, pero el **backend queda en 59** con un TBT de 384 ms y el **tablero propio de M4 en 76** (39 en móvil, LCP de 2.11 s), por el tiempo que el navegador tarda en ejecutar el JavaScript de Odoo ([4.6.4](04_06_wpo.md)); ambos se declaran como **límite conocido**. El LCP del backend ya bajó de 12.2 s a 2.2 s con Nginx, gzip y caché.
- **Límite.** Es el costo del propio framework; no se corrige con configuración de Nginx ni de PostgreSQL. Para el tablero, lo único propio que se podría probar es reducir lo que carga la acción OWL (Chart.js y las tarjetas) y el *Speed Index* de 2.97 s. Si la meta de 80 en el backend o en el tablero es un requisito real, la opción es medir y quitar módulos, no ajustar el servidor.

### 8.2.8 Protección de ramas: `enforce_admins` y `main`

- **Recomendación.** Activar **`enforce_admins`** en `develop` y `main`. Los checks obligatorios `lint` y `test` de `main` ya están puestos desde el primer PR de release.
- **Por qué.** Las reglas **no aplican a los administradores** (verificado con la API el 23/11/2026) y Orlando es el único administrador (6.6); `main` exige una aprobación y los checks `lint` y `test` (6.4, Tabla 27, 25/11/2026). Es el control **C-14**, en estado «Parcial». **El PO decidió el 23/11/2026 dejarlo desactivado** en la Retro del Sprint 2, como salida de emergencia compensada con la revisión cruzada; esta recomendación es para el proyecto **después** de la entrega, o si la salida de emergencia deja de hacer falta.
- **Cómo.** `gh api -X PUT repos/orlando572/erp-donofrio/branches/develop/protection` con `enforce_admins: true` (o *Settings → Branches*). Antes de activarlo, comprobar que haya un segundo colaborador con rol de administrador para no quedarse sin salida.

### 8.2.9 Otras mejoras de seguridad y calidad con evidencia

| Mejora | Evidencia en el informe | Cómo |
|---|---|---|
| **Probar la promoción de la réplica** y definir el *failover* | C-11: asíncrona, sin *failover* automático, «promoción no probada» (5.9) | `pg_ctl promote` en `db-replica` y reconexión de Odoo, con un guion en `scripts/` |
| **ZAP activo y autenticado**, y sobre el backend | 5.14 Tabla 24 a: baseline pasivo y sin sesión; el backend se cubre solo con las pruebas de acceso | `zap-full-scan` con un usuario de prueba y alcance acotado, solo en un entorno de pruebas |
| **Dependabot y escaneo de dependencias** | C-15 y 6.4: no hay `dependabot.yml` y *Dependabot security updates* está desactivado | `.github/dependabot.yml` para Actions y Docker, y activar las alertas |
| **Job `upgrade` en el CI** (`-u` sobre una base con datos) | RS-01 ([4.5.3](04_05_riesgos_despliegue_y_mantenimiento.md)): el CI solo instala en una base nueva | Un job que restaure un respaldo del `develop` anterior y corra `-u donofrio_base` |
| **TLS entre Odoo y PostgreSQL** y cifrado de la réplica | 5.11 y Tabla 18: PostgreSQL sin TLS dentro de la red de Docker | Solo si los servicios dejan de compartir una red local |
| **Validar el vencimiento del lote en el punto de venta** | RNF005 «Cumple con límites»: el PdV bloquea un lote rechazado (M1) pero no aplica FEFO ni verifica el vencimiento | Restricción en `pos.order.line` o lectura del lote desde el código de barras |
| **Escrituras concurrentes y el PdV en k6** | 5.14 Tabla 22: solo lecturas; una petición fallida en el esfuerzo sin investigar | Extender `scripts/perf/carga.js` |

### 8.2.10 Mejoras de los módulos de la Fase 2: trabajo futuro real

Los cuatro módulos propios **están construidos, probados (81 pruebas) y publicados** (`v1.1.0` a `v1.4.0`); lo que queda es trabajo posterior a la entrega, cada ítem con el límite que lo respalda:

| # | Mejora | Módulo | Límite documentado que la respalda | Esfuerzo |
|---|---|---|---|---|
| 1 | **Sensores de temperatura** (IoT) y **alerta por lecturas que faltan** | M3 (RF008) | Las lecturas son manuales; si nadie registra la temperatura de una cámara no se genera ninguna alerta ([5.5d.8](05_05_modulo_donofrio_frio.md)) | Alto |
| 2 | Decidir **un solo aviso por lote por vencer** (el *cron* de M3 y la alerta estándar de `product_expiry` crean dos actividades) y permitir más de un destinatario | M3 | Mini gate de M3; un solo destinatario | Bajo |
| 3 | **Aplicación móvil o PWA para el heladero** | M2 (RF004, RNF001) | La liquidación es el formulario responsive de Odoo ([5.5c](05_05_modulo_donofrio_heladeros.md)) | Medio |
| 4 | Que la **merma** de la liquidación **registre una salida de inventario** | M2 | El pedido solo mueve stock por lo vendido ([5.5c.3](05_05_modulo_donofrio_heladeros.md)) | Medio |
| 5 | **`auditlog`** para liquidaciones, inspecciones y temperaturas | M1 a M3 (RNF010) | Hoy usan el historial del chatter, no `auditlog` ([anexo 10.2](anexo_10_02_fichas_rnf.md)) | Bajo |
| 6 | **Pruebas de JavaScript** (Hoot) del componente OWL y revisión de la marca en PDF, punto de venta y portal | M4 | Sin pruebas de JavaScript; no se revisaron los PDF ni otras pantallas ([5.5e.8](05_05_modulo_donofrio_tablero.md)) | Medio |
| 7 | **Versión parcial del tablero por áreas**, filtro de almacén en liquidaciones y cumplimiento de producción contra lo planificado | M4 (RF013) | Un usuario sin permiso de ventas recibe un aviso y no un tablero parcial; el cumplimiento cuenta las OP que ya empezaron | Medio |
| 8 | **Inspecciones de las órdenes históricas** y `ir.rule` por registro en calidad y heladeros | M1, M2 | Las inspecciones solo se crean al terminar una orden nueva; los módulos se protegen con grupos y ACL | Medio |

**Regla que se mantiene:** cualquier mejora entra por su rama `feature/HU-xx-*` y un PR a `develop`, con su prueba y su mini gate; lo que no cumple su DoD no se fusiona ([CLAUDE.md](../../CLAUDE.md) y 04 §4.3).

### 8.2.11 Envío electrónico a SUNAT (EDI): fuera de alcance

- **Recomendación.** Si D'Onofrio necesitara emitir comprobantes electrónicos válidos, el camino es un Proveedor de Servicios Electrónicos (OSE) o el EDI de Odoo; **no forma parte de este proyecto**.
- **Por qué.** `l10n_pe_edi` es de Odoo **Enterprise** y está excluido por la regla del proyecto (nada de Enterprise); el sistema emite facturas y boletas con IGV del 18 % y numeración de Odoo, **sin envío a SUNAT** (limitación declarada en 4.1.1, 4.2.4 y 4.6.3). La «guía de despacho» es una nota de entrega interna, no una guía de remisión electrónica. El plan descartó la integración con OSE/SUNAT por complejidad ([03 §3.4](../plan/03_modulos_odoo.md)).
- **Si se hiciera:** un OSE con API (o un módulo de OCA, si hay uno portado a 19.0) agregaría un modelo de envío y estados del comprobante; habría que revisar la compatibilidad con Community 19.0 antes de comprometerse.

## Resumen de dependencias entre recomendaciones

| Si se hace… | Conviene antes… |
|---|---|
| T4 (VM con Let's Encrypt) | T1 (respaldos fuera del equipo), T2 (monitoreo), T5 (correo para el 2FA) y T8 (`enforce_admins`) |
| T6 (`pg_stat_statements`) | T1: reiniciar PostgreSQL con un respaldo reciente |
| T10 (mejoras de la Fase 2) | T3 (otros tamaños de pantalla) para la mejora 3; T1 y T2 si el módulo se usa en producción |
| T7 (rendimiento del backend) | Medir otra vez con `scripts/perf/lighthouse.py` y comparar con [4.6.4](04_06_wpo.md) |
