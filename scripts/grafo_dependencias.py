#!/usr/bin/env python3
"""Sección 5.4 del informe: grafo de dependencias entre módulos (Graphviz) a partir de los ``__manifest__.py``.

Lee los manifiestos de los módulos propios (``addons/``), de Odoo 19.0 Community y del módulo OCA ``auditlog``,
resuelve el árbol de ``depends`` de ``donofrio_base`` y escribe en ``docs/diagramas/dependencias/``:

  dependencias_directas.dot/.svg/.png   donofrio_base y sus ``depends`` directos, con las relaciones entre ellos
  dependencias_completo.dot/.svg/.png   todo lo que Odoo carga por ``depends`` (cierre transitivo)
  dependencias.csv                      un renglón por módulo: origen, tipo de instalación, nivel y sus ``depends``

También calcula qué módulos se instalan solos (``auto_install``) y, con ``--bd``, lo compara con los módulos
que de verdad tiene instalados una base de datos (lectura de ``ir_module_module``, sin escribir nada).

Fuente de los manifiestos de Odoo (a elegir):
  --odoo-src RUTA   un checkout de odoo/odoo 19.0 (por defecto ~/src/odoo-19.0)
  --imagen IMAGEN   la imagen de Docker de Odoo: lee ahí mismo Odoo y OCA, que es lo que corre de verdad
                    (por ejemplo, erp-donofrio/odoo:19.0 que construye docker compose)
``auditlog`` (OCA) se lee siempre de la imagen del compose (``/opt/oca``), porque el Dockerfile lo descarga
por commit y no existe en el repositorio.

Uso (solo Python 3 y Docker; Graphviz corre en una imagen con versión fija, no se instala nada):
    python3 scripts/grafo_dependencias.py                       # fuentes de ~/src/odoo-19.0
    python3 scripts/grafo_dependencias.py --imagen erp-donofrio/odoo:19.0 --bd donofrio
    python3 scripts/grafo_dependencias.py --sin-render          # solo .dot y .csv
"""
import argparse
import ast
import csv
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'docs' / 'diagramas' / 'dependencias'
# Imagen con Graphviz (dot 14.0.1) y versión fija; la misma que usa PlantUML en docs/diagramas/README.md
IMAGEN_GRAPHVIZ = 'plantuml/plantuml:1.2026.10'
IMAGEN_RSVG = 'python:3.12-slim'          # para convertir el SVG a PNG (librsvg), como en el resto de diagramas
IMAGEN_COMPOSE = 'erp-donofrio/odoo:19.0'  # trae /opt/oca/auditlog (docker compose build odoo)

# En el contenedor se lee con el mismo método que aquí: el manifiesto es un diccionario literal de Python
VOLCADO = r'''
import ast, json, os, sys
salida = {}
for base in sys.argv[1:]:
    if not os.path.isdir(base):
        continue
    for nombre in sorted(os.listdir(base)):
        ruta = os.path.join(base, nombre, '__manifest__.py')
        if os.path.isfile(ruta):
            m = ast.literal_eval(open(ruta, encoding='utf-8').read())
            salida[nombre] = {k: m.get(k) for k in ('depends', 'auto_install', 'installable', 'version', 'license', 'countries')}
print(json.dumps(salida))
'''

# Colores por origen (nodo relleno / borde)
ESTILO = {
    'propio': ('#ffe08a', '#8a6d00'),
    'oca': ('#d7f0d2', '#1e7e34'),
    'base': ('#e0e0e0', '#555555'),
    'odoo': ('#e8f1fb', '#2c5282'),
}
ETIQUETA_ORIGEN = {
    'propio': "Configuración base D'Onofrio",
    'oca': 'OCA (auditlog, fijado por commit)',
    'odoo': 'Odoo 19.0 Community',
    'base': 'Núcleo (base)',
}


def literal(texto, nombre):
    try:
        return ast.literal_eval(texto)
    except (ValueError, SyntaxError) as error:
        sys.exit(f'No se pudo leer el manifiesto de {nombre}: {error}')


def desde_carpeta(carpeta, origen):
    """{módulo: datos} de cada subcarpeta de ``carpeta`` que tenga ``__manifest__.py``."""
    modulos = {}
    for manifiesto in sorted(Path(carpeta).glob('*/__manifest__.py')):
        m = literal(manifiesto.read_text(encoding='utf-8'), manifiesto)
        modulos[manifiesto.parent.name] = {
            'depends': m.get('depends') or [], 'auto_install': m.get('auto_install'),
            'installable': m.get('installable', True), 'version': m.get('version'), 'license': m.get('license'),
            'countries': m.get('countries') or [], 'origen': origen,
        }
    return modulos


