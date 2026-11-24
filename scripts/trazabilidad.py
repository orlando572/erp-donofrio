#!/usr/bin/env python3
"""Genera docs/informe/trazabilidad.md: requisito (RF/RNF) → HU → PR → módulo o archivo → prueba → evidencia.

Los datos de los PR salen de la tabla fechada docs/capturas/sprint-3/S3-informe6_prs_fusionados.tsv
(columnas numero, rama y titulo; los títulos llevan «[HU-xx]») o, con --gh, de `gh pr list --state merged`
(solo lectura). Las filas de requisitos, HU, archivos, pruebas y evidencias están en las tablas REQUISITOS de
este archivo y se COMPRUEBAN al generar: si un archivo, una evidencia o una función de prueba no existe, el
script termina con error y no escribe nada.

Uso (desde la raíz del repo):
    python3 scripts/trazabilidad.py            # usa el TSV del repo
    python3 scripts/trazabilidad.py --gh       # consulta GitHub con gh
    python3 scripts/trazabilidad.py --salida otra/ruta.md
"""
import argparse
import csv
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TSV = RAIZ / 'docs/capturas/sprint-3/S3-informe6_prs_fusionados.tsv'
SALIDA = RAIZ / 'docs/informe/trazabilidad.md'
TESTS = 'addons/donofrio_base/tests/'
MOD = 'addons/donofrio_base/'
S1, S2, S3 = 'docs/capturas/sprint-1/', 'docs/capturas/sprint-2/', 'docs/capturas/sprint-3/'
URL_PR = 'https://github.com/orlando572/erp-donofrio/pull/'

# HU de la Fase 2 (no implementadas): se listan para que la matriz diga «sin PR»
HU_FASE_2 = {'HU-17', 'HU-18', 'HU-19', 'HU-20', 'HU-21', 'HU-22', 'HU-24'}

