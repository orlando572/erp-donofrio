# Diagramas

| Carpeta | Contenido | Herramienta | Responsable |
|---|---|---|---|
| `bpmn/` | BPMN AS-IS: venta B2B, liquidación del heladero y compra de insumos (Evelyn); producción y calidad, y recepción y despacho con cadena de frío (Orlando). BPMN TO-BE (Sprint 2): producción con Odoo estándar, producción con inspección de calidad (M1) y recepción y despacho (Orlando); venta B2B, compra de insumos, heladero con Odoo estándar y heladero con liquidación diaria (M2) (Evelyn) (`.bpmn`, `.svg`, `.png`) | `generar_bpmn.py` + bpmn.io | Evelyn y Orlando |
| `arquitectura/` | Arquitectura empresarial AS-IS y TO-BE (4.1.3), infraestructura tecnológica (4.3.1) y pipeline CI/CD (5.15), con el estado real del Sprint 3 (`.svg`, `.png`) | `generar_arquitectura.py` | Orlando |
| `c4/` | Diagramas C4 de contexto, contenedores y componentes (5.7 y 5.8) (`.puml`, `.png`, `.svg`) | PlantUML con la librería C4 | Orlando |
| `dependencias/` | Grafo de dependencias entre módulos (5.4): `dependencias_directas` y `dependencias_completo` (`.dot`, `.svg`, `.png`) y `dependencias.csv` | `scripts/grafo_dependencias.py` + Graphviz | Orlando |
| `pantallas/` | Wireframes (`wf_*`) y mockups (`mk_*`) de las 12 pantallas de los casos de uso, incluidas las de la Fase 2 (`.svg`, `.png`) | `generar_pantallas.py` | Evelyn |
| `clases/` | Diagrama de clases del núcleo (modelos de Odoo y extensiones de `donofrio_base`) y clases **propuestas** de la Fase 2 (4.2.5) (`.puml`, `.png`, `.svg`) | PlantUML | Orlando |
| `er/` | Modelo ER general (39 tablas: núcleo de la Fase 1 y M1 calidad) y diseño lógico (ventas, inventario, producción y compras) (4.2.6 y 4.2.7), extraídos de la BD real (`.puml`, `.png`, `.svg`) | `scripts/diagrama_er.py` + PlantUML | Orlando |
| `cu/` | Casos de uso de ventas, heladeros y gerencia (Evelyn) y de logística y producción (Orlando) (`.puml` y `.png`) | PlantUML | Evelyn y Orlando |

`cu/` también incluye Compras y Facturación (CU011 y CU012). Los datos de procesos son ficticios y verosímiles (supuesto S7 del plan).

## BPMN

