#!/usr/bin/env python3
"""Informe 4.2.6 y 4.2.7: modelo ER y diseño lógico extraídos de la BD real.

Lee el esquema de una BD de Odoo (tablas, columnas, claves primarias y foráneas, con
``scripts/diccionario_datos.py``) y genera diagramas PlantUML con notación de pata de gallo:

* ``er_nucleo``: modelo ER general de las tablas centrales del núcleo (``TABLAS_NUCLEO``), con las claves y las
  relaciones (4.2.6);
* ``logico_ventas``, ``logico_inventario`` y ``logico_produccion_compras``: diagrama físico de las tablas
  centrales del negocio, con tipo de dato, PK/FK, columnas clave y cardinalidad (4.2.7).

Nada se dibuja a mano: tablas, columnas, tipos, claves y si una FK admite nulo (cardinalidad 0..1 o 1) salen de
``information_schema`` y ``pg_constraint``. Si una columna listada en ``COLUMNAS_CLAVE`` no existe en la BD, el
script falla en vez de inventarla.

Salida en ``docs/diagramas/er/`` (``.puml`` y, con Docker, ``.png`` y ``.svg``). Solo lecturas sobre la BD.

    python3 scripts/diagrama_er.py --bd informe_ddl_tmp
"""
import argparse
import os
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diccionario_datos import COLUMNAS_AUDITORIA, NUCLEO, RAIZ, TABLAS_NUCLEO, Conexion, leer_esquema  # noqa: E402

SALIDA = RAIZ / 'docs/diagramas/er'

# Columnas de negocio que se muestran, además de la PK y las FK, en los diagramas del diseño lógico
COLUMNAS_CLAVE = {
    'sale_order': ['name', 'state', 'date_order', 'amount_untaxed', 'amount_tax', 'amount_total', 'invoice_status'],
    'sale_order_line': ['product_uom_qty', 'price_unit', 'discount', 'qty_delivered', 'qty_invoiced'],
    'crm_lead': ['name', 'type', 'expected_revenue'],
    'pos_order': ['name', 'state', 'date_order', 'amount_total'],
    'res_partner': ['name', 'vat', 'active'],
    'product_template': ['name', 'is_storable', 'tracking', 'list_price', 'use_expiration_date', 'expiration_time'],
    'product_product': ['default_code', 'barcode', 'active'],
    'product_category': ['name', 'complete_name'],
    'product_pricelist': ['name', 'active'],
    'product_pricelist_item': ['applied_on', 'compute_price', 'fixed_price', 'percent_price', 'min_quantity'],
    'product_supplierinfo': ['price', 'min_qty', 'delay'],
    'hr_employee': ['name', 'active'],
    'stock_warehouse': ['name', 'code'],
    'stock_location': ['name', 'complete_name', 'usage', 'removal_strategy_id'],
    'stock_picking_type': ['name', 'code', 'sequence_code'],
    'stock_picking': ['name', 'state', 'scheduled_date', 'date_done', 'origin'],
    'stock_move': ['state', 'product_uom_qty', 'quantity', 'date', 'origin'],
    'stock_move_line': ['quantity', 'date', 'state'],
    'stock_lot': ['name', 'expiration_date', 'use_date', 'removal_date', 'alert_date'],
    'stock_quant': ['quantity', 'reserved_quantity', 'in_date'],
    'stock_warehouse_orderpoint': ['product_min_qty', 'product_max_qty', 'trigger'],
    'mrp_bom': ['code', 'type', 'product_qty'],
    'mrp_bom_line': ['product_qty'],
    'mrp_production': ['name', 'state', 'product_qty', 'date_start', 'date_finished', 'origin'],
    'mrp_workorder': ['name', 'state', 'duration_expected'],
    'mrp_workcenter': ['name', 'costs_hour'],
    'mrp_routing_workcenter': ['name', 'time_cycle_manual'],
    'purchase_order': ['name', 'state', 'date_order', 'amount_total'],
    'purchase_order_line': ['product_qty', 'price_unit', 'qty_received'],
    'account_move': ['name', 'move_type', 'state', 'invoice_date', 'invoice_date_due', 'amount_total', 'payment_state'],
    'account_move_line': ['debit', 'credit', 'quantity', 'price_unit'],
    'account_journal': ['name', 'code', 'type'],
    'res_users': ['login', 'active'],
    'res_groups': ['privilege_id'],
    'auditlog_rule': ['name', 'state'],
    'project_task': ['name', 'priority', 'date_deadline', 'date_end', 'sla_estado'],
}

