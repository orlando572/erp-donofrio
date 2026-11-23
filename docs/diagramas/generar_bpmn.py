#!/usr/bin/env python3
"""Genera los BPMN AS-IS del Sprint 1 y los TO-BE del Sprint 2 como archivo .bpmn (editable en bpmn.io) y .svg.

Uso:  python3 docs/diagramas/generar_bpmn.py        (escribe en docs/diagramas/bpmn/)
El PNG se obtiene del SVG (ver docs/diagramas/README.md).

Cada proceso se describe con carriles (roles), nodos ubicados por carril y columna, y flujos.
La disposición es automática: un nodo ocupa (columna, carril); los flujos son rectos o con un
codo a media distancia entre columnas, de modo que nunca cruzan una tarea. Las tareas con
``dolor=True`` marcan un punto débil de la situación actual (supuesto S7) y salen en rojo claro. En los TO-BE,
las tareas con ``f2=True`` dependen de un módulo propio de la Fase 2 y salen en amarillo.
"""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

SALIDA = Path(__file__).resolve().parent / 'bpmn'

# Geometría (píxeles)
X0, Y0 = 20, 20          # esquina del pool
CABECERA = 30            # ancho de la cabecera rotada del pool y de cada carril
ALTO_CARRIL = 150
PASO = 150               # distancia entre columnas
MARGEN = 55              # espacio entre la cabecera y la columna 0
TAREA = (118, 74)
EVENTO = 36
COMPUERTA = 50


class Nodo:
    def __init__(self, id_, tipo, nombre, carril, col, dolor=False, f2=False):
        self.id, self.tipo, self.nombre = id_, tipo, nombre
        self.carril, self.col, self.dolor, self.f2 = carril, col, dolor, f2
        self.w, self.h = {'tarea': TAREA, 'inicio': (EVENTO, EVENTO), 'fin': (EVENTO, EVENTO),
                          'compuerta': (COMPUERTA, COMPUERTA)}[tipo]
        self.cx = X0 + CABECERA + MARGEN + col * PASO + TAREA[0] / 2
        self.cy = Y0 + carril * ALTO_CARRIL + ALTO_CARRIL / 2
        self.x, self.y = self.cx - self.w / 2, self.cy - self.h / 2


class Proceso:
    def __init__(self, id_, titulo, carriles):
        self.id, self.titulo, self.carriles = id_, titulo, carriles
        self.nodos, self.flujos, self.salidas = {}, [], {}

    def nodo(self, id_, tipo, nombre, carril, col, dolor=False, f2=False):
        self.nodos[id_] = Nodo(id_, tipo, nombre, self.carriles.index(carril), col, dolor, f2)

    def flujo(self, origen, destino, etiqueta='', salida='derecha'):
        """``salida``: lado del nodo de origen por donde sale el flujo ('derecha', 'abajo' o 'arriba')."""
        self.flujos.append((origen, destino, etiqueta))
        self.salidas[(origen, destino)] = salida

    # ---- geometría ----
    def ancho(self):
        columnas = max(n.col for n in self.nodos.values()) + 1
        return CABECERA + MARGEN + columnas * PASO + 10

    def alto(self):
        return len(self.carriles) * ALTO_CARRIL

    def ruta(self, origen, destino):
        a, b = self.nodos[origen], self.nodos[destino]
        if a.col == b.col:  # vertical
            if b.cy > a.cy:
                return [(a.cx, a.y + a.h), (b.cx, b.y)]
            return [(a.cx, a.y), (b.cx, b.y + b.h)]
        q = (b.x, b.cy)
        salida = self.salidas.get((origen, destino), 'derecha')
        if salida in ('abajo', 'arriba'):   # sale por la punta de la compuerta y llega por la izquierda
            return [(a.cx, a.y + a.h if salida == 'abajo' else a.y), (a.cx, q[1]), q]
        p = (a.x + a.w, a.cy)
        if abs(p[1] - q[1]) < 1:
            return [p, q]
        codo = q[0] - (PASO - TAREA[0]) / 2   # en el hueco justo antes del destino
        return [p, (codo, p[1]), (codo, q[1]), q]

    def validar(self):
        """Ningún tramo horizontal o vertical de un flujo debe atravesar otro nodo."""
        for origen, destino, _ in self.flujos:
            pts = self.ruta(origen, destino)
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                for n in self.nodos.values():
                    if n.id in (origen, destino):
                        continue
                    if (min(x1, x2) < n.x + n.w and max(x1, x2) > n.x
                            and min(y1, y2) < n.y + n.h and max(y1, y2) > n.y):
                        raise ValueError(f'{self.id}: el flujo {origen}→{destino} atraviesa {n.id}')


