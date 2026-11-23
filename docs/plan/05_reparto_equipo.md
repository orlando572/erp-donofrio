# 5. Reparto del trabajo: Evelyn y Orlando

[← Índice](PLAN_PROYECTO.md)

## 5.1 Criterio de reparto

El reparto es **por áreas de negocio completas, de punta a punta**: proceso BPMN → requerimientos → caso de uso → configuración o código → pruebas → sección del informe → parte de la exposición. Así cada persona puede defender su parte en la sustentación individual sin depender de la otra.

**Regla de las fases:** la parte defendible de cada integrante **no puede depender de la Fase 2**. Por eso los dos tienen código propio ya en la Fase 1:
- Evelyn: los archivos de datos de su área en `donofrio_base`, los tests del flujo de venta, los `ir.filters` de gerencia y la mesa de servicios.
- Orlando: la estructura y los hooks de `donofrio_base`, seguridad, infraestructura, CI y los tests de inventario y producción.

| | **Evelyn** (Product Owner + Developer) | **Orlando** (Scrum Master + Developer) |
|---|---|---|
| Áreas de negocio | **Marketing y Ventas** (CRM, Ventas, PdV, heladeros), **Gerencia**, **Extras administrativos** (Compras, Facturación `l10n_pe`, RR. HH., mesa de servicios TI) | **Logística** (almacenes, lotes, FEFO, cadena de frío), **Producción y Operaciones** (MRP, calidad), configuración base y seguridad |
| Código de la Fase 1 | `donofrio_base/data/` de ventas, CRM, PdV, compras, facturación, RR. HH., `ir.filters` y Project; parte de ventas y compras de `cargar_transacciones.py`; test pedido → entrega → factura | Estructura, hooks y `post_init_hook` de `donofrio_base`; datos de almacén, productos, BoM, usuarios, `ir.rule` y seguridad; parte de inventario y producción del script; tests de seguridad, compra y OP; Docker, CI/CD, réplica, Nginx |
| Módulos de la Fase 2 (dueño) | **M2** `donofrio_heladeros`, **M4** `donofrio_tablero` + branding, opcionales 5 y 8 | **M1** `donofrio_calidad`, **M3** cadena de frío, opcionales 6 y 7 |
| Gestión y negocio | Análisis empresarial (3, 4.1), Scrum y GitHub Projects (4.2.9-4.2.12, 6.1-6.3), **informes de gate (redacción con los datos del agente)**, riesgos de desarrollo, SLA/KPIs (4.7), cascada COBIT, prácticas ITIL | Arquitectura e infraestructura (4.1.3, 4.3), riesgos de despliegue y mantenimiento, **verificación de los criterios de salida del gate**, SoA ISO 27001 y trazabilidad |
| Front / Back | Front-end: prototipos, wireframes y mockups (**incluidos los de las pantallas de la F2**), UI/UX, WPO (4.4, 4.6) | Back-end y BD: clases, ER, diccionario, replicación, administración, seguridad y despliegue (4.2.5-4.2.8, 5) |
| Pruebas | Funcionales de su área, usabilidad (SUS), Lighthouse | Funcionales de su área, unitarias e integrales en CI, carga (k6), seguridad (ZAP) |
| Repo y CI | Revisa los PR de Orlando; issues y commits (6.7, 6.8); responsable de sus épicas y de los issues "Constitución", "Registro de riesgos", "Gate 0" e "Informe final" ([04 §4.11](04_scrum_pmbok.md)) | Workflows, ramas y merge (6.4-6.6); revisa los PR de Evelyn; responsable de sus épicas (incluidas "Transacciones" y "Pruebas", compartidas) y de los issues "Repo", "Dailies" y "Entrega" |
| Entregables | Informe (maquetación final en Word), PPT, **sube la entrega** | Manual de instalación, manual de herramientas, zip de la última release, **verifica la entrega** |

**Equilibrio:**
- **Fase 1:** Orlando lleva unos 53 puntos de código e infraestructura. Evelyn lleva unos 30 puntos más la mayor parte de la documentación de negocio y gestión, que en esta plantilla pesa más que el código. Con la documentación, el esfuerzo de cada uno queda parejo.
- **Fase 2:** reparto parejo: O tiene M1 + M3 y E tiene M2 + M4. Se revisa en cada gate. Si solo entra M1 (lo más probable con el plazo), Evelyn documenta M1 y prepara su demo mientras Orlando lo construye.

**Regla de conocimiento cruzado** (para la nota individual):
- Cada uno revisa **todos** los PR del otro.
- En cada Review, la otra persona hace la demo de una HU ajena.
- Antes de la exposición, cada uno debe poder ejecutar `docker compose up` y explicar la arquitectura general.

## 5.2 Tareas por persona: Fase 1

