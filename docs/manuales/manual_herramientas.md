# Manual de instalación y configuración de las herramientas (borrador)

> **Estado:** borrador del Sprint 3 · **Autor:** Orlando (SM) · **Revisa:** Evelyn · Se completa con capturas y se exporta a PDF en el Cierre (lista en la sección 12).
> Complementa el [Manual de instalación](manual_instalacion.md) (que instala el ERP) y la sección [4.3.3 del informe](../informe/04_03_infraestructura.md) (lineamientos por etapa). Los datos de la empresa son ficticios.

## 1. Cómo leer este manual

Cada herramienta se describe con los mismos seis puntos: **para qué se usa en este proyecto** (con el archivo o script real), **versión**, **instalación** en Ubuntu y en Windows con WSL2, **cómo comprobarla** (un comando con su salida esperada) y **problemas frecuentes**.

Las herramientas se reparten en tres grupos, y esa diferencia importa para la instalación:

| Grupo | Qué significa | Herramientas |
|---|---|---|
| **A. Se instalan en el equipo** | Hay que instalarlas una vez en la PC de cada integrante | Docker (con Compose), Git, `gh`, VS Code, DBeaver, Claude Code (y `python3`) |
| **B. Corren en un contenedor** | **No se instala nada**: el script descarga la imagen de Docker con la versión fijada la primera vez que se usa | PlantUML, Graphviz, k6, OWASP ZAP, Lighthouse con Chromium, librsvg (conversión de SVG a PNG), `ruff` (solo en el CI) |
| **C. Servicio en la web** | Solo hace falta una cuenta o un navegador | GitHub (repositorio, Actions, GHCR, Projects), bpmn.io |

Además hay herramientas que el plan nombraba y **no se usaron**; están en la sección 11 con lo que se usó en su lugar.

**Versiones.** Las de las imágenes de Docker se leyeron de los scripts y los *workflows* (`grep` sobre el repositorio) y se comprobaron ejecutando la imagen el 23/11/2026 en la PC de Orlando (Ubuntu). Las del grupo A son las de esa PC en esa fecha; no hay una versión «obligatoria» porque cada integrante instala la estable vigente. Donde algo **no se pudo comprobar**, se dice.

### 1.1 Resumen

| Herramienta | Grupo | Versión | Dónde se usa en el repositorio |
|---|---|---|---|
| Docker Engine y Compose | A | 29.1.3 y Compose 2.40.3 | `docker-compose.yml`, `docker/`, todos los scripts |
| Git | A | 2.53.0 | Control de versiones; ramas y *commits* de [6.4](../informe/06_04_a_06_06_repositorio.md) |
| `gh` (CLI de GitHub) | A | 2.46.0 | `scripts/trazabilidad.py --gh`, Projects, PR |
| VS Code | A | 1.146.0 | Edición; extensión WSL en Windows |
| DBeaver | A | (sin comprobar en esta PC) | Lectura de PostgreSQL en `localhost:5432` y réplica `5433` |
| Claude Code | A | 2.1.328 | `CLAUDE.md`, `.claude/`, `scripts/check_legacy.sh` |
| PlantUML (con Graphviz) | B | 1.2026.10 (Graphviz 14.0.1) | `docs/diagramas/c4/`, `clases/`, `cu/`, `er/` |
| librsvg (en `python:3.12-slim`) | B | `python:3.12` (3.12.16 al comprobar) | PNG de BPMN, arquitectura y pantallas |
| k6 | B | 1.7.1 | `scripts/perf/k6.sh` y `carga.js` |
| OWASP ZAP | B | 2.17.0 | `scripts/perf/zap.sh` |
| Lighthouse | B | 12.2.1 (sobre `node:22-bookworm-slim`) | `scripts/perf/lighthouse.py` |
| `ruff` | B (CI) | 0.8.4 | Job `lint` de `.github/workflows/ci.yml` |
| GitHub Actions / GHCR / Projects | C | `ubuntu-24.04`, acciones `@v4`/`@v6` | `.github/workflows/` |
| bpmn.io | C | (servicio web) | Abrir los `.bpmn` de `docs/diagramas/bpmn/` |

## 2. Antes de empezar

