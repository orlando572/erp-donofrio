#!/bin/bash
# Se ejecuta solo la primera vez que se crea el volumen pgdata (docker-entrypoint-initdb.d).
# Crea el rol de Odoo SIN superusuario (06 §6.5): puede crear bases de datos, nada más.
set -euo pipefail

psql -v ON_ERROR_STOP=1 -v usuario="$ODOO_DB_USER" -v clave="$ODOO_DB_PASSWORD" \
     --username "$POSTGRES_USER" --dbname postgres <<'SQL'
CREATE ROLE :"usuario" LOGIN CREATEDB NOSUPERUSER PASSWORD :'clave';
SQL
