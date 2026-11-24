#!/usr/bin/env python3
"""S4: Lighthouse del tablero gerencial (M4) y del login, con el mismo método de la HU-28 (scripts/perf/lighthouse.py).

Reutiliza de ``scripts/perf/lighthouse.py`` el inicio de sesión, la lectura de la clave de ``.env`` y la imagen de
Docker; cambia tres cosas (por eso es un script aparte y no una modificación del de HU-28):

* el usuario es el Gerente General (``--usuario``, por defecto ``gerente@donofrio.example.com``), no el jefe de ventas:
  el jefe de ventas ve el menú del tablero pero no lee Inventario, y mediría el aviso de «Sin permiso» en vez del tablero.
  En el despliegue protegido el Gerente pide 2FA (HU-27) y un script no puede darlo: ahí se usa
  ``jefe.almacen@donofrio.example.com`` (sin 2FA, lee todos los datos del tablero; no tiene el menú, pero abre la acción
  por su dirección). Si la página medida termina en el login, el script se detiene en vez de guardar una cifra falsa;
* las páginas son ``/web/login`` y ``/odoo/action-donofrio_tablero.action_tablero``;
* el contenedor de Lighthouse usa ``--network host`` (en Linux, ``host.docker.internal`` no llega a los puertos que
  Compose publica solo en 127.0.0.1).

Uso (desde la raíz del repositorio):

    python3 docs/capturas/sprint-4/S4_lighthouse_m4.py ANTES   http://localhost:8169 --debug-assets
    python3 docs/capturas/sprint-4/S4_lighthouse_m4.py DESPUES https://localhost:8443
    python3 docs/capturas/sprint-4/S4_lighthouse_m4.py DESPUES https://localhost:8443 --movil
"""
import argparse
import csv
import importlib.util
import json
import statistics
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('lh', RAIZ / 'scripts/perf/lighthouse.py')
lh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lh)

PAGINAS = {
    'login': '/web/login',
    'tablero': '/odoo/action-donofrio_tablero.action_tablero',
}


def correr(url, cookie, carpeta, movil):
    cabeceras = json.dumps({'Cookie': f'session_id={cookie}'}) if cookie else '{}'
    cmd = ['docker', 'run', '--rm', '--network', 'host', '-v', f'{carpeta}:/out', lh.IMAGEN,
           'lighthouse', url, '--only-categories=performance', '--quiet',
           '--chrome-flags=--headless=new --no-sandbox --ignore-certificate-errors',
           f'--extra-headers={cabeceras}', '--output=json', '--output-path=/out/r.json']
    if not movil:
        cmd.append('--preset=desktop')
    subprocess.run(cmd, check=True, capture_output=True)
    r = json.loads((Path(carpeta) / 'r.json').read_text())
    a = r['audits']
    peticiones = a['network-requests']['details']['items']
    if '/web/login' in r['finalDisplayedUrl'] and '/web/login' not in url:
        raise SystemExit(f'La medición terminó en el login ({r["finalDisplayedUrl"]}): la sesión no sirvió (¿2FA?).')
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
    p.add_argument('base')
    p.add_argument('--debug-assets', action='store_true')
    p.add_argument('--movil', action='store_true', help='perfil móvil de Lighthouse (por defecto, escritorio)')
    p.add_argument('--paginas', nargs='+', choices=list(PAGINAS), default=list(PAGINAS))
    p.add_argument('--usuario', default='gerente@donofrio.example.com')
    p.add_argument('--corridas', type=int, default=3)
    p.add_argument('--salida', default=str(RAIZ / 'docs/capturas/sprint-4/S4_lighthouse_m4_resultados.csv'))
    args = p.parse_args()

    lh.USUARIO = args.usuario
    lh.asegurar_imagen()
    cookie = lh.iniciar_sesion(args.base)
    perfil = 'movil' if args.movil else 'escritorio'
    nuevo = not Path(args.salida).exists()
    with open(args.salida, 'a', newline='') as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(['etiqueta', 'perfil', 'pagina', 'usuario', 'corridas', *lh.METRICAS])
        for nombre in args.paginas:
            ruta = PAGINAS[nombre]
            url = args.base + ruta + ('?debug=assets' if args.debug_assets else '')
            corridas = []
            for i in range(args.corridas):
                with tempfile.TemporaryDirectory() as carpeta:
                    corridas.append(correr(url, None if nombre == 'login' else cookie, carpeta, args.movil))
                print(f'  {args.etiqueta} {perfil} {nombre} #{i + 1}: {corridas[-1]}', flush=True)
            mediana = {m: statistics.median(c[m] for c in corridas) for m in lh.METRICAS}
            w.writerow([args.etiqueta, perfil, nombre, 'sin sesión' if nombre == 'login' else args.usuario.split('@')[0], len(corridas), *[mediana[m] for m in lh.METRICAS]])
            print(f'MEDIANA {args.etiqueta} {perfil} {nombre}: {mediana}', flush=True)


if __name__ == '__main__':
    main()
