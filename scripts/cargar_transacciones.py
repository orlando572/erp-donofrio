"""HU-16: 3-4 meses de transacciones de demostración, generadas con semilla fija.

Uso (con la BD ya inicializada con donofrio_base). Detén antes el servicio web: sus tareas programadas (cron)
corren sobre la misma BD y pueden chocar con el script («could not serialize access due to concurrent update»):

    docker compose stop odoo
    docker compose run --rm -T odoo odoo shell -d donofrio --no-http < scripts/cargar_transacciones.py
    docker compose up -d odoo

El script define dos partes, que se ejecutan en este orden:

* Orlando (inventario y producción): inventario inicial con lotes por vencer, recepciones semanales de
  insumos con lote, órdenes de producción (con lote, vencimiento y costo) y reposición semanal
  Lima → Arequipa (``cargar_inventario_y_produccion``).
* Evelyn (ventas, PdV y compras), con su propia semilla (``SEMILLA + 1``) para no alterar lo de Orlando:
  - ``ventas_de_la_semana``: pedidos de los 30 clientes por canal (distribuidores, autoservicios, bodegas y
    heladeros), con su lista de precios, entrega con FEFO, factura (01) o boleta (03) y cobro (al contado o al
    vencer el crédito). El panetón de octubre y noviembre va en su propio pedido con la lista «Campaña Navidad».
  - ``pdv_de_la_semana``: una sesión de caja por día en la «Heladería Av. Venezuela», con pedidos de mostrador
    (efectivo y Yape, algunos con boleta) y cierre cuadrado.
  - ``cargar_compras``: una orden de compra por proveedor y recepción, **enlazada a la recepción que ya hizo
    Orlando** (así no se duplica el stock), con su factura de proveedor y su pago.
  Ventas y PdV corren dentro del bucle semanal, después de producir, para que cada venta solo saque lotes que ya
  existían ese día. Las compras se registran al final.

Para probar con menos semanas (más rápido): ``docker compose run --rm -T -e DONOFRIO_DEMO_SEMANAS=2 odoo odoo shell ...``

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
import os
import random
from contextlib import contextmanager
from datetime import date, datetime, time, timedelta

from odoo import Command, fields

SEMILLA = 2026
FIN = date(2026, 11, 22)
SEMANAS = 16
SEMANAS_A_CARGAR = int(os.environ.get('DONOFRIO_DEMO_SEMANAS', SEMANAS))   # para probar con menos semanas
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


# --- Ventas, punto de venta y compras (Evelyn) ----------------------------------------------------------
#
# Las horas van en UTC: 14:00 a 22:00 UTC son las 9:00 a 17:00 de Lima (UTC-5), el horario de la tienda.
#
# Ventas y PdV se generan semana a semana, dentro del mismo bucle que la producción de Orlando, después de
# producir y de reponer Arequipa: así cada venta solo puede sacar lotes que ya existían ese día. Usan su propia
# semilla (SEMILLA + 1) para no alterar los números aleatorios de inventario y producción.
# Las compras se registran al final, sobre las recepciones de insumos que ya hizo ``recibir_insumos``: la orden
# de compra se enlaza a esa recepción en vez de crear otra, para no duplicar el stock.

# Parte de la demanda semanal de cada terminado que compra cada canal (suman 68 %; lo demás queda como existencias)
PARTICIPACION = {'distribuidor': 0.36, 'autoservicio': 0.14, 'bodega': 0.10, 'heladero': 0.08}
LINEAS_DEL_CANAL = {
    'distribuidor': ('helados', 'chocolates', 'paneton'),
    'autoservicio': ('helados', 'chocolates', 'paneton'),
    'bodega': ('helados', 'chocolates'),
    'heladero': ('helados',),
}
ALMACEN_DEL_CANAL = {'distribuidor': 'lim', 'autoservicio': 'lim', 'bodega': 'aqp', 'heladero': 'aqp'}
EQUIPO_DEL_CANAL = {'distribuidor': 'equipo_moderno', 'autoservicio': 'equipo_moderno',
                    'bodega': 'equipo_tradicional', 'heladero': 'equipo_heladeros'}
VENDEDOR_DEL_CANAL = {'distribuidor': 'user_jefe_ventas', 'autoservicio': 'user_jefe_ventas',
                      'bodega': 'user_vendedor', 'heladero': 'user_jefe_ventas'}
CATEGORIA_DEL_CANAL = {'distribuidor': 'cat_distribuidor', 'autoservicio': 'cat_autoservicio',
                       'bodega': 'cat_bodega', 'heladero': 'cat_heladero'}
DIAS_DEL_CANAL = {'distribuidor': (0, 1), 'autoservicio': (2,), 'bodega': (3, 4), 'heladero': (0, 1, 2, 3, 4, 5)}
INICIO_CAMPANIA = date(2026, 10, 1)          # panetón: campaña de Navidad (lista «Campaña Navidad»)
DEMANDA_DE_TERMINADOS_SIN_RECETA = 80        # unidades por semana; solo tienen el inventario inicial
PDV_PEDIDOS_BASE = 10                        # pedidos de mostrador por día, antes de la estación
PDV_FACTURA = 0.08                           # parte de las ventas del mostrador que pide boleta
PDV_YAPE = 0.35                              # parte de las ventas del mostrador que se paga con Yape


def preparar_ventas(ctx):
    """Clientes por canal, línea de cada terminado y tamaño de tanda de cada receta (se hace una sola vez)."""
    if getattr(ctx, 'clientes', None) is not None:
        return
    env = ctx.env
    ctx.rng_ventas = random.Random(SEMILLA + 1)
    ctx.clientes = {
        canal: env['res.partner'].search([('category_id', 'in', env.ref(f'donofrio_base.{cat}').ids)], order='id')
        for canal, cat in CATEGORIA_DEL_CANAL.items()}
    ctx.terminados = env['product.product'].search([
        ('categ_id', 'child_of', env.ref('donofrio_base.cat_terminados').id)], order='default_code')
    lineas = {env.ref(f'donofrio_base.cat_{linea}').id: linea for linea in ('helados', 'chocolates', 'paneton')}
    ctx.linea = {p.id: lineas[p.categ_id.id] for p in ctx.terminados}
    ctx.tanda = {p.id: env['mrp.bom']._bom_find(p)[p].product_qty
                 for p in ctx.terminados if p.default_code in PRODUCCION}
    ctx.banco = env['account.journal'].search([('type', '=', 'bank'), ('code', '=', 'BNK1')], limit=1)
    ctx.yape = env.ref('donofrio_base.diario_yape')
    ctx.ventas = ctx.pedidos_pdv = ctx.boletas_pdv = ctx.contador_pdv = 0


def demanda_semanal(ctx, lunes):
    """Unidades por semana de cada terminado: lo que se produce (tandas base × receta × estación)."""
    demanda = {}
    for producto in ctx.terminados:
        if producto.default_code in PRODUCCION:
            linea, base = PRODUCCION[producto.default_code]
            demanda[producto] = base * ctx.tanda[producto.id] * factor_estacional(linea, lunes + timedelta(days=2))
        else:
            demanda[producto] = DEMANDA_DE_TERMINADOS_SIN_RECETA
    return demanda


def disponible(ctx, producto, almacen):
    return ctx.env['stock.quant']._get_available_quantity(producto, almacen.lot_stock_id)


def vendedor_y_equipo(ctx, canal):
    return ctx.env.ref(f'donofrio_base.{VENDEDOR_DEL_CANAL[canal]}'), ctx.env.ref(f'donofrio_base.{EQUIPO_DEL_CANAL[canal]}')


def entregar(ctx, pedido, dia):
    """Valida la entrega del pedido (pick y ship si hay dos pasos) con fecha histórica."""
    for _ in range(3):
        listos = pedido.picking_ids.filtered(lambda p: p.state == 'assigned')
        if not listos:
            break
        listos.move_ids.picked = True
        listos.with_context(skip_expired=True, skip_backorder=True, skip_sms=True,
                            force_period_date=dia).button_validate()
        esperando = pedido.picking_ids.filtered(lambda p: p.state in ('confirmed', 'waiting'))
        if esperando:
            esperando.action_assign()
    for picking in pedido.picking_ids:
        fechar_picking(picking, momento(dia, 20))


def facturar(ctx, pedido, dia):
    """Factura (01) o boleta (03) del pedido, con la fecha de la entrega. Devuelve la factura registrada."""
    factura = pedido._create_invoices()
    factura.write({'invoice_date': dia})
    factura.action_post()
    return factura


def cobrar(ctx, factura, dia_pago, diario):
    """Registra el pago de la factura el ``dia_pago``; si cae después del cierre, queda por cobrar."""
    if dia_pago > FIN:
        return
    pago = ctx.env['account.payment.register'].with_context(
        active_model='account.move', active_ids=factura.ids).create({
            'payment_date': dia_pago, 'journal_id': diario.id, 'amount': factura.amount_residual})
    pago._create_payments()


def vender(ctx, cliente, canal, lineas, dia, lista=None):
    """Pedido de venta → entrega → factura o boleta → cobro. ``lineas`` es una lista de (producto, unidades)."""
    env, rng = ctx.env, ctx.rng_ventas
    almacen = ctx.lim if ALMACEN_DEL_CANAL[canal] == 'lim' else ctx.aqp
    vendedor, equipo = vendedor_y_equipo(ctx, canal)
    lineas_ok = []
    for producto, cantidad in lineas:
        cantidad = min(round(cantidad), math.floor(disponible(ctx, producto, almacen) * 0.8))
        if cantidad >= 1:
            lineas_ok.append((producto, cantidad))
    if not lineas_ok:
        return None
    valores = {
        'partner_id': cliente.id, 'user_id': vendedor.id, 'team_id': equipo.id, 'warehouse_id': almacen.id,
        'date_order': momento(dia, 15), 'client_order_ref': f'{PREFIJO}VTA-{dia:%Y%m%d}-{cliente.id}',
        'order_line': [Command.create({'product_id': p.id, 'product_uom_qty': q}) for p, q in lineas_ok],
    }
    if lista:
        valores['pricelist_id'] = lista.id
    pedido = env['sale.order'].create(valores)
    pedido.action_confirm()
    pedido.write({'date_order': momento(dia, 15)})
    entrega = dia + timedelta(days=1) if canal in ('distribuidor', 'autoservicio') else dia
    entregar(ctx, pedido, entrega)
    if any(p.state != 'done' for p in pedido.picking_ids):
        return pedido                      # sin entrega completa no se factura
    factura = facturar(ctx, pedido, entrega)
    # Con crédito se cobra al vencer (con algo de atraso); al contado, el mismo día
    credito = factura.invoice_date_due and factura.invoice_date_due > factura.invoice_date
    dia_pago = factura.invoice_date_due + timedelta(days=rng.randint(0, 8)) if credito else entrega
    diario = ctx.banco if cliente.l10n_latam_identification_type_id == env.ref('l10n_pe.it_RUC') else ctx.yape
    cobrar(ctx, factura, dia_pago, diario)
    ctx.ventas += 1
    return pedido


def ventas_de_la_semana(ctx, lunes):
    """Pedidos de cada canal: distribuidores cada semana, autoservicios cada dos, bodegas casi siempre, heladeros todas."""
    preparar_ventas(ctx)
    rng = ctx.rng_ventas
    demanda = demanda_semanal(ctx, lunes)
    numero_de_semana = (lunes - INICIO).days // 7
    for canal, clientes in ctx.clientes.items():
        piden = [c for i, c in enumerate(clientes)
                 if (canal != 'autoservicio' or (i + numero_de_semana) % 2 == 0)
                 and (canal != 'bodega' or rng.random() < 0.7)]
        if not piden:
            continue
        for indice, cliente in enumerate(piden):
            dias = DIAS_DEL_CANAL[canal]
            dia = lunes + timedelta(days=dias[indice % len(dias)])
            en_campania = dia >= INICIO_CAMPANIA and canal in ('distribuidor', 'autoservicio')
            productos = [p for p in demanda if ctx.linea[p.id] in LINEAS_DEL_CANAL[canal]
                         and not (en_campania and ctx.linea[p.id] == 'paneton')]
            elegidos = rng.sample(productos, min(len(productos), rng.randint(3, 6)))
            escala = len(productos) / len(elegidos)
            lineas = [(p, demanda[p] * PARTICIPACION[canal] / len(piden) * escala * rng.uniform(0.7, 1.3))
                      for p in elegidos]
            vender(ctx, cliente, canal, lineas, dia)
            if en_campania:                  # el panetón de campaña va en su pedido, con la lista de Navidad
                paneton = [p for p in demanda if ctx.linea[p.id] == 'paneton']
                lineas = [(p, demanda[p] * PARTICIPACION[canal] / len(piden) * rng.uniform(0.7, 1.3)) for p in paneton]
                vender(ctx, cliente, canal, lineas, dia, lista=ctx.env.ref('donofrio_base.lista_navidad'))


# --- Punto de venta ------------------------------------------------------------------------------------

@contextmanager
def como_si_fuera(dia):
    """Hace que Odoo crea que hoy es ``dia`` mientras se abre, vende y cierra una sesión del PdV.

    El asiento del cierre de caja toma su fecha de la hora real (``Date.context_today``) y su número, del mes de
    esa fecha: sin esto, todas las sesiones quedarían con la fecha de la corrida y no se vería la estacionalidad.
    """
    ahora = momento(dia, 22)
    fecha_original, hora_original = fields.Date.context_today, fields.Datetime.now
    fields.Date.context_today = staticmethod(lambda registro, timestamp=None: dia)
    fields.Datetime.now = staticmethod(lambda: ahora)
    try:
        yield
    finally:
        fields.Date.context_today, fields.Datetime.now = fecha_original, hora_original


def lote_fefo(ctx, producto, cantidad):
    """Primer lote de Lima (el que vence antes) con existencias para la venta, como lo elegiría el cajero."""
    Quant = ctx.env['stock.quant']
    for quant in Quant.search([
            ('product_id', '=', producto.id), ('location_id', '=', ctx.lim.lot_stock_id.id),
            ('lot_id', '!=', False), ('quantity', '>', 0)], order='removal_date, in_date, id'):
        if quant.quantity - quant.reserved_quantity >= cantidad:
            return quant.lot_id
    return None


def pedido_de_mostrador(ctx, sesion, dia, hora, metodos):
    """Datos de un pedido como los envía la interfaz del PdV, o None si no hay con qué armarlo."""
    env, rng = ctx.env, ctx.rng_ventas
    config = sesion.config_id
    campania = dia >= INICIO_CAMPANIA
    pesos = {'helados': 0.7, 'chocolates': 0.2, 'paneton': 0.1 if campania else 0.0}
    lineas = []
    for producto in rng.sample(list(ctx.terminados), len(ctx.terminados)):
        if len(lineas) >= rng.randint(1, 3):
            break
        if rng.random() > pesos[ctx.linea[producto.id]]:
            continue
        cantidad = rng.randint(1, 2 if producto.list_price > 10 else 4)
        lote = lote_fefo(ctx, producto, cantidad)
        if lote:
            lineas.append((producto, cantidad, lote))
    if not lineas:
        return None
    detalle, total_sin, total_con = [], 0.0, 0.0
    for numero, (producto, cantidad, lote) in enumerate(lineas, start=1):
        precio = config.pricelist_id._get_product_price(producto, cantidad, date=momento(dia, hora))
        impuestos = producto.taxes_id.filtered_domain(env['account.tax']._check_company_domain(env.company))
        calculo = impuestos.compute_all(precio, sesion.currency_id, cantidad)
        total_sin += calculo['total_excluded']
        total_con += calculo['total_included']
        detalle.append((0, 0, {
            'id': numero, 'pack_lot_ids': [[0, 0, {'lot_name': lote.name}]], 'price_unit': precio,
            'product_id': producto.id, 'qty': cantidad, 'price_subtotal': calculo['total_excluded'],
            'price_subtotal_incl': calculo['total_included'], 'tax_ids': [(6, 0, impuestos.ids)]}))
    metodo = metodos['yape'] if rng.random() < PDV_YAPE else metodos['efectivo']
    boleta = rng.random() < PDV_FACTURA
    ctx.contador_pdv += 1
    uuid = f'{dia:%y%m%d}{hora:02d}-{ctx.contador_pdv // 10000:03d}-{ctx.contador_pdv % 10000:04d}'
    cuando = fields_datetime(momento(dia, hora) + timedelta(minutes=rng.randint(0, 59)))
    return {
        'amount_paid': total_con, 'amount_return': 0, 'amount_tax': total_con - total_sin, 'amount_total': total_con,
        'date_order': cuando, 'pricelist_id': config.pricelist_id.id, 'name': f'Order {uuid}', 'uuid': uuid,
        'last_order_preparation_change': '{}', 'session_id': sesion.id, 'user_id': env.ref('donofrio_base.user_cajero_pdv').id,
        'partner_id': env.ref('l10n_pe_pos.partner_pe_cf').id if boleta else False, 'to_invoice': boleta,
        'fiscal_position_id': False, 'lines': detalle,
        'payment_ids': [(0, 0, {'amount': total_con, 'name': cuando, 'payment_method_id': metodo.id})],
    }, metodo, total_con, boleta


def fields_datetime(valor):
    return valor.strftime('%Y-%m-%d %H:%M:%S')


def pdv_de_la_semana(ctx, lunes):
    """Una sesión de caja por día, de martes a domingo: apertura, boletas y cierre cuadrado."""
    preparar_ventas(ctx)
    env, rng = ctx.env, ctx.rng_ventas
    config = env.ref('donofrio_base.pos_config_venezuela')
    cajero = env.ref('donofrio_base.user_cajero_pdv')
    metodos = {'efectivo': env.ref('donofrio_base.pdv_metodo_efectivo'), 'yape': env.ref('donofrio_base.pdv_metodo_yape')}
    for dia_de_la_semana in range(1, 7):
        dia = lunes + timedelta(days=dia_de_la_semana)
        factor = factor_estacional('helados', dia) * (1.3 if dia.weekday() >= 5 else 1.0)
        pedidos_del_dia = max(2, round(PDV_PEDIDOS_BASE * factor * rng.uniform(0.8, 1.2)))
        with como_si_fuera(dia):
            config.with_user(cajero).open_ui()
            sesion = config.current_session_id
            apertura = float(rng.choice((50, 100)))
            sesion.set_opening_control(apertura, None)
            datos, efectivo = [], 0.0
            for n in range(pedidos_del_dia):
                armado = pedido_de_mostrador(ctx, sesion, dia, 14 + n * 8 // pedidos_del_dia, metodos)
                if armado:
                    dato, metodo, total, boleta = armado
                    datos.append(dato)
                    efectivo += total if metodo == metodos['efectivo'] else 0.0
                    ctx.boletas_pdv += 1 if boleta else 0
            if datos:
                env['pos.order'].with_user(cajero).sync_from_ui(datos)
            sesion = sesion.with_user(cajero)
            sesion.post_closing_cash_details(round(apertura + efectivo, 2))
            resultado = sesion.close_session_from_ui()
            assert resultado.get('successful'), resultado
        fechar_sesion(ctx, sesion.sudo(), dia)
        ctx.pedidos_pdv += len(datos)


def fechar_sesion(ctx, sesion, dia):
    """Hora de apertura y de cierre de la sesión (las fechas de los asientos ya salen bien con ``como_si_fuera``)."""
    ctx.env.cr.execute("UPDATE pos_session SET start_at = %s, stop_at = %s WHERE id = %s",
                       (momento(dia, 14), momento(dia, 22), sesion.id))
    sesion.invalidate_recordset()


# --- Compras -------------------------------------------------------------------------------------------

def cargar_compras(env):
    """Una orden de compra por proveedor y recepción, enlazada a la recepción que ya hizo ``recibir_insumos``;
    su factura de proveedor (01, con IGV) y el pago a los 30 días. Así el stock no se duplica."""
    rng = random.Random(SEMILLA + 2)
    Orden = env['purchase.order']
    factura_01 = env.ref('l10n_pe.document_type01')
    banco = env['account.journal'].search([('type', '=', 'bank'), ('code', '=', 'BNK1')], limit=1)
    recepciones = env['stock.picking'].search([('origin', '=like', f'{PREFIJO}REC-%')], order='scheduled_date, id')
    numero_de_factura, ordenes, facturas, pagadas = {}, 0, 0, 0
    for recepcion in recepciones:
        dia = recepcion.date_done.date()
        por_proveedor = {}
        for movimiento in recepcion.move_ids:
            proveedor = movimiento.product_id.seller_ids[:1].partner_id
            por_proveedor.setdefault(proveedor, []).append(movimiento)
        for proveedor, movimientos in por_proveedor.items():
            plazo = max(m.product_id.seller_ids[:1].delay for m in movimientos)
            orden = Orden.create({
                'partner_id': proveedor.id, 'date_order': momento(dia - timedelta(days=plazo), 14),
                'origin': f'{PREFIJO}COM-{dia:%Y%m%d}', 'user_id': env.ref('donofrio_base.user_compras').id,
                'picking_type_id': recepcion.picking_type_id.id,
                'order_line': [Command.create({
                    'product_id': m.product_id.id, 'product_qty': m.product_uom_qty, 'price_unit': m.price_unit,
                    'date_planned': momento(dia, 13)}) for m in movimientos],
            })
            for linea, movimiento in zip(orden.order_line, movimientos):
                movimiento.purchase_line_id = linea.id       # la recepción ya hecha cuenta como recibida
            orden.button_confirm()
            orden.write({'date_order': momento(dia - timedelta(days=plazo), 14), 'date_approve': momento(dia - timedelta(days=plazo), 14)})
            assert len(orden.picking_ids) == 1, f'{orden.name} creó otra recepción: {orden.picking_ids.mapped("name")}'
            orden.action_create_invoice()
            factura = orden.invoice_ids
            numero_de_factura[proveedor.id] = numero_de_factura.get(proveedor.id, 0) + 1
            vence = dia + timedelta(days=30)
            factura.write({
                'invoice_date': dia, 'invoice_date_due': vence,
                'l10n_latam_document_type_id': factura_01.id,
                'l10n_latam_document_number': f'F{proveedor.id % 900 + 100:03d}-{numero_de_factura[proveedor.id]:08d}',
            })
            factura.action_post()
            ordenes += 1
            facturas += 1
            dia_pago = vence + timedelta(days=rng.randint(-3, 5))
            if dia_pago <= FIN:
                env['account.payment.register'].with_context(
                    active_model='account.move', active_ids=factura.ids).create({
                        'payment_date': dia_pago, 'journal_id': banco.id, 'amount': factura.amount_residual,
                    })._create_payments()
                pagadas += 1
        env.cr.commit()
    print(f'Compras: {ordenes} órdenes de compra con su factura de proveedor ({pagadas} pagadas).')


# --- Partes del script ---------------------------------------------------------------------------------

def cargar_inventario_y_produccion(env):
    ctx = Contexto(env)
    print(f'Inventario y producción: {INICIO:%d/%m/%Y} → {FIN:%d/%m/%Y} ({SEMANAS} semanas, semilla {SEMILLA})')
    inventario_inicial(ctx)
    env.cr.commit()
    for semana in range(SEMANAS_A_CARGAR):
        lunes = INICIO + timedelta(weeks=semana)
        plan = planificar_semana(ctx, lunes)
        recibir_insumos(ctx, lunes + timedelta(days=DIA_DE_RECEPCION), necesidades_de_insumos(plan))
        producidos = {}
        for producto, bom, tandas, dia in sorted(plan, key=lambda p: p[3]):
            orden = producir(ctx, producto, bom, tandas, dia)
            producidos[producto] = producidos.get(producto, 0) + orden.product_qty
        reponer_arequipa(ctx, lunes + timedelta(days=DIA_DE_REPOSICION), producidos)
        ventas_de_la_semana(ctx, lunes)
        pdv_de_la_semana(ctx, lunes)
        env.cr.commit()
        print(f'  Semana {semana + 1:>2} ({lunes:%d/%m}): {len(plan)} OP, {ctx.ventas} ventas acumuladas, {ctx.pedidos_pdv} pedidos de mostrador')
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


def main(env):
    if ya_hay_datos_de_demostracion(env):
        print('Ya hay datos de demostración (movimientos con origen DEMO-): no se carga nada. '
              'Para repetir la carga, recrea la base de datos con scripts/init_db.sh.')
        return
    cargar_inventario_y_produccion(env)   # incluye las ventas y el PdV de cada semana
    cargar_compras(env)


# `env` existe cuando el archivo se ejecuta con `odoo shell`; al importarlo (pruebas) no se ejecuta nada
if 'env' in globals():
    main(env)  # noqa: F821
