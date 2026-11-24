#!/usr/bin/env bash
# Crea la base de datos de Odoo e instala los módulos indicados (por defecto: donofrio_base).
# Es idempotente: si la BD ya existe, no hace nada.
# Uso: scripts/init_db.sh [modulo1,modulo2,...]
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env ] || { echo "Falta .env: ejecuta  cp .env.example .env" >&2; exit 1; }
set -a; . ./.env; set +a

DB="${ODOO_DB:-donofrio}"
MODULOS="${1:-donofrio_base}"

docker compose up -d --wait db

existe="$(docker compose exec -T db psql -U postgres -d postgres -tAc \
  "SELECT 1 FROM pg_database WHERE datname = '${DB}'")"
if [ "$existe" = "1" ]; then
  echo "La base de datos '${DB}' ya existe: no se hace nada."
  exit 0
fi

echo "Creando la base de datos '${DB}' e instalando: ${MODULOS}"
docker compose run --rm odoo odoo -d "$DB" -i "$MODULOS" --stop-after-init
echo "Listo. Levanta Odoo con:  docker compose up -d   y entra a http://localhost:${ODOO_PORT:-8069}"
