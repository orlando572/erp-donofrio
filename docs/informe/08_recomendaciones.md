# 8. Recomendaciones

## 8.1 Recomendaciones de negocio y gestión

**Tabla 8.1. Recomendaciones de negocio y gestión**

| # | Recomendación | Problema (1.2.3) | Plazo |
|---|---|---|---|
| 1 | Poner en marcha el sistema con datos reales y capacitación por rol | Los 7 | Corto |
| 2 | Adoptar la liquidación diaria de los heladeros y evaluar una app móvil | 1 | Corto a mediano |
| 3 | Operar la calidad y la cadena de frío ligadas al lote y conectar sensores | 3 y 4 | Mediano |
| 4 | Resolver la facturación electrónica con SUNAT | RF016 | Corto |
| 5 | Medir con el tablero gerencial y ajustar las metas de los KPI | 5 y 7 | Continuo |
| 6 | Mantener la continuidad y la seguridad probadas | RNF006 y RNF009 | Continuo |

1. Datos reales y capacitación. Pasar de los datos ficticios a los reales por áreas (almacenes y productos, clientes y precios, proveedores e insumos, empleados) y capacitar a cada rol con los casos de uso de 2.2.1.3. El ciclo vender-comprar-producir-facturar ya funciona de punta a punta, por lo que el reemplazo es de contenido y no de programación. Conviene observar a los usuarios reales para afinar las pantallas.

2. Liquidación de heladeros. M2 calcula lo vendido, el importe, la comisión y la diferencia de efectivo, y emite el PDF para firmar: es el proceso más reconocible de D'Onofrio y el que concentra el problema 1. Con los datos de demostración, 124 de 127 liquidaciones están liquidadas y la merma es de 0,27 % de lo despachado. Siguientes pasos: una aplicación móvil para el heladero y una merma que descuente inventario. Indicador: descuadre por heladero menor al 2 % de lo despachado.

3. Calidad y cadena de frío. Con M1 y M3 el lote rechazado se bloquea, el certificado sale en PDF y la temperatura fuera de rango genera una alerta, lo que respalda ISO 9001 y HACCP. El siguiente paso es conectar sensores que registren la temperatura.

4. Facturación electrónica. El ERP emite factura (01) y boleta (03) con IGV 18 %. Para el envío electrónico a SUNAT, Finanzas y TI deben elegir un proveedor de servicios electrónicos autorizado (OSE).

5. Tablero gerencial. Usar el tablero de M4 y los dashboards estándar en la reunión semanal de la gerencia y ajustar con datos reales las metas de los KPI. El tablero carga en 2.11 s.

6. Continuidad y seguridad. Operar con lo medido (réplica en caliente, respaldo diario con restauración en 31 s, Nginx con TLS, segundo factor, contraseñas de 12 o más y auditoría), repetir la restauración en el servidor definitivo, guardar una copia fuera de él y medir la disponibilidad en el tiempo.

## 8.2 Recomendaciones técnicas

Se ordenan por prioridad para una puesta en producción real.

### Tabla 8.2-a. Recomendaciones técnicas

| # | Recomendación | Para qué sirve |
|---|---|---|
| T1 | Programar la tarea programada de respaldos, cifrarlos y guardar una copia fuera del equipo | Proteger los respaldos, cuya restauración ya se midió en 31 s |
| T2 | Registrar de forma continua la página de estado de Odoo (por ejemplo, con Uptime Kuma) | Medir en el tiempo la disponibilidad que aseguran el reinicio automático y los chequeos de salud |
| T3 | Probar los casos de uso principales, el tablero y la liquidación en Chrome, Firefox y Edge | Extender a más navegadores la revisión hecha en Chrome y en 375 × 812 |
| T4 | Desplegar en una VM con dominio y Let's Encrypt, con despliegue por SSH y *rollback* a la imagen del tag anterior | Llevar a un servidor el despliegue protegido que ya funciona en local |
| T5 | Configurar un servidor de correo saliente | Habilitar el envío del código de 2FA por correo |
| T6 | Activar la estadística de consultas de PostgreSQL | Medir las consultas, además de la aplicación que mide k6 |
| T7 | Reducir el JavaScript del backend y del tablero | Subir el puntaje de Lighthouse de esas vistas |
| T8 | Activar la protección también para administradores en develop y main | Aplicar las reglas de protección también al administrador |
| T9 | Ampliar la seguridad: promoción de la réplica, ZAP activo y autenticado, Dependabot, prueba de actualización en el CI y TLS entre servicios | Extender las pruebas de 3.2.2 y 3.3.2 |
| T10 | Ampliar los módulos desarrollados para D'Onofrio: sensores de temperatura, el registro de auditoría en liquidaciones, inspecciones y lecturas, pruebas de JavaScript del tablero y app móvil del heladero | Crecer sobre los módulos de 3.1.4.2 a 3.1.4.5 |
| T11 | Envío electrónico de comprobantes a SUNAT mediante un OSE | Completar el ciclo de facturación electrónica |

Antes de la VM (T4) conviene tener los respaldos fuera del equipo (T1), el monitoreo (T2), el correo para el 2FA (T5) y la protección también para administradores (T8); antes de activar la estadística de consultas (T6), un respaldo reciente, porque exige reiniciar PostgreSQL. Toda mejora entra por una rama `feature/HU-xx-*` y un PR a develop, con su prueba.
