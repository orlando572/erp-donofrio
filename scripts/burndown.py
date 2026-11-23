#!/usr/bin/env python3
"""Informe 6.2: cuadro de sprints y burndown por puntos, a partir de GitHub (solo lectura).

Uso:  python3 scripts/burndown.py                 imprime el cuadro y el burndown (usa `gh`, hace falta `gh auth login`)
      python3 scripts/burndown.py --csv RUTA      además guarda el burndown en un CSV (y --svg RUTA, el gráfico)
      python3 scripts/burndown.py --autotest      comprueba el cálculo con datos de ejemplo (sin red)

Fuentes (todas de solo lectura):
* ``gh project item-list``: el sprint de cada épica en el GitHub Project «Scrum ERP D'Onofrio».
* ``gh issue list``: el cuerpo de cada épica, con su checklist de historias de usuario (``- [x] **HU-23** ... *(3 pts · ...)*``). Una HU
  está hecha si su casilla está marcada **o** si su épica está cerrada (una épica solo se cierra con todas sus HU terminadas).
* ``gh pr list --state merged``: la fecha en que se fusionó cada PR; una HU cuenta como terminada cuando su casilla está marcada y se
  fusionó el último PR con su ``[HU-xx]`` en el título.

Los puntos salen de las **HU** y no de la tarjeta de la épica, porque una épica puede estar parcialmente terminada (por ejemplo, #141).
El Sprint real de cada épica es el del Project; las fechas de «real» son las de fusión de los PR (hora de Lima).
"""
import argparse
import csv
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

PROPIETARIO, PROYECTO, REPO = 'orlando572', 4, 'orlando572/erp-donofrio'
LIMA = timezone(timedelta(hours=-5))
HU_LINEA = re.compile(r'^- \[(?P<marca>[ xX])\] \*\*(?P<hu>HU-\d+)\*\*.*?\*\((?P<pts>\d+) pts', re.M)


def gh(*args):
    return json.loads(subprocess.run(['gh', *args], check=True, capture_output=True, text=True).stdout)


def leer_github():
    items = gh('project', 'item-list', str(PROYECTO), '--owner', PROPIETARIO, '--limit', '100', '--format', 'json')['items']
    issues = gh('issue', 'list', '--repo', REPO, '--state', 'all', '--limit', '200', '--json', 'number,state,body')
    prs = gh('pr', 'list', '--repo', REPO, '--state', 'merged', '--limit', '500', '--json', 'number,title,mergedAt')
    return items, issues, prs


def _titulo(sprint):
    """El campo Sprint del Project llega como objeto ``{'title': 'S2', ...}``; en las pruebas puede ser un texto."""
    return sprint.get('title') if isinstance(sprint, dict) else sprint


def hu_de_epicas(items, issues):
    """{HU: {'sprint', 'puntos', 'hecha', 'epica'}} según las épicas del Project y su checklist."""
    sprint_de = {i['content']['number']: _titulo(i.get('sprint')) for i in items if i['content'].get('number')}
    cuerpo = {i['number']: i['body'] or '' for i in issues}
    cerrada = {i['number']: i['state'] == 'CLOSED' for i in issues}
    hus = {}
    for numero, sprint in sprint_de.items():
        for m in HU_LINEA.finditer(cuerpo.get(numero, '')):
            hus[m['hu']] = {'sprint': sprint, 'puntos': int(m['pts']), 'hecha': m['marca'].lower() == 'x' or cerrada.get(numero, False), 'epica': numero}
    return hus


def fecha_de_cierre(prs):
    """{HU: instante del último PR fusionado con ese [HU-xx] en el título}."""
    ultima = {}
    for pr in prs:
        instante = datetime.fromisoformat(pr['mergedAt'].replace('Z', '+00:00'))
        for hu in set(re.findall(r'HU-\d+', pr['title'])):
            ultima[hu] = max(ultima.get(hu, instante), instante)
    return ultima


def cuadro(hus):
    filas = {}
    for datos in hus.values():
        f = filas.setdefault(datos['sprint'], {'hu': 0, 'planificados': 0, 'completados': 0, 'hu_hechas': 0})
        f['hu'] += 1
        f['planificados'] += datos['puntos']
        if datos['hecha']:
            f['completados'] += datos['puntos']
            f['hu_hechas'] += 1
    return filas


