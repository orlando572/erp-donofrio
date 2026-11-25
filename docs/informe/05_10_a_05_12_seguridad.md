# 5.10 a 5.12 Gestión de seguridad de la información: riesgos, controles, ataques y defensa

> **Estado:** versión final del Cierre (25/11/2026; los datos medidos son los del 23/11/2026 salvo donde se indica) · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [02 §2.2](../plan/02_mapeo_plantilla.md), [09 §9.2, §9.6](../plan/09_normas_marcos.md), [07](../plan/07_riesgos_entrega.md), [el registro de riesgos](../pm/plan_riesgos.md)
>
> Mide el **estado real de `develop` al 23/11/2026** (HU-04, HU-27 y HU-28); los módulos de la Fase 2 (M1 a M4, 24 y 25/11/2026) no cambiaron los controles de esta sección: sus permisos están en [5.5b a 5.5e](05_05_modulo_donofrio_calidad.md) y la protección de `main` pasó a exigir `lint` y `test` (ver [4.3.1](04_03_infraestructura.md)). **La Declaración de Aplicabilidad (SoA) completa y la trazabilidad norma → control → evidencia no se repiten aquí:** están en el anexo 10.6. Esta sección solo usa de la norma lo necesario para identificar cada riesgo, su control y su prueba.
>
> *El proyecto se **alinea** con las normas y marcos citados como buenas prácticas de referencia. No constituye una implementación certificada ni auditada de ninguno de ellos; la Declaración de Aplicabilidad y las evidencias tienen fines académicos.*

**Método.** ISO 31000 (identificar, analizar, evaluar, tratar), con las **mismas escalas del plan de riesgos** ([4.5.1](../pm/plan_riesgos.md)): impacto (I) y probabilidad (P) de 1 a 3; **nivel = I × P**; prioridad **Alta** (6–9), **Media** (3–5) o **Baja** (1–2). Los riesgos de esta sección se enfocan en el sistema desplegado; los de gestión del proyecto están en el plan de riesgos y aquí se enlazan por su identificador (R8, RS-02, RS-03, RS-04).

**Activos:** (1) los datos del negocio (pedidos, clientes, lotes, precios, facturas); (2) las cuentas de usuario y sus permisos; (3) la base de datos PostgreSQL y el *filestore*; (4) el servicio web; (5) el código y las imágenes del repositorio.

## 5.10 Identificación de riesgos de seguridad

### Tabla 16. Riesgos de seguridad de la información (antes de los controles)

