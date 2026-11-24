from odoo.tests import tagged

from .common import CasoLoteRechazado


@tagged('post_install', '-at_install')
class TestHistorialEnEspanol(CasoLoteRechazado):
    """El «creado» del historial sale en español aunque la inspección la cree un script sin idioma."""

    def test_mensaje_de_creacion_en_espanol_sin_importar_el_idioma(self):
        for idioma in ('en_US', 'es_PE'):
            lote = self._lote(self.helado, f'LOTE-{idioma}', 200)
            inspeccion = self._inspeccion_de(lote, 'borrador', {'lang': idioma})
            cuerpos = ' '.join(inspeccion.message_ids.mapped('body'))
            self.assertIn(f'Inspección {inspeccion.name} creada', cuerpos, idioma)
            self.assertNotIn('created', cuerpos, idioma)
