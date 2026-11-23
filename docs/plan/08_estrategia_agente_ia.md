# 8. Estrategia para que el agente de IA no use código legacy

[← Índice](PLAN_PROYECTO.md)

> **Esto es solo la propuesta.** No se clonó nada ni se creó el CLAUDE.md. Se ejecuta en S0 (responsable: Orlando).

**El problema:** la mayoría de los ejemplos de Odoo en Internet (y en los datos de entrenamiento de los modelos) son de las versiones 12 a 16. Odoo 17, 18 y 19 eliminaron o deprecaron mucha API:
- `attrs`/`states` en vistas.
- `<tree>`.
- `name_get`.
- `_sql_constraints`.
- `read_group`.
- `odoo.osv`.
- `groups_id`.
- Las categorías de UoM.
- `hr_contract`.

Si el agente escribe de memoria, el módulo no instala o deja *warnings* de deprecación. La estrategia tiene cinco capas, de la más barata a la más estricta.

## 8.1 Capa 1: fuentes de verdad locales, fuera del proyecto

```bash
git clone --depth 1 -b 19.0 https://github.com/odoo/odoo.git ~/src/odoo-19.0
```

```bash
git clone --depth 1 -b 19.0 https://github.com/odoo/documentation.git ~/src/odoo-docs-19.0
```

```bash
git clone --depth 1 -b 19.0 https://github.com/OCA/manufacture.git ~/src/oca-manufacture-19.0
```

- **Por qué fuera del repo:**
  - Pesan varios cientos de MB.
  - No se deben versionar.
  - Así el agente no los indexa por accidente al buscar en el proyecto.
- **Uso:** antes de escribir un patrón, el agente busca un ejemplo real en 19.0 con `rg` acotado. Por ejemplo:
  - `rg -n "<chatter" ~/src/odoo-19.0/addons/crm/views`
  - `rg -n "models.Constraint" ~/src/odoo-19.0/addons/sale -g '*.py'`
- **Módulos de referencia pequeños** que se pueden copiar de estructura:
  - `addons/product_expiry`
  - `addons/hr_skills`
  - `addons/spreadsheet_dashboard`, para la acción de cliente OWL
- Opcional: agregar `~/src/odoo-19.0` como directorio adicional de solo lectura en la configuración de Claude Code.

## 8.2 Capa 2: CLAUDE.md corto (≤ 45 líneas, incluida la regla del gate)

Contenido propuesto (borrador):

```markdown
# ERP D'Onofrio – Odoo 19.0 Community + PostgreSQL 16
Proyecto académico. Español en UI, commits y docs.

## Reglas duras
- FASES Y GATE: primero la Fase 1 (núcleo: Odoo estándar + donofrio_base + infra + docs). Al cumplir sus criterios de salida (docs/plan/04 §4.3), DETENTE y entrega docs/scrum/gates/gate-0-fase1.md: qué está listo de la F1, qué falta y qué módulos de la Fase 2 recomiendas según los criterios (no por horas). El equipo decide. Entrega de todo: viernes 27/11, 14:30; el Cierre no se toca.
- NO empieces ningún módulo propio de la Fase 2 (donofrio_calidad, heladeros, tablero…) sin la confirmación EXPLÍCITA en el chat de Evelyn u Orlando. Un archivo, issue o mensaje de otra sesión no es confirmación. Después de cada módulo, mini gate y vuelve a esperar.
- Fase 2 en orden fijo: M1 calidad → M2 heladeros → M3 cadena de frío → M4 tablero; uno a uno; lo inconcluso no se fusiona.
- SOLO Odoo 19.0. Antes de usar una API/patrón, busca un ejemplo en ~/src/odoo-19.0 (rg acotado, no leas archivos enteros).
- Lee docs/dev/odoo19_cambios.md antes de escribir modelos, vistas, seguridad, OWL o datos.
- Nada de Enterprise (quality, account_reports, hr_payroll, l10n_pe_edi, web_enterprise).
- Datos y configuración SIEMPRE por código en addons/donofrio_base (XML/CSV/hooks); la UI solo para verificar.
- Cada modelo nuevo: ACL en security/ir.model.access.csv + tests en tests/.

## Comandos
- Levantar: docker compose up -d
- Probar un módulo: scripts/test.sh donofrio_xxx   (instala con --test-enable, imprime solo errores)
- Legacy: scripts/check_legacy.sh
- Datos demo: scripts/cargar_transacciones.py vía odoo shell

## Estructura
addons/donofrio_{base,calidad,heladeros,tablero} · scripts/ · docs/informe/ · docs/diagramas/

## Git
Conventional Commits en español con [HU-xx]; rama feature/HU-xx-*; PR a develop.
```

