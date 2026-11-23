# Manual de instalación (borrador)

> **Estado:** borrador del Sprint 2 · **Autor:** Orlando · **Revisa:** Evelyn · Se completa y se exporta a PDF en el Cierre.
> Cubre el ERP de la **Fase 1** (Odoo 19 Community + PostgreSQL 16 en Docker). Los datos son ficticios.

## 1. Qué se instala

| Componente | Versión | Cómo llega |
|---|---|---|
| Odoo Community | 19.0 (imagen `odoo:19.0-20261112`, con la etiqueta fija) | Imagen de Docker construida desde `docker/odoo` |
| PostgreSQL | 16 | Imagen `postgres:16` |
| Módulo `donofrio_base` | 19.0.1.0.0 | Carpeta `addons/`, montada en el contenedor |

Todo corre en contenedores. No hace falta instalar Python, Odoo ni PostgreSQL en la PC.

## 2. Requisitos

- **Sistema:** Ubuntu 22.04 o superior, o Windows 10/11 con WSL2 y Ubuntu.
- **Recursos:** unos 4 GB de RAM libres y unos 6 GB de disco.
- **Software:** Docker con el plugin Compose, Git y `python3`. Para Windows, Docker Desktop con la integración WSL activada para Ubuntu.
- **Puertos libres en la PC:** 8069 (Odoo), 8072 (*websocket*) y 5432 (PostgreSQL). Si alguno está ocupado, se cambia en `.env` (paso 4.2).

## 3. Preparar la PC

### 3.1 Ubuntu

```bash
sudo apt update && sudo apt install -y git python3
```

Instala Docker Engine con el plugin Compose siguiendo la guía oficial de Docker para Ubuntu y comprueba:

```bash
docker --version && docker compose version
```

### 3.2 Windows 10 u 11 con WSL2

