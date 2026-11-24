#!/bin/bash
# Standby en caliente (hot standby) de PostgreSQL 16, solo lectura (HU-25, 06 §6.5).
# Primera vez (volumen vacío): crea el rol 'replicador' y el slot en el primario y copia la base con
# pg_basebackup -R. Siguientes veces: solo arranca y sigue al primario.
# Es idempotente: sirve igual con un primario nuevo o con uno que ya tenía datos.
set -euo pipefail

: "${PRIMARIO_HOST:=db}"
: "${REPLICA_SLOT:=donofrio_replica}"
: "${POSTGRES_PASSWORD:?Falta POSTGRES_PASSWORD}"
: "${REPLICADOR_PASSWORD:?Falta REPLICADOR_PASSWORD en .env (ver .env.example)}"
PGDATA="${PGDATA:-/var/lib/postgresql/data}"

if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "[replica] Esperando al primario ($PRIMARIO_HOST)..."
  until PGPASSWORD="$POSTGRES_PASSWORD" pg_isready -q -h "$PRIMARIO_HOST" -U postgres; do sleep 2; done

  echo "[replica] Preparando el rol 'replicador' y el slot '$REPLICA_SLOT' en el primario"
  PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 -h "$PRIMARIO_HOST" -U postgres -d postgres \
    -v clave="$REPLICADOR_PASSWORD" -v slot="$REPLICA_SLOT" <<'SQL'
SELECT NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'replicador') AS crear \gset
\if :crear
  CREATE ROLE replicador LOGIN REPLICATION NOSUPERUSER PASSWORD :'clave';
\else
  ALTER ROLE replicador WITH LOGIN REPLICATION PASSWORD :'clave';
\endif
SELECT pg_create_physical_replication_slot(:'slot')
 WHERE NOT EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = :'slot');
SQL

  echo "[replica] Copiando la base del primario (pg_basebackup)..."
  mkdir -p "$PGDATA"
  chown postgres:postgres "$PGDATA"
  chmod 700 "$PGDATA"
  PGPASSWORD="$REPLICADOR_PASSWORD" gosu postgres pg_basebackup \
    -h "$PRIMARIO_HOST" -U replicador -D "$PGDATA" -X stream -R -S "$REPLICA_SLOT" -P
  echo "[replica] Copia lista."
fi

exec docker-entrypoint.sh postgres -c hot_standby=on
