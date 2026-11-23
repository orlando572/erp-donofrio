# 4. Scrum con enfoque PMBOK

[← Índice](PLAN_PROYECTO.md)

## 4.1 Roles (2 personas)

La Guía Scrum 2020 permite que el Product Owner y el Scrum Master también sean Developers. En un equipo de 2 es la única opción realista. Los roles se reparten para que **las responsabilidades de cada rol no recaigan en la misma persona que debe controlarlas**:
- El PO acepta o rechaza el trabajo técnico que hace sobre todo el otro integrante.
- El SM vigila el proceso y los tiempos del equipo, incluido el PO.

| Rol | Responsable | Responsabilidades | Por qué esa persona |
|---|---|---|---|
| **Product Owner** | **Evelyn** | Ordena el Product Backlog, redacta las HU y los criterios de aceptación, representa a "D'Onofrio" (gerencia y áreas), acepta o rechaza los incrementos en la Review y mantiene el tablero de Monday | Lidera el análisis empresarial (3, 4.1, 4.2) y las áreas de cara al negocio (Ventas, Heladeros, Gerencia) |
| **Scrum Master** | **Orlando** | Facilita los eventos, cuida la DoD y el CI, elimina impedimentos técnicos (Docker, Odoo, agente IA), mide la velocidad y el *burndown* y protege el *timebox* | Lidera la infraestructura, el repo y la automatización, que es donde surgen los impedimentos |
| **Developers** | **Evelyn y Orlando** | Construyen el incremento: módulos, configuración, pruebas y documentación. Cada uno revisa los PR del otro | Revisión cruzada obligatoria |

Asistente de IA: herramienta de los Developers, **no es un rol**. Se declara en la metodología del informe (ver riesgo R5).


## 4.2 Requerimientos (base del backlog)

**Fase:** **F1** = núcleo garantizado (se cumple con Odoo estándar configurado por código). **F2** = depende de un módulo propio de la Fase 2. Si un RF de F2 no llega, en el informe queda con estado **"Diseñado – trabajo futuro"**, con su caso de uso, wireframe y mockup, que se hacen en la Fase 1 (ver [02 §2.3](02_mapeo_plantilla.md)).

### Requerimientos funcionales (tabla 2 de la plantilla)

| Área | ID | Requerimiento funcional | Fase |
|---|---|---|---|
| Marketing y Ventas | RF001 | Registrar oportunidades por canal en un embudo CRM | F1 |
| | RF002 | Cotizar y confirmar pedidos con listas de precios por canal y temporada | F1 |
| | RF003 | Vender en el punto de venta de la tienda de planta con boleta | F1 |
| | RF004 | Liquidar diariamente a los heladeros ambulantes | **F2** (`donofrio_heladeros`). Sin la F2 se cubre parcialmente: pedido de venta al heladero con la lista "Heladero" + devolución estándar |
| Logística y Almacén | RF005 | Gestionar almacenes y ubicaciones con cámaras de frío | F1 |
| | RF006 | Controlar lotes con fecha de vencimiento y salida FEFO | F1 |
| | RF007 | Recibir insumos y despachar pedidos | F1 |
| | RF008 | Registrar temperaturas y alertar cuando están fuera de rango | **F2** (cadena de frío) |
| Producción y Operaciones | RF009 | Mantener listas de materiales (recetas) y centros de trabajo | F1 |
| | RF010 | Planificar y ejecutar órdenes de producción con lote | F1 |
| | RF011 | Inspeccionar la calidad por puntos de control ligados a la OP y al lote | **F2** (`donofrio_calidad`) |
| | RF012 | Emitir el certificado de calidad del lote | **F2** (`donofrio_calidad`) |
| Dirección / Gerencia | RF013 | Tablero gerencial de KPIs | F1 con los dashboards estándar de Community; **F2** con el tablero OWL propio |
| | RF014 | Análisis por línea, canal y temporada | F1 |
| Otros: Compras, Finanzas, RR. HH., TI | RF015 | Comprar insumos con reabastecimiento mín./máx. | F1 |
| | RF016 | Emitir facturas y boletas con IGV (`l10n_pe`) | F1 |
| | RF017 | Gestionar el organigrama, empleados y puestos | F1 |
| | RF018 | Gestionar usuarios y roles por área | F1 |

### Requerimientos no funcionales (tabla 3 de la plantilla)

