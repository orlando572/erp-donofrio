# Evidencias del Sprint 4 y del Cierre

Capturas de los módulos de la Fase 2 (`HU-17_*` a `HU-24_*`, en PNG de 1600 × 900 con los datos de demostración de la HU-16) y las evidencias que usa el informe final. El juego de capturas para el manual de usuario está en [`../manual/`](../manual/).

| Archivo | Sección del informe | Qué es |
|---|---|---|
| `S4_informe_final_prs_fusionados.tsv` | 6.4 a 6.6 y trazabilidad | Una fila por cada uno de los 82 PR fusionados (25/11/2026): autor, quién fusionó, método, aprobación del otro integrante, rama, fecha UTC, commits, merges de `develop` y rama base. Lo lee `scripts/trazabilidad.py` |
| `S4_informe_final_estadisticas_commits_issues.md` | 6.7 y 6.8 | Salida de `python3 scripts/estadisticas_repo.py` del 25/11/2026 |
| `S4_informe_final_burndown.csv` / `.svg` / `.png` | 6.2 | Burndown por puntos de los sprints 1 a 4 (`scripts/burndown.py --csv --svg`) |
| `S4_lighthouse_m4_resultados.csv` y `S4_lighthouse_m4.py` | 4.6.4, 5.5e y 5.14 | Lighthouse del tablero de M4 (76 en escritorio, 39 en móvil; LCP de 2,11 s): límite conocido |
| `S4_evidencia_verificacion_m4.txt` y `HU-22_evidencia_tablero.txt` | 5.5e | Verificación del tablero (carga, filtro por almacén, permisos) |
| `S4-release_v1.0.0.png`, `S4-paquete_ghcr.png` y `S4-release_corrida.png` | 6.4 | Release `v1.0.0`, paquete de GHCR y corrida de `release.yml` (24/11/2026, sin sesión) |
