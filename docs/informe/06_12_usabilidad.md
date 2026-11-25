# 6.12 Pruebas de usabilidad

La usabilidad (RNF003: interfaz en español y tareas clave en tres pasos o menos) se evaluó con tres técnicas aplicadas por el equipo sobre el sistema con los datos de demostración: una revisión pantalla por pantalla por roles del 25/11/2026 (administrador, inspector de calidad, vendedor y gerente), una nota de accesibilidad sobre el contraste de color (WCAG 2.1, calculado en 4.6.1) y una evaluación heurística de M1 a M4 con las 10 heurísticas de Nielsen (Nielsen, 1994).

## Revisión por roles

La revisión por roles encontró cuatro tipos de problemas, todos corregidos: el administrador recibía un error 403 al imprimir el certificado de calidad y tenía textos en inglés (contacto, empleado, diario «Punto de venta»); y varios roles veían fechas y plazos de tickets fuera de la ventana de datos de demostración (3/8 al 22/11/2026). El vendedor, sin acceso a Inventario, recibe en el tablero un aviso claro que dice qué falta y a quién pedirlo.

## Accesibilidad

Los pares de texto y fondo de las pantallas cumplen el contraste mínimo de 4.5 de WCAG 2.1. El amarillo de marca no se usa como color de texto (contraste 1.61) y los colores de alerta van siempre acompañados de un texto, como «Cumple» y «No cumple» en la inspección.

## Evaluación heurística de M1 a M4

| Heurística de Nielsen | Qué se observa en las pantallas |
|---|---|
| Visibilidad del estado | Barra de estado en inspección y liquidación; sello «Fuera de rango» en la lectura |
| Mundo real | Términos del negocio e importes en soles |
| Control y libertad | «Volver a borrador» en la liquidación despachada |
| Consistencia | Barra superior amarilla de la marca en todas las aplicaciones y patrones estándar de Odoo |
| Prevención de errores | Un punto sin medir no deja aprobar, rechazar exige motivo y un lote rechazado no se despacha |
| Reconocer, no recordar | Insignia de estado, filtro «Por medir» y datos del heladero visibles |
| Flexibilidad | Selector de almacén en el tablero y botón «Imprimir» |
| Diseño minimalista | Seis tarjetas, un gráfico mensual y una tabla por canal |
| Recuperarse de errores | El aviso «Sin permiso» dice qué acceso falta y a quién pedirlo |
| Ayuda | Ayuda emergente en campos clave y manuales por caso de uso |

**Alcance.** La revisión y la evaluación las hizo el propio equipo con datos de demostración, no usuarios finales de D'Onofrio; no se afirma una medición con tiempos por tarea. Quedan anotadas dos mejoras de bajo costo: traducir el mensaje automático del historial de la liquidación y explicar en el manual por qué las inspecciones pendientes aparecen sin inspector hasta iniciar la medición.
