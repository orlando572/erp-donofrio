# Anexo 10.5 Documentos y formatos de plan de rendimiento y capacidad de servicios

Este anexo trae el formato del plan de rendimiento y capacidad (ITIL 4, gestión de la capacidad y del rendimiento) y el plan lleno con las mediciones del proyecto (4.3). El plan se revisa en cada versión y antes de cada temporada alta.

## Formato y ejemplo lleno: PCR-001, ERP D'Onofrio en el despliegue protegido

| Campo | Contenido |
|---|---|
| ID, fecha y responsable | `PCR-001` · 23/11/2026 (mediciones de la HU-28) · Orlando, Responsable de TI |
| Servicio y alcance | ERP Odoo 19.0 en el despliegue protegido (`https://localhost:8443`): Nginx, Odoo con 2 procesos de trabajo, PostgreSQL 16 primario y réplica |
| Demanda considerada | 10 roles de usuario; prueba con 20 usuarios virtuales concurrentes (carga normal con pausas de 1 a 3 s y esfuerzo sin pausas) |
| Recursos del nodo | 12 CPU lógicas y 14 GB de RAM; el entorno necesita unos 4 GB libres; contenedores sin límites de CPU ni de memoria |
| Métricas y umbrales | p95 < 2 s; errores < 1 %; LCP del tablero < 3 s; RTO ≤ 2 h; RPO de 24 h con respaldo y de segundos con réplica |
| Línea base medida | p95 de 9.1 a 13.0 ms (login 342 ms) y 0 % de errores; esfuerzo: p95 de 100 ms; Odoo 39 % de CPU y 440 MiB (esfuerzo: 160 % y 513 MiB); PostgreSQL 57 % y 201 MiB en esfuerzo; tablero en 2.11 s; RTO de 31 s; réplica con retraso de 2.3 ms |
| Herramientas | k6, el monitor de recursos de Docker cada 10 s, Lighthouse 12, el script de verificación de la réplica, el script de restauración y el flujo de rendimiento |
| Recurso crítico | CPU de Odoo (2 procesos de trabajo) |
| Acciones planificadas | Aumentar los procesos de trabajo si la CPU de Odoo pasa del 80 % de forma sostenida o el p95 supera 1 s; repetir k6 antes del verano con los usuarios previstos; vigilar el tamaño de la base y de los respaldos en cada versión |
| Próxima revisión | En la siguiente versión o antes de la temporada de verano, lo que ocurra primero |
| Aprobación | Product Owner (Evelyn) y Responsable de TI (Orlando) |
