#!/usr/bin/env python3
"""Genera los wireframes (4.4.1) y mockups (4.4.2) de las pantallas de los casos de uso como .svg.

Uso:  python3 docs/diagramas/generar_pantallas.py        (escribe en docs/diagramas/pantallas/)
El PNG se obtiene del SVG (ver docs/diagramas/README.md).

Cada pantalla se describe una sola vez, como una pila de componentes (barra de estado, botones,
campos, tabla, kanban, tarjetas de KPI, gráfico...). De esa misma descripción salen dos versiones:

* ``wf_*``: wireframe en escala de grises, sin marca, para acordar la estructura.
* ``mk_*``: mockup en alta fidelidad con la paleta de marca (amarillo de los carritos, 1919).

Los datos que aparecen son ficticios y verosímiles (supuesto S7 del plan). Las pantallas con
``f2=True`` dependen de un módulo propio de la Fase 2: se diseñaron en la F1 y se implementaron en la F2.
"""
from pathlib import Path
from xml.sax.saxutils import escape

SALIDA = Path(__file__).resolve().parent / 'pantallas'

# Paleta del mockup (el amarillo es el de los carritos de D'Onofrio)
AMARILLO, AMARILLO_CLARO, TINTA = '#F7C60A', '#FFF3C4', '#2B2B2B'
AMARILLO_OSCURO = '#9A6B00'      # amarillo de los títulos de reporte (contraste sobre blanco)
FONDO, BORDE, GRIS = '#F4F5F7', '#D5D9DF', '#5C6370'
VERDE, ROJO, AZUL = '#2E7D32', '#C0392B', '#1565C0'


class Estilo:
    """Colores de cada modo; el wireframe usa solo grises."""

    def __init__(self, mockup):
        self.mockup = mockup
        self.marca = AMARILLO if mockup else '#DDDDDD'
        self.marca_clara = AMARILLO_CLARO if mockup else '#EEEEEE'
        self.tinta = TINTA if mockup else '#333333'
        self.fondo = FONDO if mockup else '#FFFFFF'
        self.borde = BORDE if mockup else '#888888'
        self.gris = GRIS if mockup else '#777777'
        self.ok = VERDE if mockup else '#555555'
        self.mal = ROJO if mockup else '#555555'
        self.info = AZUL if mockup else '#555555'
        self.fuente = "'DejaVu Sans', Arial, sans-serif"


def t(x, y, texto, e, tam=11, peso='normal', color=None, ancla='start'):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{tam}" font-weight="{peso}" text-anchor="{ancla}" '
            f'fill="{color or e.tinta}">{escape(str(texto))}</text>')


def caja(x, y, w, h, e, relleno=None, borde=None, rx=4, dash=False):
    d = ' stroke-dasharray="4 3"' if dash else ''
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" '
            f'fill="{relleno or "#fff"}" stroke="{borde or e.borde}" stroke-width="1"{d}/>')


# ----------------------------------------------------------------------------- componentes
# Cada uno devuelve (svg, alto) y dibuja desde (x, y) con ancho w.

def c_estado(x, y, w, e, etapas, activa):
    s, cx = [], x
    for i, nombre in enumerate(etapas):
        ancho = len(nombre) * 6.6 + 24
        on = i == activa
        s.append(caja(cx, y, ancho, 24, e, e.marca if on else '#fff', e.tinta if on else e.borde, rx=12))
        s.append(t(cx + ancho / 2, y + 16, nombre, e, 11, 'bold' if on else 'normal', ancla='middle'))
        cx += ancho + 6
    return ''.join(s), 34


def c_botones(x, y, w, e, nombres, primario=0):
    s, cx = [], x
    for i, nombre in enumerate(nombres):
        ancho = len(nombre) * 6.8 + 26
        on = i == primario
        s.append(caja(cx, y, ancho, 28, e, e.marca if on else '#fff', e.tinta if on else e.borde))
        s.append(t(cx + ancho / 2, y + 18, nombre, e, 11, 'bold' if on else 'normal', ancla='middle'))
        cx += ancho + 8
    return ''.join(s), 40


