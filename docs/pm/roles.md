# Roles Scrum (tabla 7 de la plantilla, sección 4.2.10)

[← docs/pm](.) · Fuente: [04 §4.1](../plan/04_scrum_pmbok.md) y [05 §5.1](../plan/05_reparto_equipo.md)

Versión S0, 22/11/2026. Redactado por Orlando por encargo de Evelyn (PO), que debe revisarlo.

La Guía Scrum 2020 permite que el Product Owner y el Scrum Master también sean Developers; en un equipo de 2 es la única opción realista. Los roles se reparten para que **las responsabilidades de cada rol no recaigan en la misma persona que debe controlarlas**: el PO acepta o rechaza el trabajo técnico que hace sobre todo el otro integrante, y el SM vigila el proceso y los tiempos del equipo, incluido el PO.

| Rol | Responsable | Responsabilidades | Por qué esa persona |
|---|---|---|---|
| **Product Owner** | **Evelyn** | Ordena el Product Backlog; redacta las HU y los criterios de aceptación; representa a D'Onofrio (gerencia y áreas); acepta o rechaza los incrementos en la Review; mantiene el GitHub Project; redacta los informes de gate y lleva la decisión | Lidera el análisis empresarial y las áreas de cara al negocio (Ventas, Heladeros, Gerencia) |
| **Scrum Master** | **Orlando** | Facilita los eventos; cuida la DoD y el CI; elimina impedimentos técnicos (Docker, Odoo, agente IA); mide la velocidad y el burndown; protege el *timebox*; verifica los criterios de salida del gate | Lidera la infraestructura, el repo y la automatización, donde surgen los impedimentos |
| **Developers** | **Evelyn y Orlando** | Construyen el incremento: módulos, configuración, pruebas y documentación; cada uno revisa **todos** los PR del otro | Revisión cruzada obligatoria |

**Asistente de IA:** herramienta de los Developers, **no es un rol**. Se declara en la metodología del informe (riesgo R5) y el equipo revisa y entiende todo lo que firma.

## Reparto por áreas (de punta a punta)

| | Evelyn | Orlando |
|---|---|---|
| Áreas de negocio | Marketing y Ventas (CRM, Ventas, PdV, heladeros), Gerencia, extras administrativos (Compras, Facturación, RR. HH., mesa de servicios TI) | Logística (almacenes, lotes, FEFO, cadena de frío), Producción (MRP, calidad), configuración base y seguridad |
| Módulos de la Fase 2 (dueño) | M2 `donofrio_heladeros`, M4 `donofrio_tablero` + branding | M1 `donofrio_calidad`, M3 cadena de frío |
| Entregables | Informe final (maquetación en Word), PPT, **sube la entrega** | Manuales, zip de la última release, **verifica la entrega** |

El detalle por sprint está en [05 §5.2 y §5.3](../plan/05_reparto_equipo.md).

## Regla de conocimiento cruzado

- Cada uno revisa todos los PR del otro.
- En cada Review, la otra persona hace la demo de una HU ajena.
- Antes de la exposición, cada uno puede ejecutar `docker compose up` y explicar la arquitectura general.
