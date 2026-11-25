#!/usr/bin/env python3
"""Genera docs/informe/trazabilidad.md: requisito (RF/RNF) → HU → PR → módulo o archivo → prueba → evidencia.

Los datos de los PR salen de la tabla fechada docs/capturas/sprint-4/S4_informe_final_prs_fusionados.tsv
(columnas numero, rama y titulo; los títulos llevan «[HU-xx]») o, con --gh, de `gh pr list --state merged`
(solo lectura). Las pruebas se buscan en addons/donofrio_base/tests/ o, con el prefijo `calidad/`, `heladeros/`
o `tablero/`, en el módulo propio de la Fase 2. Las filas de requisitos, HU, archivos, pruebas y evidencias están en las tablas REQUISITOS de
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
TSV = RAIZ / 'docs/capturas/sprint-4/S4_informe_final_prs_fusionados.tsv'
SALIDA = RAIZ / 'docs/informe/trazabilidad.md'
TESTS = 'addons/donofrio_base/tests/'
MOD = 'addons/donofrio_base/'
S1, S2, S3 = 'docs/capturas/sprint-1/', 'docs/capturas/sprint-2/', 'docs/capturas/sprint-3/'
S4 = 'docs/capturas/sprint-4/'
ADDONS = 'addons/'
URL_PR = 'https://github.com/orlando572/erp-donofrio/pull/'

# HU de la Fase 2 (implementadas en M1 a M4); HU-31 (landing opcional) no se hizo y queda «sin PR»
HU_FASE_2 = {'HU-17', 'HU-18', 'HU-19', 'HU-20', 'HU-21', 'HU-22', 'HU-24'}

# Cada requisito: id, texto, fase, HU, archivos (módulo, scripts, workflows), pruebas, evidencias, estado.
# pruebas: 'archivo.py' (todas sus pruebas) o 'archivo.py::test_nombre' (una prueba); en TESTS.
# evidencias: ruta o patrón (con *); se muestra con el número de archivos que coincide.
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
     [ADDONS + 'donofrio_heladeros/models/liquidacion.py', ADDONS + 'donofrio_heladeros/report/liquidacion_report.xml'],
     ['heladeros/test_liquidacion.py'], [S4 + 'HU-20_*', S4 + 'HU-21_*'],
     'Implementado (M2, `v1.2.0`)'),
    ('RF005', 'Gestionar almacenes y ubicaciones con cámaras de frío', 'F1', ['HU-06'],
     [MOD + 'data/almacenes_data.xml'], ['test_almacenes.py'], [S1 + 'HU-06_*'], 'Implementado'),
    ('RF006', 'Controlar lotes con vencimiento y salida FEFO', 'F1', ['HU-11'],
     [MOD + 'data/productos_data.xml'], ['test_fefo.py'], [S2 + 'HU-11_*'], 'Implementado'),
    ('RF007', 'Recibir insumos y despachar pedidos', 'F1', ['HU-12'],
     [MOD + 'data/almacenes_data.xml'], ['test_recepcion_despacho.py'], [S2 + 'HU-12_*'], 'Implementado'),
    ('RF008', 'Registrar temperaturas y alertar fuera de rango (cadena de frío)', 'F2', ['HU-19'],
     [ADDONS + 'donofrio_calidad/models/calidad_temperatura.py', ADDONS + 'donofrio_calidad/models/stock_lot.py'],
     ['calidad/test_frio.py'], [S4 + 'HU-19_*'], 'Implementado (M3, `v1.3.0`)'),
    ('RF009', 'Mantener listas de materiales (recetas) y centros de trabajo', 'F1', ['HU-07'],
     [MOD + 'data/produccion_data.xml', MOD + 'data/productos_data.xml'], ['test_productos.py'],
     [S1 + 'HU-07_*'], 'Implementado'),
    ('RF010', 'Planificar y ejecutar órdenes de producción con lote', 'F1', ['HU-14', 'HU-33'],
     [MOD + 'data/produccion_data.xml'],
     ['test_produccion.py', 'test_flujo_compra_produccion.py'], [S2 + 'HU-14_*'], 'Implementado'),
    ('RF011', 'Inspeccionar la calidad por puntos de control (`donofrio_calidad`)', 'F2', ['HU-17'],
     [ADDONS + 'donofrio_calidad/models/calidad_inspeccion.py', ADDONS + 'donofrio_calidad/models/calidad_punto.py'],
     ['calidad/test_inspeccion.py'], [S4 + 'HU-17_*'], 'Implementado (M1, `v1.1.0`)'),
    ('RF012', 'Emitir el certificado de calidad del lote (`donofrio_calidad`)', 'F2', ['HU-18'],
     [ADDONS + 'donofrio_calidad/report/calidad_report.xml', ADDONS + 'donofrio_calidad/models/report_certificado.py'],
     ['calidad/test_inspeccion.py::test_certificado_de_una_inspeccion_aprobada',
      'calidad/test_inspeccion.py::test_no_hay_certificado_si_no_esta_aprobada'],
     [S4 + 'HU-18_*'], 'Implementado (M1, `v1.1.0`)'),
    ('RF013', 'Tablero gerencial de KPIs', 'F1 (dashboards estándar) y F2 (tablero OWL de M4)', ['HU-23', 'HU-22', 'HU-24'],
     [MOD + 'data/vistas_gerencia_data.xml', ADDONS + 'donofrio_tablero/models/tablero.py',
      ADDONS + 'donofrio_tablero/static/src/tablero/tablero.js'],
     ['test_gerencia.py', 'tablero/test_tablero.py'], [S3 + 'HU-23_*', S4 + 'HU-22_*'],
     'Implementado: dashboards estándar (HU-23) y tablero OWL propio (HU-22, M4, `v1.4.0`)'),
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
    ('RNF001', 'Portabilidad: navegador de escritorio y vista adaptable', 'F1', ['HU-09', 'HU-10'], [], [],
     [S4 + 'S4_movil_*'], 'Parcial: tablero y liquidación revisados en una ventana de 375 × 812, con Chrome'),
    ('RNF002', 'Rendimiento: p95 < 2 s con 20 usuarios (k6)', 'F1', ['HU-28'],
     ['scripts/perf/carga.js', 'scripts/perf/k6.sh'], [],
     [S3 + 'HU-28_k6_resumen.json', S3 + 'HU-28_k6_esfuerzo_resumen.json', S3 + 'HU-28_evidencia_k6_zap.txt'],
     'Cumple (p95 de 12 ms)'),
    ('RNF003', 'Usabilidad: español y tareas en ≤ 3 pasos', 'F1', ['HU-03', 'HU-24'], [], [],
     ['docs/informe/06_12_usabilidad.md'], 'Cumple con límites: revisión por roles del 25/11 y evaluación heurística de M1 a M4'),
    ('RNF004', 'Trazabilidad del 100 % de los lotes (de la OP al cliente)', 'F1', ['HU-14', 'HU-33'],
     [MOD + 'data/produccion_data.xml'],
     ['test_flujo_compra_produccion.py::test_flujo_completo_del_planificador_al_lote_terminado',
      'test_produccion.py::test_el_lote_producido_sale_despues_por_fefo'],
     [S3 + 'S3-informe6_evidencia_tests.txt'], 'Cumple'),
    ('RNF005', 'Integridad: no se despacha un lote vencido ni uno rechazado por calidad', 'F1 y F2', ['HU-11', 'HU-17'],
     [MOD + 'data/productos_data.xml', ADDONS + 'donofrio_calidad/models/stock_move_line.py'],
     ['test_fefo.py::test_lote_vencido_no_se_reserva', 'test_fefo.py::test_lote_en_fecha_de_retiro_no_se_reserva',
      'test_flujo_venta.py::test_un_lote_vencido_no_entra_en_la_entrega_del_pedido',
      'calidad/test_inspeccion.py::test_un_lote_rechazado_no_se_despacha',
      'calidad/test_pdv.py::test_el_pdv_no_saca_del_stock_un_lote_rechazado'],
     [S3 + 'S3-informe6_evidencia_tests.txt'],
     'Cumple con límites: el PdV no verifica el vencimiento (el cajero escribe el lote)'),
    ('RNF006', 'Respaldo diario (RPO 24 h), réplica (RPO de segundos) y RTO ≤ 2 h', 'F1', ['HU-25', 'HU-26'],
     ['scripts/backup.sh', 'scripts/restore.sh', 'scripts/verificar_backup.sh', 'scripts/verificar_replica.sh',
      'docker/postgres/primary', 'docker/postgres/replica'],
     [], [S3 + 'HU-26_evidencia_respaldo.txt', S3 + 'HU-25_evidencia_replica.txt'],
     'Cumple (RTO medido de 31 s); la promoción de la réplica no se probó'),
    ('RNF007', 'Mantenibilidad: lint y tests en CI, sin API obsoleta', 'F1', ['HU-02'],
     ['.github/workflows/ci.yml', 'scripts/test.sh', 'scripts/check_legacy.sh'], ['test_instalacion.py'],
     [S3 + 'S3-informe6_evidencia_tests.txt'], 'Cumple'),
    ('RNF008', 'El tablero carga en < 3 s; Lighthouse ≥ 80 en el login', 'F1 y F2', ['HU-23', 'HU-28', 'HU-22'],
     ['scripts/perf/lighthouse.py', S4 + 'S4_lighthouse_m4.py'], ['tablero/test_tablero.py::test_carga_en_menos_de_3_segundos'],
     [S3 + 'HU-28_lighthouse_resultados.csv', S4 + 'S4_lighthouse_m4_resultados.csv', 'docs/informe/04_06_wpo.md'],
     'Parcial: login 100, dashboard 80 y tablero de M4 con LCP de 2,11 s; tablero 76 y backend 59 (límite conocido)'),
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
     'Implementado; releases v1.0.0 a v1.4.0 publicadas con su imagen y su zip'),
    ('RNF013', 'Ley 29733: datos personales ficticios y mínimos', 'F1', ['HU-03', 'HU-05', 'HU-16'],
     [MOD + 'data/clientes_data.xml', MOD + 'data/rrhh_data.xml'], ['test_clientes.py'],
     ['docs/informe/05_10_a_05_12_seguridad.md'], 'Parcial: datos ficticios; sin política de privacidad'),
]

# HU que no son de un RF concreto pero tienen PR (normas, tests, infraestructura)
HU_EXTRA = {
    'HU-32': 'Mesa de servicios TI en Project (ITIL, SLA)',
    'HU-33': 'Pruebas integrales (pedido → factura; compra → OP → lote)',
    'HU-29': 'Release: imagen GHCR y zip (publicadas v1.0.0 a v1.4.0)',
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


def ruta_prueba(archivo):
    """`test_x.py` → donofrio_base; `calidad/test_x.py` → addons/donofrio_calidad/tests/ (idem heladeros, tablero)."""
    modulo, _, nombre = archivo.rpartition('/')
    if not modulo:
        return RAIZ / TESTS / archivo, f'{archivo}'
    return RAIZ / ADDONS / f'donofrio_{modulo}' / 'tests' / nombre, f'donofrio_{modulo}/tests/{nombre}'


def contar_pruebas(archivo):
    texto = ruta_prueba(archivo)[0].read_text(encoding='utf-8')
    return len(re.findall(r'^\s+def test_', texto, flags=re.M))


def celda_pruebas(pruebas, errores, req):
    partes = []
    for p in pruebas:
        archivo, _, funcion = p.partition('::')
        ruta, mostrar = ruta_prueba(archivo)
        if not ruta.exists():
            errores.append(f'{req}: no existe {ruta.relative_to(RAIZ)}')
            continue
        if funcion:
            if not re.search(rf'^\s+def {re.escape(funcion)}\(', ruta.read_text(encoding='utf-8'), flags=re.M):
                errores.append(f'{req}: no existe {archivo}::{funcion}')
            partes.append(f'`{mostrar}::{funcion}`')
        else:
            partes.append(f'`{mostrar}` ({contar_pruebas(archivo)})')
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
    carpetas = {m: sum(len(re.findall(r'^\s+def test_', p.read_text(encoding='utf-8'), flags=re.M))
                       for p in (RAIZ / ADDONS / f'donofrio_{m}' / 'tests').glob('test_*.py'))
                for m in ('base', 'calidad', 'heladeros', 'tablero')}
    pruebas_total = sum(carpetas.values())

    md = [
        '# Matriz de trazabilidad: requisito → HU → PR → módulo → prueba → evidencia',
        '',
        '> **Estado:** versión final del Cierre (25/11/2026) · **Autor:** Orlando (SM) · **Revisa:** Evelyn · **Fuente:** '
        '[4.2.2](04_02_requerimientos_funcionales.md), [4.2.3](04_02_requerimientos_no_funcionales.md), '
        '[6.4 a 6.6](06_04_a_06_06_repositorio.md), [6.9 a 6.13](06_09_a_06_13_pruebas.md)',
        '>',
        '> Matriz generada a partir de los PR fusionados (25/11/2026) y de las tablas de requisitos. '
        '**Cada celda se comprobó al generarla:** un archivo, una evidencia o una función de prueba que no existe '
        'hace fallar la generación.',
        '',
        '**Cómo leerla.** *HU → PR*: las HU de cada requisito y los PR fusionados a `develop` cuyo título o rama '
        'llevan esa HU. *Prueba*: archivo de `tests/` de un módulo con su número de pruebas, o una prueba '
        'concreta. *Evidencia*: archivos del repositorio (el número entre paréntesis es cuántos archivos coinciden '
        'con el patrón). *Estado*: el real al 25/11/2026.',
        '',
        f'**Resumen.** {len(filas_rf)} RF y {len(filas_rnf)} RNF. **Los 18 RF están implementados**: los de la Fase 2 '
        '(RF004, RF008, RF011, RF012 y la parte propia de RF013) con los módulos M1 a M4, publicados en las releases '
        '`v1.1.0` a `v1.4.0`. Las pruebas del repositorio: '
        f'**{pruebas_total}** ({carpetas["base"]} de `donofrio_base`, {carpetas["calidad"]} de `donofrio_calidad`, '
        f'{carpetas["heladeros"]} de `donofrio_heladeros` y {carpetas["tablero"]} de `donofrio_tablero`; ver '
        '[6.10](06_09_a_06_13_pruebas.md)).',
        '',
        '> **Limitaciones de la matriz.** RNF001 queda «Parcial» (se revisó en una ventana de 375 × 812) y RNF003 '
        '«Cumple con límites» (revisión por roles y evaluación heurística). '
        'RF008 y RF013 (propio) tienen sus límites en las fichas del [anexo 10.1](anexo_10_01_fichas_rf.md).',
        '',
        '## Tabla A. Requisitos funcionales (RF)',
        '',
    ]
    md += tabla('RF001 a RF018', filas_rf, mapa, errores)[2:]
    md += ['## Tabla B. Requisitos no funcionales (RNF)', '']
    md += tabla('RNF001 a RNF013', filas_rnf, mapa, errores)[2:]

    md += ['## Tabla C. HU → PR (todas las HU con PR fusionado)', '',
           '| HU | Qué cubre | PR |', '|---|---|---|']
    for hu in sorted((h for h in mapa if h != 'HU-30'), key=lambda h: int(h.split('-')[1])):
        reqs = sorted({r[0] for r in REQUISITOS if hu in r[3]})
        que = (', '.join(reqs) if reqs else '') + (' · ' if reqs and hu in HU_EXTRA else '') + HU_EXTRA.get(hu, '')
        enlaces = ', '.join(f'[#{n}]({URL_PR}{n})' for n in sorted(mapa[hu]))
        md.append(f'| {hu} | {que or "—"} | {enlaces} |')
    sin = sorted(h for h in {hu for r in REQUISITOS for hu in r[3]} if h not in mapa)
    md += ['', '**HU de requisitos sin PR fusionado:** ' + (', '.join(sin) if sin else 'ninguna') + '. '
           'La HU-31 (landing «Únete como heladero», opcional) no figura en ningún requisito de esta matriz.', '']
    md += ['## Qué no cubre esta matriz', '',
           '- Los PR #172 y #176 solo agregan las capturas de HU que se implementaron en otros PR; aparecen junto a '
           'esas HU porque su título las nombra.',
           '- Los PR de documentación (informe, Scrum, capturas) no llevan HU y no aparecen: están en el '
           '[TSV completo](../capturas/sprint-4/S4_informe_final_prs_fusionados.tsv).',
           '- Los PR #230 (datos de demostración, HU-16) y #231 (capturas en PNG, HU-16, 17, 20 y 22) aparecen junto '
           'a las HU que nombran en su título.',
           '- La columna *Estado* es la evaluación del 25/11/2026; los criterios de aceptación de cada HU están en '
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
