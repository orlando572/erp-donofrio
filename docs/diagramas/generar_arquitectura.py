#!/usr/bin/env python3
"""Genera los diagramas de arquitectura (Orlando) como SVG:
  - arquitectura_empresarial.svg  (4.1.3: capas TOGAF, AS-IS frente a TO-BE)
  - infraestructura.svg           (4.3.1: PC de desarrollo, contenedores, GitHub y nube; estado real del Sprint 3)
  - pipeline_cicd.svg             (5.15: de la rama de trabajo a la release y al despliegue en el nodo)
Los diagramas C4 (5.7 y 5.8) están en docs/diagramas/c4/ (PlantUML) y el grafo de dependencias entre módulos (5.4) lo
genera scripts/grafo_dependencias.py.

Uso:  python3 docs/diagramas/generar_arquitectura.py        (escribe en docs/diagramas/arquitectura/)
El PNG se obtiene del SVG (ver docs/diagramas/README.md). No necesita librerías.
"""
from pathlib import Path
from xml.sax.saxutils import escape

SALIDA = Path(__file__).resolve().parent / 'arquitectura'
FUENTE = 'DejaVu Sans, Arial, sans-serif'


def envolver(texto, ancho_px, tam=12):
    """Parte el texto en líneas de unos ``ancho_px`` píxeles (DejaVu Sans ≈ 0.55 · tamaño por carácter)."""
    max_car = max(int(ancho_px / (tam * 0.55)), 8)
    lineas, actual = [], ''
    for palabra in texto.split():
        if actual and len(actual) + 1 + len(palabra) > max_car:
            lineas.append(actual)
            actual = palabra
        else:
            actual = f'{actual} {palabra}'.strip()
    return lineas + [actual]