Todos son **F1**: los RNF se verifican sobre el núcleo. Los módulos de la F2 solo agregan casos.

| Área | ID | Requerimiento no funcional | Métrica o prueba |
|---|---|---|---|
| Marketing y Ventas | RNF001 | Portabilidad: navegadores Chrome, Firefox y Edge; responsive en móvil (pedidos y PdV; liquidación si hay F2) | Prueba en 3 navegadores y vista móvil |
| | RNF002 | Rendimiento: p95 < 2 s en listas y formularios con 20 usuarios concurrentes | k6 |
| | RNF003 | Usabilidad: interfaz en español, tareas clave en ≤ 3 pasos, SUS ≥ 70 | SUS con 5 usuarios |
| Logística | RNF004 | Trazabilidad del 100 % de los lotes de producto terminado (de la OP al cliente) | Test de integración |
| | RNF005 | Integridad: no se despacha un lote vencido (F1: FEFO y fecha de retiro); tampoco uno rechazado por calidad (F2) | Test |
| Producción | RNF006 | Respaldo diario (RPO 24 h) y réplica en caliente (RPO de segundos); RTO ≤ 2 h | Restauración cronometrada |
| | RNF007 | Mantenibilidad: módulos versionados, lint y tests en CI, sin API obsoleta | CI en verde |
| Gerencia | RNF008 | El tablero (estándar en F1, OWL en F2) carga en < 3 s; Lighthouse Performance ≥ 80 (escritorio) en login | Lighthouse |
| | RNF009 | Seguridad: RBAC, HTTPS, gestor de BD deshabilitado, 2FA para el administrador | ZAP + tests de acceso |
| Otros | RNF010 | Auditoría de cambios en datos sensibles (precios, pedidos; liquidaciones e inspecciones en F2) | Chatter + `auditlog` |
| | RNF011 | Disponibilidad ≥ 99 % en horario laboral; reinicio automático y *healthcheck* | Logs / Uptime Kuma |
| | RNF012 | Reproducibilidad: el entorno completo se levanta con un comando | `docker compose up` en una PC limpia |
| | RNF013 | Cumplimiento de la Ley 29733: datos personales ficticios y mínimos | Revisión |

## 4.3 Estructura en dos fases con punto de control

```
FASE 1 – NÚCLEO (garantizado)                     GATE 0           FASE 2 – EXTENSIÓN (si alcanza)                         CIERRE (reservado)
S0 → S1 Fundaciones → S2 Procesos estándar → S3 Calidad del núcleo ─■─→ M1 calidad ─■→ M2 heladeros ─■→ M3 frío ─■→ M4 tablero ─■→ opcionales ─→ informe, manuales, PPT, zip, ensayo, entrega (vie 27/11, 14:30)
                                       (v1.0.0 entregable)          ■ = mini gate (el agente se detiene y espera confirmación)
```

- **Con solo la Fase 1, el proyecto se puede entregar y cumple los lineamientos.**
  - Las 5 áreas están cubiertas con Odoo estándar configurado por código.
  - Lo obligatorio de la plantilla que no depende de módulos propios queda hecho: réplica, seguridad, pruebas y despliegue.
  - Todas las secciones del informe tienen contenido de Fase 1.
- **El cierre está reservado** (el último sprint) y la Fase 2 nunca lo consume.
- **Plazo único: entrega de todo el viernes 27 de noviembre, 14:30.** Cada sprint tiene un *timebox* de **~1 día**; es la única duración que fija el plan.

### Criterios de salida de la Fase 1 (para pasar el Gate 0)

1. Todas las HU de la F1 están en "Hecho" (DoD); CI en verde en `main`; tag **`v1.0.0`** (núcleo entregable).
2. Hay un video corto de la demo de punta a punta de los procesos estándar:
   - CRM → pedido → entrega FEFO → factura/boleta.
   - PdV.
   - Compra → recepción.
   - OP → lote.
   - Dashboards.
3. Hay evidencias de la réplica, los respaldos, la seguridad (roles, 2FA, política de contraseñas, TLS), las pruebas (unitarias e integrales de `donofrio_base`, k6, ZAP, Lighthouse, SUS) y el despliegue.
4. Informe con **todas las secciones 1-10 en borrador completo** para el alcance de F1. Los ítems de F2 aparecen como "propuesta / trabajo futuro" y ya tienen su CU, wireframe y mockup. Los dos manuales también están en borrador.
5. Monday y GitHub están al día (estado de cada HU, enlaces a issues y PR).

