# 6.12 Pruebas de usabilidad

> **Estado:** método e instrumentos en borrador; **se harán la revisión por Orlando y Evelyn, el piloto y la iteración del plan, y después las mediciones con las 5 personas** · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [02 §2.2](../plan/02_mapeo_plantilla.md), [04 §4.4](../plan/04_scrum_pmbok.md) (HU-30) · **Requisito:** RNF003

## Método

Prueba de usabilidad con **5 participantes** sin experiencia previa en Odoo, **cuatro tareas cronometradas** de los procesos estándar y el cuestionario **SUS** (*System Usability Scale*, de 10 preguntas). Se eligió el SUS porque es corto, es un estándar reconocido y da un número comparable (68 es el promedio de la industria; el proyecto fija la meta en **70**, RNF003).

El detalle (participantes, entorno, consignas, criterios de éxito y limitaciones) está en [`docs/usabilidad/plan_de_pruebas.md`](../usabilidad/plan_de_pruebas.md); el cuestionario, en [`formulario_sus.md`](../usabilidad/formulario_sus.md).

| # | Tarea | Caso de uso | Usuario | Tiempo objetivo |
|---|---|---|---|---|
| T1 | Registrar una oportunidad de venta con la etiqueta «Bodega» | CU001 | Vendedor | 120 s |
| T2 | Preparar y confirmar un pedido con la lista de precios del cliente | CU002 | Vendedor | 180 s |
| T3 | Cobrar una venta en efectivo en el punto de venta | CU003 | Cajero | 150 s |
| T4 | Ver los lotes que vencen en 30 días | CU010 (vista guardada de HU-23) | Jefe de almacén | 90 s |

## Cómo se procesan los datos

`scripts/usabilidad_sus.py` lee el CSV de resultados y calcula el SUS de cada persona (de 0 a 100), el promedio y la mediana, la tasa de éxito y el tiempo mediano de cada tarea frente a su objetivo. La fórmula está verificada con casos conocidos (`--autotest`: todo 3 da 50; la mejor respuesta, 100; la peor, 0).

## Revisión e iteración antes de las pruebas

Antes de llamar a las 5 personas, el plan pasa por una revisión cruzada (Orlando y Evelyn), una prueba piloto de las cuatro tareas con la interfaz real y una iteración que corrige lo encontrado. El detalle está en [`plan_de_pruebas.md`](../usabilidad/plan_de_pruebas.md). Los datos del piloto no se cuentan en los resultados.

## Resultados

**Pendientes.** Se llenan cuando se hagan las pruebas con las 5 personas:

| Participante | T1 | T2 | T3 | T4 | SUS |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |
| P4 | | | | | |
| P5 | | | | | |
| **Promedio** | | | | | |

RNF003 se cumple si el SUS promedio es **≥ 70**. Con los resultados se agregan aquí: los problemas que aparecieron (con la frase de la persona), qué se cambiaría y la conclusión.

## Limitaciones

- Cinco personas dan una idea y no una estadística firme.
- Son voluntarios y no los usuarios reales de D'Onofrio (distribuidores, heladeros, cajeros).
- Solo se prueban las pantallas del núcleo (Fase 1); las de la Fase 2 quedan como diseño.
