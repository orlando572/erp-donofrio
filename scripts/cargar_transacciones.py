"""HU-16: 3-4 meses de transacciones de demostración, generadas con semilla fija.

Uso (con la BD ya inicializada con donofrio_base). Detén antes el servicio web: sus tareas programadas (cron)
corren sobre la misma BD y pueden chocar con el script («could not serialize access due to concurrent update»):

    docker compose stop odoo
    docker compose run --rm -T odoo odoo shell -d donofrio --no-http < scripts/cargar_transacciones.py
    docker compose up -d odoo

El script define dos partes independientes, que se ejecutan en este orden:

* Orlando (inventario y producción): inventario inicial con lotes por vencer, recepciones semanales de
  insumos con lote, órdenes de producción (con lote, vencimiento y costo) y reposición semanal
  Lima → Arequipa. Es lo que está implementado abajo (``cargar_inventario_y_produccion``).
* Evelyn (ventas, PdV y compras): ``cargar_ventas``, ``cargar_pdv`` y ``cargar_compras``, que hoy no hacen nada.
  Se agregan en este mismo archivo y se llaman desde ``main``.

Reglas para que el resultado sea siempre el mismo:

* Semilla fija (``SEMILLA``) y fechas fijas: del lunes 3/8/2026 al domingo 22/11/2026 (16 semanas).
* Idempotente: si ya hay datos de demostración (movimientos con origen ``DEMO-``) no vuelve a cargar.
  Para repetir, se recrea la BD (``scripts/init_db.sh``) y se corre otra vez.
* Estacionalidad (01 §1.1): los helados suben de agosto a noviembre porque se anticipa el verano; el panetón
  casi no se produce en agosto y despega en octubre y noviembre (campaña de Navidad); el chocolate es parejo.

Las fechas de los movimientos son históricas, pero los lotes se crean con vencimientos futuros mientras se
producen (Odoo valida el vencimiento contra la fecha real). Al final se corrigen los vencimientos de los lotes
para que sean coherentes con su fecha de producción o de ingreso.
"""
import math
import random
from datetime import date, datetime, time, timedelta

from odoo import Command

SEMILLA = 2026
FIN = date(2026, 11, 22)
SEMANAS = 16
INICIO = FIN - timedelta(weeks=SEMANAS) + timedelta(days=1)  # lunes 3/8/2026
PREFIJO = 'DEMO-'

# Producción semanal de referencia (tandas de la receta) y línea de cada terminado con BoM
# Cada receta es una tanda industrial (10 000 paletas, 20 000 chocolates, 5 000 panetones...)
PRODUCCION = {
    'PT-H01': ('helados', 2), 'PT-H03': ('helados', 2), 'PT-H05': ('helados', 2), 'PT-H07': ('helados', 2),
    'PT-H10': ('helados', 1), 'PT-H11': ('helados', 1), 'PT-H12': ('helados', 1),
    'PT-C01': ('chocolates', 2), 'PT-C02': ('chocolates', 2), 'PT-C03': ('chocolates', 2),
    'PT-P01': ('paneton', 2), 'PT-P02': ('paneton', 1),
}

# Factor estacional por línea: (fecha, factor); entre dos puntos se interpola linealmente
ESTACIONALIDAD = {
    'helados': [(date(2026, 8, 1), 0.45), (date(2026, 9, 1), 0.55), (date(2026, 10, 1), 0.85),
                (date(2026, 11, 1), 1.30), (date(2026, 11, 22), 1.60)],
    'paneton': [(date(2026, 8, 1), 0.10), (date(2026, 9, 1), 0.50), (date(2026, 10, 1), 1.30),
                (date(2026, 11, 1), 2.00), (date(2026, 11, 22), 2.20)],
    'chocolates': [(date(2026, 8, 1), 1.00), (date(2026, 10, 1), 1.00), (date(2026, 10, 20), 1.25),
                   (date(2026, 11, 22), 1.15)],
}
DIAS_DE_PRODUCCION = (1, 3)   # martes y jueves
DIA_DE_RECEPCION = 0          # lunes
DIA_DE_REPOSICION = 4         # viernes: sale a Arequipa lo producido en la semana
PARTE_PARA_AREQUIPA = 0.30