# Cada requisito: id, texto, fase, HU, archivos (módulo, scripts, workflows), pruebas, evidencias, estado.
# pruebas: 'archivo.py' (todas sus pruebas) o 'archivo.py::test_nombre' (una prueba); en TESTS.
# evidencias: ruta o patrón (con *); se muestra con el número de archivos que coincide.
F2 = 'Diseñado – trabajo futuro'
REQUISITOS = [
    # RF
    ('RF001', 'Registrar oportunidades por canal en un embudo CRM', 'F1', ['HU-08'], [MOD + 'data/crm_data.xml'],
     ['test_crm.py'], [S2 + 'HU-08_*'], 'Implementado'),
    ('RF002', 'Cotizar y confirmar pedidos con listas de precios por canal y temporada', 'F1', ['HU-09'],
     [MOD + 'data/precios_data.xml', MOD + 'data/clientes_data.xml'],
     ['test_precios.py', 'test_flujo_venta.py::test_pedido_entrega_por_fefo_y_factura_con_ruc'],
     [S2 + 'HU-09_*'], 'Implementado'),
    ('RF003', 'Vender en el punto de venta con boleta', 'F1', ['HU-10'], [MOD + 'hooks.py'],
     ['test_pdv.py'], [S2 + 'HU-10_*'], 'Implementado'),
    ('RF004', 'Liquidar diariamente a los heladeros ambulantes (`donofrio_heladeros`)', 'F2', ['HU-20', 'HU-21'],
     [], [], [], F2),
    ('RF005', 'Gestionar almacenes y ubicaciones con cámaras de frío', 'F1', ['HU-06'],
     [MOD + 'data/almacenes_data.xml'], ['test_almacenes.py'], [S1 + 'HU-06_*'], 'Implementado'),
    ('RF006', 'Controlar lotes con vencimiento y salida FEFO', 'F1', ['HU-11'],
     [MOD + 'data/productos_data.xml'], ['test_fefo.py'], [S2 + 'HU-11_*'], 'Implementado'),
    ('RF007', 'Recibir insumos y despachar pedidos', 'F1', ['HU-12'],
     [MOD + 'data/almacenes_data.xml'], ['test_recepcion_despacho.py'], [S2 + 'HU-12_*'], 'Implementado'),
    ('RF008', 'Registrar temperaturas y alertar fuera de rango (cadena de frío)', 'F2', ['HU-19'],
     [], [], [], F2),
    ('RF009', 'Mantener listas de materiales (recetas) y centros de trabajo', 'F1', ['HU-07'],
     [MOD + 'data/produccion_data.xml', MOD + 'data/productos_data.xml'], ['test_productos.py'],
     [S1 + 'HU-07_*'], 'Implementado'),
    ('RF010', 'Planificar y ejecutar órdenes de producción con lote', 'F1', ['HU-14', 'HU-33'],
     [MOD + 'data/produccion_data.xml'],
     ['test_produccion.py', 'test_flujo_compra_produccion.py'], [S2 + 'HU-14_*'], 'Implementado'),
    ('RF011', 'Inspeccionar la calidad por puntos de control (`donofrio_calidad`)', 'F2', ['HU-17'],
     [], [], [], F2),
    ('RF012', 'Emitir el certificado de calidad del lote (`donofrio_calidad`)', 'F2', ['HU-18'],
     [], [], [], F2),
    ('RF013', 'Tablero gerencial de KPIs', 'F1 (dashboards estándar)', ['HU-23'],
     [MOD + 'data/vistas_gerencia_data.xml'], ['test_gerencia.py'], [S3 + 'HU-23_*'],
     'Implementado con dashboards estándar; el tablero OWL propio (HU-22): ' + F2),
    ('RF014', 'Análisis por línea, canal y temporada', 'F1', ['HU-23'],
     [MOD + 'data/vistas_gerencia_data.xml'],
     ['test_gerencia.py::test_ventas_por_linea_canal_y_mes_agrupa_con_datos'],
     [S3 + 'HU-23_vista_ventas_linea_canal_mes.png'], 'Implementado'),
    ('RF015', 'Comprar insumos con reabastecimiento mín./máx.', 'F1', ['HU-13'],
     [MOD + 'data/reabastecimiento_data.xml'], ['test_reabastecimiento.py'], [S2 + 'HU-13_*'], 'Implementado'),
    ('RF016', 'Emitir facturas y boletas con IGV (`l10n_pe`)', 'F1', ['HU-03', 'HU-15'],
     [MOD + 'data/compania_data.xml', MOD + 'models/sale_order.py'],
     ['test_compania.py', 'test_facturacion.py'], [S1 + 'HU-03_*', S2 + 'HU-15_*'], 'Implementado'),
    ('RF017', 'Gestionar el organigrama, empleados y puestos', 'F1', ['HU-05'],
     [MOD + 'data/rrhh_data.xml'], ['test_rrhh.py'], [S1 + 'HU-05_*'], 'Implementado'),
    ('RF018', 'Gestionar usuarios y roles por área', 'F1', ['HU-04'],
     [MOD + 'security/donofrio_security.xml', MOD + 'security/ir.model.access.csv', MOD + 'data/usuarios_data.xml'],
     ['test_seguridad.py'], [S1 + 'HU-04_*'], 'Implementado'),
    # RNF
    ('RNF001', 'Portabilidad: Chrome, Firefox y Edge; responsive', 'F1', ['HU-09', 'HU-10'], [], [], [],
     'Sin evidencia: la prueba manual en 3 navegadores no se registró'),
    ('RNF002', 'Rendimiento: p95 < 2 s con 20 usuarios (k6)', 'F1', ['HU-28'],
     ['scripts/perf/carga.js', 'scripts/perf/k6.sh'], [],
     [S3 + 'HU-28_k6_resumen.json', S3 + 'HU-28_k6_esfuerzo_resumen.json', S3 + 'HU-28_evidencia_k6_zap.txt'],
     'Cumple (p95 de 12 ms)'),
    ('RNF003', 'Usabilidad: SUS ≥ 70 y tareas en ≤ 3 pasos', 'F1', ['HU-30'],
     ['scripts/usabilidad_sus.py', 'docs/usabilidad/plan_de_pruebas.md', 'docs/usabilidad/formulario_sus.md'],
     [], ['docs/informe/06_12_usabilidad.md'], 'Parcial: método listo, sin mediciones con las 5 personas'),
    ('RNF004', 'Trazabilidad del 100 % de los lotes (de la OP al cliente)', 'F1', ['HU-14', 'HU-33'],
     [MOD + 'data/produccion_data.xml'],
     ['test_flujo_compra_produccion.py::test_flujo_completo_del_planificador_al_lote_terminado',
      'test_produccion.py::test_el_lote_producido_sale_despues_por_fefo'],
     [S3 + 'S3-informe6_evidencia_tests.txt'], 'Cumple'),
    ('RNF005', 'Integridad: no se despacha un lote vencido (y, en F2, uno rechazado)', 'F1', ['HU-11'],
     [MOD + 'data/productos_data.xml'],
     ['test_fefo.py::test_lote_vencido_no_se_reserva', 'test_fefo.py::test_lote_en_fecha_de_retiro_no_se_reserva',
      'test_flujo_venta.py::test_un_lote_vencido_no_entra_en_la_entrega_del_pedido'],
     [S3 + 'S3-informe6_evidencia_tests.txt'],
     'Parcial: cumple en inventario y ventas; no en el PdV; el lote rechazado depende de la F2'),
    ('RNF006', 'Respaldo diario (RPO 24 h), réplica (RPO de segundos) y RTO ≤ 2 h', 'F1', ['HU-25', 'HU-26'],
     ['scripts/backup.sh', 'scripts/restore.sh', 'scripts/verificar_backup.sh', 'scripts/verificar_replica.sh',
      'docker/postgres/primary', 'docker/postgres/replica'],
     [], [S3 + 'HU-26_evidencia_respaldo.txt', S3 + 'HU-25_evidencia_replica.txt'],
     'Cumple (RTO medido de 31 s); la promoción de la réplica no se probó'),
    ('RNF007', 'Mantenibilidad: lint y tests en CI, sin API obsoleta', 'F1', ['HU-02'],
     ['.github/workflows/ci.yml', 'scripts/test.sh', 'scripts/check_legacy.sh'], ['test_instalacion.py'],
     [S3 + 'S3-informe6_evidencia_tests.txt'], 'Cumple'),
    ('RNF008', 'El tablero carga en < 3 s; Lighthouse ≥ 80 en el login', 'F1', ['HU-23', 'HU-28'],
     ['scripts/perf/lighthouse.py'], [], [S3 + 'HU-28_lighthouse_resultados.csv', 'docs/informe/04_06_wpo.md'],
     'Parcial: login 100 y dashboard 80; el backend queda en 59'),
    ('RNF009', 'Seguridad: RBAC, HTTPS, gestor de BD cerrado y 2FA', 'F1', ['HU-04', 'HU-27', 'HU-28'],
     ['docker/nginx/seguridad.conf', MOD + 'data/seguridad_data.xml', 'scripts/verificar_despliegue.sh',
      'scripts/perf/zap.sh'],
     ['test_seguridad.py', 'test_hardening.py'],
     [S3 + 'HU-27_evidencia_seguridad.txt', S3 + 'HU-28_zap_reporte.html'],
     'Cumple con límites (ZAP pasivo y sin sesión)'),
    ('RNF010', 'Auditoría de cambios en datos sensibles', 'F1', ['HU-27'],
     [MOD + 'models/auditlog_rule.py', MOD + 'data/seguridad_data.xml'],
     ['test_hardening.py::test_cambio_de_precio_queda_auditado',
      'test_hardening.py::test_reglas_de_auditoria_confirmadas'],
     [S3 + 'HU-27_evidencia_seguridad.txt'], 'Cumple para precios, pedidos y compras'),
    ('RNF011', 'Disponibilidad ≥ 99 %; reinicio automático y healthcheck', 'F1', ['HU-01'],
     ['docker-compose.yml'], [], [S1 + 'S1_docker_compose_ps.png'],
     'Parcial: hay healthchecks y reinicio; falta la medición (Uptime Kuma no se implementó)'),
    ('RNF012', 'Reproducibilidad: el entorno se levanta con un comando', 'F1', ['HU-01', 'HU-29'],
     ['docker-compose.yml', 'scripts/init_db.sh', '.github/workflows/release.yml', 'scripts/probar_imagen.sh'],
     [], [S3 + 'HU-29_evidencia_release.txt', S1 + 'HU-01_odoo_login.png'],
     'Implementado; la imagen en GHCR se publica en el Gate 0'),
    ('RNF013', 'Ley 29733: datos personales ficticios y mínimos', 'F1', ['HU-03', 'HU-05', 'HU-16'],
     [MOD + 'data/clientes_data.xml', MOD + 'data/rrhh_data.xml'], ['test_clientes.py'],
     ['docs/informe/05_10_a_05_12_seguridad.md'], 'Parcial: datos ficticios; sin política de privacidad'),
]