# Diseño lógico (4.2.7): figuras por flujo del negocio. Las tablas de contexto salen solo con sus claves y columnas clave.
FIGURAS_LOGICAS = OrderedDict([
    ('logico_ventas', ('Ventas, precios y facturación', [
        'res_partner', 'product_pricelist', 'product_pricelist_item', 'product_template', 'product_product',
        'sale_order', 'sale_order_line', 'crm_lead', 'account_move', 'account_move_line', 'account_journal',
    ])),
    ('logico_inventario', ('Inventario: movimientos, lotes y existencias', [
        'stock_warehouse', 'stock_location', 'stock_picking_type', 'stock_picking', 'stock_move', 'stock_move_line',
        'stock_lot', 'stock_quant', 'product_product', 'res_partner',
    ])),
    ('logico_produccion_compras', ('Producción y compras', [
        'product_product', 'product_supplierinfo', 'stock_warehouse_orderpoint', 'mrp_bom', 'mrp_bom_line',
        'mrp_routing_workcenter', 'mrp_workcenter', 'mrp_production', 'mrp_workorder', 'stock_lot', 'stock_move',
        'purchase_order', 'purchase_order_line', 'res_partner',
    ])),
])

COLORES = {
    'Ventas y CRM': '#DCEBFA', 'Maestros': '#EAF5E4', 'Inventario': '#FFF1D6', 'Producción': '#F6E3F4',
    'Compras': '#FBE5DC', 'Facturación': '#E3F0F0', 'Seguridad y mesa de servicios': '#ECECEC',
}
AREA_DE_ORDEN = list(TABLAS_NUCLEO)
AREA_DE = {t: area for area, tablas in TABLAS_NUCLEO.items() for t in tablas}

# En el ER general, las FK hacia estas tablas de uso general se anotan en cada caja pero no se dibujan: casi todo el
# esquema las tiene y la figura quedaría ilegible. Las autorreferencias tampoco se dibujan.
SIN_LINEA_A = {'res_users', 'stock_location', 'stock_picking_type', 'account_journal'}
# Máximo de columnas FK que se listan por cada par de tablas (el resto se resume en una línea)
MAX_FK_POR_PAR = 2


def tipo_sql(c):
    base = c.tipo
    if c.tipo_sql == 'character varying' and c.longitud:
        base += f'({c.longitud})'
    elif c.tipo_sql == 'numeric' and c.precision:
        base += f'({c.precision},{c.escala or 0})'
    return base


def aristas(esquema, tablas, omitir_a=()):
    """Una arista por par (hija → padre); si hay varias FK entre el mismo par se agrupan en una sola línea.

    Devuelve (dibujadas, no_dibujadas): estas últimas son las FK a ``omitir_a`` y las autorreferencias."""
    grupos = OrderedDict()
    omitidas = OrderedDict()
    for t in tablas:
        for c in esquema[t].columnas:
            if c.fk is None or c.fk[0] not in tablas or c.nombre in COLUMNAS_AUDITORIA:
                continue
            destino = omitidas if (c.fk[0] == t or c.fk[0] in omitir_a) else grupos
            destino.setdefault((t, c.fk[0]), []).append(c)
    return grupos, omitidas


def entidad(esquema, tabla, tablas, solo_claves, omitir_a=(), sangria='', color=''):
    """Caja de la tabla: PK, FK dibujadas (hasta MAX_FK_POR_PAR por destino), columnas clave y una línea que
    resume las FK que no se listan."""
    t = esquema[tabla]
    faltan = [n for n in COLUMNAS_CLAVE.get(tabla, []) if t.columna(n) is None]
    if faltan:
        sys.exit(f'La tabla {tabla} no tiene las columnas {faltan} (revisa COLUMNAS_CLAVE en scripts/diagrama_er.py)')
    pk, fks, claves = [], [], []
    por_destino = {}
    resumen = OrderedDict()
    for c in t.columnas:
        if c.nombre in COLUMNAS_AUDITORIA:
            continue
        if c.es_pk:
            pk.append(c)
        elif c.fk and c.fk[0] in tablas:
            n = por_destino[c.fk[0]] = por_destino.get(c.fk[0], 0) + 1
            if c.fk[0] in omitir_a or c.fk[0] == tabla or n > MAX_FK_POR_PAR:
                resumen[c.fk[0]] = resumen.get(c.fk[0], 0) + 1
            else:
                fks.append(c)
        elif not solo_claves and c.nombre in COLUMNAS_CLAVE.get(tabla, []):
            claves.append(c)
    cabecera = f'{sangria}entity "{tabla}" as {tabla} {color} {{'
    lineas = [cabecera]
    for c in pk:
        lineas.append(f'{sangria}  * {c.nombre} : {tipo_sql(c)} <<PK>>')
    if fks or claves or resumen:
        lineas.append(f'{sangria}  --')
    for c in fks:
        lineas.append(f"{sangria}  {'' if c.admite_nulo else '* '}{c.nombre} : {tipo_sql(c)} <<FK>>")
    if resumen:
        otras = ', '.join(f'{d} ×{n}' if n > 1 else d for d, n in resumen.items())
        lineas.append(f'{sangria}  <i>+ FK a {otras}</i>')
    for c in claves:
        lineas.append(f"{sangria}  {'' if c.admite_nulo else '* '}{c.nombre} : {tipo_sql(c)}")
    lineas.append(f'{sangria}}}')
    return lineas


