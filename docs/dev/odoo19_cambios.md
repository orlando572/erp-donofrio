# Ficha de cambios de Odoo 19 (para el agente y los humanos)

Se basa en el changelog del ORM (`~/src/odoo-docs-19.0/content/developer/reference/backend/orm/changelog.rst`, versiones 16.4 a 19.0) y en lo verificado en el código 19.0.
✓ = verificado en el código o el changelog de 19.0 el 22/11/2026.

**Regla de mantenimiento:** si el agente o el CI encuentran otra diferencia, se agrega una línea con la versión y el ejemplo de 19.0.
Esta ficha **no se pega en el CLAUDE.md**: se lee solo cuando se va a escribir código.

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