def desde_imagen(imagen, carpetas, origen_de):
    """Lo mismo, pero leyendo dentro de una imagen de Docker (solo lectura, el contenedor se borra al salir)."""
    resultado = subprocess.run(
        ['docker', 'run', '--rm', '--entrypoint', 'python3', imagen, '-c', VOLCADO, *carpetas],
        capture_output=True, text=True)
    if resultado.returncode:
        sys.exit(f'No se pudo leer la imagen {imagen}:\n{resultado.stderr.strip()}')
    modulos = {}
    for nombre, datos in json.loads(resultado.stdout).items():
        modulos[nombre] = {
            'depends': datos['depends'] or [], 'auto_install': datos['auto_install'],
            'installable': datos['installable'] is not False, 'version': datos['version'],
            'license': datos['license'], 'countries': datos['countries'] or [], 'origen': origen_de(nombre),
        }
    return modulos


def reunir(args):
    """Junta los manifiestos. Prioridad si un nombre se repite: propio > OCA > Odoo."""
    odoo = {}
    if args.imagen:
        odoo = desde_imagen(args.imagen, ['/usr/lib/python3/dist-packages/odoo/addons'],
                            lambda nombre: 'base' if nombre == 'base' else 'odoo')
        oca = desde_imagen(args.imagen, ['/opt/oca'], lambda nombre: 'oca')
    else:
        fuente = Path(args.odoo_src).expanduser()
        if not (fuente / 'addons').is_dir():
            sys.exit(f'No existe {fuente}/addons. Indica --odoo-src o usa --imagen.')
        odoo = {**desde_carpeta(fuente / 'addons', 'odoo'), **desde_carpeta(fuente / 'odoo' / 'addons', 'odoo')}
        if 'base' in odoo:
            odoo['base']['origen'] = 'base'
        oca = desde_imagen(IMAGEN_COMPOSE, ['/opt/oca'], lambda nombre: 'oca')
    todos = {**odoo, **oca, **desde_carpeta(RAIZ / 'addons', 'propio')}
    return todos


def cierre(raices, modulos):
    """Módulos que Odoo carga por ``depends`` a partir de ``raices`` (incluye las raíces)."""
    vistos, pendientes = set(), list(raices)
    while pendientes:
        nombre = pendientes.pop()
        if nombre in vistos:
            continue
        if nombre not in modulos:
            sys.exit(f'El módulo «{nombre}» está en un depends pero no se encontró su manifiesto.')
        vistos.add(nombre)
        pendientes.extend(modulos[nombre]['depends'])
    return vistos


def instalados_automaticos(base, modulos, pais='pe'):
    """Módulos con ``auto_install`` que Odoo agrega solos al instalar ``base`` (regla de ``button_install``).

    Un módulo con ``auto_install`` entra cuando todos sus disparadores (la lista de ``auto_install`` o, si es ``True``,
    todos sus ``depends``) están instalados y sus ``depends`` también. Los que declaran ``countries`` solo entran si la
    compañía es de ese país (D'Onofrio: Perú). Se repite hasta que no entra ninguno más.
    """
    instalados = set(base)
    cambio = True
    while cambio:
        cambio = False
        for nombre, datos in modulos.items():
            if nombre in instalados or not datos['auto_install'] or not datos['installable']:
                continue
            if datos['countries'] and pais not in datos['countries']:
                continue
            disparo = datos['depends'] if datos['auto_install'] is True else list(datos['auto_install'])
            if all(d in instalados for d in disparo) and all(d in instalados for d in datos['depends']):
                instalados.add(nombre)
                cambio = True
    return instalados - set(base)


def alcanzables(grafo):
    memo = {}

    def visitar(nodo):
        if nodo not in memo:
            memo[nodo] = set()
            for destino in grafo[nodo]:
                memo[nodo] |= {destino} | visitar(destino)
        return memo[nodo]
    for nodo in grafo:
        visitar(nodo)
    return memo


def reduccion_transitiva(grafo, alcance):
    """Quita la arista u→v si v ya se alcanza por otro vecino de u (el dibujo queda legible; no cambia el orden de carga)."""
    reducido = {}
    for u, destinos in grafo.items():
        reducido[u] = {v for v in destinos
                       if not any(v in alcance[w] for w in destinos if w != v)}
    return reducido


def niveles(grafo):
    """Nivel = longitud del camino más largo hasta ``base`` (base = 0). Es el orden en que Odoo los carga."""
    memo = {}

    def nivel(nodo):
        if nodo not in memo:
            memo[nodo] = 0 if not grafo[nodo] else 1 + max(nivel(d) for d in grafo[nodo])
        return memo[nodo]
    return {n: nivel(n) for n in grafo}


