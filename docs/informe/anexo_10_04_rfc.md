# Anexo 10.4 Solicitud de cambio (RFC)

> **Estado:** versión final del Cierre (25/11/2026; los datos medidos son los del 23/11/2026 salvo donde se indica) · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [09 §9.3](../plan/09_normas_marcos.md) (formato ITIL 4 «habilitación del cambio»), [06 §6.2 a §6.4](../plan/06_github_ci_infra.md), [6.6](06_04_a_06_06_repositorio.md), [5.10 a 5.12](05_10_a_05_12_seguridad.md), PR [#189](https://github.com/orlando572/erp-donofrio/pull/189)
>
> Los anexos 10.3 (solicitud de servicio o de acceso) y 10.5 (registro de incidente) son de Evelyn. Este anexo trae el **formato** de la solicitud de cambio y **un ejemplo lleno con un cambio real** del proyecto, la HU-27 (endurecimiento con Nginx, TLS, 2FA, política de contraseñas y auditoría).
>
> *El proyecto se **alinea** con las normas y marcos citados como buenas prácticas de referencia. No constituye una implementación certificada ni auditada de ninguno de ellos.*

## 1. Cómo se gestiona un cambio en el proyecto

El cambio sigue el flujo **PR → CI → revisión → fusión → verificación → cierre**. La práctica ITIL 4 de **habilitación del cambio** (y el control 8.32 de ISO/IEC 27001) se cubre así:

| Paso ITIL | En el proyecto | Quién |
|---|---|---|
| **Registro** de la solicitud | El PR con la plantilla [`.github/pull_request_template.md`](../../.github/pull_request_template.md) (HU, qué cambia, cómo probar, capturas) y la épica `Parte de #n`. **No existe** la plantilla de *issue* `solicitud_cambio.yml` que preveía 09 §9.3: la RFC es el cuerpo del PR y este formato | Quien propone |
| **Evaluación** (impacto y riesgo) | La checklist de la DoD en el PR, la tabla de riesgos de [5.10](05_10_a_05_12_seguridad.md) y el CI (`lint`, `test` y, desde el Sprint 3, `replica`, `backup` y `proxy`) | El otro integrante y el CI |
| **Autorización** | La aprobación del PR por el **otro integrante** (regla de `develop`; se descarta si se empuja código nuevo) | El otro integrante |
| **Implementación** | La fusión a `develop` (`squash`) | Quien propone o quien aprueba |
| **Verificación** | CI en verde y, si aplica, los *smoke tests* (`scripts/verificar_*.sh`) | El CI |
| **Cierre** | Release con el tag (`v1.0.0` en el Gate 0) y la épica cerrada con `Closes #n` | El Scrum Master |

### Tipos de cambio

| Tipo | Cuándo | Aprobación | Ejemplo real |
|---|---|---|---|
| **Estándar** | Cambio de bajo riesgo y repetible, sin efecto en el sistema desplegado (documentación, capturas, pruebas) | PR con aprobación del otro integrante | #197, informe 4.2.5 a 4.2.8 |
| **Normal** | Cambia código, datos o infraestructura y requiere evaluación | PR con aprobación, CI en verde y esta RFC en el cuerpo del PR | **#189, HU-27** (ejemplo del punto 3) |
| **Emergencia** | Corrige una caída o una vulnerabilidad en `main` | `hotfix/*` a `main` y a `develop` | **Ninguno hasta hoy** (no se usó la rama `hotfix/*`) |

La regla de protección de `develop` exige 1 aprobación y el CI en verde (`lint` y `test`); `enforce_admins` está desactivado, de modo que el administrador del repositorio podría saltarse la regla (se usó en los PR #152 a #156 del Sprint 1, ver [6.6](06_04_a_06_06_repositorio.md)).

## 2. Formato de la solicitud de cambio (RFC)

| Campo | Qué se anota |
|---|---|
| **ID** | `RFC-nnn` (correlativo) y el número del PR |
| **Fecha y solicitante** | Fecha de apertura y quién propone |
| **Descripción** | Qué se cambia, en una o dos frases |
| **Motivo** | Qué necesidad, historia de usuario (HU) o riesgo lo origina |
| **Tipo** | Estándar, normal o emergencia |
| **Componentes afectados** | Módulos, archivos, servicios y datos |
| **Impacto** | En usuarios, datos, rendimiento y otros cambios en curso |
| **Riesgo** | Qué puede salir mal (probabilidad × impacto, de 1 a 3) y cómo se mitiga |
| **Plan de implementación** | Pasos para desplegarlo (`-u`, scripts, orden de fusión) |
| **Plan de pruebas** | Pruebas automáticas, *smoke tests* y verificación manual |
| **Plan de reversa (*rollback*)** | Cómo volver al estado anterior y en cuánto tiempo |
| **Aprobación** | Quién autoriza y cuándo (revisión del PR) |
| **PR y release** | Enlace del PR, commit de fusión y tag de la release |
| **Resultado** | Qué pasó en la verificación, incidentes y lecciones |

## 3. Ejemplo lleno: RFC-001, endurecimiento del despliegue (HU-27)

| Campo | Contenido |
|---|---|
| **ID** | **RFC-001** · PR [#189](https://github.com/orlando572/erp-donofrio/pull/189) · épica [#140](https://github.com/orlando572/erp-donofrio/issues/140) (HU-25, HU-26, HU-27 y HU-29) |
| **Fecha y solicitante** | 23/11/2026 20:32 UTC · Orlando |
| **Descripción** | Poner Odoo detrás de Nginx con TLS 1.2/1.3 y HSTS; arrancar Odoo en modo producción (`workers = 2`, `proxy_mode`, `list_db = False`); exigir 2FA al administrador y al gerente; fijar la contraseña mínima en 12 caracteres y el bloqueo de login en 5 intentos por 60 s; auditar los cambios de precios, pedidos y compras con `auditlog` |
| **Motivo** | **HU-27** (5 puntos) y los requisitos **RNF009** (seguridad: RBAC, HTTPS, gestor de BD deshabilitado, 2FA) y **RNF010** (auditoría de cambios). Trata los riesgos RSI-02 a RSI-05, RSI-07, RSI-08, RSI-11 y RSI-15 de [5.10](05_10_a_05_12_seguridad.md) (fuerza bruta, contraseñas débiles, toma de cuenta privilegiada, tráfico sin cifrar, gestor de BD expuesto, configuración insegura, cambios sin rastro, cabeceras laxas) |
| **Tipo** | **Normal** (cambia infraestructura, configuración de seguridad y código) |
| **Componentes afectados** | Servicio `nginx` nuevo (`docker/nginx/odoo.conf.template` y `seguridad.conf`, perfil `proxy`); `docker/odoo/Dockerfile` (módulo OCA `auditlog` por commit fijo), `entrypoint.sh` y `odoo.conf.template`; `addons/donofrio_base`: `data/seguridad_data.xml`, grupo «2FA obligatorio», `res.users._mfa_type`, `depends` de `auth_totp_mail`, `auth_password_policy` y `auditlog`; scripts `levantar_prod.sh`, `generar_certificado.sh` y `verificar_despliegue.sh`; job `proxy` del CI; manual de instalación §6.2. **23 archivos, +659 y −8 líneas, 4 commits** |
| **Impacto** | **Usuarios:** el administrador y el gerente piden un código TOTP o por correo al iniciar sesión **solo** en el despliegue protegido; el resto inicia sesión igual. Contraseñas nuevas de 12 o más caracteres. **Datos:** instala `auditlog` y 4 reglas de auditoría; no modifica datos de negocio. **Rendimiento:** `workers = 2` y Nginx con gzip y caché de *assets*; en desarrollo no cambia (`workers = 0`). **Otros cambios en curso:** choca en archivos con HU-26 (`ci.yml`) y HU-23 (`__manifest__.py`, `tests/__init__.py`): se resolvió fusionando `develop` en la rama |
| **Riesgo** | **Bloquear a todos los usuarios** por el 2FA (probabilidad 2 × impacto 3 = 6, Alta). Mitigación: el parámetro `donofrio.2fa_privilegiados` (`auto`, `si` o `no`) y que solo se exija con `proxy_mode`; **el riesgo se materializó** en la primera versión (`_mfa_type` usaba `has_group` con el usuario público durante el login y devolvía 403 a todos), se detectó al probar en el despliegue y se corrigió con `sudo()` y una prueba de regresión. **Odoo no arranca en producción** con la contraseña de ejemplo o de menos de 16 caracteres (a propósito). **Bloqueo por IP y por *worker*:** con 2 *workers* el bloqueo aparece desde el intento 11 (límite aceptado, [5.11 C-03](05_10_a_05_12_seguridad.md)) |
| **Plan de implementación** | 1) Fusionar `develop` en la rama (HU-26 y HU-23 ya estaban en `develop`). 2) `docker compose build odoo` (descarga `auditlog` por commit). 3) Actualizar la base: `docker compose run --rm odoo odoo -d donofrio -u donofrio_base --stop-after-init` (instala `auditlog`, 2FA y política). 4) `scripts/levantar_prod.sh` con `ODOO_ADMIN_PASSWD` de 16 o más caracteres. 5) `scripts/verificar_despliegue.sh`. Documentado en el manual §6.2 |
| **Plan de pruebas** | `scripts/test.sh donofrio_base` (112 pruebas en ese momento; 136 al 23/11/2026 y 218 al 25/11/2026), de ellas 12 nuevas en `test_hardening.py` con la regresión del 403; `scripts/verificar_despliegue.sh` (TLS, cabeceras, gestor de BD, *assets*, *websocket*, configuración, contraseña de ejemplo y bloqueo de login) y job `proxy` del CI; verificación manual de la redirección del administrador y el gerente a `/web/login/totp`. Evidencia: `docs/capturas/sprint-3/HU-27_evidencia_seguridad.txt` |
| **Plan de reversa** | **Código:** revertir el commit de fusión `3c3150a` con un PR (`git revert 3c3150a`, un solo padre por ser *squash*); no se usa *force push* (prohibido en `develop`). **Servicio:** `docker compose --profile proxy down` apaga Nginx y `docker compose up -d` vuelve al modo de desarrollo (`workers = 0`, sin TLS). **2FA:** poner `donofrio.2fa_privilegiados = no` desde la base si alguien queda fuera sin tocar el código. **Datos:** `auditlog` no borra datos de negocio; antes de actualizar, `scripts/backup.sh` y, si hiciera falta, `scripts/restore.sh` en una base nueva (RTO medido: 31 s). **Plan de reversa preparado y no ejecutado:** no fue necesario |
| **Aprobación** | Evelyn (revisora): dos revisiones descartadas por nuevos *push* (20:35 y 20:38 UTC) y **aprobación a las 20:47 UTC**, con el CI en verde (`lint`, `test`, `replica`, `backup` y `proxy`) |
| **PR y release** | PR #189, fusionado con *squash* el 23/11/2026 20:47 UTC como `3c3150a` en `develop`. **Release:** al 23/11 aún sin tag; `v1.0.0` se publicó el 24/11/2026 con `docs/dev/release.md` (PR #222) |
| **Resultado** | **Exitoso, con observaciones.** El CI falló **2 veces** en el job `proxy` antes de la fusión (el chequeo de TLS y del bloqueo de login contaba mal; se corrigió en el mismo PR) y pasó a verde. Después, HU-28 midió el despliegue: ZAP baseline con **0 alertas altas** (6 → 4 medias tras ajustar las cabeceras de Nginx) y k6 con p95 de 12 ms ([6.13](06_09_a_06_13_pruebas.md), [5.14](05_13_a_05_14_pruebas.md)). **Lecciones:** probar el cambio de autenticación contra el despliegue real y no solo con el ORM (el 403 no lo vio una prueba unitaria); un conflicto aditivo en `ci.yml` se resuelve fusionando `develop`; aún falta `enforce_admins` activo (6.6) |

