#!/usr/bin/env bash
# HU-27: comprueba el despliegue protegido (Nginx + TLS + Odoo en modo producción) y deja las evidencias.
# Requiere:  scripts/levantar_prod.sh   (con la BD creada).   Uso: scripts/verificar_despliegue.sh
set -uo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && puerto="$(grep -E '^NGINX_HTTPS_PORT=' .env | cut -d= -f2)"
HTTPS="${NGINX_HTTPS_PORT:-${puerto:-8443}}"
http_port="$(grep -E '^NGINX_HTTP_PORT=' .env 2>/dev/null | cut -d= -f2)"; HTTP="${NGINX_HTTP_PORT:-${http_port:-8080}}"
U="https://localhost:$HTTPS"
fallos=0
ok()    { echo "  OK    $*"; }
fallo() { echo "  FALLO $*"; fallos=$((fallos + 1)); }
cabeceras() { curl -sk -I -m 15 "$@"; }
cuenta() { grep -ci "^$1:" <<<"$2" || true; }

echo "1) HTTP redirige a HTTPS"
r="$(curl -s -I -m 15 "http://localhost:$HTTP/web/login")"
echo "$r" | head -1 | grep -q " 301 " && echo "$r" | grep -qi "^location: https://" && ok "80 → 443 (301)" || fallo "no redirige: $(echo "$r" | head -1)"

echo "2) Versiones de TLS"
# curl en lugar de openssl s_client: la salida de openssl cambia entre versiones (y con 1.3 no siempre imprime el protocolo)
curl -sk --tlsv1.2 --tls-max 1.2 -o /dev/null -m 15 "$U/web/login" && ok "acepta TLS 1.2" || fallo "no acepta TLS 1.2"
curl -sk --tlsv1.3 --tls-max 1.3 -o /dev/null -m 15 "$U/web/login" && ok "acepta TLS 1.3" || fallo "no acepta TLS 1.3"
curl -sk --tls-max 1.1 -o /dev/null -m 15 "$U/web/login" 2>/dev/null && fallo "acepta TLS 1.1 o menor" || ok "rechaza TLS 1.1 y menores"

echo "3) Cabeceras de seguridad en el login (cada una una sola vez)"
h="$(cabeceras "$U/web/login")"
for c in Strict-Transport-Security X-Content-Type-Options X-Frame-Options Referrer-Policy; do
  [ "$(cuenta "$c" "$h")" = "1" ] && ok "$c: $(grep -i "^$c:" <<<"$h" | cut -d: -f2- | tr -d '\r' | xargs)" || fallo "$c aparece $(cuenta "$c" "$h") veces"
done
grep -i "^server:" <<<"$h" | grep -q "[0-9]" && fallo "la cabecera Server revela la versión" || ok "Server sin versión ($(grep -i '^server:' <<<"$h" | tr -d '\r'))"

echo "4) El gestor de bases de datos no se publica"
[ "$(curl -sk -o /dev/null -w '%{http_code}' -m 15 "$U/web/database/manager")" = "404" ] && ok "/web/database/manager → 404" || fallo "/web/database/manager responde"
[ "$(curl -sk -o /dev/null -w '%{http_code}' -m 15 -X POST -d 'master_pwd=x&name=x' "$U/web/database/create")" = "404" ] && ok "/web/database/create → 404" || fallo "/web/database/create responde"

echo "5) Compresión, caché de assets y websocket"
curl -sk -H 'Accept-Encoding: gzip' -I -m 15 "$U/web/login" | grep -qi "^content-encoding: gzip" && ok "gzip en el login" || fallo "sin gzip"
asset="$(curl -sk -m 15 "$U/web/login" | grep -oE '/web/assets/[^"]+\.css' | head -1)"
ac="$(cabeceras -H 'Accept-Encoding: gzip' "$U$asset")"
grep -qi "^cache-control:.*max-age=31536000" <<<"$ac" && ok "assets con Cache-Control de un año ($asset)" || fallo "assets sin caché: $asset"
grep -qi "^content-encoding: gzip" <<<"$ac" && ok "assets comprimidos" || fallo "assets sin gzip"
ws="$(curl -sk --http1.1 -i -m 5 -H 'Connection: Upgrade' -H 'Upgrade: websocket' -H 'Sec-WebSocket-Version: 13' \
  -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==' -H "Origin: $U" "$U/websocket" | head -1)"