def factor_estacional(linea, dia):
    puntos = ESTACIONALIDAD[linea]
    if dia <= puntos[0][0]:
        return puntos[0][1]
    for (d0, f0), (d1, f1) in zip(puntos, puntos[1:]):
        if dia <= d1:
            return f0 + (f1 - f0) * (dia - d0).days / (d1 - d0).days
    return puntos[-1][1]


def momento(dia, hora=10):
    return datetime.combine(dia, time(hora, 0))


def ya_hay_datos_de_demostracion(env):
    return bool(env['stock.picking'].search_count([('origin', '=like', f'{PREFIJO}%')], limit=1))


# --- Utilidades de Odoo -------------------------------------------------------------------------------

class Contexto:
    """Referencias que se usan en todo el script y registro de lotes para corregir sus fechas al final."""

    def __init__(self, env):
        self.env = env
        self.rng = random.Random(SEMILLA)
        self.lim = env.ref('stock.warehouse0')
        self.aqp = env.ref('donofrio_base.wh_aqp')
        self.proveedores = env.ref('stock.stock_location_suppliers')
        self.lotes = {}       # id del lote -> fecha de producción o ingreso
        self.producido = {}   # id del producto -> unidades producidas
        self.cantidad_de_ops = 0

    def producto(self, codigo):
        return self.env['product.product'].search([('default_code', '=', codigo)], limit=1)

    def registrar_lote(self, lote, dia):
        self.lotes[lote.id] = dia


def fechar_movimientos(movimientos, cuando):
    """Pone fecha histórica a los movimientos y a su detalle (Odoo los fecha con la hora de la corrida)."""
    movimientos.write({'date': cuando})
    movimientos.move_line_ids.write({'date': cuando})


def fechar_picking(picking, cuando):
    picking.write({'scheduled_date': cuando, 'date_done': cuando})
    fechar_movimientos(picking.move_ids, cuando)


# --- Inventario inicial -------------------------------------------------------------------------------

def inventario_inicial(ctx):
    """Existencias del 3/8: todos los terminados con lote; algunos lotes vencen en menos de 30 días."""
    env, rng = ctx.env, ctx.rng
    terminados = env['product.product'].search([
        ('categ_id', 'child_of', env.ref('donofrio_base.cat_terminados').id)], order='default_code')
    Lote = env['stock.lot']
    quants = []
    for producto in terminados:
        codigo = producto.default_code.replace('PT-', '')
        por_vencer = rng.random() < 0.4
        lotes = [('B', rng.randint(90, 300), rng.randint(2000, 6000))]
        if por_vencer:
            lotes.append(('A', rng.randint(6, 27), rng.randint(300, 900)))
        for sufijo, dias, cantidad in lotes:
            lote = Lote.create({
                'name': f'INI-{codigo}-{sufijo}',
                'product_id': producto.id,
                'expiration_date': momento(FIN + timedelta(days=dias), 12),
            })
            quants.append({
                'product_id': producto.id,
                'location_id': ctx.lim.lot_stock_id.id,
                'lot_id': lote.id,
                'inventory_quantity': cantidad,
            })
    Quant = env['stock.quant'].with_context(inventory_mode=True, force_period_date=INICIO)
    Quant.create(quants).action_apply_inventory()
    movimientos = env['stock.move'].search([
        ('is_inventory', '=', True), ('move_line_ids.lot_id.name', '=like', 'INI-%')])
    fechar_movimientos(movimientos, momento(INICIO, 8))
    env.cr.execute("UPDATE stock_quant SET in_date = %s WHERE lot_id IN (SELECT id FROM stock_lot WHERE name LIKE 'INI-%%')",
                   (momento(INICIO, 8),))
    print(f'  Inventario inicial: {len(quants)} lotes de {len(terminados)} terminados.')