# HU que no son de un RF concreto pero tienen PR (normas, tests, infraestructura)
HU_EXTRA = {
    'HU-32': 'Mesa de servicios TI en Project (ITIL, SLA)',
    'HU-33': 'Pruebas integrales (pedido → factura; compra → OP → lote)',
    'HU-29': 'Release: imagen GHCR y zip (se publica en el Gate 0)',
    'HU-01': 'Entorno Docker con Odoo 19 y PostgreSQL 16',
    'HU-02': 'Esqueleto de donofrio_base, `test.sh` y CI',
    'HU-16': 'Transacciones de demostración (script con semilla fija)',
}


def leer_prs(usar_gh):
    """Devuelve [(número, rama, título)] de los PR fusionados."""
    if usar_gh:
        salida = subprocess.run(
            ['gh', 'pr', 'list', '--state', 'merged', '--limit', '500', '--json', 'number,title,headRefName'],
            capture_output=True, text=True, check=True).stdout
        return sorted((p['number'], p['headRefName'], p['title']) for p in json.loads(salida))
    with open(TSV, encoding='utf-8') as f:
        return sorted((int(r['numero']), r['rama'], r['titulo']) for r in csv.DictReader(f, delimiter='\t'))


def hu_de_los_prs(prs):
    """HU → [números de PR] con las HU de la rama o del título (`[HU-01, HU-02]`)."""
    mapa = {}
    for numero, rama, titulo in prs:
        for hu in set(re.findall(r'HU-\d+', titulo)) | set(re.findall(r'HU-\d+', rama)):
            mapa.setdefault(hu, []).append(numero)
    return mapa


