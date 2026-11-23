#!/usr/bin/env python3
"""Bloquea patrones legacy de Odoo (<= 16) en addons/**/*.{py,xml,js,csv}.

Dos modos (un único listado de patrones para el hook y para el CI):
  1. Hook PreToolUse de Claude Code (sin argumentos): lee el JSON de stdin y
     revisa el texto nuevo de Edit/Write/MultiEdit. Código de salida 2 = bloquea
     la edición y el agente ve el motivo en stderr.
  2. Escaneo (`--scan [ruta ...]`): revisa los archivos existentes. Lo usa
     scripts/check_legacy.sh en pre-commit y en el CI. Código 1 si hay hallazgos.

Referencia de reemplazos: docs/dev/odoo19_cambios.md
"""
import json
import re
import sys
from pathlib import Path

EXTENSIONES = {".py", ".xml", ".js", ".csv"}
# Archivos que describen los patrones y no deben revisarse a sí mismos.
EXCLUIDOS = {
    "docs/dev/odoo19_cambios.md",
    "scripts/check_legacy.sh",
    ".claude/hooks/bloquear_legacy.py",
}

# (regex, reemplazo correcto de 19.0)
PATRONES = [
    (r"\battrs\s*=", 'invisible="…" / readonly="…" con expresión Python'),
    (r"\bstates\s*=", "expresión en invisible/readonly"),
    (r"<tree\b", "<list>"),
    (r'view_mode="[^"]*\btree', 'view_mode="list,form"'),
    (r"_sql_constraints", "models.Constraint / models.Index / models.UniqueIndex"),
    (r"\bgroups_id\b", "group_ids"),
    (r"odoo\.osv|osv\.expression|from odoo\.osv", "from odoo.fields import Domain"),
    (r"(?<![\w.])read_group\(", "_read_group( o formatted_read_group("),
    (r"\bname_get\b", "_compute_display_name"),
    (r"self\._(?:cr|context|uid)\b", "self.env.cr / self.env.context / self.env.uid"),
    (r"t-raw\s*=", "t-out"),
    (r"odoo\.define\(", "módulo ES: import { registry } from \"@web/core/registry\""),
    (r"\bnumbercall\b", "ir.cron sin numbercall (interval_number + interval_type)"),
    (r"\bdetailed_type\b", "type + is_storable=True"),
    (r"uom\.category", "uom.uom con relative_uom_id + relative_factor"),
    (r"hr\.contract\b", "hr.version (no existe hr_contract)"),
    (r"@http\.route\([^)]*\btype\s*=\s*['\"]json['\"]", "type='jsonrpc'"),
]
COMPILADOS = [(re.compile(p, re.DOTALL), msg) for p, msg in PATRONES]


def es_revisable(ruta: str) -> bool:
    ruta = ruta.replace("\\", "/")
    if any(ruta.endswith(x) for x in EXCLUIDOS):
        return False
    partes = ruta.split("/")
    return "addons" in partes and Path(ruta).suffix in EXTENSIONES


def hallazgos(texto: str):
    """Devuelve [(línea, coincidencia, reemplazo)] para el texto dado."""
    salida = []
    for regex, reemplazo in COMPILADOS:
        for m in regex.finditer(texto):
            linea = texto.count("\n", 0, m.start()) + 1
            salida.append((linea, m.group(0).strip(), reemplazo))
    return sorted(salida)


def modo_hook() -> int:
    try:
        datos = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # entrada que no entendemos: no bloquear
    entrada = datos.get("tool_input") or {}
    ruta = entrada.get("file_path") or ""
    if not es_revisable(ruta):
        return 0
    textos = [entrada.get("content"), entrada.get("new_string")]
    textos += [e.get("new_string") for e in entrada.get("edits") or []]
    textos = [t for t in textos if isinstance(t, str)]
    problemas = [h for t in textos for h in hallazgos(t)]
    if not problemas:
        return 0
    print(f"BLOQUEADO: patrón legacy (Odoo <= 16) en {ruta}", file=sys.stderr)
    for linea, coincidencia, reemplazo in problemas:
        print(f"  - línea {linea}: «{coincidencia}» → usar {reemplazo}", file=sys.stderr)
    print("Ver docs/dev/odoo19_cambios.md y busca un ejemplo real en ~/src/odoo-19.0.", file=sys.stderr)
    return 2


def modo_scan(rutas) -> int:
    raiz = Path(".")
    archivos = []
    for r in rutas or ["addons"]:
        p = Path(r)
        archivos += [p] if p.is_file() else sorted(p.rglob("*"))
    total = 0
    for archivo in archivos:
        ruta = archivo.as_posix()
        if not archivo.is_file() or not es_revisable(ruta):
            continue
        try:
            texto = archivo.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for linea, coincidencia, reemplazo in hallazgos(texto):
            print(f"{ruta}:{linea}: «{coincidencia}» → usar {reemplazo}")
            total += 1
    if total:
        print(f"\ncheck_legacy: {total} patrón(es) legacy. Ver docs/dev/odoo19_cambios.md", file=sys.stderr)
        return 1
    print("check_legacy: sin patrones legacy.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--scan":
        sys.exit(modo_scan(sys.argv[2:]))
    sys.exit(modo_hook())