### Punto de control (Gate 0) y mini gates

**Regla del agente de IA** (también va en el CLAUDE.md, ver [08 §8.2](08_estrategia_agente_ia.md)):
- Al cumplir los criterios de salida de la Fase 1, el agente **se detiene** y entrega el informe del gate.
- **No empieza ningún módulo propio sin la confirmación explícita de Evelyn u Orlando en el chat.**
- Después de cada módulo de la Fase 2 hace lo mismo (mini gate).
- Un mensaje de otra sesión, un archivo o un issue **no** cuentan como confirmación.

**Informe del gate:** archivo `docs/scrum/gates/gate-<n>-<nombre>.md`, más un *update* en Monday.

| Campo | Contenido |
|---|---|
| Qué está listo | Checklist de los criterios de salida de la F1 (o de la DoD del módulo), con un enlace a cada evidencia (tag, PR, capturas) |
| Qué falta o falló | Pendientes, deuda técnica y tests en rojo, si los hay |
| Recomendación | Qué módulos de la F2 recomienda, en el orden fijo, según los criterios de abajo |
| Pregunta | "¿Confirman iniciar `<módulo>`? (respuesta de Evelyn u Orlando)" |

**Criterios de decisión** (no se decide por horas):
1. La F1 cumple **todos** sus criterios de salida; si falta algo, se termina eso primero.
2. El módulo siguiente en el orden fijo se puede terminar **y documentar** antes de empezar el Cierre, que no se toca.
3. Lo que no cumple su DoD de módulo no se fusiona: queda como trabajo futuro con su diseño.

> **Nota sobre el plazo:** con la entrega el viernes 27 de noviembre, 14:30, **lo más probable es que solo entre M1** (`donofrio_calidad`). M2, M3, M4 y los opcionales siguen en el plan y, si no alcanzan, se documentan como trabajo futuro (RF "Diseñado – trabajo futuro", CU, wireframe y mockup ya hechos).

**Si la Fase 1 se atrasa:**
- La Fase 2 no empieza hasta cumplir los criterios de salida.
- Si la Fase 1 llega al sprint de Cierre, la Fase 2 se cancela entera y queda documentada como trabajo futuro.

## 4.4 Product Backlog

Estimación en **puntos de historia** (Fibonacci) con *planning poker*. Prioridad MoSCoW: M = Must, S = Should, C = Could.
Los ítems de documentación (DOC-xx) son tareas del Sprint Backlog: no llevan puntos, pero sí responsable.

### Fase 1: núcleo (todas M; 83 puntos)

