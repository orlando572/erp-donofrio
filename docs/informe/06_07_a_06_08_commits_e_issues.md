# 6.7 y 6.8 Resumen de commits y de issues

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [02 §2.2](../plan/02_mapeo_plantilla.md), [06 §6.7 y §6.8](../plan/06_github_ci_infra.md), [04 §4.11](../plan/04_scrum_pmbok.md)
>
> Las cifras se miden con [`scripts/estadisticas_repo.py`](../../scripts/estadisticas_repo.py) (solo lectura, repetible) y están guardadas con fecha en [las estadísticas de commits e issues](../capturas/sprint-4/S4_informe_final_estadisticas_commits_issues.md) (la del 23/11 sigue en [las estadísticas de commits e issues](../capturas/sprint-3/S3-informe6_estadisticas_commits_issues.md)). **Fecha de corte: 25/11/2026**, con `develop` en `339c907`; son **82 PR** fusionados.

## 6.7 Resumen de commits

### Convención

Los commits siguen **Conventional Commits en español** con la etiqueta de la historia de usuario o del sprint al final:

```
feat(facturacion): factura (01) y boleta (03) con IGV desde el pedido, en su diario [HU-15]
docs(informe): 4.7 métricas clave, KPI y acuerdos de nivel de servicio [S3]
```

El tipo (`feat`, `fix`, `docs`, `test`, `perf`, `chore`, `ci`…) dice qué cambia; el alcance, dónde; y la etiqueta `[HU-xx]` o `[Sn]`, a qué trabajo pertenece. Como `develop` se fusiona con **squash** (un commit por PR), **lo que queda en la historia es el título del PR**, y es ahí donde se exige la etiqueta.

### Estadísticas por autor

**Commits que quedaron en `develop`** (sin contar los de fusión), según `git log --no-merges --numstat` sobre `develop` el 25/11/2026 (no cuenta los archivos binarios, como las capturas):

| Autor | Commits en `develop` | Líneas agregadas | Líneas quitadas |
|---|---|---|---|
| Orlando (`orlando572`) | 52 | 44 387 | 802 |
| Evelyn (`Eve3000a`) | 39 | 13 108 | 257 |
| **Total** | **91** | 57 495 | 1 059 |

![Contributors de GitHub](../capturas/sprint-3/S3-6.7_github_contributors.png)

*La captura de GitHub Insights es del 23/11/2026 (65 commits) y no se repitió; las cifras de la tabla son las del 25/11.* Hay 108 commits en total en `develop`: los 91 de arriba y 17 de fusión (todos de los sprints 0 a 2). Las cifras de líneas incluyen datos, pruebas, documentación y diagramas; no miden esfuerzo, solo volumen.

**Commits dentro de los PR** (el trabajo antes del *squash*, con el login de GitHub):

| Autor | PR fusionados | Commits dentro de los PR | % |
|---|---|---|---|
| orlando572 | 43 | 180 | 58 % |
| Eve3000a | 39 | 132 | 42 % |
| **Total** | **82** | **312** | 100 % |

**Una sola persona con dos firmas.** Evelyn aparece con dos correos en `git` (36 commits con su correo de GitHub y 3 con un correo personal); es la misma persona y sus 39 commits se cuentan juntos.

### Tipos de commit

| Tipo | Cantidad |
|---|---|
| `docs` | 185 |
| `feat` | 82 |
| `fix` | 14 |
| `test` | 13 |
| `chore` | 9 |
| `ci` | 3 |
| `perf` | 3 |

El proyecto es mayormente **documentación y configuración**: el 59 % de los commits dentro de los PR son `docs` (185 de 312: el informe, las actas, las evidencias y los manuales) y el 26 %, `feat` (82: módulos, datos y scripts). Los 14 `fix` incluyen las correcciones de M1 y M4 durante la prueba de pantalla.

### Cumplimiento de la convención

| Regla | Resultado |
|---|---|
| Commits que siguen Conventional Commits | **309 de 312 (99 %)** |
| Commits que llevan la etiqueta `[HU-xx]` o `[Sn]` | 70 de 312 (22 %) |
| **Títulos de PR** (lo que queda en `develop`) con convención y etiqueta | **79 de 82 (96 %)** |

