# Sprint 2: Daily Scrum

Formato asíncrono. Se publica también como comentario en el issue «Dailies» (#132) del GitHub Project.

## 23/11/2026: Orlando

- **Qué hice:**
  - Revisé los PR de Evelyn (HU-09, HU-13, HU-15 y HU-16 en ventas, PdV y compras, #167, #178, #179 y #180): datos y pruebas correctos, CI en verde.
  - Cerré las cuatro ramas de mi parte, cada una con su commit, sus pruebas y la aprobación de Evelyn: HU-11 (lotes y FEFO, #169), HU-12 (recepción y despacho en 2 pasos, #173), HU-14 (órdenes de producción, costo y valoración, #174) y HU-16 en lo de inventario y producción (`cargar_transacciones.py`, #175). Se fusionaron en ese orden, todos contra `develop`.
  - Encontré y corregí dos problemas: las recetas de HU-07 daban un costo por unidad mayor que el precio de venta (se pasaron a tandas industriales) y Odoo 19 no generaba asientos de valoración porque `l10n_pe` no trae cuentas en las ubicaciones virtuales (se asignan por código en el hook).
  - Recreé mi base de datos con los datos nuevos, cargué 16 semanas de demostración (188 órdenes de producción y 581 asientos) y tomé las capturas de HU-11, HU-12 y HU-14 (#176).
  - Documentación: BPMN TO-BE de producción (sin y con M1) y de recepción y despacho, fichas de CU005 a CU008, 4.3.2, 4.3.3 y el borrador del manual de instalación (#177).
  - Actualicé la checklist de la épica #138, pasé #137, #138 y #139 a «Hecho» en el Project y redacté la Review y la Retro del sprint.
- **Qué haré:**
  - Esperar el PR con la documentación de Evelyn del S2 y revisarlo.
  - Hacer la demo cruzada con Evelyn y pedirle la decisión del PO sobre el incremento.
  - Pasar al Sprint 3 (calidad del núcleo) y preparar el Gate 0.
- **Qué me bloquea:**
  - Nada.
  - Hallazgo al revisar HU-10: el PdV no aplica FEFO ni bloquea un lote vencido. Se declara como limitación de la Fase 1 (RNF005 y CU005).

## 23/11/2026: Evelyn

- **Qué hice:**
  - Dejé fusionadas mis seis HU del Sprint: HU-08 (CRM), HU-09 (listas de precios), HU-10 (PdV con boleta), HU-13 (reabastecimiento mín./máx.), HU-15 (factura 01 y boleta 03 con IGV) y mi parte de HU-16 (ventas, PdV y compras en `cargar_transacciones.py`, con 30 clientes ficticios). Las épicas #136, #137 y #139 quedaron cerradas y marcadas.
  - Corregí un desfase de la vigencia de las listas de precios (UTC contra Lima, PR #171) con una prueba de borde.
  - Con la base completa (437 pedidos de venta por S/ 9 106 775, 939 pedidos de mostrador y 95 compras) tomé las capturas de HU-08 a HU-16 en `docs/capturas/sprint-2/`.
  - Documentación: BPMN TO-BE de venta B2B, compra de insumos y heladero (estándar y con M2); wireframes y mockups de las 12 pantallas, incluidas las de la Fase 2; CU011 y CU012 (compras y facturación no tenían caso de uso); estados de CU001 a CU003 y RF001 a RF003, RF015 y RF016; y la sección 4.2.9 con el cronograma y el Gantt.
- **Qué haré:**
  - Abrir el PR de documentación a `develop` y pedir la aprobación de Orlando.
  - Aceptar el incremento del Sprint 2 como PO (Review pendiente de aceptar) y mover HU-16 a «Hecho» en el Project.
  - Redactar con Orlando el informe del Gate 0 (Sprint 3).
- **Qué me bloquea:**
  - Nada técnico. Para cargar los datos de demostración hay que recrear la base (`down -v` e `init_db.sh`) y detener el servicio web; cada integrante debe hacerlo en su PC.
  - Mi token de `gh` solo lee proyectos: mover las tarjetas del Project es manual.