- **Sistema:** Ubuntu 22.04 o superior, o Windows 10 (2004 o más) / 11 con **WSL2 y Ubuntu**. Trabaja siempre **dentro de Ubuntu** (`~/`), nunca en `C:\` ni en `/mnt/c`.
- **Recursos:** unos 4 GB de RAM libres para el ERP y **unos 10 GB de disco extra** si vas a usar las herramientas del grupo B: las imágenes pesan, por ejemplo, 3.75 GB la de ZAP, 517 MB la de PlantUML, 116 MB la de k6 (tamaños leídos con `docker images`).
- **Internet** la primera vez que cada herramienta descarga su imagen.
- Los pasos de Windows con WSL2 siguen la misma guía que el [Manual de instalación §3.2](manual_instalacion.md); **no se probaron en una PC con Windows limpia para este borrador** (la PC verificada es Ubuntu). Queda como prueba del Cierre (sección 12).

## 3. Docker y Docker Compose (grupo A)

**Para qué.** Es la base del proyecto: `docker-compose.yml` levanta PostgreSQL 16, Odoo, la réplica y Nginx (perfiles `replica` y `proxy`); `scripts/*.sh` y los *workflows* de CI usan `docker run` para correr todas las herramientas del grupo B sin instalarlas.

**Versión.** Docker Engine 29.1.3 (paquete de Ubuntu), Compose 2.40.3, Buildx 0.30.1. Imágenes del proyecto: `odoo:19.0-20261112` (fijada en `docker/odoo/Dockerfile`), `postgres:16` (comprobada: 16.16) y `nginx:stable` (comprobada: 1.30.7; esta etiqueta **no** está fijada a una versión).

**Instalar en Ubuntu.**

```bash
# Opción A (la usada en la PC verificada): paquetes de Ubuntu
sudo apt update && sudo apt install -y docker.io docker-compose-v2 docker-buildx
# Opción B: Docker Engine desde el repositorio oficial de Docker (guía «Install Docker Engine on Ubuntu»)
sudo usermod -aG docker "$USER"      # luego cierra la sesión y vuelve a entrar para usar docker sin sudo
```

**Instalar en Windows con WSL2.**

1. PowerShell como administrador: `wsl --install -d Ubuntu`; reinicia y crea tu usuario de Ubuntu.
2. Instala **Docker Desktop** y activa *Settings → Resources → WSL integration → Ubuntu*.
3. En la terminal de Ubuntu **no** instales Docker Engine: usa el de Docker Desktop.

**Comprobar** (salida real del 23/11/2026):

```bash
docker --version && docker compose version
# Docker version 29.1.3, build 29.1.3-0ubuntu4.1
# Docker Compose version 2.40.3+ds1-0ubuntu1
docker run --rm hello-world           # debe imprimir «Hello from Docker!»
```

**Problemas frecuentes.**

| Síntoma | Solución |
|---|---|
| `permission denied ... /var/run/docker.sock` | Falta el grupo `docker` (`sudo usermod -aG docker "$USER"`) y volver a iniciar sesión |
| `docker: command not found` en Ubuntu de WSL | Docker Desktop no está abierto o falta activar la integración WSL para Ubuntu |
| Muy lento en Windows | El repositorio está en `/mnt/c`: clónalo en `~/` |
| `port is already allocated` | Otro programa usa 8069, 8072 o 5432: cámbialos en `.env` (variables `*_PORT`) |
| Compose usa el nombre de otro proyecto | `docker-compose.yml` fija `name: erp-donofrio`: **todas las copias del repositorio comparten contenedores y volúmenes**. No uses `docker compose down -v` sin saber en qué copia estás |

## 4. Git (grupo A)

**Para qué.** Control de versiones con ramas `main` ← `develop` ← `feature/…` y *commits* de [Conventional Commits en español](../informe/06_04_a_06_06_repositorio.md); el repositorio es `github.com/orlando572/erp-donofrio`.

**Versión.** 2.53.0.

**Instalar.** Ubuntu y WSL2: `sudo apt update && sudo apt install -y git`. En Windows, **no** uses Git for Windows para este proyecto: se trabaja con el Git de Ubuntu dentro de WSL2 (evita problemas de saltos de línea).

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo-de-github"
```

**Comprobar.**

```bash
git --version        # git version 2.53.0
git clone https://github.com/orlando572/erp-donofrio.git ~/erp-donofrio && cd ~/erp-donofrio && git switch develop
```

**Problemas frecuentes.** `main` y `develop` están protegidas: no se hace *push* directo, se abre un PR desde `feature/…` (los controles están en [4.3.1](../informe/04_03_infraestructura.md)). Si Git rechaza un *push* por «protected branch», es la regla funcionando. Con archivos de `docs/` que cambian de saltos de línea, comprueba que el repositorio esté dentro de Ubuntu.

## 5. GitHub: repositorio, Actions, GHCR, Projects y la CLI `gh`

### 5.1 `gh` (grupo A)

**Para qué.** Abrir y revisar PR sin salir de la terminal (`gh pr create`, `gh pr list`), consultar CI (`gh run list`), leer la protección de ramas (`gh api`) y el GitHub Project. En el repositorio, [`scripts/trazabilidad.py`](../../scripts/trazabilidad.py) usa `gh pr list --state merged` (solo lectura) cuando se le pasa `--gh`.

**Versión.** 2.46.0.

**Instalar.**

```bash
sudo apt update && sudo apt install -y gh          # Ubuntu y Ubuntu de WSL2
gh auth login                                       # lo ejecuta el usuario: GitHub.com → HTTPS → navegador o token
gh auth refresh -s project                          # lo ejecuta el usuario: permiso «project» para GitHub Projects
```

`gh auth login` y `gh auth refresh -s project` **piden tu confirmación en el navegador**: las ejecuta cada persona; el asistente de IA no debe hacerlo por ti ni se guardan tokens en el repositorio.

**Comprobar** (salida real, sin el nombre de la cuenta):

```bash
gh --version | head -1            # gh version 2.46.0 (2025-12-13 Ubuntu 2.46.0-4)
gh auth status                    # ✓ Logged in to github.com ... Token scopes: 'gist', 'project', 'read:org', 'repo', 'workflow'
gh project list --owner orlando572 # 4  Scrum ERP D'Onofrio  open  (el Project del equipo es el número 4)
```

El permiso `project` debe aparecer en `Token scopes`; sin él, los comandos `gh project …` fallan.

**Problemas frecuentes.** `error: your authentication token is missing required scopes [project]` → `gh auth refresh -s project`. `HTTP 403` al leer la protección de ramas → hace falta permiso de administrador sobre el repositorio. El plan ([04 §4.11](../plan/04_scrum_pmbok.md)) preveía un `scripts/burndown.py` que lee el Project con `gh project item-list --format json`; **ese script todavía no existe en el repositorio**.

### 5.2 GitHub Actions (grupo C)

**Para qué.** CI y publicación, sin instalar nada. Los tres *workflows* están en `.github/workflows/`:

| Archivo | Qué hace | Cuándo corre |
|---|---|---|
| `ci.yml` | Jobs `lint` (`scripts/check_legacy.sh` y `ruff` 0.8.4), `test` (`scripts/test.sh`), `replica`, `backup` y `proxy` | Cada PR, cada *push* a `develop` y `main`, y semanal (lunes 06:00 de Lima) |
| `perf.yml` | k6 y ZAP sobre el despliegue protegido | Solo a mano (*Run workflow*) |
| `release.yml` | Imagen a GHCR, zip del código y GitHub Release | Con un tag `v*`; sin tag, es un ensayo |

**Versión.** *Runner* `ubuntu-24.04`; acciones `actions/checkout@v4`, `actions/upload-artifact@v4`, `docker/setup-buildx-action@v3`, `docker/build-push-action@v6` y `docker/login-action@v3` (leídas de los `.yml`).

**Comprobar** (con `gh`): `gh run list --limit 3` muestra las últimas corridas con su estado (`completed success` o `failure`). Configuración, protección de ramas y procedimiento: [5.15](../informe/05_15_despliegue.md) y [4.3.1](../informe/04_03_infraestructura.md).

**Problemas frecuentes.** Un cambio que solo toca documentación igual dispara el CI (tarda unos 3 a 6 min); el check `test` falla si el CI no logra construir la imagen de Odoo (descarga). Para ver el motivo: `gh run view <id> --log-failed`.

### 5.3 GHCR, el registro de imágenes (grupo C)

**Para qué.** `release.yml` publica la imagen `ghcr.io/orlando572/erp-donofrio:vX.Y.Z` (Odoo 19 + `auditlog` + `donofrio_base` dentro). **Estado al 23/11/2026: sin imagen publicada**, porque aún no hay ningún tag; se publica con `v1.0.0` en el Gate 0 ([`docs/dev/release.md`](../dev/release.md)). El flujo se ensayó sin publicar ([evidencia](../capturas/sprint-3/HU-29_evidencia_release.txt)).

**Comprobar cuando exista:** `docker pull ghcr.io/orlando572/erp-donofrio:v1.0.0` (el paquete debe estar en visibilidad pública, ver `release.md`). **Problema probable:** `denied` al descargar → el paquete quedó privado: *Package settings → Change visibility*.

### 5.4 GitHub Projects (grupo C)

**Para qué.** Tablero Scrum «Scrum ERP D'Onofrio» (Project v2, el número 4 del propietario `orlando572`): Product Backlog, sprints, épicas por área con su checklist de HU y los PR enlazados (`Parte de #n`). Es la herramienta que la plantilla llama «Monday» (justificación en [04 §4.11](../plan/04_scrum_pmbok.md)). No se instala; se consulta en la web o con `gh project …` (permiso `project`).

**Comprobar.** `gh project list --owner orlando572` (arriba). **Problema frecuente:** el permiso `project` falta o caducó → `gh auth refresh -s project`.

## 6. VS Code (grupo A)

**Para qué.** Editor de los dos integrantes para `addons/`, `scripts/` y `docs/`; abre también las vistas previas de Markdown de los informes y manuales. En Windows se usa con la extensión **WSL**, de modo que el código queda en Ubuntu.

**Versión.** 1.146.0 (instalado con `snap`).

**Instalar.**

```bash
sudo snap install code --classic        # Ubuntu (alternativa: el paquete .deb de code.visualstudio.com)
```

Windows: instala **VS Code** desde code.visualstudio.com y la extensión **WSL** (Microsoft). Desde la terminal de Ubuntu: `cd ~/erp-donofrio && code .`. La primera vez instala un componente servidor en Ubuntu.

**Comprobar.** `code --version` imprime el número de versión en la primera línea (`1.146.0` el 23/11/2026) seguido del identificador del *commit* y la arquitectura.

**Problemas frecuentes.** `code: command not found` en WSL → abre VS Code desde Windows una vez o reinstala la extensión WSL. Los archivos `.env` no se versionan: VS Code los muestra, pero no los subas. No se exigen extensiones del proyecto; las útiles son *Python*, *PlantUML* y *Markdown All in One* (opcionales, no comprobadas como requisito).

## 7. DBeaver (grupo A)

**Para qué.** Cliente gráfico para **leer** la base de datos: `localhost:5432` (primario) y `localhost:5433` (réplica de solo lectura, perfil `replica`). Está documentado en el [Manual de instalación §6.1](manual_instalacion.md) y en [4.3.3](../informe/04_03_infraestructura.md). **Estado honesto:** el repositorio no guarda capturas ni artefactos de su uso; el modelo ER se **extrajo con `scripts/diagrama_er.py`**, no con DBeaver (ver sección 11). La captura de la conexión queda pendiente para el Cierre.

**Versión.** No se pudo comprobar en esta PC (no estaba instalado). Usa DBeaver **Community** estable.

**Instalar.**

```bash
sudo snap install dbeaver-ce                       # Ubuntu (alternativa: paquete .deb de dbeaver.io)
```

Windows: instalador de DBeaver Community desde dbeaver.io, en Windows (Docker Desktop publica los puertos también en el `localhost` de Windows).

**Configurar la conexión** (*Nueva conexión → PostgreSQL*): servidor `localhost`, puerto `5432` (o `5433` para la réplica), base de datos `donofrio`, usuario `odoo` y la contraseña `ODOO_DB_PASSWORD` de tu `.env`. El rol `odoo` no es superusuario.

**Comprobar.** Con `docker compose ps` en `healthy` y la base creada, el botón *Test Connection* debe decir «Connected» y la consulta `SELECT count(*) FROM res_users;` debe devolver un número (en la base con `donofrio_base`, al menos los 10 usuarios por rol).

**Problemas frecuentes.**

| Síntoma | Solución |
|---|---|
| Pide descargar el *driver* | Normal la primera vez; necesita Internet |
| `password authentication failed for user "odoo"` | La contraseña es `ODOO_DB_PASSWORD` de `.env`, no la de `postgres` |
| `Connection refused` | El contenedor `db` no está arriba, o cambiaste `DB_PORT` en `.env` |
| La réplica rechaza una escritura | Es lo esperado: `cannot execute INSERT in a read-only transaction` |

## 8. Herramientas de diagramas (grupo B y C)

Los diagramas del informe se **generan por código** para que sean reproducibles; el detalle de cada comando está en [`docs/diagramas/README.md`](../diagramas/README.md).

### 8.1 PlantUML y Graphviz (grupo B)

**Para qué.** Casos de uso (`docs/diagramas/cu/*.puml`), clases (`clases/`), C4 (`c4/`) y el modelo ER (`er/`, que escribe `scripts/diagrama_er.py` y renderiza con PlantUML). Graphviz viene **dentro** de la imagen de PlantUML y lo usa [`scripts/grafo_dependencias.py`](../../scripts/grafo_dependencias.py) para el grafo de dependencias de módulos (`docs/diagramas/dependencias/`).

**Versión.** Imagen `plantuml/plantuml:1.2026.10` (PlantUML 1.2026.10, Graphviz 14.0.1). **Nota:** los diagramas de casos de uso y de clases y `diagrama_er.py` usan la etiqueta `plantuml/plantuml:latest`, que no está fijada; solo los C4 y el grafo de dependencias usan la `1.2026.10`.

**Instalar.** Nada: la imagen se descarga con el primer comando (`docker pull plantuml/plantuml:1.2026.10`).

**Comprobar** (salida real):

```bash
docker run --rm plantuml/plantuml:1.2026.10 -version
# PlantUML version 1.2026.10 / a00edda [2026-11-11 11:04:35 UTC]
docker run --rm --entrypoint dot plantuml/plantuml:1.2026.10 -V
# dot - graphviz version 14.0.1 (20251006.0113)   (puede imprimir antes un aviso de libgvplugin_gd: no afecta)
```

Generar los C4: `for f in png svg; do docker run --rm -u $(id -u):$(id -g) -v "$PWD/docs/diagramas/c4":/data plantuml/plantuml:1.2026.10 -charset UTF-8 -t$f /data/*.puml; done`.

**Problemas frecuentes.** Los archivos generados quedan de `root` si falta `-u $(id -u):$(id -g)`. Tildes rotas → falta `-charset UTF-8`. El ER solo refleja `develop` si se extrae de una base limpia (`scripts/esquema_limpio.sh crear`, ver el README de diagramas).

### 8.2 librsvg para los PNG (grupo B)

**Para qué.** `generar_bpmn.py`, `generar_arquitectura.py` y `generar_pantallas.py` escriben SVG con Python sin librerías; el PNG sale de convertirlo con `rsvg-convert`, que se instala **dentro** de un contenedor `python:3.12-slim` (ver el README de diagramas). **Comprobar:** `docker run --rm python:3.12-slim python --version` → `Python 3.12.16` (en el equipo se necesita `python3` solo para lanzar los generadores).

### 8.3 bpmn.io (grupo C) y Mermaid

**bpmn.io.** Los BPMN se **generan** con `docs/diagramas/generar_bpmn.py`, que escribe el `.bpmn` y un `.svg`. Para abrir o editar un `.bpmn` se usa <https://demo.bpmn.io> (cargar el archivo; no hay nada que instalar). El informe dice que los diagramas «se editan en bpmn.io» ([4.1](../informe/04_01_analisis_sistemas.md)); lo que **sí** se verificó es que el script genera archivos `.bpmn` en el formato estándar; la captura de uno abierto en bpmn.io queda pendiente para el Cierre.

**Mermaid.** Algunos diagramas del informe (por ejemplo la figura 4.3.2-a) están escritos en bloques `mermaid` de Markdown, que GitHub dibuja sin instalar nada.

## 9. Herramientas de pruebas (grupo B)

Las tres corren en contenedor, contra el **despliegue protegido** (`scripts/levantar_prod.sh`, `https://localhost:8443`). Resultados y su lectura: [`docs/dev/pruebas_no_funcionales.md`](../dev/pruebas_no_funcionales.md) y [5.14](../informe/05_13_a_05_14_pruebas.md). Prepara antes la base con datos de demostración ([Manual de instalación §4.5 y §6.2](manual_instalacion.md)). Los reportes quedan en `scripts/perf/resultados/` (carpeta ignorada por git).

> **Windows:** `k6.sh` y `zap.sh` ejecutan `docker run --network host` para llegar a `localhost`. En Ubuntu funciona directo; **con Docker Desktop no se probó en este proyecto** y puede requerir activar la red de tipo *host* en sus ajustes. Si no funciona, ejecuta estos dos scripts en una PC con Ubuntu.

### 9.1 k6 (carga)

**Para qué.** Prueba de carga de RNF002 (p95 < 2 s con 20 usuarios virtuales): [`scripts/perf/k6.sh`](../../scripts/perf/k6.sh) lanza k6 y [`scripts/perf/carga.js`](../../scripts/perf/carga.js) define el escenario y los umbrales. También lo lanza `perf.yml` en GitHub.

**Versión.** `grafana/k6:1.7.1` (fijada en `k6.sh`).

**Instalar.** Nada (`docker pull grafana/k6:1.7.1`, 116 MB).

**Comprobar** (salida real):

```bash
docker run --rm grafana/k6:1.7.1 version
# k6 v1.7.1+dirty (commit/9f82e6f1fc-dirty, go1.26.1, linux/amd64)
scripts/perf/k6.sh        # con el despliegue protegido arriba; termina con «k6: todos los umbrales se cumplieron.»
```

Opciones: `VUS=20 DURACION=3m PAUSA=1` (con `PAUSA=0`, prueba de esfuerzo). Resultado medido el 23/11/2026: p95 de 11.6 ms en listas y 9.1 ms en formularios.

**Problemas frecuentes.** `Falta .env` o `DONOFRIO_USER_PASSWORD` → copia `.env.example` a `.env`. Muchos fallos de inicio de sesión → la base no tiene `donofrio_base` o la contraseña de prueba cambió después de crearla (hay que recrear la base). No pruebes con el administrador ni el gerente: piden 2FA en el despliegue protegido.

### 9.2 OWASP ZAP (seguridad)

**Para qué.** Análisis *baseline* (reglas pasivas y araña) del despliegue protegido para RNF009: [`scripts/perf/zap.sh`](../../scripts/perf/zap.sh), con las alertas aceptadas y su motivo en [`zap-reglas.conf`](../../scripts/perf/zap-reglas.conf). Falla si hay una alerta de riesgo alto.

**Versión.** `ghcr.io/zaproxy/zaproxy:2.17.0` (fijada en `zap.sh`; 3.75 GB, es la imagen más pesada).

**Instalar.** Nada (`docker pull ghcr.io/zaproxy/zaproxy:2.17.0`).

**Comprobar** (salida real; ZAP imprime antes un aviso de Java sobre sus preferencias, que no afecta):

```bash
docker run --rm ghcr.io/zaproxy/zaproxy:2.17.0 zap.sh -version      # 2.17.0
scripts/perf/zap.sh        # corrida final de HU-28: FAIL 0 · WARN 0 · IGNORE 10 · PASS 58
```

**Problemas frecuentes.** `No responde https://localhost:8443/web/login` → falta `scripts/levantar_prod.sh`. El certificado es autofirmado, por eso ZAP corre con la verificación TLS desactivada. La araña **no inicia sesión**: no ve el backend. Una alerta nueva sale como aviso: se corrige en `docker/nginx/` o se acepta con su motivo en `zap-reglas.conf`.

### 9.3 Lighthouse (WPO)

**Para qué.** Medir el rendimiento web (RNF008) en el login, el backend y el dashboard, antes y después de Nginx con TLS y gzip: [`scripts/perf/lighthouse.py`](../../scripts/perf/lighthouse.py). Es la tarea de Evelyn ([4.6](../informe/04_06_wpo.md); resultados en [`HU-28_lighthouse_resultados.csv`](../capturas/sprint-3/HU-28_lighthouse_resultados.csv)).

**Versión.** Lighthouse **12.2.1** con Chromium de Debian *bookworm*, sobre `node:22-bookworm-slim` (fijado en [`scripts/perf/Dockerfile.lighthouse`](../../scripts/perf/Dockerfile.lighthouse)). **No se ejecutó en esta sesión:** la imagen `donofrio-lighthouse` se construye en la primera corrida (varios minutos) y no estaba construida en esta PC; el número sale del *Dockerfile*.

**Instalar.** Nada: `lighthouse.py` construye la imagen sola. También se puede usar **DevTools → Lighthouse** de Chrome para una prueba rápida a mano.

**Comprobar** (tras la primera corrida, que construye la imagen; salida esperada según el *Dockerfile*):

```bash
python3 scripts/perf/lighthouse.py ANTES http://host.docker.internal:8069 --debug-assets
docker run --rm --entrypoint lighthouse donofrio-lighthouse --version     # 12.2.1
```

**Problemas frecuentes.** Usa `host.docker.internal` y no `localhost`, porque Chromium corre dentro del contenedor. `lighthouse.py` agrega `--add-host=host.docker.internal:host-gateway`, así que también funciona en Ubuntu con Docker 20.10 o superior. La clave de `jefe.ventas@donofrio.example.com` sale de `DONOFRIO_USER_PASSWORD` en `.env` y no se imprime. Los segundos son comparativos: Lighthouse simula red y CPU.

### 9.4 ruff (solo CI)

`ruff` 0.8.4 revisa el estilo de `addons/` en el job `lint` de `ci.yml` (se instala en un entorno virtual temporal del *runner*). No se usa en la PC: `scripts/check_legacy.sh` (sección 10.2) es el equivalente local para los patrones de Odoo. Si quieres correrlo antes del PR: `python3 -m venv ~/.venv-ruff && ~/.venv-ruff/bin/pip install ruff==0.8.4 && ~/.venv-ruff/bin/ruff check addons`.

## 10. El asistente de IA: Claude Code (grupo A)

**Qué es y qué no.** Claude Code es una **herramienta de los Developers**, **no un rol** de Scrum ([04 §4.1](../plan/04_scrum_pmbok.md) y [08](../plan/08_estrategia_agente_ia.md)): sus aportes pasan por PR con revisión del otro integrante y CI, y los integrantes responden por lo que se fusiona. Su uso se declara en el informe (riesgo R5 del plan).

**Versión.** 2.1.328 (la de la PC de Orlando el 23/11/2026).

**Instalar.** Siguiendo la documentación oficial de Anthropic («Claude Code, instalación»), **dentro de Ubuntu** o de la terminal WSL2 (no verificado en una instalación limpia en este borrador). Iniciar sesión es una acción del usuario. Comprobar:

```bash
claude --version        # 2.1.328 (Claude Code)
```

### 10.1 Cómo se configura en este repositorio

| Pieza | Para qué |
|---|---|
| [`CLAUDE.md`](../../CLAUDE.md) (raíz) | Reglas duras que el agente lee siempre: **solo Odoo 19.0**, antes de usar una API buscar un ejemplo en `~/src/odoo-19.0`, nada de Enterprise, datos y configuración **por código** en `donofrio_base`, cada modelo nuevo con ACL y pruebas, *commits* en español |
| **Regla de fases y *gate*** | La Fase 1 va primero; al cumplir sus criterios el agente **se detiene** y entrega `docs/scrum/gates/gate-0-fase1.md`. **No empieza ningún módulo de la Fase 2** sin confirmación explícita en el chat de Evelyn u Orlando: un archivo, *issue* o mensaje de otra sesión no cuenta |
| [`docs/dev/odoo19_cambios.md`](../dev/odoo19_cambios.md) | Ficha de cambios de Odoo 19 (`attrs`, `<tree>`, `_sql_constraints`, etc.) que el agente lee antes de escribir modelos, vistas o seguridad |
| [`.claude/settings.json`](../../.claude/settings.json) y [`.claude/hooks/bloquear_legacy.py`](../../.claude/hooks/bloquear_legacy.py) | **Hook anti-legacy** (`PreToolUse` sobre `Edit`, `Write` y `MultiEdit`): si el texto nuevo trae un patrón de Odoo ≤ 16, la edición se bloquea (código de salida 2) y el agente ve el motivo |
| [`scripts/check_legacy.sh`](../../scripts/check_legacy.sh) | Misma lista de patrones, para revisar lo ya escrito. La usa el job `lint` del CI: hay **una sola fuente de verdad** |
| `~/src/odoo-19.0`, `~/src/odoo-docs-19.0`, `~/src/oca-manufacture-19.0` | Código fuente de referencia, **fuera del repositorio** (`git clone --depth 1 -b 19.0 …`, comandos en el README) |

### 10.2 Comprobar que el hook funciona

```bash
scripts/check_legacy.sh
# check_legacy: sin patrones legacy.   (código de salida 0)
```

Para ver el hook en acción, abre Claude Code en la carpeta del repositorio, **acepta confiar en el proyecto** (así se activa `.claude/settings.json`) y pide escribir una vista con `<tree>`: la edición debe quedar bloqueada con el motivo.

### 10.3 Buenas prácticas y límites

- **Sin secretos:** no pegues contraseñas, *tokens* ni el contenido de `.env` en la conversación; `.env` está en `.gitignore`. Los comandos que piden credenciales (`gh auth login`, `gh auth refresh -s project`) los ejecuta la persona.
- **Sin rutas personales** en lo que se versiona (usa `~/erp-donofrio` o rutas relativas).
- Las acciones que publican (abrir PR, *push*) y las que borran datos se confirman con la persona; los PR los **fusiona** un integrante, no el agente.
- El agente **no sustituye** la revisión del otro integrante ni la lectura del código fuente de Odoo 19.

**Problemas frecuentes.** El hook no se activa si no se aceptó «confiar en el proyecto» o si no hay `python3` (el hook lo busca como `python3` o `python`). Si el agente propone un patrón antiguo, el hook lo rechaza y hay que consultar `odoo19_cambios.md`.

## 11. Herramientas previstas en el plan y no usadas

| Herramienta | Qué decía el plan | Qué se usó en su lugar | Dónde está dicho |
|---|---|---|---|
| **SchemaSpy** | Servicio `schemaspy` (perfil `tools`) para el ER | **`scripts/diagrama_er.py` + PlantUML**: extrae el esquema real de la base, filtra a las tablas del núcleo y se regenera con un comando. **No** hay servicio `schemaspy` ni perfil `tools` | [4.2.6](../informe/04_02_modelo_de_datos.md), [4.3.7](../informe/04_03_infraestructura.md), [5.15](../informe/05_15_despliegue.md) |
| **draw.io** | Arquitectura, infraestructura y pipeline (4.1.3, 4.3.1, 5.7, 5.8) | **Python + SVG** (`generar_arquitectura.py`) para arquitectura, infraestructura y CI/CD, y **PlantUML con la librería C4** para 5.7 y 5.8. No hay archivos `.drawio` en el repositorio | [`docs/diagramas/README.md`](../diagramas/README.md) |
| **Camunda Modeler** | Opción para editar BPMN | **`generar_bpmn.py`** escribe los `.bpmn`; <https://demo.bpmn.io> sirve para abrirlos. No hay archivos de Camunda Modeler | [`docs/diagramas/README.md`](../diagramas/README.md) |
| **Uptime Kuma** | Monitoreo de disponibilidad (no estaba en el listado de herramientas, pero el plan lo nombraba) | Solo los *healthchecks* de Docker (`pg_isready`, `/web/health`) y `docker compose ps`; no hay medición continua | [4.3.3](../informe/04_03_infraestructura.md) |
| **`scripts/burndown.py`** | Burndown por puntos leyendo el Project con `gh` | Aún no existe en el repositorio | Sección 5.1 de este manual |

La regla de este manual es la misma que la del informe: lo que no se usó se dice, con lo que se usó de verdad.

## 12. Pendiente para el Cierre

Capturas que **no se inventan aquí** y se toman en una PC limpia (o la PC de cada integrante) siguiendo este manual:

- [ ] `docker --version` y `docker compose version` (y `docker run --rm hello-world`) en Ubuntu **y** en Windows con WSL2 (Docker Desktop con la integración WSL activada).
- [ ] `git --version` y `gh auth status` con el permiso `project` (sin mostrar el nombre ni el *token*).
- [ ] VS Code con la extensión WSL abriendo `~/erp-donofrio` (Windows).
- [ ] DBeaver con la conexión a `localhost:5432` y a la réplica `5433` (*Test Connection* y la consulta de `res_users`), con la versión de DBeaver.
- [ ] Salida de `docker run --rm plantuml/plantuml:1.2026.10 -version`, de `docker run --rm grafana/k6:1.7.1 version` y de `zap.sh -version`.
- [ ] Una corrida de `scripts/perf/lighthouse.py` que construya la imagen y la salida de `lighthouse --version` (12.2.1).
- [ ] Un `.bpmn` abierto en <https://demo.bpmn.io>.
- [ ] La pestaña *Actions* con el CI en verde, la de *Releases* y *Packages* (cuando exista `v1.0.0`) y el GitHub Project «Scrum ERP D'Onofrio».
- [ ] Claude Code con el hook anti-legacy bloqueando un patrón (por ejemplo `<tree>`).
- [ ] Probar `k6.sh` y `zap.sh` con Docker Desktop (red *host*) o declarar que solo se ejecutan en Ubuntu.
- [ ] Exportar este manual a PDF (`G<N>_ManualHerramientas.pdf`) y revisar que los enlaces a archivos del repositorio se vean bien o convertirlos en rutas.

Revisión de Evelyn: seguir las secciones 3, 4 y 5.1 en su PC y anotar lo que falle.