def relaciones(esquema, tablas, omitir_a=()):
    lineas = []
    for (hija, padre), cols in aristas(esquema, tablas, omitir_a)[0].items():
        opcional = all(c.admite_nulo for c in cols)
        extremo = 'o|' if opcional else '||'
        nombres = [c.nombre for c in cols]
        etiqueta = ', '.join(nombres[:2]) + (f' (+{len(nombres) - 2})' if len(nombres) > 2 else '')
        lineas.append(f'{hija} }}o--{extremo} {padre} : {etiqueta}')
    return lineas


CABECERA = """@startuml {nombre}
' Generado por scripts/diagrama_er.py desde la BD real; no se edita a mano (ver docs/diagramas/README.md).
title {titulo}
hide circle
hide empty methods
left to right direction
skinparam shadowing false
skinparam defaultFontName DejaVu Sans
skinparam defaultFontSize 12
skinparam roundCorner 6
skinparam ArrowColor #555555
skinparam entity {{
  BorderColor #444444
  BackgroundColor #FFFFFF
}}
skinparam package {{
  BorderColor #888888
  FontStyle bold
}}
skinparam nodesep 30
skinparam ranksep 90
"""


def puml_er_general(esquema):
    tablas = list(NUCLEO)
    lineas = [CABECERA.format(nombre='er_nucleo', titulo='Modelo ER del núcleo (36 tablas centrales de la Fase 1)')]
    for t in tablas:
        lineas += entidad(esquema, t, tablas, solo_claves=True, omitir_a=SIN_LINEA_A, color=COLORES[AREA_DE[t]])
    lineas += relaciones(esquema, tablas, SIN_LINEA_A)
    lineas.append('legend bottom')
    lineas.append('  * = no admite nulo · <<PK>> clave primaria · <<FK>> clave foránea · color = área del negocio')
    lineas.append('  Pata de gallo: ||  uno exacto · o|  cero o uno · }o  cero o muchos')
    lineas.append('  Las FK a res_users, stock_location, stock_picking_type y account_journal y las autorreferencias se anotan')
    lineas.append('  en la caja («+ FK a …») sin línea. Áreas: ' + ', '.join(AREA_DE_ORDEN))
    lineas.append('endlegend')
    lineas.append('@enduml')
    return lineas


def puml_logico(esquema, nombre, titulo, tablas):
    lineas = [CABECERA.format(nombre=nombre, titulo=f'Diseño lógico: {titulo}')]
    for t in tablas:
        lineas += entidad(esquema, t, tablas, solo_claves=False, color=COLORES.get(AREA_DE.get(t), ''))
    lineas += relaciones(esquema, tablas)
    lineas.append('legend bottom')
    lineas.append('  * = no admite nulo · <<PK>> clave primaria · <<FK>> clave foránea · solo columnas clave')
    lineas.append('  Pata de gallo: ||  uno exacto · o|  cero o uno · }o  cero o muchos')
    lineas.append('endlegend')
    lineas.append('@enduml')
    return lineas


def renderizar(archivos):
    """PlantUML en Docker, como en los casos de uso. PLANTUML_LIMIT_SIZE sube el tope de 4096 px de la imagen."""
    base = ['docker', 'run', '--rm', '-u', f'{os.getuid()}:{os.getgid()}', '-e', 'PLANTUML_LIMIT_SIZE=16384',
            '-v', f'{SALIDA}:/data', 'plantuml/plantuml:latest', '-charset', 'UTF-8']
    for formato in ('-tpng', '-tsvg'):
        r = subprocess.run(base + [formato] + [f'/data/{a.name}' for a in archivos], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f'PlantUML falló ({formato}): {r.stderr.strip() or r.stdout.strip()}')
    print(f'Renderizados {len(archivos)} diagramas en PNG y SVG')


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--bd', default=os.environ.get('ODOO_DB', 'donofrio'), help='BD de donde sale el esquema')
    p.add_argument('--contenedor', default='erp-donofrio-db-1', help='contenedor de PostgreSQL')
    p.add_argument('--sin-render', action='store_true', help='solo escribe los .puml (sin Docker)')
    a = p.parse_args()

    esquema = leer_esquema(Conexion(a.bd, a.contenedor))
    faltan = [t for t in NUCLEO if t not in esquema]
    if faltan:
        sys.exit(f'Faltan tablas del núcleo en la BD «{a.bd}»: {", ".join(faltan)}')
    SALIDA.mkdir(parents=True, exist_ok=True)
    archivos = []
    contenidos = [('er_nucleo', puml_er_general(esquema))]
    for nombre, (titulo, tablas) in FIGURAS_LOGICAS.items():
        contenidos.append((nombre, puml_logico(esquema, nombre, titulo, tablas)))
    for nombre, lineas in contenidos:
        ruta = SALIDA / f'{nombre}.puml'
        ruta.write_text('\n'.join(lineas) + '\n', encoding='utf-8')
        archivos.append(ruta)
        print(f'Escrito {ruta.relative_to(RAIZ)}')
    if not a.sin_render:
        renderizar(archivos)


if __name__ == '__main__':
    main()
