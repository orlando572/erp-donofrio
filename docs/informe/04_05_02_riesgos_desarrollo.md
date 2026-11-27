# 2.5.1.1 Etapa de desarrollo de software

El registro tiene 15 riesgos de desarrollo: siete de prioridad Alta (R1 con nivel 9; R2, R4, R5, R6, R15 y R17 con nivel 6), seis Media y dos Baja. El riesgo dominante fue el plazo (R1), del que dependían los demás.

**Tabla 4.13. Riesgos de desarrollo**

| Id | Riesgo | Nivel | Estrategia y situación al cierre |
|---|---|---|---|
| R1 | Plazo muy corto: entrega el 27/11 a las 14:30 | 9 (Alta) | Mitigar con sprints de un día y un núcleo garantizado. El núcleo (81 puntos) se hizo en unas 21 horas y la Fase 2 se terminó el 25/11: mitigado en lo técnico |
| R2 | API obsoleta de Odoo por tutoriales o ejemplos de versiones anteriores | 6 (Alta) | Mitigar con las fuentes de Odoo 19.0 y el control de código obsoleto en el CI; las pruebas pasaron de 38 a 224: mitigado |
| R4 | Carga desigual o un integrante no puede defender su parte | 6 (Alta) | Reparto por áreas y revisión cruzada: cada integrante es dueño de dos módulos y 79 de 82 PR tienen la aprobación vigente del otro: mitigado |
| R6 | Funcionalidad no disponible en Community 19 | 6 (Alta) | La inspección de calidad (Enterprise) se cubrió con el módulo de Calidad (M1) y los comprobantes con IGV, con la localización peruana de Odoo: mitigado |
| R17 | La Fase 2 consume el Cierre | 6 (Alta) | Puntos de control por criterios; los cuatro módulos se fusionaron completos: mitigado |

Los demás riesgos se resumen así: otro grupo con la misma empresa (R3, cerrado porque el docente asignó D'Onofrio), los cambios del escenario de Froneri (R10, aceptado con corte en 2026), la documentación al final (R15, mitigada porque cada módulo trajo la suya con su PR), la fatiga por un sprint por día (R20, aceptado) y las cifras citadas sin verificar (RS-07, mitigado con la sección 9).
