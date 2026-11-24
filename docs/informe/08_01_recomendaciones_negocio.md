# 8.1 Recomendaciones de negocio

> **Estado:** borrador del Sprint 3 · **Autora:** Evelyn · **Revisa:** Orlando · **Fuente:** [7 Conclusiones](07_conclusiones.md), [4.1.4](04_01_04_oportunidades_innovacion.md), [3.7](03_aspectos_generales.md) (indicadores), [4.2.2](04_02_requerimientos_funcionales.md) y las evidencias de `docs/capturas/sprint-3/`
>
> Son recomendaciones **para una empresa como D'Onofrio** a partir de lo que el proyecto probó; los datos de la empresa son ficticios (supuesto S2) y las mediciones salen de una sola PC. Las recomendaciones **técnicas** (8.2) las redacta Orlando. Si el Gate 0 aprueba algún módulo de la Fase 2, las recomendaciones 2 a 4 se actualizan.

## 8.1.1 Resumen

| # | Recomendación | Problema que atiende (3.2.4) | Plazo | Esfuerzo |
|---|---|---|---|---|
| 1 | Poner en marcha el núcleo con datos reales y capacitación por rol | 2, 5, 6 y 7 | Corto | Bajo |
| 2 | Digitalizar la liquidación de los heladeros | 1 | Corto a mediano | Medio |
| 3 | Registrar la calidad y la temperatura ligadas al lote | 3 y 4 | Mediano | Medio |
| 4 | Resolver la facturación electrónica con SUNAT | (limitación de RF016) | Corto | Medio |
| 5 | Medir con los indicadores del tablero y decidir con ellos | 5 y 7 | Continuo | Bajo |
| 6 | Corregir el despacho del punto de venta (FEFO) | 2 | Corto | Bajo |
| 7 | Mantener la continuidad y la seguridad que el proyecto dejó probadas | (RNF006, RNF009) | Continuo | Bajo |
| 8 | Preparar el sistema para el escenario Froneri | (riesgo del entorno) | Mediano | Bajo |

## 8.1.2 Recomendaciones

### 1. Poner en marcha el núcleo con datos reales y capacitación por rol

**Qué.** Pasar de los datos ficticios a los datos reales por áreas, en este orden: almacenes y productos, clientes y listas de precios, proveedores e insumos, y empleados. Capacitar a cada rol con los casos de uso de [4.2.4](04_02_casos_de_uso.md), que ya describen cada flujo.

**Por qué.** El ciclo vender, comprar, producir y facturar funciona de punta a punta sobre 16 semanas de datos de demostración, y resuelve cuatro de los siete problemas del caso con la Fase 1 sola (2, 5, 6 y 7).

**Cómo.** Ya existe un único ERP con los datos cargados por código, así que el reemplazo es de contenido, no de programación. Conviene hacerlo **por áreas y no todo a la vez**: primero Logística y Producción (lotes y vencimientos), después Ventas y Facturación.

**Riesgo si no se hace.** Los datos ficticios no sirven para decidir, y sin capacitación los usuarios vuelven al Excel.

**Limitación.** La prueba de usabilidad con 5 personas (HU-30) quedó pendiente: se tiene el plan y el cuestionario SUS, pero **no hay una medición**. Antes de capacitar a todos, conviene hacerla con los usuarios reales y corregir lo que se encuentre (meta: SUS ≥ 70).

### 2. Digitalizar la liquidación de los heladeros

**Qué.** Liquidar a cada heladero por día con lo despachado, lo devuelto y la merma, y calcular lo vendido, el importe y la comisión.

**Por qué.** Es el proceso más reconocible de D'Onofrio y el que concentra el problema 1: descuadres y mermas que no se rastrean hasta un lote. Con la Fase 1 solo se cubre en parte (pedido de venta con la lista «Heladero» y devolución estándar): no hay merma ni comisión como campos, ni PDF para firmar.

**Cómo.** Dos pasos. Primero, usar ya la variante estándar con la lista «Heladero» (BPMN TO-BE 11). Después, construir el módulo `donofrio_heladeros` (RF004), que está diseñado con su caso de uso (CU004), su wireframe, su mockup móvil y el PDF de liquidación ([4.4](04_04_prototipos.md)).

**Indicador.** Descuadre por heladero menor al 2 % de lo despachado ([3.7](03_aspectos_generales.md), meta supuesta).

**Riesgo si no se hace.** Se mantiene la pérdida de dinero de la última milla, que es el argumento de negocio más fuerte del proyecto.

### 3. Registrar la calidad y la temperatura ligadas al lote

**Qué.** Inspecciones por puntos de control ligadas a la orden de producción y al lote, certificado de calidad en PDF y registro de temperaturas por cámara con alertas.

**Por qué.** La empresa produce alimentos perecibles, y hoy la inspección y la temperatura quedan en papel (problemas 3 y 4). Con la Fase 1 el lote es trazable de la compra del insumo a la entrega, pero el **bloqueo de un lote rechazado** y las **alertas de temperatura** no existen. Esto respalda ISO 9001 y HACCP como buenas prácticas de referencia, sin certificar nada.

