from datetime import timedelta

from odoo import Command, fields
from odoo.tests import TransactionCase


class DonofrioStockCase(TransactionCase):
    """Utilidades de inventario compartidas por los tests de logística y producción (HU-11, HU-12, HU-14)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lim = cls.env.ref('stock.warehouse0')
        cls.aqp = cls.env.ref('donofrio_base.wh_aqp')
        cls.proveedores = cls.env.ref('stock.stock_location_suppliers')
        cls.Quant = cls.env['stock.quant']
        cls.Lote = cls.env['stock.lot']

    @classmethod
    def _producto(cls, xmlid):
        return cls.env.ref(f'donofrio_base.{xmlid}').product_variant_id

    @classmethod
    def _lote(cls, producto, nombre, dias_para_vencer):
        """Crea un lote con fecha de vencimiento explícita (la fecha de retiro y de alerta se calculan sola)."""
        return cls.Lote.create({
            'name': nombre,
            'product_id': producto.id,
            'expiration_date': fields.Datetime.now() + timedelta(days=dias_para_vencer),
        })

    @classmethod
    def _stock(cls, producto, lote, cantidad, ubicacion=None):
        """Pone existencias de un lote en la ubicación (por defecto, el stock de Lima)."""
        ubicacion = ubicacion or cls.lim.lot_stock_id
        cls.Quant._update_available_quantity(producto, ubicacion, cantidad, lot_id=lote)

    def _picking(self, tipo, origen, destino, producto, cantidad):
        picking = self.env['stock.picking'].create({
            'picking_type_id': tipo.id,
            'location_id': origen.id,
            'location_dest_id': destino.id,
            'move_ids': [Command.create({
                'product_id': producto.id,
                'product_uom_qty': cantidad,
                'product_uom': producto.uom_id.id,
                'location_id': origen.id,
                'location_dest_id': destino.id,
            })],
        })
        picking.action_confirm()
        return picking

    def _recibir(self, producto, cantidad, lote=None, dias_para_vencer=None):
        """Recepción de proveedor en Lima. Si se da ``lote``, lo pone en el detalle; si no, lo deja vacío."""
        tipo = self.lim.in_type_id
        picking = self._picking(tipo, self.proveedores, tipo.default_location_dest_id, producto, cantidad)
        linea = picking.move_ids.move_line_ids
        linea.quantity = cantidad
        if lote:
            linea.lot_name = lote
            if dias_para_vencer is not None:
                linea.expiration_date = fields.Datetime.now() + timedelta(days=dias_para_vencer)
        picking.move_ids.picked = True
        return picking

    def _disponible(self, producto, lote, ubicacion=None):
        ubicacion = ubicacion or self.lim.lot_stock_id
        return self.Quant._get_available_quantity(producto, ubicacion, lot_id=lote)
