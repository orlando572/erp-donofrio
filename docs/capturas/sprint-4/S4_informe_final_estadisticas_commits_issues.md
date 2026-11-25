# Estadísticas de commits y de issues (informe 6.7 y 6.8)

Salida de `python3 scripts/estadisticas_repo.py` (solo lectura) el 25/11/2026, con `develop` en `339c907` y 82 PR fusionados.

## 6.7 Commits

| Autor (GitHub) | PR fusionados | Commits dentro de los PR | % de los commits |
|---|---|---|---|
| orlando572 | 43 | 180 | 58 % |
| Eve3000a | 39 | 132 | 42 % |
| **Total** | 82 | 312 | 100 % |

Cumplen Conventional Commits: 309 de 312 (99 %). Llevan la etiqueta [HU-xx] o [Sn]: 70 de 312 (22 %).

| Tipo de commit | Cantidad |
|---|---|
| docs | 185 |
| feat | 82 |
| fix | 14 |
| test | 13 |
| chore | 9 |
| ci | 3 |
| perf | 3 |

Título del PR (el que queda en `develop` con *squash*): 79 de 82 cumplen la convención y llevan etiqueta. Fuera de la regla: #176, #222, #229.
Commits que no siguen la convención: #168 «merge: integra develop (listas de precios HU-09) e»; #170 «merge: integra develop (CRM HU-08 y FEFO) en HU-10»; #179 «merge: integra develop (HU-15) en HU-13».

## 6.8 Issues

Total de issues: 22 · abiertos 9 · cerrados 13

| Tipo | Total | Abiertos | Cerrados |
|---|---|---|---|
| epica | 15 | 4 | 11 |
| gestion | 7 | 5 | 2 |

| Área | Total | Abiertos | Cerrados |
|---|---|---|---|
| docs | 6 | 5 | 1 |
| extras | 2 | 0 | 2 |
| gerencia | 2 | 1 | 1 |
| infra | 6 | 0 | 6 |
| logistica | 1 | 0 | 1 |
| produccion | 2 | 1 | 1 |
| ventas | 3 | 2 | 1 |

| Fase | Total | Abiertos | Cerrados |
|---|---|---|---|
| 1 | 17 | 6 | 11 |
| 2 | 5 | 3 | 2 |

| Milestone | Total | Abiertos | Cerrados |
|---|---|---|---|
| Cierre | 2 | 2 | 0 |
| Sprint 0 – Inicio | 4 | 2 | 2 |
| Sprint 1 – Fundaciones | 3 | 0 | 3 |
| Sprint 2 – Procesos estándar | 4 | 0 | 4 |
| Sprint 3 – Calidad del núcleo | 4 | 2 | 2 |
| Sprint 4 – Módulos propios | 5 | 3 | 2 |

PR con `Parte de #n`: 51 · con `Closes #n`: 5 · sin enlace a una épica: 26 (de 82 PR fusionados).
Issues de tipo bug: 0.