def burndown(hus, cierre, sprint):
    """Puntos pendientes después de cada HU terminada del sprint, en orden de fecha (hora de Lima)."""
    del_sprint = {h: d for h, d in hus.items() if d['sprint'] == sprint}
    pendientes = sum(d['puntos'] for d in del_sprint.values())
    serie = [('inicio', None, pendientes)]
    terminadas = sorted((cierre[h], h) for h, d in del_sprint.items() if d['hecha'] and h in cierre)
    for instante, hu in terminadas:
        pendientes -= del_sprint[hu]['puntos']
        serie.append((hu, instante.astimezone(LIMA), pendientes))
    return serie


def imprimir(hus, cierre, csv_ruta=None):
    filas = cuadro(hus)
    orden = [s for s in ('S0', 'S1', 'S2', 'S3', 'S4', 'Cierre') if s in filas]
    print('| Sprint | HU | HU terminadas | Puntos planificados | Puntos completados | Avance |')
    print('|---|---|---|---|---|---|')
    for s in orden:
        f = filas[s]
        avance = f'{100 * f["completados"] / f["planificados"]:.0f} %' if f['planificados'] else '—'
        print(f'| {s} | {f["hu"]} | {f["hu_hechas"]} | {f["planificados"]} | {f["completados"]} | {avance} |')
    total = {k: sum(filas[s][k] for s in orden) for k in ('hu', 'hu_hechas', 'planificados', 'completados')}
    print(f'| **Total** | {total["hu"]} | {total["hu_hechas"]} | {total["planificados"]} | {total["completados"]} | '
          f'{100 * total["completados"] / total["planificados"]:.0f} % |')
    filas_csv = []
    for s in orden:
        if not filas[s]['completados']:
            continue
        print(f'\nBurndown {s} (puntos pendientes tras cada HU terminada, hora de Lima):')
        for hu, instante, pendientes in burndown(hus, cierre, s):
            marca = instante.strftime('%d/%m %H:%M') if instante else '—'
            print(f'  {marca:>12}  {hu:<7} pendientes {pendientes}')
            filas_csv.append([s, hu, instante.strftime('%Y-%m-%d %H:%M') if instante else '', pendientes])
    if csv_ruta:
        with open(csv_ruta, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['sprint', 'hu', 'terminada_lima', 'puntos_pendientes'])
            w.writerows(filas_csv)


