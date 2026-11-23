# ERP D'Onofrio – Odoo 19 Community

ERP académico para **D'Onofrio como unidad de helados y confitería** (corte 2026), construido sobre **Odoo 19.0 Community + PostgreSQL 16** en Docker.

- **Curso:** Sistemas de Información Empresarial, UTP Arequipa.
- **Equipo:** Evelyn (Product Owner + Developer) · Orlando (Scrum Master + Developer).
- **Metodología:** Scrum con enfoque PMBOK, en dos fases (núcleo garantizado + módulos propios) con Gate 0.
- **Aviso:** proyecto académico, no afiliado a Nestlé ni a D'Onofrio. Todos los datos (RUC, clientes, empleados, precios) son ficticios.

## Estado

Sprint 0 (Inicio). Solo hay planificación; el entorno Docker llega en el Sprint 1 (HU-01).

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