echo "$ws" | grep -q " 101 " && ok "/websocket se actualiza a 101 (puerto 8072)" || fallo "websocket: ${ws:-sin respuesta}"

echo "6) Odoo en modo producción"
conf="$(docker compose exec -T odoo cat /tmp/odoo.conf 2>/dev/null)"
for k in "workers = 2" "proxy_mode = True" "list_db = False"; do
  grep -q "^$k" <<<"$conf" && ok "odoo.conf: $k" || fallo "odoo.conf no tiene '$k'"
done
grep -qE "^admin_passwd = (cambiar-|.{0,15}$)" <<<"$conf" && fallo "admin_passwd es débil" || ok "admin_passwd de 16 o más caracteres, no la de ejemplo"
docker compose run --rm --no-deps -T -e ODOO_PROXY_MODE=True -e ODOO_ADMIN_PASSWD=cambiar-admin-passwd odoo odoo --version >/dev/null 2>&1 \
  && fallo "Odoo arrancó en modo producción con la contraseña de ejemplo" || ok "Odoo se niega a arrancar en producción con la contraseña de ejemplo"

echo "7) Bloqueo por intentos fallidos (base.login_cooldown_*)"
# El contador de Odoo es por IP y por worker (no se comparte entre procesos). Se lee el umbral real de la BD
# (5 con donofrio_base; 10, el de Odoo, en una BD solo con 'base') y los workers de odoo.conf: con N workers y un
# umbral U, el intento N*U + 1 se rechaza seguro.
bd="${ODOO_DB:-$(grep -E '^ODOO_DB=' .env 2>/dev/null | cut -d= -f2)}"; bd="${bd:-donofrio}"
umbral="$(docker compose exec -T db psql -U postgres -d "$bd" -tAc "SELECT value FROM ir_config_parameter WHERE key = 'base.login_cooldown_after'" 2>/dev/null | tr -d '[:space:]')"
umbral="${umbral:-10}"
workers="$(grep -E '^workers = ' <<<"$conf" | cut -d= -f2 | tr -d '[:space:]')"; workers="${workers:-2}"
intentos=$((workers * umbral + 2))
echo "  umbral $umbral fallos, $workers workers: se hacen $intentos intentos"
jar="$(mktemp)"
bloqueados=0
for i in $(seq 1 "$intentos"); do
  tok="$(curl -sk -c "$jar" -b "$jar" -m 15 "$U/web/login" | grep -oE 'name="csrf_token" value="[^"]+"' | head -1 | sed 's/.*value="//;s/"//')"
  resp="$(curl -sk -c "$jar" -b "$jar" -m 15 -d "csrf_token=$tok&login=admin&password=incorrecta-$i" "$U/web/login" | sed 's/<[^>]*>/ /g' | tr -s ' \n' ' ')"
  grep -qi "too many login failures" <<<"$resp" && bloqueados=$((bloqueados + 1))
done
rm -f "$jar"
[ "$bloqueados" -ge 1 ] && ok "de $intentos intentos fallidos seguidos, $bloqueados se rechazaron por bloqueo (\"Too many login failures\")" || fallo "ningún intento se bloqueó"
registro="$(docker compose logs --no-color --tail=2000 odoo 2>/dev/null)"
grep -q "Login attempt ignored" <<<"$registro" && ok "el bloqueo quedó en el registro de Odoo (Login attempt ignored)" || fallo "no hay 'Login attempt ignored' en el registro"

echo
if [ "$fallos" -eq 0 ]; then echo "Despliegue protegido verificado: todas las comprobaciones pasaron."; else echo "$fallos comprobación(es) fallaron." >&2; exit 1; fi