# ----------------------------------------------------------------------------- procesos

def venta_b2b():
    p = Proceso('as_is_venta_b2b', 'AS-IS · Venta a cliente B2B (autoservicio o distribuidor)',
                ['Cliente', 'Vendedor', 'Jefe de Ventas', 'Facturación', 'Almacén'])
    p.nodo('inicio', 'inicio', 'Necesita reponer productos', 'Cliente', 0)
    p.nodo('pedido', 'tarea', 'Envía el pedido por correo o teléfono', 'Cliente', 1)
    p.nodo('anota', 'tarea', 'Anota el pedido en Excel y calcula el precio', 'Vendedor', 2, dolor=True)
    p.nodo('especial', 'compuerta', '¿Pide descuento o crédito?', 'Vendedor', 3)
    p.nodo('aprueba', 'tarea', 'Aprueba por correo, sin registro', 'Jefe de Ventas', 4, dolor=True)
    p.nodo('factura', 'tarea', 'Vuelve a digitar el pedido y emite la factura', 'Facturación', 5, dolor=True)
    p.nodo('prepara', 'tarea', 'Prepara el despacho con hoja impresa, sin ver vencimientos', 'Almacén', 6, dolor=True)
    p.nodo('entrega', 'tarea', 'Entrega con guía de remisión en papel', 'Almacén', 7)
    p.nodo('recibe', 'tarea', 'Recibe y firma la guía', 'Cliente', 8)
    p.nodo('cobra', 'tarea', 'Cobra y concilia a fin de mes en Excel', 'Facturación', 9, dolor=True)
    p.nodo('fin', 'fin', 'Pedido cerrado', 'Facturación', 10)
    p.flujo('inicio', 'pedido')
    p.flujo('pedido', 'anota')
    p.flujo('anota', 'especial')
    p.flujo('especial', 'aprueba', 'Sí', salida='abajo')
    p.flujo('especial', 'factura', 'No')
    p.flujo('aprueba', 'factura')
    p.flujo('factura', 'prepara')
    p.flujo('prepara', 'entrega')
    p.flujo('entrega', 'recibe')
    p.flujo('recibe', 'cobra')
    p.flujo('cobra', 'fin')
    return p


def liquidacion_heladero():
    p = Proceso('as_is_liquidacion_heladero', 'AS-IS · Liquidación diaria del heladero',
                ['Heladero', 'Despachador', 'Liquidador', 'Caja'])
    p.nodo('inicio', 'inicio', 'Inicio de la jornada', 'Heladero', 0)
    p.nodo('pide', 'tarea', 'Pide su carga de helados del día', 'Heladero', 1)
    p.nodo('entrega', 'tarea', 'Entrega los helados y anota en el cuaderno', 'Despachador', 2, dolor=True)
    p.nodo('ruta', 'tarea', 'Sale a la ruta y vende', 'Heladero', 3)
    p.nodo('vuelve', 'tarea', 'Regresa y entrega el sobrante y el efectivo', 'Heladero', 4)
    p.nodo('cuenta', 'tarea', 'Cuenta lo devuelto y calcula lo vendido a mano', 'Liquidador', 5, dolor=True)
    p.nodo('cuadra', 'compuerta', '¿El efectivo cuadra?', 'Liquidador', 6)
    p.nodo('cuaderno', 'tarea', 'Anota el descuadre y lo descuenta al día siguiente', 'Liquidador', 7, dolor=True)
    p.nodo('deposita', 'tarea', 'Recibe el efectivo y emite recibo', 'Caja', 7)
    p.nodo('excel', 'tarea', 'Pasa la liquidación a Excel al cierre', 'Liquidador', 8, dolor=True)
    p.nodo('fin', 'fin', 'Liquidación cerrada', 'Liquidador', 9)
    p.flujo('inicio', 'pide')
    p.flujo('pide', 'entrega')
    p.flujo('entrega', 'ruta')
    p.flujo('ruta', 'vuelve')
    p.flujo('vuelve', 'cuenta')
    p.flujo('cuenta', 'cuadra')
    p.flujo('cuadra', 'cuaderno', 'No')
    p.flujo('cuadra', 'deposita', 'Sí', salida='abajo')
    p.flujo('cuaderno', 'deposita')
    p.flujo('deposita', 'excel')
    p.flujo('excel', 'fin')
    return p


