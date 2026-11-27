# 7. Conclusiones

## 7.1 Conclusión general

El proyecto cumple su meta principal: un ERP sobre Odoo 19 Community y PostgreSQL 16, sin licencias Enterprise, donde cada lote se puede seguir desde el insumo hasta el cliente, la calidad y la temperatura dejan rastro ligado al lote, el heladero liquida con un documento firmable y la gerencia ve datos consolidados. El núcleo (módulo de configuración base) se entregó configurado por código y los cuatro módulos desarrollados para D'Onofrio (calidad, liquidación de heladeros, cadena de frío y tablero) se construyeron uno a uno. En cifras: 115 puntos de historias de usuario completados, 224 pruebas automáticas en verde, 82 PR fusionados, cinco versiones (v1.0.0 a v1.4.0), un despliegue protegido y respaldado, y una restauración de 31 s.

## 7.2 Una conclusión por problema del caso

| # | Problema (1.2.3) | Conclusión |
|---|---|---|
| 1 | Liquidación de heladeros manual | Resuelto con M2: calcula lo vendido, la comisión y la diferencia de efectivo, crea el pedido y se imprime con firmas |
| 2 | Lotes sin control de vencimiento ni FEFO | Resuelto: lotes con vencimiento, salida por FEFO y alerta 30 días antes |
| 3 | Temperaturas a mano | Resuelto con M3: rango por cámara y actividad ante una lectura fuera de rango |
| 4 | Calidad sin ligar al lote | Resuelto con M1: inspección ligada a la orden y al lote, certificado en PDF y bloqueo del lote rechazado |
| 5 | Planificación sin datos consolidados | Resuelto: dashboards y tablero de M4 |
| 6 | Cada área digita por separado | Resuelto: un solo ERP probado de punta a punta |
| 7 | Gerencia sin reportes a tiempo | Resuelto: el tablero carga en 2.11 s |

Los siete problemas se resuelven: cuatro con la Fase 1 (2, 5, 6 y 7) y tres con los módulos de la Fase 2 (1, 3 y 4). Resuelto significa que el sistema lo cubre y se verificó con pruebas.

## 7.3 Una conclusión por área

Marketing y ventas: el embudo CRM, las listas de precios por canal, el punto de venta con boleta, la facturación con IGV y la liquidación del heladero cubren el flujo de venta. Logística y producción: lotes con vencimiento, FEFO, despacho en dos pasos, reposición a Arequipa y órdenes de producción con costo y, con M1, inspección del lote. Gerencia: dashboards, vistas guardadas y el tablero de M4. Compras, RR. HH. y TI: reabastecimiento mín./máx., usuarios por rol y mesa de servicios con SLA. Infraestructura y seguridad: réplica, respaldos, Nginx con TLS, segundo factor y auditoría, verificados.

## 7.4 Una conclusión por requerimiento no funcional

Los 13 requerimientos no funcionales tienen su métrica, su prueba y su evidencia (anexo 10.2): rendimiento (p95 de 11.6 ms con 20 usuarios y 0 % de errores), continuidad (restauración en 31 s y réplica con retraso de 2.3 ms), trazabilidad de los lotes, mantenibilidad (224 pruebas automáticas), seguridad (10 roles, TLS, 2FA y 0 alertas altas en ZAP), auditoría de precios, pedidos y compras, y un entorno que se levanta con un comando.


## 7.5 Conclusión sobre la gestión del proyecto

Scrum y la revisión cruzada funcionaron: cada cambio entró por un PR aprobado por el otro integrante y con el CI en verde, y la velocidad fue de 24, 30, 27 y 34 puntos. El plazo único obligó a sprints de un día: el núcleo se completó en unas 21 horas y la Fase 2 entre el 24 y el 25/11, gracias al orden fijo M1 → M4. Los cuatro módulos desarrollados para D'Onofrio se completaron en el orden previsto. De Odoo 19 se aprendió que muchas necesidades se resuelven mejor con la configuración estándar que con código nuevo; los módulos desarrollados para D'Onofrio se limitaron a lo que Community no trae.

Las líneas de mejora para una puesta en producción se detallan en la sección 8.
