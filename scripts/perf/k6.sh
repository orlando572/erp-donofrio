#!/usr/bin/env bash
# HU-28 (RNF002): prueba de carga con k6 (20 usuarios virtuales) contra el despliegue protegido.
# Requiere:  scripts/levantar_prod.sh  (Nginx con TLS en https://localhost:8443) y la BD con datos de demostración.
# k6 corre con su imagen de Docker (no se instala nada en el equipo); usa la red del equipo para llegar a localhost.
# Las contraseñas de los usuarios de prueba salen de DONOFRIO_USER_PASSWORD (.env) y no se escriben en ningún reporte.
#
# Uso:       scripts/perf/k6.sh
# Opciones por variable de entorno:  VUS=20  DURACION=3m  PAUSA=1 (0 = sin pausas, prueba de esfuerzo)
#            ODOO_DB=donofrio  BASE_URL=https://localhost:8443
#            SALIDA=scripts/perf/resultados (carpeta ignorada por git)
# Salida en $SALIDA:  k6-resumen.json (métricas), k6-consola.txt (resumen en texto), docker-stats.txt (CPU y memoria).
set -euo pipefail
cd "$(dirname "$0")/../.."

K6_IMAGEN="grafana/k6:1.7.1"

[ -f .env ] || { echo "Falta .env: ejecuta  cp .env.example .env" >&2; exit 1; }
# Solo se toman las variables que se necesitan (no se hace 'source' de todo el .env)
leer() { grep -E "^$1=" .env | head -1 | cut -d= -f2- || true; }
DONOFRIO_USER_PASSWORD="${DONOFRIO_USER_PASSWORD:-$(leer DONOFRIO_USER_PASSWORD)}"; export DONOFRIO_USER_PASSWORD
[ -n "$DONOFRIO_USER_PASSWORD" ] || { echo "Falta DONOFRIO_USER_PASSWORD en .env (contraseña de los usuarios de prueba)" >&2; exit 1; }
bd="${ODOO_DB:-$(leer ODOO_DB)}"; bd="${bd:-donofrio}"
puerto="${NGINX_HTTPS_PORT:-$(leer NGINX_HTTPS_PORT)}"; puerto="${puerto:-8443}"
base="${BASE_URL:-https://localhost:${puerto}}"
salida="${SALIDA:-scripts/perf/resultados}"
mkdir -p "$salida"
salida="$(cd "$salida" && pwd)"

# Se comprueba que el despliegue protegido responde antes de empezar
curl -sk -o /dev/null -m 15 -f "$base/web/login" || { echo "No responde $base/web/login: ejecuta scripts/levantar_prod.sh" >&2; exit 1; }

# Muestras de CPU y memoria de los contenedores mientras corre la prueba (cada 10 s)
(
  while true; do
    echo "# $(date '+%H:%M:%S')"
    docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' | grep -E 'NAME|erp-donofrio-(odoo|db|nginx)-1' || true
    sleep 10
  done
) > "$salida/docker-stats.txt" 2>&1 &
muestreo=$!
trap 'kill "$muestreo" 2>/dev/null || true' EXIT

echo "k6 ${K6_IMAGEN}: ${VUS:-20} usuarios virtuales contra $base (BD $bd), duración ${DURACION:-3m} con todos activos"
set +e
docker run --rm --network host --user "$(id -u):$(id -g)" \
  -e BASE_URL="$base" -e ODOO_DB="$bd" -e VUS="${VUS:-20}" -e DURACION="${DURACION:-3m}" -e PAUSA="${PAUSA:-1}" \
  -e DONOFRIO_USER_PASSWORD \
  -v "$PWD/scripts/perf:/scripts:ro" -v "$salida:/salida" \
  "$K6_IMAGEN" run --no-color --quiet --summary-export /salida/k6-resumen.json /scripts/carga.js 2>&1 | tee "$salida/k6-consola.txt"
estado=${PIPESTATUS[0]}
set -e

kill "$muestreo" 2>/dev/null || true
echo
echo "Reportes en $salida (k6-resumen.json, k6-consola.txt, docker-stats.txt)"
if [ "$estado" -eq 0 ]; then echo "k6: todos los umbrales se cumplieron."; else echo "k6: algún umbral no se cumplió (código $estado)." >&2; fi
exit "$estado"
