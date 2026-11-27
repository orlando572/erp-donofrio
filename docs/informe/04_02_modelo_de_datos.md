# 4.2.5 a 4.2.8 Modelo de datos: clases, ER, diseño lógico y diccionario

El modelo de datos cubre el núcleo (Odoo 19.0 Community con el módulo de configuración base) y los cuatro módulos de la Fase 2. Las clases salen del código de los módulos; el modelo entidad–relación, el diseño lógico y el diccionario se extraen de una **base de datos real** con los módulos instalados, no de un dibujo a mano.

## 2.2.1.4 Diagrama de clases

El dominio de D'Onofrio se apoya en los modelos estándar de Odoo: cada modelo es una clase de Python con sus campos y métodos y una tabla en PostgreSQL. La figura muestra los 31 modelos que intervienen en los procesos del núcleo (venta B2B y PdV, inventario con lotes y FEFO, producción, compras, facturación con IGV, seguridad y mesa de servicios) con sus relaciones reales. El módulo de configuración base **no crea tipos de datos nuevos**: amplía cuatro de Odoo (el pedido de venta, para elegir factura o boleta según el cliente; el usuario, para el segundo factor de autenticación; las reglas de auditoría; y la tarea, que gana el campo «Cumplimiento del SLA», que indica si se respetó el plazo del acuerdo de nivel de servicio); lo demás son datos cargados.

![Diagrama de clases del núcleo](../diagramas/clases/clases_nucleo.png)

*Figura 4.11. Clases del núcleo (Fase 1). Naranja: modelo estándar que el módulo de configuración base extiende; verde: datos que no son modelos.*

Las clases de los módulos de D'Onofrio se muestran con los nombres y atributos reales del código, en amarillo, ligadas a los modelos de Odoo que usan o extienden.

![Clases de la Fase 2](../diagramas/clases/clases_fase2.png)

*Figura 4.12. Clases de la Fase 2 (M1 a M4) y su relación con el núcleo.*

Las clases desarrolladas para D'Onofrio son el punto de control, la inspección y su línea de medición (Calidad, M1, ligadas a la orden de producción y al lote), la lectura de temperatura con el rango de cada cámara (cadena de frío, M3), la liquidación del heladero y su línea (M2, que al liquidar crea un pedido de venta) y el cálculo de los indicadores del Tablero gerencial (M4), que no guarda datos propios.

## 2.2.1.5 Diseño de base de datos

## 2.2.1.5.1 Modelo entidad–relación

El modelo entidad–relación (ER) se extrajo de una base limpia de PostgreSQL 16 con 703 tablas de Odoo: un script lee del catálogo de la base las columnas, las claves primarias (PK) y foráneas (FK) y la cardinalidad de cada relación. De las 703 tablas se filtraron las **42 centrales**: 36 del núcleo (ventas, inventario con lotes, producción, compras, facturación, maestros y seguridad), 3 de calidad (M1), 2 de heladeros (M2) y 1 de cadena de frío (M3); M4 no crea tablas.

![Modelo ER de las tablas centrales](../diagramas/er/er_nucleo.png)

*Figura 4.13. Modelo ER de las 42 tablas centrales (pata de gallo, color por área).*

Las relaciones son de uno a muchos; las de muchos a muchos pasan por tablas intermedias que no se dibujan, y las que apuntan a usuarios, ubicaciones, tipos de operación y diarios contables se anotan en cada caja sin línea, para no saturar el diagrama. Las tablas con más datos son las líneas de asientos contables (17 852 filas), las líneas de movimientos de inventario (6 535) y los movimientos de inventario (6 063).

## 2.2.1.5.2 Diseño lógico

El diseño lógico muestra, para las tablas centrales del negocio, el tipo de dato, las PK y FK y las cardinalidades; sale del mismo extractor, por lo que coincide con la base real. Se presenta el flujo de inventario y lotes, base de la trazabilidad y del FEFO.

El flujo va de la transferencia (`stock_picking`) a sus movimientos (`stock_move`) y al detalle por lote (`stock_move_line`), con las existencias en `stock_quant`. El detalle registra el lote que entró o salió, las existencias guardan la cantidad por producto, ubicación y lote, y el lote (`stock_lot`) guarda las fechas de vencimiento, retiro y alerta: con la fecha de retiro Odoo despacha primero lo que vence antes (FEFO) y con el vencimiento avisa 30 días antes. El pedido se une a su entrega y a su factura, y la orden de producción consume insumos y produce el lote mediante movimientos, de modo que cada lote queda ligado a sus insumos.

**Por qué no se escribe SQL a mano.** Las tablas las crea Odoo a partir de las clases (su ORM, la capa que traduce las clases a tablas), así que siempre coinciden con el código instalado. Las reglas de negocio (FEFO, costo FIFO, IGV), los permisos y la auditoría se aplican en esa capa, y una inserción directa en la base las saltaría. Por eso los datos se cargan siempre a través de Odoo, y el SQL del proyecto se limita a consultas de lectura para documentar y medir.

## 2.2.1.5.3 Diccionario de datos

El diccionario de la plantilla (una tabla por entidad con clave, campo, tipo, tamaño, nulidad y descripción) se genera con una herramienta del proyecto a partir del catálogo de la base y de la descripción de los campos en Odoo. Aquí se presentan solo los **modelos desarrollados para D'Onofrio** (calidad, heladeros y cadena de frío); el diccionario completo de las 42 tablas centrales y del resto del esquema de Odoo se obtiene con esa misma herramienta y se entrega como archivo aparte.

El módulo de configuración base no crea tablas: agrega la columna «Cumplimiento del SLA» a las tareas y carga como datos la compañía, 2 almacenes, 47 productos, 12 listas de materiales, 5 listas de precios, 10 usuarios, 21 empleados y las reglas de seguridad y auditoría.