def nodo_dot(nombre, datos, texto_extra=''):
    relleno, borde = ESTILO[datos['origen']]
    grosor = 2.4 if datos['origen'] == 'propio' else 1.2
    etiqueta = nombre + (f'\\n{texto_extra}' if texto_extra else '')
    return (f'  "{nombre}" [label="{etiqueta}", style="filled,rounded", shape=box, fillcolor="{relleno}", '
            f'color="{borde}", penwidth={grosor}];')


def leyenda(origenes):
    lineas = ['  subgraph cluster_leyenda { label="Origen del módulo"; fontsize=11; color="#999999"; style=rounded;']
    for i, origen in enumerate(o for o in ('propio', 'oca', 'odoo', 'base') if o in origenes):
        relleno, borde = ESTILO[origen]
        lineas.append(f'    "leyenda_{origen}" [label="{ETIQUETA_ORIGEN[origen]}", shape=box, style="filled,rounded", '
                      f'fillcolor="{relleno}", color="{borde}", fontsize=10];')
    lineas.append('  }')
    return lineas


def dot_directas(propios, modulos, directas, alcance, total_por_modulo):
    nodos = list(propios) + sorted(directas)
    # Aristas: lo que declara donofrio_base y, entre los directos, la reducción transitiva de lo que se alcanzan
    entre_directos = {n: {d for d in alcance[n] if d in directas} for n in directas}
    reducido = reduccion_transitiva(entre_directos, entre_directos)
    lineas = ['digraph dependencias_directas {',
              '  graph [rankdir=LR, fontname="DejaVu Sans", fontsize=14, labelloc=t, nodesep=0.25, ranksep=0.7, '
              'label="Dependencias directas de donofrio_base (arista A → B: A depende de B)\\n'
              'Entre los módulos directos solo se dibuja la reducción transitiva"];',
              '  node [fontname="DejaVu Sans", fontsize=11]; edge [color="#555555", arrowsize=0.7];']
    for nombre in nodos:
        extra = (f'{len(directas)} directas' if nombre in propios
                 else f'+{total_por_modulo[nombre]} en su árbol' if total_por_modulo[nombre] else '')
        lineas.append(nodo_dot(nombre, modulos[nombre], extra))
    for raiz in propios:
        for destino in sorted(modulos[raiz]['depends']):
            lineas.append(f'  "{raiz}" -> "{destino}" [color="#8a6d00", penwidth=1.4];')
    for origen, destinos in sorted(reducido.items()):
        for destino in sorted(destinos):
            lineas.append(f'  "{origen}" -> "{destino}";')
    lineas += leyenda({modulos[n]['origen'] for n in nodos})
    lineas.append('}')
    return '\n'.join(lineas) + '\n'


def dot_completo(propios, modulos, instalados, grafo, alcance):
    reducido = reduccion_transitiva(grafo, alcance)
    lineas = ['digraph dependencias_completo {',
              '  graph [rankdir=TB, fontname="DejaVu Sans", fontsize=16, labelloc=t, nodesep=0.12, ranksep=0.55, '
              f'label="Árbol completo de depends de donofrio_base: {len(instalados)} módulos (arista A → B: A depende de B; reducción transitiva)"];',
              '  node [fontname="DejaVu Sans", fontsize=10, height=0.3]; edge [color="#777777", arrowsize=0.6];']
    for nombre in sorted(instalados):
        lineas.append(nodo_dot(nombre, modulos[nombre]))
    for origen in sorted(reducido):
        for destino in sorted(reducido[origen]):
            lineas.append(f'  "{origen}" -> "{destino}";')
    lineas += leyenda({modulos[n]['origen'] for n in instalados})
    lineas.append('}')
    return '\n'.join(lineas) + '\n'


def renderizar(carpeta, nombres):
    """dot → SVG en la imagen de Graphviz fija; SVG → PNG con librsvg en una imagen de Python (sin instalar nada local)."""
    uid_gid = f'{subprocess.check_output(["id", "-u"], text=True).strip()}:{subprocess.check_output(["id", "-g"], text=True).strip()}'
    for nombre in nombres:
        with open(carpeta / f'{nombre}.dot', 'rb') as entrada, open(carpeta / f'{nombre}.svg', 'wb') as salida:
            r = subprocess.run(['docker', 'run', '--rm', '-i', '--entrypoint', 'dot', IMAGEN_GRAPHVIZ, '-Tsvg'],
                               stdin=entrada, stdout=salida, stderr=subprocess.PIPE)
        errores = [linea for linea in r.stderr.decode().splitlines()
                   if 'libgvplugin_gd' not in linea and 'no value for width' not in linea and linea.strip()]
        if r.returncode or errores:
            sys.exit(f'dot falló con {nombre}.dot:\n' + '\n'.join(errores))
    script = ('apt-get update -qq >/dev/null && apt-get install -y -qq librsvg2-bin fonts-dejavu-core >/dev/null && cd /d && '
              + ' && '.join(f'rsvg-convert {n}.svg -o {n}.png' for n in nombres) + f' && chown {uid_gid} *.png')
    r = subprocess.run(['docker', 'run', '--rm', '-v', f'{carpeta}:/d', '--entrypoint', 'sh', IMAGEN_RSVG, '-c', script],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'No se pudo convertir a PNG:\n{r.stderr.strip()}')


