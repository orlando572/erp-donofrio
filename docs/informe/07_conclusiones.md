# 7. Conclusiones

Las conclusiones son las del proyecto con la Fase 2 completa (módulos M1 a M4 en `main`, releases `v1.1.0` a `v1.4.0`). Los datos de D'Onofrio son ficticios y las mediciones salen de una sola PC.

## 7.1 Conclusión general

El proyecto cumple su meta principal: un ERP sobre Odoo 19 Community y PostgreSQL 16, sin licencias Enterprise, donde cada lote se puede seguir desde el insumo hasta el cliente, la calidad y la temperatura dejan rastro ligado al lote, el heladero liquida con un documento firmable y la gerencia ve datos consolidados. El núcleo (`donofrio_base`) se entregó configurado por código y los cuatro módulos propios (calidad, liquidación de heladeros, cadena de frío y tablero) se construyeron uno a uno. En cifras: 115 de 121 puntos de historias de usuario, 218 pruebas automáticas en verde en el CI, 82 PR fusionados, cinco releases (`v1.0.0` a `v1.4.0`), un despliegue protegido y respaldado, y una restauración de 31 s. Lo que no alcanza la meta es el rendimiento web del backend y del tablero (límite conocido).

## 7.2 Una conclusión por problema del caso

| # | Problema (3.2.4) | Conclusión |
|---|---|---|
| 1 | La liquidación de heladeros es manual | Resuelto con M2: la liquidación diaria calcula lo vendido, el importe a precio de heladero, la comisión y la diferencia de efectivo, crea el pedido de venta y se imprime con firmas |
| 2 | Los lotes vencen sin control y no hay FEFO | Resuelto: los lotes llevan vencimiento, la salida respeta FEFO, un lote vencido no se despacha y hay alerta 30 días antes |
| 3 | Las temperaturas se anotan a mano | Resuelto con M3: rango por cámara, actividad al jefe de almacén ante una lectura fuera de rango y aviso de lotes por vencer. Las lecturas son manuales, sin sensores |
| 4 | La calidad no se liga al lote | Resuelto con M1: inspección por puntos de control ligada a la orden y al lote, certificado en PDF y bloqueo del lote rechazado |
| 5 | La planificación no usa datos consolidados | Resuelto: dashboards y vistas por línea, canal y mes, y el tablero propio de M4 |
| 6 | Cada área digita por separado | Resuelto: un solo ERP con el ciclo vender-comprar-producir-facturar probado de punta a punta |
| 7 | La gerencia no tiene reportes a tiempo | Resuelto: el tablero y los análisis salen del propio ERP y el tablero carga en 2.11 s |

Los siete problemas se resuelven: cuatro con la Fase 1 (2, 5, 6 y 7) y tres con los módulos de la Fase 2 (1, 3 y 4). Resuelto significa que el sistema lo cubre con datos de demostración; no se probó con usuarios ni datos reales.

## 7.3 Una conclusión por área

- **Marketing y ventas:** el embudo CRM, las listas de precios por canal y temporada, el punto de venta con boleta, la facturación con IGV y la liquidación del heladero (M2) cubren el flujo de venta. No hay envío electrónico a SUNAT, que requiere un módulo Enterprise.
- **Logística y producción:** lotes con vencimiento, FEFO, recepción, despacho en dos pasos y reposición a Arequipa funcionan y están probados; las órdenes de producción consumen insumos por FEFO, crean el lote y calculan el costo, y con M1 nace la inspección del lote.
- **Gerencia:** los dashboards, las vistas guardadas y el tablero de M4 muestran ventas, producción, stock por vencer y, según los módulos instalados, calidad, liquidaciones y temperatura.
- **Compras, RR. HH. y TI:** el reabastecimiento mín./máx., los usuarios por rol y la mesa de servicios con SLA funcionan.
- **Infraestructura y seguridad:** la réplica, los respaldos, Nginx con TLS, el segundo factor y la auditoría están hechos y verificados, y las releases publican imagen y zip.

## 7.4 Una conclusión por requerimiento no funcional

| RNF | Resultado | Cumple |
|---|---|---|
| RNF001 portabilidad | Tablero y liquidación revisados en 375 × 812 sin desplazamiento horizontal | Parcial |
| RNF002 rendimiento | p95 de 9 a 18 ms con 20 usuarios virtuales | Sí |
| RNF003 usabilidad | Interfaz en español, revisión por roles y evaluación heurística | Con límites |
| RNF004 trazabilidad de lotes | Probada de la compra a la entrega | Sí |
| RNF005 lote vencido o rechazado | Probado; el punto de venta no verifica el vencimiento | Con límites |
| RNF006 continuidad | RPO de segundos con la réplica y RTO de 31 s | Sí |
| RNF007 mantenibilidad | CI obligatorio con 218 pruebas y `ruff` | Sí |
| RNF008 rendimiento web | Login 100, tablero 76 (carga en 2.11 s) y backend 59: límite conocido | Parcial |
| RNF009 seguridad | ZAP sin alertas altas, 2FA, TLS y contraseñas | Con límites |
| RNF010 auditoría | `auditlog` en precios, pedidos y compras | Sí |
| RNF011 disponibilidad | Reinicio automático y *healthcheck*; sin medición continua | Parcial |
| RNF012 reproducibilidad | Entorno con un comando; cinco releases con imagen y zip | Sí |
| RNF013 datos personales | Datos ficticios, sin política de privacidad | Parcial |

De los 13 RNF, 6 cumplen, 3 cumplen con límites y 4 son parciales.

## 7.5 Conclusión sobre la gestión del proyecto

Scrum y la revisión cruzada funcionaron: cada cambio entró por un PR aprobado por el otro integrante y con el CI en verde (79 de 82 PR con la aprobación vigente), y la velocidad fue de 24, 30, 27 y 34 puntos. El plazo único obligó a sprints de un día: el núcleo se completó en unas 21 horas y la Fase 2 entre el 24 y el 25/11, gracias al orden fijo M1 → M4. Ningún módulo quedó a medias; lo que quedó fuera es la página de aterrizaje opcional (HU-31). De Odoo 19 se aprendió que muchas necesidades se resuelven mejor con la configuración estándar que con código propio; los módulos propios se limitaron a lo que Community no trae.

Como trabajo futuro quedan la medición de la disponibilidad en el tiempo, la revisión de la portabilidad en más navegadores, y lo que se recomienda en la sección 8: sensores de temperatura, aplicación móvil para el heladero, envío electrónico a SUNAT, `auditlog` en los módulos nuevos y pruebas de JavaScript.
