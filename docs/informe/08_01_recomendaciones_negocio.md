# 8.1 Recomendaciones de negocio

Son recomendaciones para una empresa como D'Onofrio a partir de lo que el proyecto probó; los datos de la empresa son ficticios y las mediciones salen de una sola PC. Con la Fase 2 completa, varias pasan de «construir» a «adoptar, medir y ampliar» lo ya construido.

**Tabla 8.1. Recomendaciones de negocio y gestión**

| # | Recomendación | Problema (1.2.3) | Plazo |
|---|---|---|---|
| 1 | Poner en marcha el sistema con datos reales y capacitación por rol | Los 7 | Corto |
| 2 | Adoptar la liquidación diaria de los heladeros y evaluar una app móvil | 1 | Corto a mediano |
| 3 | Operar la calidad y la cadena de frío ligadas al lote y conectar sensores | 3 y 4 | Mediano |
| 4 | Resolver la facturación electrónica con SUNAT | RF016 | Corto |
| 5 | Medir con el tablero gerencial y ajustar las metas de los KPI | 5 y 7 | Continuo |
| 6 | Mantener la continuidad y la seguridad probadas | RNF006 y RNF009 | Continuo |

**1. Datos reales y capacitación.** Pasar de los datos ficticios a los reales por áreas (almacenes y productos, clientes y precios, proveedores e insumos, empleados) y capacitar a cada rol con los casos de uso de 2.2.1.3. El ciclo vender-comprar-producir-facturar ya funciona de punta a punta, por lo que el reemplazo es de contenido y no de programación. Conviene observar a los usuarios reales para afinar las pantallas.

**2. Liquidación de heladeros.** M2 calcula lo vendido, el importe, la comisión y la diferencia de efectivo, y emite el PDF para firmar: es el proceso más reconocible de D'Onofrio y el que concentra el problema 1. Con los datos de demostración, 124 de 127 liquidaciones están liquidadas y la merma es de 0,27 % de lo despachado. Siguientes pasos: una aplicación móvil para el heladero y una merma que descuente inventario. Indicador: descuadre por heladero menor al 2 % de lo despachado (meta supuesta).

**3. Calidad y cadena de frío.** Con M1 y M3 el lote rechazado se bloquea, el certificado sale en PDF y la temperatura fuera de rango genera una alerta, lo que respalda ISO 9001 y HACCP como buenas prácticas de referencia, sin certificar nada. El siguiente paso es conectar sensores que registren la temperatura.

**4. Facturación electrónica.** El ERP emite factura (01) y boleta (03) con IGV 18 %. Para el envío electrónico a SUNAT, Finanzas y TI deben elegir un proveedor de servicios electrónicos autorizado (OSE).

**5. Tablero gerencial.** Usar el tablero de M4 y los dashboards estándar en la reunión semanal de la gerencia y ajustar con datos reales las metas de los KPI, que hoy son supuestos. El tablero carga en 2.11 s.

**6. Continuidad y seguridad.** Operar con lo medido (réplica en caliente, respaldo diario con restauración en 31 s, Nginx con TLS, segundo factor, contraseñas de 12 o más y auditoría), repetir la restauración en el servidor definitivo, guardar una copia fuera de él y medir la disponibilidad en el tiempo.