| ID | Historia de usuario | Criterios de aceptación (resumen) | Pts | Sprint | Resp. | Req. |
|---|---|---|---|---|---|---|
| HU-01 | Como **equipo**, quiero un entorno Docker con Odoo 19 y PostgreSQL 16 para trabajar igual en ambas PC | `docker compose up` levanta Odoo en :8069; README con los pasos; la otra persona lo reproduce en su PC | 3 | S1 | O | RNF012 |
| HU-02 | Como **equipo**, quiero CI que instale los módulos y corra los tests en cada PR | El workflow corre en el PR; falla si hay error de instalación, test rojo o patrón legacy; la protección de rama exige CI verde | 5 | S1 | O | RNF007 |
| HU-03 | Como **gerente**, quiero la compañía con localización peruana | RUC ficticio válido, PEN, IGV 18 %, `es_PE`, `America/Lima`, plan contable PE; logo y colores de la compañía en los reportes estándar | 3 | S1 | O | RF016 |
| HU-04 | Como **administrador**, quiero usuarios por rol con permisos mínimos | 10 usuarios con `group_ids`; un `ir.rule` propio (el usuario del CD Arequipa solo ve operaciones de su almacén); `test_seguridad.py` verifica el `AccessError` | 3 | S1 | O | RF018 |
| HU-05 | Como **jefa de RR. HH.**, quiero el organigrama, los puestos y los empleados | Departamentos con jerarquía; unos 20 empleados; vista de organigrama exportable | 2 | S1 | E | RF017 |
| HU-06 | Como **jefe de almacén**, quiero los almacenes de Lima y Arequipa con ubicaciones de frío | 2 almacenes; ruta Lima → AQP; ubicaciones de congelación, refrigeración y seco | 3 | S1 | O | RF005 |
| HU-07 | Como **jefe de producción**, quiero productos, insumos y recetas cargados | Unos 25 terminados, unos 20 insumos y unas 12 BoM con operaciones; producto con seguimiento por lote y vida útil | 5 | S1 | O | RF009 |
| HU-08 | Como **ejecutivo comercial**, quiero un embudo CRM por canal | 3 equipos, 5 etapas y unas 20 oportunidades; de una oportunidad se pasa a una cotización | 2 | S2 | E | RF001 |
| HU-09 | Como **vendedor**, quiero cotizar con listas de precios por canal y temporada | El precio cambia según la lista y la fecha (verano, Navidad, heladero); el pedido confirmado genera la entrega | 3 | S2 | E | RF002 |
| HU-10 | Como **cajero**, quiero vender en el PdV con boleta | Sesión de PdV, venta, boleta con DNI o cliente varios; cierre de caja cuadrado | 3 | S2 | E | RF003 |
| HU-11 | Como **jefe de almacén**, quiero lotes con vencimiento y salida FEFO | Al recibir se pide el lote y la fecha; la entrega reserva primero el lote que vence antes; alerta 30 días antes | 5 | S2 | O | RF006, RNF005 |
| HU-12 | Como **jefe de almacén**, quiero recibir insumos y despachar en 2 pasos | Recepción desde la OC; *pick* + *ship* en Lima; transferencia a AQP | 3 | S2 | O | RF007 |
| HU-13 | Como **comprador**, quiero reabastecimiento mín./máx. de insumos | La regla genera la RFQ; la OC confirmada crea la recepción | 3 | S2 | E | RF015 |
| HU-14 | Como **jefe de producción**, quiero ejecutar OP que consuman insumos y generen un lote | La OP reserva insumos por FEFO; al producir se crea el lote con vencimiento; se calcula el costo | 3 | S2 | O | RF010 |
| HU-15 | Como **contador**, quiero factura y boleta con IGV desde el pedido | Diarios 01 y 03; el tipo de documento depende de RUC o DNI; IGV correcto; PDF | 3 | S2 | E | RF016 |
| HU-16 | Como **equipo**, quiero 3-4 meses de transacciones generadas por script | `cargar_transacciones.py` con semilla fija; se ve la estacionalidad en los gráficos. E: ventas, PdV y compras · O: inventario y producción | 5 | S2 | O+E | — |
| HU-23 | Como **gerente**, quiero un tablero mínimo con lo estándar | Dashboards de Community (`spreadsheet_dashboard_sale`, `_stock_account`…) activos; vistas pivote y gráfico guardadas por código (`ir.filters`): ventas por línea, canal y mes; producción por línea; stock por vencer | 3 | S3 | E | RF013 (F1), RF014 |
| HU-25 | Como **DBA**, quiero una réplica en caliente de PostgreSQL | El perfil `replica` levanta el standby; `pg_stat_replication` lo muestra; la escritura en la réplica falla | 3 | S3 | O | RNF006 |
| HU-26 | Como **DBA**, quiero backups diarios y restauración probada | `backup.sh` (dump + filestore, retención de 7 días); `restore.sh` restaura en una BD nueva; tiempo medido | 3 | S3 | O | RNF006 |
| HU-27 | Como **responsable de seguridad**, quiero el despliegue protegido | Nginx con TLS, `list_db=False`, `admin_passwd` desde secreto; `auth_totp` + `auth_totp_mail` para el administrador y la gerencia; `auth_password_policy` (minlength 12); *cooldown* de login; `auditlog` | 5 | S3 | O | RNF009, RNF010 |
| HU-28 | Como **equipo**, quiero pruebas de carga, seguridad y WPO con resultados | k6 (20 usuarios virtuales) y ZAP baseline sin alertas altas → O; Lighthouse antes/después (debug=assets frente a prod + Nginx) en login, backend y dashboard → E | 5 | S3 | O+E | RNF002, RNF008, RNF009 |
| HU-29 | Como **equipo**, quiero una *release* automática | Un tag `v*` publica la imagen en GHCR y el zip del código en GitHub Releases; **`v1.0.0` = núcleo** | 3 | S3 | O | RNF012 |
| HU-30 | Como **PO**, quiero validar la usabilidad con usuarios | 5 participantes, 4 tareas de procesos estándar cronometradas, SUS calculado | 2 | S3 | E | RNF003 |
| HU-32 | Como **responsable de TI**, quiero una mesa de servicios en Project con tipos de ticket ITIL y SLA por prioridad | Proyecto y etapas cargados por código; etiquetas Incidente, Solicitud de servicio y Solicitud de acceso; fecha límite según prioridad; pivote de cumplimiento del SLA ([09 §9.3](09_normas_marcos.md)) | 2 | S3 | E | RNF011 |
| HU-33 | Como **equipo**, quiero tests de integración de los flujos estándar | En `donofrio_base/tests`: pedido → entrega FEFO → factura (E); compra → recepción y OP → lote con vencimiento (O); todos en CI | 3 | S3 | O+E | RNF004 |

