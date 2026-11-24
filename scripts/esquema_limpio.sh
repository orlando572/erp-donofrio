#!/usr/bin/env bash
# Crea (o borra) una BD temporal con donofrio_base recién instalado desde el código de este checkout.
# Sirve para extraer el esquema real de `develop` (ER y diccionario de datos, informe 4.2.6 a 4.2.8) sin tocar
# la BD de desarrollo, que puede ir por detrás del código.
#
# Uso: scripts/esquema_limpio.sh crear [nombre]    (por defecto: esquema_tmp_informe; tarda 1-2 minutos)
#      scripts/esquema_limpio.sh borrar [nombre]
#
# Usa `docker run` con la imagen y la red del compose, sin `docker compose up/run`, para no recrear el contenedor `db`
# (en un worktree el compose apunta a otras rutas). Solo borra BD cuyo nombre empieza por `esquema_tmp_`.
set -euo pipefail
cd "$(dirname "$0")/.."

accion="${1:-}"
bd="${2:-esquema_tmp_informe}"
[[ "$bd" == esquema_tmp_* ]] || { echo "El nombre debe empezar por esquema_tmp_ (es '$bd')" >&2; exit 1; }
[ -f .env ] || { echo "Falta .env: ejecuta  cp .env.example .env" >&2; exit 1; }
set -a; . ./.env; set +a
contenedor_db="${DB_CONTENEDOR:-erp-donofrio-db-1}"
red="${COMPOSE_RED:-erp-donofrio_default}"

case "$accion" in
  crear)
    docker run --rm --network "$red" \
      -e HOST=db -e USER="${ODOO_DB_USER:-odoo}" -e PASSWORD="$ODOO_DB_PASSWORD" \
      -e ODOO_DB="$bd" -e ODOO_ADMIN_PASSWD="$ODOO_ADMIN_PASSWD" -e DONOFRIO_USER_PASSWORD="${DONOFRIO_USER_PASSWORD:-}" \
      -v "$PWD/addons":/mnt/extra-addons:ro \
      erp-donofrio/odoo:19.0 odoo -d "$bd" --db-filter "^${bd}\$" -i donofrio_base --load-language es_PE --stop-after-init
    echo "Listo: BD '${bd}'. Ahora: python3 scripts/diccionario_datos.py --bd ${bd} y python3 scripts/diagrama_er.py --bd ${bd}"
    ;;
  borrar)
    docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" "$contenedor_db" \
      psql -U postgres -d postgres -qc "DROP DATABASE IF EXISTS \"${bd}\" WITH (FORCE)"
    echo "BD '${bd}' borrada."
    ;;
  *) echo "Uso: $0 crear|borrar [nombre]" >&2; exit 1 ;;
esac
