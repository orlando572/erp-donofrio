#!/usr/bin/env python3
"""Informe 6.7 y 6.8: estadísticas de commits y de issues del repositorio, de solo lectura.

Uso:  python3 scripts/estadisticas_repo.py            imprime las tablas en Markdown (usa `gh`, hace falta `gh auth login`)
      python3 scripts/estadisticas_repo.py --autotest comprueba las reglas con datos de ejemplo (sin red)

Qué mide:
* 6.7: los commits **dentro de los PR fusionados** (porque `develop` se fusiona con *squash* y allí cada PR deja un solo commit),
  por autor, y cuántos cumplen la convención de commits del proyecto: Conventional Commits en español con la etiqueta de la HU
  o del sprint (``feat(ventas): ... [HU-15]``, ``docs(informe): ... [S3]``). También los PR por autor y el tipo de commit.
* 6.8: los issues por tipo, área, fase, milestone y estado, y cuántos PR se enlazan con ``Parte de #n`` o ``Closes #n``.

Los dos autores se juntan por login de GitHub; un mismo autor puede firmar con dos correos y cuenta como una persona.
"""
import argparse
import json
import re
import subprocess
import sys
from collections import Counter

REPO = 'orlando572/erp-donofrio'
TIPOS = 'feat|fix|docs|test|perf|chore|refactor|ci|build|style|revert'
CONVENCION = re.compile(rf'^(?P<tipo>{TIPOS})(\([\w\-./ ]+\))?!?: .+')
ETIQUETA = re.compile(r'\[(HU-\d+(?:, ?HU-\d+)*|S\d|S0)\]\s*(\(#\d+\))?$')
ENLACE_EPICA = re.compile(r'(?im)^\s*(Closes|Parte de) #(\d+)')


def gh(*args):
    return json.loads(subprocess.run(['gh', *args], check=True, capture_output=True, text=True).stdout)


def conforme(titulo):
    """(sigue Conventional Commits, lleva etiqueta [HU-xx] o [Sn])."""
    return bool(CONVENCION.match(titulo)), bool(ETIQUETA.search(titulo.strip()))


def commits(prs):
    por_autor, tipos, total = Counter(), Counter(), Counter()
    for pr in prs:
        for c in pr['commits']:
            titulo = c['messageHeadline']
            if titulo.startswith('Merge '):       # fusiones de develop dentro de la rama: no son trabajo propio
                continue
            conv, etiq = conforme(titulo)
            logins = [a['login'] for a in c['authors'] if a.get('login')] or [c['authors'][0]['name']]
            autor = logins[0]
            por_autor[autor] += 1
            total['commits'] += 1
            total['convencion'] += conv
            total['etiqueta'] += etiq
            if conv:
                tipos[CONVENCION.match(titulo)['tipo']] += 1
    return por_autor, tipos, total


def tabla_commits(prs):
    por_autor, tipos, total = commits(prs)
    prs_autor = Counter(pr['author']['login'] for pr in prs)
    print('| Autor (GitHub) | PR fusionados | Commits dentro de los PR | % de los commits |')
    print('|---|---|---|---|')
    for autor, n in por_autor.most_common():
        print(f'| {autor} | {prs_autor.get(autor, 0)} | {n} | {100 * n / total["commits"]:.0f} % |')
    print(f'| **Total** | {len(prs)} | {total["commits"]} | 100 % |')
    print(f'\nCumplen Conventional Commits: {total["convencion"]} de {total["commits"]} ({100 * total["convencion"] / total["commits"]:.0f} %). '
          f'Llevan la etiqueta [HU-xx] o [Sn]: {total["etiqueta"]} de {total["commits"]} ({100 * total["etiqueta"] / total["commits"]:.0f} %).')
    print('\n| Tipo de commit | Cantidad |')
    print('|---|---|')
    for tipo, n in tipos.most_common():
        print(f'| {tipo} | {n} |')
    titulos = [pr['title'] for pr in prs]
    ok = sum(all(conforme(t)) for t in titulos)
    fuera = [f'#{pr["number"]}' for pr in prs if not all(conforme(pr['title']))]
    print(f'\nTítulo del PR (el que queda en `develop` con *squash*): {ok} de {len(titulos)} cumplen la convención y llevan etiqueta.'
          + (f' Fuera de la regla: {", ".join(fuera)}.' if fuera else ''))
    sin = [(pr['number'], c['messageHeadline']) for pr in prs for c in pr['commits']
           if not c['messageHeadline'].startswith('Merge ') and not CONVENCION.match(c['messageHeadline'])]
    if sin:
        print('Commits que no siguen la convención: ' + '; '.join(f'#{n} «{t[:50]}»' for n, t in sin) + '.')