| ID | Activo | Riesgo (amenaza → consecuencia) | I | P | Nivel | Prioridad | Plan de riesgos |
|---|---|---|---|---|---|---|---|
| RSI-01 | Datos, cuentas | Un usuario con permisos de más lee o cambia datos de otra área o de otro almacén (control de acceso roto) | 3 | 2 | 6 | Alta | — |
| RSI-02 | Cuentas | Adivinar contraseñas por fuerza bruta o relleno de credenciales en el login web | 3 | 2 | 6 | Alta | — |
| RSI-03 | Cuentas | Contraseñas cortas o de ejemplo en uso | 3 | 2 | 6 | Alta | — |
| RSI-04 | Cuentas | Toma de control de la cuenta del administrador o del gerente (privilegios máximos) con solo la contraseña | 3 | 2 | 6 | Alta | — |
| RSI-05 | Datos, sesión | Intercepción del tráfico o robo de la sesión si el sitio se sirve por HTTP | 3 | 2 | 6 | Alta | — |
| RSI-06 | Datos | Inyección SQL o XSS por una entrada de usuario (búsquedas, parámetros, formularios) | 3 | 2 | 6 | Alta | — |
| RSI-07 | Base de datos | El gestor de bases de datos de Odoo o el puerto de PostgreSQL quedan expuestos | 3 | 2 | 6 | Alta | RS-03 |
| RSI-08 | Servicio | Despliegue con configuración insegura: `admin_passwd` de ejemplo, modo debug, workers en 0 | 3 | 2 | 6 | Alta | — |
| RSI-09 | Datos | Pérdida o corrupción de la base o del *filestore* (disco, error humano, fallo del contenedor) | 3 | 2 | 6 | Alta | R8, RS-04 |
| RSI-10 | Servicio | Indisponibilidad: se cae un contenedor o el equipo en temporada alta | 2 | 2 | 4 | Media | — |
| RSI-11 | Datos | Cambios no autorizados o sin rastro en precios, pedidos u órdenes de compra (fraude o error) | 3 | 2 | 6 | Alta | — |
| RSI-12 | Código, secretos | Contraseñas o llaves publicadas en el repositorio público | 3 | 2 | 6 | Alta | RS-02 |
| RSI-13 | Código | Componentes de terceros vulnerables o alterados (imagen de Odoo, módulo OCA, acciones de GitHub) | 2 | 2 | 4 | Media | — |
| RSI-14 | Código | Código defectuoso o malicioso llega a `develop` o `main` sin revisión ni pruebas | 2 | 2 | 4 | Media | — |
| RSI-15 | Servicio | Cabeceras de seguridad ausentes o laxas (clickjacking, CSP, cookies sin `Secure`) | 2 | 2 | 4 | Media | — |
| RSI-16 | Datos personales | Exposición de datos personales de clientes o empleados (Ley 29733) | 2 | 1 | 2 | Baja | — |

*Nota.* La probabilidad es la de un sistema sin los controles de 5.11 y expuesto a una red real; el proyecto se ejecuta hoy en un solo equipo, de modo que muchas de estas probabilidades son menores en la práctica (por eso la matriz de [4.5.1](../pm/plan_riesgos.md) pone RS-03 en P = 1).

## 5.11 Identificación de controles de seguridad

### Escalas

| Valor | Eficacia del control | Significado |
|---|---|---|
| 3 | Alta | Automático y **verificado** con una prueba repetible (test de Odoo, script o CI) |
| 2 | Media | Implementado y verificado una vez, con alguna limitación declarada, o que depende de una acción manual |
| 1 | Baja | Solo documentado o sin verificar |

**Estado:** *Implementado* (existe en `develop` y se verificó), *Parcial* (existe con una limitación importante) o *No implementado*. El **riesgo residual** se vuelve a calcular con I × P después del control y con la misma escala de 4.5.1.

### Tabla 17. Controles de seguridad, eficacia y riesgo residual

