#!/usr/bin/env bash
# Revisa addons/ en busca de patrones legacy de Odoo (<= 16).
# Usa el MISMO listado que el hook de Claude Code (.claude/hooks/bloquear_legacy.py),
# así hay una sola fuente de verdad. Corre en pre-commit y en el CI.
# Uso: scripts/check_legacy.sh [ruta ...]   (por defecto: addons)
set -euo pipefail
cd "$(dirname "$0")/.."
PY="$(command -v python3 || command -v python)" || { echo "Falta Python (python3 o python)" >&2; exit 1; }
exec "$PY" .claude/hooks/bloquear_legacy.py --scan "$@"