def celda_pr(hus, mapa):
    partes = []
    for hu in hus:
        numeros = mapa.get(hu)
        if numeros:
            enlaces = ', '.join(f'[#{n}]({URL_PR}{n})' for n in sorted(numeros))
            partes.append(f'{hu}: {enlaces}')
        else:
            partes.append(f'{hu}: sin PR' + (' (Fase 2)' if hu in HU_FASE_2 else ''))
    return '<br>'.join(partes)


def contar_pruebas(archivo):
    texto = (RAIZ / TESTS / archivo).read_text(encoding='utf-8')
    return len(re.findall(r'^\s+def test_', texto, flags=re.M))


def celda_pruebas(pruebas, errores, req):
    partes = []
    for p in pruebas:
        archivo, _, funcion = p.partition('::')
        ruta = RAIZ / TESTS / archivo
        if not ruta.exists():
            errores.append(f'{req}: no existe {TESTS}{archivo}')
            continue
        if funcion:
            if not re.search(rf'^\s+def {re.escape(funcion)}\(', ruta.read_text(encoding='utf-8'), flags=re.M):
                errores.append(f'{req}: no existe {archivo}::{funcion}')
            partes.append(f'`{archivo}::{funcion}`')
        else:
            partes.append(f'`{archivo}` ({contar_pruebas(archivo)})')
    return '<br>'.join(partes) if partes else '—'