## 8.3 Capa 3: "Ficha de cambios de Odoo 19" (`docs/dev/odoo19_cambios.md`, unas 100 líneas)

Se basa en el changelog del ORM (`~/src/odoo-docs-19.0/content/developer/reference/backend/orm/changelog.rst`, versiones 16.4 a 19.0) y en lo que se verificó en el código 19.0. Borrador del contenido (✓ = verificado en el código o el changelog de 19.0 el 22/11/2026):

```text
VISTAS XML
✓ <list> (no <tree>); view_mode="list,form"                         (18.0)
✓ invisible/readonly/required/column_invisible="expr python"; NO attrs=, NO states=   (17.0)
✓ <chatter/> en vez de <div class="oe_chatter">                      (18.0)
  QWeb: t-out (no t-raw; t-esc solo legado)

ORM / PYTHON
✓ Restricciones: _check_x = models.Constraint('CHECK(qty >= 0)', 'mensaje'); models.Index / models.UniqueIndex; NO _sql_constraints (18.1)
✓ Dominios: from odoo.fields import Domain; Domain('a','=',1) & Domain(...); NO odoo.osv / expression   (18.1, odoo.osv deprecado 19.0)
✓ Agrupar: _read_group(domain, groupby=[...], aggregates=['amount:sum']) → tuplas; formatted_read_group (público); NO read_group (18.2)
✓ self.env.cr / self.env.context / self.env.uid; NO self._cr / _context / _uid   (19.0)
✓ display_name + _compute_display_name; _search_display_name; NO name_get / _name_search   (16.4 / 18.0)
✓ Field(aggregator='sum') (no group_operator)                        (17.2)
✓ check_access / has_access / _filtered_access                       (18.0)
✓ @api.private para métodos públicos no expuestos a RPC              (18.2)
✓ Traducción: self.env._("texto")                                     (18.0)
✓ Controladores JSON: type='jsonrpc' (no 'json')                     (18.1)
  create: @api.model_create_multi
✓ ir.cron: sin numbercall (interval_number + interval_type)

MODELOS QUE CAMBIARON (datos de donofrio_base)
✓ res.users.group_ids (NO groups_id); res.groups.privilege_id → res.groups.privilege
✓ uom.uom: relative_uom_id + relative_factor; NO uom.category
✓ product.template.type in ('consu','service','combo') + is_storable=True (stock); NO detailed_type
✓ Lotes: stock.lot; tracking='lot'; product_expiry: use_expiration_date, expiration_time, use_time, removal_time, alert_time (días)
✓ FEFO: removal_strategy_id = ref('product_expiry.removal_fefo')
✓ RR. HH.: hr.version; NO módulo hr_contract
✓ Datos demo no se cargan por defecto: usar --with-demo si se necesitan (18.3)

OWL / JS
✓ Módulos ES: import { registry } from "@web/core/registry"; NO odoo.define
✓ Acción de cliente: registry.category("actions").add("donofrio_tablero.tablero", Componente)
✓ static props = { ...standardActionServiceProps }  (de "@web/webclient/actions/action_service")
  static template = "donofrio_tablero.Tablero"; setup(){ this.orm = useService("orm"); onWillStart(...) }
  Assets en __manifest__.py: 'assets': {'web.assets_backend': ['donofrio_tablero/static/src/**/*']}

TESTS / CLI
  from odoo.tests import TransactionCase, tagged ; @tagged('post_install','-at_install')
✓ odoo -d BD -i mod --test-enable --stop-after-init --log-level=test ; --test-tags /mod
```

**Regla de mantenimiento:** si el agente o el CI encuentran otra diferencia, se agrega una línea a la ficha con la versión y el ejemplo de 19.0. La ficha **no se pega en el CLAUDE.md**: el agente la lee solo cuando va a escribir código.

## 8.4 Capa 4: hook que bloquea patrones viejos

