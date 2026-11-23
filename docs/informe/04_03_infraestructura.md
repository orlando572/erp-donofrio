# 4.3 Back-end y despliegue: infraestructura y contenedores

> **Estado:** borrador del Sprint 1 · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [06 §6.5](../plan/06_github_ci_infra.md), [02 §2.2](../plan/02_mapeo_plantilla.md)
>
> Las secciones 4.3.2 a 4.3.6 y 4.3.8 son de los Sprints 2 y 3. Aquí van solo 4.3.1 y 4.3.7.

## 4.3.1 Infraestructura tecnológica

El ERP corre sobre contenedores en la PC de cada integrante (Ubuntu o Ubuntu dentro de WSL2). El mismo `docker-compose.yml` y la misma imagen de Odoo con etiqueta fechada (`odoo:19.0-20261112`) se usan en las dos PC y en el CI de GitHub, de modo que el entorno es reproducible con un solo comando (RNF012).

![Infraestructura tecnológica](../diagramas/arquitectura/infraestructura.png)

*Figura 4.3.1-a. Infraestructura tecnológica. Línea continua: ya existe en `develop`. Línea punteada: planificado (Sprint 3) u opcional. Se genera con [`generar_arquitectura.py`](../diagramas/generar_arquitectura.py).*

| Elemento | Qué es | Estado |
|---|---|---|
| **PC de desarrollo** | Ubuntu nativo o WSL2 con Docker Engine y el plugin Compose; unos 4 GB de RAM libres. Una por integrante | En uso |
| **Contenedor `odoo`** | Imagen propia (`docker/odoo/Dockerfile`) sobre `odoo:19.0-20261112`; HTTP en 8069 y *websocket* en 8072, solo en `127.0.0.1`; monta `./addons` en modo lectura | En uso |
| **Contenedor `db`** | `postgres:16` con el rol `odoo` sin superusuario; puerto 5432 solo en `127.0.0.1` para DBeaver | En uso |
| **Contenedor `db-replica`** | Segundo `postgres:16` en *hot standby* de solo lectura (perfil `replica`, puerto 5433) | Planificado (HU-25, Sprint 3) |
| **Contenedor `nginx`** | Proxy inverso con TLS, gzip y caché de *assets* (perfil `proxy`, puertos 80 y 443) | Planificado (HU-27, Sprint 3) |
| **GitHub** | Repositorio público, Projects e Issues; ramas `main`, `develop` y `feature/HU-xx` con protección | En uso |
| **GitHub Actions** | *Runner* `ubuntu-24.04` efímero; job `lint` (`check_legacy.sh` y `ruff`) y job `test` (`docker compose` y `scripts/test.sh`) en cada PR | En uso (HU-02) |
| **GHCR** | Registro de imágenes (`ghcr.io/orlando572/erp-donofrio`); una imagen y un zip del código por cada tag `v*` | Planificado (HU-29) |
| **VM en la nube** | Oracle Free u otra, con Compose, Nginx y Let's Encrypt; despliegue por SSH desde Actions | Opcional (decisión abierta) |

**Seguridad de la infraestructura ya aplicada:** los puertos solo escuchan en `127.0.0.1`; el gestor de bases de datos de Odoo está deshabilitado (`list_db = False`); la contraseña maestra y las claves de PostgreSQL salen de `.env`, que no se sube al repositorio; el rol de la aplicación no es superusuario de PostgreSQL.

## 4.3.7 Máquinas virtuales y contenedores

La plataforma de contenedores es **Docker Compose** (un archivo `docker-compose.yml` en la raíz del repositorio). No se usan máquinas virtuales en desarrollo; la VM en la nube es opcional (4.3.8).

### Servicios

| Servicio | Imagen | Perfil | Puertos publicados | Volumen | Salud y reinicio |
|---|---|---|---|---|---|
| `db` | `postgres:16` | (siempre) | `127.0.0.1:5432` → 5432 | `pgdata` → `/var/lib/postgresql/data` | `pg_isready` cada 5 s, 10 reintentos · `restart: unless-stopped` |
| `odoo` | `erp-donofrio/odoo:19.0` (construida desde `docker/odoo`) | (siempre) | `127.0.0.1:8069` → 8069 · `127.0.0.1:8072` → 8072 | `odoo-data` → `/var/lib/odoo` · `./addons` → `/mnt/extra-addons` (solo lectura) | `GET /web/health` cada 15 s, inicio con 30 s de gracia · `depends_on: db` (saludable) · `restart: unless-stopped` |
| `db-replica` | `postgres:16` | `replica` | 5433 | propio | Planificado (HU-25) |
| `nginx` | `nginx:stable` | `proxy` | 80 y 443 | configuración de `docker/nginx/` | Planificado (HU-27) |
| `schemaspy` | `schemaspy/schemaspy` | `tools` | — | `docs/diagramas/schemaspy/` | Planificado (Sprint 3) |

### Volúmenes y red

| Recurso | Tipo | Contenido | Cómo se borra |
|---|---|---|---|
| `erp-donofrio_pgdata` | Volumen local | Base de datos PostgreSQL | `docker compose down -v` |
| `erp-donofrio_odoo-data` | Volumen local | *Filestore* de Odoo (adjuntos, sesiones) | `docker compose down -v` |
| `erp-donofrio_default` | Red `bridge` | Red interna; los servicios se ven por nombre (`db`, `odoo`) | `docker compose down` |

### Configuración

- **Variables de entorno:** `.env` (copia de `.env.example`; no se versiona) define la base de datos, las contraseñas de prueba y los puertos. Compose las inyecta y el `entrypoint.sh` de la imagen genera `odoo.conf` a partir de `docker/odoo/odoo.conf.template`.
- **Primer arranque:** `scripts/init_db.sh` crea la base de datos `donofrio` e instala `donofrio_base`; es idempotente.
- **Base de datos:** el rol `odoo` lo crea `docker/postgres/primary/init-usuario-odoo.sh` solo la primera vez que se crea el volumen.

### Evidencia

![docker compose ps](../capturas/sprint-1/S1_docker_compose_ps.png)

*Figura 4.3.7-a. Servicios, volúmenes, red e imágenes del proyecto, con ambos contenedores en estado `healthy`.*

```text
$ docker compose ps
NAME                  IMAGE                    SERVICE   STATUS                 PORTS
erp-donofrio-db-1     postgres:16              db        Up 2 hours (healthy)   127.0.0.1:5432->5432/tcp
erp-donofrio-odoo-1   erp-donofrio/odoo:19.0   odoo      Up 2 hours (healthy)   127.0.0.1:8069->8069/tcp, 127.0.0.1:8072->8072/tcp, 8071/tcp
```

> El tamaño de las imágenes (166 MB y 700 MB) y el tiempo de arranque dependen de la PC; la primera vez se descargan unos 900 MB.
