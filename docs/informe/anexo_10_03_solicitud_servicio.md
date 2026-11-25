# Anexo 10.3 Solicitud de servicio o de acceso

> **Estado:** versión final del Cierre (25/11/2026; los datos medidos son los del 23/11/2026 salvo donde se indica) · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [09 §9.3](../plan/09_normas_marcos.md) (ITIL 4, gestión de solicitudes de servicio), [4.7](04_07_acuerdos_de_nivel_de_servicio.md) (SLA) y la mesa de servicios de HU-32
>
> Los anexos 10.4 (solicitud de cambio) y 10.6 (SoA) son de Orlando; el 10.5 (registro de incidente) es de Evelyn. Este anexo trae el **formato** de la solicitud de servicio o de acceso y **un ejemplo lleno** con un caso de D'Onofrio. El ejemplo es **ficticio** y coincide con uno de los cinco tickets de ejemplo de la «Mesa de Servicios TI».
>
> *El proyecto se **alinea** con las normas y marcos citados como buenas prácticas de referencia. No constituye una implementación certificada ni auditada de ninguno de ellos.*

## 1. Cuándo se usa

Una **solicitud de servicio** es una petición de un usuario que no es una falla: un reporte nuevo, un cambio de datos o una información. Una **solicitud de acceso** es una petición de un usuario o de un rol nuevo, o de un cambio de permisos. Las dos se registran como ticket en la app **Project** de Odoo (proyecto «Mesa de Servicios TI»), con la etiqueta *Solicitud de servicio* o *Solicitud de acceso*. Si lo que se pide es una **falla**, se usa el [anexo 10.5](anexo_10_05_incidente.md); si es un **cambio al software**, el [anexo 10.4](anexo_10_04_rfc.md).

## 2. Formato de la solicitud

| Campo | Qué se anota |
|---|---|
| **ID** | `SOL-nnn` y el ticket de la mesa de servicios |
| **Fecha y hora** | De la solicitud |
| **Solicitante y área** | Quién pide y su área |
| **Tipo** | Solicitud de servicio o solicitud de acceso |
| **Descripción** | Qué se pide, en una o dos frases |
| **Justificación** | Para qué lo necesita el negocio |
| **Aprobador** | Quién autoriza (el jefe del área; para accesos, el jefe y el responsable de TI) |
| **Rol o permiso solicitado** | Solo para accesos: grupo de Odoo y alcance |
| **Prioridad y SLA** | Según la matriz de [4.7.3](04_07_acuerdos_de_nivel_de_servicio.md): Urgente, Alta, Media o Baja, y su plazo de resolución |
| **Atención** | Quién la resuelve, qué se hizo y cuándo |
| **Cierre y SLA** | Fecha de cierre y si se cumplió el plazo |
| **Observaciones** | Retrasos, aprendizajes o seguimiento |

## 3. Ejemplo lleno: alta de un liquidador para la temporada de verano

| Campo | Contenido |
|---|---|
| **ID** | `SOL-001` · ticket «Alta de un liquidador para la temporada de verano en el CD Arequipa» |
| **Fecha y hora** | 16/11/2026, 10:00 (hora de Lima) |
| **Solicitante y área** | Jefe de Ventas, área Comercial |
| **Tipo** | **Solicitud de acceso** |
| **Descripción** | Crear un usuario con el rol de liquidador de heladeros para el CD Arequipa durante la campaña de verano |
| **Justificación** | La demanda de helados sube en verano y la liquidación diaria de los heladeros de Arequipa necesita una persona más; sin usuario no puede registrar su trabajo |
| **Aprobador** | Gerente General (autoriza el rol) y Responsable de TI (crea el usuario) |
| **Rol o permiso solicitado** | Usuario interno con el grupo **«Solo operaciones del CD Arequipa»** (ve únicamente las transferencias, los movimientos y las existencias de ese almacén) y los permisos del liquidador de heladeros. Sin acceso a datos de otras áreas |
| **Prioridad y SLA** | **Media (P3)**: respuesta en 8 h y **resolución en 3 días**. Fecha límite: 19/11/2026, 10:00 |
| **Atención** | Responsable de TI: crea el usuario, le asigna el grupo, activa la contraseña inicial por el canal acordado y confirma el primer ingreso |
| **Cierre y SLA** | Cerrado el 21/11/2026, 09:00. **SLA incumplido** por 47 h |
| **Observaciones** | El retraso se debió a que la aprobación del Gerente General llegó el 20/11. Mejora propuesta: pedir la aprobación al abrir la solicitud y no al atenderla; para campañas conocidas, abrir el ticket con una semana de anticipación |

## 4. Cómo se ve en la mesa de servicios

El ticket del ejemplo está en la mesa de servicios con su etiqueta, su prioridad Media y las fechas de arriba. Su estado de cumplimiento («SLA incumplido») sale del campo calculado y aparece en el pivote «Cumplimiento del SLA por tipo de ticket». Captura: `docs/capturas/sprint-3/HU-32_pivote_cumplimiento_sla.png`.

## 5. Limitaciones

- El ejemplo es ficticio y se cargó como dato de demostración; las fechas son las del ticket de ejemplo.
- La aprobación del Gerente General no está automatizada en Odoo: es un paso manual y queda en el historial del ticket.
- La mesa mide la **resolución**, no la respuesta ([4.7.3](04_07_acuerdos_de_nivel_de_servicio.md#limitaciones)).
