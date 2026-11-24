# Sprint 1 (Fundaciones): Review

**Fecha:** 23/11/2026 · **Presenta:** Orlando (SM) · **PO:** Evelyn (pendiente de aceptar) · **Demo cruzada:** pendiente (ver más abajo)

## Objetivo

"Odoo 19 corre igual en ambas PC, con CI y datos maestros de D'Onofrio."

**Resultado: cumplido.** Las 7 HU del sprint están fusionadas en `develop` (24 de 24 puntos: Orlando 22, Evelyn 2) y las tres épicas (#133, #134 y #135) están cerradas y en «Hecho» en el Project.

## Incremento mostrado

| HU | Entregable | PR | Evidencia | Resultado |
|---|---|---|---|---|
| HU-01 (3 pts) | Entorno Docker con Odoo 19 y PostgreSQL 16; `docker compose up`, README y `scripts/init_db.sh` | #153 | `HU-01_odoo_login.png`, `S1_docker_compose_ps.png` | Listo. Reproducido desde cero en las PC de Orlando y de Evelyn (ambos servicios `healthy`, login 200) |
| HU-02 (5 pts) | CI en cada PR: `lint` (`check_legacy.sh` y `ruff`) y `test` (instalación con `--test-enable`); `scripts/test.sh`; `develop` exige ambos checks | #154, #159 | Pestaña Actions del repo | Listo. Falla con test rojo, error de instalación o patrón legacy (probado los tres casos); ver la salvedad de la protección más abajo |
| HU-03 (3 pts) | Compañía con localización peruana: RUC ficticio válido, PEN, IGV 18 %, `es_PE`, `America/Lima`, plan contable PE, logo y colores | #155 | `HU-03_compania.png`, `HU-03_reporte_estandar.png` | Listo |
| HU-04 (3 pts) | 10 usuarios por rol con mínimo privilegio y regla de registro del CD Arequipa; `test_seguridad.py` | #157 | `HU-04_usuarios.png`, `HU-04_liquidador_transferencias.png`, `HU-04_admin_transferencias.png` | Listo. El liquidador ve solo las transferencias de su almacén; el administrador ve ambas |
| HU-05 (2 pts) | Organigrama, 18 puestos y 21 empleados ficticios | #160 | `HU-05_organigrama_departamentos.png`, `HU-05_organigrama_empleados.png` | Listo (Evelyn) |
| HU-06 (3 pts) | Almacenes WH-LIM y WH-AQP, 8 ubicaciones de frío y seco, ruta Lima → Arequipa | #156 | `HU-06_almacenes.png`, `HU-06_ubicaciones.png`, `HU-06_rutas.png` | Listo |
| HU-07 (5 pts) | 25 productos terminados, 22 insumos y 12 recetas con operaciones; seguimiento por lote y vida útil; FEFO por categoría | #158 | `HU-07_productos.png`, `HU-07_recetas.png`, `HU-07_receta_operaciones.png` | Listo |

**Calidad del incremento:** `donofrio_base` tiene 38 pruebas (`scripts/test.sh`), que pasan en el CI de cada PR y en cada push a `develop`. Las capturas están en `docs/capturas/sprint-1/`.

**Documentación del sprint (DoD 8):** análisis de sistemas, BPMN AS-IS (5), RF, casos de uso, arquitectura empresarial, RNF e infraestructura, en `docs/informe/` y `docs/diagramas/` (PR #161 y #162).

## Cómo se demuestra

1. `cp .env.example .env && docker compose up -d --build && scripts/init_db.sh`.
2. Entrar a <http://localhost:8069> con `admin` y recorrer: Empresas (HU-03), Almacenes y Ubicaciones (HU-06), Productos y Listas de materiales (HU-07), Empleados (HU-05).
3. Entrar como `liquidador@donofrio.example.com` y comprobar en Inventario → Traslados que solo aparecen las del CD Arequipa (HU-04).
4. `scripts/test.sh` para las 38 pruebas.

## Pendiente y deuda técnica

- **Protección de `develop`:** exige 1 aprobación y los checks `lint` y `test`, pero no aplica a administradores (`enforce_admins` desactivado). En el sprint hubo cinco fusiones con excepción (#152 a #156), documentadas en 4.3.1. Decisión abierta: activar `enforce_admins`.
- **Colores de la compañía:** guardados y probados por test, pero aún no vistos en un reporte real; se verán con la primera factura (HU-15).
- **Nombres de las rutas de reabastecimiento:** los genera Odoo en inglés.
- **Valoración FIFO de las categorías:** queda para el costeo de la HU-14.
- **S0:** siguen «En curso» el registro de riesgos (#131) y las Dailies (#132).
- **Demo cruzada** (05 §5.1): cada integrante hace la demo de una HU ajena. Falta que Evelyn demuestre una HU de Orlando y Orlando una de Evelyn.
- **Capturas del Project:** en el PR #163.

## Decisión del PO

Pendiente de Evelyn (aceptar o rechazar el incremento).
