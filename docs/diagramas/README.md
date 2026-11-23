# Diagramas

| Carpeta | Contenido | Herramienta | Responsable |
|---|---|---|---|
| `bpmn/` | BPMN AS-IS: venta B2B, liquidación del heladero y compra de insumos (Evelyn); producción y calidad, y recepción y despacho con cadena de frío (Orlando) (`.bpmn`, `.svg`, `.png`) | `generar_bpmn.py` + bpmn.io | Evelyn y Orlando |
| `arquitectura/` | Arquitectura empresarial AS-IS y TO-BE (4.1.3) e infraestructura tecnológica (4.3.1) (`.svg`, `.png`) | `generar_arquitectura.py` | Orlando |
| `cu/` | Casos de uso de ventas, heladeros y gerencia (`.puml` y `.png`) | PlantUML | Evelyn |

Los datos de procesos son ficticios y verosímiles (supuesto S7 del plan).

## BPMN

Los procesos se definen en [`generar_bpmn.py`](generar_bpmn.py) (carriles, tareas y flujos). El script escribe el `.bpmn` (se abre y se edita en <https://demo.bpmn.io>) y un `.svg` con la misma disposición. No necesita librerías.

```bash
python3 docs/diagramas/generar_bpmn.py
```

El PNG sale del SVG. Con Docker, sin instalar nada en tu PC:

```bash
docker run --rm -v "$PWD/docs/diagramas/bpmn":/b --entrypoint sh python:3.12-slim -c \
  "apt-get update -qq && apt-get install -y -qq librsvg2-bin fonts-dejavu-core && cd /b && for f in *.svg; do rsvg-convert \$f -o \${f%.svg}.png; done && chown $(id -u):$(id -g) *.png"
```

## Casos de uso

```bash
docker run --rm -u $(id -u):$(id -g) -v "$PWD/docs/diagramas/cu":/data plantuml/plantuml:latest -tpng -charset UTF-8 /data/*.puml
```

## Arquitectura e infraestructura

Los dos diagramas se definen en [`generar_arquitectura.py`](generar_arquitectura.py) y se escriben como `.svg` en `arquitectura/`. No necesita librerías.

```bash
python3 docs/diagramas/generar_arquitectura.py
docker run --rm -v "$PWD/docs/diagramas/arquitectura":/b --entrypoint sh python:3.12-slim -c \
  "apt-get update -qq && apt-get install -y -qq librsvg2-bin fonts-dejavu-core && cd /b && for f in *.svg; do rsvg-convert \$f -o \${f%.svg}.png; done && chown $(id -u):$(id -g) *.png"
```
