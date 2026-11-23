## HU
<!-- Título con el formato del commit: tipo(alcance): descripción [HU-xx] -->
Closes #

## Qué cambia

## Cómo probar

## Capturas
<!-- Evidencia en docs/capturas/sprint-N/HU-xx_descripcion.png -->

## Checklist del revisor (Definition of Done)
- [ ] El PR lo revisa el **otro integrante**
- [ ] CI en verde (lint, `check_legacy`, instalación con `--test-enable`, sin `ERROR`)
- [ ] Sin patrones legacy de Odoo (ver `docs/dev/odoo19_cambios.md`)
- [ ] Modelos nuevos con ACL (`ir.model.access.csv`) y tests (`TransactionCase`)
- [ ] `-u` sobre una BD con datos sin errores
- [ ] Textos visibles en español y criterios de aceptación verificados en la UI
- [ ] Capturas de evidencia en `docs/capturas/sprint-N/`
- [ ] Monday en "Hecho" con el enlace a este PR
- [ ] Hay al menos un borrador de la sección del informe
