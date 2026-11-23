# ERP D'Onofrio – Odoo 19 Community

ERP académico para **D'Onofrio como unidad de helados y confitería** (corte 2026), construido sobre **Odoo 19.0 Community + PostgreSQL 16** en Docker.

- **Curso:** Sistemas de Información Empresarial, UTP Arequipa.
- **Equipo:** Evelyn (Product Owner + Developer) · Orlando (Scrum Master + Developer).
- **Metodología:** Scrum con enfoque PMBOK, en dos fases (núcleo garantizado + módulos propios) con Gate 0.
- **Aviso:** proyecto académico, no afiliado a Nestlé ni a D'Onofrio. Todos los datos (RUC, clientes, empleados, precios) son ficticios.

## Estado

Sprint 0 cerrado. El entorno Docker llega en el Sprint 1 (HU-01).

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
