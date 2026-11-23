# Sprint 2: Daily Scrum

Formato asíncrono. Se publica también como comentario en el issue «Dailies» (#132) del GitHub Project.

## 23/11/2026: Orlando

- **Qué hice:**
  - Revisé el PR #167 de Evelyn (HU-09, listas de precios): datos y pruebas correctos, CI en verde.
  - Dejé listas las cuatro ramas de mi parte, cada una con su commit y sus pruebas: HU-11 (lotes y FEFO, PR #169 abierto, CI en verde), HU-12 (recepción y despacho en 2 pasos), HU-14 (órdenes de producción, costo y valoración) y HU-16 en lo de inventario y producción (`cargar_transacciones.py`).
  - Encontré y corregí dos problemas: las recetas de HU-07 daban un costo por unidad mayor que el precio de venta (se pasaron a tandas industriales) y Odoo 19 no generaba asientos de valoración porque `l10n_pe` no trae cuentas en las ubicaciones virtuales (se asignan por código en el hook).
  - Recreé mi base de datos con los datos nuevos, cargué 16 semanas de demostración (188 órdenes de producción y 581 asientos) y tomé las capturas de HU-11, HU-12 y HU-14.
  - Documentación: BPMN TO-BE de producción (sin y con M1) y de recepción y despacho, fichas de CU005 a CU008, 4.3.2, 4.3.3 y el borrador del manual de instalación.
- **Qué haré:**
  - Abrir los PR de HU-12, HU-14 y HU-16 de a uno, cuando se fusione el anterior, y pedir la aprobación de Evelyn.
  - Actualizar la checklist de las épicas #138 y #139 con el enlace a cada PR.
  - Redactar la Review y la Retro del sprint.
- **Qué me bloquea:**
  - La aprobación de Evelyn al PR #169.
  - Avisar a Evelyn de que, con el PR de HU-14, debe recrear su base de datos.

> La Daily de Evelyn se agrega aquí cuando la redacte.