| Sprint | Evelyn | Orlando |
|---|---|---|
| **S0** | Acta de constitución, interesados, roles, el GitHub Project "Scrum ERP D'Onofrio" (campos y vistas de [04 §4.11](04_scrum_pmbok.md)), backlog por fases, plan de riesgos, confirmar con el docente que la empresa no se repite | Repo, ramas `main`/`develop` con protección, plantillas de issue y PR, etiquetas y milestones; poner en marcha la propuesta de [08](08_estrategia_agente_ia.md): fuentes 19.0, CLAUDE.md con la regla del gate, ficha y hook |
| **S1** | HU-05 (RR. HH.); secciones 3.1-3.7; 4.1.1; BPMN AS-IS de ventas, heladeros y compras; tabla RF (con columna de fase); CU de ventas, heladeros y gerencia | HU-01, 02, 03, 04, 06, 07; BPMN AS-IS de producción y almacén; tabla RNF; 4.1.3; 4.3.1; 4.3.7 |
| **S2** | HU-08, 09, 10, 13, 15, HU-16 (parte de ventas y compras); BPMN TO-BE de su área (heladeros: TO-BE mínimo estándar y TO-BE con M2); **wireframes y mockups de todas las pantallas, incluidas las de la F2**; fichas de CU; 4.2.9 | HU-11, 12, 14, HU-16 (parte de inventario y producción); BPMN TO-BE de su área (calidad: con y sin M1); fichas de CU; 4.3.2; 4.3.3; manual de instalación (borrador) |
| **S3** | HU-23, 30, 32, HU-28 (Lighthouse), HU-33 (test de venta); 4.6 (prototipos y reportes estándar, WPO); 4.7; 6.1-6.3, 6.7, 6.8, 6.12; cascada COBIT, ITIL, anexos 10.3 y 10.5; resumen y conclusiones en borrador | HU-25, 26, 27, 29, HU-28 (k6, ZAP), HU-33 (tests de compra y OP); 4.2.5-4.2.8 (núcleo); 5.1-5.15; 6.4-6.6, 6.9-6.11, 6.13; SoA y trazabilidad; anexo 10.4; abstract; manual de herramientas (borrador) |
| **Gate 0** | Redacta el informe del gate y lleva la decisión como PO | Verifica los criterios de salida de la F1 y adjunta las evidencias |

## 5.3 Tareas por persona: Fase 2 (uno a uno, con mini gate)

Mientras el dueño construye un módulo con el agente, **el otro integrante documenta el módulo anterior**: actualiza la 5.5, las clases y el ER y diccionario, y toma las capturas. Así hay un solo módulo en construcción a la vez y nada queda sin documentar.

| Paso | Construye (dueño) | En paralelo, el otro |
|---|---|---|
| M1 `donofrio_calidad` | **O**: HU-17, HU-18 | E: prototipo y reporte del certificado (4.6.2-4.6.3), prepara la demo |
| Mini gate 1 | O verifica la DoD del módulo; E decide | — |
| M2 `donofrio_heladeros` | **E**: HU-20, HU-21 | O: documenta M1 (5.5, clases, ER y diccionario), actualiza ISO 9001/HACCP en [09](09_normas_marcos.md) |
| Mini gate 2 | — | — |
| M3 Cadena de frío | **O**: HU-19 | E: documenta M2 (5.5, reporte de liquidación, BPMN TO-BE con M2) |
| Mini gate 3 | — | — |
| M4 `donofrio_tablero` + branding | **E**: HU-22, HU-24 | O: documenta M3; ejecuta otra vez Lighthouse y k6 con los módulos nuevos |
| Mini gate 4 → opcionales | Según el dueño de cada uno ([03 §3.4](03_modulos_odoo.md)) | — |

**Cierre (reservado, igual con o sin F2):**
- **Evelyn:** informe final en PDF, PPT, ensayo y subida de la entrega.
- **Orlando:** manuales en PDF, zip de la última release, checklist de verificación y ensayo.

## 5.4 Presentación de 10 minutos (dos variantes)

Son unas 12 diapositivas, con un **video de respaldo** de la demo (2-3 min por persona). Los bloques 3:00-7:00 cambian según hasta dónde llegó la Fase 2; si un módulo no llegó, se muestra su mockup como "siguiente iteración".

| Min | Bloque | Quién | Solo Fase 1 | Con Fase 2 |
|---|---|---|---|---|
| 0:00-0:45 | Apertura | Evelyn | D'Onofrio (1897, carritos amarillos, Nestlé 1997), contexto 2026 (Froneri), problema | Igual |
| 0:45-2:00 | Análisis y plan | Evelyn | BPMN AS-IS → oportunidades; Scrum en dos fases con gate, burndown, GitHub Projects | Igual |
| 2:00-3:00 | Arquitectura | Orlando | Odoo 19 + PostgreSQL 16 en Docker, módulos estándar + `donofrio_base`, C4 de contenedores, réplica | + módulos propios |
| 3:00-5:00 | Demo 1: Ventas y Gerencia | Evelyn | CRM → pedido con lista de verano → boleta en PdV → factura → dashboards estándar y pivotes | Pedido → **liquidación del heladero** (M2) → PDF → **tablero OWL** (M4) |
| 5:00-7:00 | Demo 2: Producción y Logística | Orlando | Compra → recepción con lote → OP de helado → lote con vencimiento → despacho FEFO | OP → **inspección rechazada que bloquea el despacho** (M1) → certificado → **alerta de temperatura** (M3) |
| 7:00-8:00 | Calidad del software y normas | Orlando | CI en verde, tests, ER/diccionario desde la BD real, controles ISO 27001 (roles, 2FA, TLS), réplica | Igual |
| 8:00-9:00 | Front-end y servicio | Evelyn | Prototipo → pantalla real, Lighthouse antes/después, SLA y mesa ITIL, SUS | + prototipos de la F2 implementados |
| 9:00-10:00 | Cierre | Ambos (30 s cada uno) | Conclusiones (E); recomendaciones: módulos de la F2 como trabajo futuro, EDI SUNAT, Froneri (O) | Conclusiones; trabajo futuro restante |

Reglas:
- Cronometrar dos ensayos completos.
- Si a los 8:30 no se llegó al cierre, se saltan las diapositivas de 7:00-9:00.
- Vestimenta formal.
