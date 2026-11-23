#!/usr/bin/env bash
# HU-29: genera el zip del código de una release (el entregable «código fuente comprimido») con `git archive` y lo revisa.
# Lo usa .github/workflows/release.yml y se puede correr a mano.
# Uso: scripts/empaquetar_release.sh <tag|rama|commit> [carpeta_de_salida]   (por defecto: dist/)
# Resultado: <salida>/erp-donofrio-<tag>.zip  (la carpeta raíz dentro del zip se llama erp-donofrio-<tag>/)
set -euo pipefail
cd "$(dirname "$0")/.."

ref="${1:?Uso: scripts/empaquetar_release.sh <tag|rama|commit> [carpeta_de_salida]}"
salida="${2:-dist}"
git rev-parse --verify --quiet "$ref^{commit}" >/dev/null || { echo "No existe '$ref' en este repositorio" >&2; exit 1; }
nombre="erp-donofrio-${ref//\//-}"
zip="$salida/$nombre.zip"

mkdir -p "$salida"
git archive --format=zip --prefix="$nombre/" -o "$zip" "$ref"

lista="$(unzip -Z1 "$zip")"
falta=0
for obligatorio in README.md docker-compose.yml .env.example docker/odoo/Dockerfile scripts/init_db.sh \
                   addons/donofrio_base/__manifest__.py docs/manuales/manual_instalacion.md; do
  grep -qx "$nombre/$obligatorio" <<<"$lista" || { echo "FALTA en el zip: $obligatorio" >&2; falta=1; }
done
# Nunca deben viajar secretos ni archivos de entorno reales
if grep -E "^$nombre/(\.env|secrets/|.*\.(key|pem))$" <<<"$lista"; then echo "El zip contiene secretos" >&2; falta=1; fi
[ "$falta" -eq 0 ] || exit 1

echo "$zip: $(du -h "$zip" | cut -f1), $(grep -c . <<<"$lista") entradas"
