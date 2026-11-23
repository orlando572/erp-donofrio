#!/usr/bin/env bash
# HU-28 (RNF009, OWASP A05): análisis de seguridad con OWASP ZAP baseline (reglas pasivas + araña de 1 minuto)
# contra el despliegue protegido (Nginx con TLS). ZAP corre con su imagen de Docker; no se instala nada en el equipo.
# Requiere:  scripts/levantar_prod.sh  (https://localhost:8443).
#
# Uso:       scripts/perf/zap.sh
# Opciones:  SALIDA=scripts/perf/resultados (carpeta ignorada por git)   URL_OBJETIVO=https://localhost:8443
# Salida en $SALIDA:  zap-reporte.html, zap-reporte.json, zap-reporte.md, zap-consola.txt
# Criterio de la HU-28: sin alertas de riesgo ALTO. Cada alerta media o baja se corrige en docker/nginx/ o se
# acepta con su motivo en scripts/perf/zap-reglas.conf. El script falla si el reporte trae alguna alerta alta.
set -euo pipefail
cd "$(dirname "$0")/../.."

ZAP_IMAGEN="ghcr.io/zaproxy/zaproxy:2.17.0"

[ -f .env ] && puerto="$(grep -E '^NGINX_HTTPS_PORT=' .env | cut -d= -f2)" || puerto=""
objetivo="${URL_OBJETIVO:-https://localhost:${NGINX_HTTPS_PORT:-${puerto:-8443}}}"
salida="${SALIDA:-scripts/perf/resultados}"
mkdir -p "$salida"
salida="$(cd "$salida" && pwd)"
curl -sk -o /dev/null -m 15 -f "$objetivo/web/login" || { echo "No responde $objetivo/web/login: ejecuta scripts/levantar_prod.sh" >&2; exit 1; }

# El usuario «zap» del contenedor (uid 1000) debe poder escribir en la carpeta de reportes
cp scripts/perf/zap-reglas.conf "$salida/zap-reglas.conf"
chmod 777 "$salida"
chmod 666 "$salida/zap-reglas.conf"
rm -f "$salida"/zap-reporte.*

echo "ZAP ${ZAP_IMAGEN}: baseline contra $objetivo"
# -T 5: araña de 5 minutos como máximo (el sitio sin sesión es pequeño y termina antes) · -j: araña AJAX no
# (Odoo es una SPA que sin sesión solo muestra el login) · -c: reglas aceptadas con su motivo
set +e
docker run --rm --network host -v "$salida:/zap/wrk:rw" "$ZAP_IMAGEN" \
  zap-baseline.py -t "$objetivo/web/login" -c zap-reglas.conf -T 5 \
  -r zap-reporte.html -J zap-reporte.json -w zap-reporte.md 2>&1 | tee "$salida/zap-consola.txt"
estado=${PIPESTATUS[0]}
set -e
echo "zap-baseline terminó con código $estado (0 limpio, 1 FAIL, 2 avisos, 3 error de ejecución)"
[ "$estado" -le 2 ] || { echo "ZAP no pudo ejecutarse bien (código $estado)" >&2; exit "$estado"; }

# Conteo por nivel de riesgo desde el JSON (riskcode: 3 alto, 2 medio, 1 bajo, 0 informativo)
python3 -I - "$salida/zap-reporte.json" <<'PY'
import json, sys
datos = json.load(open(sys.argv[1]))
n = {3: 0, 2: 0, 1: 0, 0: 0}
detalle = []
for sitio in datos.get('site', []):
    for a in sitio.get('alerts', []):
        r = int(a['riskcode'])
        n[r] += 1
        detalle.append((r, a['pluginid'], a['name'], len(a.get('instances', []))))
print('Alertas por nivel:  Alto %d · Medio %d · Bajo %d · Informativo %d' % (n[3], n[2], n[1], n[0]))
for r, pid, nombre, inst in sorted(detalle, reverse=True):
    print('  %-12s %-6s %s (%d instancias)' % (['Informativo', 'Bajo', 'Medio', 'Alto'][r], pid, nombre, inst))
if n[3]:
    print('FALLO: hay alertas de riesgo alto.', file=sys.stderr)
    sys.exit(1)
PY
echo "Reportes en $salida (zap-reporte.html, zap-reporte.json, zap-reporte.md, zap-consola.txt)"
