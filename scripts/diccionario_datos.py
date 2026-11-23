#!/usr/bin/env python3
"""Informe 4.2.8: diccionario de datos generado desde la BD real (``information_schema`` + ``ir_model_fields``).

Lee el esquema de una BD de Odoo que corre en el contenedor ``db`` (solo lecturas: la sesión de psql se abre en
modo ``default_transaction_read_only``) y escribe:

* el diccionario del núcleo, en formato «Tabla 5» de la plantilla (clave, campo, tipo, tamaño, nulo, descripción)
  por cada una de las ~34 tablas centrales (``TABLAS_NUCLEO``): ``docs/informe/04_02_diccionario_datos.md``;
* el anexo con el resto del esquema, agrupado por el módulo de Odoo que define cada tabla:
  ``docs/informe/anexo_diccionario_datos.md``;
* opcionalmente (``--csv``) todo el diccionario en CSV, que Excel abre sin instalar nada.

No necesita librerías: solo Python 3 y Docker. Las descripciones salen de ``ir_model_fields`` (etiqueta y ayuda
en es_PE, con respaldo en en_US); las tablas y columnas, de ``information_schema``.

Uso (desde la raíz del repo, con ``.env`` y el contenedor ``db`` arriba):

    python3 scripts/diccionario_datos.py --bd donofrio_base_limpia --bd-tamanos donofrio_perf

``--bd`` es la BD de donde sale el esquema. Para que el diccionario refleje exactamente ``develop``, conviene una
BD recién instalada con ``donofrio_base`` (la de desarrollo puede estar desactualizada). ``--bd-tamanos`` es
opcional: una BD con datos (por ejemplo ``donofrio_perf``) para contar las filas de las tablas centrales.
"""
import argparse
import csv
import io
import os
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Tablas centrales del núcleo de la Fase 1 por área. Son las mismas del modelo ER (4.2.6), del diseño lógico
# (4.2.7) y de la parte del diccionario que va en el cuerpo del informe (4.2.8).
TABLAS_NUCLEO = OrderedDict([
    ('Ventas y CRM', [
        'sale_order', 'sale_order_line', 'crm_lead', 'pos_order',
    ]),
    ('Maestros', [
        'res_partner', 'product_template', 'product_product', 'product_category',
        'product_pricelist', 'product_pricelist_item', 'product_supplierinfo', 'hr_employee',
    ]),
    ('Inventario', [
        'stock_warehouse', 'stock_location', 'stock_picking_type', 'stock_picking', 'stock_move',
        'stock_move_line', 'stock_lot', 'stock_quant', 'stock_warehouse_orderpoint',
    ]),
    ('Producción', [
        'mrp_bom', 'mrp_bom_line', 'mrp_production', 'mrp_workorder', 'mrp_workcenter',
        'mrp_routing_workcenter',
    ]),
    ('Compras', [
        'purchase_order', 'purchase_order_line',
    ]),
    ('Facturación', [
        'account_move', 'account_move_line', 'account_journal',
    ]),
    ('Seguridad y mesa de servicios', [
        'res_users', 'res_groups', 'auditlog_rule', 'project_task',
    ]),
])
NUCLEO = [t for tablas in TABLAS_NUCLEO.values() for t in tablas]

# Columnas de auditoría que Odoo agrega a casi todos los modelos
COLUMNAS_AUDITORIA = ('create_uid', 'create_date', 'write_uid', 'write_date')

TAMANOS_FIJOS = {
    'smallint': '2 B', 'integer': '4 B', 'bigint': '8 B', 'real': '4 B', 'double precision': '8 B',
    'boolean': '1 B', 'date': '4 B', 'time without time zone': '8 B', 'timestamp without time zone': '8 B',
    'timestamp with time zone': '8 B',
}
TIPOS_CORTOS = {
    'character varying': 'varchar', 'timestamp without time zone': 'timestamp',
    'timestamp with time zone': 'timestamptz', 'time without time zone': 'time',
}


# --------------------------------------------------------------------------------------------------- acceso a la BD
def leer_env(ruta=RAIZ / '.env'):
    valores = {}
    if ruta.exists():
        for linea in ruta.read_text(encoding='utf-8').splitlines():
            linea = linea.strip()
            if linea and not linea.startswith('#') and '=' in linea:
                clave, valor = linea.split('=', 1)
                valores[clave.strip()] = valor.strip().strip('"').strip("'")
    return valores


