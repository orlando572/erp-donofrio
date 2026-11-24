# Sprint 1 (Fundaciones): Retrospectiva

**Fecha:** 23/11/2026 · **Facilita:** Orlando (SM)
**Estado:** borrador de Orlando a partir de lo ocurrido en el sprint; se completa y confirma con Evelyn.

## Qué salió bien

- Las 7 HU quedaron fusionadas con CI en verde: 24 de 24 puntos.
- Evelyn revisó y reprodujo el entorno en su PC, y su revisión detectó dos puntos reales (el estado de RNF012 y lo que de verdad exige la protección de `develop`).
- Los controles automáticos se probaron con casos que deben pasar y casos que deben fallar (test rojo, error de instalación y patrón legacy).
- Los datos y la configuración se cargaron por código, con pruebas, tal como pide el CLAUDE.md.

## Empezar

- Abrir cada PR directo contra `develop` desde un `develop` actualizado.
- Dejar que exista el CI **antes** de exigirlo como check obligatorio de la protección de rama.
- Marcar la checklist de la épica con el enlace al PR en cuanto se fusiona cada HU, no al final del sprint.

## Dejar de hacer

- Apilar varios PR uno sobre otro: al fusionar el primero, GitHub cambia la base de los siguientes y descarta las aprobaciones. Eso obligó a pedir cada aprobación dos veces y a fusionar cinco PR como administrador, saltándose una regla.
- Dar por hecho que una regla de protección se cumple solo porque está configurada: aplica a quien colabora, pero no a administradores.

## Continuar

- Probar cada control automático con casos que pasan y casos que fallan.
- Dejar las decisiones y sus excepciones por escrito en el repositorio, con número de PR.
- Cada integrante revisa los PR del otro antes de fusionar.

## Acciones de mejora

| # | Acción | Responsable | Para cuándo |
|---|---|---|---|
| 1 | Decidir si se activa `enforce_admins` en `develop` para que la protección valga también para administradores | Orlando y Evelyn | Antes del Planning del S2 |
| 2 | Un PR por HU, directo contra `develop`, sin apilar | Orlando | S2 |
| 3 | Hacer la demo cruzada de una HU ajena en la Review (Evelyn demuestra una HU de Orlando y viceversa) | Orlando y Evelyn | Review del S2 |
| 4 | Cerrar el registro de riesgos (#131) y las Dailies (#132) que quedaron «En curso» desde el S0 | Evelyn y Orlando | S2 |