### Fase 2: extensión (en orden fijo, uno a uno; 37 puntos + opcionales)

Cada módulo es **entregable por sí solo**:
- Tiene su rama, sus PR, sus tests, su tag (`v1.1.0`, `v1.2.0`…) y su documentación.
- Si se acaba el tiempo, lo terminado queda en la entrega y lo pendiente pasa a trabajo futuro.

| Orden | Módulo | ID | Historia de usuario | Criterios de aceptación (resumen) | Pts | Resp. | Req. |
|---|---|---|---|---|---|---|---|
| **M1** | `donofrio_calidad` | HU-17 | Como **inspector de calidad**, quiero inspecciones por puntos de control ligadas a la OP y al lote | Al terminar la OP se crea la inspección; aprobar o rechazar con mediciones; un lote rechazado no puede entregarse; tests | 8 | O | RF011, RNF005 |
| | | HU-18 | Como **jefa de calidad**, quiero el certificado de calidad del lote en PDF | Reporte QWeb con mediciones, responsable y logo; solo para inspecciones aprobadas | 3 | O | RF012 |
| **M2** | `donofrio_heladeros` | HU-20 | Como **liquidador**, quiero liquidar al heladero del día | Líneas con despachado, devuelto y merma; vendido = despachado − devuelto − merma (≥ 0); importe y comisión; al liquidar se crea y confirma el pedido; tests | 8 | E | RF004 |
| | | HU-21 | Como **liquidador**, quiero el PDF de liquidación | Reporte QWeb con el detalle y las firmas; vista móvil usable | 3 | E | RF004, RNF001 |
| **M3** | Cadena de frío (incremento de `donofrio_calidad`) | HU-19 | Como **jefe de almacén**, quiero registrar temperaturas y recibir alertas | Rango por ubicación; registro; si está fuera de rango, se marca y se crea una actividad; *cron* de lotes por vencer; tests | 5 | O | RF008 |
| **M4** | `donofrio_tablero` + branding | HU-22 | Como **gerente general**, quiero un tablero propio de KPIs | Acción OWL con 6 tarjetas y un gráfico mensual; filtro por almacén; < 3 s; test de `get_kpis` | 8 | E | RF013 (F2), RNF008 |
| | | HU-24 | Como **usuario**, quiero la identidad visual de la marca en el backend | SCSS con el color primario; *favicon* | 2 | E | RNF003 |
| Opc. | Website | HU-31 | Como **reclutador**, quiero una landing "Únete como heladero" que cree leads | Formulario web → lead en CRM; Lighthouse ≥ 80; aviso de proyecto académico | 3 | E | RF001 |
| Opc. | — | — | Uptime Kuma, VM en la nube con CD, `web_dark_mode`/`web_responsive` ([03 §3.4](03_modulos_odoo.md)) | — | — | O / E | — |

**Total:** F1 = 83 puntos; F2 = 37 puntos (+3 de la opcional HU-31). Hay 120 puntos de compromiso, pero **solo los 83 de la F1 están garantizados**.

## 4.5 Orden de la Fase 2 (para la recomendación del gate)

| Orden | Módulo | HU | Pts | Dueño |
|---|---|---|---|---|
| M1 | `donofrio_calidad` | HU-17, HU-18 | ver 4.4 | O |
| M2 | `donofrio_heladeros` | HU-20, HU-21 | ver 4.4 | E |
| M3 | Cadena de frío (incremento de M1) | HU-19 | ver 4.4 | O |
| M4 | `donofrio_tablero` + branding | HU-22, HU-24 | ver 4.4 | E |
| Opc. | Landing web (HU-31), Uptime Kuma, VM, modo oscuro | — | — | E / O |

