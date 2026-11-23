# 4.1.3 Arquitectura empresarial

> **Estado:** borrador del Sprint 1 · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** [01 §1.6](../plan/01_alcance_escenario.md), [09 §9.1](../plan/09_normas_marcos.md), [03](../plan/03_modulos_odoo.md)
>
> La situación actual (AS-IS) es un supuesto académico (S7): no hay acceso a los sistemas internos de D'Onofrio. La propuesta (TO-BE) sí describe lo que se construye en este proyecto.

## Marco y alcance

Se ordena la arquitectura con las **cuatro capas de TOGAF** (negocio, datos, aplicación y tecnología), usadas de forma simplificada: no se aplica el método completo de TOGAF, solo su clasificación de capas, para comparar la situación actual con la propuesta. Los objetivos de gestión de **COBIT 2019** que el ERP ayuda a cumplir se enlazan al final de la sección.

![Arquitectura empresarial AS-IS y TO-BE](../diagramas/arquitectura/arquitectura_empresarial.png)

*Figura 4.1.3-a. Capas de la arquitectura empresarial, situación actual frente a propuesta. Se genera con [`generar_arquitectura.py`](../diagramas/generar_arquitectura.py).*

## Arquitectura actual (AS-IS) y propuesta (TO-BE) por capa

| Capa | AS-IS (supuesto S7) | TO-BE (propuesta con Odoo 19) | Problemas que resuelve ([01 §1.6](../plan/01_alcance_escenario.md)) |
|---|---|---|---|
| **Negocio** | Cinco áreas con procesos manuales: venta B2B, liquidación del heladero, producción y calidad, almacén con cadena de frío y compras. Cada área decide con sus papeles; la gerencia recibe reportes armados a mano al cierre | Procesos de punta a punta en un solo flujo: CRM → pedido → entrega FEFO → factura; compra → recepción; orden de producción → lote. Punto de venta con boleta, gerencia con dashboards y vistas pivote, y mesa de servicios TI | 5, 6 y 7 |
| **Datos** | Excel por área, kárdex, planillas de temperatura y formatos de inspección en papel. No hay lote ni vencimiento en un sistema, y el mismo dato se digita dos o más veces | Una sola base **PostgreSQL 16** donde lote, vencimiento y movimiento quedan ligados. Los datos maestros se cargan por código con `donofrio_base`. Réplica de lectura y respaldos diarios (Sprint 3) | 2, 4 y 6 |
| **Aplicación** | Excel, correo y Word; un sistema contable aislado; ninguna integración entre áreas | **Odoo 19 Community** con Ventas, CRM, Punto de venta, Inventario, Manufactura, Compras, Facturación (`l10n_pe`), RR. HH. y Project. `donofrio_base` en la Fase 1; `donofrio_calidad`, `donofrio_heladeros` y `donofrio_tablero` en la Fase 2, solo si se confirman en el gate | 1 a 7 (la F2 cubre 1, 3 y 4 de forma completa) |
| **Tecnología** | PC de oficina y un servidor de archivos. Sin entornos separados ni respaldos verificados | **Docker Compose** (Odoo 19 + PostgreSQL 16), Nginx con TLS y réplica en el Sprint 3. GitHub (código y Projects), Actions (CI) y GHCR (imágenes). Ubuntu o WSL2 en las PC de desarrollo ([4.3.1](04_03_infraestructura.md)) | 6 |

## Estado de la arquitectura propuesta al cierre del Sprint 1

| Capa | Ya está en `develop` | Falta |
|---|---|---|
| Negocio | Compañía con localización peruana (RUC ficticio, PEN, IGV 18 %), 10 usuarios por rol con permisos mínimos, organigrama y empleados en RR. HH. (HU-05) | Los procesos de punta a punta (Sprint 2) y los dashboards (Sprint 3) |
| Datos | Base PostgreSQL 16 con datos maestros cargados por código: 2 almacenes y 8 ubicaciones, 25 productos terminados, 22 insumos y 12 recetas con lote y vida útil | Transacciones de demostración (HU-16), réplica (HU-25) y respaldos (HU-26) |
| Aplicación | Odoo 19 con Inventario, Manufactura, Ventas, Compras, Punto de venta, Facturación y RR. HH. instalados; módulo `donofrio_base` | CRM, Project y los dashboards; los módulos propios de la Fase 2 no se empiezan sin confirmación del equipo |
| Tecnología | Docker Compose con Odoo y PostgreSQL, CI en cada PR, protección de `develop` con revisión y CI obligatorios | Nginx con TLS (HU-27), imágenes en GHCR y release `v1.0.0` (HU-29), VM en la nube (opcional) |

## Objetivos de COBIT 2019 que soporta la arquitectura

COBIT 2019 se usa como marco de referencia (alineación, no certificación). Estos son los objetivos de gestión que cubre el ERP y el elemento de la arquitectura que los respalda:

| Objetivo COBIT 2019 | Qué elemento de la arquitectura lo respalda |
|---|---|
| **BAI03** Gestión de la identificación y construcción de soluciones | Odoo configurado por código y `donofrio_base` versionado en Git, con pruebas automáticas en el CI |
| **BAI06** Gestión de los cambios de TI | Ramas `feature/HU-xx` → PR con revisión cruzada → `develop`; protección de rama y CI obligatorio |
| **DSS01** Gestión de operaciones | Docker Compose con *healthchecks* y reinicio automático; un solo comando para levantar el entorno |
| **DSS02** Gestión de solicitudes de servicio e incidentes | Mesa de servicios en Project con tipos ITIL (HU-32, Sprint 3) |
| **DSS03** Gestión de problemas | Issues de GitHub con la plantilla «Bug» |
| **DSS04** Gestión de la continuidad | Réplica de PostgreSQL y respaldos con restauración probada (HU-25 y HU-26, Sprint 3) |
| **DSS05** Gestión de servicios de seguridad | Roles con mínimo privilegio y `ir.rule` (HU-04); gestor de BD deshabilitado; TLS, 2FA y política de contraseñas en el Sprint 3 |
| **APO12** Gestión del riesgo | Plan de riesgos en `docs/pm/plan_riesgos.md` |
| **APO13** Gestión de la seguridad | Controles de ISO 27001 demostrados en Odoo (ver [09 §9.2](../plan/09_normas_marcos.md)) |
| **APO09** Gestión de acuerdos de servicio | SLA por prioridad de la mesa de servicios (Sprint 3) |
| **MEA01** Monitoreo del desempeño y la conformidad | Burndown por puntos, CI y pruebas de carga, seguridad y WPO (Sprint 3) |

> Los objetivos DSS02, DSS04, APO09 y MEA01 dependen de trabajo del Sprint 3: hoy están **planificados**, no implementados.
