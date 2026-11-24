from odoo import Command, api, fields, models
from odoo.exceptions import UserError, ValidationError


class Liquidacion(models.Model):
    """Liquidación diaria de un heladero concesionario (HU-20, RF004, CU004)."""
    _name = 'donofrio.liquidacion'
    _description = 'Liquidación diaria del heladero'
    _inherit = ['mail.thread']
    _order = 'fecha desc, id desc'

    _unica_por_dia = models.Constraint(
        'UNIQUE(partner_id, fecha)', 'Ya existe una liquidación de ese heladero para esa fecha.')
    _comision_valida = models.Constraint(
        'CHECK(porcentaje_comision >= 0 AND porcentaje_comision <= 100)',
        'El porcentaje de comisión debe estar entre 0 y 100.')

    name = fields.Char('Número', default='/', readonly=True, copy=False)
    partner_id = fields.Many2one(
        'res.partner', 'Heladero', required=True, tracking=True,
        domain=lambda self: [('category_id', 'in', self.env.ref('donofrio_base.cat_heladero').ids)])
    fecha = fields.Date('Fecha', required=True, default=fields.Date.context_today, tracking=True)
    pricelist_id = fields.Many2one(
        'product.pricelist', 'Lista de precios', required=True,
        default=lambda self: self.env.ref('donofrio_base.lista_heladero', raise_if_not_found=False))
    state = fields.Selection(
        [('borrador', 'Borrador'), ('despachado', 'Despachado'), ('liquidado', 'Liquidado')],
        'Estado', default='borrador', required=True, tracking=True, copy=False)
    linea_ids = fields.One2many('donofrio.liquidacion.linea', 'liquidacion_id', 'Productos', copy=True)
    porcentaje_comision = fields.Float(
        'Comisión (%)', default=10.0, help="Porcentaje del importe vendido que se queda el heladero. Valor supuesto del caso.")
    efectivo_entregado = fields.Float('Efectivo entregado')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(related='pricelist_id.currency_id')
    total_vendido = fields.Float('Unidades vendidas', compute='_compute_totales', store=True)
    total_importe = fields.Monetary('Importe vendido', compute='_compute_totales', store=True)
    total_comision = fields.Monetary('Comisión', compute='_compute_totales', store=True)
    diferencia_efectivo = fields.Monetary('Diferencia de efectivo', compute='_compute_totales', store=True,
                                          help="Efectivo entregado menos el importe vendido. Positivo: a favor de la empresa.")
    order_id = fields.Many2one('sale.order', 'Pedido de venta', readonly=True, copy=False)

    @api.depends('linea_ids.vendido', 'linea_ids.importe', 'porcentaje_comision', 'efectivo_entregado')
    def _compute_totales(self):
        for liq in self:
            liq.total_vendido = sum(liq.linea_ids.mapped('vendido'))
            liq.total_importe = sum(liq.linea_ids.mapped('importe'))
            liq.total_comision = liq.total_importe * liq.porcentaje_comision / 100.0
            liq.diferencia_efectivo = liq.efectivo_entregado - liq.total_importe

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('donofrio.liquidacion') or '/'
        return super().create(vals_list)

    def action_despachar(self):
        for liq in self:
            if liq.state != 'borrador':
                raise UserError(self.env._('Solo se puede despachar una liquidación en borrador.'))
            if not liq.linea_ids:
                raise UserError(self.env._('Agrega al menos un producto despachado.'))
            liq.state = 'despachado'

    def action_volver_borrador(self):
        for liq in self:
            if liq.state != 'despachado':
                raise UserError(self.env._('Solo se puede volver a borrador una liquidación despachada.'))
            liq.state = 'borrador'

    def action_confirmar(self):
        """Confirma la liquidación: crea y confirma el pedido de venta con lo vendido."""
        for liq in self:
            if liq.state != 'despachado':
                raise UserError(self.env._('Solo se puede confirmar una liquidación despachada.'))
            vendidas = liq.linea_ids.filtered(lambda lin: lin.vendido > 0)
            if not vendidas:
                raise UserError(self.env._('No hay unidades vendidas: no se crea ningún pedido.'))
            pedido = self.env['sale.order'].create({
                'partner_id': liq.partner_id.id,
                'pricelist_id': liq.pricelist_id.id,
                'date_order': fields.Datetime.now(),
                'origin': liq.name,
                'company_id': liq.company_id.id,
                'order_line': [Command.create({
                    'product_id': lin.product_id.id,
                    'product_uom_qty': lin.vendido,
                }) for lin in vendidas],
            })
            pedido.action_confirm()
            liq.write({'order_id': pedido.id, 'state': 'liquidado'})
            liq.message_post(body=self.env._('Liquidación confirmada: pedido %s.', pedido.name))


class LiquidacionLinea(models.Model):
    """Una línea por producto: despachado, devuelto y merma. Vendido = despachado − devuelto − merma."""
    _name = 'donofrio.liquidacion.linea'
    _description = 'Línea de la liquidación del heladero'
    _order = 'id'

    _cantidades_positivas = models.Constraint(
        'CHECK(despachado >= 0 AND devuelto >= 0 AND merma >= 0)', 'Las cantidades no pueden ser negativas.')

    liquidacion_id = fields.Many2one('donofrio.liquidacion', required=True, ondelete='cascade', index=True)
    product_id = fields.Many2one(
        'product.product', 'Producto', required=True, domain=[('sale_ok', '=', True)])
    despachado = fields.Float('Despachado', default=0.0)
    devuelto = fields.Float('Devuelto', default=0.0)
    merma = fields.Float('Merma', default=0.0)
    vendido = fields.Float('Vendido', compute='_compute_vendido', store=True)
    precio_unitario = fields.Float('Precio', compute='_compute_precio', store=True)
    importe = fields.Monetary('Importe', compute='_compute_importe', store=True)
    currency_id = fields.Many2one(related='liquidacion_id.currency_id')

    @api.depends('despachado', 'devuelto', 'merma')
    def _compute_vendido(self):
        for lin in self:
            lin.vendido = lin.despachado - lin.devuelto - lin.merma

    @api.depends('product_id', 'liquidacion_id.pricelist_id', 'liquidacion_id.fecha')
    def _compute_precio(self):
        for lin in self:
            liq = lin.liquidacion_id
            if not lin.product_id or not liq.pricelist_id:
                lin.precio_unitario = 0.0
                continue
            lin.precio_unitario = liq.pricelist_id._get_product_price(
                lin.product_id, 1.0, currency=liq.currency_id, date=liq.fecha)

    @api.depends('vendido', 'precio_unitario')
    def _compute_importe(self):
        for lin in self:
            lin.importe = lin.vendido * lin.precio_unitario

    @api.constrains('despachado', 'devuelto', 'merma')
    def _check_vendido(self):
        for lin in self:
            if lin.devuelto + lin.merma > lin.despachado:
                raise ValidationError(self.env._(
                    'En %(producto)s, lo devuelto más la merma (%(suma)g) supera lo despachado (%(desp)g).',
                    producto=lin.product_id.display_name, suma=lin.devuelto + lin.merma, desp=lin.despachado))
