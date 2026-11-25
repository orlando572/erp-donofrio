# 8.1 Recomendaciones de negocio

> **Estado:** versión final del Cierre (25/11/2026) · **Autora:** Evelyn · **Revisa:** Orlando · **Fuente:** [7 Conclusiones](07_conclusiones.md), [4.1.4](04_01_04_oportunidades_innovacion.md), [3.7](03_aspectos_generales.md) (indicadores), [4.2.2](04_02_requerimientos_funcionales.md) y las evidencias de `docs/capturas/sprint-3/` y `sprint-4/`
>
> Son recomendaciones **para una empresa como D'Onofrio** a partir de lo que el proyecto probó; los datos de la empresa son ficticios (supuesto S2) y las mediciones salen de una sola PC. Las recomendaciones **técnicas** (8.2) las redacta Orlando. Con la Fase 2 completa, las recomendaciones 2, 3 y 5 pasan de «construir» a **«adoptar, medir y ampliar»** lo que ya está construido (M1 a M4); lo que sigue sin existir (sensores, app móvil, SUNAT) queda como trabajo futuro real.

## 8.1.1 Resumen

| # | Recomendación | Problema que atiende (3.2.4) | Plazo | Esfuerzo |
|---|---|---|---|---|
| 1 | Poner en marcha el sistema con datos reales y capacitación por rol | Los 7 | Corto | Bajo |
| 2 | Adoptar la liquidación diaria de los heladeros y llevarla a una app móvil | 1 | Corto a mediano | Medio |
| 3 | Operar la calidad y la cadena de frío ligadas al lote y conectar sensores | 3 y 4 | Mediano | Medio |
| 4 | Resolver la facturación electrónica con SUNAT | (limitación de RF016) | Corto | Medio |
| 5 | Medir con el tablero gerencial y decidir con él | 5 y 7 | Continuo | Bajo |
| 6 | Corregir el vencimiento en el despacho del punto de venta (FEFO) | 2 | Corto | Bajo |
| 7 | Mantener la continuidad y la seguridad que el proyecto dejó probadas | (RNF006, RNF009) | Continuo | Bajo |
| 8 | Preparar el sistema para el escenario Froneri | (riesgo del entorno) | Mediano | Bajo |

## 8.1.2 Recomendaciones

### 1. Poner en marcha el sistema con datos reales y capacitación por rol

**Qué.** Pasar de los datos ficticios a los datos reales por áreas, en este orden: almacenes y productos, clientes y listas de precios, proveedores e insumos, y empleados. Capacitar a cada rol con los casos de uso de [4.2.4](04_02_casos_de_uso.md), que ya describen cada flujo.

**Por qué.** El ciclo vender, comprar, producir y facturar funciona de punta a punta sobre datos de demostración (del 3/8 al 22/11/2026), y con la Fase 1 y la Fase 2 resuelve los siete problemas del caso (cuatro con la Fase 1 sola: 2, 5, 6 y 7).

**Cómo.** Ya existe un único ERP con los datos cargados por código, así que el reemplazo es de contenido, no de programación. Conviene hacerlo **por áreas y no todo a la vez**: primero Logística y Producción (lotes y vencimientos), después Ventas y Facturación.

**Riesgo si no se hace.** Los datos ficticios no sirven para decidir, y sin capacitación los usuarios vuelven al Excel.

**Limitación.** La usabilidad se evaluó con una revisión por roles y una evaluación heurística hechas por el equipo (6.12), no con usuarios reales. Antes de capacitar a todos, conviene observar a los usuarios reales con sus tareas y corregir lo que se encuentre.

### 2. Adoptar la liquidación diaria de los heladeros y llevarla a una app móvil

**Qué.** Usar el módulo `donofrio_heladeros` (M2, `v1.2.0`) para liquidar a cada heladero por día con lo despachado, lo devuelto y la merma, con el vendido, el importe, la comisión y el PDF para firmar; y, como trabajo futuro, una **app móvil** para el heladero y una merma que descuente inventario.

