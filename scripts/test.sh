#!/usr/bin/env bash
# Instala módulos en una BD nueva con --test-enable, corre SOLO sus tests y muestra solo los errores.
# Sale con código distinto de 0 si Odoo falla, si hay ERROR/CRITICAL/FAIL/Traceback en el log
# o si no se ejecutó ninguna prueba (para que un filtro mal puesto no dé un falso verde).
# Uso: scripts/test.sh [modulo ...]     (sin argumentos: todos los módulos de addons/)
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env ] || { echo "Falta .env: ejecuta  cp .env.example .env" >&2; exit 1; }

if [ "$#" -gt 0 ]; then
  modulos=("$@")
else
  modulos=()
  for manifest in addons/*/__manifest__.py; do
    [ -e "$manifest" ] && modulos+=("$(basename "$(dirname "$manifest")")")
  done
fi
[ "${#modulos[@]}" -gt 0 ] || { echo "No hay módulos en addons/" >&2; exit 1; }

lista="$(IFS=,; echo "${modulos[*]}")"
tags="$(printf '/%s,' "${modulos[@]}")"; tags="${tags%,}"
db="test_$(date +%s)_$$"
log="$(mktemp)"

limpiar() {
  docker compose exec -T db psql -U postgres -d postgres -qc "DROP DATABASE IF EXISTS \"${db}\" WITH (FORCE)" >/dev/null 2>&1 || true
  rm -f "$log"
}
trap limpiar EXIT

echo "Probando: ${lista}  (BD temporal ${db})"
docker compose up -d --wait db

rc=0
# --db-filter propio: el healthcheck del compose consulta /web/health mientras corren los tests y,
# con el dbfilter de odoo.conf (la BD de desarrollo), Odoo intentaría cargar esa otra BD.
docker compose run --rm -T odoo odoo -d "$db" --db-filter "^${db}\$" -i "$lista" \
  --test-enable --test-tags "$tags" --stop-after-init --log-level=test >"$log" 2>&1 || rc=$?

resumen="$(grep -E 'of [0-9]+ tests' "$log" | tail -n 1 || true)"
errores="$(grep -E -A12 ' (ERROR|CRITICAL) |^FAIL:|Traceback' "$log" | head -n 80 || true)"
pruebas="$(grep -Eo 'of [0-9]+ tests' "$log" | tail -n 1 | grep -Eo '[0-9]+' || echo 0)"

if [ -n "$errores" ]; then
  echo "$errores"
fi
[ -n "$resumen" ] && echo "$resumen"

if [ "$rc" -ne 0 ] || [ -n "$errores" ]; then
  echo "FALLÓ (código de Odoo: ${rc}). Log completo:" >&2
  [ -n "$errores" ] || tail -n 40 "$log" >&2
  exit 1
fi
if [ "$pruebas" -eq 0 ]; then
  echo "FALLÓ: no se ejecutó ninguna prueba (revisa --test-tags: ${tags})" >&2
  exit 1
fi
echo "OK: ${lista} instalado y ${pruebas} pruebas sin errores."