**Alineación con ITIL 4 e ISO/IEC 27001.** El ejemplo recorre todos los pasos de la habilitación del cambio y evidencia el control **8.32 Gestión de cambios** de la SoA ([10.6](anexo_10_06_soa_iso27001.md), estado *Parcial* por `enforce_admins` y por la plantilla de *issue* inexistente); COBIT BAI06 (cambios de TI).

## 4. Cambios del Sprint 3 clasificados (referencia)

Clasificación propuesta a partir del contenido de cada PR; el tipo no se registró en GitHub (no hay etiquetas `tipo:cambio-*`).

| PR | Cambio | Tipo propuesto |
|---|---|---|
| #186 (HU-25) | Réplica en *streaming* de PostgreSQL con perfil `replica` | Normal |
| #187 (HU-26) | Respaldo diario con retención de 7 días y restauración en una base nueva | Normal |
| **#189 (HU-27)** | **Nginx con TLS, modo producción, 2FA, política de contraseñas y auditoría** | **Normal (RFC-001)** |
| #190 (HU-29) | Publicar la imagen en GHCR y el zip en Releases con cada tag | Normal |
| #193 (HU-32) | Mesa de servicios en Project | Normal |
| #191, #192 (HU-33) | Pruebas integrales | Estándar |
| #197, #198 | Informe 4.2.5 a 4.2.8 y sección 5 | Estándar |
