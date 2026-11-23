#!/bin/bash
# Genera /tmp/odoo.conf desde la plantilla y delega en el entrypoint oficial de la imagen.
set -euo pipefail
umask 077

: "${ODOO_DB:?Falta ODOO_DB (defínela en .env)}"
: "${ODOO_ADMIN_PASSWD:?Falta ODOO_ADMIN_PASSWD (defínela en .env)}"

# En bash 5.2 el '&' del reemplazo es especial; se desactiva para aceptar cualquier contraseña.
shopt -u patsub_replacement 2>/dev/null || true

conf="$(< /etc/odoo/odoo.conf.template)"
conf="${conf//\$\{ODOO_DB\}/${ODOO_DB}}"
conf="${conf//\$\{ODOO_ADMIN_PASSWD\}/${ODOO_ADMIN_PASSWD}}"
printf '%s\n' "$conf" > /tmp/odoo.conf

export ODOO_RC=/tmp/odoo.conf
exec /entrypoint.sh "$@"