def compra_insumos():
    p = Proceso('as_is_compras_insumos', 'AS-IS · Compra de insumos',
                ['Almacén', 'Compras', 'Gerencia', 'Proveedor', 'Finanzas'])
    p.nodo('inicio', 'inicio', 'Baja el stock de un insumo', 'Almacén', 0)
    p.nodo('revisa', 'tarea', 'Revisa el stock a simple vista y detecta el faltante', 'Almacén', 1, dolor=True)
    p.nodo('pide', 'tarea', 'Pide la compra por correo a Compras', 'Almacén', 2)
    p.nodo('cotiza', 'tarea', 'Pide cotizaciones por teléfono y correo', 'Compras', 3)
    p.nodo('envia', 'tarea', 'Envía su cotización', 'Proveedor', 4)
    p.nodo('compara', 'tarea', 'Compara en Excel y elige proveedor', 'Compras', 5, dolor=True)
    p.nodo('firma', 'tarea', 'Firma la aprobación en papel', 'Gerencia', 6, dolor=True)
    p.nodo('oc', 'tarea', 'Emite la orden de compra en Word y la envía', 'Compras', 7, dolor=True)
    p.nodo('entrega', 'tarea', 'Entrega los insumos con guía y factura', 'Proveedor', 8)
    p.nodo('recibe', 'tarea', 'Recibe y firma la guía, sin registrar lote ni vencimiento', 'Almacén', 9, dolor=True)
    p.nodo('digita', 'tarea', 'Digita la factura del proveedor y programa el pago', 'Finanzas', 10, dolor=True)
    p.nodo('fin', 'fin', 'Compra cerrada', 'Finanzas', 11)
    for a, b in [('inicio', 'revisa'), ('revisa', 'pide'), ('pide', 'cotiza'), ('cotiza', 'envia'),
                 ('envia', 'compara'), ('compara', 'firma'), ('firma', 'oc'), ('oc', 'entrega'),
                 ('entrega', 'recibe'), ('recibe', 'digita'), ('digita', 'fin')]:
        p.flujo(a, b)
    return p


def produccion_calidad():
    p = Proceso('as_is_produccion_calidad', 'AS-IS · Producción y calidad',
                ['Jefe de Producción', 'Calidad', 'Operario de línea', 'Almacén'])
    p.nodo('inicio', 'inicio', 'Llega la demanda del mes o de la campaña', 'Jefe de Producción', 0)
    p.nodo('programa', 'tarea', 'Programa la producción en Excel y imprime la orden', 'Jefe de Producción', 1, dolor=True)
    p.nodo('insumos', 'tarea', 'Entrega los insumos con un vale de papel, sin lote ni vencimiento', 'Almacén', 2, dolor=True)
    p.nodo('produce', 'tarea', 'Produce siguiendo la fórmula impresa', 'Operario de línea', 3)
    p.nodo('anota', 'tarea', 'Anota a mano las temperaturas de cada etapa (80-85 °C)', 'Operario de línea', 4, dolor=True)
    p.nodo('inspecciona', 'tarea', 'Inspecciona una muestra y llena el formato en papel', 'Calidad', 5, dolor=True)
    p.nodo('cumple', 'compuerta', '¿El lote cumple?', 'Calidad', 6)
    p.nodo('decide', 'tarea', 'Decide a criterio si se reprocesa o se descarta, sin registro', 'Calidad', 7, dolor=True)
    p.nodo('fin_no', 'fin', 'Lote reprocesado o descartado', 'Calidad', 8)
    p.nodo('etiqueta', 'tarea', 'Etiqueta el lote con un código manual y lo envía al almacén', 'Operario de línea', 7, dolor=True)
    p.nodo('kardex', 'tarea', 'Registra la entrada en el kárdex de Excel', 'Almacén', 8, dolor=True)
    p.nodo('fin', 'fin', 'Producto terminado en almacén', 'Almacén', 9)
    for a_, b_ in [('inicio', 'programa'), ('programa', 'insumos'), ('insumos', 'produce'), ('produce', 'anota'),
                   ('anota', 'inspecciona'), ('inspecciona', 'cumple')]:
        p.flujo(a_, b_)
    p.flujo('cumple', 'decide', 'No')
    p.flujo('cumple', 'etiqueta', 'Sí', salida='abajo')
    p.flujo('decide', 'fin_no')
    p.flujo('etiqueta', 'kardex')
    p.flujo('kardex', 'fin')
    return p


