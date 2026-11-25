from datetime import datetime, time

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
MESES_DEL_GRAFICO = 6
DIAS_POR_VENCER = 30
DIAS_ALERTAS_TEMPERATURA = 7
# Modelos que lee el tablero sí o sí (las tarjetas de los módulos opcionales se ocultan por su cuenta)
MODELOS_BASE = {
    'sale.order': 'Ventas',
    'stock.warehouse': 'Inventario',
    'stock.quant': 'Inventario',
    'stock.lot': 'Inventario',
    'mrp.production': 'Fabricación',
}


class Tablero(models.AbstractModel):
    """Datos del tablero gerencial (HU-22, RF013, CU009). Solo lee: no tiene tablas ni escribe nada.

    Respeta los permisos de quien lo abre (no usa ``sudo``). Las tarjetas de los módulos opcionales de la
    Fase 2 (calidad, heladeros y cadena de frío) salen solo si el módulo está instalado.
    """
    _name = 'donofrio.tablero'
    _description = 'Tablero gerencial de KPIs'

    @api.model
    def _modelo_disponible(self, modelo):
        """El módulo del modelo está instalado y quien abre el tablero puede leerlo."""
        return modelo in self.env and self.env[modelo].has_access('read')

    @api.model
    def _areas_sin_permiso(self):
        """Áreas (Ventas, Inventario, Fabricación) cuyos datos base el usuario no puede leer."""
        faltan = {area for modelo, area in MODELOS_BASE.items() if not self.env[modelo].has_access('read')}
        return sorted(faltan)

    @api.model
    def _inicio_de_mes(self, ahora, desplazamiento=0):
        """Primer instante del mes de ``ahora`` (más ``desplazamiento`` meses), como datetime ingenuo en UTC."""
        primero = ahora.date().replace(day=1) + relativedelta(months=desplazamiento)
        return datetime.combine(primero, time.min)

    @api.model
    def get_kpis(self, warehouse_id=False):
        """Devuelve los KPI del tablero, opcionalmente de un solo almacén.

        Si el usuario no puede leer los datos base (por ejemplo, entró por la dirección sin permiso de ventas),
        no lanza un error de acceso: devuelve ``sin_permiso`` y un mensaje que el componente muestra en pantalla.
        """
        areas = self._areas_sin_permiso()
        if areas:
            return {
                'sin_permiso': True,
                'areas': areas,
                'mensaje': self.env._(
                    'No tienes permiso para ver el tablero gerencial: falta acceso a %s. '
                    'Pide a un administrador que te dé acceso a esas áreas.', ', '.join(areas)),
            }
        warehouse_id = int(warehouse_id) if warehouse_id else False
        ahora = fields.Datetime.now()
        moneda = self.env.company.currency_id
        resultado = {
            'almacenes': [{'id': w.id, 'nombre': w.name} for w in self.env['stock.warehouse'].search([])],
            'almacen_id': warehouse_id,
            'moneda': moneda.symbol,
            'decimales': moneda.decimal_places,
            'generado': fields.Datetime.to_string(ahora),
            'ventas_mes': self._ventas_mes(ahora, warehouse_id),
            'ventas_por_mes': self._ventas_por_mes(ahora, warehouse_id),
            'produccion': self._produccion(ahora, warehouse_id),
            'stock_por_vencer': self._stock_por_vencer(ahora, warehouse_id),
        }
        if self._modelo_disponible('donofrio.calidad.inspeccion'):
            resultado['lotes_aprobados'] = self._lotes_aprobados(warehouse_id)
        if self._modelo_disponible('donofrio.liquidacion'):
            resultado['liquidaciones_pendientes'] = self._liquidaciones_pendientes()
        if self._modelo_disponible('donofrio.temperatura'):
            resultado['alertas_temperatura'] = self._alertas_temperatura(ahora, warehouse_id)
        return resultado

    # --- Ventas ----------------------------------------------------------------------------------------

    @api.model
    def _dominio_ventas(self, desde, hasta, warehouse_id):
        dominio = [('state', 'in', ('sale', 'done')), ('date_order', '>=', desde), ('date_order', '<', hasta)]
        if warehouse_id:
            dominio.append(('warehouse_id', '=', warehouse_id))
        return dominio

    @api.model
    def _ventas_mes(self, ahora, warehouse_id):
        Pedido = self.env['sale.order']
        este, siguiente, anterior = (self._inicio_de_mes(ahora, d) for d in (0, 1, -1))
        grupos = Pedido._read_group(
            self._dominio_ventas(este, siguiente, warehouse_id), groupby=['team_id'], aggregates=['amount_total:sum'])
        por_canal = sorted(
            ({'canal': equipo.name or self.env._('Sin equipo'), 'total': total} for equipo, total in grupos),
            key=lambda fila: -fila['total'])
        total = sum(fila['total'] for fila in por_canal)
        total_anterior = sum(
            Pedido._read_group(self._dominio_ventas(anterior, este, warehouse_id), aggregates=['amount_total:sum'])[0])
        variacion = round((total - total_anterior) / total_anterior * 100, 1) if total_anterior else None
        return {'total': total, 'anterior': total_anterior, 'variacion_pct': variacion, 'por_canal': por_canal}

    @api.model
    def _ventas_por_mes(self, ahora, warehouse_id):
        """Ventas de los últimos seis meses (incluido el actual); los meses sin ventas salen en cero."""
        desde = self._inicio_de_mes(ahora, -(MESES_DEL_GRAFICO - 1))
        hasta = self._inicio_de_mes(ahora, 1)
        grupos = self.env['sale.order']._read_group(
            self._dominio_ventas(desde, hasta, warehouse_id),
            groupby=['date_order:month'], aggregates=['amount_total:sum'])
        por_mes = {(fecha.year, fecha.month): total for fecha, total in grupos}
        meses = []
        for desplazamiento in range(-(MESES_DEL_GRAFICO - 1), 1):
            inicio = self._inicio_de_mes(ahora, desplazamiento)
            meses.append({
                'mes': inicio.strftime('%Y-%m'),
                'etiqueta': MESES[inicio.month - 1],
                'total': por_mes.get((inicio.year, inicio.month), 0.0),
            })
        return meses

    # --- Producción ------------------------------------------------------------------------------------

    @api.model
    def _produccion(self, ahora, warehouse_id):
        este, siguiente = self._inicio_de_mes(ahora, 0), self._inicio_de_mes(ahora, 1)
        dominio = [('state', 'in', ('confirmed', 'progress', 'to_close', 'done')),
                   ('date_start', '>=', este), ('date_start', '<', siguiente)]
        if warehouse_id:
            dominio.append(('picking_type_id.warehouse_id', '=', warehouse_id))
        grupos = self.env['mrp.production']._read_group(dominio, groupby=['state'], aggregates=['__count'])
        cuenta = {estado: n for estado, n in grupos}
        planificadas = sum(cuenta.values())
        hechas = cuenta.get('done', 0)
        return {
            'hechas': hechas,
            'planificadas': planificadas,
            'cumplimiento_pct': round(hechas / planificadas * 100, 1) if planificadas else None,
        }

    # --- Stock por vencer ------------------------------------------------------------------------------

    @api.model
    def _stock_por_vencer(self, ahora, warehouse_id):
        limite = ahora + relativedelta(days=DIAS_POR_VENCER)
        dominio = [('location_id.usage', '=', 'internal'), ('quantity', '>', 0), ('lot_id.expiration_date', '!=', False)]
        if warehouse_id:
            dominio.append(('location_id.warehouse_id', '=', warehouse_id))
        quants = self.env['stock.quant'].search(dominio)
        por_vencer = quants.filtered(lambda q: ahora <= q.lot_id.expiration_date <= limite)
        vencidos = quants.filtered(lambda q: q.lot_id.expiration_date < ahora)
        return {
            'dias': DIAS_POR_VENCER,
            'lotes': len(por_vencer.lot_id),
            'valor': sum(q.quantity * q.product_id.standard_price for q in por_vencer),
            'vencidos': len(vencidos.lot_id),
        }

    # --- Módulos opcionales de la Fase 2 ---------------------------------------------------------------

    @api.model
    def _lotes_aprobados(self, warehouse_id):
        """M1: de los lotes con inspección terminada, cuántos se aprobaron."""
        dominio = [('state', 'in', ('aprobada', 'rechazada'))]
        if warehouse_id:
            dominio.append(('production_id.picking_type_id.warehouse_id', '=', warehouse_id))
        grupos = self.env['donofrio.calidad.inspeccion']._read_group(dominio, groupby=['state'], aggregates=['__count'])
        cuenta = {estado: n for estado, n in grupos}
        aprobados = cuenta.get('aprobada', 0)
        inspeccionados = aprobados + cuenta.get('rechazada', 0)
        return {
            'aprobados': aprobados,
            'inspeccionados': inspeccionados,
            'aprobados_pct': round(aprobados / inspeccionados * 100, 1) if inspeccionados else None,
        }

    @api.model
    def _liquidaciones_pendientes(self):
        """M2: liquidaciones de heladeros que aún no están liquidadas (no dependen del almacén)."""
        pendientes = self.env['donofrio.liquidacion'].search_count([('state', '!=', 'liquidado')])
        return {'cantidad': pendientes}

    @api.model
    def _alertas_temperatura(self, ahora, warehouse_id):
        """M3: lecturas fuera de rango de los últimos días."""
        dominio = [('fuera_de_rango', '=', True), ('fecha', '>=', ahora - relativedelta(days=DIAS_ALERTAS_TEMPERATURA))]
        if warehouse_id:
            dominio.append(('location_id.warehouse_id', '=', warehouse_id))
        return {'cantidad': self.env['donofrio.temperatura'].search_count(dominio), 'dias': DIAS_ALERTAS_TEMPERATURA}
