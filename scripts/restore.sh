#!/usr/bin/env bash
# HU-26: restaura un respaldo de scripts/backup.sh en una BASE NUEVA (nunca sobrescribe una existente)
# y mide el tiempo (RTO objetivo: 2 horas, RNF006).
# Uso: scripts/restore.sh <respaldo> [nombre_de_la_bd_nueva]
#   <respaldo>  el .dump, el _filestore.tar.gz o el prefijo (backups/donofrio_20261123_020000)
#   nombre      por defecto <bd>_restaurada
# Para abrir la base restaurada en Odoo: ODOO_DB=<nombre> docker compose up -d odoo  (el dbfilter sigue a ODOO_DB).
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && { set -a; . ./.env; set +a; }

[ $# -ge 1 ] || { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }
prefijo="${1%.dump}"; prefijo="${prefijo%_filestore.tar.gz}"; prefijo="${prefijo%.sha256}"
dump="$prefijo.dump"; filestore="${prefijo}_filestore.tar.gz"; sumas="$prefijo.sha256"
origen="$(basename "$prefijo")"; origen="${origen%_[0-9]*_[0-9]*}"
NUEVA="${2:-${origen}_restaurada}"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

[[ "$NUEVA" =~ ^[a-z][a-z0-9_]*$ ]] || { log "ERROR: nombre de BD no válido: '$NUEVA' (minúsculas, dígitos y _)"; exit 2; }
[ -f "$dump" ] && [ -f "$filestore" ] || { log "ERROR: faltan $dump o $filestore"; exit 1; }

inicio=$SECONDS
docker compose up -d --wait db >/dev/null
if [ -f "$sumas" ]; then
  ( cd "$(dirname "$prefijo")" && sha256sum --quiet -c "$(basename "$sumas")" ) || { log "ERROR: las sumas de verificación no coinciden"; exit 1; }
  log "Sumas de verificación correctas"
else
  log "AVISO: no hay $sumas; no se verificó la integridad"
fi
[ "$(docker compose exec -T db psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$NUEVA'")" = "" ] \
  || { log "ERROR: la base '$NUEVA' ya existe; elige otro nombre (este script no sobrescribe)"; exit 1; }

log "Creando la base '$NUEVA' y restaurando $(basename "$dump")"
docker compose exec -T db createdb -U "${ODOO_DB_USER:-odoo}" -O "${ODOO_DB_USER:-odoo}" "$NUEVA"
if ! docker compose exec -T db pg_restore -U "${ODOO_DB_USER:-odoo}" -d "$NUEVA" --no-owner --no-privileges --exit-on-error < "$dump"; then
  docker compose exec -T db dropdb -U postgres "$NUEVA" || true
  log "ERROR: falló pg_restore; se eliminó la base parcial '$NUEVA'"; exit 1
fi

log "Restaurando el filestore de '$NUEVA'"
docker compose run --rm --no-deps -T --entrypoint bash odoo -c \
  'mkdir -p /var/lib/odoo/filestore && tar -xzf - -C /var/lib/odoo/filestore --transform "s,^[^/]*,$0,"' "$NUEVA" < "$filestore"

log "Base '$NUEVA' restaurada. Comprobación:"
docker compose exec -T db psql -U postgres -d "$NUEVA" -X -tA -F ' = ' \
  -c "SELECT 'módulos instalados', count(*) FROM ir_module_module WHERE state = 'installed'" \
  -c "SELECT 'usuarios', count(*) FROM res_users" \
  -c "SELECT 'adjuntos', count(*) FROM ir_attachment" | sed 's/^/  /'
log "RTO medido: $((SECONDS - inicio)) s (objetivo: 7200 s)"
