# 6.12 Pruebas de usabilidad

La usabilidad (RNF003: interfaz en español y tareas clave en tres pasos o menos) se evaluó con tres técnicas aplicadas por el equipo sobre el sistema con los datos de demostración: una revisión pantalla por pantalla por roles del 25/11/2026 (administrador, inspector de calidad, vendedor y gerente), una nota de accesibilidad sobre el contraste de color (WCAG 2.1, calculado en 4.6.1) y una evaluación heurística de M1 a M4 con las 10 heurísticas de Nielsen (Nielsen, 1994).

## Revisión por roles

La revisión encontró cuatro tipos de problemas, todos corregidos:

| Rol | Hallazgo | Corrección |
|---|---|---|
| Administrador | Error 403 al imprimir el certificado de calidad | Entra a los grupos de jefatura de calidad y de heladeros, con pruebas de esa pertenencia |
| Administrador | Textos en inglés: nombre del contacto y del empleado, diario «Punto de venta» y referencias de asientos | Pasados a español |
| Vendedor, inspector y gerente | Fechas fuera de la ventana de datos de demostración (3/8 al 22/11/2026) | Llevadas a la ventana; listas y filtros muestran datos coherentes |
| Todos | Plazos de los tickets de la mesa de servicios fuera de la ventana | Corregidos dentro de la ventana |

El vendedor, que no tiene acceso a Inventario, recibe en el tablero un aviso claro que dice qué falta y a quién pedirlo, y no una pantalla en blanco.

## Accesibilidad

Los pares de texto y fondo de las pantallas cumplen el contraste mínimo de 4.5 de WCAG 2.1. El amarillo de marca no se usa como color de texto (contraste 1.61) y los colores de alerta van siempre acompañados de un texto, como «Cumple» y «No cumple» en la inspección.

## Evaluación heurística de M1 a M4

| Heurística de Nielsen | Qué se observa en las pantallas |
|---|---|
| Visibilidad del estado | La inspección muestra su barra de estado y el resultado de cada punto; la lectura fuera de rango lleva el sello «Fuera de rango»; la liquidación muestra Borrador, Despachado y Liquidado |
| Mundo real | Términos del negocio (heladero, liquidador, lote, cámara de frío, punto de control) e importes en soles |
| Control y libertad | La liquidación despachada ofrece «Volver a borrador»; las actividades se pueden marcar como hechas, editar o cancelar |
| Consistencia | Barra superior amarilla de la marca en todas las aplicaciones y patrones estándar de Odoo |
| Prevención de errores | Un punto sin medir no deja aprobar, rechazar exige un motivo y un lote rechazado no se despacha |
| Reconocer, no recordar | Estado de cada inspección en una insignia, filtro «Por medir» y heladero, lista de precios y pedido visibles en la liquidación |
| Flexibilidad | Selector de almacén en el tablero, botón «Imprimir» en la liquidación y filtros estándar |
| Diseño minimalista | Seis tarjetas, un gráfico mensual y una tabla por canal; en 375 px las tarjetas pasan a una columna |
| Recuperarse de errores | El aviso «Sin permiso» dice qué acceso falta y a quién pedirlo |
| Ayuda | Ayuda emergente en «Comisión (%)» y «Diferencia de efectivo» y manuales por caso de uso |

**Alcance.** La revisión y la evaluación las hizo el propio equipo con datos de demostración, no usuarios finales de D'Onofrio, y las capturas son de un navegador de escritorio y de una ventana de 375 × 812 (5.5e). El criterio de RNF003 queda respaldado por estas técnicas y por la interfaz en español (`es_PE`); no se afirma una medición con tiempos por tarea. Dos mejoras de bajo costo quedan anotadas: traducir el mensaje automático del historial de la liquidación y explicar en el manual por qué las inspecciones pendientes aparecen sin inspector hasta iniciar la medición.
