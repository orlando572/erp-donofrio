# Anexo 10.5 Registro de incidente

> **Estado:** versión final del Cierre (25/11/2026; los datos medidos son los del 23/11/2026 salvo donde se indica) · **Autora:** Evelyn (PO) · **Revisa:** Orlando · **Fuente:** [09 §9.3](../plan/09_normas_marcos.md) (ITIL 4, gestión de incidentes), [4.7](04_07_acuerdos_de_nivel_de_servicio.md) (SLA) y la mesa de servicios de HU-32
>
> Este anexo trae el **formato** del registro de incidente, la **matriz de prioridad** (impacto × urgencia) y **un ejemplo lleno** con un caso de D'Onofrio. El ejemplo es **ficticio** y coincide con uno de los cinco tickets de ejemplo de la «Mesa de Servicios TI».
>
> *El proyecto se **alinea** con las normas y marcos citados como buenas prácticas de referencia. No constituye una implementación certificada ni auditada de ninguno de ellos.*

## 1. Cuándo se usa

Un **incidente** es una interrupción o una falla del servicio: algo que antes funcionaba y ya no. Se registra como ticket de tipo *Incidente* en la «Mesa de Servicios TI». Si lo que se pide no es una falla, se usa el [anexo 10.3](anexo_10_03_solicitud_servicio.md).

## 2. Matriz de prioridad (impacto × urgencia)

El **impacto** es cuánto del negocio afecta; la **urgencia**, qué tan pronto hay que resolverlo.

| | **Urgencia alta** (no se puede trabajar) | **Urgencia media** (hay alternativa) | **Urgencia baja** (puede esperar) |
|---|---|---|---|
| **Impacto alto** (varias áreas o ventas) | **P1 Crítica** | **P2 Alta** | **P3 Media** |
| **Impacto medio** (un área) | **P2 Alta** | **P3 Media** | **P4 Baja** |
| **Impacto bajo** (una persona) | **P3 Media** | **P4 Baja** | **P4 Baja** |

Y su plazo, tomado de la tabla 15 de [4.7.3](04_07_acuerdos_de_nivel_de_servicio.md): **P1** respuesta 30 min y resolución 4 h · **P2** 2 h y 8 h · **P3** 8 h y 3 días · **P4** 1 día y 5 días. En Odoo 19 las prioridades son Urgente (P1), Alta (P2), Media (P3) y Baja (P4), y el plazo se calcula solo al crear el ticket.

## 3. Formato del registro

| Campo | Qué se anota |
|---|---|
| **ID** | `INC-nnn` y el ticket de la mesa de servicios |
| **Fecha y hora** | De la detección y del registro |
| **Reportante** | Quién avisa y su área |
| **Servicio afectado** | Qué parte del ERP o de la infraestructura falla |
| **Descripción del síntoma** | Qué se ve, desde cuándo y a quién afecta |
| **Impacto × urgencia → prioridad** | Según la matriz de la sección 2 |
| **SLA** | Respuesta y resolución esperadas |
| **Diagnóstico** | Qué se encontró |
| **Solución o contención** | Qué se hizo para restablecer el servicio |
| **Tiempo de resolución frente al SLA** | Cuánto tardó y si se cumplió |
| **Causa raíz** | Por qué ocurrió; si se repite o es de software, se abre un **problema** (plantilla `bug.yml`) |
| **Acción preventiva** | Qué evita que se repita |

## 4. Ejemplo lleno: el tablero gerencial no carga

| Campo | Contenido |
|---|---|
| **ID** | `INC-001` · ticket «Tablero gerencial no carga» |
| **Fecha y hora** | 20/11/2026, 07:00 (hora de Lima) |
| **Reportante** | Gerente General, Dirección |
| **Servicio afectado** | Tableros de Odoo (panel de ventas del gerente) |
| **Descripción del síntoma** | Al abrir el panel de ventas, la pantalla queda en blanco. Afecta solo al gerente |
| **Impacto × urgencia → prioridad** | Impacto **medio** (una persona de dirección que decide con ese panel) × urgencia **alta** (lo necesita para una reunión del día) → **P2 Alta** |
| **SLA** | Respuesta 2 h · **resolución 8 h**. Fecha límite: 20/11/2026, 15:00 |
| **Diagnóstico** | Otros usuarios abren el mismo panel sin problema, así que el servidor funciona. El problema es del navegador del gerente: guardó una versión vieja de los archivos de la página |
| **Solución o contención** | Se limpió la memoria del navegador (caché) y se volvió a abrir el panel. El responsable de TI confirmó con el gerente que se veía bien |
| **Tiempo de resolución frente al SLA** | Cerrado el 20/11/2026 a las 12:30: **5 h 30 min**, dentro de las 8 h. **SLA cumplido** |
| **Causa raíz** | Caché del navegador con archivos antiguos después de una actualización de los paquetes de la página. No es un defecto del sistema |
| **Acción preventiva** | Avisar a los usuarios de dirección que, tras una actualización, deben recargar con *Ctrl + F5*. No se abre un problema porque no hay un defecto que corregir |

## 5. Cómo se ve en la mesa de servicios

El ticket está en la etapa **Cerrado**, con la etiqueta *Incidente*, prioridad Alta y fecha límite 20/11/2026 15:00. Su estado «SLA cumplido» sale del campo calculado y aparece en el pivote «Cumplimiento del SLA por tipo de ticket». Captura: `docs/capturas/sprint-3/HU-32_pivote_cumplimiento_sla.png`.

## 6. Limitaciones

- El ejemplo es ficticio y se cargó como dato de demostración; la causa y el diagnóstico están en la descripción del ticket y aquí se amplían con un texto de ejemplo.
- Odoo Project no registra la primera respuesta, así que solo se mide la resolución.
- La matriz es una propuesta del proyecto: no la firmó ningún cliente.
