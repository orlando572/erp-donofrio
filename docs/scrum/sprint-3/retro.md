# Sprint 3 (Calidad del núcleo): Retrospectiva

**Fecha:** 23/11/2026 · **Facilita:** Orlando (SM)
**Estado:** borrador de Orlando; **Evelyn la confirma** (o la corrige) y agrega sus aportes al final. Todo sale de los PR, los issues y los commits reales (`gh` y `git` en solo lectura, 23/11/2026); lo que no se pudo comprobar se dice. El Sprint 3 corrió el mismo día que el 2: los 22 PR (#185 a #206) se abrieron y se fusionaron en unas 4 horas de reloj.

## Seguimiento de las acciones de la Retro del S2

| # | Acción | Resultado |
|---|---|---|
| 1 | Decidir si se activa `enforce_admins` en `develop` | **Decidida; no se activó.** Evelyn (PO) decidió el 23/11/2026, en la Retro del S2, dejarlo desactivado como salida de emergencia y compensarlo con la revisión cruzada. Se verificó con la API el 23/11/2026: sigue en `false` en `develop` y `main`. **Queda abierto un punto:** el planning del S3 aún lista «decidir si se activa `enforce_admins`» como pendiente del S2 (ya está decidido) y `main` sigue sin checks obligatorios. Pasa a la recomendación técnica [8.2.8](../../informe/08_recomendaciones.md) y a la decisión final antes de la entrega |
| 2 | Un PR por HU, directo contra `develop`, sin apilar | **Cumplida.** Los 22 PR del S3 (#185 a #206) tienen `develop` como base y los 22 se fusionaron con *squash*; ninguno se apiló sobre otro. Costos: **5 PR** integraron `develop` en su rama (#187, #189, #192, #194 y #196: 6 *merge commits*) y **7 aprobaciones se descartaron** al cambiar el código en 5 PR (#189, #192, #194, #195 y #201), con nueva aprobación en cada caso |
| 3 | Demo cruzada de una HU ajena en la Review | **Pendiente: diferida por decisión del equipo (23/11/2026) al final, después del Sprint 4.** Sigue sin hacerse; el guion está en [`../sprint-2/demo_cruzada.md`](../sprint-2/demo_cruzada.md). Es la forma de cubrir R4 y no se cierra |
| 4 | Cerrar el registro de riesgos (#131) y las Dailies (#132); marcar la checklist de cada épica y pasarla a «Hecho» al fusionar | **Parcial.** #131 y #132 **siguen abiertos**: #132 se cierra cuando la Daily del S3 esté fusionada; #131 es de Evelyn. Checklists: Evelyn marcó #141 y #142 con los enlaces a los PR; la de #140 (HU-25, 26, 27 y 29) **quedó sin marcar hasta el cierre del sprint** y se marcó el 23/11/2026 con sus PR (#186, #187, #189 y #190). La tarjeta de #140 se pasó a «Hecho» en el Project; las de #141 y #142 siguen en «Backlog» (el acceso de Evelyn al Project es solo de lectura) |

## Qué salió bien

- **Cumplimos el objetivo del sprint salvo HU-30:** 27 de 29 puntos en `develop` (HU-25, 26, 27, 28, 29, 23, 32 y 33); `donofrio_base` pasó de **100 a 136 pruebas** y todo corre en el CI. La HU-30 se difiere (ver más abajo).
- **La aprobación llegó rápido.** Después de la acción del S2 («pedir la aprobación apenas el CI esté en verde»), los PR de HU y de informe tardaron una **mediana de 7 minutos** entre abrirse y fusionarse (21 PR de #186 a #206; el máximo, 63 minutos, fue el de HU-30 #195, con 8 commits y 2 aprobaciones descartadas).
- **Las verificaciones automáticas probaron lo que decía el informe.** Los jobs `replica`, `backup` y `proxy` del CI convierten cada HU de infraestructura en una comprobación repetible (`verificar_replica.sh`, `verificar_backup.sh`, `verificar_despliegue.sh`), con **RTO de 31 s** y 0 alertas altas en ZAP.
- **Trabajo en paralelo sin perder control.** Las tareas de la cola de Orlando (HU-33 de compra y OP, HU-28 de k6 y ZAP, y los bloques de informe de 4.2, 5, 6 y de manuales; PR #192, #196, #197, #198, #200 y #202) se hicieron en sesiones aparte del asistente de IA y la sesión principal **validó cada PR antes de avisar a Orlando**; todos entraron con la aprobación del otro integrante.
- **El informe avanzó junto con el código.** Evelyn y Orlando entregaron su documentación del sprint en PR separados el mismo día (11 PR de cada uno en el sprint), y el informe dice lo que existe: la VM en la nube, el `cd.yml` y Uptime Kuma están declarados como **no implementados** en lugar de maquillarse.
- **La revisión cruzada y el CI atraparon errores reales** (ver abajo), y las discrepancias plan–realidad quedaron escritas (por ejemplo, `main` sin checks obligatorios y el hook de Git que no existe).

## Errores hallados al validar (y qué enseñan)

| Dónde | Qué pasó | Cómo se halló y se corrigió |
|---|---|---|
| **2FA en el login (HU-27, #189)** | El código preguntaba `has_group` del grupo «2FA obligatorio» durante el inicio de sesión, cuando el usuario actual todavía es el público; `has_group` solo acepta al usuario actual y la comprobación fallaba (en la validación del PR el acceso daba **403**) | Al validar el PR contra el despliegue real y no solo con las pruebas. Se corrigió con `sudo()` en `_exige_2fa` (`addons/donofrio_base/models/res_users.py`, con el comentario que explica el motivo) y el comportamiento quedó probado: `admin` y `gerente` → `/web/login/totp`, `vendedor` → `/odoo` |
| **El CI frente al entorno local (HU-27, #189)** | El PR tuvo **2 corridas del CI en rojo** en el job `proxy`: la verificación de TLS usaba `openssl` y en el *runner* no aceptaba TLS 1.3, y el bloqueo de login contaba mal porque con 2 *workers* el contador es por proceso | La prueba pasaba en la PC y no en el *runner* de GitHub. Se corrigió en el mismo PR (commit «el chequeo de TLS usa curl y el de bloqueo de login lee el umbral real de la BD»). En HU-28 se volvió a corregir el conteo del bloqueo por *worker* |
| **Estado de las ramas y la protección** | El informe decía que `enforce_admins` «no registra un motivo» cuando la Retro del S2 ya lo había decidido; las cifras de `main` (76 commits atrás) y de PR (49) del informe de 6.4 quedaron viejas en horas | Al validar el informe contra la API. Se corrigió la frase en 6.6; los números llevan fecha y la verificación de Gate 0 los vuelve a medir |

## Conflictos aditivos entre HU fusionadas en paralelo

Cuando dos HU tocan los mismos archivos de lista (`__manifest__.py`, `tests/__init__.py`, `ci.yml`, el README de capturas), el segundo PR en fusionarse choca aunque los cambios no se pisen. Pasó en **5 PR** del sprint: #187 (HU-26) con `ci.yml` de la HU-25, #189 (HU-27) con el manifiesto y las pruebas de la HU-23 de Evelyn (y antes con `ci.yml` de HU-26), #192 (HU-33) con el test de ventas de Evelyn, #194 (HU-28) y #196 (HU-28). En todos fue **aditivo**: se fusionó `develop` en la rama (no *rebase*, sin *force push*) y se conservaron los dos lados. Cada fusión descarta la aprobación (`dismiss_stale_reviews`) y hay que pedirla de nuevo; fue el costo de trabajar en paralelo.

## Empezar

- Avisar al otro integrante **antes de abrir** un PR que toque `__manifest__.py`, `tests/__init__.py` o `ci.yml`, para fusionar en orden y no encadenar conflictos aditivos.
- Probar cada HU de infraestructura **también en el entorno del CI** (el *runner* `ubuntu-24.04`, sin las herramientas de la PC) antes de abrir el PR, no solo en la PC de quien la hizo.
- Dejar la **medición del tiempo** del próximo sprint registrada (hora de inicio y fin de cada HU) para el cuadro de sprints y el burndown con fechas reales.
- Marcar la checklist de la épica en el mismo PR (o al fusionarlo), no al cierre: la de #140 se hizo al final del sprint.

## Dejar de hacer

- Dar por verificado un control porque pasa en la PC: el 2FA (403 en el login) y el bloqueo por intentos (contado por *worker*) pasaban en desarrollo y fallaban en el despliegue real.
- Cifras fijas en la documentación sin fecha ni comando que las reproduzca: `main` «76 commits detrás» pasó a **84** en el mismo día.
- Dejar el movimiento de las tarjetas del Project para el final: las de #140, #141 y #142 estuvieron en «Backlog» con las épicas ya cerradas.

## Continuar

- Una rama y un PR por HU, directo contra `develop`, con `[HU-xx]` o `[S3]` en cada commit y el PR aprobado por el otro integrante.
- Datos y configuración por código, con pruebas (136 en el CI) y evidencias en `docs/capturas/sprint-3/`.
- Sesiones en paralelo con **validación del PR antes de avisar**, y reportar lo que no se hizo con la misma claridad que lo que sí.
- Declarar las limitaciones con su evidencia (backend 59 en Lighthouse, RNF001 y RNF011 sin medir, `enforce_admins` desactivado).

## Acciones de mejora

| # | Acción | Responsable | Para cuándo |
|---|---|---|---|
| 1 | Decidir con confirmación explícita, antes de la entrega, si se activa `enforce_admins` y se ponen checks obligatorios en `main` (la regla actual es del S2; el Gate 0 abre el PR `develop` → `main`) | Orlando y Evelyn | Gate 0 |
| 2 | Hacer la **demo cruzada** (Evelyn una HU de Orlando y viceversa) y las **pruebas de usabilidad de HU-30** con 5 personas: diferidas por decisión del equipo al final, **después del Sprint 4** y antes de la exposición | Evelyn (HU-30), Orlando y Evelyn (demo) | Después del S4 |
| 3 | Cerrar #132 cuando la Daily del S3 esté fusionada y #131 con el comentario de seguimiento de riesgos del S3 (con los cambios propuestos en [4.5.3 y 4.5.4](../../informe/04_05_riesgos_despliegue_y_mantenimiento.md)); pasar a «Hecho» las tarjetas de #141 y #142 cuando Evelyn tenga permiso de escritura o lo haga Orlando | Orlando (#132) y Evelyn (#131, tarjetas) | Antes del Gate 0 |

## Riesgos que cambian

El registro es `docs/pm/plan_riesgos.md`; **estos cambios los propone Orlando y los valida Evelyn**, y recién entonces se anotan como comentario en #131. El detalle y la evidencia de cada uno está en [4.5.3 y 4.5.4](../../informe/04_05_riesgos_despliegue_y_mantenimiento.md).

| Riesgo | Hoy | Propuesta | Motivo |
|---|---|---|---|
| RS-04 Backups no probados | 3 × 2 = 6 Alta | P a 1: **3 Media**, «Mitigado» | HU-26: restauración probada (RTO 31 s), integridad y job `backup` del CI (36 correctas) |
| RS-02 Secretos expuestos | 3 × 2 = 6 Alta | P a 1: **3 Media**, «Mitigado con límites» | *Secret scanning* y *push protection* activos; Odoo rechaza la clave de ejemplo; el zip sale sin `.env` |
| RS-05 Disco lleno | 2 × 2 = 4 Media | P a 3: **6 Alta**, «Abierto, en alza» | Disco al 91 % (18 GB libres) frente al 85 % del S0; 15 GB recuperables en Docker sin limpiar |
| RS-03 Gestor de BD expuesto | 3 × 1 = 3 Media | Sin cambio: «Mitigado» | `verificar_despliegue.sh` y ZAP sin altas |
| RS-01 Migración fallida (`-u`) | 2 × 2 = 4 Media | Sin cambio; **sin prueba automática** | El CI no corre `-u` sobre una base con datos |
| R4 Carga desigual y defensa de cada parte | 3 × 2 = 6 Alta | Sin cambio, **sigue abierto** | La demo cruzada se difiere: no se podrá cubrir antes del Gate 0 |
| R14 La demo en vivo falla | 3 × 2 = 6 Alta | Sin cambio; baja a 4 con el video y el ensayo | El video y la prueba de la PC de la exposición están diferidos |
| R2 API obsoleta | 3 × 2 = 6 Alta | Sin cambio, se revisa en el Gate 0 | `lint` con `check_legacy.sh`: 101 corridas correctas; el CI falla con errores, no con avisos de deprecación |
| R1 Plazo muy corto | 3 × 3 = 9 Alta | Sin cambio | Entrega el viernes 27/11 a las 14:30; el Cierre no se toca |

## Aportes de Evelyn a la Retro

> Pendiente de Evelyn: qué aprendió, qué cambiaría y qué pide para el próximo sprint. Esta Retro queda en borrador hasta que Evelyn la confirme (en la del S2 la confirmación se anotó en el encabezado).
