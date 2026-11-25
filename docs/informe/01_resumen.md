# 1. Resumen

## Resumen

Este trabajo presenta un sistema de planificación de recursos empresariales (ERP) académico para **D'Onofrio**, una unidad ficticia de helados, chocolates y panetón con un negocio estacional, una amplia red de heladeros ambulantes y productos perecibles. Los datos de la empresa son inventados. El caso parte de cuatro problemas: la liquidación diaria de los heladeros se hace en papel o Excel, los lotes vencen sin que nadie los vea a tiempo, la calidad y el frío no dejan rastro ligado al lote, y la gerencia decide tarde y sin datos consolidados.

La solución es un ERP web sobre **Odoo 19 Community y PostgreSQL 16**, en Docker y sin licencias Enterprise. Se desarrolló con **Scrum** en dos fases. La primera configura Odoo estándar por código en el módulo `donofrio_base`: ventas, logística con lotes y salida por vencimiento (FEFO), producción, gerencia, compras, facturación, recursos humanos y mesa de servicios, con réplica de PostgreSQL, respaldos y un despliegue protegido con Nginx y TLS. La segunda agrega cuatro módulos propios: inspección de calidad con certificado (`donofrio_calidad`), liquidación diaria de heladeros (`donofrio_heladeros`), cadena de frío con alertas de temperatura y un tablero gerencial en OWL (`donofrio_tablero`).

Se completaron **115 de los 121 puntos** de historias de usuario (95 %), las versiones `v1.0.0` a `v1.4.0` están publicadas y las **218 pruebas automáticas** pasan en la integración continua. Restaurar un respaldo tardó 31 segundos (meta: 2 horas); con 20 usuarios virtuales, el percentil 95 fue de 11.6 ms en listas; no hubo alertas de seguridad altas; y el rendimiento web del panel de ventas subió de 45 a 80 puntos. El backend (59) y el tablero propio (76) quedan bajo la meta de 80, un límite que explica el JavaScript de Odoo. Las mediciones provienen de una sola máquina con datos de demostración.

**Palabras clave:** Odoo 19; ERP; PostgreSQL; Scrum; Docker.
