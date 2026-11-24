# Sprint 3: Daily Scrum

Formato asíncrono. Se publica también como comentario en el issue «Dailies» (#132) del GitHub Project.

## 23/11/2026: Evelyn

- **Qué hice:**
  - Terminé mis historias del Sprint: **HU-23** (dashboards estándar y cuatro vistas guardadas, PR #188), **HU-32** (mesa de servicios en Project con SLA por prioridad, #193), **HU-33** en lo de ventas (test pedido → entrega FEFO → factura, #191) y **HU-28** en lo de rendimiento web (Lighthouse antes y después, #194). Comprobé con una mutación que el test de HU-33 falla si la salida pasa a FIFO.
  - Dejé listo lo de **HU-30** que no necesita personas (plan de pruebas de usabilidad, cuestionario SUS y script de cálculo, #195). Las pruebas con las 5 personas se harán después de la revisión de Orlando y de Evelyn y de la iteración del plan.
  - Marqué las casillas de las épicas #141 y #142 con los enlaces a los PR y cerré la #142.
  - Documentación del Sprint: 4.7 métricas, KPI y SLA (#199), 4.6.1 a 4.6.3 prototipos web y reportes (#201), cascada COBIT, prácticas ITIL y anexos 10.3 y 10.5 (#203). Abrí el PR de 6.1 a 6.3, 6.7 y 6.8 (#204, con `scripts/burndown.py` y `scripts/estadisticas_repo.py`) y el del Resumen y las Conclusiones (#205).
  - Revisé los PR de Orlando de este Sprint y resolví los conflictos de mis PR cuando se fusionó otro que tocaba el mismo archivo.
- **Qué haré:**
  - Pedir la aprobación de Orlando a los PR #204 y #205.
  - Redactar el informe del Gate 0 (`docs/scrum/gates/gate-0-fase1.md`) con lo que está listo de la Fase 1, lo que falta y qué módulos de la Fase 2 recomiendo según los criterios.
  - Hacer la demo cruzada con Orlando, la prueba piloto de HU-30 y cerrar #131 y #132 al terminar.
  - Actualizar las iteraciones y el estado de las tarjetas del GitHub Project.
- **Qué me bloquea:**
  - La aprobación de Orlando a los PR #204 y #205.
  - HU-30 depende de personas reales y de la revisión del plan; no se puede cerrar sola.
  - Mi acceso a GitHub solo lee proyectos: mover las tarjetas y activar el *workflow* «Item closed» del Project hay que hacerlo a mano.

## 23/11/2026: Orlando

- **Qué hice:**
  - Terminé mis historias del Sprint, con sus evidencias en `docs/capturas/sprint-3/`: **HU-25** (réplica de PostgreSQL en *streaming*, #186), **HU-26** (respaldo con retención de 7 días y restauración en una base nueva, con RTO medido de 31 s, #187), **HU-27** (despliegue protegido: Nginx con TLS, modo producción, 2FA, contraseñas de 12 o más, bloqueo por intentos y auditoría, #189) y **HU-29** (release automática: imagen en GHCR y zip en GitHub Releases con cada tag; probada en ensayo, #190).
  - **HU-33**, mi parte: pruebas de integración compra → recepción → orden de producción → lote con vencimiento (#192). **HU-28**, mi parte: carga con k6 (20 usuarios virtuales) y seguridad con ZAP baseline sobre el despliegue protegido (#196): p95 de 9 a 18 ms y 0 alertas altas. `donofrio_base` quedó en 136 pruebas.
  - Documentación del Sprint: planning (#185); 4.2.5 a 4.2.8 clases, ER, diseño lógico y diccionario (#197); sección 5 completa (#198); 6.4 a 6.6 y 6.9 a 6.13, SoA ISO 27001, trazabilidad y anexo 10.4 (#200); abstract, manual de instalación al día y manual de herramientas (#202).
  - Revisé y aprobé los PR de Evelyn #188, #191, #193, #194, #195, #199, #201, #203, #204, #205 y #206. Corregí los conflictos de mis PR fusionando `develop` en la rama (#187, #189, #192 y #196).
  - **Cierre del sprint:** abrí el PR #209 (informe: 4.3.6, 4.3.8, 4.5.3, 4.5.4, anexo 10.2, 8.2 y 4.2.3 al día con los resultados de HU-25 a HU-29), la Retro y esta Daily. Marqué la checklist de la épica #140 con sus PR y pasé su tarjeta a «Hecho» en el Project.
- **Qué haré:**
  - Pedir la aprobación de Evelyn a #209 y a los PR de eventos (Retro, Daily y Review) y de la verificación del Gate 0.
  - Entregar la verificación de los criterios de salida de la Fase 1 (`docs/scrum/gates/gate-0-verificacion.md`) para que Evelyn redacte el informe del Gate 0. No empiezo ningún módulo de la Fase 2.
  - Revisar los PR abiertos de Evelyn (#207 y #208) cuando estén listos.
  - Con la confirmación aparte del equipo: el PR `develop` → `main` y el tag `v1.0.0`.
  - Después del Sprint 4, por decisión del equipo del 23/11/2026: la demo cruzada y la HU-30 con 5 personas (la parte de HU-30 es de Evelyn).
- **Qué me bloquea:**
  - Nada técnico. Dependo de la aprobación de Evelyn a mis PR y de su confirmación de la Retro y de la Review.
  - `main` va **84 commits detrás** de `develop` y sin tag: el criterio «CI en verde en `main`» y el tag `v1.0.0` necesitan el PR `develop` → `main`, que se hace en el Gate 0 con confirmación aparte.
  - #131 (registro de riesgos) es de Evelyn y sigue abierto; #132 (Dailies) se cierra cuando esta Daily esté fusionada.