# --- Plan de producción -------------------------------------------------------------------------------

def planificar_semana(ctx, lunes):
    """Devuelve las OP de la semana: lista de (producto, bom, tandas, día)."""
    rng = ctx.rng
    plan = []
    for codigo, (linea, base) in PRODUCCION.items():
        factor = factor_estacional(linea, lunes + timedelta(days=2))
        tandas = round(base * factor * rng.uniform(0.8, 1.2))
        if tandas <= 0:
            continue
        producto = ctx.producto(codigo)
        bom = ctx.env['mrp.bom']._bom_find(producto)[producto]
        if tandas >= 4:
            primera = math.ceil(tandas / 2)
            partes = [(primera, DIAS_DE_PRODUCCION[0]), (tandas - primera, DIAS_DE_PRODUCCION[1])]
        else:
            partes = [(tandas, DIAS_DE_PRODUCCION[0])]
        for cantidad, dia_semana in partes:
            plan.append((producto, bom, cantidad, lunes + timedelta(days=dia_semana)))
    return plan


def necesidades_de_insumos(plan):
    necesidades = {}
    for producto, bom, tandas, _dia in plan:
        for linea in bom.bom_line_ids:
            cantidad = linea.product_uom_id._compute_quantity(linea.product_qty * tandas, linea.product_id.uom_id)
            necesidades[linea.product_id] = necesidades.get(linea.product_id, 0) + cantidad
    return necesidades


# --- Recepción de insumos -----------------------------------------------------------------------------

def recibir_insumos(ctx, dia, necesidades):
    """Recibe en Lima lo que se va a consumir en la semana, con un lote por insumo y precio con variación."""
    if not necesidades:
        return
    env, rng = ctx.env, ctx.rng
    tipo = ctx.lim.in_type_id
    picking = env['stock.picking'].with_context(force_period_date=dia).create({
        'picking_type_id': tipo.id,
        'location_id': ctx.proveedores.id,
        'location_dest_id': tipo.default_location_dest_id.id,
        'origin': f'{PREFIJO}REC-{dia:%Y%m%d}',
        'move_ids': [Command.create({
            'product_id': insumo.id,
            'product_uom_qty': cantidad,
            'product_uom': insumo.uom_id.id,
            'location_id': ctx.proveedores.id,
            'location_dest_id': tipo.default_location_dest_id.id,
            'price_unit': round(insumo.standard_price * rng.uniform(0.93, 1.08), 4),
        }) for insumo, cantidad in necesidades.items()],
    })
    picking.action_confirm()
    for movimiento in picking.move_ids:
        linea = movimiento.move_line_ids
        linea.quantity = movimiento.product_uom_qty
        if movimiento.product_id.tracking == 'lot':
            linea.lot_name = f'{movimiento.product_id.default_code}-{dia:%y%m%d}'
    picking.move_ids.picked = True
    picking.with_context(skip_expired=True, skip_backorder=True, skip_sms=True, force_period_date=dia).button_validate()
    fechar_picking(picking, momento(dia, 8))
    for movimiento in picking.move_ids:
        for lote in movimiento.move_line_ids.lot_id:
            ctx.registrar_lote(lote, dia)


# --- Órdenes de producción ----------------------------------------------------------------------------

