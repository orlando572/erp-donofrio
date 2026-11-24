from odoo.addons.donofrio_base.tests.common import DonofrioStockCase


class CasoLoteRechazado(DonofrioStockCase):
    """Prepara un lote de helado con una inspección rechazada, sin pasar por toda la producción."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.helado = cls.env.ref('donofrio_base.pt_h01').product_variant_id
        cls.bom = cls.env.ref('donofrio_base.bom_pt_h01')

    @classmethod
    def _inspeccion_de(cls, lote, estado, contexto=None):
        orden = cls.env['mrp.production'].create({
            'product_id': cls.helado.id, 'product_qty': 10, 'bom_id': cls.bom.id})
        return cls.env['donofrio.calidad.inspeccion'].with_context(**(contexto or {})).create({
            'production_id': orden.id, 'lot_id': lote.id, 'state': estado})


