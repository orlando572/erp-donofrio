# Sprint 2 (Procesos estándar): Retrospectiva

**Fecha:** 23/11/2026 · **Facilita:** Orlando (SM)
**Estado:** confirmada por Evelyn el 23/11/2026. La documentación de Evelyn del S2 ya se subió (PR #181); las acciones de mejora quedan para antes del Gate 0 y el S3.

## Seguimiento de las acciones de la Retro del S1

| # | Acción | Resultado |
|---|---|---|
| 1 | Decidir si se activa `enforce_admins` en `develop` | **Decidida el 23/11/2026 por Evelyn (PO): se deja desactivado.** La protección exige 1 aprobación y los checks `lint` y `test`, pero no aplica a administradores; se conserva esa salida de emergencia y se compensa cumpliendo siempre la revisión cruzada |
| 2 | Un PR por HU, directo contra `develop`, sin apilar | **Cumplida.** Los 8 PR del S2 (#173 a #180) se abrieron contra `develop`, se fusionaron en orden y ninguno perdió su aprobación |
| 3 | Demo cruzada de una HU ajena en la Review | **Pendiente.** No se hizo en el S2; se hace antes del Gate 0 |
| 4 | Cerrar el registro de riesgos (#131) y las Dailies (#132) | **Pendiente.** Siguen abiertos; se cierran en el S3 |

## Qué salió bien

- Las 9 HU quedaron fusionadas: 30 de 30 puntos, con CI en verde en `develop`.
- El script `cargar_transacciones.py` dejó 16 semanas de datos reproducibles (semilla fija) con la estacionalidad visible en los gráficos de ventas.
- Las pruebas pasaron de 38 a 100 y cada PR llegó con las suyas.
- La revisión cruzada encontró problemas reales antes de que se acumularan: la vigencia de las listas de precios estaba en UTC y no en hora de Lima (PR #171) y el PdV no aplica FEFO.
- Evelyn y Orlando se repartieron HU-16 por áreas y las dos partes encajaron en un solo script.

## Empezar

- Pedir la aprobación del otro integrante apenas el CI esté en verde, no al final: los PR de Orlando #173 a #177 esperaron a Evelyn y se fusionaron juntos.
- Marcar la checklist de la épica con el enlace al PR y pasarla a «Hecho» en el Project en cuanto se fusiona cada HU. En el S2 las épicas #137, #138 y #139 se cerraron pero seguían en «Backlog» en el Project, y la checklist de #138 sin marcar.
- Probar cada caso de la UI con la base recreada desde cero (`scripts/init_db.sh`), no con una base arrastrada de pruebas anteriores.
- Hacer la demo cruzada el mismo día que se cierra la HU.

## Dejar de hacer

- Dar por buena una receta o un dato maestro sin revisar su costo: las recetas de HU-07 daban un costo por unidad mayor que el precio de venta y se descubrió recién en HU-14.
- Asumir que `l10n_pe` deja la valoración lista: en Odoo 19 no trae cuentas en las ubicaciones virtuales y los asientos de valoración no se generaban.
- Dejar la documentación del sprint para el final: la de Evelyn entró (PR #181) horas después de que el código ya estaba fusionado.

## Continuar

- Una rama y un PR por HU, directo contra `develop`, con `[HU-xx]` en cada commit.
- Datos y configuración por código, con pruebas.
- Dejar por escrito las limitaciones y decisiones (FEFO en el PdV, boleta con plantilla de factura, `enforce_admins`) con el número de PR.
- Avisar al otro integrante antes de fusionar un cambio de datos `noupdate`, porque obliga a recrear su base.

## Acciones de mejora

| # | Acción | Responsable | Para cuándo |
|---|---|---|---|
| 1 | ~~Decidir si se activa `enforce_admins` en `develop`~~ Decidido: queda desactivado; solo fusionar con la aprobación del otro y el CI en verde | Orlando y Evelyn | Hecho (23/11) |
| 2 | Hacer la demo cruzada de una HU ajena (Evelyn una de Orlando y viceversa) | Orlando y Evelyn | Antes del Gate 0 |
| 3 | Cerrar el registro de riesgos (#131) y las Dailies (#132) | Evelyn y Orlando | S3 |
| 4 | Marcar la checklist de la épica con el enlace al PR y pasarla a «Hecho» al fusionar cada HU | Evelyn y Orlando | S3 |

## Riesgos

Ningún riesgo cambia de nivel. R4 (carga desigual y defensa de cada parte) sigue abierto: la demo cruzada pendiente es la forma de cubrirlo. El hallazgo del PdV sin FEFO queda aceptado como limitación de RNF005 en la Fase 1. El seguimiento se registra como comentario en el issue #131.

## Aportes de Evelyn a la Retro

- **Qué aprendí:**
  - Las fechas de vigencia de las listas se guardan en UTC: una vigencia «a medianoche» se veía 5 horas corrida en Lima (PR #171). Desde entonces, las fechas de los datos se escriben en UTC con la hora de Lima y se prueba el borde.
  - Un dato creado por el hook de instalación no existe en una base ya creada: el PdV, la facturación y los diarios necesitaron una llamada única en `odoo shell` o recrear la base.
  - HU-16 dependía de HU-13 y HU-15 sin fusionar. Tuve que trabajar sobre una rama de integración local y rebasarla al fusionarse; fue la razón de que HU-16 esperara.
- **Para el S3:** aprobar los PR del otro apenas el CI esté en verde, y pasar la épica a «Hecho» al fusionar su último PR.
