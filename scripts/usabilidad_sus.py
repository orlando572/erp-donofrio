#!/usr/bin/env python3
"""HU-30: calcula el SUS y los tiempos de las pruebas de usabilidad (6.12, RNF003).

Uso:  python3 scripts/usabilidad_sus.py docs/usabilidad/resultados.csv
      python3 scripts/usabilidad_sus.py --autotest        (comprueba la fórmula con casos conocidos)

El CSV tiene una fila por persona (ver docs/usabilidad/resultados_plantilla.csv): ``tN_ok`` (si/no), ``tN_seg`` (segundos)
y ``s1`` a ``s10`` (respuestas de 1 a 5). SUS = ((suma de impares − 1) + (suma de pares: 5 − valor)) × 2.5, de 0 a 100.
RNF003 se cumple si el SUS promedio es ≥ 70.
"""
import csv
import statistics
import sys

META_SUS = 70
OBJETIVO_SEG = {1: 90, 2: 180, 3: 150, 4: 90}      # ver docs/usabilidad/plan_de_pruebas.md
SI = {'si', 'sí', 's', '1', 'true', 'x'}


def sus(respuestas):
    """Puntaje SUS (0 a 100) de las 10 respuestas (1 a 5), en el orden del cuestionario."""
    if len(respuestas) != 10 or any(not 1 <= r <= 5 for r in respuestas):
        raise ValueError(f'se esperan 10 respuestas de 1 a 5: {respuestas}')
    # los enunciados impares (posición 0, 2, ...) son positivos y los pares, negativos
    puntos = sum((r - 1) if i % 2 == 0 else (5 - r) for i, r in enumerate(respuestas))
    return puntos * 2.5


def autotest():
    assert sus([3] * 10) == 50
    assert sus([5, 1] * 5) == 100
    assert sus([1, 5] * 5) == 0
    assert sus([4, 2] * 5) == 75
    assert sus([4, 2, 4, 2, 4, 2, 4, 2, 4, 3]) == 72.5
    for malo in ([3] * 9, [3] * 9 + [6], [0] + [3] * 9):
        try:
            sus(malo)
        except ValueError:
            continue
        raise AssertionError(f'debió rechazar {malo}')
    print('autotest OK: la fórmula del SUS da los valores esperados.')


def leer(ruta):
    with open(ruta, newline='', encoding='utf-8') as f:
        return [fila for fila in csv.DictReader(f) if (fila.get('participante') or '').strip()]


def resumen(filas):
    if not filas:
        sys.exit('El CSV no tiene participantes: llena una fila por persona.')
    puntajes = []
    print('Participante  SUS')
    for fila in filas:
        valor = sus([int(fila[f's{i}']) for i in range(1, 11)])
        puntajes.append(valor)
        print(f"{fila['participante']:<12}  {valor:5.1f}")
    promedio = statistics.mean(puntajes)
    print(f'\nSUS promedio: {promedio:.1f}  (mediana {statistics.median(puntajes):.1f}, mín. {min(puntajes):.1f}, máx. {max(puntajes):.1f}, n = {len(puntajes)})')
    print(f'RNF003 (SUS ≥ {META_SUS}): ' + ('SÍ se cumple' if promedio >= META_SUS else 'NO se cumple'))
    if len(puntajes) < 5:
        print(f'Aviso: el plan pide 5 participantes y hay {len(puntajes)}.')

    print('\nTarea  Éxito      Tiempo mediano (s)  Objetivo (s)')
    for n, objetivo in OBJETIVO_SEG.items():
        oks = [(fila[f't{n}_ok'] or '').strip().lower() in SI for fila in filas]
        tiempos = [float(fila[f't{n}_seg']) for fila, ok in zip(filas, oks) if ok and fila[f't{n}_seg']]
        mediana = f'{statistics.median(tiempos):.0f}' if tiempos else '-'
        print(f'T{n}     {sum(oks)}/{len(oks)} ({100 * sum(oks) / len(oks):.0f} %)   {mediana:>18}  {objetivo:>12}')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--autotest':
        autotest()
    elif len(sys.argv) == 2:
        resumen(leer(sys.argv[1]))
    else:
        sys.exit(__doc__)
