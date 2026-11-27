# 1. Resumen

## Resumen

Este trabajo presenta un sistema de planificación de recursos empresariales (ERP) académico para **D'Onofrio**, una unidad ficticia de helados, chocolates y panetón con un negocio estacional, una amplia red de heladeros ambulantes y productos perecibles. Los datos de la empresa son inventados. El caso parte de cuatro problemas: liquidación de heladeros en papel, lotes que vencen sin aviso, calidad y frío sin rastro ligado al lote, y decisiones tardías sin datos consolidados.

La solución es un ERP web sobre **Odoo 19 Community y PostgreSQL 16**, en Docker y sin licencias Enterprise. Se desarrolló con **Scrum** en dos fases. La primera configura Odoo estándar por código en el módulo de configuración base: ventas, logística con lotes y salida por vencimiento (FEFO), producción, compras, facturación, recursos humanos y mesa de servicios, con réplica de PostgreSQL, respaldos y un despliegue protegido con Nginx y conexión cifrada (TLS). La segunda agrega cuatro módulos desarrollados para D'Onofrio: inspección de calidad con certificado (módulo de Calidad), liquidación diaria de heladeros (módulo de Liquidación de heladeros), cadena de frío con alertas de temperatura y un tablero gerencial en OWL (módulo del Tablero gerencial).

Se completaron **115 puntos** de historias de usuario en cuatro sprints, las versiones v1.0.0 a v1.4.0 están publicadas y las **218 pruebas automáticas** pasan en la integración continua. Restaurar un respaldo tardó 31 segundos (meta: 2 horas); con 20 usuarios virtuales, el percentil 95 fue de 11.6 ms en listas, sin errores; no hubo alertas de seguridad altas; el rendimiento web del panel de ventas subió de 45 a 80 puntos y el tablero gerencial carga en 2.11 s. Las mediciones provienen de una sola máquina con datos de demostración.

**Palabras clave:** Odoo 19; ERP; PostgreSQL; Scrum; Docker.