def recepcion_despacho_frio():
    p = Proceso('as_is_recepcion_despacho_frio', 'AS-IS · Recepción y despacho con cadena de frío',
                ['Proveedor', 'Cámara de frío', 'Almacén', 'Despacho', 'Cliente o CD Arequipa'])
    p.nodo('inicio', 'inicio', 'Llega el camión con insumos', 'Proveedor', 0)
    p.nodo('recibe', 'tarea', 'Descarga y recibe con la guía, sin registrar lote ni vencimiento', 'Almacén', 1, dolor=True)
    p.nodo('guarda', 'tarea', 'Guarda el producto en la cámara que corresponde', 'Cámara de frío', 2)
    p.nodo('temperatura', 'tarea', 'Anota la temperatura en una planilla de papel, dos veces al día', 'Cámara de frío', 3, dolor=True)
    p.nodo('rango', 'compuerta', '¿Fuera de rango?', 'Cámara de frío', 4)
    p.nodo('avisa', 'tarea', 'Detecta tarde el problema y avisa por llamada al jefe', 'Almacén', 5, dolor=True)
    p.nodo('kardex', 'tarea', 'Registra salidas y saldos en el kárdex de Excel', 'Almacén', 6, dolor=True)
    p.nodo('prepara', 'tarea', 'Prepara el pedido revisando las fechas a ojo, sin FEFO', 'Despacho', 7, dolor=True)
    p.nodo('despacha', 'tarea', 'Despacha con guía en papel; Arequipa se coordina por teléfono', 'Despacho', 8, dolor=True)
    p.nodo('recibe_cliente', 'tarea', 'Recibe la mercadería y firma la guía', 'Cliente o CD Arequipa', 9)
    p.nodo('fin', 'fin', 'Entrega cerrada', 'Cliente o CD Arequipa', 10)
    for a_, b_ in [('inicio', 'recibe'), ('recibe', 'guarda'), ('guarda', 'temperatura'), ('temperatura', 'rango')]:
        p.flujo(a_, b_)
    p.flujo('rango', 'avisa', 'Sí', salida='abajo')
    p.flujo('rango', 'kardex', 'No')
    for a_, b_ in [('avisa', 'kardex'), ('kardex', 'prepara'), ('prepara', 'despacha'),
                   ('despacha', 'recibe_cliente'), ('recibe_cliente', 'fin')]:
        p.flujo(a_, b_)
    return p


# ----------------------------------------------------------------------------- procesos TO-BE (Sprint 2)

def to_be_produccion():
    """Fase 1: orden de producción de Odoo con FEFO, lote, costo y controles en las operaciones."""
    p = Proceso('to_be_produccion', 'TO-BE · Producción con Odoo estándar (Fase 1)',
                ['Operario de línea', 'Jefe de Producción', 'Almacén'])
    p.nodo('inicio', 'inicio', 'Llega la demanda del mes o de la campaña', 'Jefe de Producción', 0)
    p.nodo('op', 'tarea', 'Crea la orden de producción desde la receta (BoM) y la confirma', 'Jefe de Producción', 1)
    p.nodo('reserva', 'tarea', 'Odoo reserva los insumos por FEFO: sale primero el lote que vence antes', 'Almacén', 2)
    p.nodo('entrega', 'tarea', 'Entrega los insumos reservados a la línea', 'Almacén', 3)
    p.nodo('produce', 'tarea', 'Ejecuta cada operación en su centro de trabajo y registra el tiempo', 'Operario de línea', 4)
    p.nodo('controla', 'tarea', 'Verifica los controles críticos de la operación y los anota en la orden', 'Operario de línea', 5)
    p.nodo('cumple', 'compuerta', '¿Cumple los controles?', 'Operario de línea', 6)
    p.nodo('hecho', 'tarea', 'Marca la orden como hecha: Odoo crea el lote con vencimiento y calcula el costo', 'Operario de línea', 7)
    p.nodo('decide', 'tarea', 'Decide reproceso o descarte y lo deja escrito en la orden', 'Jefe de Producción', 7)
    p.nodo('fin_no', 'fin', 'Lote reprocesado o descartado', 'Jefe de Producción', 8)
    p.nodo('stock', 'tarea', 'El lote entra a Lima/Stock listo para salir por FEFO', 'Almacén', 9)
    p.nodo('fin', 'fin', 'Producto terminado en almacén', 'Almacén', 10)
    for a_, b_ in [('inicio', 'op'), ('op', 'reserva'), ('reserva', 'entrega'), ('entrega', 'produce'),
                   ('produce', 'controla'), ('controla', 'cumple')]:
        p.flujo(a_, b_)
    p.flujo('cumple', 'hecho', 'Sí')
    p.flujo('cumple', 'decide', 'No', salida='abajo')
    p.flujo('decide', 'fin_no')
    p.flujo('hecho', 'stock')
    p.flujo('stock', 'fin')
    return p


