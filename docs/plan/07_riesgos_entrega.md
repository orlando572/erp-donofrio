# 7. Riesgos del proyecto y checklist de entrega

[← Índice](PLAN_PROYECTO.md)

## 7.1 Riesgos del proyecto

Escalas de la plantilla:
- Impacto (I) y Probabilidad (P) van de 1 a 3.
- **Nivel = I × P**.
- Prioridad: **Alta** si el nivel es 6-9 (acción inmediata), **Media** si es 3-5 (seguimiento constante), **Baja** si es 1-2 (monitoreo).

Estos riesgos se registran como issues con la etiqueta `riesgo` (vista "Riesgos" del GitHub Project) y se revisan en cada Planning y Retro.

| Id | Tipo | Riesgo | I | P | Nivel | Prio | Estrategia | Resp. |
|---|---|---|---|---|---|---|---|---|
| R1 | Externo | **Plazo muy corto: todo se entrega el viernes 27 de noviembre, 14:30** (el "18 de julio, 07:00" del PDF es un dato de la plantilla) | 3 | 3 | 9 | Alta | **Mitigar:** sprints con *timebox* de ~1 día en orden fijo ([04 §4.6](04_scrum_pmbok.md)); la Fase 1 garantiza un entregable aunque la Fase 2 no alcance; Gate 0 por criterios; Cierre reservado; lo más probable es que de la F2 solo entre M1 | E |
| R2 | Técnico | El agente de IA o tutoriales viejos generan **API obsoleta de Odoo** (`attrs`, `<tree>`, `_sql_constraints`…) que rompe la instalación | 3 | 3 | 9 | Alta | **Mitigar:** código fuente 19.0 local, ficha de cambios, hook que bloquea, `check_legacy` en CI, instalación con tests en cada PR ([08](08_estrategia_agente_ia.md)) | O |
| R3 | Organizacional | **Otro grupo elige la misma empresa** (prohibido por la regla 10) | 3 | 2 | 6 | Alta | **Evitar:** confirmar D'Onofrio con el docente en S0; alternativa de respaldo: otra empresa de consumo masivo | E |
| R4 | Humano | **Carga desigual** o un integrante no puede defender su parte (la nota también es individual) | 3 | 2 | 6 | Alta | **Mitigar:** reparto por áreas de punta a punta, revisión cruzada de todos los PR, demos cruzadas en la Review, 2 ensayos | E+O |
| R5 | Organizacional | **Uso de IA no declarado** se interpreta como plagio (regla 11) | 3 | 2 | 6 | Alta | **Evitar:** declarar en la metodología el uso del asistente de IA y la verificación humana; todo el contenido revisado y entendido por quien lo firma; citar las fuentes | E+O |
| R6 | Técnico | Un módulo OCA o una funcionalidad necesaria no está en Community 19 (pasó con `quality_control_mrp_oca` y el EDI) | 2 | 3 | 6 | Alta | **Aceptar o mitigar:** módulo propio pequeño; limitación declarada para EDI y nómina | O |
| R7 | Técnico | **PC con poca RAM** para Odoo, PostgreSQL, réplica y Nginx | 2 | 2 | 4 | Media | **Mitigar:** perfiles de Compose; la réplica y las herramientas solo se levantan para las evidencias | O |
| R8 | Técnico | **Pérdida de trabajo** (disco, rama borrada, BD corrupta) | 3 | 1 | 3 | Media | **Mitigar:** push diario, ramas protegidas, BD reproducible por código, `backup.sh` | O |
| R9 | Externo | **Falla la subida única** a UTP+Class (tamaño, formato, hora o conexión) | 3 | 2 | 6 | Alta | **Mitigar:** generar los PDF y el zip al inicio del Cierre; revisar el límite de tamaño; subir con margen antes del viernes 27, 14:30; checklist de 7.2 | E |
| R10 | Externo | **Cambia el escenario Froneri** antes de la entrega (noticias nuevas) | 1 | 2 | 2 | Baja | **Aceptar:** la fecha de corte de 2026 está declarada; se actualiza solo el párrafo del entorno | E |
| R11 | Legal/ético | Uso de marca, logo o identidad real (**impersonación**) si se publica una web o un RUC real | 2 | 2 | 4 | Media | **Evitar:** RUC ficticio, aviso de "proyecto académico, no afiliado", sitio con `noindex`, repo sin PDF del docente | E |
| R12 | Organizacional | La plantilla nombra Monday (6.3 "Resumen del Monday") y se usa GitHub Projects | 1 | 2 | 2 | Baja | **Mitigar:** nota de reemplazo bajo el título con su justificación ([04 §4.11](04_scrum_pmbok.md)) y aviso al docente | E |
| R13 | Humano | La **exposición pasa de 10 minutos** y se corta | 2 | 2 | 4 | Media | **Mitigar:** guion cronometrado, punto de corte a los 8:30, video de respaldo | E+O |
| R14 | Técnico | La demo en vivo falla (Docker, red, datos) | 3 | 2 | 6 | Alta | **Mitigar:** BD de demo pre-cargada y respaldada, video grabado, PC probada el día anterior | O |
| R15 | Organizacional | La documentación se deja para el final y no da el tiempo | 3 | 2 | 6 | Alta | **Evitar:** la DoD exige un borrador de la sección por HU; vista "Entregables del informe" del Project con un issue por sección; el Gate 0 exige el informe completo en borrador para el alcance de la F1 | E |
| R16 | Técnico | La evidencia de Scrum se concentra en pocos días (commits todos juntos) | 2 | 2 | 4 | Media | **Mitigar:** commits pequeños y diarios de ambos, sprints con fechas reales, actas fechadas | O |
| R17 | Organizacional | **La Fase 2 se come el tiempo del cierre** o la entrega queda con un módulo a medias | 3 | 2 | 6 | Alta | **Evitar:** Gate 0 y mini gates por criterios (F1 completa; el módulo se termina y documenta antes del Cierre); cierre reservado que la F2 no puede usar; orden fijo M1 → M4; lo inconcluso no se fusiona y se documenta como trabajo futuro | O (criterios), E (decisión) |
| R18 | Técnico | El agente de IA **sigue con la Fase 2 sin autorización** después del gate | 2 | 2 | 4 | Media | **Evitar:** la regla del gate en el CLAUDE.md; solo vale la confirmación explícita en el chat de Evelyn u Orlando; los PR de la F2 requieren revisión humana | O |
| R19 | Humano | Sin Fase 2, un integrante se queda **sin código propio que defender** | 2 | 2 | 4 | Media | **Mitigar:** desde la F1, cada uno es dueño de sus archivos de datos, tests y configuración en `donofrio_base` ([05 §5.1](05_reparto_equipo.md)) | E+O |
| R20 | Humano | **Fatiga** por el ritmo de un sprint por día: errores y retrabajo | 2 | 2 | 4 | Media | **Mitigar:** dailies cortas, revisión cruzada obligatoria, CI como red de seguridad, Cierre sin desarrollo | E+O |