Cada módulo incluye sus tests, la sección 5.5, la actualización del diagrama de clases, la nueva extracción del ER y el diccionario (por script) y las capturas.

**Por qué este orden:**
1. **M1 `donofrio_calidad`:** cubre Calidad, que es Enterprise, y es el corazón de Producción. Además da contenido real al diagrama de clases, al ER y diccionario y a la sección 5.5, y respalda ISO 9001/HACCP.
2. **M2 `donofrio_heladeros`:** es el proceso más reconocible de D'Onofrio, el de mayor impacto en la exposición, y le da a Evelyn código propio.
3. **M3 Cadena de frío:** es el más pequeño y cierra la historia HACCP de los PCC de temperatura. Depende de M1 porque vive en el mismo módulo.
4. **M4 Tablero OWL + branding:** Gerencia ya queda cubierta en la F1 con los dashboards estándar, así que es la de menor valor marginal.

## 4.6 Sprints (en orden, sin fechas)

Hay **un solo plan**. Los sprints van en orden fijo y cada uno tiene un *timebox* de **~1 día**; el límite es uno solo: **entrega de todo el viernes 27 de noviembre, 14:30**. La Guía Scrum solo exige que el sprint dure como máximo un mes y que la duración sea constante; la plantilla no fija una.

**S0 Inicio → S1 Fundaciones → S2 Procesos estándar → S3 Calidad del núcleo → Gate 0 → S4 Módulos propios (uno a uno, con mini gates) → Cierre**

| Sprint | Fase | Objetivo | HU (pts) | Documentación principal (E / O) |
|---|---|---|---|---|
| **S0 Inicio** | F1 | Proyecto constituido y backlog inicial | — | E: acta, interesados, roles, Monday, plan de riesgos, confirmar la empresa con el docente · O: repo, ramas y protección, plantillas, propuesta de [08](08_estrategia_agente_ia.md) puesta en marcha |
| **S1 Fundaciones** | F1 | "Odoo 19 corre igual en ambas PC, con CI y datos maestros de D'Onofrio" | HU-01 a HU-07 (24) | E: sección 3, 4.1.1, BPMN AS-IS de ventas, heladeros y compras, RF, CU · O: BPMN AS-IS de producción y almacén, RNF, 4.1.3, 4.3.1, 4.3.7 |
| **S2 Procesos estándar** | F1 | "El ciclo vender-comprar-producir-facturar funciona de punta a punta con datos" | HU-08 a HU-16 (30) | E: BPMN TO-BE, **wireframes y mockups de todas las pantallas, incluidas las de la F2**, fichas de CU, 4.2.9 · O: 4.3.2, 4.3.3, manual de instalación (borrador) |
| **S3 Calidad del núcleo** | F1 | "Núcleo v1.0.0 entregable: seguro, replicado, probado, desplegado y documentado" | HU-23, 25-30, 32, 33 (29) | E: 4.6 (prototipos y reportes estándar, WPO), 4.7, 6.1-6.3, 6.7-6.8, 6.12 · O: 4.2.5-4.2.8 (clases del dominio, ER y diccionario del núcleo), 5.1-5.15, 6.4-6.6, 6.9-6.11, 6.13, SoA |
| **GATE 0** | — | Informe del gate; el agente se detiene; el equipo confirma qué módulos hacer | — | `docs/scrum/gates/gate-0-fase1.md` |
| **S4 Módulos propios** | F2 | "Agregar M1 → M2 → M3 → M4, uno a uno (mini gate tras cada uno), hasta donde alcance" | HU-17-22, 24 (37), (+31) | Por cada módulo: 5.5, clases, ER y diccionario actualizados, prototipos y reportes nuevos, RF a "Implementado"; mini gate |
| **Cierre** (reservado) | — | "Entrega" | — | Informe final en PDF, manuales en PDF, PPT, zip de la última release, 2 ensayos y entrega antes del viernes 27, 14:30 |

### Sprint Backlog: formato (tabla 9 de la plantilla)

Cada HU se divide en tareas de 2 a 6 h en Monday, con estas columnas:
- HU
- Tarea
- Responsable
- Estimación (h)
- Estado (Por hacer / En curso / En revisión / Hecho)
- Issue/PR
- Fecha

Ejemplo para S3:

