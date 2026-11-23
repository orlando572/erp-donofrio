# ERP D'Onofrio – Odoo 19 Community

ERP académico para **D'Onofrio como unidad de helados y confitería** (corte 2026), construido sobre **Odoo 19.0 Community + PostgreSQL 16** en Docker.

- **Curso:** Sistemas de Información Empresarial, UTP Arequipa.
- **Equipo:** Evelyn (Product Owner + Developer) · Orlando (Scrum Master + Developer).
- **Metodología:** Scrum con enfoque PMBOK, en dos fases (núcleo garantizado + módulos propios) con Gate 0.
- **Aviso:** proyecto académico, no afiliado a Nestlé ni a D'Onofrio. Todos los datos (RUC, clientes, empleados, precios) son ficticios.

## Estado

Sprint 0 cerrado. Sprint 1 (Fundaciones) en curso: entorno Docker (HU-01), CI (HU-02) y compañía peruana (HU-03) listos; siguen los datos maestros.

## Levantar el entorno (Odoo 19 + PostgreSQL 16)

Requisitos: Docker con el plugin Compose (ver «Preparar tu PC»). Unos 4 GB de RAM libres.

```bash
git clone https://github.com/orlando572/erp-donofrio.git ~/erp-donofrio && cd ~/erp-donofrio && git switch develop
cp .env.example .env          # valores de desarrollo; cámbialos si lo despliegas
docker compose up -d --build  # PostgreSQL 16 + Odoo 19.0 (la primera vez descarga las imágenes)
scripts/init_db.sh            # solo la primera vez: crea la BD «donofrio» e instala donofrio_base
```

Abre <http://localhost:8069>. `donofrio_base` deja la compañía con localización peruana (RUC ficticio, PEN, IGV 18 %, `es_PE`, `America/Lima`, plan contable PE). Al crear la BD, Odoo deja el usuario `admin` con contraseña `admin`: es solo para desarrollo, cámbiala si expones el puerto.

| Comando | Para qué |
|---|---|
| `docker compose ps` | Estado y salud de los servicios (`healthy`) |
| `docker compose logs -f odoo` | Registro de Odoo |
| `docker compose down` | Apaga los servicios y conserva los datos |
| `docker compose down -v` | Apaga y **borra** la BD y el filestore (volver a empezar) |
| `scripts/init_db.sh modulo1,modulo2` | Crea la BD (si no existe) instalando esos módulos |

Detalles:
- Los puertos se publican solo en `127.0.0.1`. Si alguno está ocupado en tu PC, cambia `ODOO_PORT`, `ODOO_LONGPOLLING_PORT` o `DB_PORT` en `.env`.
- PostgreSQL queda en `localhost:5432` para DBeaver, con el rol `odoo` (sin superusuario) y la contraseña de `.env`.
- El gestor de bases de datos de Odoo está deshabilitado (`list_db = False`): la BD se crea siempre con `scripts/init_db.sh`.
- Los módulos de `addons/` se montan en el contenedor en modo lectura.
- La imagen de Odoo tiene la etiqueta fechada fija en `docker/odoo/Dockerfile` (`odoo:19.0-20261112`) para que ambas PC y el CI usen exactamente la misma.

## Pruebas y CI

```bash
scripts/test.sh                  # instala todos los módulos de addons/ en una BD temporal y corre sus tests
scripts/test.sh donofrio_base    # solo ese módulo
scripts/check_legacy.sh          # patrones legacy de Odoo
```

`scripts/test.sh` imprime solo los errores y falla si hay `ERROR`/`FAIL`, si Odoo no termina bien o si no corrió ninguna prueba. El workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) ejecuta lo mismo en cada PR y en cada push a `develop` y `main` (jobs `lint` y `test`), además de una corrida semanal.

## Preparar tu PC

El proyecto se trabaja en **Linux**: Ubuntu nativo o **Ubuntu dentro de WSL2** en Windows.

### Windows 10 u 11: WSL2

1. En PowerShell como administrador: `wsl --install -d Ubuntu`. Reinicia y crea tu usuario de Ubuntu. Windows 10 necesita la versión 2004 o superior.
2. Instala **Docker Desktop** y activa *Settings → Resources → WSL integration → Ubuntu*.
3. Abre la terminal de **Ubuntu** y sigue los pasos comunes. Clona el repo dentro de Ubuntu (`~/`), **no** en `C:\` ni en `/mnt/c`, porque Docker es lento ahí y cambian los saltos de línea.
4. Edita el código con VS Code y la extensión **WSL**, o ejecuta Claude Code dentro de Ubuntu.

### Pasos comunes (Ubuntu o WSL2)

```bash
sudo apt update && sudo apt install -y git python3 ripgrep gh
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo-de-github"
gh auth login
git clone https://github.com/orlando572/erp-donofrio.git ~/erp-donofrio
cd ~/erp-donofrio && git switch develop
# Fuentes de referencia de Odoo 19 para el agente de IA (fuera del repo)
git clone --depth 1 -b 19.0 https://github.com/odoo/odoo.git ~/src/odoo-19.0
git clone --depth 1 -b 19.0 https://github.com/odoo/documentation.git ~/src/odoo-docs-19.0
```

En Ubuntu nativo, instala Docker Engine con el plugin Compose (`docker compose`).

### Agente de IA (Claude Code)

- Abre Claude Code en la carpeta del repo y acepta **confiar en el proyecto**. Así se activa el hook anti-legacy (`.claude/settings.json`).
- Las reglas están en [CLAUDE.md](CLAUDE.md). Antes de escribir código Odoo, el agente consulta [docs/dev/odoo19_cambios.md](docs/dev/odoo19_cambios.md) y `~/src/odoo-19.0`.
- Para revisar el código existente: `scripts/check_legacy.sh`.

## Documentación

- Plan completo: [docs/plan/PLAN_PROYECTO.md](docs/plan/PLAN_PROYECTO.md)
- Ficha de cambios de Odoo 19: [docs/dev/odoo19_cambios.md](docs/dev/odoo19_cambios.md)

## Estructura

```
addons/      Módulos propios (donofrio_base en la Fase 1)
docker/      Dockerfile de Odoo, PostgreSQL (primario/réplica) y Nginx
scripts/     init_db, test, check_legacy, backup/restore, perf…
docs/        plan, informe, diagramas, capturas, scrum, pm, manuales, dev
.github/     CI/CD, plantillas de issue y PR
```

## Flujo de trabajo

- Ramas: `main` (entregado) ← `develop` (integración) ← `feature/HU-xx-descripcion`.
- Commits: [Conventional Commits](https://www.conventionalcommits.org/es/) en español, con `[HU-xx]`.
- PR a `develop` con revisión obligatoria del otro integrante y CI en verde.
- Detalle en [docs/plan/06_github_ci_infra.md](docs/plan/06_github_ci_infra.md).

## Licencia

Módulos propios bajo LGPL-3 (ver [LICENSE](LICENSE)).
