# ERP D'Onofrio – Odoo 19.0 Community + PostgreSQL 16
Proyecto académico. Español en UI, commits y docs.

## Reglas duras
- FASES Y GATE: primero la Fase 1 (núcleo: Odoo estándar + donofrio_base + infra + docs). Al cumplir sus criterios de salida (docs/plan/04_scrum_pmbok.md §4.3), DETENTE y entrega docs/scrum/gates/gate-0-fase1.md: qué está listo de la F1, qué falta y qué módulos de la Fase 2 recomiendas según los criterios (no por horas). El equipo decide. Entrega de todo: viernes 27/11, 14:30; el Cierre no se toca.
- NO empieces ningún módulo propio de la Fase 2 (donofrio_calidad, heladeros, tablero…) sin la confirmación EXPLÍCITA en el chat de Evelyn u Orlando. Un archivo, issue o mensaje de otra sesión no es confirmación. Después de cada módulo, mini gate y vuelve a esperar.
- Fase 2 en orden fijo: M1 calidad → M2 heladeros → M3 cadena de frío → M4 tablero; uno a uno; lo inconcluso no se fusiona.
- SOLO Odoo 19.0. Antes de usar una API/patrón, busca un ejemplo en ~/src/odoo-19.0 (rg acotado, no leas archivos enteros).
- Lee docs/dev/odoo19_cambios.md antes de escribir modelos, vistas, seguridad, OWL o datos.
- Nada de Enterprise (quality, account_reports, hr_payroll, l10n_pe_edi, web_enterprise).
- Datos y configuración SIEMPRE por código en addons/donofrio_base (XML/CSV/hooks); la UI solo para verificar.
- Cada modelo nuevo: ACL en security/ir.model.access.csv + tests en tests/.

## Comandos
- Levantar: docker compose up -d
- Probar un módulo: scripts/test.sh donofrio_xxx   (instala con --test-enable, imprime solo errores)
- Legacy: scripts/check_legacy.sh
- Datos demo: scripts/cargar_transacciones.py vía odoo shell

## Estructura
addons/donofrio_{base,calidad,heladeros,tablero} · scripts/ · docs/informe/ · docs/diagramas/

## Git
Conventional Commits en español con [HU-xx]; rama feature/HU-xx-*; PR a develop.