class Conexion:
    """psql dentro del contenedor ``db``, siempre en modo solo lectura."""

    def __init__(self, bd, contenedor='erp-donofrio-db-1'):
        env = leer_env()
        self.bd = bd
        self.contenedor = contenedor
        self.usuario = os.environ.get('ODOO_DB_USER') or env.get('ODOO_DB_USER', 'odoo')
        self.clave = os.environ.get('ODOO_DB_PASSWORD') or env.get('ODOO_DB_PASSWORD', '')

    def consultar(self, sql):
        """Devuelve la consulta como lista de diccionarios (todo texto; vacío = NULL)."""
        orden = [
            'docker', 'exec', '-i', '-e', f'PGPASSWORD={self.clave}', '-e', 'PGOPTIONS=-c default_transaction_read_only=on',
            self.contenedor, 'psql', '-h', 'localhost', '-U', self.usuario, '-d', self.bd,
            '--csv', '-X', '-v', 'ON_ERROR_STOP=1', '-f', '-',
        ]
        r = subprocess.run(orden, input=sql, capture_output=True, text=True, encoding='utf-8')
        if r.returncode != 0:
            sys.exit(f'psql falló en la BD «{self.bd}»: {r.stderr.strip()}')
        return list(csv.DictReader(io.StringIO(r.stdout)))


# ------------------------------------------------------------------------------------------------- lectura del esquema
SQL_COLUMNAS = """
SELECT c.table_name AS tabla, c.column_name AS columna, c.ordinal_position AS orden, c.data_type AS tipo,
       c.character_maximum_length AS longitud, c.numeric_precision AS precision, c.numeric_scale AS escala,
       c.is_nullable AS nulo, c.udt_name AS udt
  FROM information_schema.columns c
  JOIN information_schema.tables t ON t.table_schema = c.table_schema AND t.table_name = c.table_name
 WHERE c.table_schema = 'public' AND t.table_type = 'BASE TABLE'
 ORDER BY c.table_name, c.ordinal_position;
"""

# Claves primarias y foráneas. Se leen de pg_constraint y no de information_schema.table_constraints porque esas vistas
# (en especial constraint_column_usage) tardan más de un minuto con las ~700 tablas de Odoo; el resultado es el mismo.
SQL_RESTRICCIONES = """
SELECT cl.relname AS tabla, a.attname AS columna,
       CASE co.contype WHEN 'p' THEN 'PRIMARY KEY' ELSE 'FOREIGN KEY' END AS tipo,
       rcl.relname AS ref_tabla, ra.attname AS ref_columna,
       CASE co.confdeltype WHEN 'c' THEN 'CASCADE' WHEN 'n' THEN 'SET NULL' WHEN 'r' THEN 'RESTRICT'
            WHEN 'd' THEN 'SET DEFAULT' ELSE 'NO ACTION' END AS al_borrar
  FROM pg_constraint co
  JOIN pg_class cl ON cl.oid = co.conrelid
  JOIN pg_namespace n ON n.oid = cl.relnamespace AND n.nspname = 'public'
  JOIN LATERAL unnest(co.conkey) WITH ORDINALITY AS k(attnum, pos) ON true
  JOIN pg_attribute a ON a.attrelid = co.conrelid AND a.attnum = k.attnum
  LEFT JOIN pg_class rcl ON rcl.oid = co.confrelid
  LEFT JOIN LATERAL (SELECT (co.confkey)[k.pos] AS attnum) rk ON co.contype = 'f'
  LEFT JOIN pg_attribute ra ON ra.attrelid = co.confrelid AND ra.attnum = rk.attnum
 WHERE co.contype IN ('p', 'f')
 ORDER BY cl.relname, a.attname, co.contype;
"""

# Etiqueta y ayuda de cada campo (es_PE con respaldo en en_US) y si lo agregó donofrio_base
SQL_CAMPOS = """
SELECT f.model AS modelo, f.name AS campo,
       COALESCE(NULLIF(f.field_description->>'es_PE', ''), f.field_description->>'en_US') AS etiqueta,
       COALESCE(NULLIF(f.help->>'es_PE', ''), f.help->>'en_US', '') AS ayuda,
       f.ttype AS ttype, f.store AS almacenado, COALESCE(f.relation_table, '') AS tabla_m2m,
       COALESCE(f.relation, '') AS relacion,
       EXISTS (SELECT 1 FROM ir_model_data d WHERE d.model = 'ir.model.fields' AND d.res_id = f.id
                  AND d.module = 'donofrio_base') AS de_donofrio
  FROM ir_model_fields f
 ORDER BY f.model, f.name;
"""