def to_be_produccion_m1():
    """Con el módulo M1 (Fase 2): inspección ligada a la OP y al lote, bloqueo y certificado."""
    p = Proceso('to_be_produccion_m1', 'TO-BE · Producción con inspección de calidad (M1, Fase 2)',
                ['Operario de línea', 'Almacén', 'Inspector de Calidad', 'Jefe de Producción'])
    p.nodo('inicio', 'inicio', 'Llega la demanda del mes o de la campaña', 'Jefe de Producción', 0)
    p.nodo('op', 'tarea', 'Crea la orden desde la receta y Odoo reserva los insumos por FEFO', 'Jefe de Producción', 1)
    p.nodo('produce', 'tarea', 'Ejecuta las operaciones y registra los tiempos', 'Operario de línea', 2)
    p.nodo('termina', 'tarea', 'Termina la orden: Odoo crea el lote con su vencimiento', 'Operario de línea', 3)
    p.nodo('inspeccion', 'tarea', 'Se crea la inspección ligada a la orden y al lote', 'Inspector de Calidad', 4, f2=True)
    p.nodo('mide', 'tarea', 'Mide en cada punto de control (pasteurización, peso, microbiología)', 'Inspector de Calidad', 5, f2=True)
    p.nodo('aprueba', 'compuerta', '¿Aprueba el lote?', 'Inspector de Calidad', 6)
    p.nodo('certifica', 'tarea', 'Emite el certificado de calidad del lote', 'Inspector de Calidad', 7, f2=True)
    p.nodo('rechaza', 'tarea', 'Lote rechazado: Odoo bloquea su despacho; el jefe decide su destino', 'Jefe de Producción', 7, f2=True)
    p.nodo('fin_no', 'fin', 'Lote reprocesado o descartado', 'Jefe de Producción', 8)
    p.nodo('libera', 'tarea', 'El lote liberado queda disponible para el despacho FEFO', 'Almacén', 8)
    p.nodo('fin', 'fin', 'Lote liberado en almacén', 'Almacén', 9)
    for a_, b_ in [('inicio', 'op'), ('op', 'produce'), ('produce', 'termina'), ('termina', 'inspeccion'),
                   ('inspeccion', 'mide'), ('mide', 'aprueba')]:
        p.flujo(a_, b_)
    p.flujo('aprueba', 'certifica', 'Sí')
    p.flujo('aprueba', 'rechaza', 'No', salida='abajo')
    p.flujo('rechaza', 'fin_no')
    p.flujo('certifica', 'libera')
    p.flujo('libera', 'fin')
    return p


def to_be_recepcion_despacho():
    """Fase 1: recepción desde la OC con lote, despacho en 2 pasos y reposición a Arequipa."""
    p = Proceso('to_be_recepcion_despacho', 'TO-BE · Recepción y despacho con Odoo estándar (Fase 1)',
                ['Proveedor', 'Almacén', 'Despacho', 'Cliente', 'CD Arequipa'])
    p.nodo('inicio', 'inicio', 'Llega el camión con una orden de compra confirmada', 'Proveedor', 0)
    p.nodo('recibe', 'tarea', 'Recibe contra la recepción que creó la OC y escribe lote y vencimiento', 'Almacén', 1)
    p.nodo('guarda', 'tarea', 'Odoo guarda el lote en su cámara y valoriza el stock por FIFO', 'Almacén', 2)
    p.nodo('alerta', 'tarea', 'Odoo avisa al jefe de almacén 30 días antes de que el lote venza', 'Almacén', 3)
    p.nodo('pedido', 'tarea', 'Llega un pedido confirmado o una reposición a Arequipa', 'Despacho', 4)
    p.nodo('pick', 'tarea', 'Pick: Odoo reserva por FEFO y arma la lista de recolección', 'Despacho', 5)
    p.nodo('ship', 'tarea', 'Ship: verifica el pick, despacha desde la zona de salida y emite la guía', 'Despacho', 6)
    p.nodo('destino', 'compuerta', '¿Quién recibe?', 'Despacho', 7)
    p.nodo('cliente', 'tarea', 'El cliente recibe y firma la entrega', 'Cliente', 8)
    p.nodo('transito', 'tarea', 'El CD Arequipa recibe la transferencia y el stock queda en AQP', 'CD Arequipa', 8)
    p.nodo('fin', 'fin', 'Entrega cerrada', 'Cliente', 9)
    for a_, b_ in [('inicio', 'recibe'), ('recibe', 'guarda'), ('guarda', 'alerta'), ('alerta', 'pedido'),
                   ('pedido', 'pick'), ('pick', 'ship'), ('ship', 'destino')]:
        p.flujo(a_, b_)
    p.flujo('destino', 'cliente', 'Cliente')
    p.flujo('destino', 'transito', 'Arequipa', salida='abajo')
    p.flujo('cliente', 'fin')
    p.flujo('transito', 'fin')
    return p


