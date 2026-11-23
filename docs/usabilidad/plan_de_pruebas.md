# HU-30: Plan de pruebas de usabilidad (6.12, RNF003)

> **Estado:** preparado el 23/11/2026 · **Responsable:** Evelyn (PO) · **Participantes:** 5 personas reales, **todavía sin reclutar ni medir**
>
> RNF003: interfaz en español, tareas clave en ≤ 3 pasos y **SUS ≥ 70**, con 5 usuarios y 4 tareas cronometradas.

## Objetivo

Comprobar que una persona sin entrenamiento previo puede hacer cuatro tareas de los procesos estándar de Odoo configurado para D'Onofrio, y medir qué tan usable le parece el sistema con el cuestionario SUS (*System Usability Scale*).

## Participantes

- **5 personas** que no hayan participado en el proyecto (compañeros de otra carrera, familiares o conocidos). Con 5 usuarios se detecta la mayoría de los problemas de usabilidad (Nielsen) y es lo que pide el plan.
- Sin experiencia previa con Odoo. Se anota su edad, su experiencia con sistemas de gestión (ninguna, poca, media o mucha) y si usa a diario el computador.
- **Consentimiento:** se les dice que se prueba el sistema y no a ellos, que pueden parar cuando quieran y que se guardan solo su código (P1 a P5), la edad y la experiencia. **No se registran nombres ni datos personales** (Ley 29733).

## Entorno

- Base de datos con los datos de demostración cargados (`scripts/cargar_transacciones.py`) y el idioma `es_PE`.
- Navegador en pantalla de escritorio, ventana nueva, sesión **ya iniciada** con el usuario de la tarea (el inicio de sesión no se cronometra). Las claves de prueba no se escriben en este documento.
- Quien modera **no ayuda**: solo lee la consigna, cronometra y anota. Si la persona se queda atascada más de 3 minutos en una tarea, se marca como **no completada** y se pasa a la siguiente.

## Las cuatro tareas

Cada tarea se lee tal cual, sin decir dónde hacer clic. Los pasos esperados son una estimación: **la prueba piloto (ver abajo) debe confirmarlos** contra la interfaz real.

| # | Proceso | Usuario | Consigna para la persona | Éxito si… | Pasos esperados | Tiempo objetivo |
|---|---|---|---|---|---|---|
| T1 | CRM (CU001) | Vendedor | «Un nuevo cliente, la *Bodega Don Pepe*, quiere comprar helados por unos S/ 3 000. Regístrelo como una posibilidad de venta del canal Tradicional.» | Existe la oportunidad con el cliente, el ingreso esperado y el equipo «Canal Tradicional» | 3 | 90 s |
| T2 | Cotización (CU002) | Vendedor | «Prepare un pedido de 100 paletas de fresa para la *Distribuidora Sur Ejemplo SAC* y confírmelo.» | El pedido está confirmado, con la lista de precios del cliente y la entrega creada | 3 | 180 s |
| T3 | Punto de venta (CU003) | Cajero | «Un cliente compra 2 paletas de fresa y paga en efectivo. Cobre la venta.» | La venta queda pagada y se muestra la boleta | 3 | 150 s |
| T4 | Consulta (CU010) | Jefe de almacén | «Vea qué lotes de productos vencen en los próximos 30 días.» | Llega a la vista de lotes por vencer (la vista guardada «Stock por vencer (30 días)») | 3 | 90 s |

Para T3 hay una sesión de PdV abierta antes de empezar. Para T2 el producto «Paleta de fresa» tiene existencias en Lima.

## Qué se anota por tarea y por persona

1. **Completada o no** (sin ayuda).
2. **Tiempo** en segundos, desde que termina de leer la consigna hasta que dice que terminó.
3. **Errores:** clics en un lugar equivocado o pasos de más, y una frase con lo que le costó.
4. Lo que dice en voz alta (qué esperaba ver y no vio).

Todo se registra en [`resultados_plantilla.csv`](resultados_plantilla.csv) (una fila por persona).

## Cuestionario SUS

Al terminar las cuatro tareas, cada persona responde las 10 preguntas del [formulario SUS](formulario_sus.md), en una escala de 1 (muy en desacuerdo) a 5 (muy de acuerdo). Se puede pasar por Google Forms (el plan lo indica) copiando los enunciados del archivo; el resultado se pasa al mismo CSV.

## Cómo se calcula

El script [`scripts/usabilidad_sus.py`](../../scripts/usabilidad_sus.py) lee el CSV y calcula:

- **SUS de cada persona:** (suma de las preguntas impares − 1 y de las pares 5 − valor) × 2.5, de 0 a 100.
- **SUS promedio y mediana** del grupo. **Se cumple RNF003 si el promedio es ≥ 70.** (68 es el promedio de la industria.)
- **Tasa de éxito** por tarea y **tiempo mediano** frente al objetivo.

```bash
python3 scripts/usabilidad_sus.py docs/usabilidad/resultados.csv
```

## Prueba piloto (antes de las cinco personas)

Una persona del equipo que no haya armado esa parte hace las cuatro tareas, para confirmar que: las consignas se entienden, los pasos y tiempos esperados son razonables, y los usuarios y datos de cada tarea existen. Lo que salga se corrige antes de empezar; los datos del piloto **no** cuentan.

## Limitaciones previstas

- Cinco personas dan una idea y no una estadística firme.
- No son los usuarios reales de D'Onofrio (distribuidores, heladeros, cajeros): son voluntarios, así que el resultado orienta pero no es una validación del negocio.
- Las pantallas de la Fase 2 (liquidación, inspección, tablero propio) no se prueban: se midieron solo las del núcleo.
