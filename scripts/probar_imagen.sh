#!/usr/bin/env bash
# HU-29: humo de la imagen publicada: Odoo 19, los módulos propios y auditlog (OCA) están dentro y la configuración
# se genera bien con y sin el modo producción. Lo usa release.yml antes de publicar; sirve igual a mano.
# Uso: scripts/probar_imagen.sh <imagen[:tag]>
set -euo pipefail
imagen="${1:?Uso: scripts/probar_imagen.sh <imagen[:tag]>}"
correr() { docker run --rm -e ODOO_DB=humo -e ODOO_ADMIN_PASSWD="$ADMIN" "${@}"; }

ADMIN="una-clave-maestra-de-prueba-2026"
echo "1) Versión de Odoo"
v="$(correr --entrypoint odoo "$imagen" --version)"; echo "  $v"
grep -q "19\.0" <<<"$v" || { echo "La imagen no es Odoo 19.0" >&2; exit 1; }

echo "2) Módulos propios y auditlog (OCA) dentro de la imagen"
correr --entrypoint ls "$imagen" /mnt/extra-addons/donofrio_base/__manifest__.py /opt/oca/auditlog/__manifest__.py

echo "3) La configuración se genera (desarrollo)"
dev="$(correr --entrypoint bash "$imagen" -c '/usr/local/bin/donofrio-entrypoint.sh true; grep -E "^(workers|proxy_mode|list_db|addons_path)" /tmp/odoo.conf' 2>&1 || true)"
echo "$dev" | sed 's/^/  dev:  /'
grep -q "list_db = False" <<<"$dev" || { echo "Configuración incorrecta: list_db debe ser False" >&2; exit 1; }
grep -q "addons_path = /mnt/extra-addons,/opt/oca" <<<"$dev" || { echo "addons_path no incluye /opt/oca" >&2; exit 1; }

echo "4) Modo producción (workers, proxy_mode y rechazo de la contraseña de ejemplo)"
prod="$(docker run --rm -e ODOO_DB=humo -e ODOO_ADMIN_PASSWD="$ADMIN" -e ODOO_WORKERS=2 -e ODOO_PROXY_MODE=True \
  --entrypoint bash "$imagen" -c '/usr/local/bin/donofrio-entrypoint.sh true; grep -E "^(workers|proxy_mode)" /tmp/odoo.conf' 2>&1 || true)"
echo "$prod" | sed 's/^/  prod: /'
grep -q "proxy_mode = True" <<<"$prod" || { echo "Configuración de producción incorrecta" >&2; exit 1; }
rechazo="$(docker run --rm -e ODOO_DB=humo -e ODOO_ADMIN_PASSWD=cambiar-admin-passwd -e ODOO_PROXY_MODE=True \
  --entrypoint /usr/local/bin/donofrio-entrypoint.sh "$imagen" true 2>&1 || true)"
grep -q "contraseña maestra" <<<"$rechazo" || { echo "La imagen no rechazó la contraseña de ejemplo en producción: $rechazo" >&2; exit 1; }
echo "  la contraseña de ejemplo se rechaza, como se espera"
echo "Imagen verificada: $imagen"