class Lienzo:
    def __init__(self, ancho, alto):
        self.ancho, self.alto, self.p = ancho, alto, []
        self.p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" '
                      f'viewBox="0 0 {ancho} {alto}" font-family="{FUENTE}">')
        self.p.append('<defs><marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
                      'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>')
        self.p.append(f'<rect width="{ancho}" height="{alto}" fill="#fff"/>')

    def texto(self, x, y, lineas, tam=12, peso='normal', ancla='middle', color='#222', alto_linea=None):
        alto_linea = alto_linea or tam + 3
        if isinstance(lineas, str):
            lineas = [lineas]
        for i, linea in enumerate(lineas):
            self.p.append(f'<text x="{x:.0f}" y="{y + i * alto_linea:.0f}" text-anchor="{ancla}" font-size="{tam}" '
                          f'font-weight="{peso}" fill="{color}">{escape(linea)}</text>')

    def caja(self, x, y, w, h, titulo=None, lineas=(), relleno='#f4f7fb', borde='#222', punteada=False,
             tam=12, titulo_tam=13, ancla_texto='start', rx=8):
        trazo = ' stroke-dasharray="6 4"' if punteada else ''
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{relleno}" '
                      f'stroke="{borde}" stroke-width="1.5"{trazo}/>')
        cy = y + 20
        if titulo:
            self.texto(x + 10 if ancla_texto == 'start' else x + w / 2, cy, envolver(titulo, w - 20, titulo_tam),
                       titulo_tam, 'bold', ancla_texto)
            cy += (len(envolver(titulo, w - 20, titulo_tam))) * (titulo_tam + 3) + 3
        for linea in lineas:
            partes = envolver(linea, w - 24, tam)
            for j, parte in enumerate(partes):
                prefijo = '• ' if j == 0 else '  '
                self.texto(x + 10, cy, prefijo + parte, tam, ancla='start')
                cy += tam + 3
            cy += 2

    def flecha(self, puntos, punteada=False, etiqueta=None, doble=False):
        trazo = ' stroke-dasharray="6 4"' if punteada else ''
        inicio = ' marker-start="url(#flecha)"' if doble else ''
        self.p.append('<polyline fill="none" stroke="#333" stroke-width="1.6"' + trazo + inicio +
                      ' marker-end="url(#flecha)" points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in puntos) + '"/>')
        if etiqueta:
            (x1, y1), (x2, y2) = puntos[0], puntos[-1]
            self.texto((x1 + x2) / 2, (y1 + y2) / 2 - 5, etiqueta, 11, ancla='middle', color='#333')

    def cierre(self):
        self.p.append('</svg>')
        return '\n'.join(self.p)


# ----------------------------------------------------------------------------- 4.1.3 arquitectura empresarial

def arquitectura_empresarial():
    W, H = 1500, 640
    L = Lienzo(W, H)
    L.texto(W / 2, 34, 'Arquitectura empresarial de D\'Onofrio: situación actual (AS-IS) y propuesta (TO-BE)', 18, 'bold')
    L.texto(W / 2, 56, 'Capas TOGAF simplificadas: negocio, datos, aplicación y tecnología (los datos de la situación actual son un supuesto, S7)',
            12, color='#555')
    x_capa, w_capa = 20, 140
    x_asis, w_asis = 175, 610
    x_tobe, w_tobe = 840, 640
    L.texto(x_asis + w_asis / 2, 94, 'AS-IS · situación actual', 15, 'bold', color='#c0392b')
    L.texto(x_tobe + w_tobe / 2, 94, 'TO-BE · propuesta con Odoo 19', 15, 'bold', color='#1e7e34')
    capas = [
        ('Negocio', '#fff8e1', [
            'Cinco áreas con procesos manuales: ventas B2B, liquidación de heladeros, producción y calidad, almacén con cadena de frío y compras',
            'Cada área decide con sus propios papeles; la gerencia recibe reportes armados a mano al cierre',
        ], [
            'Procesos de punta a punta en un solo flujo: CRM → pedido → entrega FEFO → factura; compra → recepción; orden de producción → lote',
            'Punto de venta con boleta; gerencia con dashboards y vistas pivote; mesa de servicios TI',
        ]),
        ('Datos', '#eef7ee', [
            'Excel por área, kárdex, planillas de temperatura y formatos de inspección en papel',
            'Sin lote ni vencimiento en un sistema; el mismo dato se digita dos o más veces',
        ], [
            'Una sola base PostgreSQL 16: el lote, el vencimiento y el movimiento quedan ligados',
            'Datos maestros cargados por código (donofrio_base); réplica de lectura (HU-25) y respaldos con restauración probada (HU-26)',
        ]),
        ('Aplicación', '#eef3fb', [
            'Excel, correo y Word; un sistema contable aislado; sin integración entre áreas',
        ], [
            'Odoo 19 Community: Ventas, CRM, Punto de venta, Inventario, Manufactura, Compras, Facturación (l10n_pe), RR. HH. y Project',
            'donofrio_base en la Fase 1; donofrio_calidad, donofrio_heladeros y donofrio_tablero en la Fase 2, solo si se confirman en el gate',
        ]),
        ('Tecnología', '#f3eefb', [
            'PC de oficina y un servidor de archivos (supuesto)',
            'Sin entornos separados ni respaldos verificados',
        ], [
            'Docker Compose (Odoo 19 + PostgreSQL 16), Nginx con TLS (perfil proxy) y réplica de PostgreSQL (perfil replica)',
            'GitHub (código, Projects), Actions (CI) y GHCR (imágenes); Ubuntu o WSL2 en las PC de desarrollo',
        ]),
    ]
    y, alto = 112, 118
    for i, (nombre, color, asis, tobe) in enumerate(capas):
        yy = y + i * (alto + 12)
        L.caja(x_capa, yy, w_capa, alto, None, relleno=color)
        L.texto(x_capa + w_capa / 2, yy + alto / 2 + 5, nombre, 15, 'bold')
        L.caja(x_asis, yy, w_asis, alto, None, asis, tam=13, relleno='#fdf2f0', borde='#c0392b')
        L.caja(x_tobe, yy, w_tobe, alto, None, tobe, tam=13, relleno='#f0f9f2', borde='#1e7e34')
        L.flecha([(x_asis + w_asis, yy + alto / 2), (x_tobe, yy + alto / 2)])
    return L.cierre()


# ----------------------------------------------------------------------------- 4.3.1 infraestructura

def infraestructura():
    W, H = 1500, 760
    L = Lienzo(W, H)
    L.texto(W / 2, 32, "Infraestructura tecnológica del ERP de D'Onofrio", 18, 'bold')
    L.texto(W / 2, 54, 'Línea continua: existe en develop (Sprint 3) · Línea punteada: opcional o aún sin publicar (GHCR espera el primer tag v*)', 12, color='#555')

    # Usuario
    L.caja(120, 75, 790, 70, 'Usuario (navegador)', ['Chrome, Firefox o Edge · https://localhost:8443 con el perfil proxy · http://localhost:8069 en desarrollo'],
           relleno='#fff', borde='#555')

    # PC de desarrollo
    L.caja(20, 170, 1130, 400, 'PC de desarrollo (Ubuntu o WSL2) · una por integrante', [], relleno='#fafafa', borde='#555')
    L.caja(40, 205, 1090, 350, 'Docker Engine · proyecto «erp-donofrio» (docker-compose.yml)', [], relleno='#f4f7fb', borde='#2c5282')

    # Fila de servicios
    L.caja(60, 245, 245, 170, 'nginx · nginx:stable',
           ['Perfil proxy · HU-27', 'TLS 1.2/1.3, HSTS, CSP, gzip y caché de assets', 'Puertos 8080 y 8443'], relleno='#e8f4ff', borde='#2c5282')
    L.caja(335, 245, 245, 170, 'odoo · odoo:19.0-20261112',
           ['Imagen propia (docker/odoo)', 'Puertos 8069 y 8072, solo en 127.0.0.1', 'Monta ./addons en lectura',
            'Healthcheck /web/health'], relleno='#e8f4ff', borde='#2c5282')
    L.caja(610, 245, 245, 170, 'db · postgres:16',
           ['Puerto 5432, solo en 127.0.0.1 (DBeaver)', 'Rol «odoo» sin superusuario', 'Healthcheck pg_isready'],
           relleno='#e8f4ff', borde='#2c5282')
    L.caja(885, 245, 225, 170, 'db-replica · postgres:16',
           ['Perfil replica · HU-25', 'Streaming replication, solo lectura', 'Puerto 5433 en 127.0.0.1'], relleno='#e8f4ff', borde='#2c5282')

    # Volúmenes
    L.caja(335, 455, 245, 80, 'Volumen odoo-data', ['/var/lib/odoo: filestore'], relleno='#fffbe6', borde='#8a6d00')
    L.caja(610, 455, 245, 80, 'Volumen pgdata', ['/var/lib/postgresql/data'], relleno='#fffbe6', borde='#8a6d00')

    # Flujos
    L.flecha([(180, 145), (180, 245)])
    L.texto(188, 163, 'HTTPS', 11, ancla='start', color='#333')
    L.flecha([(457, 145), (457, 245)])
    L.texto(465, 163, 'HTTP 8069', 11, ancla='start', color='#333')
    L.flecha([(305, 330), (335, 330)])
    L.flecha([(580, 330), (610, 330)], doble=True)
    L.texto(595, 322, 'SQL', 10, color='#333')
    L.flecha([(855, 330), (885, 330)])
    L.flecha([(457, 415), (457, 455)])
    L.flecha([(732, 415), (732, 455)])

    # GitHub
    L.caja(1190, 75, 290, 490, 'GitHub · repo erp-donofrio (público)', [], relleno='#fafafa', borde='#555')
    L.caja(1205, 115, 260, 100, 'Repositorio y Projects',
           ['Ramas main, develop y feature/HU-xx', 'PR con revisión cruzada', 'Project «Scrum ERP D\'Onofrio»'], relleno='#fff', borde='#555')
    L.caja(1205, 230, 260, 130, 'Actions · runner ubuntu-24.04',
           ['ci.yml: jobs lint, test, replica, backup y proxy', 'perf.yml (manual): k6 y ZAP', 'release.yml: imagen y zip'], relleno='#e8f9ee', borde='#1e7e34')
    L.caja(1205, 375, 260, 175, 'GHCR · ghcr.io/orlando572/erp-donofrio',
           ['Imagen de Odoo en cada tag v*', 'Zip del código en la Release', 'HU-29: workflow listo y probado en ensayo; aún no hay tag publicado'], relleno='#fff', borde='#555', punteada=True)
    L.flecha([(1150, 330), (1190, 330)], etiqueta='')
    L.texto(1170, 318, 'push', 11, color='#333')

    # VM opcional
    L.caja(1190, 600, 290, 130, 'VM en la nube (opcional)',
           ['Oracle Free u otra, con Docker Compose', 'Nginx y Let\'s Encrypt', 'Despliegue por SSH desde Actions'],
           relleno='#fff', borde='#555', punteada=True)
    L.flecha([(1335, 565), (1335, 600)], punteada=True)

    # Leyenda
    L.caja(20, 600, 1130, 130, 'Cómo se usa', [
        'Cada integrante levanta todo con: cp .env.example .env · docker compose up -d --build · scripts/init_db.sh',
        'Los puertos de Odoo y PostgreSQL solo escuchan en 127.0.0.1; Nginx publica 8080 y 8443. Perfiles opcionales: docker compose --profile replica up -d y scripts/levantar_prod.sh (proxy)',
        'El CI de GitHub usa el mismo docker-compose.yml y la misma imagen fechada que las PC (RNF012)'],
           relleno='#fff', borde='#999')
    return L.cierre()


# ----------------------------------------------------------------------------- 5.15 pipeline CI/CD

def pipeline_cicd():
    W, H = 1500, 700
    L = Lienzo(W, H)
    L.texto(W / 2, 32, 'Pipeline CI/CD del ERP de D\'Onofrio: de la rama de trabajo a la release y al despliegue', 18, 'bold')
    L.texto(W / 2, 54, 'Línea continua: automático en GitHub Actions · Línea punteada: paso manual en el nodo de despliegue', 12, color='#555')

    # Fila 1: integración
    L.caja(20, 90, 230, 150, '1. Rama feature/HU-xx', ['Commit convencional en español', 'scripts/test.sh y check_legacy.sh en local', 'Sale de develop'],
           relleno='#fff', borde='#555')
    L.caja(290, 90, 230, 150, '2. Pull request a develop', ['Plantilla con checklist de la DoD', '«Parte de #n» (la épica se cierra en el último PR)'],
           relleno='#fff', borde='#555')
    L.caja(560, 90, 470, 150, '3. ci.yml (pull_request, push y lunes 06:00 Lima)', [], relleno='#e8f9ee', borde='#1e7e34')
    jobs = [('lint', 'ruff y patrones legacy', True), ('test', 'instala y prueba', True),
            ('replica', 'streaming', False), ('backup', 'restauración', False), ('proxy', 'TLS y cabeceras', False)]
    for i, (nombre, detalle, requerido) in enumerate(jobs):
        x = 572 + i * 90
        L.caja(x, 130, 84, 100, nombre, [detalle], relleno='#fff' if not requerido else '#d7f0d2', borde='#1e7e34', tam=10, titulo_tam=12)
    L.caja(1070, 90, 190, 150, '4. Revisión cruzada', ['1 aprobación del otro integrante', 'Conversaciones resueltas', 'Checks obligatorios en develop: lint y test'],
           relleno='#fff', borde='#555')
    L.caja(1290, 90, 190, 150, '5. Squash and merge', ['A develop, un commit por HU', 'El CI corre otra vez en el push'], relleno='#fff', borde='#555')
    for x1, x2 in ((250, 290), (520, 560), (1030, 1070), (1260, 1290)):
        L.flecha([(x1, 165), (x2, 165)])

    # Fila 2: release y despliegue
    L.caja(20, 330, 230, 150, '6. PR develop → main', ['Merge commit (no squash)', 'Conserva la trazabilidad de cada HU', 'CI en verde y 1 aprobación'], relleno='#fff', borde='#555')
    L.caja(290, 330, 230, 150, '7. Tag vX.Y.Z', ['git tag -a desde main', 'v0.x = preliminar; v1.0.0 = núcleo de la Fase 1', 'Al 23/11/2026 no se publicó ninguno'],
           relleno='#fff', borde='#555', punteada=True)
    L.caja(560, 330, 470, 150, '8. release.yml (tag v*; en PR y manual es un ensayo)', [
        'Construye la imagen con --build-context addons=./addons y la prueba (scripts/probar_imagen.sh)',
        'Empaqueta erp-donofrio-vX.Y.Z.zip (scripts/empaquetar_release.sh)',
        'Solo con tag: publica en GHCR (:vX.Y.Z y :latest) y crea la GitHub Release con el zip'],
           relleno='#e8f9ee', borde='#1e7e34', tam=11)
    L.caja(1070, 330, 410, 150, '9. Despliegue en el nodo (manual, un solo nodo)', [
        'scripts/backup.sh antes de cambiar nada',
        'git checkout vX.Y.Z y scripts/levantar_prod.sh (Nginx + TLS, workers = 2)',
        'scripts/verificar_despliegue.sh como prueba de humo',
        'Rollback: volver al tag anterior (y restore.sh si cambiaron los datos)'], relleno='#fff', borde='#555', punteada=True, tam=11)
    L.flecha([(1385, 240), (1385, 285), (135, 285), (135, 330)])
    L.flecha([(250, 405), (290, 405)])
    L.flecha([(520, 405), (560, 405)])
    L.flecha([(1030, 405), (1070, 405)], punteada=True)

    # Disparadores y repositorio de imágenes
    L.caja(20, 530, 700, 140, 'Otros disparadores y controles', [
        'perf.yml (solo workflow_dispatch): k6 (carga) y ZAP baseline sobre el despliegue protegido; reportes como artefactos',
        'ci.yml también corre cada lunes 11:00 UTC: regresión de mantenimiento',
        'Secretos: solo GITHUB_TOKEN en Actions; las contraseñas del compose salen de .env (no versionado)'], relleno='#f4f7fb', borde='#999', tam=11)
    L.caja(760, 530, 720, 140, 'Dónde queda cada entregable', [
        'Código y PR: github.com/orlando572/erp-donofrio (ramas main y develop protegidas)',
        'Imagen: ghcr.io/orlando572/erp-donofrio:vX.Y.Z (aparece con el primer tag)',
        'Zip del código: adjunto de la GitHub Release',
        'Evidencias de cada job: pestaña Actions del repositorio'], relleno='#f4f7fb', borde='#999', tam=11)
    return L.cierre()


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for nombre, fabrica in {'arquitectura_empresarial': arquitectura_empresarial, 'infraestructura': infraestructura,
                             'pipeline_cicd': pipeline_cicd}.items():
        (SALIDA / f'{nombre}.svg').write_text(fabrica(), encoding='utf-8')
        print(f'{nombre}.svg')


if __name__ == '__main__':
    main()