| ID | Control (cómo está implementado) | Trata | ISO 27001:2022 · OWASP | Tipo | Efic. | Estado | Residual (I×P) | Evidencia |
|---|---|---|---|---|---|---|---|---|
| C-01 | **Mínimo privilegio:** 10 usuarios por rol sin administradores, grupo «Solo operaciones del CD Arequipa», 4 `ir.rule` y 1 ACL (`donofrio_security.xml`, `ir.model.access.csv`) | RSI-01 | 5.15, 5.18, 8.3 · A01 | Preventivo | 3 | Implementado | 3×1 = 3 Media | `test_seguridad.py` (9 pruebas, `AccessError` al operar en otro almacén; vendedor y cajero sin acceso a compras). Límite: las reglas por registro cubren solo el inventario; las de calidad y heladeros son de la Fase 2 (no existen) |
| C-02 | **Política de contraseñas:** `auth_password_policy.minlength = 12`; contraseñas con hash PBKDF2-SHA512 (600 000 iteraciones) | RSI-03 | 5.17 · A07 | Preventivo | 2 | Implementado | 3×1 = 3 Media | `test_hardening.py` (rechaza una corta, acepta una de 12); consulta SQL con el hash en la evidencia de seguridad. Límite: solo se exige longitud, no complejidad |
| C-03 | **Bloqueo por intentos fallidos:** `base.login_cooldown_after = 5` y `base.login_cooldown_duration = 60` | RSI-02 | 8.5 · A07 | Preventivo | 2 | Implementado | 3×1 = 3 Media | `test_bloqueo_tras_5_intentos_por_60_s`; `verificar_despliegue.sh` paso 7 (HU-27: 10 de 12 intentos rechazados con «Too many login failures»; HU-28, con el script corregido para contar *workers*: 2 de 12) y el registro `Login attempt ignored`. Límite: el contador es **por IP y por *worker***: con 2 *workers* y umbral 5, el bloqueo solo es seguro desde el intento 11 |
| C-04 | **Segundo factor** para el administrador y el gerente (grupo «2FA obligatorio»): TOTP o código por correo (`auth_totp_mail`) cuando `proxy_mode` está activo | RSI-04, RSI-02 | 8.5, 8.2 · A07 | Preventivo | 3 | Implementado | 3×1 = 3 Media | `test_hardening.py` (6 pruebas del 2FA); HU-27: `admin` y `gerente` reciben `303 → /web/login/totp`; `vendedor`, `303 → /odoo`. Límites: solo se exige en el despliegue protegido (el parámetro `donofrio.2fa_privilegiados` lo fuerza o lo apaga); el código por correo necesita un servidor de correo que el proyecto no configura |
| C-05 | **Cifrado en tránsito:** Nginx con TLS 1.2 y 1.3, redirección 80 → 443 y HSTS (`max-age=31536000`) | RSI-05 | 8.24, 8.20 · A02 | Preventivo | 3 | Implementado | 3×1 = 3 Media | `verificar_despliegue.sh` (pasos 1 a 3: acepta TLS 1.2 y 1.3, **rechaza 1.1 y menores**); `openssl s_client`: TLSv1.3. Límite: certificado **autofirmado** de la demo |
| C-06 | **Cabeceras y cookies seguras** en `docker/nginx/seguridad.conf`: CSP, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-Opener-Policy`; cookies `Secure; HttpOnly; SameSite=Lax` | RSI-15, RSI-05, RSI-06 | 8.9, 8.20 · A05 | Preventivo | 2 | Implementado | 2×1 = 2 Baja | ZAP: 6 → 4 alertas medias y 7 → 3 bajas, **0 altas** (HU-28). Límite: la CSP necesita `unsafe-inline` y `unsafe-eval` porque OWL compila con `new Function`; es una limitación de Odoo 19, aceptada con su motivo |
| C-07 | **Solo ORM, sin SQL crudo**, y escape automático de QWeb | RSI-06 | 8.28, 8.25 · A03 | Preventivo | 3 | Implementado | 3×1 = 3 Media | Búsqueda con `' OR '1'='1` y `x'); DROP TABLE…` → 0 filas y la tabla intacta; el parámetro `redirect` con `<script>` sale escapado ([evidencia](../capturas/sprint-3/S3-informe5_evidencia_inyeccion_xss.txt)); `grep` de `cr.execute` en `addons/`: sin resultados |
| C-08 | **Gestor de bases de datos cerrado** (`list_db = False`, `dbfilter`), Nginx responde 404 a `/web/database/`, puertos de PostgreSQL y de Odoo solo en `127.0.0.1`, `scram-sha-256` | RSI-07 | 8.20, 8.9 · A05 | Preventivo | 3 | Implementado | 3×1 = 3 Media | `verificar_despliegue.sh` paso 4 (`/web/database/manager` y `/create` → 404); `docker compose ps` (HU-27): `127.0.0.1:5432`. Límite: Nginx publica 8080 y 8443 en **todas** las interfaces (así lo pide la demo) |
| C-09 | **Despliegue endurecido:** `entrypoint.sh` rechaza una `admin_passwd` de menos de 16 caracteres o de ejemplo con `proxy_mode`; `workers = 2`; sin modo debug; `.env` fuera de Git y secretos solo por entorno o archivo | RSI-08, RSI-03, RSI-12 | 8.9, 8.31 · A05 | Preventivo | 3 | Implementado | 3×1 = 3 Media | `verificar_despliegue.sh` paso 6; `probar_imagen.sh` («la contraseña de ejemplo se rechaza») |
| C-10 | **Respaldos:** `backup.sh` (dump + *filestore* + SHA-256, retención de 7 días) y `restore.sh` (solo a una base nueva, con RTO medido) | RSI-09 | 8.13 (ISO 22301) | Correctivo | 2 | Implementado | 2×2 = 4 Media | la evidencia del respaldo: **RTO de 31 s** (objetivo 2 h); `verificar_backup.sh` y job `backup` del CI. Límites: el *cron* diario está documentado y no instalado; los respaldos no se cifran y viven en el mismo equipo salvo que `BACKUP_DIR` apunte a otro |
| C-11 | **Réplica en *streaming*** de solo lectura (copia caliente) | RSI-09, RSI-10 | 8.14 (ISO 22301) | Correctivo | 2 | Implementado | 2×2 = 4 Media | la evidencia de la réplica; job `replica` del CI. Límites: asíncrona, sin *failover* automático, **promoción no probada** |
| C-12 | **Auditoría de cambios:** `auditlog` (OCA) sobre listas de precios y sus líneas (crear, modificar, borrar) y sobre pedidos de venta y de compra (modificar, borrar); *chatter* estándar | RSI-11 | 8.15, 8.16 · A09 | Detectivo | 3 | Implementado | 3×1 = 3 Media | `test_hardening.py` (`test_cambio_de_precio_queda_auditado`); HU-27: el cambio 15 → 20 → 15 del jefe de ventas con usuario, fecha, valor anterior y nuevo |
| C-13 | **Reinicio automático y *healthcheck*:** `restart: unless-stopped` y `GET /web/health` cada 15 s en Odoo, `pg_isready` en PostgreSQL | RSI-10 | 8.14, 5.30 | Correctivo | 1 | Parcial | 2×2 = 4 Media | `docker inspect`: política `unless-stopped` y estado `healthy` en los tres contenedores. Límite: **no hay medición de disponibilidad** (Uptime Kuma no se implementó), un solo nodo |
| C-14 | **Cambios controlados:** PR a `develop` con 1 aprobación del otro integrante, conversaciones resueltas y CI (`lint` y `test`) obligatorio; *force push* prohibido; releases solo desde `main` | RSI-14 | 8.32, 8.25, 8.31 · A08 | Preventivo | 2 | Parcial | 2×1 = 2 Baja | Reglas de protección verificadas con la API de GitHub el 23/11/2026. Límites: `enforce_admins` desactivado (en el Sprint 1 hubo fusiones como administrador, documentadas en [4.3.1](04_03_infraestructura.md)); `main` exige 1 aprobación pero **no** checks obligatorios |
| C-15 | **Versiones fijadas:** `odoo:19.0-20261112`, `postgres:16`, imágenes de k6, ZAP y PlantUML con versión, `auditlog` por **commit**; `ruff` 0.8.4 | RSI-13 | 8.8 · A06 | Preventivo | 2 | Parcial | 2×1 = 2 Baja | `docker/odoo/Dockerfile`; 5.3. Límite: **Dependabot no está configurado** (no hay `.github/dependabot.yml` y las actualizaciones de seguridad están desactivadas); el plan lo contemplaba |
| C-16 | **Secretos:** `secret scanning` y `push protection` activos en el repositorio; `.env` en `.gitignore`; solo `GITHUB_TOKEN` en Actions | RSI-12 | 8.9 · A05 | Preventivo | 2 | Implementado | 3×1 = 3 Media | `gh api repos/orlando572/erp-donofrio` el 23/11/2026: `secret_scanning` y `secret_scanning_push_protection` = `enabled`. Límite: el repositorio es público y la contraseña de prueba de los usuarios está en `.env.example` (valor de desarrollo, no de producción) |
| C-17 | **Pruebas de seguridad:** ZAP *baseline* (pasivo) sobre el despliegue protegido y tests de acceso | RSI-15, RSI-01 | 8.29 · A05 | Detectivo | 2 | Implementado | — | 5.14; `HU-28_zap_reporte.html`. Límite: sin sesión y sin análisis activo |
| C-18 | **Datos ficticios y mínimos**; campos privados de empleados protegidos por Odoo (grupo de RR. HH.) | RSI-16 | 5.34 | Preventivo | 2 | Parcial | 2×1 = 2 Baja | RUC `20999999990` inventado, correos `.example.com`; RNF013 «Parcial» en [4.2.3](04_02_requerimientos_funcionales.md). No hay política de privacidad ni consentimiento: no aplica con datos ficticios |

