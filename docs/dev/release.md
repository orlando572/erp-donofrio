# Cómo publicar una release (HU-29)

Un tag `vX.Y.Z` en `main` dispara `.github/workflows/release.yml` y publica tres cosas:

| Qué | Dónde | Para qué |
|---|---|---|
| Imagen Docker con Odoo 19, `auditlog` y los módulos propios dentro | `ghcr.io/orlando572/erp-donofrio:vX.Y.Z` (y `:latest`) | Correr el ERP sin montar `./addons` |
| `erp-donofrio-vX.Y.Z.zip` (`git archive` del tag) | Adjunto de la GitHub Release | Entregable «código fuente comprimido» |
| GitHub Release con notas generadas de los PR | Pestaña Releases | Registro de lo entregado (`v1.0.0` = núcleo) |

## Versiones

- `v0.1.0`, `v0.2.0`…: una por sprint de la Fase 1 (se marcan como *pre-release*).
- **`v1.0.0` = núcleo de la Fase 1** (Gate 0, [04 §4.3](../plan/04_scrum_pmbok.md)).
- `v1.1.0`, `v1.2.0`…: un módulo de la Fase 2 cada uno, solo si cumple su DoD y el equipo lo confirmó en el gate.

## Pasos

1. El PR `develop` → `main` se fusiona con *merge commit* ([06 §6.2](../plan/06_github_ci_infra.md)) y el CI de `main` está en verde.
2. Desde `main` actualizado:

   ```bash
   git checkout main && git pull
   git tag -a v1.0.0 -m "Núcleo v1.0.0 (Fase 1)"
   git push origin v1.0.0
   ```

3. Mirar la corrida **Release** en Actions. Hace, en orden: construye la imagen y la prueba (`scripts/probar_imagen.sh`: Odoo 19, módulos dentro, configuración de desarrollo y producción, rechazo de la contraseña de ejemplo), arma el zip (`scripts/empaquetar_release.sh`), publica la imagen en GHCR y crea la Release con el zip.
4. Comprobar: la Release tiene el zip adjunto, el paquete aparece en el repositorio (Packages) y su visibilidad es pública (Package settings → Change visibility, si GHCR lo creó privado).

## Probar sin publicar

- **Automático:** cada PR que toque `release.yml`, `docker/odoo/**` o los dos scripts corre la misma cadena en modo **ensayo** (construye, prueba y empaqueta; no publica nada y guarda el zip como artefacto del workflow).
- **A mano:** Actions → Release → *Run workflow* (también es un ensayo).
- **En local:**

  ```bash
  docker buildx build --load --build-context addons=./addons -t erp-donofrio:prueba docker/odoo
  scripts/probar_imagen.sh erp-donofrio:prueba
  scripts/empaquetar_release.sh HEAD dist     # dist/erp-donofrio-HEAD.zip
  ```

## Usar la imagen publicada

```bash
docker pull ghcr.io/orlando572/erp-donofrio:v1.0.0
docker run --rm -e ODOO_DB=donofrio -e ODOO_ADMIN_PASSWD=<16+ caracteres> -e HOST=<db> -e USER=odoo -e PASSWORD=<clave> \
  ghcr.io/orlando572/erp-donofrio:v1.0.0 odoo -d donofrio --stop-after-init
```

Con `docker compose` en el equipo de desarrollo no hace falta: el compose construye la imagen y monta `./addons`.

## Reglas y límites

- El tag debe tener el formato `vX.Y.Z`; otro formato hace fallar el workflow antes de publicar.
- Si el commit del tag no está en `main`, el workflow avisa (no falla): las releases salen de `main`.
- Si la prueba de la imagen falla, **no se publica nada**.
- El zip nunca lleva `.env` ni llaves (el script lo comprueba); `.claude/` (hooks del agente) sí viaja porque está versionado.
- Solo se usa `GITHUB_TOKEN`; no hay secretos propios que configurar.
- No hay despliegue automático a una VM (`cd.yml` es opcional en [06 §6.4](../plan/06_github_ci_infra.md) y no se hace).
