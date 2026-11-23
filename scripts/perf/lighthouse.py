#!/usr/bin/env python3
"""HU-28: mide el rendimiento web (WPO) con Lighthouse en el login, el backend y el dashboard.

Uso:  scripts/perf/lighthouse.py ANTES  http://host.docker.internal:8069  --debug-assets
      scripts/perf/lighthouse.py DESPUES https://host.docker.internal:8443

* ANTES: el desarrollo (Odoo sin Nginx, sin compresión ni caché) con ``?debug=assets``, que sirve los assets sin empaquetar.
* DESPUES: el despliegue protegido (scripts/levantar_prod.sh): Nginx con TLS, gzip y caché de assets, Odoo con workers.

Cada página se mide ``--corridas`` veces y se guarda la mediana. Escribe una fila por página en el CSV de resultados
(``--salida``). Requiere Docker; la imagen con Lighthouse y Chromium se construye sola la primera vez (unos minutos).
El usuario es el jefe de ventas (``jefe.ventas@donofrio.example.com``) con la clave DONOFRIO_USER_PASSWORD de ``.env``,
que no se imprime ni se guarda. Los datos son los de demostración (scripts/cargar_transacciones.py).
"""
import argparse
import csv
import http.cookiejar
import json
import re
import ssl
import statistics
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
IMAGEN = 'donofrio-lighthouse'
USUARIO = 'jefe.ventas@donofrio.example.com'
PAGINAS = {
    'login': '/web/login',
    'backend': '/odoo/action-sale.action_orders',
    'dashboard': '/odoo/action-spreadsheet_dashboard.ir_actions_dashboard_action',
}
METRICAS = ['rendimiento', 'fcp_s', 'lcp_s', 'tbt_ms', 'cls', 'si_s', 'peticiones', 'transferido_kb']


def leer_clave():
    for linea in (RAIZ / '.env').read_text().splitlines():
        if linea.startswith('DONOFRIO_USER_PASSWORD='):
            return linea.split('=', 1)[1].strip()
    sys.exit('Falta DONOFRIO_USER_PASSWORD en .env')


def iniciar_sesion(base):
    """Devuelve el valor de la cookie session_id de un inicio de sesión normal."""
    contexto = ssl.create_default_context()
    contexto.check_hostname, contexto.verify_mode = False, ssl.CERT_NONE   # certificado autofirmado
    jar = http.cookiejar.CookieJar()
    abrir = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar), urllib.request.HTTPSHandler(context=contexto)).open
    pagina = abrir(f'{base}/web/login', timeout=60).read().decode()
    token = re.search(r'name="csrf_token" value="([^"]+)"', pagina).group(1)
    datos = urllib.parse.urlencode({'login': USUARIO, 'password': leer_clave(), 'csrf_token': token, 'redirect': ''}).encode()
    abrir(f'{base}/web/login', datos, timeout=60).read()
    cookie = next((c.value for c in jar if c.name == 'session_id'), None)
    if not cookie:
        sys.exit('No se pudo iniciar sesión: revisa el usuario, la clave y la base.')
    return cookie


def asegurar_imagen():
    if subprocess.run(['docker', 'image', 'inspect', IMAGEN], capture_output=True).returncode:
        print('Construyendo la imagen de Lighthouse (solo la primera vez)...', flush=True)
        subprocess.run(['docker', 'build', '-q', '-t', IMAGEN, '-f', str(RAIZ / 'scripts/perf/Dockerfile.lighthouse'),
                        str(RAIZ / 'scripts/perf')], check=True)


def correr(url, cookie, carpeta):
    cabeceras = json.dumps({'Cookie': f'session_id={cookie}'}) if cookie else '{}'
    subprocess.run([
        'docker', 'run', '--rm', '--add-host=host.docker.internal:host-gateway', '-v', f'{carpeta}:/out', IMAGEN,
        'lighthouse', url, '--preset=desktop', '--only-categories=performance', '--quiet',
        '--chrome-flags=--headless=new --no-sandbox --ignore-certificate-errors',
        f'--extra-headers={cabeceras}', '--output=json', '--output-path=/out/r.json',
    ], check=True, capture_output=True)
    r = json.loads((Path(carpeta) / 'r.json').read_text())
    a = r['audits']
    peticiones = a['network-requests']['details']['items']
    return {
        'rendimiento': round(r['categories']['performance']['score'] * 100),
        'fcp_s': round(a['first-contentful-paint']['numericValue'] / 1000, 2),
        'lcp_s': round(a['largest-contentful-paint']['numericValue'] / 1000, 2),
        'tbt_ms': round(a['total-blocking-time']['numericValue']),
        'cls': round(a['cumulative-layout-shift']['numericValue'], 3),
        'si_s': round(a['speed-index']['numericValue'] / 1000, 2),
        'peticiones': len(peticiones),
        'transferido_kb': round(sum(p.get('transferSize', 0) for p in peticiones) / 1024),
        'url_final': r['finalDisplayedUrl'],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('etiqueta', choices=['ANTES', 'DESPUES'])
    p.add_argument('base', help='URL base vista desde el contenedor, p. ej. http://host.docker.internal:8069')
    p.add_argument('--debug-assets', action='store_true', help='agrega ?debug=assets a cada página')
    p.add_argument('--corridas', type=int, default=3)
    p.add_argument('--salida', default=str(RAIZ / 'docs/capturas/sprint-3/HU-28_lighthouse_resultados.csv'))
    args = p.parse_args()

    asegurar_imagen()
    # El inicio de sesión corre en el PC (localhost); Lighthouse corre en el contenedor (host.docker.internal)
    cookie = iniciar_sesion(args.base.replace('host.docker.internal', 'localhost'))
    nuevo = not Path(args.salida).exists()
    with open(args.salida, 'a', newline='') as f:
        csv_ = csv.writer(f)
        if nuevo:
            csv_.writerow(['etiqueta', 'pagina', 'corridas', *METRICAS])
        for nombre, ruta in PAGINAS.items():
            url = args.base + ruta + ('?debug=assets' if args.debug_assets else '')
            corridas = []
            for i in range(args.corridas):
                with tempfile.TemporaryDirectory() as carpeta:
                    corridas.append(correr(url, None if nombre == 'login' else cookie, carpeta))
                print(f'  {args.etiqueta} {nombre} #{i + 1}: {corridas[-1]}', flush=True)
            mediana = {m: statistics.median(c[m] for c in corridas) for m in METRICAS}
            csv_.writerow([args.etiqueta, nombre, len(corridas), *[mediana[m] for m in METRICAS]])
            print(f'MEDIANA {args.etiqueta} {nombre}: {mediana}', flush=True)


if __name__ == '__main__':
    main()
