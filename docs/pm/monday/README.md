# Tableros de Monday: archivos de importación

[← docs/pm](..)

El plan ([04 §4.11](../../plan/04_scrum_pmbok.md)) pide 3 tableros en el plan gratuito de Monday (2 usuarios, 3 tableros). Estos CSV (UTF-8, abren bien en Excel) tienen los datos listos para importar.

| Archivo | Tablero | Filas | Grupos |
|---|---|---|---|
| [tablero1_scrum.csv](tablero1_scrum.csv) | 1. Scrum ERP D'Onofrio | 46 | Product Backlog F1 (25 HU, 83 pts) · Product Backlog F2 (8 HU, 37 pts + 3 de la opcional) · Sprint 0 · Gates |
| [tablero2_riesgos.csv](tablero2_riesgos.csv) | 2. Riesgos e impedimentos | 28 | Desarrollo · Despliegue · Mantenimiento · Impedimentos |
| [tablero3_entregables.csv](tablero3_entregables.csv) | 3. Entregables del informe | 52 | Secciones 1 a 10 · Manuales · PPT · Entrega |

## Cómo importar

1. En Monday, crear un tablero nuevo con el nombre de la tabla.
2. **Add → Import data → Excel/CSV** y subir el archivo.
3. Mapear: la primera columna es el nombre del ítem; **Estado**, **Prioridad**, **Fase** y **Tipo** como columnas de estado; **Puntos** y **Nivel** como números; **Fecha** como fecha.
4. Si Monday no reconoce la columna `Grupo`, crear los grupos a mano y mover los ítems.
5. Vistas: Tabla y Kanban (y Gantt/Timeline si el plan gratuito lo permite).
6. En el tablero 2, la columna **Nivel** del CSV ya trae el resultado de impacto × probabilidad; en Monday se puede reemplazar por una fórmula.

## Criterios usados al armar los CSV

- Los datos de las HU, los puntos, los sprints y los responsables salen de [04 §4.4](../../plan/04_scrum_pmbok.md). El **Product Backlog F1 suma 83 puntos** y el **F2 suma 37** (comprobado al generar los archivos).
- **Prioridad:** la F1 es Must (como indica el plan). El plan no da prioridad para la F2, así que se puso *Should* a los módulos M1-M4 y *Could* a HU-31 (opcional). Se puede cambiar en Monday.
- **Sprint 0:** las tareas hechas el 22/11/2026 figuran con estado *Hecho* o *En revisión* (las de Evelyn, hasta que ella las revise).
- **Riesgos:** R1-R20 son los del plan ([07 §7.1](../../plan/07_riesgos_entrega.md)). Los **RS-01 a RS-06** son propuestos en el S0 a partir de los ejemplos de las tablas 11-13 y se validan en el Planning del S1. Los **IMP-xx** son impedimentos reales del S0.
- **Entregables:** una fila por sección o apartado de [02 §2.2](../../plan/02_mapeo_plantilla.md), con responsable según el plan, el otro integrante como revisor y la marca "Depende de F2" según [02 §2.3](../../plan/02_mapeo_plantilla.md).
- El plan gratuito de Monday no se integra con GitHub: el número de issue o PR se anota a mano en la columna **Issue/PR**.
