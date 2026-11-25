# 5.15 Despliegue: enfoque, herramientas, mejores prácticas y gestión de servicios

## 5.15.1 Enfoque de despliegue

El sistema se despliega con Docker Compose en un solo nodo. Hay tres entornos: desarrollo (la PC de cada integrante, `http://localhost:8069`), integración continua (el *runner* `ubuntu-24.04` de GitHub Actions) y la demostración protegida (`https://localhost:8443`, con Nginx, TLS, 2 *workers* y `proxy_mode`).

| Aspecto | Decisión |
|---|---|
| Estrategia | Reemplazo de contenedores en un nodo: `docker compose up -d --build --wait` recrea solo lo que cambió y espera a que quede `healthy`; hay unos segundos de corte, aceptables para una demostración |
| Rollback | Por versión etiquetada: volver al tag anterior (`git checkout vX.Y.Z` o la imagen `ghcr.io/orlando572/erp-donofrio:vX.Y.Z`) y, si los datos cambiaron, restaurar el respaldo en una base nueva |
| Respaldo previo | Se hace con `backup.sh` antes de actualizar, según el manual de instalación |
| Perfiles de Compose | Base (`db`, `odoo`) para desarrollo; `replica` para la réplica de lectura; `proxy` para el despliegue protegido, que levanta `levantar_prod.sh` |

**Procedimiento.** (1) Copiar `.env.example` a `.env` y, para el modo protegido, fijar una `ODOO_ADMIN_PASSWD` de 16 caracteres o más. (2) Levantar los contenedores y crear la base con `init_db.sh`. (3) Cargar los datos de demostración con el script de transacciones. (4) Levantar el despliegue protegido con `levantar_prod.sh`, que genera el certificado autofirmado. (5) Ejecutar `verificar_despliegue.sh`. (6) Opcionalmente, la réplica y el respaldo.

**Resultados.** `verificar_despliegue.sh` comprueba siete grupos (redirección, TLS, cabeceras, gestor de BD, gzip y *websocket*, modo producción y bloqueo de login) y todos pasaron. Los contenedores `db`, `db-replica` y `odoo` quedan en `healthy`. La imagen de release (3.25 GB) arranca sola, carga 109 módulos y `probar_imagen.sh` confirma Odoo 19.0, los módulos propios y `auditlog` dentro de ella, y rechaza la contraseña de ejemplo.

## 5.15.2 Herramientas utilizadas

### Tabla 25. Herramientas de despliegue

| Herramienta | Uso en el proyecto |
|---|---|
| Git y GitHub | Control de versiones, PR con revisión cruzada, ramas `main` y `develop` protegidas, issues y Project |
| Docker 29.1.3 y Compose 2.40.3 | Contenedores, perfiles, *healthchecks* y volúmenes; el mismo `docker-compose.yml` en las dos PC y en el CI |
| GitHub Actions | `ci.yml` (`lint`, `test`, `replica`, `backup`, `proxy`), `perf.yml` (manual) y `release.yml` |
| GHCR | Registro de imágenes `ghcr.io/orlando572/erp-donofrio`, llenado por `release.yml` con cada tag |
| Nginx 1.30.7 | Proxy inverso con TLS 1.2 y 1.3, HSTS, CSP, gzip, caché de *assets* y *websocket* |

Kubernetes no aplica: con un solo nodo no hay réplicas de Odoo que orquestar.

## 5.15.3 Pipeline CI/CD

![Pipeline CI/CD](../diagramas/arquitectura/pipeline_cicd.png)

*Figura 5.15-a. Pipeline CI/CD: de la rama de trabajo a la release y al despliegue en el nodo. Línea continua: automático en GitHub Actions; línea punteada: paso manual.*

| Flujo | Disparador | Qué hace |
|---|---|---|
| `ci.yml` | PR, push a `develop` y `main`, lunes 06:00 de Lima y manual | `lint` (`check_legacy.sh` y `ruff`, 11 s), `test` (instala los módulos en una base nueva y corre las 218 pruebas, 199 s), `replica` (24 s), `backup` (65 s) y `proxy` (105 s). `lint` y `test` son obligatorios en `develop` y `main` |
| `perf.yml` | Manual | Carga de datos, despliegue protegido, k6 y ZAP; sube los reportes como artefactos |
| `release.yml` | Tag `v*` (ensayo en PR y manual) | Construye y prueba la imagen, empaqueta el zip y, con tag, publica en GHCR (`:vX.Y.Z` y `:latest`) y crea la GitHub Release |

Las ramas `develop` y `main` exigen 1 aprobación, conversaciones resueltas, los checks `lint` y `test`, y prohíben el *force push*. Los PR de trabajo entran a `develop` con *squash* y las releases salen de `main` con tag.

**Mejores prácticas.** Los secretos no están en el repositorio: `.env` está fuera de Git, la contraseña maestra se puede leer de un archivo y, en modo protegido, Odoo se niega a arrancar con menos de 16 caracteres o con la de ejemplo; `GITHUB_TOKEN` es el único secreto de Actions, con *secret scanning* y *push protection* activos. Los respaldos tienen sumas, retención de 7 días y RTO medido (31 s). Las imágenes y herramientas llevan versión fija y el CI usa la misma imagen que las PC. Los puertos de Odoo y PostgreSQL solo se publican en `127.0.0.1`.

## 5.15.4 Resultados: releases y URLs

### Tabla 26. Releases publicadas

| Release | Fecha | Contenido |
|---|---|---|
| `v1.0.0` | 24/11/2026 | Núcleo: Odoo 19.0 y `donofrio_base` |
| `v1.1.0` | 25/11/2026 | M1: `donofrio_calidad` (inspección y certificado) |
| `v1.2.0` | 25/11/2026 | M2: `donofrio_heladeros` (liquidación del heladero) |
| `v1.3.0` | 25/11/2026 | M3: cadena de frío (incremento de `donofrio_calidad`) |
| `v1.4.0` | 25/11/2026 | M4: `donofrio_tablero` (tablero gerencial y marca) |

Cada release trae su `erp-donofrio-vX.Y.Z.zip` (de 23,5 a 26,1 MiB) y su imagen en GHCR. El sistema corre en la PC donde se levanta: ERP protegido en `https://localhost:8443`, desarrollo en `http://localhost:8069`, PostgreSQL en `localhost:5432` y la réplica en `localhost:5433`.

## 5.15.5 Gestión de servicios (ITIL 4 / ISO 20000-1)

El control de cambios sigue el flujo de GitHub: la solicitud nace como issue (épica o bug con plantilla); el otro integrante revisa el PR con la lista de la definición de terminado (sin patrones legacy, ACL y pruebas, actualización sin errores, textos en español) y lo aprueba; la implementación es un *squash* a `develop` o un *merge commit* a `main`; la verificación es el CI en verde y `verificar_despliegue.sh`; y el cierre es el tag que dispara `release.yml`. El formato de solicitud de cambio (RFC) está en el anexo 10.4 y la mesa de servicios TI, con incidentes y solicitudes, en `donofrio_base` (HU-32).

En capacidad, k6 con 20 usuarios virtuales mostró que el primer recurso que se agota es la CPU de Odoo (160 % de una CPU con 2 *workers* al ritmo de esfuerzo; 39 % a ritmo normal), mientras PostgreSQL llegó a 57 % y 201 MiB. El proyecto necesita unos 4 GB de RAM libres para todos los perfiles; la PC medida tiene 12 CPU y 14 GB.