**Por qué.** Es el proceso más reconocible de D'Onofrio y el que concentra el problema 1: descuadres y mermas que no se rastrean hasta un lote. Con la Fase 1 sola se cubría en parte (pedido de venta con la lista «Heladero» y devolución estándar); M2 agrega la merma y la comisión como campos y el PDF para firmar. Con los datos de demostración, 124 de 127 liquidaciones están liquidadas y la merma es de 0,27 % de lo despachado.

**Cómo.** Dos pasos. Primero, capacitar a los liquidadores con CU004 y cargar los heladeros reales ([5.5c](05_05_modulo_donofrio_heladeros.md)). Después, revisar el formulario con los heladeros en el dispositivo que usen y evaluar una app o una PWA propia ([8.2.10](08_recomendaciones.md#8210-mejoras-de-los-módulos-de-la-fase-2-trabajo-futuro-real)).

**Indicador.** Descuadre por heladero menor al 2 % de lo despachado ([3.7](03_aspectos_generales.md), meta supuesta).

**Riesgo si no se hace.** Se mantiene la pérdida de dinero de la última milla, que es el argumento de negocio más fuerte del proyecto.

### 3. Operar la calidad y la cadena de frío ligadas al lote y conectar sensores

**Qué.** Usar las inspecciones por puntos de control ligadas a la orden de producción y al lote, el certificado de calidad en PDF (M1, `v1.1.0`) y el registro de temperaturas por cámara con alertas (M3, `v1.3.0`); y, como trabajo futuro, **sensores** que registren la temperatura y una alerta por lecturas que faltan.

**Por qué.** La empresa produce alimentos perecibles, y la inspección y la temperatura estaban en papel (problemas 3 y 4). Con la Fase 1 el lote es trazable de la compra del insumo a la entrega; con M1 y M3 se suman el **bloqueo de un lote rechazado** y las **alertas de temperatura**. Esto respalda ISO 9001 y HACCP como buenas prácticas de referencia, sin certificar nada.

**Cómo.** Los módulos `donofrio_calidad` (RF011, RF012 y RF008) están construidos ([5.5b](05_05_modulo_donofrio_calidad.md) y [5.5d](05_05_modulo_donofrio_frio.md)); en Community no hay inspecciones de calidad (el módulo Calidad es Enterprise), por eso se hizo módulo propio. Lo que falta: las lecturas son manuales, no hay alerta por lecturas que faltan y solo se inspeccionan las órdenes nuevas.

**Complemento.** Los puntos críticos de control (por ejemplo, pasteurizar a 80-85 °C) siguen escritos en el nombre de cada operación; la inspección de M1 los mide y los registra. Se recomienda que Aseguramiento de Calidad la use desde el primer día.

### 4. Resolver la facturación electrónica con SUNAT

**Qué.** El ERP emite factura (01) y boleta (03) con IGV 18 % desde el pedido, pero **no las envía a SUNAT**, porque `l10n_pe_edi` es Enterprise.

**Por qué.** Los comprobantes electrónicos son obligatorios (SUNAT); sin el envío, el ERP no reemplaza al sistema contable actual.

**Cómo.** Evaluar, antes de poner el ERP en producción, entre conectar el ERP a un proveedor de servicios electrónicos autorizado, o mantener el sistema actual solo para el envío y conciliar con la numeración de Odoo. No se evaluó ninguna de las dos opciones en este proyecto: es una **decisión que corresponde** a Finanzas y TI, y el costo no se estimó.

### 5. Medir con el tablero gerencial y decidir con él

**Qué.** Usar el tablero propio de M4 (Tablero › Gerencia, `v1.4.0`: ventas del mes, cumplimiento de producción, stock por vencer, lotes aprobados, liquidaciones pendientes y alertas de temperatura) y, para el detalle, los dashboards estándar y las vistas guardadas, en la reunión semanal de la gerencia.

**Por qué.** La gerencia hoy recibe reportes armados a mano al cierre del mes (problemas 5 y 7). Los datos de demostración muestran la estacionalidad (helados en verano, panetón en Navidad), que es la base para producir con anticipación.

**Cómo.** Adoptar los KPI de [3.7](03_aspectos_generales.md) como punto de partida y ajustar sus metas con datos reales: las actuales son supuestos (por ejemplo, +10 % de ventas, menos del 2 % de stock vencido o por vencer, 95 % de pedidos a tiempo).

**Limitación.** El rendimiento queda por debajo de la meta de 80 en el backend (59) y en el tablero (76; 39 en móvil), un **límite conocido** del JavaScript de Odoo; la carga del tablero sí cumple los 3 s (LCP de 2,11 s). Se recomienda usarlo en un equipo con memoria suficiente y navegador actualizado hasta que se mida en el servidor real, y revisar el tablero con los dispositivos de la gerencia.

### 6. Corregir el vencimiento en el despacho del punto de venta (FEFO)

**Qué.** En el punto de venta el cajero escribe el lote y Odoo estándar no comprueba su fecha de vencimiento ni propone el que vence antes: una venta de mostrador puede salir con un lote vencido (RNF005). Desde M1, el PdV sí bloquea un lote **rechazado por calidad**.

**Por qué.** Es el único hueco del control FEFO que el proyecto detectó y es el más barato de cerrar: una restricción sobre el detalle del movimiento, con su prueba.

**Mientras tanto.** Instruir al cajero para que elija el lote que **vence primero** y revisar el reporte de stock por vencer a 30 días cada semana.

### 7. Mantener la continuidad y la seguridad que el proyecto dejó probadas

**Qué.** Operar con lo que ya está medido: réplica en caliente, respaldo diario con retención de 7 días (restauración probada en 31 s), Nginx con TLS, verificación en dos pasos para administración y gerencia, contraseñas de 12 o más y auditoría de cambios en precios, pedidos y compras.

**Por qué.** El negocio es estacional y no puede perder sus datos en temporada alta. Todo esto está probado en una PC, no en el servidor real.

**Cómo.** Repetir la prueba de restauración en el servidor definitivo, guardar una copia **fuera** del servidor y medir la disponibilidad en el tiempo (RNF011 no se midió; la meta es 99 %).

### 8. Preparar el sistema para el escenario Froneri

**Qué.** Si el negocio de helados cambia de dueño, el ERP debe poder seguir con chocolates y panetón.

**Por qué.** El diseño separa líneas de producto y canales, y las listas de precios por temporada; no se modeló la transición porque no está confirmada para Perú (supuesto S1).

**Cómo.** Mantener las líneas separadas en los datos reales (categorías y equipos de venta) y no mezclar costos entre líneas; así se puede separar o conservar cada una sin rehacer el sistema.

## 8.1.3 Hoja de ruta sugerida

| Etapa | Qué hacer | Recomendaciones |
|---|---|---|
| **Corto plazo** (primeras semanas) | Cargar datos reales por áreas, capacitar y medir la usabilidad con usuarios reales; decidir cómo se envían los comprobantes a SUNAT; corregir el vencimiento en el punto de venta | 1, 4, 6 |
| **Mediano plazo** | Adoptar la liquidación, la calidad y la cadena de frío en la operación; ajustar las metas de los KPI del tablero; app móvil y sensores | 2, 3, 5 |
| **Continuo** | Respaldos probados, seguridad y observación del escenario Froneri | 7, 8 |

## 8.1.4 Lo que este proyecto no permite afirmar

- **No hay costos ni retorno de la inversión.** No se estimaron costos de implantación, capacitación ni de soporte; la única cifra de costo es la licencia, que es cero porque se usa Odoo Community.
- **No hay datos reales de D'Onofrio.** Los problemas son supuestos del caso (S7); las metas de los KPI también.
- **Las mediciones salen de una PC.** Los resultados de carga, seguridad y rendimiento no sustituyen una prueba en el servidor definitivo.
- **La Fase 2 se construyó, pero se probó con datos de demostración.** Las recomendaciones 2, 3 y 5 se apoyan en módulos con 81 pruebas automáticas y capturas, no en una operación real; la usabilidad se evaluó solo con el equipo.
