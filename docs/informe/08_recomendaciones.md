# 8. Recomendaciones

Cada recomendación sale de una limitación que el propio proyecto documentó. Con la Fase 2 completa (releases `v1.1.0` a `v1.4.0`) ya no hay módulos propios por construir, así que las recomendaciones apuntan a operar, medir y mejorar lo construido. Las de negocio están en 8.1 y las técnicas en 8.2.

## 8.1 Recomendaciones de negocio y gestión

Se desarrollan en la sección 8.1 siguiente.

## 8.2 Recomendaciones técnicas

Se ordenan por prioridad para una puesta en producción real.

### Tabla 8.2-a. Recomendaciones técnicas

| # | Recomendación | Qué la respalda |
|---|---|---|
| T1 | Instalar el *cron* de respaldos, cifrarlos y sacarlos del equipo | El *cron* diario está documentado y no instalado; los respaldos viven en el mismo equipo y sin cifrar |
| T2 | Medir la disponibilidad con un registro continuo de `/web/health` (por ejemplo Uptime Kuma) | RNF011 parcial: sin medición no se puede afirmar el 99 % |
| T3 | Probar los casos de uso principales, el tablero y la liquidación en Chrome, Firefox y Edge y en ventana angosta | RNF001 parcial: la revisión usó Chrome y una ventana de 375 × 812 |
| T4 | Desplegar en una VM con dominio y Let's Encrypt, con un flujo de despliegue por SSH y *rollback* a la imagen del tag anterior | El sistema solo corre en la PC que lo levanta, con certificado autofirmado y despliegue manual |
| T5 | Configurar un servidor de correo saliente | El código de 2FA por correo lo necesita; sin él no hay recuperación si se pierde la app TOTP |
| T6 | Activar `pg_stat_statements` | Disponible en la imagen y no activado; k6 mide la aplicación, no las consultas |
| T7 | Reducir el JavaScript del backend y del tablero para subir Lighthouse (59 y 76) hacia 80 | RNF008 parcial: límite conocido que no se corrige con configuración del servidor |
| T8 | Activar `enforce_admins` en `develop` y `main` | Las reglas de protección no aplican al único administrador |
| T9 | Completar la seguridad: probar la promoción de la réplica, ZAP activo y autenticado, Dependabot, una prueba de actualización en el CI, TLS entre servicios y vencimiento en el punto de venta | Controles parciales de 5.11 y límites de 5.14 |
| T10 | Mejorar los módulos de la Fase 2: sensores y alerta por lecturas que faltan, `auditlog` en liquidaciones, inspecciones y lecturas, pruebas de JavaScript del tablero, merma con salida de inventario y app móvil del heladero | Límites declarados en 5.5b a 5.5e |
| T11 | Envío electrónico de comprobantes a SUNAT mediante un OSE | `l10n_pe_edi` es Enterprise: fuera del alcance |

Antes de la VM (T4) conviene tener los respaldos fuera del equipo (T1), el monitoreo (T2), el correo para el 2FA (T5) y `enforce_admins` (T8); antes de activar `pg_stat_statements` (T6), un respaldo reciente, porque exige reiniciar PostgreSQL. Toda mejora entra por una rama `feature/HU-xx-*` y un PR a `develop`, con su prueba.