def tabla_issues(issues, prs):
    def etiqueta(i, prefijo):
        return next((l['name'][len(prefijo):] for l in i['labels'] if l['name'].startswith(prefijo)), '—')
    print(f'Total de issues: {len(issues)} · abiertos {sum(i["state"] == "OPEN" for i in issues)} · cerrados {sum(i["state"] == "CLOSED" for i in issues)}\n')
    for titulo, f in (('Tipo', lambda i: etiqueta(i, 'tipo:')), ('Área', lambda i: etiqueta(i, 'area:')),
                      ('Fase', lambda i: etiqueta(i, 'fase-')), ('Milestone', lambda i: (i.get('milestone') or {}).get('title', '—'))):
        cuenta = Counter(f(i) for i in issues)
        print(f'| {titulo} | Total | Abiertos | Cerrados |')
        print('|---|---|---|---|')
        for clave in sorted(cuenta):
            grupo = [i for i in issues if f(i) == clave]
            print(f'| {clave} | {len(grupo)} | {sum(i["state"] == "OPEN" for i in grupo)} | {sum(i["state"] == "CLOSED" for i in grupo)} |')
        print()
    enlaces = Counter()
    for pr in prs:
        m = ENLACE_EPICA.search(pr.get('body') or '')
        enlaces[m.group(1).lower() if m else 'sin enlace'] += 1
    print(f'PR con `Parte de #n`: {enlaces["parte de"]} · con `Closes #n`: {enlaces["closes"]} · sin enlace a una épica: {enlaces["sin enlace"]} (de {len(prs)} PR fusionados).')
    bugs = [i for i in issues if etiqueta(i, 'tipo:') == 'bug']
    print(f'Issues de tipo bug: {len(bugs)}.')


def autotest():
    assert conforme('feat(ventas): lista de precios [HU-09]') == (True, True)
    assert conforme('docs(informe): sección 5 [S3] (#198)') == (True, True)
    assert conforme('feat(pruebas): carga con k6 [HU-28] (#196)') == (True, True)
    assert conforme('Arregla un error') == (False, False)
    assert conforme('fix: arreglo sin etiqueta') == (True, False)
    assert conforme('feat(x): varias [HU-01, HU-02]') == (True, True)
    prs = [{'number': 1, 'title': 'feat(a): b [HU-01]', 'author': {'login': 'ana'}, 'body': 'Parte de #5',
            'commits': [{'messageHeadline': 'feat(a): b [HU-01]', 'authors': [{'login': 'ana', 'name': 'Ana'}]},
                        {'messageHeadline': 'Merge branch develop', 'authors': [{'login': 'ana', 'name': 'Ana'}]},
                        {'messageHeadline': 'arreglo', 'authors': [{'login': 'ben', 'name': 'Ben'}]}]}]
    por_autor, tipos, total = commits(prs)
    assert por_autor == {'ana': 1, 'ben': 1} and total['commits'] == 2 and total['convencion'] == 1 and tipos == {'feat': 1}
    assert ENLACE_EPICA.search('## HU\nCloses #139').group(1) == 'Closes'
    print('autotest OK: la convención, las etiquetas y los conteos dan los valores esperados.')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--autotest', action='store_true')
    if p.parse_args().autotest:
        return autotest()
    # La lista completa con los commits supera el límite de la API de GitHub: se pide el detalle de cada PR por separado
    numeros = [pr['number'] for pr in gh('pr', 'list', '--repo', REPO, '--state', 'merged', '--limit', '500', '--json', 'number')]
    prs = [gh('pr', 'view', str(n), '--repo', REPO, '--json', 'number,title,author,body,commits') for n in sorted(numeros)]
    issues = gh('issue', 'list', '--repo', REPO, '--state', 'all', '--limit', '200', '--json', 'number,state,labels,milestone')
    print('## 6.7 Commits\n')
    tabla_commits(prs)
    print('\n## 6.8 Issues\n')
    tabla_issues(issues, prs)


if __name__ == '__main__':
    sys.exit(main())