1. En PowerShell como administrador: `wsl --install -d Ubuntu`. Reinicia y crea tu usuario de Ubuntu.
2. Instala **Docker Desktop** y activa *Settings → Resources → WSL integration → Ubuntu*.
3. Abre la terminal de **Ubuntu** y sigue los pasos desde 3.1 (sin instalar Docker Engine).
4. Trabaja siempre **dentro de Ubuntu** (`~/`), nunca en `C:\` ni en `/mnt/c`: Docker es lento ahí y los saltos de línea cambian.

## 4. Instalar el ERP

### 4.1 Obtener el código

```bash
git clone https://github.com/orlando572/erp-donofrio.git ~/erp-donofrio
cd ~/erp-donofrio && git switch develop
```

### 4.2 Configurar el entorno

```bash
cp .env.example .env
```

`.env` no se sube al repositorio. Trae valores de desarrollo; estas son las variables que importan:

| Variable | Para qué sirve |
|---|---|
| `ODOO_DB` | Nombre de la base de datos (`donofrio`) |
| `DONOFRIO_USER_PASSWORD` | Contraseña de prueba de los 10 usuarios por rol. Se aplica **al instalar** el módulo |
| `ODOO_ADMIN_PASSWD`, `POSTGRES_PASSWORD`, `ODOO_DB_PASSWORD` | Claves de Odoo y PostgreSQL. Cámbialas si expones los puertos |
| `ODOO_PORT`, `ODOO_LONGPOLLING_PORT`, `DB_PORT` | Puertos publicados en `127.0.0.1` |

### 4.3 Levantar los contenedores

```bash
docker compose up -d --build
docker compose ps
```

La primera vez descarga las imágenes. Espera a que los dos servicios (`db` y `odoo`) aparezcan como `healthy`.

### 4.4 Crear la base de datos con los datos de la empresa

```bash
scripts/init_db.sh
```

Crea la base `donofrio` e instala `donofrio_base` (compañía peruana, almacenes, productos y recetas, usuarios, RR. HH. y listas de precios). Tarda cerca de un minuto. Es idempotente: si la base ya existe, no hace nada.

### 4.5 Cargar los datos de demostración (opcional)

Genera 16 semanas de inventario, recepciones, órdenes de producción con lote y reposiciones a Arequipa (del 3/8 al 22/11/2026, con semilla fija):

Detén antes el servicio web: sus tareas programadas corren sobre la misma base y pueden chocar con el script (error «could not serialize access due to concurrent update»).

```bash
docker compose stop odoo
docker compose run --rm -T odoo odoo shell -d donofrio --no-http < scripts/cargar_transacciones.py
docker compose up -d odoo
```

Tarda entre 5 y 8 minutos. Si ya hay datos de demostración, el script no carga nada; para repetir la carga hay que recrear la base (sección 7).

## 5. Entrar al sistema

Abre <http://localhost:8069> y entra con:

| Usuario | Contraseña | Uso |
|---|---|---|
| `admin` | `admin` | Administración y verificación (solo desarrollo; cámbiala si expones el puerto) |
| `jefe.almacen@donofrio.example.com` y los otros 9 de la lista del README | El valor de `DONOFRIO_USER_PASSWORD` en tu `.env` | Probar cada rol con sus permisos mínimos |

## 6. Verificar la instalación

```bash
scripts/test.sh donofrio_base
```

Instala el módulo en una base temporal y corre todas sus pruebas; imprime solo los errores y termina con `OK` si todo pasó. Para revisar patrones de versiones anteriores de Odoo: `scripts/check_legacy.sh`.

Qué deberías ver en la interfaz:

- **Inventario → Almacenes:** WH-LIM Planta Lima y WH-AQP CD Arequipa, con sus cámaras de frío.
- **Fabricación → Productos → Listas de materiales:** 12 recetas con sus operaciones.
- **Inventario → Productos → Números de serie/lote:** lotes con fecha de caducidad (si cargaste los datos de demostración).

### 6.1 Réplica de la base de datos (opcional)

Un segundo PostgreSQL (`db-replica`) copia al primero en *streaming* y solo permite leer. Agrega `REPLICADOR_PASSWORD` (y, si quieres, `REPLICA_PORT`) a tu `.env` como en `.env.example` y ejecuta:

```bash
docker compose --profile replica up -d --wait
scripts/verificar_replica.sh
```

La primera vez, `db` se recrea (sus datos se conservan) porque ahora carga el `pg_hba.conf` del repo; `db-replica` copia la base con `pg_basebackup`. El script comprueba `pg_stat_replication` (estado `streaming`), `pg_is_in_recovery()` en la réplica, que un dato escrito en el primario llegue a la réplica y que un `INSERT` en la réplica falle con `read-only transaction`. Para leer desde DBeaver: `localhost:5433` con el usuario `odoo`. Para apagarla: `docker compose --profile replica stop db-replica`; para recrearla desde cero: `docker compose --profile replica rm -sf db-replica && docker volume rm erp-donofrio_pgdata-replica`.

### 6.2 Despliegue protegido: Nginx con TLS y Odoo en modo producción

Para la demo «en producción» (y para las pruebas de carga y de seguridad) se levanta Odoo detrás de Nginx. En tu `.env` pon una `ODOO_ADMIN_PASSWD` de **16 caracteres o más** (no la de ejemplo: en este modo Odoo se niega a arrancar con ella) y ejecuta:

```bash
scripts/levantar_prod.sh          # certificado autofirmado + Odoo con workers=2 y proxy_mode + Nginx
scripts/verificar_despliegue.sh   # comprueba TLS, cabeceras, gestor de BD, assets, websocket, configuración y bloqueo
```

Entra por `https://localhost:8443` (acepta la advertencia: el certificado es autofirmado; en una VM real se cambia por Let's Encrypt). `http://localhost:8080` redirige a HTTPS. Para volver a desarrollo: `docker compose --profile proxy down && docker compose up -d`.

Qué protege (todo por código, ver `docker/nginx/` y `donofrio_base`):

| Control | Cómo |
|---|---|
| Cifrado en tránsito (A.8.24) | TLS 1.2 y 1.3, HSTS y redirección 80 → 443 en `docker/nginx/odoo.conf.template` |
| Gestor de bases de datos | `list_db = False` en Odoo y `/web/database/*` responde 404 en Nginx |
| Contraseña maestra | Viene de `.env` (en GitHub, de Secrets) o de un archivo (`ODOO_ADMIN_PASSWD_FILE`); en modo producción debe tener 16+ caracteres |
| Contraseñas de usuario (A.5.17) | Mínimo 12 caracteres (`auth_password_policy`), guardadas con hash PBKDF2 |
| Bloqueo por intentos (A.8.5) | 5 fallos, espera de 60 s (`base.login_cooldown_*`). El contador de Odoo es **por IP y por worker**: con 2 workers puede tardar hasta 10 fallos en bloquear |
| 2FA (A.8.5 y A.8.2) | El administrador y el gerente (grupo «2FA obligatorio») piden código en el despliegue protegido. Quien activó su app de autenticación (Preferencias → Seguridad → Activar autenticación de dos factores) la usa; quien no, recibe un código por correo, **lo que requiere configurar un servidor de correo saliente**. Parámetro `donofrio.2fa_privilegiados`: `auto` (por defecto, solo con proxy), `si` o `no` |
| Auditoría (A.8.15, RNF010) | `auditlog` (OCA, fijado por commit en el Dockerfile) registra quién, cuándo y el valor anterior y nuevo de listas de precios, pedidos de venta y órdenes de compra (Ajustes → Técnico → Auditoría) |

