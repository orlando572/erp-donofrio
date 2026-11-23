# Acta de constitución del proyecto

[← docs/pm](.)

| Campo | Valor |
|---|---|
| **Proyecto** | ERP para D'Onofrio con Odoo 19 (proyecto final) |
| **Fecha** | 22/11/2026 (Sprint 0) |
| **Curso** | Sistemas de Información Empresarial, UTP Arequipa |
| **Patrocinador académico** | MBA Mg. Ing. René Alonso Nieto Valencia (docente) |
| **Product Owner** | Evelyn |
| **Scrum Master** | Orlando |
| **Estado** | Redactada por Orlando por encargo de Evelyn, que no pudo hacer su parte del S0. **Pendiente de revisión y aprobación de Evelyn** |

## 1. Empresa asignada

El docente asignó **D'Onofrio** a este grupo y **somos el único grupo con esta empresa** (informado por el equipo el 22/11/2026). Con esto se cumple la regla de "sin empresas repetidas" y se cierra el hito H0 y el riesgo R3.

## 2. Objetivo

Construir un ERP funcional sobre **Odoo 19.0 Community + PostgreSQL 16 en Docker** para la unidad de helados y confitería de D'Onofrio (corte 2026), que cubra las cinco áreas de los lineamientos: Marketing y Ventas, Logística, Producción, Gerencia y áreas de apoyo (Compras, Facturación, RR. HH.). El proyecto incluye el informe, los dos manuales, la presentación de 10 minutos, el repositorio y el código fuente comprimido.

## 3. Justificación

El negocio es estacional: helados en verano y panetón en Navidad (ver [01 §1.1](../plan/01_alcance_escenario.md)). Hoy la liquidación de heladeros, las temperaturas y las inspecciones se llevan en papel o Excel, con sistemas separados por área (supuesto S7). Un ERP integrado resuelve los 7 problemas identificados en [01 §1.6](../plan/01_alcance_escenario.md).

## 4. Alcance en dos fases

- **Fase 1, núcleo (garantizada, 83 puntos):** Docker, GitHub, CI y GitHub Projects; `donofrio_base` con datos y configuración por código; CRM, Ventas, PdV, Inventario con lotes y FEFO, MRP, Compras, Facturación `l10n_pe` y RR. HH.; dashboards estándar; réplica, respaldos, Nginx con TLS y seguridad; pruebas; release `v1.0.0`; informe completo para ese alcance.
- **Gate 0:** el agente de IA se detiene y entrega un informe; el equipo decide por criterios si empieza la Fase 2. No empieza ningún módulo propio sin confirmación explícita de Evelyn u Orlando.
- **Fase 2, extensión (si alcanza el tiempo, 37 puntos):** M1 `donofrio_calidad`, M2 `donofrio_heladeros`, M3 cadena de frío, M4 `donofrio_tablero` + branding, uno a uno y con mini gate. Lo inconcluso no se fusiona y queda como trabajo futuro con su diseño.

**Fuera del alcance** (limitaciones declaradas): envío de comprobantes a SUNAT/OSE, nómina peruana, contabilidad con reportes financieros (Enterprise), app móvil nativa, integración con proveedores reales, migración de datos históricos y simulación de la transición a Froneri.

## 5. Supuestos

- Los supuestos S1 a S9 de [01 §1.3](../plan/01_alcance_escenario.md) (corte 2026, datos ficticios, heladeros concesionarios, rangos de temperatura, un servidor con réplica, moneda PEN).
- Los dos integrantes pueden dedicar un sprint de ~1 día por etapa hasta el viernes 27/11.
- GitHub, Docker, Odoo Community y OCA se mantienen disponibles y gratuitos.

## 6. Restricciones

- **Plazo único:** entrega de todo el **viernes 27 de noviembre de 2026, 14:30**, por UTP+Class, **un solo integrante y un solo intento**. El "18 de julio, 07:00" del PDF es un dato de la plantilla.
- Equipo de **2 personas** (los lineamientos permiten hasta 3) más un asistente de IA que no es un rol.
- **S/ 0 en licencias:** solo software libre y planes gratuitos (Odoo Community, GitHub y GitHub Projects).
- Solo Odoo 19.0 Community: nada de Enterprise (Calidad, `account_reports`, `hr_payroll`, `l10n_pe_edi`, `web_enterprise`).
- Datos ficticios: RUC ficticio con dígito verificador válido, personas y precios inventados (Ley 29733).
- Informe sobre la plantilla del docente, en PDF, con APA 7 y uso de IA declarado.

## 7. Hitos

Los hitos van en orden y sin fechas intermedias; el único plazo es el de H8 (ver [04 §4.10](../plan/04_scrum_pmbok.md)).

| Hito | Entregable verificable | Sprint | Resp. | Estado |
|---|---|---|---|---|
| H0 | Acta de constitución; empresa confirmada con el docente | S0 | E | Acta redactada; empresa confirmada. Falta la revisión de Evelyn |
| H1 | Entorno Docker + repo + CI en verde | S1 | O | Repo listo; falta Docker y CI |
| H2 | Datos maestros de D'Onofrio por código (`donofrio_base`) | S1 | O | Pendiente |
| H3 | Ciclo estándar de punta a punta + transacciones | S2 | E+O | Pendiente |
| **H4** | **Núcleo v1.0.0 entregable → Gate 0** | S3 | E+O | Pendiente |
| H5 | Módulos de la F2 confirmados en el gate, cada uno con su tag | S4 | E+O | Pendiente |
| H6 | Informe PDF, manuales, PPT y zip finales | Cierre | E+O | Pendiente |
| H7 | 2 ensayos cronometrados (≤ 10 min) | Cierre | E+O | Pendiente |
| **H8** | **Entrega de todo: viernes 27/11, 14:30** | Cierre | E sube, O verifica | Pendiente |

## 8. Presupuesto

S/ 0 en licencias. El costo es el tiempo del equipo.

## 9. Riesgos de alto nivel

R1 (plazo), R2 (API obsoleta de Odoo), R9 (subida única), R14 (demo en vivo) y R17 (la Fase 2 se come el Cierre). El registro completo está en [plan_riesgos.md](plan_riesgos.md).

## 10. Criterios de éxito

1. La Fase 1 cumple todos sus criterios de salida y existe el tag `v1.0.0` con CI en verde ([04 §4.3](../plan/04_scrum_pmbok.md)).
2. Los seis entregables a-f están completos y subidos antes del viernes 27/11, 14:30.
3. Cada integrante puede levantar el entorno con `docker compose up`, explicar la arquitectura y defender su área de punta a punta.
4. La exposición cabe en 10 minutos.

## 11. Aprobaciones

| Rol | Persona | Aprobación |
|---|---|---|
| Product Owner | Evelyn | Pendiente |
| Scrum Master | Orlando | Redactó y aprueba el 22/11/2026 |