def celda_rutas(rutas, errores, req):
    partes = []
    for ruta in rutas:
        coinciden = glob.glob(str(RAIZ / ruta))
        if not coinciden:
            errores.append(f'{req}: no existe {ruta}')
            continue
        if '*' in ruta:
            partes.append(f'`{ruta}` ({len(coinciden)} archivos)')
        else:
            partes.append(f'`{ruta}`')
    return '<br>'.join(partes) if partes else '—'


def tabla(titulo, filas, mapa, errores):
    lineas = [f'### {titulo}', '',
              '| Requisito | Fase | HU → PR | Módulo o archivo | Prueba (n.º de pruebas) | Evidencia | Estado |',
              '|---|---|---|---|---|---|---|']
    for req, texto, fase, hus, archivos, pruebas, evidencias, estado in filas:
        lineas.append('| ' + ' | '.join([
            f'**{req}** {texto}', fase, celda_pr(hus, mapa), celda_rutas(archivos, errores, req),
            celda_pruebas(pruebas, errores, req), celda_rutas(evidencias, errores, req), estado]) + ' |')
    return lineas + ['']


def generar(prs):
    mapa = hu_de_los_prs(prs)
    errores = []
    filas_rf = [r for r in REQUISITOS if r[0].startswith('RF')]
    filas_rnf = [r for r in REQUISITOS if r[0].startswith('RNF')]
    f2 = [r for r in REQUISITOS if r[7] == F2]
    pruebas_total = sum(len(re.findall(r'^\s+def test_', p.read_text(encoding='utf-8'), flags=re.M))
                        for p in (RAIZ / TESTS).glob('test_*.py'))

    md = [
        '# Matriz de trazabilidad: requisito → HU → PR → módulo → prueba → evidencia',
        '',
        '> **Estado:** borrador del Sprint 3 · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** '
        '[4.2.2](04_02_requerimientos_funcionales.md), [4.2.3](04_02_requerimientos_no_funcionales.md), '
        '[6.4 a 6.6](06_04_a_06_06_repositorio.md), [6.9 a 6.13](06_09_a_06_13_pruebas.md)',
        '>',
        '> **Generada por `scripts/trazabilidad.py`** a partir de los PR fusionados '
        '([`S3-informe6_prs_fusionados.tsv`](../capturas/sprint-3/S3-informe6_prs_fusionados.tsv), 23/11/2026) y de '
        'las tablas de requisitos del propio script. **Cada celda se comprueba al generar:** el script falla si un '
        'archivo, una evidencia o una función de prueba no existe. Para regenerar: `python3 scripts/trazabilidad.py` '
        '(o `--gh` para volver a leer los PR de GitHub). No edites este archivo a mano.',
        '',
        '**Cómo leerla.** *HU → PR*: las HU de cada requisito y los PR fusionados a `develop` cuyo título o rama '
        'llevan esa HU. *Prueba*: archivo de `addons/donofrio_base/tests/` con su número de pruebas, o una prueba '
        'concreta. *Evidencia*: archivos del repositorio (el número entre paréntesis es cuántos archivos coinciden '
        'con el patrón). *Estado*: el real al 23/11/2026, que puede ser distinto del de las tablas 2 y 3 del informe, '
        'escritas en el Sprint 1.',
        '',
        f'**Resumen.** {len(filas_rf)} RF y {len(filas_rnf)} RNF. Los requisitos de la Fase 2 sin implementar '
        f'({len(f2)} filas: RF004, RF008, RF011 y RF012) están como «{F2}»; la parte propia de RF013 (tablero OWL) '
        'también. Las pruebas de `donofrio_base`: '
        f'**{pruebas_total}** (ver [6.10](06_09_a_06_13_pruebas.md)).',
        '',
        '> **Nota posterior al 23/11/2026.** La matriz es la foto de la Fase 1: las filas de RF004, RF008, RF011 y RF012 '
        'siguen como «Diseñado – trabajo futuro» porque se escribieron antes de construir los módulos propios. Hoy están '
        '**Implementados**: RF011 y RF012 en M1 ([5.5b](05_05_modulo_donofrio_calidad.md)), RF004 en M2 '
        '([5.5c](05_05_modulo_donofrio_heladeros.md)) y RF008 en M3 ([5.5d](05_05_modulo_donofrio_frio.md), HU-19, '
        '29 pruebas en `addons/donofrio_calidad/tests/test_frio.py`). El estado vigente está en [4.2.2](04_02_requerimientos_funcionales.md) '
        'y en el [anexo 10.1](anexo_10_01_fichas_rf.md); aquí no hay PR de esos módulos porque la matriz lee los PR fusionados al 23/11/2026.',
        '',
        '## Tabla A. Requisitos funcionales (RF)',
        '',
    ]
    md += tabla('RF001 a RF018', filas_rf, mapa, errores)[2:]
    md += ['## Tabla B. Requisitos no funcionales (RNF)', '']
    md += tabla('RNF001 a RNF013', filas_rnf, mapa, errores)[2:]

    md += ['## Tabla C. HU → PR (todas las HU con PR fusionado)', '',
           '| HU | Qué cubre | PR |', '|---|---|---|']
    for hu in sorted(mapa, key=lambda h: int(h.split('-')[1])):
        reqs = sorted({r[0] for r in REQUISITOS if hu in r[3]})
        que = (', '.join(reqs) if reqs else '') + (' · ' if reqs and hu in HU_EXTRA else '') + HU_EXTRA.get(hu, '')
        enlaces = ', '.join(f'[#{n}]({URL_PR}{n})' for n in sorted(mapa[hu]))
        md.append(f'| {hu} | {que or "—"} | {enlaces} |')
    sin = sorted(h for h in {hu for r in REQUISITOS for hu in r[3]} if h not in mapa)
    md += ['', f'**HU de requisitos sin PR fusionado:** {", ".join(sin)} (Fase 2: no se implementó ningún módulo '
           'propio; la HU-31 del CRM extendido era opcional y no se hizo).', '']
    md += ['## Qué no cubre esta matriz', '',
           '- Los PR #172 y #176 solo agregan las capturas de HU que se implementaron en otros PR; aparecen junto a '
           'esas HU porque su título las nombra.',
           '- Los PR de documentación (informe, Scrum, capturas) no llevan HU y no aparecen: están en el '
           '[TSV completo](../capturas/sprint-3/S3-informe6_prs_fusionados.tsv).',
           '- La columna *Estado* es la evaluación del 23/11/2026; los criterios de aceptación de cada HU están en '
           'el Project y en los PR.',
           '- La trazabilidad hacia las normas (ISO 27001, ITIL, COBIT) está en el anexo '
           '[10.6](anexo_10_06_soa_iso27001.md).', '']
    return '\n'.join(md), errores


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--gh', action='store_true', help='leer los PR con `gh pr list` en vez del TSV')
    ap.add_argument('--salida', default=str(SALIDA))
    args = ap.parse_args()
    texto, errores = generar(leer_prs(args.gh))
    if errores:
        print('No se escribió nada; hay celdas que no se pueden comprobar:', file=sys.stderr)
        for e in errores:
            print('  -', e, file=sys.stderr)
        return 1
    Path(args.salida).write_text(texto + '\n', encoding='utf-8')
    print(f'OK: {args.salida}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
