from odoo.tests import TransactionCase, tagged

# Departamento → departamento padre, según el organigrama de 01 §1.5
JERARQUIA = {
    'dep_ventas': 'dep_gerencia',
    'dep_canal_moderno': 'dep_ventas',
    'dep_canal_tradicional': 'dep_ventas',
    'dep_heladeros': 'dep_ventas',
    'dep_logistica': 'dep_gerencia',
    'dep_alm_lima': 'dep_logistica',
    'dep_cd_arequipa': 'dep_logistica',
    'dep_despacho': 'dep_logistica',
    'dep_produccion': 'dep_gerencia',
    'dep_linea_helados': 'dep_produccion',
    'dep_linea_chocolates': 'dep_produccion',
    'dep_linea_paneton': 'dep_produccion',
    'dep_calidad': 'dep_produccion',
    'dep_compras': 'dep_gerencia',
    'dep_finanzas': 'dep_gerencia',
    'dep_rrhh': 'dep_gerencia',
    'dep_ti': 'dep_gerencia',
}


@tagged('post_install', '-at_install')
class TestRRHH(TransactionCase):
    """HU-05: organigrama, puestos y empleados."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.empleados = cls.env['hr.employee'].search([
            ('company_id', '=', cls.env.ref('base.main_company').id),
        ])

    def _ref(self, xmlid):
        return self.env.ref(f'donofrio_base.{xmlid}')

    def test_departamentos_con_jerarquia(self):
        raiz = self._ref('dep_gerencia')
        self.assertFalse(raiz.parent_id)
        for hijo, padre in JERARQUIA.items():
            with self.subTest(departamento=hijo):
                self.assertEqual(self._ref(hijo).parent_id, self._ref(padre))
        # Los 7 departamentos de primer nivel de 01 §1.5 cuelgan de la Gerencia General
        self.assertEqual(len(raiz.child_ids), 7)
        self.assertEqual(len(raiz.child_ids), len(raiz.child_ids.filtered('manager_id')))
        self.assertEqual(self._ref('dep_ventas').child_ids, self._ref('dep_canal_moderno')
                         | self._ref('dep_canal_tradicional') | self._ref('dep_heladeros'))

    def test_unos_veinte_empleados(self):
        propios = self.env['hr.employee'].browse(
            self.env['ir.model.data'].search([
                ('module', '=', 'donofrio_base'), ('model', '=', 'hr.employee'),
            ]).mapped('res_id'))
        self.assertEqual(len(propios), 21)
        for empleado in propios:
            with self.subTest(empleado=empleado.name):
                self.assertTrue(empleado.department_id)
                self.assertTrue(empleado.job_id)
                self.assertTrue(empleado.job_title)

    def test_organigrama_de_personas(self):
        gerente = self._ref('emp_gerente')
        self.assertFalse(gerente.parent_id)
        # Todos los demás empleados llegan hasta el gerente por la cadena de jefes
        for empleado in self.empleados.filtered(lambda e: e.get_external_id().get(e.id, '').startswith('donofrio_base.')):
            if empleado == gerente:
                continue
            with self.subTest(empleado=empleado.name):
                self.assertTrue(empleado.parent_id)
                self.assertIn(gerente, empleado.parent_id | empleado.parent_id.parent_id
                              | empleado.parent_id.parent_id.parent_id)
        # El jefe de ventas manda sobre su canal y el liquidador responde al supervisor de heladeros
        self.assertEqual(self._ref('emp_vendedor').parent_id, self._ref('emp_jefe_ventas'))
        self.assertEqual(self._ref('emp_liquidador').parent_id, self._ref('emp_sup_heladeros'))
        self.assertEqual(self._ref('emp_enc_aqp').department_id, self._ref('dep_cd_arequipa'))

    def test_empleados_vinculados_a_usuarios_por_rol(self):
        """Los 10 usuarios de HU-04 tienen su empleado, con el puesto de su rol."""
        usuarios = [
            'user_gerente', 'user_jefe_ventas', 'user_vendedor', 'user_cajero_pdv', 'user_jefe_almacen',
            'user_jefe_produccion', 'user_inspector_calidad', 'user_liquidador', 'user_compras', 'user_contador',
        ]
        for xmlid in usuarios:
            with self.subTest(usuario=xmlid):
                usuario = self._ref(xmlid)
                self.assertEqual(len(usuario.employee_ids), 1)
        self.assertEqual(self._ref('user_liquidador').employee_ids, self._ref('emp_liquidador'))
        self.assertEqual(self._ref('emp_liquidador').job_id.name, 'Liquidador de Heladeros')

    def test_vista_de_organigrama_disponible(self):
        """hr_org_chart agrega la vista jerárquica a empleados y departamentos (organigrama)."""
        self.assertIn('hierarchy', self.env['hr.employee'].get_views([(False, 'hierarchy')])['views'])
        self.assertIn('hierarchy', self.env['hr.department'].get_views([(False, 'hierarchy')])['views'])