**R2, R17 y R18** se revisan en cada gate.

Las tablas 11-13 de la plantilla (riesgos por etapa del software: desarrollo, despliegue y mantenimiento) se construyen a partir de esta tabla, con riesgos técnicos del sistema. Por ejemplo:
- Desarrollo: R2 y R6.
- Despliegue: migración fallida de un módulo (`-u`), secretos expuestos, puerto del gestor de BD abierto.
- Mantenimiento: backups no probados, disco lleno, lotes vencidos por *cron* caído.

Cada tabla agrega:
- Seguimiento: en cada sprint, en el GitHub Project.
- Validación: el PO valida y ambos revisan.

## 7.2 Checklist final de entrega

### Entregables (apartado 7 del lineamiento)

- [ ] **a. Informe final (PDF)** sobre la plantilla del docente, sin texto de ejemplo; secciones 1-10; índices actualizados; leyendas numeradas; APA 7; historial de revisiones lleno
- [ ] **b. Manual de instalación y configuración del proyecto (PDF)**: requisitos, clonar, `.env`, `docker compose up`, `init_db.sh`, carga de transacciones, usuarios de prueba, perfiles (réplica, proxy), backup y restauración, actualización de módulos, solución de problemas
- [ ] **c. Manual de instalación y configuración de las herramientas (PDF)**: Docker, Git, VS Code, DBeaver, SchemaSpy, bpmn.io/Camunda Modeler, draw.io, PlantUML, Lighthouse, k6, OWASP ZAP, GitHub (Actions, GHCR, Projects y la CLI `gh` con el permiso `project`), asistente de IA
- [ ] **d. Material audiovisual (PPTX o PDF)** para 10 minutos + video de respaldo de la demo
- [ ] **e. Enlace al repositorio** (público o con acceso del docente) que muestre el 100 % de la construcción: releases, Actions, issues, PR
- [ ] **f. Código fuente comprimido** (`erp-donofrio-v1.0.0.zip` de la Release) con un README de indicaciones y especificaciones

### Reglas

- [ ] **Lo sube un solo integrante** (Evelyn) y **solo hay un intento**: verificar los archivos uno por uno antes de enviar (Orlando hace de segundo par de ojos)
- [ ] **Entrega de todo: viernes 27 de noviembre, 14:30** (único límite), por el enlace de UTP+Class que indique el docente. Subir con margen. El "18 de julio, 07:00" del PDF es un dato de la plantilla, no el plazo
- [ ] **Formato PDF** para los documentos; zip para el código
- [ ] **Empresa no repetida** entre grupos (confirmado con el docente en S0)
- [ ] Sin plagio: fuentes citadas y uso de IA declarado
- [ ] Vestimenta formal para la sustentación; tiempo ≤ 10 min ensayado

### Estado de las fases

- [ ] Gate 0 y mini gates archivados en `docs/scrum/gates/`, con la decisión del equipo
- [ ] La entrega corresponde a la **última release que cumplió su DoD** (`v1.0.0` como mínimo); nada a medias en `main`
- [ ] Las secciones de la [§2.3](02_mapeo_plantilla.md) reflejan los módulos de la F2 realmente terminados. Los no terminados aparecen como "Diseñado – trabajo futuro" en los RF, CU, clases y recomendaciones, y la PPT usa la variante correcta

### Verificación técnica previa (H6-H7)

- [ ] Clonar el repo en una carpeta limpia → `docker compose up` → `init_db.sh` → todo funciona siguiendo **solo el manual**
- [ ] CI en verde en `main`; tag `v1.0.0` (y los de la F2 alcanzados) publicado; el zip corresponde al último tag
- [ ] Capturas de todas las secciones en `docs/capturas/` y en el informe
- [ ] ER, diccionario y diagrama de clases coinciden con la versión final de los módulos
- [ ] Los números del informe (pruebas, Lighthouse, k6, SUS, burndown) coinciden con las evidencias
- [ ] Cada fila de la tabla de trazabilidad norma → evidencia ([09 §9.9](09_normas_marcos.md)) tiene su captura, archivo o commit, y el informe dice "alineación, no certificación"

Nombres de archivo sugeridos:
- `G<N>_InformeFinal_ERP_DOnofrio.pdf`
- `G<N>_ManualProyecto.pdf`
- `G<N>_ManualHerramientas.pdf`
- `G<N>_Presentacion.pdf`
- `G<N>_CodigoFuente_v1.0.0.zip`
