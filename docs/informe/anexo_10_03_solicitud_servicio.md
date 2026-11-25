# Anexo 10.3 Solicitud de servicio o de acceso

Este anexo trae el formato de la solicitud de servicio o de acceso (ITIL 4) y un ejemplo ficticio de D'Onofrio que coincide con uno de los tickets de la «Mesa de Servicios TI». Una solicitud de servicio es una petición que no es una falla (un reporte, un cambio de datos, una información) y una de acceso pide un usuario, un rol o un cambio de permisos. Se registran como ticket de Project en Odoo; una falla usa el anexo 10.5 y un cambio al software, el 10.4.

## Formato y ejemplo lleno: alta de un liquidador para la temporada de verano

| Campo | Contenido |
|---|---|
| ID, fecha y tipo | `SOL-001` · 16/11/2026, 10:00 (hora de Lima) · **solicitud de acceso** |
| Solicitante | Jefe de Ventas, área Comercial |
| Descripción y justificación | Crear un usuario con el rol de liquidador de heladeros para el CD Arequipa durante la campaña de verano, porque la demanda sube y la liquidación diaria necesita una persona más |
| Aprobador | Gerente General (autoriza el rol) y Responsable de TI (crea el usuario) |
| Rol solicitado | Usuario interno con el grupo «Solo operaciones del CD Arequipa» (ve solo las transferencias, movimientos y existencias de ese almacén) y los permisos del liquidador; sin acceso a otras áreas |
| Prioridad y SLA | Media (P3): respuesta en 8 h y resolución en 3 días; fecha límite 19/11/2026, 10:00 (matriz de 4.7.3) |
| Atención | El Responsable de TI crea el usuario, le asigna el grupo, entrega la contraseña inicial por el canal acordado y confirma el primer ingreso |
| Cierre | 21/11/2026, 09:00: SLA incumplido por 47 h |
| Observaciones | La aprobación del Gerente General llegó el 20/11. Mejora: pedirla al abrir la solicitud y, para campañas conocidas, abrir el ticket con una semana de anticipación |

El estado «SLA incumplido» sale del campo calculado del ticket y aparece en el pivote «Cumplimiento del SLA por tipo de ticket». La mesa mide la resolución y no la primera respuesta, y la aprobación del Gerente General es un paso manual que queda en el historial del ticket.