- **Los 3 commits fuera de la convención** son commits de fusión escritos a mano al resolver conflictos (`merge: integra develop (…)`, en los PR #168, #170 y #179). Usan un tipo, `merge:`, que no es de Conventional Commits.
- **El 22 % de commits con etiqueta es bajo a propósito de la regla:** la etiqueta se exige en el **título del PR**, que es el commit que sobrevive al *squash*; los commits intermedios de una rama no siempre la llevan. Con esa medida, **79 de 82 PR cumplen**.
- **Los 3 PR fuera de la regla** son el #176 (capturas de HU-11, HU-12 y HU-14 del S2, sin etiqueta) y los dos PR de release, el #222 y el #229, cuyos títulos usan `release:`, un tipo que no está en la lista de Conventional Commits del proyecto (llevan la etiqueta `[S3]` y `[S4]`).

### Qué se aprendió

- La regla de la etiqueta en el título del PR funciona y deja una historia legible: cada commit de `develop` se enlaza con una HU o un sprint. Este informe y su PR de cierre usan la etiqueta `[S4]`: el plan no asigna una HU al informe final, que es el issue de gestión #149.
- Falta una regla para los commits de fusión; se sugiere **no hacerlos a mano** (rebasar la rama) o usar el tipo `chore(merge)`.

## 6.8 Resumen de issues

### Qué hay

GitHub tiene **22 issues** (9 abiertos y 13 cerrados). **Ninguno es de tipo «bug»** (aún no se registró ningún defecto de software; las fallas del servicio van a la mesa de servicios de TI, no a GitHub). Las épicas agrupan las HU de un área y un dueño, con una checklist de HU dentro de cada una.

| Tipo | Total | Abiertos | Cerrados |
|---|---|---|---|
| Épica | 15 | 4 | 11 |
| Gestión | 7 | 5 | 2 |

| Fase | Total | Abiertos | Cerrados |
|---|---|---|---|
| Fase 1 (núcleo) | 17 | 6 | 11 |
| Fase 2 (módulos propios) | 5 | 3 | 2 |

| Área | Total | Abiertos | Cerrados |
|---|---|---|---|
| docs | 6 | 5 | 1 |
| infra | 6 | 0 | 6 |
| ventas | 3 | 2 | 1 |
| extras | 2 | 0 | 2 |
| gerencia | 2 | 1 | 1 |
| producción | 2 | 1 | 1 |
| logística | 1 | 0 | 1 |

Los 9 issues abiertos son: el registro de riesgos (#131), las dailies (#132), el Gate 0 (#143), las épicas de M1 y M2 (#144 y #145, con módulos ya fusionados y una casilla sin marcar), la opcional HU-31 (#148), la épica de gerencia (#141) y los dos del Cierre (#149 informe final y #150 entrega). Los módulos M3 y M4 (#146 y #147) están cerrados.

### Etiquetas y milestones

Cada issue lleva tres etiquetas: **`tipo:`** (épica, gestión o bug), **`area:`** (ventas, logística, producción, gerencia, infra, extras o docs) y **`fase-`** (1 o 2). Y un **milestone** por sprint:

| Milestone | Total | Abiertos | Cerrados |
|---|---|---|---|
| Sprint 0 – Inicio | 4 | 2 | 2 |
| Sprint 1 – Fundaciones | 3 | 0 | 3 |
| Sprint 2 – Procesos estándar | 4 | 0 | 4 |
| Sprint 3 – Calidad del núcleo | 4 | 2 | 2 |
| Sprint 4 – Módulos propios | 5 | 3 | 2 |
| Cierre | 2 | 2 | 0 |

Los abiertos del Sprint 0 son el registro de riesgos (#131) y las dailies (#132), que se cierran al final del proyecto.

### Cierre de issues con los PR

Cada PR dice en su descripción a qué épica pertenece:

| Forma | PR | Cuándo se usa |
|---|---|---|
| `Parte de #n` | 51 | El PR es parte de la épica, pero no la termina |
| `Closes #n` | 5 | **El último PR de la épica**, que la cierra al fusionarse |
| Sin enlace a una épica | 26 | Documentación, capturas y actas que no son parte de una HU |

La regla es que **solo el último PR de una épica la cierra** (`Closes`), para que una épica no se cierre con trabajo a medias. Ejemplo: HU-16 cerró la épica #139 («Transacciones de demostración») con `Closes #139` porque era la única HU que quedaba.

### Prevención de defectos

- Una **plantilla de PR** con checklist (Definition of Done) y una plantilla de **bug** (`bug.yml`) para registrar defectos del software, con pasos para reproducir.
- **CI obligatorio** (`lint` y `test`): ningún PR se fusiona con el CI en rojo.
- **Revisión del otro integrante** en todos los PR.
- **Pruebas** que fallan si se rompe lo ya hecho (218 pruebas al 25/11/2026: 137 de `donofrio_base` y 81 de los módulos propios).

### Hallazgos de gestión

- Las épicas #142, #146 y #147 están cerradas, pero su tarjeta del Project sigue en «Backlog»; la #144 está abierta con su tarjeta en «Hecho» ([6.3](06_01_a_06_03_equipo_sprints_y_project.md#hallazgos-de-gestión-al-25112026)).
- Quedan 26 PR (de 82) sin enlace a una épica: son documentación, capturas y actas, además de los dos PR de release; se aceptan porque no cierran trabajo de una HU.
- **Ningún issue de tipo bug** en todo el proyecto, aunque las pruebas de pantalla de M1 y M4 hallaron defectos (por ejemplo, la tarjeta de un módulo opcional que rompía todo el tablero y el «Error de acceso» para usuarios sin permiso de lotes); se corrigieron dentro de sus PR (#228) y quedaron documentados en 5.5e y en el mini gate de M4 en lugar de abrir issues.
