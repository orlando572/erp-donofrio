# 3.1.4.5 Módulo del Tablero gerencial (M4)

Gerencia ya tenía en la Fase 1 los dashboards estándar de Community, de solo lectura. El Tablero gerencial (`donofrio_tablero`, M4; HU-22 y HU-24; RF013; CU009) agrega un tablero hecho para D'Onofrio y la marca visual. Se publicó en la versión v1.4.0 y no crea tablas: solo calcula a partir de los datos que ya existen.

Qué hace. El tablero (menú Tablero › Gerencia) es una pantalla con hasta seis tarjetas de indicadores (KPI), un gráfico de ventas de los últimos seis meses, una tabla de ventas del mes por canal y un filtro por almacén. La marca (HU-24) pone la barra superior en el amarillo de los carritos de D'Onofrio, con texto oscuro, usa un dorado oscuro como color principal (legible sobre blanco) en todo el sistema y en el inicio de sesión, y agrega el ícono del helado en la pestaña del navegador.

| Tarjeta | Qué cuenta |
|---|---|
| Ventas del mes | Pedidos confirmados del mes con IGV, variación contra el mes anterior y desglose por canal |
| Cumplimiento de producción | Órdenes del mes hechas entre las confirmadas, en curso y por cerrar |
| Stock por vencer (30 d) | Lotes con existencias que vencen en 30 días, a costo estándar, y lotes ya vencidos |
| Lotes aprobados (M1), liquidaciones pendientes (M2) y alertas de temperatura (M3) | Inspecciones aprobadas entre aprobadas y rechazadas; liquidaciones que no están en «Liquidado»; lecturas fuera de rango de los últimos 7 días |

Las tres últimas tarjetas solo salen si el módulo correspondiente está instalado y el usuario tiene permiso para verlo, por lo que el tablero solo necesita la configuración base y Ventas, Inventario y Fabricación de Odoo. El cálculo de los indicadores agrupa los datos en la base y respeta los permisos de quien abre el tablero: si el usuario no puede ver pedidos, existencias, lotes u órdenes, el tablero muestra un aviso amarillo «sin permiso» en lugar de un error. El Gerente General ve el tablero completo; el Jefe de Ventas y el Vendedor reciben el aviso de que falta acceso a Inventario.

![Tablero gerencial con las seis tarjetas, el gráfico y la barra amarilla de la marca](../capturas/sprint-4/HU-22_tablero_todos_los_almacenes.png)

*Figura 5.5e-a. Tablero del Gerente General: ventas de noviembre de S/ 2,844,413.33, igual a la suma de los pedidos confirmados.*

Pruebas. El módulo tiene 21 pruebas sin errores: estructura de los indicadores, ventas contra un pedido real, filtro de almacén, producciones, stock por vencer, tarjetas opcionales con y sin su módulo, aviso de «sin permiso» y carga en menos de 3 s (el cálculo de los indicadores tardó entre 30 y 57 ms). En la pantalla se verificaron el tablero completo, el filtro, el aviso para el vendedor, una ventana de 375 × 812 sin desplazamiento horizontal y el inicio de sesión con la marca. El tablero termina de cargar en 2.11 s.