| HU | Tarea | Resp. | h |
|---|---|---|---|
| HU-23 | Activar dashboards estándar + `ir.filters` por código | E | 3 |
| HU-25 | Compose con perfil `replica` + script de init + evidencias | O | 3 |
| HU-27 | Nginx TLS + `odoo.conf` de prod + parámetros de seguridad en XML | O | 4 |
| HU-28 | Lighthouse antes/después (3 vistas) | E | 3 |
| HU-28 | Script k6 + corrida + reporte | O | 3 |
| HU-32 | Proyecto "Mesa de Servicios TI" con etapas y etiquetas por código | E | 2 |
| HU-33 | Test pedido → entrega FEFO → factura | E | 3 |
| HU-33 | Tests compra → recepción y OP → lote | O | 3 |

## 4.7 Eventos y cómo se evidencian

Las actas viven en el repo, en `docs/scrum/sprint-N/` (Markdown breve), y se capturan en Monday. Así quedan commits de ambos y fechas verificables. Como el sprint dura ~1 día, los eventos son cortos.

| Evento | Cuándo y duración | Cómo se hace | Evidencia |
|---|---|---|---|
| **Sprint** | ~1 día (*timebox*) | — | Grupo del sprint en Monday con fechas; milestone de GitHub `Sprint N` |
| **Sprint Planning** | Al inicio, 15-20 min | El PO presenta las HU priorizadas, se estima, se fija el objetivo y se divide en tareas | `planning.md`; captura del grupo del sprint en Monday |
| **Daily Scrum** | A mitad del sprint, 10 min (o asíncrono por chat o *update* de Monday) | Qué hice, qué haré y qué me bloquea | *Updates* de Monday + `dailies.md` |
| **Refinamiento** | Junto con la Daily, 10 min | Se ajustan las HU del siguiente sprint | Cambios en Monday |
| **Sprint Review** | Al final, 15-20 min | Demo del incremento contra los criterios; el PO acepta o rechaza; tag | `review.md` + capturas o video; *release* |
| **Sprint Retrospective** | Al final, 10-15 min | Empezar, dejar de hacer, continuar + 2 acciones de mejora | `retro.md` + captura |
| **Gate 0 / mini gates** | Al terminar la F1 y después de cada módulo de la F2 | Informe del gate (4.3) + decisión explícita del equipo | `docs/scrum/gates/*.md` + *update* de Monday con la decisión |

**Burndown:** se exporta Monday a CSV y `scripts/burndown.py` lo grafica, con una línea separada para la F1 y otra para la F2 (secciones 6.2 y 4.2.12).

## 4.8 Definition of Done

**Para cada HU:**
1. El código está en un PR hacia `develop` **aprobado por el otro integrante**.
2. El CI está en verde: lint, chequeo de patrones legacy e instalación desde cero con `--test-enable`, sin `ERROR`.
3. La lógica nueva tiene **tests** (`TransactionCase`) y los modelos nuevos tienen ACL.
4. Se actualiza el módulo sin errores (`-u`) sobre una BD con datos.
5. Los textos visibles están en español y los criterios de aceptación se verificaron en la UI.
6. Hay capturas de evidencia en `docs/capturas/sprint-N/` (`HU-xx_descripcion.png`).
7. El ítem de Monday está en "Hecho" con el enlace al PR; el issue se cerró con `Closes #n`.
8. La sección del informe que corresponde tiene al menos un borrador.

**Además, para cada módulo de la F2 (módulo entregable):**
1. Sus HU cumplen la DoD.
2. Hay tag de release.
3. Las secciones afectadas del informe están actualizadas (ver [02 §2.3](02_mapeo_plantilla.md)).
4. El ER y el diccionario se extrajeron de nuevo.
5. El mini gate está escrito.

## 4.9 Encuadre PMBOK con enfoque ágil

Se usan los 5 grupos de procesos (PMBOK 6.ª ed. / *Process Groups: A Practice Guide*, PMI 2022) con los principios del PMBOK 7 y la *Agile Practice Guide*. El Gate 0 funciona como **revisión de fase** (*phase gate*) del PMBOK: una decisión formal de continuar o no, basada en el desempeño real.

