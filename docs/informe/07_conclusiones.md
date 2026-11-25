# 7. Conclusiones

Las conclusiones son las del proyecto con la Fase 2 completa (módulos M1 a M4 en `main`, releases `v1.1.0` a `v1.4.0`). Los datos de D'Onofrio son ficticios y las mediciones salen de una sola PC.

## 7.1 Conclusión general

El proyecto cumple su meta principal: un ERP sobre Odoo 19 Community y PostgreSQL 16, sin licencias Enterprise, donde cada lote se puede seguir desde el insumo hasta el cliente, la calidad y la temperatura dejan rastro ligado al lote, el heladero liquida con un documento firmable y la gerencia ve datos consolidados. El núcleo (`donofrio_base`) se entregó configurado por código y los cuatro módulos propios (calidad, liquidación de heladeros, cadena de frío y tablero) se construyeron uno a uno. En cifras: 115 de 121 puntos de historias de usuario, 218 pruebas automáticas en verde en el CI, 82 PR fusionados, cinco releases (`v1.0.0` a `v1.4.0`), un despliegue protegido y respaldado, y una restauración de 31 s. Lo que no alcanza la meta es el rendimiento web del backend y del tablero (límite conocido).

## 7.2 Una conclusión por problema del caso

| # | Problema (3.2.4) | Conclusión |
|---|---|---|
| 1 | Liquidación de heladeros manual | Resuelto con M2: calcula lo vendido, la comisión y la diferencia de efectivo, crea el pedido y se imprime con firmas |
| 2 | Lotes sin control de vencimiento ni FEFO | Resuelto: lotes con vencimiento, salida por FEFO y alerta 30 días antes |
| 3 | Temperaturas a mano | Resuelto con M3: rango por cámara y actividad ante una lectura fuera de rango (lecturas manuales, sin sensores) |
| 4 | Calidad sin ligar al lote | Resuelto con M1: inspección ligada a la orden y al lote, certificado en PDF y bloqueo del lote rechazado |
| 5 | Planificación sin datos consolidados | Resuelto: dashboards y tablero de M4 |
| 6 | Cada área digita por separado | Resuelto: un solo ERP probado de punta a punta |
| 7 | Gerencia sin reportes a tiempo | Resuelto: el tablero carga en 2.11 s |

Los siete problemas se resuelven: cuatro con la Fase 1 (2, 5, 6 y 7) y tres con los módulos de la Fase 2 (1, 3 y 4). Resuelto significa que el sistema lo cubre con datos de demostración; no se probó con usuarios ni datos reales.

## 7.3 Una conclusión por área

**Marketing y ventas:** el embudo CRM, las listas de precios por canal, el punto de venta con boleta, la facturación con IGV y la liquidación del heladero cubren el flujo de venta (sin envío electrónico a SUNAT, que es Enterprise). **Logística y producción:** lotes con vencimiento, FEFO, despacho en dos pasos, reposición a Arequipa y órdenes de producción con costo y, con M1, inspección del lote. **Gerencia:** dashboards, vistas guardadas y el tablero de M4. **Compras, RR. HH. y TI:** reabastecimiento mín./máx., usuarios por rol y mesa de servicios con SLA. **Infraestructura y seguridad:** réplica, respaldos, Nginx con TLS, segundo factor y auditoría, verificados.

## 7.4 Una conclusión por requerimiento no funcional

De los 13 requerimientos no funcionales, 6 cumplen (rendimiento, trazabilidad, continuidad, mantenibilidad, auditoría y reproducibilidad), 3 cumplen con límites (usabilidad, lote vencido o rechazado y seguridad) y 4 son parciales (portabilidad, rendimiento web, disponibilidad y datos personales).


## 7.5 Conclusión sobre la gestión del proyecto

Scrum y la revisión cruzada funcionaron: cada cambio entró por un PR aprobado por el otro integrante y con el CI en verde (79 de 82 PR con la aprobación vigente), y la velocidad fue de 24, 30, 27 y 34 puntos. El plazo único obligó a sprints de un día: el núcleo se completó en unas 21 horas y la Fase 2 entre el 24 y el 25/11, gracias al orden fijo M1 → M4. Ningún módulo quedó a medias; lo que quedó fuera es la página de aterrizaje opcional (HU-31). De Odoo 19 se aprendió que muchas necesidades se resuelven mejor con la configuración estándar que con código propio; los módulos propios se limitaron a lo que Community no trae.

Como trabajo futuro quedan la medición de la disponibilidad en el tiempo, la revisión de la portabilidad en más navegadores, y lo que se recomienda en la sección 8: sensores de temperatura, aplicación móvil para el heladero, envío electrónico a SUNAT, `auditlog` en los módulos nuevos y pruebas de JavaScript.