Los usuarios de prueba (`DONOFRIO_USER_PASSWORD`) tienen 18 caracteres y cumplen la política. Si tu `.env` tiene una más corta, la instalación de `donofrio_base` fallará: usa 12 o más.

### 6.3 Pruebas de carga y de seguridad (opcional)

Con el despliegue protegido levantado (§6.2) y la base con datos de demostración (§4.5): `scripts/perf/k6.sh` (20 usuarios virtuales con k6, umbral de RNF002: p95 < 2 s) y `scripts/perf/zap.sh` (OWASP ZAP baseline, sin alertas altas). Cómo se leen los reportes y qué resultados dieron: [docs/dev/pruebas_no_funcionales.md](../dev/pruebas_no_funcionales.md).

## 7. Actualizar, reiniciar y desinstalar

| Quiero… | Comando |
|---|---|
| Ver el estado | `docker compose ps` |
| Ver el registro de Odoo | `docker compose logs -f odoo` |
| Apagar y conservar los datos | `docker compose down` |
| Actualizar el módulo tras un `git pull` | `docker compose run --rm odoo odoo -d donofrio -u donofrio_base --stop-after-init` |
| **Empezar de cero** (borra la base y los archivos) | `docker compose down -v`, luego `docker compose up -d` y `scripts/init_db.sh` |

> **Importante:** los datos de configuración se cargan con `noupdate`. Si un cambio modifica esos datos (por ejemplo las recetas), `-u` **no** los actualiza: hay que recrear la base (última fila). Si cambias `DONOFRIO_USER_PASSWORD`, también.

### 7.1 Copias de seguridad y restauración

```bash
scripts/backup.sh                                   # respaldo ahora
scripts/restore.sh backups/donofrio_AAAAMMDD_HHMMSS  # restaura en una BD nueva (donofrio_restaurada)
scripts/verificar_backup.sh                          # prueba el ciclo completo con una BD temporal
```

`backup.sh` guarda en `backups/` (carpeta ignorada por git) tres archivos por corrida: el `.dump` de la base (`pg_dump -Fc`), el `_filestore.tar.gz` con los adjuntos y un `.sha256`; y borra los respaldos de más de 7 días. `restore.sh` **nunca sobrescribe**: crea una base nueva, comprueba las sumas, restaura la base y el filestore y muestra el tiempo (RTO medido; el objetivo es 2 horas). Para abrir la base restaurada en Odoo: `ODOO_DB=donofrio_restaurada docker compose up -d odoo` (y luego vuelve a dejar `ODOO_DB` como estaba).

Para que sea diario, agrega al `crontab -e` del equipo (02:00): `0 2 * * * cd /ruta/a/ERP-Donofrio && scripts/backup.sh >> backups/backup.log 2>&1`. Para tener la copia fuera del equipo, define `BACKUP_DIR` en `.env` con una carpeta sincronizada (o copia `backups/` a un disco externo).

## 8. Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `port is already allocated` al levantar | Otro programa usa 8069, 8072 o 5432 | Cambia `ODOO_PORT`, `ODOO_LONGPOLLING_PORT` o `DB_PORT` en `.env` y repite `docker compose up -d` |
| Odoo no abre y `docker compose ps` no muestra `healthy` | Todavía está iniciando, o falló la base | `docker compose logs odoo`; espera un minuto y revisa |
| Los usuarios por rol no pueden entrar | `DONOFRIO_USER_PASSWORD` no estaba en `.env` al crear la base | Define la variable y recrea la base (sección 7) |
| Muy lento en Windows | El repositorio está en `C:\` o `/mnt/c` | Clónalo dentro de Ubuntu (`~/erp-donofrio`) |
| `scripts/init_db.sh` dice que la base ya existe | La base se creó antes | Es normal; para recrearla, usa «Empezar de cero» |
| El script de datos de demostración falla con «could not serialize access due to concurrent update» | El servicio web corría a la vez y sus tareas programadas tocaron las mismas existencias | Recrea la base (sección 7), detén el servicio web (`docker compose stop odoo`) y repite la carga |

## 9. Pendiente para el Cierre

- Capturas de cada paso en una PC limpia y la prueba con Evelyn siguiendo solo este manual.
- Despliegue en una VM en la nube (Let's Encrypt en lugar del certificado autofirmado y servidor de correo para el 2FA por correo), solo si se decide hacerlo.
