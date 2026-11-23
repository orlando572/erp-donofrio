# Plan de calidad

[← docs/pm](.)

Versión S0, 22/11/2026. Redactado por Orlando por encargo de Evelyn (PO), que debe revisarlo.

La calidad se controla con dos mecanismos: la **Definition of Done** (personas) y el **CI** (automatización). Detalle en [04 §4.8](../plan/04_scrum_pmbok.md) y [06 §6.4](../plan/06_github_ci_infra.md).

## Definition of Done de cada HU

1. El código está en un PR hacia `develop` **aprobado por el otro integrante**.
2. El CI está en verde: lint, chequeo de patrones legacy e instalación desde cero con `--test-enable`, sin `ERROR`.
3. La lógica nueva tiene tests (`TransactionCase`) y los modelos nuevos tienen ACL.
4. Se actualiza el módulo sin errores (`-u`) sobre una BD con datos.
5. Los textos visibles están en español y los criterios de aceptación se verificaron en la UI.
6. Hay capturas de evidencia en `docs/capturas/sprint-N/` (`HU-xx_descripcion.png`).
7. El ítem de Monday está en "Hecho" con el enlace al PR; el issue se cierra con `Closes #n`.
8. La sección del informe que corresponde tiene al menos un borrador.

**Módulo de la F2:** sus HU cumplen la DoD, hay tag de release, las secciones afectadas del informe están actualizadas, el ER y el diccionario se extrajeron de nuevo y el mini gate está escrito.

## Controles automáticos

| Control | Qué detecta | Estado en S0 |
|---|---|---|
| Hook anti-legacy (`.claude/hooks/bloquear_legacy.py`) | Patrones de Odoo ≤ 16 al editar con el agente | Activo y probado |
| `scripts/check_legacy.sh` | Los mismos patrones, en pre-commit y CI | Listo; se conecta al CI en HU-02 |
| CI (`ci.yml`: `lint`, `test`, `upgrade` opcional) | Errores de instalación, tests rojos, patrones legacy | HU-02 (S1) |
| Plantillas de issue y PR con la checklist de la DoD | Olvidos en la revisión | Activas |
| Protección de `main` y `develop` | Cambios sin PR ni aprobación | Activa; el check de CI se exige cuando exista |
| Secret scanning y push protection | Secretos subidos al repo público | Activos |

## Revisión cruzada

Cada integrante revisa todos los PR del otro con la checklist de la DoD. Una sección del informe se considera completa cuando tiene texto propio, leyendas numeradas, fuentes citadas, al menos una evidencia real y la revisión del otro integrante.

## Métricas de calidad

Las metas verificables están en los RNF ([04 §4.2](../plan/04_scrum_pmbok.md)): p95 < 2 s con 20 usuarios (k6), SUS ≥ 70, Lighthouse Performance ≥ 80 (escritorio), CI en verde, restauración con RTO ≤ 2 h y entorno reproducible con un comando.
