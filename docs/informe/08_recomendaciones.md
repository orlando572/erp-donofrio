# 8. Recomendaciones

Con los cuatro módulos desarrollados para D'Onofrio completos (versiones v1.1.0 a v1.4.0), las recomendaciones apuntan a operar, medir y ampliar lo construido. Las de negocio están en 8.1 y las técnicas en 8.2.

## 8.1 Recomendaciones de negocio y gestión

Se desarrollan en la sección 8.1 siguiente.

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
