#!/usr/bin/env bash
# HU-27: levanta el despliegue protegido: Odoo con workers=2 y proxy_mode, detrás de Nginx con TLS (perfil proxy).
# Requiere la BD creada (scripts/init_db.sh) y en .env una ODOO_ADMIN_PASSWD de 16 caracteres o más
# (el entrypoint de Odoo se niega a arrancar en este modo con la contraseña de ejemplo).
# Uso: scripts/levantar_prod.sh          Para volver a desarrollo: docker compose --profile proxy down && docker compose up -d
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] || { echo "Falta .env: ejecuta  cp .env.example .env" >&2; exit 1; }

scripts/generar_certificado.sh
export ODOO_WORKERS="${ODOO_WORKERS_PROD:-2}" ODOO_PROXY_MODE=True
docker compose --profile proxy up -d --build --wait
puerto="${NGINX_HTTPS_PORT:-$(grep -E '^NGINX_HTTPS_PORT=' .env | cut -d= -f2)}"
echo "Listo: https://localhost:${puerto:-8443}  (certificado autofirmado: acepta la advertencia del navegador)"
