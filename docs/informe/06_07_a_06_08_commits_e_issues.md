# 6.7 y 6.8 Resumen de commits y de issues

Las cifras se miden con un script de solo lectura sobre develop con fecha de corte 25/11/2026: son 82 PR fusionados.

## 6.4.3 Resumen de commits

Los commits siguen Conventional Commits en español con la etiqueta de la historia de usuario o del sprint al final, por ejemplo `feat(facturacion): factura (01) y boleta (03) con IGV desde el pedido [HU-15]`. Como develop se fusiona con *squash*, lo que queda en la historia es el título del PR y es ahí donde se exige la etiqueta.

| Autor | Commits en develop | Líneas agregadas | Líneas quitadas | PR fusionados | Commits dentro de los PR |
|---|---|---|---|---|---|
| Orlando | 52 | 44 387 | 802 | 43 | 180 (58 %) |
| Evelyn | 39 | 13 108 | 257 | 39 | 132 (42 %) |
| **Total** | **91** | 57 495 | 1 059 | **82** | **312** |

Las líneas incluyen datos, pruebas, documentación y diagramas; miden volumen, no esfuerzo. Por tipo, los 312 commits dentro de los PR son 185 de documentación (59 %), 82 de funcionalidad nueva (26 %), 14 correcciones, 13 de pruebas, 9 de mantenimiento, 3 de integración continua y 3 de rendimiento: el proyecto es sobre todo documentación y configuración.

| Regla | Cumplimiento |
|---|---|
| Commits que siguen Conventional Commits | 309 de 312 (99 %); los 3 restantes son commits de fusión escritos a mano |
| Títulos de PR con convención y etiqueta | 79 de 82 (96 %); los 3 restantes son unas capturas y los dos PR de release |

## 6.4.4 Resumen de issues

GitHub tiene 22 issues: 15 épicas (11 cerradas) y 7 de gestión (2 cerradas). Las épicas agrupan las HU de un área con su checklist; 17 issues son de la Fase 1 y 5 de la Fase 2. Cada issue lleva tres etiquetas (tipo, área y fase) y un milestone por sprint, de «Sprint 0 – Inicio» a «Cierre».

| Área | Issues | Cerrados |
|---|---|---|
| Infraestructura | 6 | 6 |
| Documentación | 6 | 1 |
| Ventas | 3 | 1 |
| Extras, gerencia y producción | 6 | 4 |
| Logística | 1 | 1 |

Cada PR indica a qué épica pertenece: 51 la citan como parte de ella y 5, los últimos de cada épica, la cierran al fusionarse; los otros 26 son documentación, capturas y actas. Ningún issue es de tipo bug: los defectos hallados en las pruebas de pantalla de M1 y M4 se corrigieron dentro de sus PR y quedaron documentados en 3.1.4.2 y 3.1.4.5.

La prevención de defectos se apoya en la plantilla de PR con la definición de terminado, la plantilla de bug, el CI obligatorio (estilo (lint) y pruebas), la revisión del otro integrante en todos los PR y las 218 pruebas automáticas.
