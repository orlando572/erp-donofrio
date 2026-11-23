#!/usr/bin/env bash
# HU-26 (06 §6.5, 09 control #5, ISO 27001 A.8.13): copia de seguridad de la base y del filestore de Odoo.
# Genera en backups/ (o en $BACKUP_DIR) tres archivos por corrida:
#   <bd>_AAAAMMDD_HHMMSS.dump                pg_dump -Fc de la base
#   <bd>_AAAAMMDD_HHMMSS_filestore.tar.gz    adjuntos y archivos de la BD (/var/lib/odoo/filestore/<bd>)
#   <bd>_AAAAMMDD_HHMMSS.sha256              sumas de verificación de los dos anteriores
# y borra los respaldos con más de 7 días ($RETENCION_DIAS). No requiere que Odoo esté encendido,
# solo la base (db). El dump y el filestore se toman uno tras otro, no en el mismo instante.
# Uso: scripts/backup.sh
# Diario a las 02:00 (cron del equipo):
#   0 2 * * * cd /ruta/a/ERP-Donofrio && scripts/backup.sh >> backups/backup.log 2>&1
# Para una copia fuera del equipo, apunta BACKUP_DIR a una carpeta sincronizada.
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && { set -a; . ./.env; set +a; }

DB="${ODOO_DB:-donofrio}"
DESTINO="${BACKUP_DIR:-backups}"
DIAS="${RETENCION_DIAS:-7}"
sello="$(date +%Y%m%d_%H%M%S)"
base="${DB}_${sello}"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

mkdir -p "$DESTINO"
parcial=("$DESTINO/$base.dump.parcial" "$DESTINO/$base""_filestore.tar.gz.parcial")
trap 'rm -f "${parcial[@]}"' EXIT

docker compose up -d --wait db >/dev/null
[ "$(docker compose exec -T db psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$DB'")" = "1" ] \
  || { log "ERROR: la base '$DB' no existe"; exit 1; }

inicio=$SECONDS
log "Respaldo de '$DB' en $DESTINO/ ($base)"

docker compose exec -T db pg_dump -U postgres -Fc "$DB" > "${parcial[0]}"
log "pg_dump listo: $(du -h "${parcial[0]}" | cut -f1)"

# El filestore se lee con el mismo volumen que usa Odoo; sin adjuntos queda un tar vacío.
docker compose run --rm --no-deps -T --entrypoint bash odoo -c \
  'cd /var/lib/odoo/filestore 2>/dev/null && [ -d "$0" ] && tar -czf - "$0" || tar -czf - --files-from /dev/null' "$DB" \
  > "${parcial[1]}"
log "filestore listo: $(du -h "${parcial[1]}" | cut -f1)"

mv "${parcial[0]}" "$DESTINO/$base.dump"
mv "${parcial[1]}" "$DESTINO/${base}_filestore.tar.gz"
( cd "$DESTINO" && sha256sum "$base.dump" "${base}_filestore.tar.gz" > "$base.sha256" )

borrados="$(find "$DESTINO" -maxdepth 1 -type f -name "${DB}_*" -mmin +"$((DIAS * 1440))" -print -delete | wc -l)"
log "Retención de $DIAS días: $borrados archivo(s) borrado(s)"
log "Respaldo terminado en $((SECONDS - inicio)) s"

echo
echo "Respaldos de '$DB' en $DESTINO/:"
( cd "$DESTINO" && ls -lh --time-style='+%Y-%m-%d %H:%M' "${DB}"_*.dump "${DB}"_*_filestore.tar.gz 2>/dev/null \
  | awk '{print "  " $6 " " $7 "  " $5 "  " $8}' )
