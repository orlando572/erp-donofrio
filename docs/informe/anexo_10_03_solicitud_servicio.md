# Anexo 10.3 Documentos y formatos de solicitud de servicios, información y accesos

Este anexo trae el formato de la solicitud de servicio, de información o de acceso (ITIL 4) y dos ejemplos de D'Onofrio que coinciden con tickets de la «Mesa de Servicios TI». Una solicitud de servicio es una petición que no es una falla (un reporte, un cambio de datos, una información) y una de acceso pide un usuario, un rol o un cambio de permisos. Se registran como ticket de Project en Odoo; una falla usa el anexo 10.6 y un cambio al software, el 10.4.

## Formato y ejemplo lleno: alta de un liquidador para la temporada de verano

| Campo | Contenido |
|---|---|
| ID, fecha y tipo | `SOL-001` · 16/11/2026, 10:00 (hora de Lima) · solicitud de acceso |
| Solicitante | Jefe de Ventas, área Comercial |
| Descripción y justificación | Crear un usuario con el rol de liquidador de heladeros para el CD Arequipa durante la campaña de verano, porque la demanda sube y la liquidación diaria necesita una persona más |
| Aprobador | Gerente General (autoriza el rol) y Responsable de TI (crea el usuario) |
| Rol solicitado | Usuario interno con el grupo «Solo operaciones del CD Arequipa» (ve solo las transferencias, movimientos y existencias de ese almacén) y los permisos del liquidador; sin acceso a otras áreas |
| Prioridad y SLA | Media (P3): respuesta en 8 h y resolución en 3 días; fecha límite 19/11/2026, 10:00 (matriz de 2.7.3) |
| Atención | El Responsable de TI crea el usuario, le asigna el grupo, entrega la contraseña inicial por el canal acordado y confirma el primer ingreso |
| Cierre | 21/11/2026, 09:00: SLA incumplido por 47 h |
| Observaciones | La aprobación del Gerente General llegó el 20/11. Mejora: pedirla al abrir la solicitud y, para campañas conocidas, abrir el ticket con una semana de anticipación |

El estado «SLA incumplido» sale del campo calculado del ticket; la aprobación del Gerente General es un paso manual que queda en el historial.

## Ejemplo lleno: nuevo reporte de ventas por zona

| Campo | Contenido |
|---|---|
| ID y tipo | `SOL-002` · solicitud de servicio (un reporte nuevo; una consulta sobre un reporte existente se registra igual y se marca como solicitud de información) |
| Solicitante | Jefatura de Ventas, área Comercial |
| Descripción y justificación | Ver las ventas por distrito de Lima para asignar zonas a los vendedores |
| Aprobador | Jefe de Ventas (necesidad) y Responsable de TI (solución) |
| Prioridad y SLA | Baja (P4): respuesta en 1 día y resolución en 5 días (matriz de 2.7.3) |
| Atención | El Responsable de TI evalúa si basta con una vista guardada del análisis de ventas agrupada por distrito; si exige código, abre una solicitud de cambio (anexo 10.4) |
| Estado | Nuevo, en la etapa inicial de la Mesa de Servicios TI |