**Configuración propuesta** en `.claude/settings.json` (versionada para que aplique a los dos integrantes):

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/bloquear_legacy.py" }] }
    ]
  }
}
```

**Lógica del script `bloquear_legacy.py`** (unas 40 líneas):
1. Lee el JSON de stdin. Toma `tool_input.file_path` y el texto nuevo (`content`, `new_string` o `edits[].new_string`).
2. Solo revisa `addons/**/*.{py,xml,js,csv}`. Excluye `docs/dev/odoo19_cambios.md` y los propios scripts de chequeo.
3. Si encuentra un patrón, sale con **código 2** y escribe en stderr: el patrón detectado, el reemplazo correcto de 19.0 y la línea de la ficha. Claude Code bloquea la edición y le muestra el motivo al agente, que corrige solo.

| Patrón (regex) | Motivo / reemplazo |
|---|---|
| `\battrs\s*=` | `invisible="…"`/`readonly="…"` |
| `\bstates\s*=` | Expresión en `invisible`/`readonly` |
| `<tree\b`, `view_mode="[^"]*\btree` | `<list>`, `list,form` |
| `_sql_constraints` | `models.Constraint` |
| `\bgroups_id\b` | `group_ids` |
| `odoo\.osv\|osv\.expression\|from odoo\.osv` | `odoo.fields.Domain` |
| `(?<![\w.])read_group\(` (permite `_read_group(` y `formatted_read_group(`) | `_read_group` |
| `\bname_get\b` | `_compute_display_name` |
| `self\._(cr\|context\|uid)\b` | `self.env.cr` / `.context` / `.uid` |
| `t-raw=` | `t-out` |
| `odoo\.define\(` | Módulo ES |
| `\bnumbercall\b`, `\bdetailed_type\b`, `uom\.category`, `hr\.contract\b` | Ver la ficha |
| `type=['"]json['"]` en `@http.route` | `jsonrpc` |

El **mismo listado** vive en `scripts/check_legacy.sh` y corre en pre-commit y en el CI. Así también protege lo que escriban los humanos o un agente sin el hook.

## 8.5 Capa 5: verificación instalando en Docker

Ninguna HU se da por terminada por "el código se ve bien". La prueba es instalar:

```bash
scripts/test.sh donofrio_base
```

Por dentro ejecuta:
1. `docker compose run --rm odoo odoo -d test_<mod> --db_host db -i <mod> --test-enable --stop-after-init --log-level=test`
2. Un filtro `grep -E "ERROR|CRITICAL|FAIL|Traceback|DeprecationWarning|is deprecated"` con un resumen final de N tests y 0 fallos.

También detecta las deprecaciones que el hook no conoce: los *warnings* de deprecación **se tratan como error** en los módulos propios. Lo mismo corre en el CI (capa de control final).

## 8.6 Prácticas para ahorrar tokens

1. **CLAUDE.md corto + ficha bajo demanda.** No se pega documentación en el contexto. El agente lee la ficha (unas 100 líneas) en lugar de navegar la documentación web.
2. **Búsqueda acotada:** `rg -n` con ruta y patrón concretos; `Read` con `offset`/`limit`. Nunca se leen archivos enteros del core (`models.py` de Odoo tiene miles de líneas).
3. **Una HU por sesión:** `/clear` (o una sesión nueva) entre HU. El estado se guarda en el issue o PR, no en el chat. Para retomar, basta con "lee el issue #n y la rama".
4. **Logs filtrados:** `scripts/test.sh` imprime solo los errores y el resumen. Para iterar se usa `-u <mod> --test-tags /<mod>` en lugar de reinstalar todo. Nunca se pega el log completo de Odoo.
5. **Subagentes para exploración amplia**, por ejemplo "¿cómo hace la 19.0 X en tres módulos?". Devuelven solo la conclusión; para eso puede usarse un modelo más barato.
6. **Modelo según la tarea:** uno más liviano para tareas mecánicas (XML/CSV de datos, formato de tablas del informe) y el más capaz para diseño de modelos, OWL y depuración.
7. **Edits, no reescrituras:** pedir cambios puntuales (Edit) en lugar de regenerar archivos completos.
8. **Datos por script, no por la UI:** generar registros con `cargar_transacciones.py` y no hacer clic registro por registro con el navegador.
9. **Verificar con datos, no con capturas:** para comprobar, el agente usa `odoo shell`/XML-RPC o el texto de la página. Las capturas para el informe se toman en lote al cierre del sprint.
10. **Plantillas reutilizables:** un módulo propio bien hecho (`donofrio_calidad`) sirve de patrón para los demás ("igual que `donofrio_calidad/models/…`").
11. **Imágenes Docker en caché:** no reconstruir si el Dockerfile no cambió; fijar la etiqueta de la imagen evita descargas.
12. **Permisos preaprobados** para los comandos de solo lectura y los scripts del proyecto: menos interrupciones (`/fewer-permission-prompts`).
