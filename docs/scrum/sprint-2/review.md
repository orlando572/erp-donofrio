# Sprint 2 (Procesos estándar): Review

**Fecha:** 23/11/2026 · **Presenta:** Orlando (SM) · **PO:** Evelyn (pendiente de aceptar) · **Demo cruzada:** pendiente (ver más abajo)

## Objetivo

"El ciclo vender-comprar-producir-facturar funciona de punta a punta con datos."

**Resultado: cumplido en el código.** Las 9 HU del sprint están fusionadas en `develop` (30 de 30 puntos: Evelyn 14, Orlando 11 y 5 compartidos de HU-16) y las cuatro épicas (#136, #137, #138 y #139) están cerradas. El CI de `develop` (`lint` y `test`) está en verde en el último commit, el merge del PR #180. La documentación de Evelyn del sprint también está fusionada (PR #181).

## Incremento mostrado

| HU | Entregable | PR | Evidencia | Resultado |
|---|---|---|---|---|
| HU-08 (2 pts) | Embudo CRM con 3 equipos (Heladeros, Canal Tradicional y Canal Moderno), 5 etapas y 20 oportunidades; de una oportunidad se pasa a una cotización | #168 | `HU-08_embudo_kanban.png`, `HU-08_oportunidades_por_etapa.png` | Listo (Evelyn) |
| HU-09 (3 pts) | Listas de precios por canal y temporada (verano, Navidad, heladero); el pedido confirmado genera la entrega; vigencia en hora de Lima | #167, #171 | `HU-09_listas_de_precios.png`, `HU-09_lista_verano_vigencias.png` | Listo (Evelyn) |
| HU-10 (3 pts) | PdV con efectivo y Yape, boleta con DNI o cliente varios y cierre de caja cuadrado | #170, #172 | `HU-10_pdv_*.png` (6), `HU-10_boleta_facturacion.png`, `HU-10_metodos_de_pago.png` | Listo (Evelyn). Limitación: el PdV no aplica FEFO (ver «Pendiente») |
| HU-11 (5 pts) | Lotes con fecha de caducidad al recibir, salida FEFO en la entrega, alerta 30 días antes con el jefe de almacén como responsable | #169 | `HU-11_recepcion_lote_y_vencimiento.png`, `HU-11_lote_por_vencer.png` | Listo (Orlando) |
| HU-12 (3 pts) | Recepción desde la OC, despacho en 2 pasos (pick + ship) en Lima y reposición a Arequipa | #173 | `HU-12_recepcion_insumos.png`, `HU-12_pick_lima_reposicion_aqp.png` | Listo (Orlando) |
| HU-13 (3 pts) | 22 reglas mín./máx. de insumos; el planificador genera las RFQ (una por proveedor) y la OC confirmada crea la recepción | #179 | `HU-13_*.png` (5) | Listo (Evelyn) |
| HU-14 (3 pts) | OP que reserva insumos por FEFO, crea el lote con vencimiento, calcula el costo y genera asientos de valoración; recetas a tandas industriales | #174 | `HU-14_op_terminada_con_lote.png`, `HU-14_op_ordenes_de_trabajo.png` | Listo (Orlando) |
| HU-15 (3 pts) | Factura (01) y boleta (03) con IGV 18 % desde el pedido, en su diario y con PDF | #178 | `HU-15_*.png` (5) | Listo (Evelyn). Limitación: la plantilla estándar titula «Factura» a la boleta |
| HU-16 (5 pts) | `scripts/cargar_transacciones.py` con semilla fija: 16 semanas (3/8 al 22/11/2026) con estacionalidad visible. Orlando: inventario y producción · Evelyn: ventas, PdV y compras y 30 clientes ficticios | #175 (Orlando), #180 (Evelyn) | `HU-16_*.png` (5) | Listo |

**Datos que genera el script** (semilla 2026, cada corrida da lo mismo): 188 órdenes de producción y 581 asientos de valoración; 437 pedidos de venta por S/ 9 106 775, 939 pedidos de mostrador en 96 sesiones de caja cerradas, 95 compras con su factura de proveedor y 516 documentos de cliente (facturas `F` a crédito y boletas `B` pagadas).

**Calidad del incremento:** `donofrio_base` pasó de 38 a **100 pruebas** (`scripts/test.sh`), que corren en el CI de cada PR y en cada push a `develop`. Las capturas están en `docs/capturas/sprint-2/`. Todos los PR del sprint se abrieron directo contra `develop` y tuvieron la aprobación del otro integrante.

**Documentación de Orlando (DoD 8):** BPMN TO-BE de producción (sin y con M1) y de recepción y despacho, fichas CU005 a CU008, 4.3.2, 4.3.3 y borrador del manual de instalación (PR #177).

**Documentación de Evelyn (DoD 8):** BPMN TO-BE de venta B2B, compra de insumos y heladero (estándar y con M2), wireframes y mockups de 12 pantallas (incluidas las de la Fase 2), CU011 y CU012 (compras y facturación) y la sección 4.2.9 con el cronograma y el Gantt (PR #181).

## Cómo se demuestra

1. `cp .env.example .env && docker compose up -d --build && scripts/init_db.sh`.
2. Detener el servicio web y cargar los datos con `scripts/cargar_transacciones.py` por `odoo shell` (ver el manual de instalación).
3. Ventas → CRM (HU-08), listas de precios (HU-09) y Punto de venta (HU-10).
4. Inventario → Lotes (HU-11 y alerta por vencer), recepción desde la OC y traslado Lima → Arequipa (HU-12).
5. Fabricación → una OP hecha con su lote y sus asientos (HU-14); Compras → RFQ del planificador (HU-13); Contabilidad → facturas y boletas (HU-15).
6. Ventas → Análisis por mes y por equipo para ver la estacionalidad (HU-16).
7. `scripts/test.sh` para las 100 pruebas.

## Pendiente y deuda técnica

- **FEFO en el punto de venta (RNF005):** el cajero escribe el lote y Odoo estándar no comprueba su vencimiento. Decisión del 23/11: limitación declarada de la Fase 1 (CU005 y RNF005), sin restricción propia.
- **PDF de la boleta:** la plantilla estándar la titula «Factura» y rotula «RUC» al DNI. Se declara como limitación; no hay envío a SUNAT (el EDI es Enterprise).
- **Datos `noupdate`:** las recetas ajustadas en HU-14 obligan a recrear la base en cada PC. Orlando la recreó; Evelyn ya lo hizo con HU-16.
- **Stock de terminados sin receta:** solo tienen inventario inicial; las ventas se dimensionaron con el resumen que imprime el script.
- **Protección de `develop`:** sigue sin aplicar a administradores (`enforce_admins` desactivado). Decisión abierta desde el S1.
- **Demo cruzada** (05 §5.1): falta que Evelyn demuestre una HU de Orlando (por ejemplo HU-11 o HU-14) y Orlando una de Evelyn (por ejemplo HU-15 o HU-10). Se hace antes del Gate 0.
- **Valoración y costos:** las categorías usan FIFO y los asientos de valoración salen de cuentas asignadas por código a las ubicaciones virtuales, porque `l10n_pe` no las trae en Odoo 19.

## Decisión del PO

Pendiente de Evelyn (aceptar o rechazar el incremento).