# Modelo de cada tabla y módulo que lo define (el primero que lo registró)
SQL_MODELOS = """
SELECT m.model AS modelo, COALESCE(NULLIF(m.name->>'es_PE', ''), m.name->>'en_US') AS nombre,
       COALESCE((SELECT d.module FROM ir_model_data d
                  WHERE d.model = 'ir.model' AND d.res_id = m.id ORDER BY d.id LIMIT 1), '') AS modulo
  FROM ir_model m
 ORDER BY m.model;
"""


class Columna:
    def __init__(self, fila):
        self.nombre = fila['columna']
        self.orden = int(fila['orden'])
        self.tipo_sql = fila['tipo']
        self.udt = fila['udt']
        self.longitud = fila['longitud']
        self.precision = fila['precision']
        self.escala = fila['escala']
        self.admite_nulo = fila['nulo'] == 'YES'
        self.es_pk = False
        self.fk = None            # (tabla, columna)
        self.al_borrar = ''
        self.etiqueta = ''
        self.ayuda = ''
        self.de_donofrio = False

    @property
    def tipo(self):
        if self.tipo_sql == 'ARRAY':
            return self.udt.lstrip('_') + '[]'
        return TIPOS_CORTOS.get(self.tipo_sql, self.tipo_sql)

    @property
    def tamano(self):
        if self.tipo_sql == 'character varying':
            return self.longitud or 'variable'
        if self.tipo_sql == 'numeric':
            if self.precision:
                return f'{self.precision},{self.escala or 0}'
            return 'variable'
        if self.tipo_sql in TAMANOS_FIJOS:
            return TAMANOS_FIJOS[self.tipo_sql]
        return 'variable'

    @property
    def clave(self):
        return ', '.join(p for p, activo in (('PK', self.es_pk), ('FK', self.fk is not None)) if activo)


class Tabla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.columnas = []
        self.modelo = ''
        self.nombre_modelo = ''
        self.modulo = ''
        self.m2m_de = ''          # descripción si es la tabla intermedia de un many2many

    def columna(self, nombre):
        return next((c for c in self.columnas if c.nombre == nombre), None)

    @property
    def titulo(self):
        return self.nombre_modelo or self.m2m_de or 'Sin modelo de Odoo'


def leer_esquema(con):
    """Devuelve ``{tabla: Tabla}`` con columnas, claves y descripciones de la BD."""
    tablas = {}
    for f in con.consultar(SQL_COLUMNAS):
        tablas.setdefault(f['tabla'], Tabla(f['tabla'])).columnas.append(Columna(f))
    for f in con.consultar(SQL_RESTRICCIONES):
        col = tablas[f['tabla']].columna(f['columna'])
        if f['tipo'] == 'PRIMARY KEY':
            col.es_pk = True
        else:
            col.fk = (f['ref_tabla'], f['ref_columna'])
            col.al_borrar = f['al_borrar']
    modelos = {m['modelo']: m for m in con.consultar(SQL_MODELOS)}
    for modelo, m in modelos.items():
        t = tablas.get(modelo.replace('.', '_'))
        if t is not None and not t.modelo:
            t.modelo, t.nombre_modelo, t.modulo = modelo, m['nombre'], m['modulo']
    for f in con.consultar(SQL_CAMPOS):
        t = tablas.get(f['modelo'].replace('.', '_'))
        if t is not None and t.modelo == f['modelo']:
            col = t.columna(f['campo'])
            if col is not None:
                col.etiqueta, col.ayuda = f['etiqueta'], f['ayuda']
                col.de_donofrio = f['de_donofrio'] == 't' and f['campo'] not in ('id', 'display_name')
        if f['ttype'] == 'many2many' and f['tabla_m2m'] in tablas and not tablas[f['tabla_m2m']].m2m_de:
            tablas[f['tabla_m2m']].m2m_de = f"Relación muchos a muchos entre «{f['modelo']}» y «{f['relacion']}»"
    # Módulo de las tablas intermedias: el del modelo que declara el campo
    for t in tablas.values():
        if not t.modulo and t.m2m_de:
            origen = t.m2m_de.split('«')[1].split('»')[0]
            t.modulo = modelos.get(origen, {}).get('modulo', '')
    return tablas


# ------------------------------------------------------------------------------------------------------- Markdown
def texto(valor):
    """Una sola línea y sin barras verticales (rompen las tablas Markdown)."""
    return ' '.join((valor or '').replace('|', '/').split())


