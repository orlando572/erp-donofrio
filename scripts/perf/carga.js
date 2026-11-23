// HU-28 (RNF002): carga con k6 sobre el despliegue protegido (Nginx + TLS + Odoo con workers).
// 20 usuarios virtuales (VU) navegan listas, formularios y el tablero con el JSON-RPC de Odoo 19, como lo hace el
// cliente web (/web/dataset/call_kw/<modelo>/web_search_read y web_read). Se inicia sesión una sola vez por VU
// (/web/session/authenticate) con usuarios SIN 2FA: vendedor, jefe de ventas y jefe de almacén. Admin y gerente
// usan segundo factor en este modo y no sirven para una prueba automática. Nunca se hacen intentos fallidos:
// el bloqueo de login de Odoo (5 fallos por IP y worker) no debe saltar.
//
// Se ejecuta con scripts/perf/k6.sh (imagen de Docker de k6). Variables de entorno:
//   DONOFRIO_USER_PASSWORD  contraseña de los usuarios de prueba (obligatoria; viene del .env, nunca va en el código)
//   BASE_URL   por defecto https://localhost:8443      ODOO_DB   por defecto donofrio
//   VUS        por defecto 20                          DURACION  por defecto 3m (tiempo con todos los VU activos)
//   PAUSA      factor de las pausas entre pantallas (1 = ritmo de una persona, 1-3 s; 0 = sin pausas, prueba de esfuerzo)
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const BASE = __ENV.BASE_URL || 'https://localhost:8443';
const BD = __ENV.ODOO_DB || 'donofrio';
const CLAVE = __ENV.DONOFRIO_USER_PASSWORD;
const VUS = parseInt(__ENV.VUS || '20', 10);
const DURACION = __ENV.DURACION || '3m';
const PAUSA = parseFloat(__ENV.PAUSA || '1');

// Pausa entre pantallas (tiempo de lectura de una persona), escalada por PAUSA
const pausar = (min, extra) => { if (PAUSA > 0) sleep(PAUSA * (min + Math.random() * extra)); };

if (!CLAVE) {
  throw new Error('Falta DONOFRIO_USER_PASSWORD (la toma scripts/perf/k6.sh del .env)');
}

// Errores que Odoo devuelve dentro de un 200 (AccessError, etc.): http_req_failed no los ve
const erroresRpc = new Rate('errores_rpc');