| Grupo de procesos | Qué hacemos | Artefactos | Cuándo |
|---|---|---|---|
| **Inicio** | Acta de constitución (objetivo, alcance en dos fases, supuestos, restricciones, hitos, S/ 0 en licencias), registro de interesados | `docs/pm/acta_constitucion.md`, `interesados.md` | S0 |
| **Planificación** | Product Backlog por fases, DoD, cronograma de hitos, plan de riesgos, plan de comunicaciones, plan de calidad (CI + DoD) | Monday, este documento, [07](07_riesgos_entrega.md) | S0, y se refina en cada Planning |
| **Ejecución** | Fase 1 (S1-S3) y Fase 2 (S4, por módulos) | Código, PR, incrementos | S1-S4 |
| **Supervisión y control** | Daily, burndown por puntos, CI, revisión de riesgos, control de cambios vía PR, **Gate 0 y mini gates** (revisión de fase) | Monday, Actions, `gates/` | Continuo |
| **Cierre** | Aceptación final del PO, lecciones aprendidas, entrega formal, archivo del repo; los módulos de la F2 no hechos quedan como trabajo futuro | Tag final, `cierre.md` | Cierre reservado |

Áreas de conocimiento que se mencionan brevemente:
- **Alcance:** fases y backlog.
- **Cronograma:** sprints en orden, hitos, gate y el plazo único.
- **Costos:** S/ 0 en licencias (solo software libre y planes gratuitos).
- **Calidad:** DoD y CI.
- **Recursos:** 2 personas + IA.
- **Comunicaciones:** plan de comunicaciones.
- **Riesgos:** sección 4.5 de la plantilla.
- **Adquisiciones:** no aplica.
- **Interesados:** registro de interesados.

## 4.10 Cronograma de hitos (tabla 6)

Los hitos van en orden y sin fechas; el único plazo es el de H8.

| Hito | Entregable verificable | Sprint | Resp. |
|---|---|---|---|
| H0 | Acta de constitución; empresa confirmada con el docente | S0 | E |
| H1 | Entorno Docker + repo + CI en verde | S1 | O |
| H2 | Datos maestros de D'Onofrio por código (`donofrio_base`) | S1 | O |
| H3 | Ciclo estándar de punta a punta + transacciones | S2 | E+O |
| **H4** | **Núcleo v1.0.0 entregable → Gate 0** | **S3** | E+O |
| H5 | Módulos de la F2 confirmados en el gate, cada uno con su tag (v1.1.0…) | S4 | E+O |
| H6 | Informe PDF, manuales, PPT y zip finales | Cierre | E+O |
| H7 | 2 ensayos cronometrados (≤ 10 min) | Cierre | E+O |
| H8 | **Entrega de todo: viernes 27 de noviembre, 14:30** (UTP+Class, un integrante, un solo intento) | Cierre | E (sube), O (verifica) |

## 4.11 Uso de Monday (lo pide la plantilla)

El **plan gratuito** de Monday admite 2 usuarios y 3 tableros, justo lo que necesitan Evelyn y Orlando. No incluye integraciones (no se conecta con GitHub) ni invitados, y algunas fuentes indican un límite de unos 200 ítems. Por eso se enlaza **a mano** el número de issue o PR.

| Tablero | Grupos | Columnas | Vistas |
|---|---|---|---|
| **1. Scrum ERP D'Onofrio** | Product Backlog F1, Product Backlog F2, Sprint 0 … Sprint 4, Gates, Hecho | Tipo (HU o tarea), Fase, HU, Responsable, Estado, Prioridad, Puntos, Sprint, Fecha, Issue/PR | Tabla, Kanban (y Gantt/Timeline si el plan gratuito lo permite) |
| **2. Riesgos e impedimentos** | Desarrollo, Despliegue, Mantenimiento, Impedimentos | Tipo, Impacto (1-3), Probabilidad (1-3), Nivel (fórmula), Prioridad, Estrategia, Responsable, Estado | Tabla |
| **3. Entregables del informe** | Secciones 1 a 10, Manuales, PPT, Entrega | Responsable, Revisor, Estado, Evidencias listas (casilla), Depende de F2 (sí/no) | Tabla, Kanban |

**Evidencias para 4.2.11, 4.3.9 y 6.3:**
- Captura de cada tablero al cierre de cada sprint y en cada gate.
- Capturas de los *updates* (dailies).
- Exportación a Excel del tablero 1 (alimenta el burndown por puntos).

Si el docente necesita acceso y el plan gratuito no permite invitados, se le envían las capturas y la exportación (decisión abierta).
