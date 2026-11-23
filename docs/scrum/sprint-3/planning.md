# Sprint 3 (Calidad del núcleo): Planning

**Fecha:** 23/11/2026 · **Timebox:** ~1 día · **Facilita:** Orlando (SM) · **PO:** Evelyn (pendiente de revisar este planning)

## Objetivo del sprint

"Núcleo v1.0.0 entregable: seguro, replicado, probado, desplegado y documentado."

Fuente: [04 §4.6](../../plan/04_scrum_pmbok.md) y [05 §5.2](../../plan/05_reparto_equipo.md). Fase 1 (núcleo): no hay ningún módulo de la Fase 2 en este sprint. Al cumplir los criterios de salida de [04 §4.3](../../plan/04_scrum_pmbok.md) se llega al Gate 0 (`docs/scrum/gates/gate-0-fase1.md`) y el equipo decide, con confirmación explícita en el chat, qué módulos de la Fase 2 se construyen.

## Historias de usuario (29 puntos)

| HU | Historia | Criterios de aceptación (resumen) | Pts | Resp. | Req. | Épica |
|---|---|---|---|---|---|---|
| HU-23 | Tablero mínimo con lo estándar | Dashboards de Community activos; pivotes y gráficos guardados por código (`ir.filters`): ventas por línea, canal y mes; producción por línea; stock por vencer | 3 | Evelyn | RF013, RF014 | #141 |
| HU-25 | Réplica en caliente de PostgreSQL | El perfil `replica` levanta el standby; `pg_stat_replication` lo muestra; la escritura en la réplica falla | 3 | Orlando | RNF006 | #140 |
| HU-26 | Backups diarios y restauración probada | `backup.sh` (dump + filestore, retención de 7 días); `restore.sh` restaura en una BD nueva; tiempo medido | 3 | Orlando | RNF006 | #140 |
| HU-27 | Despliegue protegido | Nginx con TLS, `list_db=False`, `admin_passwd` desde secreto; `auth_totp` y `auth_totp_mail` para administrador y gerencia; `auth_password_policy` (mínimo 12); *cooldown* de login; `auditlog` | 5 | Orlando | RNF009, RNF010 | #140 |
| HU-28 | Pruebas de carga, seguridad y WPO con resultados | k6 (20 usuarios virtuales) y ZAP baseline sin alertas altas (Orlando); Lighthouse antes/después en login, backend y dashboard (Evelyn) | 5 | Orlando + Evelyn | RNF002, RNF008, RNF009 | #142 |
| HU-29 | *Release* automática | Un tag `v*` publica la imagen en GHCR y el zip del código en GitHub Releases; `v1.0.0` = núcleo | 3 | Orlando | RNF012 | #140 |
| HU-30 | Usabilidad con usuarios | 5 participantes, 4 tareas de procesos estándar cronometradas, SUS calculado | 2 | Evelyn | RNF003 | #141 |
| HU-32 | Mesa de servicios en Project con tipos de ticket ITIL y SLA | Proyecto y etapas por código; etiquetas Incidente, Solicitud de servicio y Solicitud de acceso; fecha límite según prioridad; pivote de cumplimiento del SLA | 2 | Evelyn | RNF011 | #141 |
| HU-33 | Tests de integración de los flujos estándar | En `donofrio_base/tests`: pedido → entrega FEFO → factura (Evelyn); compra → recepción y OP → lote con vencimiento (Orlando); todos en CI | 3 | Orlando + Evelyn | RNF004 | #142 |
| | **Total** | | **29** | | | |

### Épicas del sprint (Project «Scrum ERP D'Onofrio»)

| Issue | Título | Puntos | Responsable |
|---|---|---|---|
| #140 | [HU-25, HU-26, HU-27, HU-29] Infraestructura, réplica y seguridad | 14 | Orlando |
| #141 | [HU-23, HU-30, HU-32] Gerencia, KPIs y mesa de servicios ITIL | 7 | Evelyn |
| #142 | [HU-28, HU-33] Pruebas y calidad del software | 8 | Orlando + Evelyn |
| #143 | Gate 0 | 0 | Evelyn (Orlando verifica) |

## Orden de ejecución de la parte de Orlando

