# Plan de gestión de riesgos (sección 4.5.1, tabla 10)

[← docs/pm](.) · Detalle y justificación de cada riesgo: [docs/plan/07_riesgos_entrega.md](../plan/07_riesgos_entrega.md)

Versión S0, 22/11/2026. Redactado por Orlando por encargo de Evelyn (PO), que debe revisarlo. Este archivo es el registro de riesgos; se enlaza desde el issue «Registro de riesgos» del GitHub Project, que lleva un comentario en cada Retro.

## Escalas

| Valor | Impacto (I) | Probabilidad (P) |
|---|---|---|
| 1 | Bajo: no afecta la entrega | Poco probable |
| 2 | Medio: retrasa o resta calidad a una sección o módulo | Posible |
| 3 | Alto: pone en riesgo la entrega o la nota | Probable |

**Nivel = I × P.** Prioridad: **Alta** si el nivel es 6-9 (acción inmediata), **Media** si es 3-5 (seguimiento constante), **Baja** si es 1-2 (monitoreo).

## Estrategias

| Estrategia | Significado |
|---|---|
| Evitar | Cambiar el plan para que el riesgo no exista |
| Mitigar | Reducir su impacto o su probabilidad |
| Transferir | Pasar el riesgo a un tercero (no aplica: S/ 0 y sin proveedores) |
| Aceptar | Asumirlo y vigilarlo |

## Matriz de riesgos (impacto × probabilidad)

| Impacto \ Probabilidad | 1 | 2 | 3 |
|---|---|---|---|
| **3** | R3, RS-03, R8 | R4, R5, R15, R17, R9, R14, RS-02, RS-04 | R1, R2 |
| **2** | RS-06 | R16, R18, R19, R20, R7, R11, R13, RS-01, RS-05 | R6 |
| **1** | · | R10, R12 | · |

## Registro

Los riesgos **RS-xx** son propuestos en el S0 a partir de los ejemplos de las tablas 11-13 del plan (docs/plan/07 §7.1); sus valores de I y P se validan en el Planning del S1.

