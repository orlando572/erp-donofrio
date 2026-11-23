#!/usr/bin/env python3
"""Genera los BPMN AS-IS de Evelyn (Sprint 1) como archivo .bpmn (editable en bpmn.io) y .svg.

Uso:  python3 docs/diagramas/generar_bpmn.py        (escribe en docs/diagramas/bpmn/)
El PNG se obtiene del SVG (ver docs/diagramas/README.md).

Cada proceso se describe con carriles (roles), nodos ubicados por carril y columna, y flujos.
La disposición es automática: un nodo ocupa (columna, carril); los flujos son rectos o con un
codo a media distancia entre columnas, de modo que nunca cruzan una tarea. Las tareas con
``dolor=True`` marcan un punto débil de la situación actual (supuesto S7) y salen en rojo claro.
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
    def __init__(self, id_, tipo, nombre, carril, col, dolor=False):
        self.id, self.tipo, self.nombre = id_, tipo, nombre
        self.carril, self.col, self.dolor = carril, col, dolor
        self.w, self.h = {'tarea': TAREA, 'inicio': (EVENTO, EVENTO), 'fin': (EVENTO, EVENTO),
                          'compuerta': (COMPUERTA, COMPUERTA)}[tipo]
        self.cx = X0 + CABECERA + MARGEN + col * PASO + TAREA[0] / 2
        self.cy = Y0 + carril * ALTO_CARRIL + ALTO_CARRIL / 2
        self.x, self.y = self.cx - self.w / 2, self.cy - self.h / 2


class Proceso:
    def __init__(self, id_, titulo, carriles):
        self.id, self.titulo, self.carriles = id_, titulo, carriles
        self.nodos, self.flujos, self.salidas = {}, [], {}

    def nodo(self, id_, tipo, nombre, carril, col, dolor=False):
        self.nodos[id_] = Nodo(id_, tipo, nombre, self.carriles.index(carril), col, dolor)

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


PROCESOS = {
    'as-is_venta_b2b': venta_b2b,
    'as-is_liquidacion_heladero': liquidacion_heladero,
    'as-is_compras_insumos': compra_insumos,
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
            relleno, borde = ('#fde0dc', '#c0392b') if n.dolor else ('#f4f7fb', '#222')
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
    s.append(f'<rect x="{X0}" y="{ly - 12}" width="16" height="14" rx="3" fill="#fde0dc" stroke="#c0392b"/>'
             f'<text x="{X0 + 24}" y="{ly}" font-size="11">Punto débil de la situación actual (supuesto S7 del plan: '
             'los datos de procesos son ficticios y verosímiles)</text>')
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