def c_campos(x, y, w, e, campos, columnas=2):
    s, ancho = [], (w - 24 * (columnas - 1)) / columnas
    filas = -(-len(campos) // columnas)
    for i, (etiqueta, valor) in enumerate(campos):
        cx, cy = x + (i % columnas) * (ancho + 24), y + (i // columnas) * 42
        s.append(t(cx, cy + 10, etiqueta, e, 10, color=e.gris))
        s.append(caja(cx, cy + 15, ancho, 22, e, '#fff'))
        s.append(t(cx + 8, cy + 30, valor, e, 11))
    return ''.join(s), filas * 42 + 6


def c_tabla(x, y, w, e, cabeceras, filas, pesos=None, total=None):
    pesos = pesos or [1] * len(cabeceras)
    suma = sum(pesos)
    anchos = [w * p / suma for p in pesos]
    s = [caja(x, y, w, 26, e, e.marca_clara if e.mockup else '#EEEEEE')]
    cx = x
    for h, a in zip(cabeceras, anchos):
        s.append(t(cx + 8, y + 17, h, e, 10, 'bold'))
        cx += a
    for i, fila in enumerate(filas):
        fy = y + 26 + i * 26
        s.append(caja(x, fy, w, 26, e, '#fff'))
        cx = x
        for v, a in zip(fila, anchos):
            s.append(t(cx + 8, fy + 17, v, e, 11))
            cx += a
    alto = 26 + len(filas) * 26
    if total:
        s.append(t(x + w - 8, y + alto + 18, total, e, 12, 'bold', ancla='end'))
        alto += 26
    return ''.join(s), alto + 10


def c_kanban(x, y, w, e, columnas):
    s, ancho = [], (w - 8 * (len(columnas) - 1)) / len(columnas)
    alto = 0
    for i, (titulo, tarjetas) in enumerate(columnas):
        cx = x + i * (ancho + 8)
        s.append(caja(cx, y, ancho, 26, e, e.marca if e.mockup else '#DDDDDD'))
        s.append(t(cx + ancho / 2, y + 17, titulo, e, 11, 'bold', ancla='middle'))
        for j, (nombre, detalle) in enumerate(tarjetas):
            ty = y + 34 + j * 58
            s.append(caja(cx, ty, ancho, 52, e, '#fff'))
            s.append(t(cx + 8, ty + 20, nombre, e, 11, 'bold'))
            s.append(t(cx + 8, ty + 38, detalle, e, 10, color=e.gris))
        alto = max(alto, 34 + len(tarjetas) * 58)
    return ''.join(s), alto + 6


def c_kpis(x, y, w, e, tarjetas):
    s, ancho = [], (w - 10 * (len(tarjetas) - 1)) / len(tarjetas)
    for i, (titulo, valor, nota) in enumerate(tarjetas):
        cx = x + i * (ancho + 10)
        s.append(caja(cx, y, ancho, 78, e, '#fff'))
        s.append(f'<rect x="{cx:.0f}" y="{y}" width="5" height="78" fill="{e.marca if e.mockup else "#BBBBBB"}"/>')
        s.append(t(cx + 14, y + 20, titulo, e, 10, color=e.gris))
        s.append(t(cx + 14, y + 50, valor, e, 20, 'bold'))
        s.append(t(cx + 14, y + 68, nota, e, 10, color=e.gris))
    return ''.join(s), 90


def c_barras(x, y, w, e, titulo, valores, etiquetas):
    alto = 150
    s = [caja(x, y, w, alto + 40, e, '#fff'), t(x + 12, y + 20, titulo, e, 12, 'bold')]
    maximo = max(valores)
    ancho = (w - 40) / len(valores)
    for i, (v, et) in enumerate(zip(valores, etiquetas)):
        h = (alto - 40) * v / maximo
        bx = x + 20 + i * ancho
        s.append(f'<rect x="{bx + 6:.0f}" y="{y + 30 + (alto - 40 - h):.0f}" width="{ancho - 12:.0f}" height="{h:.0f}" '
                 f'fill="{e.marca if e.mockup else "#BBBBBB"}" stroke="{e.tinta}" stroke-width="0.8"/>')
        s.append(t(bx + ancho / 2, y + alto + 18, et, e, 10, ancla='middle', color=e.gris))
    return ''.join(s), alto + 50


def c_alerta(x, y, w, e, texto, tono='info'):
    color = {'info': e.info, 'ok': e.ok, 'mal': e.mal}[tono]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="4" fill="{"#fff" if not e.mockup else color + "18"}" '
            f'stroke="{color}"/>' + t(x + 12, y + 20, texto, e, 11, color=color)), 40


def c_texto(x, y, w, e, texto, tam=11, peso='normal'):
    return t(x, y + 12, texto, e, tam, peso), 24


def c_pdv(x, y, w, e, productos, lineas, total):
    """Pantalla del punto de venta: rejilla de productos a la izquierda y ticket a la derecha."""
    izq = w * 0.62
    s = []
    ancho = (izq - 24) / 3
    for i, (nombre, precio) in enumerate(productos):
        cx, cy = x + (i % 3) * (ancho + 12), y + (i // 3) * 92
        s.append(caja(cx, cy, ancho, 84, e, e.marca_clara if e.mockup else '#F2F2F2'))
        s.append(caja(cx + ancho / 2 - 18, cy + 8, 36, 28, e, '#fff', dash=not e.mockup))
        s.append(t(cx + ancho / 2, cy + 56, nombre, e, 11, 'bold', ancla='middle'))
        s.append(t(cx + ancho / 2, cy + 72, precio, e, 10, color=e.gris, ancla='middle'))
    dx = x + izq + 12
    dw = w - izq - 12
    alto = (-(-len(productos) // 3)) * 92
    s.append(caja(dx, y, dw, alto, e, '#fff'))
    s.append(t(dx + 10, y + 20, 'Pedido · Cliente varios', e, 11, 'bold'))
    for i, (nombre, importe) in enumerate(lineas):
        s.append(t(dx + 10, y + 46 + i * 20, nombre, e, 11))
        s.append(t(dx + dw - 10, y + 46 + i * 20, importe, e, 11, ancla='end'))
    s.append(t(dx + 10, y + alto - 60, 'Total (IGV incl.)', e, 12, 'bold'))
    s.append(t(dx + dw - 10, y + alto - 60, total, e, 14, 'bold', ancla='end'))
    s.append(caja(dx + 10, y + alto - 44, dw - 20, 34, e, e.marca if e.mockup else '#DDDDDD', e.tinta))
    s.append(t(dx + dw / 2, y + alto - 22, 'Cobrar', e, 13, 'bold', ancla='middle'))
    return ''.join(s), alto + 10


COMPONENTES = {
    'estado': c_estado, 'botones': c_botones, 'campos': c_campos, 'tabla': c_tabla, 'kanban': c_kanban,
    'kpis': c_kpis, 'barras': c_barras, 'alerta': c_alerta, 'texto': c_texto, 'pdv': c_pdv,
}


# ----------------------------------------------------------------------------- pantallas

class Pantalla:
    def __init__(self, id_, cu, titulo, modulo, ruta, partes, ancho=960, f2=False, hu='', reporte=False):
        self.id, self.cu, self.titulo, self.modulo, self.ruta = id_, cu, titulo, modulo, ruta
        self.partes, self.ancho, self.f2, self.hu, self.reporte = partes, ancho, f2, hu, reporte


def p(componente, *args, **kw):
    return (componente, args, kw)


PANTALLAS = [
    Pantalla('cu001_embudo_crm', 'CU001', 'Embudo CRM por canal', 'CRM', 'CRM › Canal Tradicional', hu='HU-08', partes=[
        p('botones', ['Nueva', 'Kanban', 'Lista', 'Pivote'], 0),
        p('kanban', [
            ('Prospecto', [('Bodega La Esquina', 'S/ 4 800 · Canal Tradicional'), ('Minimarket Sol', 'S/ 6 200')]),
            ('Calificado', [('Autoservicio Andino', 'S/ 18 500 · Canal Moderno')]),
            ('Propuesta', [('Distribuidora Sur SAC', 'S/ 42 000'), ('Bodega Don Lucho', 'S/ 3 900')]),
            ('Negociación', [('Supermercado Ejemplo', 'S/ 65 000')]),
            ('Ganado', [('Distribuidora Norte SAC', 'S/ 38 000')]),
        ]),
    ]),
    Pantalla('cu002_cotizacion', 'CU002', 'Cotización con lista de precios', 'Ventas', 'Ventas › Cotizaciones › S00015',
             hu='HU-09', partes=[
        p('estado', ['Cotización', 'Cotización enviada', 'Pedido de venta'], 0),
        p('botones', ['Enviar por correo', 'Confirmar', 'Cancelar'], 1),
        p('campos', [('Cliente', 'Distribuidora Sur SAC'), ('Lista de precios', 'Verano (-10 %)'),
                     ('Fecha', '15/01/2027'), ('Condición de pago', '30 días')]),
        p('tabla', ['Producto', 'Cantidad', 'Precio unit.', 'Impuesto', 'Subtotal'], [
            ['Paleta de fresa', '2 000', 'S/ 1.35', 'IGV 18 %', 'S/ 2 700.00'],
            ['Cono vainilla', '1 200', 'S/ 2.52', 'IGV 18 %', 'S/ 3 024.00'],
            ['Familiar 1 L chocolate', '240', 'S/ 9.90', 'IGV 18 %', 'S/ 2 376.00'],
        ], [3, 1.2, 1.3, 1.2, 1.5], total='Total  S/ 8 100.00'),
    ]),
    Pantalla('cu003_pdv', 'CU003', 'Punto de venta con boleta', 'Punto de venta', 'PdV › Heladería Av. Venezuela',
             hu='HU-10', partes=[
        p('alerta', 'Sesión abierta · Cajero: Rosa Quispe · Efectivo inicial S/ 200.00', 'ok'),
        p('pdv', [('Paleta fresa', 'S/ 1.50'), ('Paleta lúcuma', 'S/ 1.50'), ('Cono vainilla', 'S/ 3.00'),
                  ('Vaso chocolate', 'S/ 3.50'), ('Familiar 1 L', 'S/ 11.00'), ('Panetón clásico', 'S/ 22.00')],
          [('2 × Paleta fresa', 'S/ 3.00'), ('1 × Cono vainilla', 'S/ 3.00'), ('1 × Vaso chocolate', 'S/ 3.50')],
          'S/ 9.50'),
        p('botones', ['Efectivo', 'Yape', 'Cliente (DNI/RUC)', 'Cerrar caja'], 0),
    ]),
    Pantalla('cu004_liquidacion', 'CU004', 'Liquidación diaria del heladero', 'Heladeros (M2)',
             'Heladeros › Liquidaciones › LIQ/2027/00031', hu='HU-20, HU-21', f2=True, partes=[
        p('estado', ['Borrador', 'Despachado', 'Liquidado'], 1),
        p('botones', ['Confirmar liquidación', 'Imprimir', 'Volver a borrador'], 0),
        p('campos', [('Heladero', 'Juan Mamani (concesionario)'), ('Fecha', '15/01/2027'),
                     ('Lista de precios', 'Heladero'), ('Efectivo entregado', 'S/ 214.50')]),
        p('tabla', ['Producto', 'Despachado', 'Devuelto', 'Merma', 'Vendido', 'Importe'], [
            ['Paleta de fresa', '120', '18', '2', '100', 'S/ 75.00'],
            ['Paleta de lúcuma', '80', '10', '0', '70', 'S/ 52.50'],
            ['Cono vainilla', '60', '8', '1', '51', 'S/ 76.50'],
        ], [3, 1.3, 1.2, 1, 1.2, 1.5], total='Vendido S/ 204.00 · Comisión S/ 20.40'),
        p('alerta', 'Diferencia de efectivo: S/ 10.50 a favor. Queda registrada en la liquidación.', 'info'),
    ]),
    Pantalla('cu004_liquidacion_movil', 'CU004', 'Liquidación (vista móvil)', 'Heladeros (M2)',
             'LIQ/2027/00031', hu='HU-21', f2=True, ancho=400, partes=[
        p('estado', ['Despachado', 'Liquidado'], 0),
        p('campos', [('Heladero', 'Juan Mamani'), ('Fecha', '15/01/2027')], 1),
        p('tabla', ['Producto', 'Desp.', 'Dev.', 'Vend.'], [
            ['Paleta fresa', '120', '18', '100'], ['Paleta lúcuma', '80', '10', '70'], ['Cono vainilla', '60', '8', '51'],
        ], [3, 1, 1, 1], total='S/ 204.00'),
        p('botones', ['Confirmar'], 0),
    ]),
    Pantalla('cu005_recepcion_lote', 'CU005', 'Recepción de insumos con lote y vencimiento', 'Inventario',
             'Inventario › Recepciones › LIM/IN/00007', hu='HU-11, HU-12', partes=[
        p('estado', ['Borrador', 'Listo', 'Hecho'], 1),
        p('botones', ['Validar', 'Imprimir', 'Devolución'], 0),
        p('campos', [('Proveedor', 'Lácteos del Valle SAC'), ('Origen', 'P00001'),
                     ('Ubicación destino', 'LIM/Cámara fría'), ('Fecha prevista', '16/11/2026')]),
        p('tabla', ['Producto', 'Demanda', 'Hecho', 'Lote', 'Vencimiento'], [
            ['Leche fresca', '1 200 L', '1 200', 'L-2611-A', '23/11/2026'],
            ['Crema de leche', '300 kg', '300', 'L-2611-B', '07/12/2026'],
            ['Mantequilla', '150 kg', '150', 'L-2611-C', '14/01/2027'],
        ], [2.5, 1.3, 1, 1.5, 1.7]),
        p('alerta', 'Alerta de vencimiento: se avisa al Jefe de Almacén 30 días antes de cada fecha.', 'info'),
    ]),
    Pantalla('cu006_temperaturas', 'CU006', 'Registro de temperaturas de las cámaras', 'Cadena de frío (M3)',
             'Inventario › Cadena de frío › Lecturas', hu='HU-19', f2=True, partes=[
        p('botones', ['Nueva lectura', 'Alertas abiertas'], 0),
        p('kpis', [('Cámara de helados', '-19.2 °C', 'Rango -22 a -18 °C'), ('Cámara de lácteos', '3.1 °C', 'Rango 0 a 4 °C'),
                   ('Lecturas de hoy', '14', '2 por cámara y turno'), ('Alertas abiertas', '1', 'Cámara de panetón')]),
        p('tabla', ['Fecha y hora', 'Cámara', 'Lectura', 'Rango', 'Estado', 'Registró'], [
            ['15/01 08:05', 'Cámara de helados', '-19.2 °C', '-22 a -18', 'En rango', 'Operario'],
            ['15/01 08:07', 'Cámara de lácteos', '3.1 °C', '0 a 4', 'En rango', 'Operario'],
            ['15/01 14:02', 'Cámara de helados', '-16.4 °C', '-22 a -18', 'FUERA', 'Operario'],
        ], [1.5, 2, 1.1, 1.3, 1.1, 1.2]),
        p('alerta', 'Alerta creada para el Jefe de Almacén: Cámara de helados fuera de rango (-16.4 °C).', 'mal'),
    ]),
    Pantalla('cu007_orden_produccion', 'CU007', 'Orden de producción con lote', 'Fabricación',
             'Fabricación › Órdenes › LIM/MO/00012', hu='HU-14', partes=[
        p('estado', ['Borrador', 'Confirmado', 'En progreso', 'Hecho'], 2),
        p('botones', ['Producir todo', 'Órdenes de trabajo', 'Cancelar'], 0),
        p('campos', [('Producto', 'Paleta de fresa'), ('Cantidad', '10 000 unidades'),
                     ('Lista de materiales', 'Tanda industrial 10 000'), ('Lote producido', 'PT-2611-0042')]),
        p('tabla', ['Componente', 'A consumir', 'Lote reservado (FEFO)', 'Vence'], [
            ['Leche fresca', '800 L', 'L-2611-A', '23/11/2026'],
            ['Azúcar', '250 kg', 'L-2610-B', '15/03/2027'],
            ['Pulpa de fresa', '300 kg', 'L-2611-F', '10/02/2027'],
        ], [2.2, 1.3, 2.2, 1.4], total='Costo del lote (FIFO): S/ 6 120.00 · Costo unitario S/ 0.61'),
    ]),
    Pantalla('cu008_inspeccion', 'CU008', 'Inspección de calidad del lote', 'Calidad (M1)',
             'Calidad › Inspecciones › INS/00018', hu='HU-17, HU-18', f2=True, partes=[
        p('estado', ['Pendiente', 'En medición', 'Aprobado', 'Rechazado'], 1),
        p('botones', ['Aprobar lote', 'Rechazar lote', 'Certificado PDF'], 0),
        p('campos', [('Orden de producción', 'LIM/MO/00012'), ('Lote', 'PT-2611-0042'),
                     ('Producto', 'Paleta de fresa'), ('Inspector', 'Carmen Rojas')]),
        p('tabla', ['Punto de control', 'Norma', 'Medición', 'Resultado'], [
            ['Pasteurización', '80 a 85 °C', '82 °C', 'Cumple'],
            ['Peso por unidad', '58 a 62 g', '60 g', 'Cumple'],
            ['Microbiología (coliformes)', '< 10 UFC/g', '4 UFC/g', 'Cumple'],
        ], [2.5, 1.5, 1.3, 1.3]),
        p('alerta', 'Todos los puntos cumplen: el lote puede aprobarse y liberarse al despacho.', 'ok'),
    ]),
    Pantalla('cu009_tablero', 'CU009', 'Tablero gerencial de KPIs', 'Tablero (M4)', 'Tablero › Gerencia',
             hu='HU-22, HU-23', f2=True, partes=[
        p('kpis', [('Ventas del mes', 'S/ 612 340', '+8 % vs. mes anterior'), ('Cumplimiento de producción', '94 %', '188 de 200 OP'),
                   ('Lotes aprobados', '98 %', 'Solo con M1'), ('Stock por vencer (30 d)', '12 lotes', 'Valor S/ 18 400')]),
        p('barras', 'Ventas por mes (S/ miles)', [380, 450, 520, 640], ['Ago', 'Sep', 'Oct', 'Nov']),
        p('alerta', 'Liquidaciones pendientes: 3 · Alertas de temperatura abiertas: 1', 'info'),
    ]),
    Pantalla('cu010_ventas_pivote', 'CU010', 'Análisis de ventas por línea, canal y temporada', 'Ventas',
             'Ventas › Informes › Análisis de ventas', hu='HU-23', partes=[
        p('botones', ['Medidas: Importe', 'Filtros', 'Agrupar por', 'Favoritos'], 0),
        p('tabla', ['Línea de producto', 'Ago', 'Sep', 'Oct', 'Nov', 'Total'], [
            ['Paletas', '212 400', '248 300', '301 900', '342 100', '1 104 700'],
            ['Conos y vasos', '98 700', '116 200', '140 800', '160 500', '516 200'],
            ['Familiares 1 L', '64 100', '75 900', '91 300', '104 800', '336 100'],
            ['Panetón (Navidad)', '0', '0', '12 400', '88 600', '101 000'],
        ], [2.5, 1.2, 1.2, 1.2, 1.2, 1.4], total='Total S/ 2 058 000'),
        p('barras', 'Importe por canal (S/ miles)', [820, 480, 290, 190], ['Distribuidor', 'Autoservicio', 'Bodega', 'Heladero']),
    ]),
    Pantalla('cu011_rfq', 'CU011', 'Solicitud de cotización generada por la regla mín./máx.', 'Compras',
             'Compras › Solicitudes de cotización › P00001', hu='HU-13', partes=[
        p('estado', ['RFQ', 'RFQ enviada', 'Orden de compra', 'Recibido'], 0),
        p('botones', ['Confirmar pedido', 'Enviar por correo', 'Cancelar'], 0),
        p('campos', [('Proveedor', 'Lácteos del Valle SAC'), ('Comprador', 'Compras (Compras D\'Onofrio)'),
                     ('Entrega prevista', '16/11/2026'), ('Destino', 'Planta Lima')]),
        p('tabla', ['Producto', 'Cantidad', 'Precio unit.', 'Impuesto', 'Subtotal'], [
            ['Leche fresca', '1 200 L', 'S/ 2.10', 'IGV 18 %', 'S/ 2 520.00'],
            ['Crema de leche', '300 kg', 'S/ 14.00', 'IGV 18 %', 'S/ 4 200.00'],
            ['Mantequilla', '150 kg', 'S/ 22.00', 'IGV 18 %', 'S/ 3 300.00'],
        ], [3, 1.2, 1.3, 1.2, 1.5], total='Total  S/ 10 020.00 + IGV'),
    ]),
    Pantalla('cu012_factura', 'CU012', 'Factura (01) o boleta (03) con IGV', 'Facturación',
             'Facturación › Clientes › Facturas › F 00000001', hu='HU-15', partes=[
        p('estado', ['Borrador', 'Publicado', 'Pagado'], 1),
        p('botones', ['Registrar pago', 'Imprimir', 'Restablecer a borrador'], 0),
        p('campos', [('Cliente', 'Distribuidora Sur SAC · RUC 20123456786'), ('Tipo de documento', '(01) Factura'),
                     ('Diario', 'Facturas'), ('Vencimiento', '30 días')]),
        p('tabla', ['Producto', 'Cantidad', 'Precio unit.', 'Impuesto', 'Subtotal'], [
            ['Paleta de fresa', '100', 'S/ 1.27', 'IGV 18 %', 'S/ 127.12'],
        ], [3, 1.2, 1.3, 1.2, 1.5], total='Subtotal 127.12 · IGV 22.88 · Total S/ 150.00'),
    ]),
]


# Reportes en PDF (QWeb) de la Fase 2: se diseñaron en la F1 y se implementaron en la F2 (4.6.3). Hoja A4 sin barra de la aplicación.
REPORTES = [
    Pantalla('rp_certificado_calidad', 'CU008', 'Certificado de calidad del lote', 'Calidad (M1)',
             'Calidad › Inspecciones › INS/00018 › Imprimir', hu='HU-18', f2=True, reporte=True, ancho=794, partes=[
        p('campos', [('Producto', '[PT-H01] Paleta de fresa 60 g'), ('Lote', 'PT-2611-0042'),
                     ('Orden de producción', 'LIM/MO/00012'), ('Fecha de producción', '15/01/2027'),
                     ('Vence', '15/07/2027'), ('Inspector', 'Carmen Rojas')]),
        p('tabla', ['Punto de control', 'Norma', 'Medición', 'Resultado'], [
            ['Pasteurización', '80 a 85 °C', '82 °C', 'Cumple'],
            ['Peso por unidad', '58 a 62 g', '60 g', 'Cumple'],
            ['Microbiología (coliformes)', '< 10 UFC/g', '4 UFC/g', 'Cumple'],
        ], [2.5, 1.5, 1.3, 1.3]),
        p('alerta', 'RESULTADO: lote APROBADO para su despacho.', 'ok'),
        p('texto', 'Firma del inspector de calidad: ____________________        Firma del jefe de producción: ____________________'),
    ]),
    Pantalla('rp_liquidacion_heladero', 'CU004', 'Liquidación del heladero', 'Heladeros (M2)',
             'Heladeros › Liquidaciones › LIQ/2027/00031 › Imprimir', hu='HU-21', f2=True, reporte=True, ancho=794, partes=[
        p('campos', [('Heladero', 'Juan Mamani (concesionario)'), ('Fecha', '15/01/2027'),
                     ('Lista de precios', 'Heladero'), ('Liquidador', 'Liquidador de Heladeros')]),
        p('tabla', ['Producto', 'Despachado', 'Devuelto', 'Merma', 'Vendido', 'Importe'], [
            ['Paleta de fresa', '120', '18', '2', '100', 'S/ 75.00'],
            ['Paleta de lúcuma', '80', '10', '0', '70', 'S/ 52.50'],
            ['Cono vainilla', '60', '8', '1', '51', 'S/ 76.50'],
        ], [3, 1.3, 1.2, 1, 1.2, 1.5], total='Vendido S/ 204.00 · Comisión S/ 20.40'),
        p('alerta', 'Efectivo entregado S/ 214.50 · Diferencia a favor del heladero: S/ 10.50', 'info'),
        p('texto', 'Firma del heladero: ____________________        Firma del liquidador: ____________________'),
    ]),
]


# ----------------------------------------------------------------------------- render

def dibujar(pantalla, mockup):
    e = Estilo(mockup)
    w = pantalla.ancho
    margen = 24
    cuerpo_w = w - 2 * margen
    cuerpo, y = [], 150 if w > 600 else 130
    for nombre, args, kw in pantalla.partes:
        svg, alto = COMPONENTES[nombre](margen, y, cuerpo_w, e, *args, **kw)
        cuerpo.append(svg)
        y += alto
    alto_total = y + 24
    cabecera = [t(margen, 100, pantalla.titulo, e, 17 if w > 600 else 14, 'bold')]
    if pantalla.reporte:
        # Hoja con la cabecera de la compañía (logo, nombre y RUC ficticio), como el layout de los reportes de Odoo
        cabecera = [
            f'<circle cx="{margen + 20}" cy="40" r="18" fill="{e.marca}" stroke="{e.tinta}"/>',
            t(margen + 48, 36, "D'Onofrio", e, 16, 'bold', color=e.tinta),
            t(margen + 48, 52, 'Helados y Confitería', e, 9, color=e.gris),
            t(w - margen, 34, "D'Onofrio – Unidad de Helados y Confitería (proyecto académico)", e, 9, ancla='end'),
            t(w - margen, 48, 'Av. Ejemplo 123, Lima · RUC 20999999990', e, 9, color=e.gris, ancla='end'),
            f'<line x1="{margen}" y1="66" x2="{w - margen}" y2="66" stroke="{e.borde}"/>',
            t(margen, 100, pantalla.titulo, e, 17, 'bold', color=AMARILLO_OSCURO if mockup else None),
            t(w - margen, 100, f'{pantalla.cu} · {pantalla.hu}', e, 11, color=e.gris, ancla='end'),
        ]
    else:
        cabecera = [
            # barra superior de la aplicación
            f'<rect width="{w}" height="46" fill="{e.marca if mockup else "#CCCCCC"}"/>',
            t(margen, 29, "D'Onofrio ERP", e, 14, 'bold'),
            t(margen + 130, 29, pantalla.modulo, e, 12),
            t(w - margen, 29, 'Evelyn · Ventas' if not pantalla.f2 else 'Usuario del módulo', e, 11, ancla='end'),
            # ruta y título
            t(margen, 72, pantalla.ruta, e, 11, color=e.gris),
            t(margen, 100, pantalla.titulo, e, 17 if w > 600 else 14, 'bold'),
            t(w - margen, 72 if w <= 600 else 100, f'{pantalla.cu} · {pantalla.hu}', e, 11, color=e.gris, ancla='end'),
        ]
    fondo = '#FFFFFF' if pantalla.reporte else e.fondo
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{alto_total:.0f}" '
         f'viewBox="0 0 {w} {alto_total:.0f}" font-family="{e.fuente}">',
         f'<rect width="{w}" height="{alto_total:.0f}" fill="{fondo}"/>'] + cabecera
    if pantalla.f2:
        s.append(f'<rect x="{margen}" y="110" width="250" height="20" rx="10" '
                 f'fill="{AMARILLO_CLARO if mockup else "#EEEEEE"}" stroke="{e.tinta}" stroke-dasharray="3 2"/>'
                 + t(margen + 125, 124, 'Módulo propio de la Fase 2 (implementado)', e, 10, ancla='middle'))
    s += cuerpo
    s.append(t(w - margen, alto_total - 8, 'Wireframe' if not mockup else 'Mockup', e, 9, color=e.gris, ancla='end'))
    s.append('</svg>')
    return '\n'.join(s)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for pantalla in PANTALLAS + REPORTES:
        for prefijo, mockup in (('wf', False), ('mk', True)):
            (SALIDA / f'{prefijo}_{pantalla.id}.svg').write_text(dibujar(pantalla, mockup), encoding='utf-8')
        print(f'{pantalla.id}: wf + mk')


if __name__ == '__main__':
    main()