**Cómo.** Los módulos `donofrio_calidad` (RF011 y RF012) y la cadena de frío (RF008) están diseñados (CU006 y CU008). En Community no hay inspecciones de calidad: el módulo Calidad es Enterprise, por eso se propone módulo propio.

**Mientras tanto.** La Fase 1 deja el control como **documental** en el nombre de cada operación (por ejemplo, pasteurizar a 80-85 °C) y una nota en la orden. Se recomienda que Aseguramiento de Calidad la use desde el primer día.

### 4. Resolver la facturación electrónica con SUNAT

**Qué.** El ERP emite factura (01) y boleta (03) con IGV 18 % desde el pedido, pero **no las envía a SUNAT**, porque `l10n_pe_edi` es Enterprise.

**Por qué.** Los comprobantes electrónicos son obligatorios (SUNAT); sin el envío, el ERP no reemplaza al sistema contable actual.

**Cómo.** Evaluar, antes de poner el ERP en producción, entre conectar el ERP a un proveedor de servicios electrónicos autorizado, o mantener el sistema actual solo para el envío y conciliar con la numeración de Odoo. No se evaluó ninguna de las dos opciones en este proyecto: es una **decisión pendiente** de Finanzas y TI, y el costo no se estimó.

### 5. Medir con los indicadores del tablero y decidir con ellos

**Qué.** Usar los dashboards estándar y las vistas guardadas (ventas por línea, canal y mes; producción por producto y mes; stock por vencer a 30 días) en la reunión semanal de la gerencia.

**Por qué.** La gerencia hoy recibe reportes armados a mano al cierre del mes (problemas 5 y 7). Los datos de demostración muestran la estacionalidad (helados en verano, panetón en Navidad), que es la base para producir con anticipación.

**Cómo.** Adoptar los KPI de [3.7](03_aspectos_generales.md) como punto de partida y ajustar sus metas con datos reales: las actuales son supuestos (por ejemplo, +10 % de ventas, menos del 2 % de stock vencido o por vencer, 95 % de pedidos a tiempo).

**Limitación.** El rendimiento del backend es 59 frente a la meta de 80 (login 100, dashboard 80). Se recomienda usarlo en un equipo con memoria suficiente y navegador actualizado hasta que se mida en el servidor real.

### 6. Corregir el despacho del punto de venta (FEFO)

**Qué.** En el punto de venta el cajero escribe el lote y Odoo estándar no comprueba su fecha de vencimiento ni propone el que vence antes: una venta de mostrador puede salir con un lote vencido (RNF005).

**Por qué.** Es el único hueco del control FEFO que el proyecto detectó y es el más barato de cerrar: una restricción sobre el detalle del movimiento, con su prueba.

**Mientras tanto.** Instruir al cajero para que elija el lote que **vence primero** y revisar el reporte de stock por vencer a 30 días cada semana.

### 7. Mantener la continuidad y la seguridad que el proyecto dejó probadas

**Qué.** Operar con lo que ya está medido: réplica en caliente, respaldo diario con retención de 7 días (restauración probada en 31 s), Nginx con TLS, verificación en dos pasos para administración y gerencia, contraseñas de 12 o más y auditoría de cambios en precios, pedidos y compras.

**Por qué.** El negocio es estacional y no puede perder sus datos en temporada alta. Todo esto está probado en una PC, no en el servidor real.

**Cómo.** Repetir la prueba de restauración en el servidor definitivo, guardar una copia **fuera** del servidor y medir la disponibilidad en el tiempo (RNF011 sigue pendiente; la meta es 99 %).

### 8. Preparar el sistema para el escenario Froneri

**Qué.** Si el negocio de helados cambia de dueño, el ERP debe poder seguir con chocolates y panetón.

**Por qué.** El diseño separa líneas de producto y canales, y las listas de precios por temporada; no se modeló la transición porque no está confirmada para Perú (supuesto S1).

**Cómo.** Mantener las líneas separadas en los datos reales (categorías y equipos de venta) y no mezclar costos entre líneas; así se puede separar o conservar cada una sin rehacer el sistema.

## 8.1.3 Hoja de ruta sugerida

| Etapa | Qué hacer | Recomendaciones |
|---|---|---|
| **Corto plazo** (primeras semanas) | Cargar datos reales por áreas, capacitar y medir la usabilidad con usuarios reales; decidir cómo se envían los comprobantes a SUNAT; corregir el FEFO del punto de venta | 1, 4, 6 |
| **Mediano plazo** | Liquidación de heladeros y, después, calidad y temperaturas; ajustar las metas de los KPI | 2, 3, 5 |
| **Continuo** | Respaldos probados, seguridad y observación del escenario Froneri | 7, 8 |

## 8.1.4 Lo que este proyecto no permite afirmar

- **No hay costos ni retorno de la inversión.** No se estimaron costos de implantación, capacitación ni de soporte; la única cifra de costo es la licencia, que es cero porque se usa Odoo Community.
- **No hay datos reales de D'Onofrio.** Los problemas son supuestos del caso (S7); las metas de los KPI también.
- **Las mediciones salen de una PC.** Los resultados de carga, seguridad y rendimiento no sustituyen una prueba en el servidor definitivo.
- **La Fase 2 no se construyó.** Las recomendaciones 2 y 3 se apoyan en diseños, no en código probado.