**Lectura.** Los 11 riesgos de prioridad **Alta** de la Tabla 16 pasan a nivel residual 3 o 4 (**Media**) y los demás quedan en Media o Baja: **ninguno queda en prioridad Alta**. Los residuales «Media» más relevantes dependen de supuestos del despliegue en un solo equipo (RSI-09 y RSI-10: respaldos sin *cron* instalado y sin medición de disponibilidad). Controles **no implementados** que el plan nombraba: Uptime Kuma, Dependabot y la cinta de entorno de OCA (`web_environment_ribbon`).

## 5.12 Identificación de ataques y defensa

### Tabla 18. Ataques, defensa y prueba

| Ataque | OWASP 2021 | Cómo se intenta | Defensa en el proyecto | Prueba realizada | Resultado y límite |
|---|---|---|---|---|---|
| **Inyección SQL** | A03 | Comillas y sentencias SQL en un filtro de búsqueda (`' OR '1'='1`, `x'); DROP TABLE res_partner;--`) | Solo ORM (consultas parametrizadas); `addons/` sin SQL crudo (C-07) | Dos intentos reales con JSON-RPC como el cliente web, usuario `jefe.ventas`, base `donofrio` | **Rechazado**: 0 filas en ambos, la tabla sigue con 60 contactos. Límite: prueba manual puntual, no un escaneo activo de ZAP |
| **XSS** | A03 | `"><script>alert(1)</script>` en el parámetro `redirect` de `/web/login` (el punto que ZAP marcó como atributo controlable) | Escape automático de QWeb; CSP `default-src 'self'` con `object-src`, `base-uri` y `form-action` cerrados | GET con el parámetro malicioso; ZAP baseline | El texto sale **escapado** (`&lt;script&gt;`); ZAP lo clasificó informativo y se comprobó como falso positivo. Límite: la CSP admite `unsafe-inline` y `unsafe-eval` (OWL), de modo que **no impediría** un XSS que lograra inyectar un script |
| **Fuerza bruta** | A07 | Intentos repetidos de contraseña en `/web/login` | Bloqueo tras 5 intentos por 60 s; contraseñas de 12+; 2FA al administrador y al gerente (C-02, C-03, C-04) | `test_bloqueo_tras_5_intentos_por_60_s` y `verificar_despliegue.sh` paso 7 | **Mitigado**: con 2 *workers* el bloqueo aparece a partir del intento 11 (2 de 12 rechazados en la verificación de HU-28; 10 de 12 en la de HU-27) y deja `Login attempt ignored` en el registro. Límite: el contador es por IP y por *worker* y la espera dura solo 60 s |
| **Gestor de BD o PostgreSQL expuestos** | A05 | Pedir `/web/database/manager` o conectarse al puerto 5432 desde otra máquina | `list_db = False`, 404 en Nginx, puertos en `127.0.0.1`, `scram-sha-256` (C-08) | `verificar_despliegue.sh` paso 4 y ZAP | **Rechazado**: `/web/database/manager` y `/create` → 404. Límite: PostgreSQL sin TLS dentro de Docker |
| **Robo de sesión** | A02, A07 | Leer la cookie por JavaScript o capturarla en la red; clickjacking | `session_id` con `HttpOnly; Secure; SameSite=Lax`; TLS 1.2/1.3 y HSTS; `X-Frame-Options: SAMEORIGIN`; 2FA (C-04, C-05, C-06) | `curl -skI https://localhost:8443/web/login`, `openssl s_client`, ZAP | **Mitigado**: cookie con las tres banderas; TLS 1.1 rechazado. Límites: certificado autofirmado; la cookie `frontend_lang` sin `HttpOnly` (la lee el JavaScript de Odoo; no guarda sesión); la cookie de sesión dura 7 días (`Max-Age=604800`) |
| **Pérdida de datos** | A04 (diseño), ISO 22301 | Borrado accidental, disco dañado o base corrupta | Respaldos con sumas, retención de 7 días, restauración en base nueva y réplica en *streaming* (C-10, C-11) | `verificar_backup.sh` (6 comprobaciones) y restauración cronometrada | **Recuperable**: RTO 31 s (objetivo 2 h); un respaldo alterado se rechaza. Límites: sin *cron* instalado, sin cifrado, copia en el mismo equipo |
| **Caída del servicio** | ISO 22301 | Un contenedor se cae o se agota la CPU | `restart: unless-stopped`, *healthchecks*, `workers = 2`; capacidad medida con k6 (C-13) | k6 normal (20 usuarios) y de esfuerzo (sin pausas); `docker stats` | **Resiste** la carga medida: 0 % de errores en la normal y 0.005 % en la de esfuerzo, CPU de Odoo hasta 160 %. Límites: un solo nodo, sin medición de disponibilidad y la réplica no toma el control sola |