Los procesos se definen en [`generar_bpmn.py`](generar_bpmn.py) (carriles, tareas y flujos). El script escribe el `.bpmn` (se abre y se edita en <https://demo.bpmn.io>) y un `.svg` con la misma disposición. No necesita librerías.

```bash
python3 docs/diagramas/generar_bpmn.py
```

Genera los AS-IS (`as-is_*`) y los TO-BE (`to-be_*`). En los TO-BE, las tareas en amarillo dependen de un módulo propio de la Fase 2. El PNG sale del SVG. Con Docker, sin instalar nada en tu PC:

```bash
docker run --rm -v "$PWD/docs/diagramas/bpmn":/b --entrypoint sh python:3.12-slim -c \
  "apt-get update -qq && apt-get install -y -qq librsvg2-bin fonts-dejavu-core && cd /b && for f in *.svg; do rsvg-convert \$f -o \${f%.svg}.png; done && chown $(id -u):$(id -g) *.png"
```

## Casos de uso

```bash
docker run --rm -u $(id -u):$(id -g) -v "$PWD/docs/diagramas/cu":/data plantuml/plantuml:latest -tpng -charset UTF-8 /data/*.puml
```

## Arquitectura, infraestructura y pipeline CI/CD

Los tres diagramas (arquitectura empresarial, infraestructura y `pipeline_cicd`) se definen en [`generar_arquitectura.py`](generar_arquitectura.py) y se escriben como `.svg` en `arquitectura/`. No necesita librerías.

```bash
python3 docs/diagramas/generar_arquitectura.py
docker run --rm -v "$PWD/docs/diagramas/arquitectura":/b --entrypoint sh python:3.12-slim -c \
  "apt-get update -qq && apt-get install -y -qq librsvg2-bin fonts-dejavu-core && cd /b && for f in *.svg; do rsvg-convert \$f -o \${f%.svg}.png; done && chown $(id -u):$(id -g) *.png"
```

## Diagramas C4 (5.7 y 5.8)

Contexto, contenedores y componentes están escritos a mano en PlantUML con la librería C4 que ya trae la imagen (`!include <C4/…>`, sin descargar nada). Reflejan el estado real de `develop` (réplica, Nginx con TLS, release en GHCR, k6 y ZAP) y marcan como **no implementado** lo que el plan nombraba y no existe (SUNAT, Uptime Kuma, correo saliente). Versión de PlantUML fijada: `1.2026.10` (con Graphviz 14.0.1).

```bash
for f in png svg; do docker run --rm -u $(id -u):$(id -g) -v "$PWD/docs/diagramas/c4":/data plantuml/plantuml:1.2026.10 -charset UTF-8 -t$f /data/*.puml; done
```

## Grafo de dependencias entre módulos (5.4)

`scripts/grafo_dependencias.py` lee los `__manifest__.py` del repositorio, de Odoo 19.0 y de `auditlog` (OCA), resuelve el árbol de `depends` de `donofrio_base`, calcula los módulos que entran por `auto_install` y escribe los `.dot` y el `.csv`. Graphviz corre en la imagen `plantuml/plantuml:1.2026.10` y el PNG sale del SVG con librsvg en `python:3.12-slim`: no se instala nada en el equipo. Los manifiestos de Odoo salen de una imagen de Docker (la que corre de verdad) o de un checkout en `~/src/odoo-19.0`; con `--bd` compara el resultado con los módulos instalados de una base (solo lectura).

```bash
docker compose build odoo                                         # solo si falta la imagen erp-donofrio/odoo:19.0 (trae auditlog)
python3 scripts/grafo_dependencias.py --imagen erp-donofrio/odoo:19.0 --bd donofrio_perf
python3 scripts/grafo_dependencias.py                             # alternativa: fuentes de ~/src/odoo-19.0
python3 scripts/grafo_dependencias.py --sin-render                # solo .dot y .csv (sin Docker de Graphviz)
```

## Wireframes y mockups

Cada pantalla se describe una vez en [`generar_pantallas.py`](generar_pantallas.py) y de ahí salen el wireframe (grises) y el mockup (paleta de marca). No necesita librerías.

```bash
python3 docs/diagramas/generar_pantallas.py
docker run --rm -v "$PWD/docs/diagramas/pantallas":/b --entrypoint sh python:3.12-slim -c \
  "apt-get update -qq && apt-get install -y -qq librsvg2-bin fonts-dejavu-core && cd /b && for f in *.svg; do rsvg-convert \$f -o \${f%.svg}.png; done && chown $(id -u):$(id -g) *.png"
```

## Clases (4.2.5)

Las dos figuras están escritas a mano en PlantUML (los modelos y campos se verificaron contra `ir_model_fields`; las clases de la Fase 2 son **propuestas**, con estereotipo `<<propuesto>>`).

```bash
for f in png svg; do docker run --rm -u $(id -u):$(id -g) -v "$PWD/docs/diagramas/clases":/data plantuml/plantuml:latest -charset UTF-8 -t$f /data/*.puml; done
```

## Modelo ER, diseño lógico y diccionario de datos (4.2.6 a 4.2.8)

No se dibujan a mano: salen de una BD real. Para reflejar `develop` conviene una BD limpia con `donofrio_base` recién instalado (la de desarrollo puede estar desactualizada). Solo hacen lecturas (sesión de psql en modo solo lectura). Con el contenedor `db` arriba y `.env`:

```bash
MODULOS=donofrio_base,donofrio_calidad scripts/esquema_limpio.sh crear   # BD temporal esquema_tmp_informe (1-2 min); no toca las demás
python3 scripts/diagrama_er.py --bd esquema_tmp_informe           # docs/diagramas/er/*.puml, .png y .svg (PlantUML en Docker)
python3 scripts/diccionario_datos.py --bd esquema_tmp_informe --bd-tamanos donofrio_perf   # docs/informe/04_02_diccionario_datos.md y anexo_diccionario_datos.md
scripts/esquema_limpio.sh borrar                                  # borra la BD temporal
```

`diagrama_er.py` también acepta `--sin-render` (solo escribe los `.puml`). `diccionario_datos.py` acepta `--csv ruta.csv` para volcar todo el diccionario a un CSV (Excel lo abre) y `--bd-tamanos` (opcional) para contar filas en una BD con datos. Solo usan Python 3 y Docker, sin librerías. El ER usa PlantUML con Graphviz en vez de SchemaSpy porque deja filtrar las tablas del núcleo y no descarga otra imagen.