PROCESOS = {
    'as-is_venta_b2b': venta_b2b,
    'as-is_liquidacion_heladero': liquidacion_heladero,
    'as-is_compras_insumos': compra_insumos,
    'as-is_produccion_calidad': produccion_calidad,
    'as-is_recepcion_despacho_frio': recepcion_despacho_frio,
    'to-be_produccion': to_be_produccion,
    'to-be_produccion_m1': to_be_produccion_m1,
    'to-be_recepcion_despacho': to_be_recepcion_despacho,
}

# ----------------------------------------------------------------------------- BPMN 2.0 XML

def _f(v):
    return f'{v:.0f}'


def pos_etiqueta(p, origen, destino):
    """Posición (x, y) de la esquina superior izquierda de la etiqueta «Sí»/«No» de un flujo."""
    pts = p.ruta(origen, destino)
    salida = p.salidas.get((origen, destino), 'derecha')
    if salida == 'abajo':
        return pts[0][0] + 6, pts[0][1] + 4
    if salida == 'arriba':
        return pts[0][0] + 6, pts[0][1] - 18
    return pts[0][0] + 6, pts[0][1] - 20


def a_bpmn(p):
    ids_flujo = {(o, d): f'flujo_{i}' for i, (o, d, _) in enumerate(p.flujos, 1)}
    entra = {n: [] for n in p.nodos}
    sale = {n: [] for n in p.nodos}
    for o, d, _ in p.flujos:
        sale[o].append(ids_flujo[(o, d)])
        entra[d].append(ids_flujo[(o, d)])
    etiqueta = {'tarea': 'task', 'inicio': 'startEvent', 'fin': 'endEvent', 'compuerta': 'exclusiveGateway'}

    x = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"'
        ' xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"'
        ' xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"'
        ' xmlns:di="http://www.omg.org/spec/DD/20100524/DI"'
        ' xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0"'
        f' id="def_{p.id}" targetNamespace="http://bpmn.io/schema/bpmn">',
        f'  <bpmn:collaboration id="colab_{p.id}">',
        f'    <bpmn:participant id="pool_{p.id}" name={quoteattr(p.titulo)} processRef="proc_{p.id}" />',
        '  </bpmn:collaboration>',
        f'  <bpmn:process id="proc_{p.id}" isExecutable="false">',
        '    <bpmn:laneSet id="carriles">',
    ]
    for i, c in enumerate(p.carriles):
        x.append(f'      <bpmn:lane id="carril_{i}" name={quoteattr(c)}>')
        x += [f'        <bpmn:flowNodeRef>{n.id}</bpmn:flowNodeRef>' for n in p.nodos.values() if n.carril == i]
        x.append('      </bpmn:lane>')
    x.append('    </bpmn:laneSet>')
    for n in p.nodos.values():
        x.append(f'    <bpmn:{etiqueta[n.tipo]} id="{n.id}" name={quoteattr(n.nombre)}>')
        x += [f'      <bpmn:incoming>{f}</bpmn:incoming>' for f in entra[n.id]]
        x += [f'      <bpmn:outgoing>{f}</bpmn:outgoing>' for f in sale[n.id]]
        x.append(f'    </bpmn:{etiqueta[n.tipo]}>')
    for o, d, et in p.flujos:
        nombre = f' name={quoteattr(et)}' if et else ''
        x.append(f'    <bpmn:sequenceFlow id="{ids_flujo[(o, d)]}"{nombre} sourceRef="{o}" targetRef="{d}" />')
    x += ['  </bpmn:process>', '  <bpmndi:BPMNDiagram id="diagrama">',
          f'    <bpmndi:BPMNPlane id="plano" bpmnElement="colab_{p.id}">',
          f'      <bpmndi:BPMNShape id="pool_{p.id}_di" bpmnElement="pool_{p.id}" isHorizontal="true">',
          f'        <dc:Bounds x="{X0}" y="{Y0}" width="{_f(p.ancho())}" height="{_f(p.alto())}" />',
          '      </bpmndi:BPMNShape>']
    for i, _ in enumerate(p.carriles):
        x += [f'      <bpmndi:BPMNShape id="carril_{i}_di" bpmnElement="carril_{i}" isHorizontal="true">',
              f'        <dc:Bounds x="{X0 + CABECERA}" y="{Y0 + i * ALTO_CARRIL}"'
              f' width="{_f(p.ancho() - CABECERA)}" height="{ALTO_CARRIL}" />',
              '      </bpmndi:BPMNShape>']
    for n in p.nodos.values():
        color = ' bioc:fill="#fde0dc" bioc:stroke="#c0392b"' if n.dolor else ''
        marca = ' isMarkerVisible="true"' if n.tipo == 'compuerta' else ''
        x += [f'      <bpmndi:BPMNShape id="{n.id}_di" bpmnElement="{n.id}"{marca}{color}>',
              f'        <dc:Bounds x="{_f(n.x)}" y="{_f(n.y)}" width="{_f(n.w)}" height="{_f(n.h)}" />']
        if n.tipo != 'tarea':
            ly = n.y + n.h + 4 if n.tipo != 'compuerta' else n.y - 34
            x += ['        <bpmndi:BPMNLabel>',
                  f'          <dc:Bounds x="{_f(n.cx - 60)}" y="{_f(ly)}" width="120" height="30" />',
                  '        </bpmndi:BPMNLabel>']
        x.append('      </bpmndi:BPMNShape>')
    for o, d, et in p.flujos:
        x.append(f'      <bpmndi:BPMNEdge id="{ids_flujo[(o, d)]}_di" bpmnElement="{ids_flujo[(o, d)]}">')
        pts = p.ruta(o, d)
        x += [f'        <di:waypoint x="{_f(px)}" y="{_f(py)}" />' for px, py in pts]
        if et:
            x += ['        <bpmndi:BPMNLabel>',
                  '          <dc:Bounds x="{}" y="{}" width="22" height="14" />'.format(*map(_f, pos_etiqueta(p, o, d))),
                  '        </bpmndi:BPMNLabel>']
        x.append('      </bpmndi:BPMNEdge>')
    x += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</bpmn:definitions>', '']
    return '\n'.join(x)