def descripcion(tabla, col):
    """Etiqueta del campo, destino si es FK y, tras un guion, su ayuda (recortada)."""
    texto_final = col.etiqueta or (f'Referencia a {col.fk[0]}' if col.fk else '')
    if col.fk and col.etiqueta:
        texto_final += f' → `{col.fk[0]}`'
    if col.ayuda:
        ayuda = texto(col.ayuda)
        texto_final += ' — ' + (ayuda if len(ayuda) <= 140 else ayuda[:137].rstrip() + '…')
    if col.de_donofrio:
        texto_final = f'**[donofrio_base]** {texto_final}'
    return texto(texto_final) or '—'


def tabla_markdown(tabla, numero=None):
    lineas = []
    prefijo = f'Tabla 4.2.8-{numero}. ' if numero else ''
    cabecera = f'### {prefijo}`{tabla.nombre}`'
    lineas += [cabecera, '']
    modelo = f'modelo `{tabla.modelo}`' if tabla.modelo else 'tabla intermedia, sin modelo propio'
    datos = [f'**{texto(tabla.titulo)}**', modelo]
    if tabla.modulo:
        datos.append(f'módulo `{tabla.modulo}`')
    datos.append(f'{len(tabla.columnas)} columnas')
    lineas += [' · '.join(datos), '']
    lineas += ['| Clave | Campo | Tipo | Tamaño | Nulo | Descripción |', '|---|---|---|---|---|---|']
    for c in tabla.columnas:
        lineas.append(f"| {c.clave or ''} | `{c.nombre}` | {c.tipo} | {c.tamano} | {'Sí' if c.admite_nulo else 'No'} "
                      f'| {descripcion(tabla, c)} |')
    lineas.append('')
    return lineas


