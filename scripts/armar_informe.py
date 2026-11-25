#!/usr/bin/env python3
"""Arma el informe final (DOCX y PDF) sobre la plantilla del docente, desde los Markdown de docs/informe/.

CÓMO CORRERLO (no necesita Docker ni Odoo)
------------------------------------------
Requisitos: Python 3.10+, LibreOffice (``soffice``), ``pdftotext`` y ``pdftoppm`` (poppler-utils)
y, para los 5 diagramas Mermaid, Node con ``@mermaid-js/mermaid-cli`` (opcional: sin él, esos 5
diagramas salen como bloque de código).

    python3 -m venv ~/informe_venv && ~/informe_venv/bin/pip install python-docx lxml Pillow markdown-it-py
    # opcional, para los diagramas Mermaid (se instala fuera del repo):
    mkdir -p ~/informe_mmdc && cd ~/informe_mmdc && npm init -y && PUPPETEER_SKIP_DOWNLOAD=1 npm i @mermaid-js/mermaid-cli
    # desde la raíz del repo:
    ~/informe_venv/bin/python scripts/armar_informe.py

Entradas:
  * docs/informe/*.md (contenido), docs/capturas/ y docs/diagramas/ (imágenes).
  * La plantilla del docente ``docs/TEMPLATE - INFORME PROYECTO FINAL.docx``. Está ignorada por git: si no
    está en el checkout actual, el script la busca en el checkout principal (``git worktree``), o se
    indica con ``--plantilla RUTA``.
Salidas (carpeta docs/informe/entrega/):
  * informe_final.pdf   -> se sube al repositorio.
  * informe_final.docx  -> deriva de la plantilla del docente: está ignorado por git (.gitignore).

Detalles:
  * Los índices de contenido, figuras y tablas se escriben como campos de Word con los números de página
    reales: el script arma el DOCX, lo exporta a PDF con LibreOffice, lee en qué página cae cada título y
    cada leyenda, y vuelve a armar (2 o 3 pasadas hasta que los números no cambian).
  * LibreOffice (snap) solo lee carpetas visibles de HOME: la carpeta de trabajo por defecto es
    ~/informe_build (``--trabajo`` la cambia). Se puede borrar al terminar.
  * Cuando el equipo llene los marcadores [PENDIENTE: ...] en los .md, se vuelve a correr este script.
  * ``--con-diccionario-completo`` agrega el anexo generado de 661 tablas (unas 300 páginas más). Por
    defecto ese anexo no se copia al PDF y se enlaza a GitHub.
  * Los datos de la portada que no están en el repositorio (ciclo, CUI y apellidos) salen como [PENDIENTE]:
    se completan en la constante PORTADA de este archivo y se vuelve a correr.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.text.paragraph import Paragraph
from lxml import etree
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INFORME = ROOT / "docs" / "informe"
GITHUB = "https://github.com/orlando572/erp-donofrio"
PLANTILLA = "TEMPLATE - INFORME PROYECTO FINAL.docx"

# ---------------------------------------------------------------- portada (datos que no están en el repo)
PORTADA = {
    "titulo": "ERP para D'Onofrio con Odoo 19",
    "github": GITHUB,
    "ciclo": None,  # None -> [PENDIENTE: ciclo]; por ejemplo "VI"
    "fecha": "27 de noviembre de 2026",
    # (CUI, apellidos, nombres); None -> [PENDIENTE]. Orden: por apellidos, cuando se conozcan.
    "integrantes": [
        (None, None, "Evelyn"),
        (None, None, "Orlando"),
    ],
}

# Historial de revisiones: una fila por sprint (solo las 4 primeras columnas de la plantilla).
HISTORIAL = [
    ("23/11/2026", "v0.1", "Evelyn, Orlando", "Sprint 1: aspectos generales, análisis de sistemas y procesos AS-IS, arquitectura, requerimientos (borrador)."),
    ("24/11/2026", "v0.2", "Evelyn, Orlando", "Sprint 2: procesos TO-BE, casos de uso, wireframes y mockups, ER y diccionario de datos."),
    ("25/11/2026", "v0.3", "Evelyn, Orlando", "Sprint 3: núcleo v1.0.0 (back-end, seguridad, réplica, pruebas, despliegue, repositorio)."),
    ("25/11/2026", "v0.4", "Evelyn, Orlando", "Sprint 4: Fase 2 completa (M1 calidad, M2 heladeros, M3 cadena de frío, M4 tablero), v1.1.0 a v1.4.0."),
    ("27/11/2026", "v1.0", "Evelyn, Orlando", "Cierre: informe final para la entrega, con los marcadores [PENDIENTE] que el equipo llena."),
]

TEXT_W = 8504      # ancho útil en twips (A4, márgenes de 3 cm)
LAND_W = 14570     # ancho útil en horizontal (márgenes de 2 cm)
IMG_MAX_W_CM = 14.9
IMG_MAX_H_CM = 19.5
EMU_CM = 360000

# ---------------------------------------------------------------- estructura del informe (orden de la plantilla)
# f: archivo; h1: 'drop' (el título del .md lo pone el script) | 'keep' (el título del .md es un apartado);
# quote: 'meta' (quita solo la línea «Estado») | 'none' (quita todo el bloque inicial);
# shift: suma al nivel por número de sección; key/title/level: ajustes; retitle: cambia títulos de apartados.
F = lambda f, **kw: dict(f=f, **kw)  # noqa: E731

PLAN = [
    dict(title="1. RESUMEN", level=1, files=[F("01_resumen", h1="drop", quote="none", skip_h2=["Resumen"])]),
    dict(title="2. ABSTRACT", level=1, files=[F("02_abstract", h1="drop", quote="none", skip_h2=["Abstract"])]),
    dict(title="3. ASPECTOS GENERALES", level=1, files=[F("03_aspectos_generales", h1="drop")]),
    dict(title="4. PLANIFICACIÓN Y FRONT-END", level=1, sub=[
        dict(title="4.1 ANÁLISIS EMPRESARIAL", level=2, files=[
            F("04_01_analisis_sistemas", h1="drop"),
            F("04_01_arquitectura_empresarial", h1="keep", labels=False),
            F("04_01_04_oportunidades_innovacion", h1="keep")]),
        dict(title="4.2 PLANIFICACIÓN DE PROYECTOS", level=2, files=[
            F("04_02_requerimientos_funcionales", h1="drop"),
            F("04_02_requerimientos_no_funcionales", h1="keep"),
            F("04_02_casos_de_uso", h1="keep", labels=False),
            F("04_02_modelo_de_datos", h1="drop"),
            F("04_02_diccionario_datos", h1="keep", caption_prefix="Diccionario de datos: ", title="Diccionario de datos del núcleo (tablas centrales)", level=4, key="4.2.8.5"),
            F("04_02_calendarizacion", h1="keep"),
            F("04_02_10_a_12_scrum", h1="drop")]),
        dict(title="4.3 GESTIÓN DE DESARROLLO DE SOFTWARE", level=2, files=[
            F("04_03_infraestructura", h1="drop"), F("04_03_04_ides_y_gestion_proyectos", h1="drop")]),
        dict(title="4.4 DISEÑO DE PROTOTIPOS", level=2, files=[F("04_04_prototipos", h1="drop")]),
        dict(title="4.5 GESTIÓN DE RIESGOS", level=2, files=[
            F("04_05_riesgos_despliegue_y_mantenimiento", h1="drop",
              retitle={"Escalas y método": "4.5.1 Plan de gestión de riesgos: escalas y método"}),
            F("04_05_02_riesgos_desarrollo", h1="keep")]),
        dict(title="4.6 DESARROLLO FRONT-END", level=2, files=[
            F("04_06_prototipos_web_y_reportes", h1="drop"), F("04_06_wpo", h1="keep")]),
        dict(title="4.7 ACUERDOS DE NIVELES DE SERVICIO", level=2, files=[F("04_07_acuerdos_de_nivel_de_servicio", h1="drop")]),
    ]),
    dict(title="5. BACK-END Y DESPLIEGUE", level=1, files=[
        F("05_01_a_05_06_backend", h1="drop"),
        F("05_05_modulo_donofrio_calidad", h1="keep", shift=1),
        F("05_05_modulo_donofrio_heladeros", h1="keep", shift=1),
        F("05_05_modulo_donofrio_frio", h1="keep", shift=1),
        F("05_05_modulo_donofrio_tablero", h1="keep", shift=1),
        F("05_07_a_05_09_arquitectura_bd", h1="drop"),
        F("05_10_a_05_12_seguridad", h1="drop"),
        F("05_13_a_05_14_pruebas", h1="drop"),
        F("05_15_despliegue", h1="keep")]),
    dict(title="6. DOCUMENTACIÓN DE LA SOLUCIÓN O APLICACIÓN", level=1, files=[
        F("06_01_a_06_03_equipo_sprints_y_project", h1="drop"),
        F("06_04_a_06_06_repositorio", h1="drop"),
        F("06_07_a_06_08_commits_e_issues", h1="drop"),
        F("06_09_a_06_13_pruebas", h1="drop"),
        F("06_12_usabilidad", h1="keep")]),
    dict(title="7. CONCLUSIONES", level=1, files=[F("07_conclusiones", h1="drop")]),
    dict(title="8. RECOMENDACIONES", level=1, files=[F("08_recomendaciones", h1="drop"), F("08_01_recomendaciones_negocio", h1="drop")]),
    dict(title="9. REFERENCIAS Y BIBLIOGRAFÍA", level=1, files=[F("09_referencias", h1="drop", hang_under="9.2")]),
    dict(title="10. ANEXOS", level=1, files=[
        F("anexo_10_01_fichas_rf", h1="keep"),
        F("anexo_10_02_fichas_rnf", h1="keep"),
        F("anexo_10_03_solicitud_servicio", h1="keep"),
        F("anexo_10_04_rfc", h1="keep"),
        F("anexo_10_05_incidente", h1="keep"),
        F("anexo_10_06_soa_iso27001", h1="keep"),
        F("trazabilidad", h1="keep", title="10.7 Matriz de trazabilidad: requisito, HU, PR, módulo, prueba y evidencia"),
        F("anexo_diccionario_datos", h1="keep", title="10.8 Diccionario de datos del resto del esquema", optional=True)]),
]

# ---------------------------------------------------------------- utilidades
WARN: list[str] = []
UNRESOLVED: dict[str, int] = {}


def warn(msg: str) -> None:
    WARN.append(msg)


def el(tag: str, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def sub(parent, tag: str, **attrs):
    e = el(tag, **attrs)
    parent.append(e)
    return e


def mk_rpr(b=False, i=False, code=False, sz=None, color=None, hl=False, strike=False, link=False, caps=False):
    rpr = OxmlElement("w:rPr")
    if link:
        sub(rpr, "w:rStyle", val="Hipervnculo")
    if code:
        sub(rpr, "w:rFonts", ascii="Courier New", hAnsi="Courier New", cs="Courier New")
    if b:
        sub(rpr, "w:b")
        sub(rpr, "w:bCs")
    if i:
        sub(rpr, "w:i")
        sub(rpr, "w:iCs")
    if strike:
        sub(rpr, "w:strike")
    if color:
        sub(rpr, "w:color", val=color)
    if sz:
        sub(rpr, "w:sz", val=sz)
        sub(rpr, "w:szCs", val=sz)
    if hl:
        sub(rpr, "w:highlight", val="yellow")
    sub(rpr, "w:lang", val="es-PE")
    return rpr


def mk_run(text: str, **fmt):
    r = OxmlElement("w:r")
    r.append(mk_rpr(**fmt))
    parts = text.split("\n")
    for n, part in enumerate(parts):
        if n:
            r.append(OxmlElement("w:br"))
        t = OxmlElement("w:t")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = part
        r.append(t)
    return r


def mk_br_run():
    r = OxmlElement("w:r")
    r.append(OxmlElement("w:br"))
    return r


def mk_ppr(style=None, keep_next=False, keep_lines=False, page_break=False, border_left=False, shd=None,
           tabs=None, spacing=None, ind=None, jc=None):
    ppr = OxmlElement("w:pPr")
    if style:
        sub(ppr, "w:pStyle", val=style)
    if keep_next:
        sub(ppr, "w:keepNext")
    if keep_lines:
        sub(ppr, "w:keepLines")
    if page_break:
        sub(ppr, "w:pageBreakBefore")
    if border_left:
        b = sub(ppr, "w:pBdr")
        sub(b, "w:left", val="single", sz=12, space=6, color="9A9A9A")
    if shd:
        sub(ppr, "w:shd", val="clear", color="auto", fill=shd)
    if tabs:
        t = sub(ppr, "w:tabs")
        for pos, kind, leader in tabs:
            a = dict(val=kind, pos=pos)
            if leader:
                a["leader"] = leader
            sub(t, "w:tab", **a)
    if spacing:
        sub(ppr, "w:spacing", **{k: v for k, v in spacing.items() if v is not None})
    if ind:
        sub(ppr, "w:ind", **{k: v for k, v in ind.items() if v is not None})
    if jc:
        sub(ppr, "w:jc", val=jc)
    return ppr


def mk_p(ppr=None):
    p = OxmlElement("w:p")
    if ppr is not None:
        p.append(ppr)
    return p


def fld_runs(instr: str, cached: str, **fmt):
    """Campo complejo: begin / instrText / separate / texto en caché / end."""
    out = []
    for kind in ("begin", None, "separate", "txt", "end"):
        r = OxmlElement("w:r")
        r.append(mk_rpr(**fmt))
        if kind == "begin" or kind == "separate" or kind == "end":
            r.append(el("w:fldChar", fldCharType=kind))
        elif kind is None:
            t = OxmlElement("w:instrText")
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            t.text = f" {instr} "
            r.append(t)
        else:
            t = OxmlElement("w:t")
            t.text = cached
            r.append(t)
        out.append(r)
    return out


def plain_text(node) -> str:
    """Texto plano de un nodo inline (sin marcas de Markdown)."""
    if node.type == "text":
        return node.content
    if node.type == "code_inline":
        return node.content
    if node.type in ("softbreak", "hardbreak"):
        return " "
    if node.type == "html_inline":
        return " " if re.match(r"<br\s*/?>", node.content) else ""
    if node.type == "image":
        return node.content or ""
    return "".join(plain_text(c) for c in node.children)


def real_kids(inline):
    """Hijos de un nodo inline sin los textos vacíos que markdown-it deja junto a negritas y cursivas."""
    return [k for k in inline.children if not (k.type == "text" and not k.content)]


def node_text(node) -> str:
    return re.sub(r"\s+", " ", plain_text(node)).strip()


# ---------------------------------------------------------------- numeración de apartados
NUM_RE = re.compile(r"^(?:Anexo\s+)?(\d+[a-z]?(?:\.\d+[a-z]?)*)\.?\s+(.*)$")
CAPH_RE = re.compile(r"^(Tabla|Figura|Ilustración)\s+([0-9A-Z][\w.\-]*?)\s*[.:]\s+(.*)$", re.S)
PAREN_RE = re.compile(r"\s*\(((?:tabla|ilustración|figura)[^)]*)\)\s*$", re.I)
CONT_RE = re.compile(r"^(\d+(?:\.\d+)*)\s+\(continuación\)\s+(.*)$")


def parse_num(text: str, md_level: int):
    m = NUM_RE.match(text)
    if not m:
        return None
    num = m.group(1)
    if "." not in num and md_level > 1:  # «1. Cuándo se usa»: lista, no apartado
        return None
    if "." not in num and re.fullmatch(r"\d+", num) and not text.startswith(num + "."):
        return None
    return num


def num_key(num: str):
    out = []
    for part in num.split("."):
        m = re.match(r"(\d+)([a-z]?)$", part)
        out.append((int(m.group(1)), m.group(2)) if m else (0, part))
    return tuple(out)


# ---------------------------------------------------------------- el armado
class Builder:
    def __init__(self, template: Path, labels: dict | None, pages: dict | None, opts):
        self.opts = opts
        self.doc = docx.Document(str(template))
        self.labels_in = labels or {}
        self.labels_out: dict = {}
        self.pages = pages or {}
        self.heads: list = []      # (nivel, texto, bookmark)
        self.figs: list = []       # (n, texto, bookmark)
        self.tabs: list = []       # (n, texto, bookmark)
        self.n_fig = 0
        self.n_tab = 0
        self.bm_id = 5000
        self.bm_seq = 0
        self.pending = None        # (kind, label, titulo) de un encabezado «Tabla N: ...»
        self.head_labels: list = []
        self.cur_head = ""
        self.tab_count_by_head: dict = {}
        self.tab_seen_by_head: dict = {}
        self.cur_file = None
        self.cur_dir = INFORME
        self.stack = [(0, 1)]
        self.shift = 0
        self.cfg: dict = {}
        self.first_h1 = True
        self.body = self.doc.element.body
        self.sect = self.body.find(qn("w:sectPr"))
        self.hyper_cache: dict = {}
        self.split_done = False
        self.hang = False
        self.land_open = False
        self.land_close = None
        self.mmd_dir = Path(opts.trabajo) / "mermaid"
        self.mmd_dir.mkdir(parents=True, exist_ok=True)
        self.md = MarkdownIt("commonmark").enable("table").enable("strikethrough")

    # ----- inserción
    def put(self, el_):
        self.sect.addprevious(el_)
        return el_

    def new_bm(self, prefix="_Toc9"):
        self.bm_seq += 1
        self.bm_id += 1
        return f"{prefix}{self.bm_seq:06d}", self.bm_id

    # ----- texto con marcas
    def text_runs(self, text, fmt, raw=False):
        """Devuelve lista de elementos (runs) para un texto: resalta [PENDIENTE] y renumera referencias."""
        out = []
        if not fmt.get("code") and not raw:
            text = self.fix_refs(text)
        text = text.replace("↔", "↔\ufe0e").replace("⇄", "⇄\ufe0e")
        for piece in re.split(r"(\[PENDIENTE[^\]]*\])", text):
            if not piece:
                continue
            f = dict(fmt)
            if piece.startswith("[PENDIENTE"):
                f["hl"] = True
                f["b"] = True
            out.append(mk_run(piece, **f))
        return out

    REF_RE = re.compile(r"\b(Tabla|tabla|Figura|figura|Ilustración|ilustración)\s+(\d+(?:\.\d+)*(?:-\d+|-?[a-z])?(?![\w]))")

    def fix_refs(self, text):
        if not self.labels_in:
            return text

        def rep(m):
            word, label = m.group(1), m.group(2).lower()
            kind = "tabla" if word.lower() == "tabla" else "fig"
            new = self.labels_in.get((kind, label))
            if new is None:
                UNRESOLVED[f"{word} {m.group(2)}"] = UNRESOLVED.get(f"{word} {m.group(2)}", 0) + 1
                return m.group(0)
            if kind == "tabla":
                return f"{word} {new}"
            return ("Ilustración " if word[0].isupper() else "ilustración ") + str(new)

        return self.REF_RE.sub(rep, text)

    def link_target(self, href, shown):
        """Convierte un enlace del .md en (url|None). None -> solo texto."""
        if re.match(r"^(https?:|mailto:)", href):
            return href
        if href.startswith("#"):
            return None
        path_part = href.split("#")[0]
        if not path_part:
            return None
        target = (self.cur_dir / urllib.parse.unquote(path_part)).resolve()
        try:
            rel = target.relative_to(ROOT)
        except ValueError:
            warn(f"enlace fuera del repo en {self.cur_file}: {href}")
            return None
        if not target.exists():
            warn(f"enlace roto en {self.cur_file}: {href}")
            return None
        if target.parent == INFORME and target.suffix == ".md":
            if shown.strip("` ").endswith(".md"):
                return f"{GITHUB}/blob/develop/{rel.as_posix()}"
            return None  # referencia cruzada interna: queda como texto (el apartado está en este informe)
        if rel.as_posix().startswith("docs/TEMPLATE") or rel.as_posix().startswith("docs/TF_"):
            return None
        kind = "tree" if target.is_dir() else "blob"
        return f"{GITHUB}/{kind}/develop/{rel.as_posix()}"

    def inline_runs(self, node, fmt=None, out=None):
        fmt = dict(fmt or {})
        out = [] if out is None else out
        for c in node.children:
            t = c.type
            if t == "text":
                out += self.text_runs(c.content, fmt)
            elif t == "code_inline":
                f = dict(fmt)
                f["code"] = True
                f["sz"] = f.get("sz") and max(f["sz"] - 2, 12) or None
                out += self.text_runs(c.content, f)
            elif t in ("softbreak",):
                out.append(mk_run(" ", **fmt))
            elif t == "hardbreak":
                out.append(mk_br_run())
            elif t == "html_inline":
                if re.match(r"<br\s*/?>", c.content):
                    out.append(mk_br_run())
            elif t == "strong":
                self.inline_runs(c, {**fmt, "b": True}, out)
            elif t == "em":
                self.inline_runs(c, {**fmt, "i": True}, out)
            elif t == "s":
                self.inline_runs(c, {**fmt, "strike": True}, out)
            elif t == "link":
                href = c.attrs.get("href", "")
                shown = node_text(c)
                url = self.link_target(href, shown)
                if url is None:
                    self.inline_runs(c, fmt, out)
                else:
                    rid = self.doc.part.relate_to(url, RT.HYPERLINK, is_external=True)
                    h = OxmlElement("w:hyperlink")
                    h.set(qn("r:id"), rid)
                    h.set(qn("w:history"), "1")
                    for r in self.inline_runs(c, {**fmt, "link": True}, []):
                        h.append(r)
                    out.append(h)
            elif t == "image":
                out.append(("IMG", c))
            else:
                self.inline_runs(c, fmt, out)
        return out

    # ----- párrafos
    def para(self, node_inline, *, style="Textoindependiente", ctx=None, sz=22, **ppr_kw):
        ctx = ctx or {}
        ind_left = ctx.get("indent", 0)
        ind = {"left": ind_left + (360 if ctx.get("quote") else 0)} if (ind_left or ctx.get("quote")) else None
        ppr_args = dict(style=style, spacing=dict(before=0, after=100, line=252, lineRule="auto"),
                        ind=ind, border_left=bool(ctx.get("quote")))
        ppr_args.update(ppr_kw)
        p = mk_p(mk_ppr(**ppr_args))
        fmt = {"sz": sz}
        if ctx.get("quote"):
            fmt["color"] = "404040"
        runs = self.inline_runs(node_inline, fmt)
        pend_imgs = []
        for r in runs:
            if isinstance(r, tuple):
                pend_imgs.append(r[1])
            else:
                p.append(r)
        return p, pend_imgs

    # ----- imágenes
    def resolve_img(self, src):
        path = (self.cur_dir / urllib.parse.unquote(src)).resolve()
        if not path.exists():
            warn(f"imagen no encontrada en {self.cur_file}: {src}")
            return None
        return path

    def add_picture(self, p_el, path: Path, max_w_cm, max_h_cm):
        try:
            with Image.open(path) as im:
                w, h = im.size
        except Exception as e:  # noqa: BLE001
            warn(f"imagen ilegible {path}: {e}")
            return False
        w_emu, h_emu = w * 9525, h * 9525
        scale = min(max_w_cm * EMU_CM / w_emu, max_h_cm * EMU_CM / h_emu, 1.5)
        if self.opts.sin_imagenes:
            return True
        para = Paragraph(p_el, self.doc._body)
        run = para.add_run()
        run.add_picture(str(path), width=int(w_emu * scale), height=int(h_emu * scale))
        return True

    def figure_block(self, path: Path, ctx, caption=None, alt=""):
        try:
            with Image.open(path) as im:
                w, h = im.size
        except Exception:  # noqa: BLE001
            w, h = 0, 0
        land = w >= 2000 and w / max(h, 1) >= 1.2 and not ctx.get("indent")
        if land:
            self.section_break(landscape=True)
        p = mk_p(mk_ppr(jc="center", keep_next=True, spacing=dict(before=60, after=60)))
        mw, mh = (25.2, 15.0) if land else (IMG_MAX_W_CM, IMG_MAX_H_CM)
        if self.add_picture(p, path, mw, mh):
            self.put(p)
            self.caption("fig", caption, alt)
        if land:
            self.section_break(landscape=False)

    # ----- leyendas
    def caption(self, kind, text, fallback=""):
        pend = self.pending
        label = None
        pend_prefix = self.cfg.get("caption_prefix", "")
        title = (text or "").strip()
        if pend and pend[0] == kind:
            _, label, ptitle = pend
            title = ptitle
            self.pending = None
        if not title:
            title = fallback or self.cur_head or ("Tabla" if kind == "tabla" else "Figura")
        # Solo la primera oración va a la leyenda; el resto, a una nota.
        note = ""
        if len(title) > 110:
            m = re.match(r"^(.{25,200}?[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡«`(])(.*)$", title, re.S)
            if m:
                title, note = m.group(1), m.group(2)
        title = title.rstrip(".")
        if len(title) > 230:
            title = title[:227].rsplit(" ", 1)[0] + "…"
        if kind == "tabla" and pend_prefix and label:
            title = pend_prefix + title
        if kind == "tabla":
            self.n_tab += 1
            n, word, lst = self.n_tab, "Tabla", self.tabs
            seq = "Tabla"
        else:
            self.n_fig += 1
            n, word, lst = self.n_fig, "Ilustración", self.figs
            seq = "Ilustración"
        regs = []
        if label:
            regs.append((kind, label.lower()))
        for hk, hl in list(self.head_labels):
            if hk == kind:
                regs.append((kind, hl.lower()))
                self.head_labels.remove((hk, hl))
        for k in regs:
            if k in self.labels_out and self.labels_out[k] != n:
                self.labels_out[k] = None   # ambiguo
            else:
                self.labels_out[k] = n
        bm, bid = self.new_bm()
        lst.append((n, title, bm))
        p = mk_p(mk_ppr(style="Descripcin", jc="center", spacing=dict(before=40, after=160, line=240, lineRule="auto")))
        p.append(el("w:bookmarkStart", id=bid, name=bm))
        p.append(mk_run(f"{word} ", sz=19, i=True))
        for r in fld_runs(f"SEQ {seq} \\* ARABIC", str(n), sz=19, i=True):
            p.append(r)
        for r in self.text_runs(f". {title}", {"sz": 19, "i": True}, raw=True):
            p.append(r)
        p.append(el("w:bookmarkEnd", id=bid))
        self.put(p)
        if note:
            pn, _ = self.para(self.inline_of(note), ctx={}, sz=18, jc="center")
            self.put(pn)

    def inline_of(self, text):
        n = self.md.parse(text)
        return SyntaxTreeNode(n).children[0].children[0]

    # ----- encabezados
    def heading(self, level, text, page_break=None):
        level = max(1, min(level, 5))
        bm, bid = self.new_bm()
        disp = text.upper() if level == 1 else text
        if level <= 3:
            self.heads.append((level, disp, bm))
        sizes = {1: (28, None), 2: (26, "2F5496"), 3: (24, "2F5496"), 4: (22, "434343"), 5: (21, "595959")}
        sz, color = sizes[level]
        ppr = mk_ppr(style=f"Ttulo{level}", page_break=(level == 1 if page_break is None else page_break),
                     spacing=dict(before=0 if level == 1 else (300 if level == 2 else 220), after=120, line=240, lineRule="auto"))
        p = mk_p(ppr)
        p.append(el("w:bookmarkStart", id=bid, name=bm))
        p.append(mk_run(disp, b=True, i=(level == 5), sz=sz, color=color))
        p.append(el("w:bookmarkEnd", id=bid))
        self.put(p)
        self.cur_head = re.sub(r"^\d+(?:\.\d+)*[a-z]?(?:\.\d+[a-z]?)*\.?\s+", "", text)

    # ----- bloques
    def block(self, node, ctx):
        t = node.type
        if t == "heading":
            return self.on_heading(node)
        if t == "paragraph":
            return self.on_paragraph(node, ctx)
        if t in ("bullet_list", "ordered_list"):
            return self.on_list(node, ctx)
        if t == "blockquote":
            for c in node.children:
                self.block(c, {**ctx, "quote": True})
            return None
        if t in ("fence", "code_block"):
            return self.on_code(node, ctx)
        if t == "table":
            return self.on_table(node, ctx)
        if t == "hr":
            return None
        if t == "html_block":
            return None
        warn(f"bloque no manejado {t} en {self.cur_file}")
        return None

    def on_heading(self, node):
        md = int(node.tag[1])
        text = node_text(node)
        m = CAPH_RE.match(text)
        if m:
            kind = "tabla" if m.group(1) == "Tabla" else "fig"
            self.pending = (kind, m.group(2), m.group(3).strip())
            return
        if md == 1 and not self.first_h1:
            md = 2
        self.first_h1 = False
        text = self.cfg.get("retitle", {}).get(text, text)
        if self.cfg.get("title") and md == 1:
            text = self.cfg["title"]
        # etiquetas en paréntesis: (tabla 14)
        pm = PAREN_RE.search(text)
        if pm:
            text = text[:pm.start()].rstrip()
            if self.cfg.get("labels", True):
                for k, lab in re.findall(r"(tabla|ilustración|figura)\s+(\d+[a-z]?)", pm.group(1), re.I):
                    self.head_labels.append(("tabla" if k.lower() == "tabla" else "fig", lab))
        cm = CONT_RE.match(text)
        while self.stack and self.stack[-1][0] >= md:
            self.stack.pop()
        parent = self.stack[-1][1] if self.stack else 1
        if cm:
            depth = len(cm.group(1).split("."))
            lvl = min(depth + self.shift + 1, 5)
            text = cm.group(2)
        else:
            num = parse_num(text, md)
            if "level" in self.cfg and md == 1:
                lvl = self.cfg["level"]
            elif num:
                lvl = min(len(num.split(".")) + self.shift, 5)
                if lvl <= parent and md > 1:
                    lvl = min(parent + 1, 5)
            else:
                lvl = min(parent + 1, 5)
        text = re.sub(r"^Anexo\s+(\d)", r"\1", text)
        self.stack.append((md, lvl))
        self.pending = None
        self.hang = bool(self.cfg.get("hang_under")) and text.startswith(self.cfg["hang_under"])
        self.heading(lvl, text)

    def on_paragraph(self, node, ctx):
        inline = node.children[0] if node.children else None
        if inline is None:
            return
        kids = real_kids(inline)
        if len(kids) == 1 and kids[0].type == "strong":
            m = CAPH_RE.match(node_text(kids[0]))
            if m:  # «**Tabla 14. Métricas clave**»: rótulo escrito a mano; la leyenda la pone el script
                self.pending = ("tabla" if m.group(1) == "Tabla" else "fig", m.group(2), m.group(3).strip())
                return
        imgs = [k for k in kids if k.type == "image"]
        if imgs and all(k.type in ("image", "softbreak") for k in kids):
            for k in imgs:
                path = self.resolve_img(k.attrs.get("src", ""))
                if path is None:
                    continue
                self.figure_block(path, ctx, alt=k.content or "")
            return
        extra = {}
        if self.hang and not ctx.get("quote"):
            extra = dict(ind={"left": 567, "hanging": 567})
        p, pend = self.para(inline, ctx=ctx, **extra)
        self.put(p)
        for k in pend:
            path = self.resolve_img(k.attrs.get("src", ""))
            if path:
                self.figure_block(path, ctx, alt=k.content or "")

    def on_list(self, node, ctx):
        ordered = node.type == "ordered_list"
        n = int(node.attrs.get("start", 1)) if ordered else 0
        base = ctx.get("indent", 0)
        for li in node.children:
            first = True
            for c in li.children:
                if c.type == "paragraph":
                    inline = c.children[0]
                    marker = f"{n}." if ordered else "•"
                    # casillas de verificación
                    first_txt = node_text(inline)
                    box = None
                    if first_txt.startswith("[ ]"):
                        box = "☐"
                    elif first_txt.lower().startswith("[x]"):
                        box = "☑"
                    ctx2 = {**ctx, "indent": base + 360}
                    p, pend = self.para(inline, ctx=ctx2, style="Textoindependiente",
                                        ind={"left": base + 360 + (360 if ctx.get("quote") else 0), "hanging": 300} if first else
                                        {"left": base + 360 + (360 if ctx.get("quote") else 0)})
                    if first:
                        # tabulación tras la viñeta
                        runs = [mk_run(marker, sz=22), mk_run("\t", sz=22)]
                        first_run_idx = len(p.findall(qn("w:pPr")))
                        for r in reversed(runs):
                            p.insert(first_run_idx, r)
                        tabs = el("w:tabs")
                        sub(tabs, "w:tab", val="left", pos=base + 360 + (360 if ctx.get("quote") else 0))
                        ppr = p.find(qn("w:pPr"))
                        sp = ppr.find(qn("w:spacing"))
                        sp.addprevious(tabs)
                        if box:
                            # quitar «[ ] » del primer texto
                            for t in p.iter(qn("w:t")):
                                if t.text and t.text.lstrip().startswith(("[ ]", "[x]", "[X]")):
                                    t.text = box + t.text.lstrip()[3:]
                                    break
                    self.put(p)
                    for k in pend:
                        path = self.resolve_img(k.attrs.get("src", ""))
                        if path:
                            self.figure_block(path, ctx, alt=k.content or "")
                    first = False
                elif c.type in ("bullet_list", "ordered_list"):
                    self.on_list(c, {**ctx, "indent": base + 360})
                else:
                    self.block(c, {**ctx, "indent": base + 360})
            n += 1

    def on_code(self, node, ctx):
        code = node.content.rstrip("\n").replace("\t", "    ")
        info = (node.info or "").strip() if hasattr(node, "info") else ""
        if info == "mermaid" and self.render_mermaid(code, ctx):
            return
        sz = 15 if max((len(l) for l in code.split("\n")), default=0) > 95 else 16
        lines = code.split("\n")
        for n, line in enumerate(lines):
            p = mk_p(mk_ppr(shd="F2F2F2", spacing=dict(before=0, after=0, line=240, lineRule="auto"),
                            ind={"left": 120 + ctx.get("indent", 0), "right": 60}, keep_lines=True,
                            keep_next=(n < min(len(lines) - 1, 3))))
            p.append(mk_run(line if line else " ", code=True, sz=sz))
            self.put(p)
        sp = mk_p(mk_ppr(spacing=dict(before=0, after=80, line=120, lineRule="auto")))
        self.put(sp)

    def render_mermaid(self, code, ctx):
        mmdc = self.opts.mmdc
        if not mmdc:
            warn(f"mermaid sin mmdc en {self.cur_file}: sale como código")
            return False
        h = hashlib.sha1(code.encode()).hexdigest()[:12]
        png = self.mmd_dir / f"{h}.png"
        if not png.exists():
            src = self.mmd_dir / f"{h}.mmd"
            src.write_text(code, encoding="utf8")
            cfg = self.mmd_dir / "puppeteer.json"
            cfg.write_text('{"executablePath":"%s","args":["--no-sandbox","--disable-gpu"]}' % self.opts.chrome)
            r = subprocess.run([mmdc, "-p", str(cfg), "-i", str(src), "-o", str(png), "-s", "2", "-w", "1400", "-b", "white"],
                               capture_output=True, text=True)
            if r.returncode != 0 or not png.exists():
                warn(f"mermaid falló en {self.cur_file}: {r.stderr[-200:]}")
                return False
        self.figure_block(png, ctx, alt="")
        return True

    # ----- tablas
    def on_table(self, node, ctx):
        head_rows, body_rows = [], []
        for part in node.children:
            for tr in part.children:
                cells = tr.children
                (head_rows if part.type == "thead" else body_rows).append(cells)
        rows = head_rows + body_rows
        ncols = max(len(r) for r in rows)
        aligns = []
        for c in (head_rows[0] if head_rows else rows[0]):
            st = (c.attrs.get("style") or "")
            aligns.append("center" if "center" in st else ("right" if "right" in st else None))
        aligns += [None] * (ncols - len(aligns))

        def cell_text(c):
            return node_text(c)

        n_img = sum(1 for r in body_rows for c in r if any(k.type == "image" for k in c.children[0].children)) if body_rows else 0
        n_cells = sum(len(r) for r in body_rows)
        is_grid = n_cells > 0 and n_img >= 0.5 * n_cells
        # texto de la leyenda
        pend = self.pending
        if pend and pend[0] == ("fig" if is_grid else "tabla"):
            pass
        row_chars = [sum(len(cell_text(c)) for c in r) for r in rows]
        avg_chars = sum(row_chars) / max(len(row_chars), 1)
        wide = (not is_grid) and (ncols >= 7 or (ncols >= 5 and avg_chars > 320) or (ncols >= 4 and avg_chars > 700))
        if wide:
            sz = 17 if ncols <= 6 else (16 if ncols <= 8 else 15)
        else:
            sz = 18 if ncols <= 4 else (16 if ncols <= 6 else 14)
            if ncols >= 9:
                sz = 13
        charw = sz * 10.4
        # anchos
        total = LAND_W if wide else TEXT_W
        if wide:
            self.section_break(landscape=True)
        lens, maxl, longest = [], [], []
        for j in range(ncols):
            col = [cell_text(r[j]) for r in rows if j < len(r)]
            lens.append(sum(len(x) for x in col) / max(len(col), 1))
            maxl.append(max((len(x) for x in col), default=1))
            tok = max((len(w) for x in col for w in x.split()), default=1)
            longest.append(min(tok, 26))
        weights = [max(6, min(lens[j] * 0.6 + maxl[j] * 0.4, 70)) for j in range(ncols)]
        if is_grid:
            weights = [1] * ncols
        mins = [max(500, int(longest[j] * charw * 0.62) + 140) for j in range(ncols)]
        if sum(mins) > total:
            mins = [int(m * total / sum(mins)) for m in mins]
        rest = total - sum(mins)
        sw = sum(weights)
        widths = [mins[j] + int(rest * weights[j] / sw) for j in range(ncols)]
        widths[-1] += total - sum(widths)

        tbl = OxmlElement("w:tbl")
        tp = sub(tbl, "w:tblPr")
        sub(tp, "w:tblStyle", val="Tablaconcuadrcula")
        sub(tp, "w:tblW", w=total, type="dxa")
        sub(tp, "w:jc", val="center")
        sub(tp, "w:tblLayout", type="fixed")
        cm = sub(tp, "w:tblCellMar")
        for side, w in (("top", 30), ("left", 60), ("bottom", 30), ("right", 60)):
            sub(cm, "w:" + side, w=w, type="dxa")
        sub(tp, "w:tblLook", val="04A0", firstRow=1, lastRow=0, firstColumn=0, lastColumn=0, noHBand=0, noVBand=1)
        grid = sub(tbl, "w:tblGrid")
        for w in widths:
            sub(grid, "w:gridCol", w=w)
        for ri, cells in enumerate(rows):
            is_head = ri < len(head_rows)
            tr = sub(tbl, "w:tr")
            trpr = sub(tr, "w:trPr")
            if not is_grid:
                sub(trpr, "w:cantSplit") if sum(len(cell_text(c)) for c in cells) < 400 else None
            if is_head:
                sub(trpr, "w:tblHeader")
            for j in range(ncols):
                tc = sub(tr, "w:tc")
                tcpr = sub(tc, "w:tcPr")
                sub(tcpr, "w:tcW", w=widths[j], type="dxa")
                if is_head:
                    sub(tcpr, "w:shd", val="clear", color="auto", fill="F3F3F3")
                cell = cells[j] if j < len(cells) else None
                p = mk_p(mk_ppr(spacing=dict(before=0, after=0, line=240, lineRule="auto"),
                                jc=aligns[j] or ("center" if is_grid else None)))
                tc.append(p)
                if cell is None:
                    continue
                inline = cell.children[0] if cell.children else None
                if inline is None:
                    continue
                fmt = {"sz": sz, "b": is_head}
                imgs = []
                for r in self.inline_runs(inline, fmt):
                    if isinstance(r, tuple):
                        imgs.append(r[1])
                    else:
                        p.append(r)
                for k in imgs:
                    path = self.resolve_img(k.attrs.get("src", ""))
                    if path:
                        wcm = max(2.0, (widths[j] - 160) / 567.0)
                        self.add_picture(p, path, wcm, 9.0)
        # el último elemento de una celda debe ser un párrafo (ya lo es)
        self.put(tbl)
        # leyenda
        if is_grid:
            self.caption("fig", None)
        else:
            cnt = self.tab_count_by_head.get(self.cur_head, 1)
            k = self.tab_seen_by_head.get(self.cur_head, 0) + 1
            self.tab_seen_by_head[self.cur_head] = k
            title = None
            if not (self.pending and self.pending[0] == "tabla"):
                title = self.cur_head + (f" (parte {k} de {cnt})" if cnt > 1 else "")
                if self.pending and self.pending[0] != "tabla":
                    pass
            self.caption("tabla", title)
        self.put(mk_p(mk_ppr(spacing=dict(before=0, after=60, line=120, lineRule="auto"))))
        if wide:
            self.section_break(landscape=False)

    def section_break(self, landscape: bool):
        """Cierra la sección actual con un salto de página; la tabla ancha va en una sección horizontal."""
        prev = self.sect.getprevious()
        if landscape and self.land_close is not None and prev is self.land_close:
            # dos tablas anchas seguidas: la sección horizontal continúa
            self.body.remove(self.land_close)
            self.land_close = None
            return
        base = copy.deepcopy(self.sect)
        for tag in ("w:type",):
            for e in base.findall(qn(tag)):
                base.remove(e)
        if not self.split_done:
            # la primera sección conserva titlePg y la numeración; el resto del cuerpo continúa la numeración
            for tag in ("w:pgNumType", "w:titlePg"):
                for e in self.sect.findall(qn(tag)):
                    self.sect.remove(e)
            self.split_done = True
        if landscape:
            sp = base
        else:
            sp = OxmlElement("w:sectPr")
            sub(sp, "w:pgSz", w=16838, h=11906, orient="landscape")
            sub(sp, "w:pgMar", top=1134, right=1134, bottom=1134, left=1134, header=720, footer=567, gutter=0)
            sub(sp, "w:cols", space=720)
        if landscape:
            # el párrafo con la sectPr cierra la sección vertical anterior
            ppr = mk_ppr(spacing=dict(before=0, after=0, line=120, lineRule="auto"))
            ppr.append(sp)
            self.put(mk_p(ppr))
            self.land_open = True
        else:
            ppr = mk_ppr(spacing=dict(before=0, after=0, line=120, lineRule="auto"))
            ppr.append(sp)
            self.land_close = self.put(mk_p(ppr))
            self.land_open = False

    # ----- archivos y fragmentos
    def load_file(self, cfg):
        path = INFORME / f"{cfg['f']}.md"
        text = path.read_text(encoding="utf8")
        tokens = self.md.parse(text)
        root = SyntaxTreeNode(tokens)
        nodes = list(root.children)
        # quitar bloque de metadatos
        h1 = nodes[0] if nodes and nodes[0].type == "heading" and nodes[0].tag == "h1" else None
        if h1 is None:
            warn(f"{cfg['f']}: no empieza con H1")
        rest = nodes[1:] if h1 else nodes
        if rest and rest[0].type == "blockquote":
            bq = rest[0]
            keep = []
            for i, par in enumerate(bq.children):
                s = node_text(par)
                if cfg.get("quote") == "none":
                    continue
                if i == 0 and re.match(r"^(Estado|Archivo generado)", s):
                    if "PENDIENTE" in s:
                        keep.append(par)
                    continue
                keep.append(par)
            if keep:
                bq.children = keep
                rest = [bq] + rest[1:]
            else:
                rest = rest[1:]
        return h1, rest

    def chunks_of(self, cfg):
        h1, rest = self.load_file(cfg)
        cfg["_h1"] = h1
        h1_text = node_text(h1) if h1 else ""
        if cfg.get("title"):
            h1_text = cfg["title"]
        h1_text = PAREN_RE.sub("", h1_text)
        if cfg["h1"] == "keep":
            num = parse_num(h1_text, 1) if not cfg.get("title") else parse_num(cfg["title"], 1)
            key = num_key(cfg["key"]) if cfg.get("key") else (num_key(num) if num else ((99,),))
            nodes = ([h1] if h1 else []) + rest
            return [dict(key=key, nodes=nodes, cfg=cfg)]
        # drop: partir por H2
        skip = set(cfg.get("skip_h2", []))
        chunks, cur = [], dict(key=None, nodes=[], cfg=cfg)
        for n in rest:
            if n.type == "heading" and n.tag == "h2":
                t = node_text(n)
                if CAPH_RE.match(t):
                    cur["nodes"].append(n)
                    continue
                if t in skip:
                    continue
                if cur["nodes"] or cur["key"] is not None:
                    chunks.append(cur)
                cm = CONT_RE.match(t)
                num = cm.group(1) if cm else parse_num(t, 2)
                cur = dict(key=num_key(num) if num else None, nodes=[n], cfg=cfg)
            else:
                cur["nodes"].append(n)
        if cur["nodes"]:
            chunks.append(cur)
        # claves heredadas y retitle
        prev = None
        for ch in chunks:
            t0 = ch["nodes"][0]
            rt = cfg.get("retitle", {})
            if t0.type == "heading" and node_text(t0) in rt:
                num = parse_num(rt[node_text(t0)], 2)
                if num:
                    ch["key"] = num_key(num)
            if ch["key"] is None:
                ch["key"] = prev
            prev = ch["key"]
        # el preámbulo (sin clave) toma una clave anterior a la primera numerada
        first = next((c["key"] for c in chunks if c["key"] is not None), None)
        for ch in chunks:
            if ch["key"] is None:
                ch["key"] = first
        return chunks

    def count_tables(self, nodes):
        """Tablas por encabezado, para numerar «(parte k de m)»."""
        cur = ""
        for n in nodes:
            if n.type == "heading":
                t = node_text(n)
                if not CAPH_RE.match(t):
                    cur = re.sub(r"^\d+(?:\.\d+)*[a-z]?(?:\.\d+[a-z]?)*\.?\s+", "", PAREN_RE.sub("", self.cfg.get("retitle", {}).get(t, t)))
                    cur = re.sub(r"^Anexo\s+\d+(\.\d+)*\s+", "", cur)
            elif n.type == "table":
                self.tab_count_by_head[cur] = self.tab_count_by_head.get(cur, 0) + 1
            elif n.type == "blockquote":
                self.count_tables(n.children)

    def render_chunk(self, ch, container_level):
        cfg = ch["cfg"]
        self.cfg = cfg
        self.cur_file = cfg["f"]
        self.shift = cfg.get("shift", 0)
        self.first_h1 = cfg["h1"] == "keep"
        self.stack = [(0, container_level)] if cfg["h1"] == "keep" else [(1, container_level)]
        self.pending = None
        self.head_labels = []
        self.cur_head = ""
        self.tab_count_by_head = {}
        self.tab_seen_by_head = {}
        self.count_tables(ch["nodes"])
        nodes = ch["nodes"]
        i = 0
        while i < len(nodes):
            n = nodes[i]
            # peek: leyenda en cursiva después de una imagen sola
            self.peek_caption = None
            if n.type == "paragraph" and n.children and real_kids(n.children[0]) and all(k.type in ("image", "softbreak") for k in real_kids(n.children[0])):
                nx = nodes[i + 1] if i + 1 < len(nodes) else None
                if nx is not None and nx.type == "paragraph" and nx.children:
                    kk = real_kids(nx.children[0])
                    if len(kk) == 1 and kk[0].type == "em":
                        txt = node_text(kk[0])
                        m = re.match(r"^(Figura|Ilustración)\s+([\w.\-]+?)\s*[.:]\s+(.*)$", txt, re.S)
                        if m:
                            self.pending = ("fig", m.group(2), m.group(3).strip())
                            self.on_paragraph(n, {})
                            i += 2
                            continue
            if n.type == "fence" and (n.info or "").strip() == "mermaid":
                # leyenda en cursiva siguiente
                nx = nodes[i + 1] if i + 1 < len(nodes) else None
                if nx is not None and nx.type == "paragraph" and nx.children:
                    kk = real_kids(nx.children[0])
                    if len(kk) == 1 and kk[0].type == "em":
                        m = re.match(r"^(Figura|Ilustración)\s+([\w.\-]+?)\s*[.:]\s+(.*)$", node_text(kk[0]), re.S)
                        if m and not (self.pending and self.pending[0] == "fig"):
                            self.pending = ("fig", m.group(2), m.group(3).strip())
                            self.block(n, {})
                            i += 2
                            continue
            self.block(n, {})
            i += 1

    peek_caption = None

    # ----- ensamblado
    def build(self):
        self.prepare_template()
        self.plan(PLAN)
        self.finish_indexes()
        return self.doc

    def plan(self, items):
        for it in items:
            if it.get("title"):
                self.cfg = {}
                self.stack = [(0, it["level"])]
                self.heading(it["level"], it["title"])
            if "sub" in it:
                self.plan(it["sub"])
                continue
            chunks = []
            for cfg in it["files"]:
                if cfg.get("optional") and not self.opts.con_diccionario_completo:
                    chunks.append(self.pointer_chunk(cfg))
                    continue
                for ch in self.chunks_of(dict(cfg)):
                    chunks.append(ch)
            chunks = sorted(enumerate(chunks), key=lambda x: (x[1]["key"] or ((0,),), x[0]))
            for _, ch in chunks:
                if ch.get("pointer"):
                    self.render_pointer(ch)
                    continue
                self.render_chunk(ch, it["level"])

    def pointer_chunk(self, cfg):
        return dict(key=((99, ""), (99, "")), pointer=cfg, nodes=[], cfg=cfg)

    def render_pointer(self, ch):
        cfg = ch["pointer"]
        text = (INFORME / f"{cfg['f']}.md").read_text(encoding="utf8")
        m = re.search(r"las otras (\d+) tablas", text)
        n = m.group(1) if m else "más de 600"
        self.cfg = {}
        self.stack = [(0, 1)]
        self.heading(2, cfg["title"], page_break=False)
        url = f"{GITHUB}/blob/develop/docs/informe/{cfg['f']}.md"
        rid = self.doc.part.relate_to(url, RT.HYPERLINK, is_external=True)
        p = mk_p(mk_ppr(style="Textoindependiente", spacing=dict(before=0, after=100, line=252, lineRule="auto")))
        p.append(mk_run(f"El diccionario de las otras {n} tablas del esquema (agrupadas por el módulo de Odoo que define cada una) es un archivo generado por scripts/diccionario_datos.py desde la base de datos real. "
                        "Por su tamaño no se copia a este PDF; el diccionario de las tablas centrales está en 4.2.8 y el archivo completo se consulta en: ", sz=22))
        h = OxmlElement("w:hyperlink")
        h.set(qn("r:id"), rid)
        h.set(qn("w:history"), "1")
        h.append(mk_run(url, sz=20, link=True))
        p.append(h)
        p.append(mk_run(".", sz=22))
        self.put(p)

    # ----- plantilla
    def prepare_template(self):
        body = self.body
        ch = list(body.iterchildren())
        self.ch = ch
        d = self.doc
        # índices de los elementos clave (según la plantilla del docente)
        def idx_of(text, style=None):
            for n, e in enumerate(ch):
                if e.tag == qn("w:p"):
                    t = "".join(x.text or "" for x in e.iter(qn("w:t"))).strip()
                    if t.startswith(text):
                        return n
            raise SystemExit(f"plantilla: no encuentro «{text}»")
        i_hist = idx_of("Historial de Revisiones")
        i_res = idx_of("RESUMEN")
        self.i_idx_cont = idx_of("ÍNDICE CONTENIDOS")
        self.i_idx_fig = idx_of("ÍNDICE DE FIGURAS")
        self.i_idx_tab = idx_of("ÍNDICE DE TABLAS")
        self.el_idx_cont = ch[self.i_idx_cont]
        self.el_idx_fig = ch[self.i_idx_fig]
        self.el_idx_tab = ch[self.i_idx_tab]
        self.bm_idx = {}
        for name, e in (("cont", ch[self.i_idx_cont]), ("fig", ch[self.i_idx_fig]), ("tab", ch[self.i_idx_tab])):
            b = e.find(qn("w:bookmarkStart"))
            if b is None:
                nm, bid = self.new_bm("_Toc8")
                b = el("w:bookmarkStart", id=bid, name=nm)
                e.insert(1, b)
                e.append(el("w:bookmarkEnd", id=bid))
            self.bm_idx[name] = b.get(qn("w:name"))
        # estructura de los índices en la plantilla
        self.sdt = next(e for e in ch if e.tag == qn("w:sdt"))
        figs_para = [e for e in ch[self.i_idx_fig + 1:self.i_idx_tab] if e.tag == qn("w:p") and e.find(".//" + qn("w:pStyle")) is not None
                     and e.find(".//" + qn("w:pStyle")).get(qn("w:val")) == "Tabladeilustraciones"]
        tabs_para = [e for e in ch[self.i_idx_tab + 1:i_hist] if e.tag == qn("w:p") and e.find(".//" + qn("w:pStyle")) is not None
                     and e.find(".//" + qn("w:pStyle")).get(qn("w:val")) == "Tabladeilustraciones"]
        self.fig_anchor = figs_para[-1].getnext()   # párrafo con el fin del campo
        self.tab_anchor = tabs_para[-1].getnext()
        for e in figs_para + tabs_para:
            body.remove(e)
        # historial de revisiones
        self.fill_history(ch[i_hist + 2])
        # texto de ejemplo del historial y todo el cuerpo de ejemplo
        instr = ch[i_hist + 4]
        for e in ch[i_hist + 3:]:
            if e is self.sect:
                continue
            if e.tag == qn("w:p") and e is not ch[i_hist + 3] and e is not ch[i_hist + 5] and e is not ch[i_hist + 6]:
                pass
        # conservar: i_hist+3 (vacío) y el salto de página; quitar instrucción y cuerpo
        keep_until = i_hist + 3
        for e in ch[i_hist + 4:]:
            if e is self.sect:
                continue
            body.remove(e)
        # salto de página antes del 1.º encabezado: lo pone pageBreakBefore del H1
        self.fill_cover(ch)

    def fill_history(self, tbl_el):
        tbl = docx.table.Table(tbl_el, self.doc._body)
        rows = tbl.rows
        proto = copy.deepcopy(rows[1]._tr)
        for r in list(rows)[1:]:
            tbl_el.remove(r._tr)
        for fecha, ver, quien, desc in HISTORIAL:
            tr = copy.deepcopy(proto)
            tbl_el.append(tr)
            cells = tr.findall(qn("w:tc"))
            for c, val in zip(cells[:4], (fecha, ver, quien, desc)):
                p = c.find(qn("w:p"))
                for r in p.findall(qn("w:r")):
                    p.remove(r)
                p.append(mk_run(val, sz=18))
            for c in cells[4:]:
                p = c.find(qn("w:p"))
                for r in p.findall(qn("w:r")):
                    p.remove(r)

    def set_runs(self, p, parts):
        """Reemplaza el contenido de un párrafo de la portada conservando el formato de su primer run."""
        runs = p.findall(qn("w:r"))
        proto_rpr = copy.deepcopy(runs[0].find(qn("w:rPr")))
        for r in runs:
            p.remove(r)
        for text, kw in parts:
            r = OxmlElement("w:r")
            rpr = copy.deepcopy(proto_rpr)
            for tag in ("w:color", "w:spacing"):
                for e in rpr.findall(qn(tag)):
                    rpr.remove(e)
            if kw.get("b"):
                rpr.insert(1, OxmlElement("w:b"))
            if kw.get("hl"):
                rpr.append(el("w:highlight", val="yellow"))
            r.append(rpr)
            t = OxmlElement("w:t")
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            t.text = text
            r.append(t)
            p.append(r)

    def fill_cover(self, ch):
        P = PORTADA

        def find_p(prefix):
            for e in ch[:30]:
                if e.tag == qn("w:p") and "".join(x.text or "" for x in e.iter(qn("w:t"))).strip().startswith(prefix):
                    return e
            raise SystemExit(f"portada: no encuentro «{prefix}»")

        self.set_runs(find_p("Título:"), [("Título: ", {}), (P["titulo"], {"b": True})])
        self.set_runs(find_p("GitHub/GitLab:"), [("GitHub: ", {}), (P["github"], {"b": True})])
        parts = [("Ciclo: ", {})]
        parts += [(P["ciclo"], {"b": True})] if P["ciclo"] else [("[PENDIENTE: ciclo]", {"b": True, "hl": True})]
        self.set_runs(find_p("Ciclo:"), parts)
        self.set_runs(find_p("Integrante(s):"), [("Integrante(s):", {})])
        # tabla de integrantes
        tbl_el = next(e for e in ch[:30] if e.tag == qn("w:tbl"))
        trs = tbl_el.findall(qn("w:tr"))
        data = P["integrantes"]
        while len(trs) - 1 > len(data):
            tbl_el.remove(trs[-1])
            trs = tbl_el.findall(qn("w:tr"))
        for i, (cui, ape, nom) in enumerate(data, start=1):
            tr = trs[i]
            cells = tr.findall(qn("w:tc"))
            vals = [(str(i), {}), (cui or "[PENDIENTE: CUI]", {"hl": cui is None}),
                    (ape or "[PENDIENTE: apellidos]", {"hl": ape is None}), (nom, {})]
            for c, (v, kw) in zip(cells, vals):
                p = c.find(qn("w:p"))
                for r in p.findall(qn("w:r")):
                    p.remove(r)
                p.append(mk_run(v, sz=22 if kw.get("hl") else 28, hl=bool(kw.get("hl")), b=bool(kw.get("hl"))))
        # fecha de entrega
        p2026 = find_p("2026")
        self.set_runs(p2026, [(P["fecha"], {})])
        # propiedades
        cp = self.doc.core_properties
        cp.title = "Informe final: ERP para D'Onofrio con Odoo 19"
        cp.author = "Evelyn y Orlando"
        cp.subject = "Sistemas de Información Empresarial"
        cp.last_modified_by = "Evelyn y Orlando"
        cp.keywords = "Odoo 19; ERP; PostgreSQL; Scrum"

    # ----- índices
    def page_of(self, bm):
        return str(self.pages.get(bm, 1))

    def toc_entry(self, style, bm, text, page, first_instr=None, dots=True, b=False, sz=20):
        ppr = mk_ppr(style=style, tabs=[(TEXT_W - 10, "right", "dot" if dots else None)],
                     spacing=dict(before=0, after=30, line=240, lineRule="auto"))
        p = mk_p(ppr)
        if first_instr:
            for kind in ("begin", None, "separate"):
                r = OxmlElement("w:r")
                if kind is None:
                    t = OxmlElement("w:instrText")
                    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                    t.text = f" {first_instr} "
                    r.append(t)
                else:
                    r.append(el("w:fldChar", fldCharType=kind))
                p.append(r)
        h = OxmlElement("w:hyperlink")
        h.set(qn("w:anchor"), bm)
        h.set(qn("w:history"), "1")
        for r in self.text_runs(text, {"sz": sz, "b": b}, raw=True):
            h.append(r)
        tr = OxmlElement("w:r")
        tr.append(OxmlElement("w:tab"))
        h.append(tr)
        for r in fld_runs(f"PAGEREF {bm} \\h", page, sz=sz, b=b):
            h.append(r)
        p.append(h)
        return p

    def fix_footer_total(self):
        """El pie dice «Página: N/total»; la cubierta no cuenta, así que el total se escribe con el valor real."""
        total = self.pages.get("__total__")
        if not total:
            return
        ftr = self.doc.sections[-1].footer._element
        done = False
        for p in ftr.iter(qn("w:p")):
            runs = list(p.findall(qn("w:r")))
            for i, r in enumerate(runs):
                it = r.find(qn("w:instrText"))
                if it is not None and "NUMPAGES" in (it.text or ""):
                    # runs: begin, instr, separate, texto, end
                    for rr in runs[i - 1:i + 4]:
                        if rr.find(qn("w:t")) is not None:
                            rr.find(qn("w:t")).text = str(total)
                    for rr in (runs[i - 1], runs[i], runs[i + 1], runs[i + 3]):
                        p.remove(rr)
                    done = True
                    break
        if not done:
            warn("no pude fijar el total de páginas del pie")

    def finish_indexes(self):
        self.fix_footer_total()
        # contenido (sdt)
        content = self.sdt.find(qn("w:sdtContent"))
        for c in list(content):
            content.remove(c)
        entries = [(1, "ÍNDICE CONTENIDOS", self.bm_idx["cont"]), (1, "ÍNDICE DE FIGURAS", self.bm_idx["fig"]),
                   (1, "ÍNDICE DE TABLAS", self.bm_idx["tab"]), (1, "HISTORIAL DE REVISIONES", None)] + self.heads
        entries = [e for e in entries if e[2]]
        for n, (lvl, text, bm) in enumerate(entries):
            content.append(self.toc_entry(f"TDC{lvl}", bm, text, self.page_of(bm),
                                          first_instr="TOC \\h \\u \\z" if n == 0 else None, b=(lvl == 1)))
        fin = mk_p()
        r = OxmlElement("w:r")
        r.append(el("w:fldChar", fldCharType="end"))
        fin.append(r)
        content.append(fin)
        # figuras y tablas
        for lst, anchor, word, instr in ((self.figs, self.fig_anchor, "Ilustración", 'TOC \\h \\z \\c "Ilustración"'),
                                         (self.tabs, self.tab_anchor, "Tabla", 'TOC \\h \\z \\c "Tabla"')):
            for n, (num, title, bm) in enumerate(lst):
                p = self.toc_entry("Tabladeilustraciones", bm, f"{word} {num}. {title}", self.page_of(bm),
                                   first_instr=instr if n == 0 else None, sz=18)
                anchor.addprevious(p)


# ---------------------------------------------------------------- PDF y números de página
def convert_pdf(docx_path: Path, outdir: Path, opts) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    pdf = outdir / (docx_path.stem + ".pdf")
    if pdf.exists():
        pdf.unlink()
    filt = ('pdf:writer_pdf_Export:{"ReduceImageResolution":{"type":"boolean","value":"true"},'
            '"MaxImageResolution":{"type":"long","value":"150"},"Quality":{"type":"long","value":"85"},'
            '"ExportBookmarks":{"type":"boolean","value":"true"}}')
    r = subprocess.run([opts.soffice, "--headless", "--convert-to", filt, "--outdir", str(outdir), str(docx_path)],
                       capture_output=True, text=True, timeout=1800)
    if not pdf.exists():
        raise SystemExit(f"LibreOffice no generó el PDF:\n{r.stdout}\n{r.stderr}")
    return pdf


def read_pages(pdf: Path):
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def locate(b: Builder, pdf: Path):
    pages = read_pages(pdf)
    lines = [[norm(l) for l in p.split("\n") if l.strip()] for p in pages]
    hist = next((i for i, ls in enumerate(lines) if "Historial de Revisiones" in ls), None)
    if hist is None:
        warn("no encontré la página del historial de revisiones")
        return {}, len(pages)
    body0 = hist + 1
    res = {}
    # encabezados de índices: página impresa = física - 1
    for key, title in (("cont", "ÍNDICE CONTENIDOS"), ("fig", "ÍNDICE DE FIGURAS"), ("tab", "ÍNDICE DE TABLAS")):
        for i in range(0, hist):
            if title in lines[i]:
                res[b.bm_idx[key]] = i
                break
    cur = body0
    for lvl, text, bm in b.heads:
        t = norm(text)
        key = t[:45]
        found = None
        for i in range(cur, len(lines)):
            if any((ln == t) or (len(t) > 45 and ln.startswith(key)) or (len(t) <= 45 and ln.startswith(t) and len(ln) <= len(t) + 2)
                   for ln in lines[i]):
                found = i
                break
        if found is None:
            warn(f"título no ubicado en el PDF: {t[:60]}")
            found = cur
        res[bm] = found
        cur = found
    for lst, word in ((b.figs, "Ilustración"), (b.tabs, "Tabla")):
        cur = body0
        for num, title, bm in lst:
            pat = re.compile(rf"^{word} {num}\.\s")
            found = None
            for i in range(cur, len(lines)):
                if any(pat.match(ln + " ") for ln in lines[i]):
                    found = i
                    break
            if found is None:
                warn(f"leyenda no ubicada: {word} {num}")
                found = cur
            res[bm] = found
            cur = found
    return res, len(pages)


# ---------------------------------------------------------------- principal
def find_template(arg):
    if arg:
        p = Path(arg)
        if p.exists():
            return p
        raise SystemExit(f"no existe la plantilla: {arg}")
    cands = [ROOT / "docs" / PLANTILLA]
    try:
        common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if common:
            cands.append((ROOT / common).resolve().parent / "docs" / PLANTILLA)
    except Exception:  # noqa: BLE001
        pass
    env = os.environ.get("INFORME_PLANTILLA")
    if env:
        cands.insert(0, Path(env))
    for c in cands:
        if c.exists():
            return c
    raise SystemExit("No encuentro la plantilla del docente; use --plantilla RUTA o INFORME_PLANTILLA.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plantilla")
    ap.add_argument("--trabajo", default=str(Path.home() / "informe_build"))
    ap.add_argument("--salida", default=str(INFORME / "entrega"))
    ap.add_argument("--soffice", default=shutil.which("soffice") or "/snap/bin/libreoffice")
    ap.add_argument("--mmdc", default=os.environ.get("MMDC") or shutil.which("mmdc") or str(Path.home() / "informe_mmdc/node_modules/.bin/mmdc"))
    ap.add_argument("--chrome", default=shutil.which("google-chrome") or shutil.which("chromium") or "/usr/bin/google-chrome")
    ap.add_argument("--con-diccionario-completo", action="store_true")
    ap.add_argument("--sin-pdf", action="store_true")
    ap.add_argument("--sin-imagenes", action="store_true", help="solo para pruebas rápidas de estructura")
    ap.add_argument("--pasadas", type=int, default=4)
    opts = ap.parse_args()
    if not Path(opts.mmdc).exists():
        opts.mmdc = None
    Path(opts.trabajo).mkdir(parents=True, exist_ok=True)
    tpl = find_template(opts.plantilla)
    print(f"plantilla: {tpl}")
    out = Path(opts.salida)
    out.mkdir(parents=True, exist_ok=True)
    work_docx = Path(opts.trabajo) / "informe_final.docx"

    # pasada 0: numeración de leyendas y referencias
    b0 = Builder(tpl, None, None, opts)
    b0.build()
    labels = {k: v for k, v in b0.labels_out.items() if v is not None}
    print(f"pasada 0: {b0.n_fig} figuras, {b0.n_tab} tablas, {len(b0.heads)} títulos (hasta nivel 3), {len(labels)} etiquetas")
    pages = None
    last = None
    for n in range(1, opts.pasadas + 1):
        WARN_before = len(WARN)
        b = Builder(tpl, labels, pages, opts)
        doc = b.build()
        doc.save(str(work_docx))
        if opts.sin_pdf:
            shutil.copy(work_docx, out / "informe_final.docx")
            break
        pdf = convert_pdf(work_docx, Path(opts.trabajo), opts)
        found, total = locate(b, pdf)
        newpages = {k: v for k, v in found.items()}
        printed = {k: max(v, 0) for k, v in newpages.items()}  # física (0-based) = impresa (cubierta = 0)
        printed["__total__"] = total - 1
        print(f"pasada {n}: {total} páginas")
        if pages == printed:
            last = pdf
            break
        pages = printed
        last = pdf
    shutil.copy(work_docx, out / "informe_final.docx")
    if last:
        shutil.copy(last, out / "informe_final.pdf")
        size = (out / "informe_final.pdf").stat().st_size
        print(f"PDF: {out/'informe_final.pdf'}  ({size/1e6:.1f} MB)")
    if UNRESOLVED:
        print("\nReferencias a tablas/figuras sin leyenda equivalente (se dejan como están):")
        for k, v in sorted(UNRESOLVED.items(), key=lambda x: -x[1])[:40]:
            print(f"  {k}: {v}")
    uniq = sorted(set(WARN))
    if uniq:
        print(f"\n{len(uniq)} avisos:")
        for w in uniq[:80]:
            print("  -", w)


if __name__ == "__main__":
    main()