Una tarea a la vez: cada PR se abre directo contra `develop`, se espera la aprobación de Evelyn y recién después se empieza la siguiente. Antes de cada tarea se revisan los últimos commits y PR de `develop`. Se empieza por lo que no depende del trabajo de Evelyn.

1. **HU-25** (`feature/HU-25-replica`): perfil `replica` en `docker-compose.yml`, init del standby en `docker/postgres/replica` y evidencia de `pg_stat_replication`.
2. **HU-26** (`feature/HU-26-backups`): `backup.sh` y `restore.sh` con el tiempo de restauración medido.
3. **HU-27** (`feature/HU-27-seguridad-despliegue`): perfil `proxy` con Nginx y TLS, `odoo.conf` de producción, 2FA, política de contraseñas, *cooldown* y `auditlog`, con la configuración por código. Va antes de k6 y ZAP porque se miden sobre el despliegue con Nginx.
4. **HU-29** (`feature/HU-29-release`): workflow de *release* (imagen en GHCR y zip en GitHub Releases). El tag `v1.0.0` se crea en el Gate 0, no en esta HU.
5. **HU-33, mi parte** (`feature/HU-33-tests-compra-op`): tests de compra → recepción y OP → lote con vencimiento; se revisa antes qué cubren ya las pruebas existentes para no duplicarlas.
6. **HU-28, mi parte** (`feature/HU-28-k6-zap`): script k6 (20 usuarios virtuales) y ZAP baseline en `scripts/perf`, con su reporte.

## Documentación del sprint

| Responsable | Entregables |
|---|---|
| Evelyn | 4.6 (prototipos y reportes estándar, WPO), 4.7, 6.1-6.3, 6.7, 6.8, 6.12, cascada COBIT, ITIL, anexos 10.3 y 10.5, resumen y conclusiones (borrador) |
| Orlando | 4.2.5-4.2.8 (clases del dominio, ER y diccionario del núcleo), 5.1-5.15, 6.4-6.6, 6.9-6.11, 6.13, SoA ISO 27001 y trazabilidad, anexo 10.4, abstract, manual de herramientas (borrador) |

La documentación de Orlando se entrega en PR aparte, uno por bloque, después del código.

## Definition of Done (resumen, [04 §4.8](../../plan/04_scrum_pmbok.md))

- PR a `develop` aprobado por el otro integrante y CI en verde.
- Tests para la lógica nueva y ACL para cada modelo nuevo.
- Textos en español, criterios verificados y capturas o evidencias en `docs/capturas/sprint-3/`.
- Épica marcada en el Project con el enlace al PR (`Parte de #n`; el último PR de la épica cierra con `Closes #n`).

## Pendientes del Sprint 2 que se cierran en este sprint

Vienen de la Retro del S2 y de la Review (ver `docs/scrum/sprint-2/`):

- Decidir si se activa `enforce_admins` en `develop` (Orlando y Evelyn, antes del Gate 0).
- Demo cruzada de una HU ajena (Evelyn una de Orlando y viceversa, antes del Gate 0).
- Cerrar el registro de riesgos (#131) y las Dailies (#132).
- Marcar la checklist de cada épica con el enlace al PR y pasarla a «Hecho» en el Project al fusionar cada HU.
- Pedir la aprobación del otro integrante apenas el CI esté en verde.

## Riesgos y dependencias del sprint

- **El plazo es único** (entrega el viernes 27/11, 14:30) y el Cierre no se toca. Si el sprint se atrasa, la Fase 2 se reduce y queda como trabajo futuro con su diseño.
- **HU-27 antes que HU-28.** k6 y ZAP se corren contra el despliegue con Nginx y TLS; sin HU-27 los resultados no representan el sistema entregado.
- **HU-28 y HU-33 dependen de las dos partes.** Lighthouse y el test de pedido → entrega → factura son de Evelyn; las épicas #142 y #141 se cierran cuando estén ambas partes.
- **Secretos.** `admin_passwd` y los certificados no se suben al repo; los valores de desarrollo quedan en `.env.example`.
- **Cambios de datos `noupdate` y de configuración** (2FA, política de contraseñas) pueden obligar a recrear la base; se avisa a Evelyn antes de fusionar.
- **Gate 0.** Al cumplir los criterios de salida se redacta el informe y no se empieza ningún módulo de la Fase 2 sin la confirmación explícita de Evelyn u Orlando en el chat.
