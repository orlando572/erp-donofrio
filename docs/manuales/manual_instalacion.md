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

## 7. Actualizar, reiniciar y desinstalar

| Quiero… | Comando |
|---|---|
| Ver el estado | `docker compose ps` |
| Ver el registro de Odoo | `docker compose logs -f odoo` |
| Apagar y conservar los datos | `docker compose down` |
| Actualizar el módulo tras un `git pull` | `docker compose run --rm odoo odoo -d donofrio -u donofrio_base --stop-after-init` |
| **Empezar de cero** (borra la base y los archivos) | `docker compose down -v`, luego `docker compose up -d` y `scripts/init_db.sh` |

> **Importante:** los datos de configuración se cargan con `noupdate`. Si un cambio modifica esos datos (por ejemplo las recetas), `-u` **no** los actualiza: hay que recrear la base (última fila). Si cambias `DONOFRIO_USER_PASSWORD`, también.

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
- Pasos de despliegue en la nube (Nginx con TLS y copias de seguridad) cuando se completen en el Sprint 3.
