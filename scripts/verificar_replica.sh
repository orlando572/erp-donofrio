#!/usr/bin/env bash
# HU-25 (06 §6.5, sección 5.9): comprueba la réplica en streaming y deja las evidencias.
# Requiere:  docker compose --profile replica up -d --wait
# Uso: scripts/verificar_replica.sh      (sale con error si falla alguna comprobación)
set -uo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && { set -a; . ./.env; set +a; }

DB_USER="${ODOO_DB_USER:-odoo}"
fallos=0
ok()   { echo "  OK    $*"; }
fallo() { echo "  FALLO $*"; fallos=$((fallos + 1)); }
primario() { docker compose exec -T db psql -U postgres -d postgres -tAX "$@"; }
replica()  { docker compose exec -T db-replica psql -U postgres -d postgres -tAX "$@"; }

echo "1) Primario: pg_stat_replication"
estado="$(primario -c "SELECT state || '/' || sync_state FROM pg_stat_replication")"
primario -c "SELECT client_addr, state, sync_state, replay_lag FROM pg_stat_replication"
[ "$estado" = "streaming/async" ] && ok "la réplica está en streaming (asíncrona)" || fallo "pg_stat_replication dice '${estado:-vacío}'"

echo "2) Réplica: pg_is_in_recovery()"
[ "$(replica -c "SELECT pg_is_in_recovery()")" = "t" ] && ok "la réplica está en recuperación (standby)" || fallo "la réplica no es un standby"

echo "3) Un dato escrito en el primario se lee en la réplica"
valor="hu25_$(date +%s)"
primario -c "CREATE TABLE IF NOT EXISTS verificacion_replica (valor text, creado timestamptz DEFAULT now())" >/dev/null
primario -c "INSERT INTO verificacion_replica (valor) VALUES ('$valor')" >/dev/null
leido=""
for _ in $(seq 1 20); do
  leido="$(replica -c "SELECT valor FROM verificacion_replica WHERE valor = '$valor'" 2>/dev/null)"
  [ "$leido" = "$valor" ] && break
  sleep 1
done
[ "$leido" = "$valor" ] && ok "'$valor' llegó a la réplica" || fallo "'$valor' no llegó a la réplica en 20 s"

echo "4) La réplica rechaza escrituras (solo lectura)"
salida="$(docker compose exec -T -e PGPASSWORD="${ODOO_DB_PASSWORD:-}" db-replica \
  psql -h localhost -U "$DB_USER" -d postgres -tAX \
  -c "INSERT INTO verificacion_replica (valor) VALUES ('no-debe-entrar')" 2>&1)"
echo "  $salida"
echo "$salida" | grep -q "read-only transaction" && ok "INSERT en la réplica rechazado" || fallo "la réplica aceptó (o no entendió) la escritura"

echo "5) El rol de Odoo no es superusuario ni de replicación"
[ "$(primario -c "SELECT rolsuper OR rolreplication FROM pg_roles WHERE rolname = '$DB_USER'")" = "f" ] \
  && ok "el rol '$DB_USER' no puede replicar ni es superusuario" || fallo "el rol '$DB_USER' tiene privilegios de más"

primario -c "DROP TABLE IF EXISTS verificacion_replica" >/dev/null
echo
if [ "$fallos" -eq 0 ]; then echo "Réplica verificada: todas las comprobaciones pasaron."; else echo "$fallos comprobación(es) fallaron." >&2; exit 1; fi