# ----------------------------------------------------------------------------- SVG

def partir(texto, ancho=17):
    lineas, actual = [], ''
    for palabra in texto.split():
        if actual and len(actual) + 1 + len(palabra) > ancho:
            lineas.append(actual)
            actual = palabra
        else:
            actual = f'{actual} {palabra}'.strip()
    return lineas + [actual]


def texto_svg(cx, cy, lineas, tam=11, peso='normal', ancla='middle'):
    alto = tam + 2
    y0 = cy - (len(lineas) - 1) * alto / 2 + tam * 0.35
    return ''.join(
        f'<text x="{cx:.0f}" y="{y0 + i * alto:.0f}" text-anchor="{ancla}" font-size="{tam}" '
        f'font-weight="{peso}">{escape(l)}</text>' for i, l in enumerate(lineas))


def a_svg(p):
    ancho, alto = p.ancho() + 2 * X0, p.alto() + 2 * Y0 + 38
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho:.0f}" height="{alto:.0f}" '
         f'viewBox="0 0 {ancho:.0f} {alto:.0f}" font-family="DejaVu Sans, Arial, sans-serif">',
         '<defs><marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker></defs>',
         f'<rect width="{ancho:.0f}" height="{alto:.0f}" fill="#fff"/>',
         f'<rect x="{X0}" y="{Y0}" width="{p.ancho():.0f}" height="{p.alto()}" fill="none" stroke="#222" stroke-width="1.5"/>',
         f'<line x1="{X0 + CABECERA}" y1="{Y0}" x2="{X0 + CABECERA}" y2="{Y0 + p.alto()}" stroke="#222"/>',
         f'<g transform="rotate(-90 {X0 + 15} {Y0 + p.alto() / 2})">'
         + texto_svg(X0 + 15, Y0 + p.alto() / 2, [p.titulo], 12, 'bold') + '</g>']
    for i, c in enumerate(p.carriles):
        y = Y0 + i * ALTO_CARRIL
        if i:
            s.append(f'<line x1="{X0 + CABECERA}" y1="{y}" x2="{X0 + p.ancho():.0f}" y2="{y}" stroke="#222"/>')
        s.append(f'<line x1="{X0 + CABECERA + 22}" y1="{y}" x2="{X0 + CABECERA + 22}" y2="{y + ALTO_CARRIL}" stroke="#222"/>')
        s.append(f'<g transform="rotate(-90 {X0 + CABECERA + 11} {y + ALTO_CARRIL / 2})">'
                 + texto_svg(X0 + CABECERA + 11, y + ALTO_CARRIL / 2, [c], 11, 'bold') + '</g>')
    for o, d, et in p.flujos:
        pts = p.ruta(o, d)
        s.append('<polyline fill="none" stroke="#222" stroke-width="1.4" marker-end="url(#flecha)" points="'
                 + ' '.join(f'{px:.0f},{py:.0f}' for px, py in pts) + '"/>')
        if et:
            lx, ly = pos_etiqueta(p, o, d)
            s.append(f'<text x="{lx:.0f}" y="{ly + 11:.0f}" font-size="11" font-weight="bold">{escape(et)}</text>')
    for n in p.nodos.values():
        if n.tipo == 'tarea':
            relleno, borde = ('#fde0dc', '#c0392b') if n.dolor else ('#fff3c4', '#b7950b') if n.f2 else ('#f4f7fb', '#222')
            s.append(f'<rect x="{n.x:.0f}" y="{n.y:.0f}" width="{n.w}" height="{n.h}" rx="8" fill="{relleno}" '
                     f'stroke="{borde}" stroke-width="1.5"/>' + texto_svg(n.cx, n.cy, partir(n.nombre)))
        elif n.tipo == 'compuerta':
            s.append(f'<polygon points="{n.cx:.0f},{n.y:.0f} {n.x + n.w:.0f},{n.cy:.0f} {n.cx:.0f},{n.y + n.h:.0f} '
                     f'{n.x:.0f},{n.cy:.0f}" fill="#fff8e1" stroke="#222" stroke-width="1.5"/>'
                     f'<path d="M{n.cx - 9:.0f},{n.cy - 9:.0f} L{n.cx + 9:.0f},{n.cy + 9:.0f} M{n.cx + 9:.0f},{n.cy - 9:.0f} '
                     f'L{n.cx - 9:.0f},{n.cy + 9:.0f}" stroke="#222" stroke-width="2.5"/>'
                     + texto_svg(n.cx, n.y - 20, partir(n.nombre, 22), 11, 'bold'))
        else:
            grosor = 1.5 if n.tipo == 'inicio' else 4
            s.append(f'<circle cx="{n.cx:.0f}" cy="{n.cy:.0f}" r="{n.w / 2}" fill="#e8f5e9" stroke="#222" '
                     f'stroke-width="{grosor}"/>' + texto_svg(n.cx, n.cy + n.h / 2 + 18, partir(n.nombre, 22)))
    ly = Y0 + p.alto() + 28
    if any(n.dolor for n in p.nodos.values()):
        s.append(f'<rect x="{X0}" y="{ly - 12}" width="16" height="14" rx="3" fill="#fde0dc" stroke="#c0392b"/>'
                 f'<text x="{X0 + 24}" y="{ly}" font-size="11">Punto débil de la situación actual (supuesto S7 del plan: '
                 'los datos de procesos son ficticios y verosímiles)</text>')
    else:
        s.append(f'<rect x="{X0}" y="{ly - 12}" width="16" height="14" rx="3" fill="#f4f7fb" stroke="#222"/>'
                 f'<text x="{X0 + 24}" y="{ly}" font-size="11">Tarea con Odoo estándar (Fase 1)</text>')
        if any(n.f2 for n in p.nodos.values()):
            s.append(f'<rect x="{X0 + 230}" y="{ly - 12}" width="16" height="14" rx="3" fill="#fff3c4" stroke="#b7950b"/>'
                     f'<text x="{X0 + 254}" y="{ly}" font-size="11">Depende del módulo propio de la Fase 2 '
                     '(si no se construye, queda como diseño)</text>')
    s.append('</svg>')
    return '\n'.join(s)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for nombre, fabrica in PROCESOS.items():
        p = fabrica()
        p.validar()
        (SALIDA / f'{nombre}.bpmn').write_text(a_bpmn(p), encoding='utf-8')
        (SALIDA / f'{nombre}.svg').write_text(a_svg(p), encoding='utf-8')
        print(f'{nombre}: {len(p.nodos)} nodos, {len(p.flujos)} flujos, {p.ancho() + 2 * X0:.0f}x{p.alto() + 2 * Y0 + 38:.0f}')


if __name__ == '__main__':
    main()