export const options = {
  // El certificado de Nginx es autofirmado (demo): solo en esta prueba se desactiva la verificación
  insecureSkipTLSVerify: true,
  // k6 vacía las cookies en cada iteración; la sesión se abre una sola vez por VU y debe conservarse
  noCookiesReset: true,
  scenarios: {
    usuarios: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '20s', target: VUS },
        { duration: DURACION, target: VUS },
        { duration: '10s', target: 0 },
      ],
      gracefulRampDown: '15s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    errores_rpc: ['rate<0.01'],
    checks: ['rate>0.99'],
    // RNF002: p95 < 2 s en listas y formularios con 20 usuarios concurrentes
    'http_req_duration{tipo:lista}': ['p(95)<2000'],
    'http_req_duration{tipo:formulario}': ['p(95)<2000'],
    // lo demás se mide y se reporta (tablero, carga de la app, inicio de sesión)
    'http_req_duration{tipo:tablero}': ['p(95)<2000'],
    'http_req_duration{tipo:app}': ['p(95)<2000'],
    'http_req_duration{tipo:login}': ['p(95)<2000'],
  },
  summaryTrendStats: ['min', 'med', 'avg', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

// Cada rol recorre lo que usa en el día a día: [modelo, especificación de la lista, orden, dominio]
const rel = () => ({ fields: { display_name: {} } });

const PEDIDOS = ['sale.order', { name: {}, partner_id: rel(), date_order: {}, amount_total: {}, state: {} }, 'date_order desc'];
const CLIENTES = ['res.partner', { name: {}, email: {}, city: {}, customer_rank: {} }, 'name asc'];
const PRODUCTOS = ['product.template', { name: {}, default_code: {}, list_price: {}, type: {} }, 'name asc'];
const FACTURAS = ['account.move', { name: {}, partner_id: rel(), invoice_date: {}, amount_total: {}, state: {} }, 'invoice_date desc',
  [['move_type', 'in', ['out_invoice', 'out_refund']]]];
const TRANSFERENCIAS = ['stock.picking', { name: {}, partner_id: rel(), scheduled_date: {}, state: {}, origin: {} }, 'scheduled_date desc'];
const LOTES = ['stock.lot', { name: {}, product_id: rel(), expiration_date: {}, product_qty: {} }, 'expiration_date asc'];
const PRODUCCION = ['mrp.production', { name: {}, product_id: rel(), product_qty: {}, state: {}, date_start: {} }, 'date_start desc'];

const FORM_PEDIDO = ['sale.order', {
  name: {}, partner_id: rel(), date_order: {}, state: {}, amount_untaxed: {}, amount_tax: {}, amount_total: {},
  order_line: { fields: { product_id: rel(), product_uom_qty: {}, price_unit: {}, price_subtotal: {} } },
}];
const FORM_PICKING = ['stock.picking', {
  name: {}, partner_id: rel(), scheduled_date: {}, state: {}, origin: {},
  move_ids: { fields: { product_id: rel(), product_uom_qty: {}, state: {} } },
}];
const FORM_PRODUCTO = ['product.template', { name: {}, default_code: {}, list_price: {}, standard_price: {}, type: {}, categ_id: rel() }];

const ROLES = [
  {
    usuario: 'vendedor@donofrio.example.com',
    listas: [PEDIDOS, CLIENTES, PRODUCTOS],
    formulario: FORM_PEDIDO, de: PEDIDOS,
    tablero: ['sale.report', 'date:month', 'price_subtotal:sum'],
  },
  {
    usuario: 'jefe.ventas@donofrio.example.com',
    listas: [PEDIDOS, FACTURAS, CLIENTES],
    formulario: FORM_PEDIDO, de: PEDIDOS,
    tablero: ['sale.report', 'date:month', 'price_subtotal:sum'],
  },
  {
    usuario: 'jefe.almacen@donofrio.example.com',
    listas: [TRANSFERENCIAS, LOTES, PRODUCCION, PRODUCTOS],
    formulario: FORM_PICKING, de: TRANSFERENCIAS,
    tablero: ['stock.lot', 'expiration_date:month', '__count'],
  },
];

let sesionIniciada = false;

function rpc(url, params, tipo, nombre) {
  const r = http.post(url, JSON.stringify({ jsonrpc: '2.0', method: 'call', params }), {
    headers: { 'Content-Type': 'application/json' },
    tags: { tipo, name: nombre },
  });
  let cuerpo = null;
  try { cuerpo = r.json(); } catch (e) { cuerpo = null; }
  const bien = r.status === 200 && cuerpo !== null && cuerpo.error === undefined && cuerpo.result !== undefined;
  erroresRpc.add(!bien);
  if (!bien) {
    const motivo = cuerpo && cuerpo.error && cuerpo.error.data ? cuerpo.error.data.message : `HTTP ${r.status}`;
    console.error(`${nombre} falló: ${String(motivo).slice(0, 160)}`);
  }
  check(r, { [`${nombre}: respuesta correcta`]: () => bien });
  return bien ? cuerpo.result : null;
}

function llamar(modelo, metodo, args, kwargs, tipo) {
  const nombre = `${modelo} ${metodo}`;
  return rpc(`${BASE}/web/dataset/call_kw/${modelo}/${metodo}`,
    { model: modelo, method: metodo, args, kwargs: { context: { lang: 'es_PE', tz: 'America/Lima' }, ...kwargs } }, tipo, nombre);
}

function lista([modelo, especificacion, orden, dominio]) {
  return llamar(modelo, 'web_search_read', [], {
    domain: dominio || [], specification: especificacion, order: orden, limit: 80, offset: 0, count_limit: 10001,
  }, 'lista');
}

function iniciarSesion(rol) {
  const r = http.post(`${BASE}/web/session/authenticate`,
    JSON.stringify({ jsonrpc: '2.0', method: 'call', params: { db: BD, login: rol.usuario, password: CLAVE } }),
    { headers: { 'Content-Type': 'application/json' }, tags: { tipo: 'login', name: 'authenticate' } });
  let uid = null;
  try { const c = r.json(); uid = c.result ? c.result.uid : null; } catch (e) { uid = null; }
  const bien = check(r, { 'inicio de sesión correcto': () => r.status === 200 && !!uid });
  erroresRpc.add(!bien);
  return bien;
}

export default function () {
  const rol = ROLES[(__VU - 1) % ROLES.length];

  if (!sesionIniciada) {
    sesionIniciada = iniciarSesion(rol);
    if (!sesionIniciada) { sleep(5); return; }
  }

  group('app', () => {
    const r = http.get(`${BASE}/odoo`, { tags: { tipo: 'app', name: '/odoo' } });
    check(r, { 'la app carga (200)': () => r.status === 200 });
    const m = http.get(`${BASE}/web/webclient/load_menus`, { tags: { tipo: 'app', name: 'load_menus' } });
    check(m, { 'menús (200)': () => m.status === 200 });
  });
  pausar(1, 1);

  group('listas', () => {
    for (const l of rol.listas) {
      lista(l);
      pausar(1, 2);
    }
  });

  group('formulario', () => {
    const [modeloLista, , orden, dominio] = rol.de;
    const res = llamar(modeloLista, 'web_search_read', [], {
      domain: dominio || [], specification: { display_name: {} }, order: orden, limit: 20, offset: 0,
    }, 'lista');
    const registros = (res && res.records) || [];
    if (registros.length > 0) {
      const id = registros[Math.floor(Math.random() * registros.length)].id;
      const [modelo, especificacion] = rol.formulario;
      llamar(modelo, 'web_read', [[id]], { specification: especificacion }, 'formulario');
    }
  });
  pausar(1, 2);

  group('tablero', () => {
    const [modelo, agrupar, agregado] = rol.tablero;
    llamar(modelo, 'web_read_group', [], {
      domain: [], groupby: [agrupar], aggregates: [agregado], limit: 80,
    }, 'tablero');
  });
  pausar(1, 2);
}