def modulos_de_la_bd(bd):
    r = subprocess.run(['docker', 'compose', 'exec', '-T', 'db', 'psql', '-U', 'postgres', '-d', bd, '-X', '-tA', '-c',
                        "SELECT name FROM ir_module_module WHERE state = 'installed'"],
                       cwd=RAIZ, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'No se pudo consultar la BD «{bd}»:\n{r.stderr.strip()}')
    return set(r.stdout.split())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--odoo-src', default='~/src/odoo-19.0', help='checkout de odoo/odoo 19.0 (por defecto ~/src/odoo-19.0)')
    ap.add_argument('--imagen', help='leer Odoo y OCA de esta imagen de Docker en vez de --odoo-src')
    ap.add_argument('--bd', help='comparar con los módulos instalados de esta base (solo lectura)')
    ap.add_argument('--sin-render', action='store_true', help='escribir solo los .dot y el .csv')
    args = ap.parse_args()

    modulos = reunir(args)
    propios = sorted(n for n, d in modulos.items() if d['origen'] == 'propio')
    if not propios:
        sys.exit('No hay módulos propios en addons/.')
    directas = {d for p in propios for d in modulos[p]['depends']} - set(propios)
    por_depends = cierre(propios, modulos)
    extras = instalados_automaticos(por_depends, modulos)
    grafo = {n: set(modulos[n]['depends']) for n in por_depends}
    alcance = alcanzables(grafo)
    nivel = niveles(grafo)
    total_por_modulo = {n: len(alcance[n]) for n in por_depends}

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / 'dependencias_directas.dot').write_text(
        dot_directas(propios, modulos, directas, alcance, total_por_modulo), encoding='utf-8')
    (SALIDA / 'dependencias_completo.dot').write_text(
        dot_completo(propios, modulos, por_depends, grafo, alcance), encoding='utf-8')
    with open(SALIDA / 'dependencias.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['modulo', 'origen', 'instalacion', 'nivel', 'depende_de'])
        for nombre in sorted(por_depends | extras, key=lambda n: (n not in propios, nivel.get(n, 99), n)):
            if nombre in propios:
                tipo = 'propio'
            elif nombre in directas:
                tipo = 'depends directo de donofrio_base'
            elif nombre in por_depends:
                tipo = 'depends transitivo'
            else:
                tipo = 'auto_install'
            w.writerow([nombre, modulos[nombre]['origen'], tipo, nivel.get(nombre, ''),
                        ' '.join(sorted(modulos[nombre]['depends']))])

    cuenta = {}
    for n in por_depends:
        cuenta[modulos[n]['origen']] = cuenta.get(modulos[n]['origen'], 0) + 1
    print(f'Módulos propios: {", ".join(propios)}')
    print(f'depends directos de los propios: {len(directas)}')
    print(f'Árbol de depends (con los propios): {len(por_depends)} módulos · por origen: '
          + ', '.join(f'{o} {c}' for o, c in sorted(cuenta.items())))
    print(f'Profundidad máxima del árbol: {max(nivel.values())} niveles')
    print(f'Instalados solos por auto_install: {len(extras)} módulos · total esperado: {len(por_depends) + len(extras)}')
    if args.bd:
        real = modulos_de_la_bd(args.bd)
        esperado = por_depends | extras
        print(f'Módulos instalados en la base «{args.bd}»: {len(real)} · coinciden: {len(real & esperado)}')
        if real - esperado:
            print('  En la base y no calculados: ' + ', '.join(sorted(real - esperado)))
        if esperado - real:
            print('  Calculados y no instalados: ' + ', '.join(sorted(esperado - real)))
    if args.sin_render:
        return
    renderizar(SALIDA, ['dependencias_directas', 'dependencias_completo'])
    print(f'Escrito en {SALIDA.relative_to(RAIZ)}/')


if __name__ == '__main__':
    main()
