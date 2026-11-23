# Sprint 3 (Calidad del núcleo): Review

**Fecha:** 23/11/2026 · **Facilita:** Orlando (SM) · **PO:** Evelyn (pendiente de aceptar) · **Demo cruzada:** pendiente · **Estado:** borrador preparado por Evelyn; Orlando lo revisa y lo presenta

## Objetivo

"Núcleo v1.0.0 entregable: seguro, replicado, probado, desplegado y documentado."

**Resultado: cumplido, salvo HU-30.** Ocho de las nueve HU del sprint están fusionadas en `develop` (27 de 29 puntos: Evelyn 12, Orlando 15 y 5 compartidos de HU-28 y HU-33 que se reparten entre los dos). La HU-30 (2 puntos, usabilidad con usuarios) sigue abierta: su plan, su cuestionario y su script están hechos, pero las pruebas con las 5 personas se harán después de la revisión del plan por Orlando y por Evelyn y de su iteración. Las épicas #140 y #142 están cerradas; la #141 sigue abierta por HU-30. El CI de `develop` está en verde.

## Incremento mostrado

| HU | Entregable | PR | Evidencia | Resultado |
|---|---|---|---|---|
| HU-23 (3 pts) | Dashboards estándar de Community (ventas, producto, almacén, facturación y PdV) y 4 vistas guardadas por código: ventas por línea, canal y mes (pivote y gráfico), producción por producto y mes, stock por vencer a 30 días | #188 | `HU-23_*.png` (5) | Listo (Evelyn) |
| HU-25 (3 pts) | Réplica de PostgreSQL en streaming con el perfil `replica`; la escritura en la réplica falla | #186 | `HU-25_evidencia_replica.txt` | Listo (Orlando) |
| HU-26 (3 pts) | Respaldo diario con retención de 7 días y restauración en una base nueva con el tiempo medido (RTO de 31 s frente a una meta de 2 h) | #187 | `HU-26_evidencia_respaldo.txt` | Listo (Orlando) |
| HU-27 (5 pts) | Despliegue protegido: Nginx con TLS, Odoo en modo producción (workers y proxy), 2FA para el administrador y la gerencia, contraseñas de 12 o más, bloqueo por intentos fallidos y auditoría de cambios | #189 | `HU-27_evidencia_seguridad.txt` | Listo (Orlando) |
| HU-28 (5 pts) | Carga con k6 (20 usuarios virtuales) y seguridad con ZAP baseline (Orlando); Lighthouse antes y después en login, backend y dashboard (Evelyn) | #196, #194 | `HU-28_*` (k6, ZAP y Lighthouse) | Listo. Limitación: el backend queda en 59 de rendimiento, por debajo de la meta de 80 |
| HU-29 (3 pts) | Release automática: un tag `vX.Y.Z` publica la imagen en GHCR y el zip en GitHub Releases (el `v1.0.0` se crea en el Gate 0) | #190 | `HU-29_evidencia_release.txt` | Listo (Orlando) |
| HU-30 (2 pts) | Plan de pruebas de usabilidad, cuestionario SUS y script de cálculo | #195 | `docs/usabilidad/` | **Pendiente**: faltan las pruebas con 5 personas (Evelyn) |
| HU-32 (2 pts) | Mesa de servicios en Project: 5 etapas, 3 tipos de ticket ITIL, 5 tickets de ejemplo, fecha límite según la prioridad y pivote de cumplimiento del SLA | #193 | `HU-32_*.png` (2) | Listo (Evelyn) |
| HU-33 (3 pts) | Pruebas de integración: pedido → entrega FEFO → factura (Evelyn) y compra → recepción → orden de producción → lote con vencimiento (Orlando), en el CI | #191, #192 | `test_flujo_venta.py` y la prueba de compra y producción | Listo |

**Medidas del sprint** (corridas reales del 23/11/2026, sobre una PC con datos de demostración): restauración en 31 s; p95 de 9 a 18 ms con 20 usuarios virtuales (342 ms en el login) frente a un límite de 2 s; ZAP sin alertas altas (4 medias y 3 bajas); réplica con un retraso de 2 ms; rendimiento web del dashboard de 45 a 80 y del login de 98 a 100.

**Calidad del incremento:** `donofrio_base` pasó de 100 a **136 pruebas** (`scripts/test.sh`), que corren en el CI de cada PR. Todos los PR del sprint se abrieron contra `develop` y tuvieron la aprobación del otro integrante.

**Documentación del sprint:**

| Quién | Entregables | PR |
|---|---|---|
| Evelyn | 4.6.1 a 4.6.3 (prototipos web y reportes), 4.7 (métricas, KPI y SLA), cascada COBIT, prácticas ITIL y anexos 10.3 y 10.5; **abiertos:** 6.1 a 6.3, 6.7 y 6.8; 1 Resumen y 7 Conclusiones | #201, #199, #203; #204, #205 |
| Orlando | 4.2.5 a 4.2.8 (clases, ER y diccionario), sección 5, 6.4 a 6.6 y 6.9 a 6.13, SoA y trazabilidad, anexo 10.4, abstract y manual de herramientas | #197, #198, #200, #202 |

## Cómo se demuestra

1. `docker compose up -d --build && scripts/init_db.sh`, y cargar los datos con `scripts/cargar_transacciones.py` (ver el manual de instalación).
2. Tableros → los cinco dashboards; Ventas → Análisis → Favoritos (HU-23).
3. Proyectos → Mesa de Servicios TI y el pivote de cumplimiento del SLA (HU-32).
4. `scripts/levantar_prod.sh` y `scripts/verificar_despliegue.sh` (HU-27), `scripts/verificar_replica.sh` (HU-25) y `scripts/verificar_backup.sh` (HU-26).
5. `python3 scripts/perf/lighthouse.py` y la prueba de carga de `scripts/perf/` (HU-28).
6. `scripts/test.sh` para las 136 pruebas.

## Pendiente y deuda técnica

- **HU-30:** revisión del plan por Orlando y por Evelyn, prueba piloto, iteración y después las 5 personas.
- **Gate 0 y `v1.0.0`:** falta el informe del Gate 0 (`docs/scrum/gates/gate-0-fase1.md`) y el tag. Además, `main` está **81 commits detrás de `develop`** y no tiene ninguna de las HU; el criterio de salida «CI en verde en `main`» exige fusionar `develop` en `main` antes del tag.
- **Demo cruzada** (05 §5.1): sigue sin hacerse; Evelyn demuestra una HU de Orlando y viceversa, antes del Gate 0 ([`demo_cruzada.md`](../sprint-2/demo_cruzada.md)).
- **Cierre de issues de gestión:** #131 (registro de riesgos) y #132 (dailies) siguen abiertos.
- **GitHub Project:** las iteraciones están en las fechas planificadas (S1 el 23/11, S3 el 25/11) y no en las reales, así que «Sprint actual» sigue mostrando el S1; y las tarjetas de #140 y #142 siguen en «Backlog» aunque sus épicas están cerradas, porque el *workflow* «Item closed» está desactivado.
- **Requerimientos no funcionales:** la tabla de 4.2.3 aún no refleja los resultados de HU-25 a HU-29; RNF001 (tres navegadores y móvil) y la medición de la disponibilidad en el tiempo (RNF011) siguen sin hacerse.
- **Rendimiento del backend:** 59 frente a la meta de 80; es el costo del JavaScript del cliente web de Odoo y se declara como limitación.

## Decisión del PO

Pendiente de Evelyn (aceptar o rechazar el incremento).