def escribir(ruta, lineas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text('\n'.join(lineas).rstrip('\n') + '\n', encoding='utf-8')
    print(f'Escrito {ruta.relative_to(RAIZ) if ruta.is_relative_to(RAIZ) else ruta}')


def contar_filas(con, tablas):
    """Filas de cada tabla (conteo exacto). Las que no existen en esa BD quedan fuera (la BD de carga puede ser
    anterior a algún módulo)."""
    existentes = {f['t'] for f in con.consultar(
        "SELECT table_name AS t FROM information_schema.tables WHERE table_schema = 'public';")}
    tablas = [t for t in tablas if t in existentes]
    sql = ' UNION ALL '.join(f"SELECT '{t}' AS tabla, count(*) AS filas FROM \"{t}\"" for t in tablas)
    return {f['tabla']: int(f['filas']) for f in con.consultar(sql + ';')}


def informe_nucleo(esquema, origen, filas=None, bd_filas=''):
    faltan = [t for t in NUCLEO if t not in esquema]
    if faltan:
        sys.exit(f'Faltan tablas del núcleo en la BD: {", ".join(faltan)}')
    lineas = [
        '# 4.2.8 Diccionario de datos del núcleo (tablas centrales)', '',
        f'> **Archivo generado** por [`scripts/diccionario_datos.py`](../../scripts/diccionario_datos.py); no se edita a mano. '
        f'Origen: {origen}.',
        '>',
        '> Formato de la «Tabla 5» de la plantilla: una tabla por entidad con su clave (PK/FK), campo, tipo, tamaño, '
        'si admite nulo y descripción. **Tipo y tamaño** salen de `information_schema`; la **descripción**, de la '
        'etiqueta y la ayuda del campo en `ir_model_fields` (es_PE). Tamaño: caracteres en `varchar`, `precisión,escala` '
        'en `numeric`, bytes en los tipos fijos y «variable» en `text` y `jsonb`. Las columnas que agregó '
        '`donofrio_base` van marcadas con **[donofrio_base]**.', '',
    ]
    lineas += ['## Resumen de las tablas centrales', '']
    cab = '| Área | Tabla | Modelo de Odoo | Módulo | Columnas |'
    sep = '|---|---|---|---|---|'
    if filas:
        cab += f' Filas (`{bd_filas}`) |'
        sep += '---|'
    lineas += [cab, sep]
    numero = {}
    for area, nombres in TABLAS_NUCLEO.items():
        for n in nombres:
            numero[n] = len(numero) + 1
            t = esquema[n]
            fila = f'| {area} | `{n}` | `{t.modelo}` | `{t.modulo}` | {len(t.columnas)} |'
            if filas:
                fila += (f' {filas[n]:,} |'.replace(',', '.') if n in filas else ' n/d |')
            lineas.append(fila)
    lineas.append('')
    agregadas = [(t.nombre, c.nombre) for t in esquema.values() for c in t.columnas if c.de_donofrio]
    lineas += ['## Lo que agrega `donofrio_base` al esquema', '']
    lineas.append('`donofrio_base` **no crea tablas propias** en la Fase 1: sus registros (compañía, almacenes, productos, '
                  'clientes, listas de precios, listas de materiales, empleados, usuarios, grupos y reglas) se cargan '
                  'por XML/CSV en las tablas de Odoo de arriba. En el esquema solo agrega:')
    lineas.append('')
    for tabla, campo in agregadas:
        c = esquema[tabla].columna(campo)
        lineas.append(f'* `{tabla}.{campo}` ({c.tipo}, calculada y almacenada): {texto(c.etiqueta)}.')
    if not agregadas:
        lineas.append('* (ninguna columna en esta BD)')
    lineas.append('')
    for area, nombres in TABLAS_NUCLEO.items():
        lineas += [f'## {area}', '']
        for n in nombres:
            lineas += tabla_markdown(esquema[n], numero[n])
    return lineas


def informe_anexo(esquema, origen):
    resto = sorted((t for n, t in esquema.items() if n not in NUCLEO), key=lambda t: (t.modulo or '~', t.nombre))
    lineas = [
        '# Anexo: diccionario de datos del resto del esquema', '',
        f'> **Archivo generado** por [`scripts/diccionario_datos.py`](../../scripts/diccionario_datos.py); no se edita a mano. '
        f'Origen: {origen}.',
        '>',
        f'> Complementa el [diccionario del núcleo](04_02_diccionario_datos.md) (4.2.8) con las otras {len(resto)} tablas '
        f'del esquema, agrupadas por el módulo de Odoo que define cada modelo. El esquema completo tiene {len(esquema)} tablas '
        f'({len(NUCLEO)} en el núcleo). Mismo formato y mismas fuentes que el diccionario del núcleo.', '',
        '## Índice por módulo', '', '| Módulo | Tablas |', '|---|---|',
    ]
    por_modulo = OrderedDict()
    for t in resto:
        por_modulo.setdefault(t.modulo or 'sin módulo', []).append(t)
    for modulo, ts in por_modulo.items():
        lineas.append(f'| `{modulo}` | {len(ts)} |')
    lineas.append('')
    for modulo, ts in por_modulo.items():
        lineas += [f'## Módulo `{modulo}`', '']
        for t in ts:
            lineas += tabla_markdown(t)
    return lineas


def escribir_csv(ruta, esquema):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['ámbito', 'módulo', 'tabla', 'modelo', 'clave', 'campo', 'tipo', 'tamaño', 'nulo', 'descripción'])
        for n in sorted(esquema):
            t = esquema[n]
            for c in t.columnas:
                w.writerow(['núcleo' if n in NUCLEO else 'anexo', t.modulo, n, t.modelo, c.clave, c.nombre, c.tipo,
                            c.tamano, 'Sí' if c.admite_nulo else 'No', descripcion(t, c).replace('**', '')])
    print(f'Escrito {ruta}')


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--bd', default=os.environ.get('ODOO_DB', 'donofrio'), help='BD de donde sale el esquema')
    p.add_argument('--bd-tamanos', default='', help='BD con datos para contar las filas de las tablas centrales')
    p.add_argument('--contenedor', default='erp-donofrio-db-1', help='contenedor de PostgreSQL')
    p.add_argument('--origen', default='BD limpia con `donofrio_base` instalado desde `develop` (Odoo 19.0, PostgreSQL 16)',
                   help='texto que describe el origen, para la cabecera de los archivos')
    p.add_argument('--salida-nucleo', type=Path, default=RAIZ / 'docs/informe/04_02_diccionario_datos.md')
    p.add_argument('--salida-anexo', type=Path, default=RAIZ / 'docs/informe/anexo_diccionario_datos.md')
    p.add_argument('--csv', type=Path, default=None, help='escribe además todo el diccionario en CSV')
    a = p.parse_args()

    esquema = leer_esquema(Conexion(a.bd, a.contenedor))
    filas = contar_filas(Conexion(a.bd_tamanos, a.contenedor), NUCLEO) if a.bd_tamanos else None
    escribir(a.salida_nucleo, informe_nucleo(esquema, a.origen, filas, a.bd_tamanos))
    escribir(a.salida_anexo, informe_anexo(esquema, a.origen))
    if a.csv:
        escribir_csv(a.csv, esquema)
    print(f'{len(esquema)} tablas en el esquema, {len(NUCLEO)} en el núcleo.')


if __name__ == '__main__':
    main()
