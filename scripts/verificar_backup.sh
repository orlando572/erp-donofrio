#!/usr/bin/env bash
# HU-26: prueba el ciclo completo respaldo → restauración en una BD nueva → comparación → limpieza,
# más la retención de 7 días. Usa una carpeta temporal y una BD temporal; no toca tus respaldos.
# Requiere la BD de Odoo creada (scripts/init_db.sh). Uso: scripts/verificar_backup.sh
set -uo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && { set -a; . ./.env; set +a; }

DB="${ODOO_DB:-donofrio}"
TMP_BK="$(mktemp -d)"
NUEVA="${DB}_verif_$(date +%H%M%S)"
fallos=0
ok()    { echo "  OK    $*"; }
fallo() { echo "  FALLO $*"; fallos=$((fallos + 1)); }
psqlq() { docker compose exec -T db psql -U postgres -d "$1" -X -tA -c "$2"; }
cuentas() { psqlq "$1" "SELECT (SELECT count(*) FROM ir_module_module WHERE state='installed') || '/' || (SELECT count(*) FROM res_users) || '/' || (SELECT count(*) FROM ir_attachment) || '/' || (SELECT count(*) FROM res_partner)"; }
archivos() { docker compose run --rm --no-deps -T --entrypoint bash odoo -c 'find "/var/lib/odoo/filestore/$0" -type f 2>/dev/null | wc -l' "$1"; }
limpiar() {
  docker compose exec -T db dropdb -U postgres --if-exists "$NUEVA" >/dev/null 2>&1
  docker compose run --rm --no-deps -T --entrypoint bash odoo -c 'rm -rf "/var/lib/odoo/filestore/$0"' "$NUEVA" >/dev/null 2>&1
  rm -rf "$TMP_BK"
}
trap limpiar EXIT

echo "1) Respaldo de '$DB'"
BACKUP_DIR="$TMP_BK" scripts/backup.sh >/dev/null 2>"$TMP_BK/err.log" || { cat "$TMP_BK/err.log" >&2; fallo "backup.sh falló"; exit 1; }
dump="$(ls "$TMP_BK"/"$DB"_*.dump 2>/dev/null | head -1)"
[ -s "$dump" ] && [ -s "${dump%.dump}_filestore.tar.gz" ] && [ -s "${dump%.dump}.sha256" ] \
  && ok "dump, filestore y sumas generados ($(du -h "$dump" | cut -f1))" || fallo "faltan archivos del respaldo"

echo "2) Restauración en una BD nueva ('$NUEVA')"
salida="$(scripts/restore.sh "${dump%.dump}" "$NUEVA" 2>&1)"; estado=$?
echo "$salida" | grep -E "RTO medido|ERROR"
[ "$estado" -eq 0 ] && ok "restore.sh terminó bien" || fallo "restore.sh falló (código $estado)"

echo "3) La BD restaurada coincide con la original (módulos/usuarios/adjuntos/contactos y archivos del filestore)"
a="$(cuentas "$DB")"; b="$(cuentas "$NUEVA")"
[ -n "$a" ] && [ "$a" = "$b" ] && ok "tablas: $a = $b" || fallo "tablas: original '$a' contra restaurada '$b'"
fa="$(archivos "$DB")"; fb="$(archivos "$NUEVA")"
[ "$fa" = "$fb" ] && ok "filestore: $fa archivos en las dos" || fallo "filestore: original $fa contra restaurada $fb"

echo "4) restore.sh no sobrescribe una BD existente"
scripts/restore.sh "${dump%.dump}" "$NUEVA" >/dev/null 2>&1 && fallo "restauró sobre una BD existente" || ok "se negó a sobrescribir '$NUEVA'"

echo "5) Sumas de verificación: un respaldo alterado se rechaza"
echo corrupto >> "$dump"
scripts/restore.sh "${dump%.dump}" "${NUEVA}_x" >/dev/null 2>&1 && fallo "aceptó un respaldo alterado" || ok "rechazó el respaldo alterado"

echo "6) Retención de 7 días"
viejo="$TMP_BK/${DB}_20200101_020000.dump"; reciente="$TMP_BK/${DB}_20200101_020001.dump"
touch -d '8 days ago' "$viejo"; touch -d '6 days ago' "$reciente"
BACKUP_DIR="$TMP_BK" scripts/backup.sh >/dev/null 2>&1
[ ! -e "$viejo" ] && [ -e "$reciente" ] && ok "borró el de 8 días y conservó el de 6" || fallo "la retención no se comportó como se esperaba"

echo
if [ "$fallos" -eq 0 ]; then echo "Respaldo y restauración verificados."; else echo "$fallos comprobación(es) fallaron." >&2; exit 1; fi