def grafico_svg(hus, cierre, ruta):
    """Un panel por sprint con la línea ideal (de todos los puntos a 0) y la real (tras cada HU terminada)."""
    sprints = [sp for sp in ('S1', 'S2', 'S3') if any(d['sprint'] == sp and d['hecha'] for d in hus.values())]
    ancho, alto, margen = 340, 250, 44
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho * len(sprints) + 20}" height="{alto + 70}" font-family="DejaVu Sans, Arial, sans-serif" font-size="11">',
              f'<rect width="100%" height="100%" fill="#fff"/>']
    for k, sp in enumerate(sprints):
        serie = burndown(hus, cierre, sp)
        x0, y0 = 10 + k * ancho + margen, 40
        w, h = ancho - margen - 20, alto - 60
        total = serie[0][2]
        n = len(serie) - 1
        px = lambda i: x0 + w * i / max(n, 1)
        py = lambda v: y0 + h * (1 - v / total)
        partes.append(f'<text x="{x0}" y="22" font-weight="bold" font-size="13">Burndown {sp}: {total} puntos</text>')
        for v in range(0, total + 1, max(total // 4, 1)):
            partes.append(f'<line x1="{x0}" y1="{py(v):.0f}" x2="{x0 + w}" y2="{py(v):.0f}" stroke="#ddd"/><text x="{x0 - 6}" y="{py(v) + 4:.0f}" text-anchor="end">{v}</text>')
        partes.append(f'<line x1="{px(0):.0f}" y1="{py(total):.0f}" x2="{px(n):.0f}" y2="{py(0):.0f}" stroke="#999" stroke-dasharray="5 4"/>')
        puntos = ' '.join(f'{px(i):.0f},{py(p):.0f}' for i, (_, _, p) in enumerate(serie))
        partes.append(f'<polyline points="{puntos}" fill="none" stroke="#c28a00" stroke-width="2.5"/>')
        for i, (hu, instante, p) in enumerate(serie):
            partes.append(f'<circle cx="{px(i):.0f}" cy="{py(p):.0f}" r="3.5" fill="#c28a00"/>')
            if i:
                partes.append(f'<text x="{px(i):.0f}" y="{y0 + h + 14}" text-anchor="middle" font-size="9">{hu[3:]}</text>')
        partes.append(f'<text x="{x0 + w / 2}" y="{y0 + h + 32}" text-anchor="middle" fill="#555">HU terminadas, en orden (n.º de HU)</text>')
    partes.append(f'<text x="10" y="{alto + 62}" fill="#555">Línea punteada: ritmo ideal. Línea amarilla: puntos pendientes tras cada HU terminada (fusión del último PR).</text></svg>')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('\n'.join(partes))


def autotest():
    cuerpo = ('- [x] **HU-01**: a *(3 pts · RNF)*\n    - [x] criterio\n- [x] **HU-02**: b *(2 pts · RNF)*\n'
              '- [ ] **HU-03**: c *(4 pts · RNF)*\n')
    items = [{'content': {'number': 10}, 'sprint': 'S1'}, {'content': {'number': 11}, 'sprint': 'S2'}, {'content': {'number': 12}, 'sprint': 'S3'}]
    issues = [{'number': 10, 'state': 'OPEN', 'body': cuerpo}, {'number': 11, 'state': 'OPEN', 'body': '- [x] **HU-04**: d *(5 pts · RF)*'},
              {'number': 12, 'state': 'CLOSED', 'body': '- [ ] **HU-05**: e *(7 pts · RF)*'}]
    prs = [{'number': 1, 'title': 'feat: a [HU-01]', 'mergedAt': '2026-11-23T10:00:00Z'},
           {'number': 2, 'title': 'feat: b [HU-02]', 'mergedAt': '2026-11-23T15:00:00Z'},
           {'number': 3, 'title': 'feat: b2 [HU-02]', 'mergedAt': '2026-11-23T17:00:00Z'},
           {'number': 4, 'title': 'feat: d [HU-04]', 'mergedAt': '2026-11-24T03:00:00Z'}]
    hus = hu_de_epicas(items, issues)
    assert hus['HU-01'] == {'sprint': 'S1', 'puntos': 3, 'hecha': True, 'epica': 10}
    assert not hus['HU-03']['hecha']
    f = cuadro(hus)
    assert f['S1'] == {'hu': 3, 'planificados': 9, 'completados': 5, 'hu_hechas': 2}, f['S1']
    assert f['S2']['completados'] == 5
    assert f['S3']['completados'] == 7, 'una épica cerrada da por hechas sus HU aunque la casilla no esté marcada'
    cierre = fecha_de_cierre(prs)
    assert cierre['HU-02'].hour == 17, 'una HU con dos PR cuenta desde el último'
    serie = burndown(hus, cierre, 'S1')
    assert [p for _, _, p in serie] == [9, 6, 4], serie
    assert serie[2][1].strftime('%d/%m %H:%M') == '23/11 12:00', 'hora de Lima = UTC − 5'
    assert burndown(hus, cierre, 'S2')[-1][2] == 0
    print('autotest OK: el cuadro y el burndown dan los valores esperados.')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--csv', help='guarda el burndown en este CSV')
    p.add_argument('--svg', help='guarda el gráfico del burndown en este SVG')
    p.add_argument('--autotest', action='store_true')
    args = p.parse_args()
    if args.autotest:
        return autotest()
    items, issues, prs = leer_github()
    hus, cierre = hu_de_epicas(items, issues), fecha_de_cierre(prs)
    imprimir(hus, cierre, args.csv)
    if args.svg:
        grafico_svg(hus, cierre, args.svg)


if __name__ == '__main__':
    sys.exit(main())