| Id | Etapa | Tipo | Riesgo | I | P | Nivel | Prioridad | Estrategia | Resp. | Estado (S0) |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | Desarrollo | Externo | Plazo muy corto: entrega de todo el viernes 27/11, 14:30 | 3 | 3 | 9 | Alta | Mitigar: sprints de ~1 día en orden fijo; la F1 garantiza el entregable; Gate 0 por criterios; Cierre reservado | Evelyn | Abierto |
| R2 | Desarrollo | Técnico | API obsoleta de Odoo generada por el agente de IA o tutoriales viejos | 3 | 3 | 9 | Alta | Mitigar: fuentes 19.0 locales, ficha de cambios, hook, check_legacy en CI, instalación con tests en cada PR | Orlando | Mitigando (capas 1-4 hechas en S0; falta CI) |
| R3 | Desarrollo | Organizacional | Otro grupo elige la misma empresa | 3 | 1 | 3 | Media | Evitar: el docente asignó D'Onofrio al grupo en S0 y es el único grupo con esta empresa | Evelyn | Cerrado (22/11: el docente asignó D'Onofrio; único grupo) |
| R4 | Desarrollo | Humano | Carga desigual o un integrante no puede defender su parte | 3 | 2 | 6 | Alta | Mitigar: reparto por áreas de punta a punta, revisión cruzada, demos cruzadas, 2 ensayos | Evelyn + Orlando | Abierto (en S0 Orlando cubrió el trabajo de PO; Evelyn debe revisarlo) |
| R5 | Desarrollo | Organizacional | Uso de IA no declarado se interpreta como plagio | 3 | 2 | 6 | Alta | Evitar: declarar el asistente de IA en la metodología; todo revisado y entendido por quien lo firma; fuentes citadas | Evelyn + Orlando | Abierto |
| R6 | Desarrollo | Técnico | Módulo OCA o funcionalidad no disponible en Community 19 | 2 | 3 | 6 | Alta | Aceptar/Mitigar: módulo propio pequeño; EDI y nómina declarados como limitación | Orlando | Abierto |
| R10 | Desarrollo | Externo | Cambia el escenario Froneri antes de la entrega | 1 | 2 | 2 | Baja | Aceptar: fecha de corte 2026 declarada; solo se actualiza el párrafo del entorno | Evelyn | Abierto |
| R12 | Desarrollo | Organizacional | El título 6.3 de la plantilla nombra otra herramienta y el evaluador espera verla | 1 | 2 | 2 | Baja | Mitigar: una línea bajo el título que justifica GitHub Projects (04 §4.11) y aviso al docente | Evelyn | Abierto |
| R15 | Desarrollo | Organizacional | La documentación se deja para el final | 3 | 2 | 6 | Alta | Evitar: la DoD exige un borrador por HU; checklist de secciones en el issue «Informe final»; el Gate 0 exige el informe en borrador | Evelyn | Abierto |
| R16 | Desarrollo | Técnico | La evidencia de Scrum se concentra en pocos días | 2 | 2 | 4 | Media | Mitigar: commits pequeños y diarios de ambos; actas fechadas | Orlando | Abierto |
| R17 | Desarrollo | Organizacional | La Fase 2 se come el tiempo del Cierre o deja un módulo a medias | 3 | 2 | 6 | Alta | Evitar: Gate 0 y mini gates por criterios; cierre reservado; lo inconcluso no se fusiona | Orlando (criterios), Evelyn (decisión) | Abierto (se revisa en cada gate) |
| R18 | Desarrollo | Técnico | El agente de IA sigue con la Fase 2 sin autorización tras el gate | 2 | 2 | 4 | Media | Evitar: regla del gate en CLAUDE.md; solo vale la confirmación explícita en el chat | Orlando | Mitigado (regla en CLAUDE.md desde S0) |
| R19 | Desarrollo | Humano | Sin Fase 2, un integrante se queda sin código propio que defender | 2 | 2 | 4 | Media | Mitigar: cada uno es dueño de sus datos, tests y configuración en donofrio_base | Evelyn + Orlando | Abierto |
| R20 | Desarrollo | Humano | Fatiga por el ritmo de un sprint por día | 2 | 2 | 4 | Media | Mitigar: dailies cortas, revisión cruzada, CI como red de seguridad, Cierre sin desarrollo | Evelyn + Orlando | Abierto |
| R7 | Despliegue | Técnico | PC con poca RAM para Odoo, PostgreSQL, réplica y Nginx | 2 | 2 | 4 | Media | Mitigar: perfiles de Compose; réplica y herramientas solo para las evidencias | Orlando | Abierto (PC de Orlando: 14 GB de RAM, ~4 GB libres) |
| R9 | Despliegue | Externo | Falla la subida única a UTP+Class | 3 | 2 | 6 | Alta | Mitigar: generar PDF y zip al inicio del Cierre; subir con margen; checklist 7.2 | Evelyn | Abierto |
| R11 | Despliegue | Legal/ético | Uso de marca, logo o identidad real (impersonación) | 2 | 2 | 4 | Media | Evitar: RUC ficticio, aviso de proyecto académico, repo sin PDF del docente | Evelyn | Mitigando (aviso en el README; PDF del docente en .gitignore) |
| R13 | Despliegue | Humano | La exposición pasa de 10 minutos y se corta | 2 | 2 | 4 | Media | Mitigar: guion cronometrado, corte a los 8:30, video de respaldo | Evelyn + Orlando | Abierto |
| R14 | Despliegue | Técnico | La demo en vivo falla (Docker, red, datos) | 3 | 2 | 6 | Alta | Mitigar: BD de demo respaldada, video grabado, PC probada el día anterior | Orlando | Abierto |
| RS-01 | Despliegue | Técnico | Migración fallida de un módulo (-u) en una BD con datos (propuesto en S0, validar en Planning S1) | 2 | 2 | 4 | Media | Mitigar: la DoD exige -u sobre BD con datos; job upgrade opcional en CI | Orlando | Abierto |
| RS-02 | Despliegue | Técnico | Secretos expuestos en un repo público (propuesto en S0, validar en Planning S1) | 3 | 2 | 6 | Alta | Evitar: .env en .gitignore, GitHub Secrets, secret scanning y push protection activos | Orlando | Mitigando (scanning activo desde S0) |
| RS-03 | Despliegue | Técnico | Puerto del gestor de BD (5432) o /web/database abiertos (propuesto en S0, validar en Planning S1) | 3 | 1 | 3 | Media | Evitar: red interna de Docker, list_db=False, ZAP baseline | Orlando | Abierto |
| R8 | Mantenimiento | Técnico | Pérdida de trabajo (disco, rama borrada, BD corrupta) | 3 | 1 | 3 | Media | Mitigar: push diario, ramas protegidas, BD reproducible por código, backup.sh | Orlando | Mitigando (repo en GitHub con ramas protegidas) |
| RS-04 | Mantenimiento | Técnico | Backups no probados (propuesto en S0, validar en Planning S1) | 3 | 2 | 6 | Alta | Mitigar: restore.sh probado y cronometrado (HU-26) | Orlando | Abierto |
| RS-05 | Mantenimiento | Técnico | Disco lleno (propuesto en S0; disco local al 85 %) | 2 | 2 | 4 | Media | Mitigar: retención de 7 días en backups, limpiar imágenes Docker, revisar espacio antes de cada sprint | Orlando | Abierto |
| RS-06 | Mantenimiento | Técnico | Lotes vencidos por un cron caído (propuesto en S0, validar en Planning S1) | 2 | 1 | 2 | Baja | Mitigar: healthcheck y ejecución semanal de tests | Orlando | Abierto |
| IMP-01 | Impedimentos | Impedimento | GitHub Free no permite proteger ramas en repos privados | 2 | 3 | 6 | Alta | Resuelto: repo público (decisión de Orlando, 22/11) | Orlando | Resuelto |
| IMP-02 | Impedimentos | Impedimento | Evelyn no pudo hacer su parte del S0; la hizo Orlando | 2 | 3 | 6 | Alta | Evelyn revisa los artefactos del PO y los aprueba o corrige | Evelyn | Abierto |

## Seguimiento y validación

- **Seguimiento:** en cada Planning y Retro; **R2, R17 y R18** también en cada gate. Se registra con un comentario en el issue «Registro de riesgos».
- **Validación:** el PO valida y ambos revisan.
- **Tablas 11-13 del informe:** se construyen desde las etapas *Desarrollo*, *Despliegue* y *Mantenimiento* de este registro, con seguimiento, frecuencia, herramienta y validación.