def producir(ctx, producto, bom, tandas, dia):
    env, rng = ctx.env, ctx.rng
    cantidad = bom.product_qty * tandas
    orden = env['mrp.production'].with_context(force_period_date=dia).create({
        'product_id': producto.id,
        'product_qty': cantidad,
        'bom_id': bom.id,
        'origin': f'{PREFIJO}OP-{dia:%Y%m%d}',
    })
    orden.action_confirm()
    orden.action_assign()
    lote = env['stock.lot'].create({
        'name': f'{producto.default_code.replace("PT-", "")}-{dia:%y%m%d}',
        'product_id': producto.id,
    })
    orden.lot_producing_ids = [Command.set(lote.ids)]
    orden.qty_producing = cantidad
    orden.move_raw_ids.picked = True

    inicio = momento(dia, 7)
    fin = inicio
    for operacion in orden.workorder_ids:
        minutos = operacion.duration_expected * rng.uniform(0.9, 1.15)
        fin_operacion = fin + timedelta(minutes=minutos)
        operacion.write({
            'time_ids': [Command.create({
                'workcenter_id': operacion.workcenter_id.id,
                'loss_id': env.ref('mrp.block_reason7').id,
                'date_start': fin,
                'date_end': fin_operacion,
            })],
            'date_start': fin,
            'date_finished': fin_operacion,
            'state': 'done',
        })
        fin = fin_operacion
    orden.with_context(skip_backorder=True, force_period_date=dia).button_mark_done()

    # Una OP terminada no admite cambios de fecha por el ORM: se corrige directamente en la tabla
    env.cr.execute("UPDATE mrp_production SET date_start = %s, date_finished = %s WHERE id = %s",
                   (inicio, fin, orden.id))
    orden.invalidate_recordset(['date_start', 'date_finished'])
    fechar_movimientos(orden.move_raw_ids | orden.move_finished_ids, fin)
    ctx.registrar_lote(lote, dia)
    ctx.producido[producto.id] = ctx.producido.get(producto.id, 0) + cantidad
    ctx.cantidad_de_ops += 1
    return orden


# --- Reposición Lima → Arequipa -----------------------------------------------------------------------

def reponer_arequipa(ctx, dia, producidos):
    """Pide a Arequipa una parte de lo producido en la semana y la mueve: pick, ship y recepción."""
    env = ctx.env
    Regla = env['stock.rule']
    origen = f'{PREFIJO}AQP-{dia:%Y%m%d}'
    pedidos = []
    for producto, cantidad in producidos.items():
        disponible = env['stock.quant']._get_available_quantity(producto, ctx.lim.lot_stock_id)
        a_enviar = math.floor(min(cantidad * PARTE_PARA_AREQUIPA, disponible))
        if a_enviar > 0:
            pedidos.append(Regla.Procurement(
                producto, a_enviar, producto.uom_id, ctx.aqp.lot_stock_id, f'Reposición AQP {dia:%d/%m}',
                origen, env.company, {'warehouse_id': ctx.aqp, 'route_ids': ctx.aqp.resupply_route_ids}))
    if not pedidos:
        return
    Regla.run(pedidos)
    pickings = env['stock.picking'].search([('origin', '=', origen)], order='id')
    for _ in range(3):
        listos = pickings.filtered(lambda p: p.state == 'assigned')
        if not listos:
            break
        listos.move_ids.picked = True
        listos.with_context(skip_expired=True, skip_backorder=True, skip_sms=True, force_period_date=dia).button_validate()
        esperando = pickings.filtered(lambda p: p.state in ('confirmed', 'waiting'))
        if esperando:
            esperando.action_assign()
    for picking in pickings:
        fechar_picking(picking, momento(dia, 15))


# --- Corrección final de lotes ------------------------------------------------------------------------

