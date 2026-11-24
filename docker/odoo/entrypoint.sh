#!/bin/bash
# Genera /tmp/odoo.conf desde la plantilla y delega en el entrypoint oficial de la imagen.
set -euo pipefail
umask 077

: "${ODOO_DB:?Falta ODOO_DB (defínela en .env)}"

# La contraseña maestra puede venir de un secreto montado (ODOO_ADMIN_PASSWD_FILE, p. ej. /run/secrets/...)
# o de la variable ODOO_ADMIN_PASSWD (.env). El archivo tiene prioridad.
if [ -n "${ODOO_ADMIN_PASSWD_FILE:-}" ]; then
  [ -r "$ODOO_ADMIN_PASSWD_FILE" ] || { echo "No se puede leer ODOO_ADMIN_PASSWD_FILE=$ODOO_ADMIN_PASSWD_FILE" >&2; exit 1; }
  ODOO_ADMIN_PASSWD="$(< "$ODOO_ADMIN_PASSWD_FILE")"
fi
: "${ODOO_ADMIN_PASSWD:?Falta ODOO_ADMIN_PASSWD o ODOO_ADMIN_PASSWD_FILE}"

ODOO_WORKERS="${ODOO_WORKERS:-0}"
ODOO_PROXY_MODE="${ODOO_PROXY_MODE:-False}"
[[ "$ODOO_WORKERS" =~ ^[0-9]+$ ]] || { echo "ODOO_WORKERS debe ser un número entero (es '$ODOO_WORKERS')" >&2; exit 1; }
[[ "$ODOO_PROXY_MODE" =~ ^(True|False)$ ]] || { echo "ODOO_PROXY_MODE debe ser True o False (es '$ODOO_PROXY_MODE')" >&2; exit 1; }

# Con proxy_mode (despliegue protegido) la contraseña maestra no puede ser la de ejemplo ni corta (RNF009, A05).
if [ "$ODOO_PROXY_MODE" = "True" ]; then
  if [ "${#ODOO_ADMIN_PASSWD}" -lt 16 ] || [[ "$ODOO_ADMIN_PASSWD" == cambiar-* ]]; then
    echo "Despliegue protegido: la contraseña maestra (admin_passwd) debe tener 16 caracteres o más y no ser la de ejemplo." >&2
    exit 1
  fi
fi

# En bash 5.2 el '&' del reemplazo es especial; se desactiva para aceptar cualquier contraseña.
shopt -u patsub_replacement 2>/dev/null || true

conf="$(< /etc/odoo/odoo.conf.template)"
conf="${conf//\$\{ODOO_DB\}/${ODOO_DB}}"
conf="${conf//\$\{ODOO_ADMIN_PASSWD\}/${ODOO_ADMIN_PASSWD}}"
conf="${conf//\$\{ODOO_WORKERS\}/${ODOO_WORKERS}}"
conf="${conf//\$\{ODOO_PROXY_MODE\}/${ODOO_PROXY_MODE}}"
printf '%s\n' "$conf" > /tmp/odoo.conf

export ODOO_RC=/tmp/odoo.conf
exec /entrypoint.sh "$@"