**Otras categorías OWASP con evidencia.** *A05 Mala configuración:* ZAP baseline con 0 alertas altas y 58 reglas pasivas sin hallazgo (5.14). *A06 Componentes vulnerables:* imagen y OCA fijados, Dependabot sin configurar (C-15). *A09 Registro y monitoreo:* `auditlog`, *chatter* y `res_users_log` (HU-27: inicios de sesión registrados). *A08 Integridad:* CI obligatorio y ramas protegidas (C-14). *A10 SSRF:* no aplica: los módulos propios no hacen peticiones a URLs del usuario.

### Evidencias de seguridad (archivos del repositorio)

| Evidencia | Archivo |
|---|---|
| Despliegue protegido, 2FA, TLS, cabeceras, parámetros, hash, auditoría y bloqueo | [la evidencia de seguridad](../capturas/sprint-3/HU-27_evidencia_seguridad.txt) |
| ZAP antes y después, cabeceras y cookies | [la evidencia de k6 y ZAP](../capturas/sprint-3/HU-28_evidencia_k6_zap.txt), [`HU-28_zap_reporte.html`](../capturas/sprint-3/HU-28_zap_reporte.html), [`.json`](../capturas/sprint-3/HU-28_zap_reporte.json) |
| Alertas aceptadas con su motivo | [el procedimiento de pruebas no funcionales](../dev/pruebas_no_funcionales.md) y `scripts/perf/zap-reglas.conf` |
| Inyección SQL y XSS | [la evidencia de inyección y XSS](../capturas/sprint-3/S3-informe5_evidencia_inyeccion_xss.txt) |
| Respaldo y réplica | [la evidencia del respaldo](../capturas/sprint-3/HU-26_evidencia_respaldo.txt), [la evidencia de la réplica](../capturas/sprint-3/HU-25_evidencia_replica.txt) |
| Pruebas de acceso | `addons/donofrio_base/tests/test_seguridad.py` y `test_hardening.py` (21 pruebas, en el CI) |