def corregir_fechas_de_lotes(ctx):
    """Vencimiento, retiro y alerta de cada lote según su fecha real de producción o ingreso."""
    env = ctx.env
    cr = env.cr
    for lote in env['stock.lot'].browse(list(ctx.lotes)):
        producto = lote.product_id
        dia = ctx.lotes[lote.id]
        vence = momento(dia + timedelta(days=producto.expiration_time), 12)
        cr.execute("""
            UPDATE stock_lot SET expiration_date = %(vence)s,
                   use_date = %(vence)s - make_interval(days => %(vence_uso)s),
                   removal_date = %(vence)s - make_interval(days => %(retiro)s),
                   alert_date = %(vence)s - make_interval(days => %(alerta)s),
                   product_expiry_reminded = FALSE
             WHERE id = %(id)s""", {
            'vence': vence, 'id': lote.id,
            'vence_uso': producto.expiration_time - producto.use_time,
            'retiro': producto.removal_time, 'alerta': producto.alert_time,
        })
        cr.execute("UPDATE stock_quant SET in_date = %s WHERE lot_id = %s", (momento(dia, 8), lote.id))
    cr.execute("""
        UPDATE stock_quant q SET expiration_date = l.expiration_date, removal_date = l.removal_date
          FROM stock_lot l WHERE q.lot_id = l.id AND l.id = ANY(%s)""", (list(ctx.lotes),))
    cr.execute("""
        UPDATE stock_move_line ml SET expiration_date = l.expiration_date, removal_date = l.removal_date
          FROM stock_lot l WHERE ml.lot_id = l.id AND l.id = ANY(%s)""", (list(ctx.lotes),))
    env.invalidate_all()


# --- Partes del script ---------------------------------------------------------------------------------

def cargar_inventario_y_produccion(env):
    ctx = Contexto(env)
    print(f'Inventario y producción: {INICIO:%d/%m/%Y} → {FIN:%d/%m/%Y} ({SEMANAS} semanas, semilla {SEMILLA})')
    inventario_inicial(ctx)
    env.cr.commit()
    for semana in range(SEMANAS):
        lunes = INICIO + timedelta(weeks=semana)
        plan = planificar_semana(ctx, lunes)
        recibir_insumos(ctx, lunes + timedelta(days=DIA_DE_RECEPCION), necesidades_de_insumos(plan))
        producidos = {}
        for producto, bom, tandas, dia in sorted(plan, key=lambda p: p[3]):
            orden = producir(ctx, producto, bom, tandas, dia)
            producidos[producto] = producidos.get(producto, 0) + orden.product_qty
        reponer_arequipa(ctx, lunes + timedelta(days=DIA_DE_REPOSICION), producidos)
        env.cr.commit()
        print(f'  Semana {semana + 1:>2} ({lunes:%d/%m}): {len(plan)} OP')
    corregir_fechas_de_lotes(ctx)
    env.cr.commit()
    resumen_de_stock(env, ctx)


def resumen_de_stock(env, ctx):
    print(f'Listo: {ctx.cantidad_de_ops} órdenes de producción.')
    print('Existencias de terminados al cierre (Lima + Arequipa), para dimensionar las ventas:')
    terminados = env['product.product'].search([
        ('categ_id', 'child_of', env.ref('donofrio_base.cat_terminados').id)], order='default_code')
    for producto in terminados:
        lima = env['stock.quant']._get_available_quantity(producto, ctx.lim.lot_stock_id)
        arequipa = env['stock.quant']._get_available_quantity(producto, ctx.aqp.lot_stock_id)
        print(f'  {producto.default_code:<8} {producto.name[:34]:<34} Lima {lima:>7.0f}  Arequipa {arequipa:>6.0f}')


def cargar_ventas(env):
    """Evelyn: pedidos de venta de los canales, con entregas y facturas (pendiente)."""


def cargar_pdv(env):
    """Evelyn: sesiones de punto de venta con boletas (pendiente)."""


def cargar_compras(env):
    """Evelyn: órdenes de compra de insumos y facturas de proveedor (pendiente)."""


def main(env):
    if ya_hay_datos_de_demostracion(env):
        print('Ya hay datos de demostración (movimientos con origen DEMO-): no se carga nada. '
              'Para repetir la carga, recrea la base de datos con scripts/init_db.sh.')
        return
    cargar_inventario_y_produccion(env)
    cargar_compras(env)
    cargar_ventas(env)
    cargar_pdv(env)


# `env` existe cuando el archivo se ejecuta con `odoo shell`; al importarlo (pruebas) no se ejecuta nada
if 'env' in globals():
    main(env)  # noqa: F821
