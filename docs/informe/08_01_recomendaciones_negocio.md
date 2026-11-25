# 8.1 Recomendaciones de negocio

Son recomendaciones para una empresa como D'Onofrio a partir de lo que el proyecto probó; los datos de la empresa son ficticios y las mediciones salen de una sola PC. Con la Fase 2 completa, varias pasan de «construir» a «adoptar, medir y ampliar» lo ya construido.

| # | Recomendación | Problema (3.2.4) | Plazo |
|---|---|---|---|
| 1 | Poner en marcha el sistema con datos reales y capacitación por rol | Los 7 | Corto |
| 2 | Adoptar la liquidación diaria de los heladeros y evaluar una app móvil | 1 | Corto a mediano |
| 3 | Operar la calidad y la cadena de frío ligadas al lote y conectar sensores | 3 y 4 | Mediano |
| 4 | Resolver la facturación electrónica con SUNAT | Límite de RF016 | Corto |
| 5 | Medir con el tablero gerencial y ajustar las metas de los KPI | 5 y 7 | Continuo |
| 6 | Corregir el vencimiento en el despacho del punto de venta | 2 | Corto |
| 7 | Mantener la continuidad y la seguridad probadas | RNF006 y RNF009 | Continuo |

**1. Datos reales y capacitación.** Pasar de los datos ficticios a los reales por áreas (almacenes y productos, clientes y precios, proveedores e insumos, empleados) y capacitar a cada rol con los casos de uso de 4.2.4. El ciclo vender-comprar-producir-facturar ya funciona de punta a punta, por lo que el reemplazo es de contenido y no de programación. Conviene observar a usuarios reales, porque la usabilidad solo se evaluó con el equipo (6.12).

**2. Liquidación de heladeros.** M2 calcula lo vendido, el importe, la comisión y la diferencia de efectivo, y emite el PDF para firmar: es el proceso más reconocible de D'Onofrio y el que concentra el problema 1. Con los datos de demostración, 124 de 127 liquidaciones están liquidadas y la merma es de 0,27 % de lo despachado. Siguientes pasos: una aplicación móvil para el heladero y una merma que descuente inventario. Indicador: descuadre por heladero menor al 2 % de lo despachado (meta supuesta).

**3. Calidad y cadena de frío.** Con M1 y M3 el lote rechazado se bloquea, el certificado sale en PDF y la temperatura fuera de rango genera una alerta, lo que respalda ISO 9001 y HACCP como buenas prácticas de referencia, sin certificar nada. Faltan sensores que registren la temperatura y una alerta por lecturas que faltan.

**4. Facturación electrónica.** El ERP emite factura (01) y boleta (03) con IGV 18 %, pero no las envía a SUNAT porque `l10n_pe_edi` es Enterprise. Finanzas y TI deben decidir entre un proveedor de servicios electrónicos autorizado o mantener el sistema actual para el envío; el costo no se estimó.

**5. Tablero gerencial.** Usar el tablero de M4 y los dashboards estándar en la reunión semanal de la gerencia y ajustar con datos reales las metas de los KPI, que hoy son supuestos. El tablero carga en 2.11 s, aunque su Lighthouse (76) queda bajo la meta de 80, un límite conocido del JavaScript de Odoo.

**6. Vencimiento en el punto de venta.** El cajero escribe el lote y Odoo estándar no comprueba su vencimiento; desde M1 solo se bloquea un lote rechazado. Una restricción sobre el detalle del movimiento, con su prueba, cierra el único hueco del control FEFO detectado. Mientras tanto, el cajero debe elegir el lote que vence primero.

**7. Continuidad y seguridad.** Operar con lo medido (réplica en caliente, respaldo diario con restauración en 31 s, Nginx con TLS, segundo factor, contraseñas de 12 o más y auditoría), repetir la restauración en el servidor definitivo, guardar una copia fuera de él y medir la disponibilidad en el tiempo.

**Lo que el proyecto no permite afirmar.** No hay costos ni retorno de la inversión (la única cifra es la licencia, cero con Odoo Community), ni datos reales de D'Onofrio: los problemas y las metas son supuestos del caso. Las mediciones salen de una PC y la Fase 2 se probó con datos de demostración y 81 pruebas automáticas, no con una operación real.
