# 1. Alcance, escenario, supuestos y fuentes

[← Índice](PLAN_PROYECTO.md)

## 1.1 Escenario

**"D'Onofrio como unidad de helados y confitería"**, con fecha de corte en **2026**, antes de que el negocio de helados pase a Froneri.

- Se modela a D'Onofrio como **unidad de negocio de Nestlé Perú S.A.** con tres líneas: **helados**, **chocolates** y **panetón**.
- La venta global del negocio de helados de Nestlé a Froneri se **menciona en el entorno** (sección 3 del informe) como riesgo y oportunidad estratégica. **No se modela** en el ERP porque para Perú no hay nada confirmado.
- La empresa de Odoo se llamará `D'Onofrio – Unidad de Helados y Confitería (proyecto académico)`. Usará un **RUC ficticio** con dígito verificador válido y datos maestros ficticios, para no emitir documentos con la identidad tributaria real de Nestlé.
- Sedes modeladas: **Planta Lima** (Av. Venezuela, Cercado de Lima) y **CD Arequipa** (centro de distribución regional; es un supuesto que conecta el proyecto con la sede UTP Arequipa).

### Estacionalidad (el eje del caso de negocio)

| Línea | Temporada alta | Consecuencia para el ERP |
|---|---|---|
| Helados | Verano (diciembre a marzo) [S] | Producción anticipada en invierno, stock en cámara a −18 °C o menos, más heladeros y rutas en verano |
| Panetón | Campaña de Navidad (octubre a diciembre) [V] | Planificación de producción por lotes con vencimiento corto; listas de precios de campaña |
| Chocolates | Todo el año, con picos en fechas comerciales [S] | Producción continua; FEFO por vencimiento |

La complementariedad de helados en verano y panetón en Navidad permite usar la misma capacidad de planta, almacenes y fuerza de distribución todo el año. Este es el argumento central del análisis empresarial.

## 1.2 Alcance funcional (qué entra y qué no)

**Entra** (en dos fases, ver [04 §4.3](04_scrum_pmbok.md)):
- **Fase 1 (núcleo garantizado):** todo con Odoo estándar configurado por código en `donofrio_base`.
- **Fase 2 (completa, con hora de corte el jueves 26/11/2026, 08:00; lo no fusionado queda como trabajo futuro):** módulos propios para heladeros, calidad, cadena de frío y tablero OWL.

Las áreas que cubre:
- Marketing y Ventas: CRM, Ventas, Punto de Venta y liquidación de heladeros.
- Logística: inventario con lotes, vencimiento, FEFO y cadena de frío.
- Producción: MRP con listas de materiales y calidad propia.
- Gerencia: tablero de KPIs.
- Extras: Compras, Facturación con `l10n_pe` y RR. HH. (organigrama, empleados y puestos).

**No entra** (se declara como limitación o trabajo futuro):
- Envío de comprobantes a SUNAT/OSE: el módulo EDI `l10n_pe_edi` es Enterprise.
- Nómina peruana (Enterprise o terceros).
- Contabilidad completa con reportes financieros (`account_reports` es Enterprise).
- App móvil nativa.
- Integración con proveedores reales.
- Migración de datos históricos.
- Simulación de la transición a Froneri.

## 1.3 Supuestos declarados

Estos supuestos van en una tabla del informe (sección 3.2) con la etiqueta **"Supuesto académico"**.

| # | Supuesto | Por qué |
|---|---|---|
| S1 | Fecha de corte: 2026, operación normal bajo Nestlé Perú | La transición a Froneri no está confirmada para Perú |
| S2 | Los datos maestros (clientes, proveedores, empleados, precios, recetas y cantidades) son **ficticios pero verosímiles** | No hay acceso a datos internos; se cumple la Ley 29733 de datos personales |
| S3 | Los nombres de productos se inspiran en marcas públicas de D'Onofrio y Nestlé Perú. Las recetas, los precios y los tiempos de vida son estimados | Solo sirven para dar realismo a la demo |
| S4 | Los heladeros ambulantes son **concesionarios** que compran a precio de heladero y liquidan cada día lo vendido, lo devuelto y la merma | No hay un modelo de comisión público; es una simplificación |
| S5 | El helado se almacena a −18 °C o menos (estándar general de la industria); los insumos lácteos, entre 2 y 6 °C | Son los rangos que usa el módulo de cadena de frío |
| S6 | CD Arequipa es un almacén regional que se abastece desde la Planta Lima | Permite mostrar transferencias entre almacenes |
| S7 | La situación actual es: Excel y registros manuales para liquidaciones de heladeros, temperaturas e inspecciones; sistemas separados por área | Es la base del análisis AS-IS y de la tabla de oportunidades |
| S8 | Hay un solo servidor (contenedores) más una réplica de base de datos | Es suficiente para el alcance académico |
| S9 | Moneda PEN, IGV 18 %, idioma es_PE y zona horaria America/Lima | Contexto peruano |

## 1.4 Datos verificados de la empresa

Leyenda: **[V]** verificado con fuente · **[P]** reportado por una sola fuente o sin fecha clara (citar con cautela) · **[S]** supuesto

| Dato | Estado | Fuente (año) |
|---|---|---|
| Fundada en 1897 por Pedro (Pietro) D'Onofrio, inmigrante italiano que aprendió el oficio en Argentina; empezó vendiendo helados en carretilla | [V] | Wikipedia "D'Onofrio (brand)" (consulta 2026); Infomercado (2023); Mercado Negro (2026) |
| En 1919 los carritos se pintan de amarillo, color que se mantiene | [V] | Wikipedia (consulta 2026) |
| Fábrica de chocolates desde 1924 (Jr. Cotabambas) | [V] | Gestión / Peru Retail (historia de la marca) |
| La fórmula del panetón llega de Italia en 1950 (Alemagna, Milán) | [V] | Gestión / Peru Retail |
| En los años 50 la planta pasa a la Av. Venezuela (exfundo Aramburú, unos 36 000 m²) | [V] | Gestión / Peru Retail |
| Nestlé la compra en 1997 y mantiene la operación en la Av. Venezuela | [V] | Wikipedia; Peru Retail |
| Precio de compra de unos US$ 80 millones | [P] | Peru Retail (sin documento primario) |
| Más de 6 000 heladeros, unos 400 helados por triciclo al día | [P] (dato de 2022) | El Popular (31/07/2022) |
| Panetón D'Onofrio: alrededor del 30 % del mercado en 2024; el mercado mueve unos US$ 125 millones al año | [P] | CMA citado en LinkedIn (2024); El Comercio (año no indicado) |
| Panetón Delicia / Delicia Bites (campaña 2025-2026) | [V] | La República, publirreportaje (18/11/2026) |
| Nestlé Perú tiene cerca de la mitad del mercado peruano de chocolates (Sublime y otras) | [P] | Gestión; Infomercado (2024) |
| Nestlé Perú exporta Sublime, Princesa y Triángulo a EE. UU. | [V] | America Retail |
| **Feb-2026:** Nestlé anuncia negociaciones avanzadas para vender su negocio global de helados a Froneri (*joint venture* con PAI Partners); transición de 12 a 18 meses | [V] | Infobae (20/02/2026); El Comercio (2026) |
| Nestlé Perú: "evaluando detalles y próximos pasos en Perú"; no hay anuncio sobre D'Onofrio | [V] | El Comercio (2026); Gestión (2026) |
| **Jun-2026:** Froneri inicia el registro de su denominación y logotipo ante Indecopi. No confirma un cambio de dueño | [V] | Peru Retail (16/06/2026); Mercado Negro (24/06/2026) |
| El traspaso efectivo de las marcas de helados se espera durante 2027 | [P] | Prensa peruana (2026); no hay comunicado de Froneri para Perú |

> Para el informe: cada dato [V] o [P] se cita en formato **APA 7** en la sección 9. Los datos [P] se redactan con "según…" y nunca como hechos de la empresa.

### Fuentes (enlaces)

- Wikipedia. *D'Onofrio (brand)*. https://en.wikipedia.org/wiki/D%27Onofrio_(brand)
- Gestión. *D'Onofrio: de una carretilla a ser vendida a Nestlé…* https://gestion.pe/economia/empresas/donofrio-de-una-carretilla-a-ser-vendida-a-nestle-y-competir-con-alicorp-helados-grupo-romero-lamborgini-noticia/
- Mercado Negro. *D'Onofrio: la exitosa compañía que inició con una carretilla de helados.* https://mercadonegro.pe/marketing/marcas/donofrio-la-exitosa-compania-que-inicio-con-una-carretilla-de-helados
- Infomercado (2023). *Pietro D'Onofrio: la historia del pionero…* https://infomercado.pe/pietro-donofrio-la-historia-del-pionero-de-las-heladerias-y-confiterias-en-el-peru-helados-080223-gb/
- Peru Retail. *D'Onofrio: ¿cuántos millones pagó Nestlé…?* https://www.peru-retail.com/donofrio-cuantos-millones-pago-nestle-por-la-tradicional-marca-peruana-de-helados/
- El Popular (2022). *D'Onofrio: de vender helados en una carretilla…* https://elpopular.pe/actualidad/2022/07/31/donofrio-historia-como-pasaron-vender-helados-carretilla-madera-ser-empresa-exitosa-peru-142580
- El Comercio. *Mercado de panetones mueve unos US$125 millones al año.* https://elcomercio.pe/economia/negocios/mercado-panetones-mueve-us-125-millones-ano-peru-150832-noticia/
- La República (2026). *Panetón D'Onofrio: Delicia Bites…* https://larepublica.pe/publirreportajes/2026/11/18/paneton-donofrio-conoce-delicia-bites-y-delicia-doble-tentacion-826146
- Gestión. *Nestlé Perú y su fórmula… chocolates.* https://gestion.pe/economia/empresas/nestle-peru-y-su-formula-para-lograr-crecimiento-a-doble-digito-en-la-linea-de-chocolates-consumidores-sublime-kit-kat-puntos-de-venta-marketing-noticia/
- America Retail. *Nestlé impulsa icónicas marcas peruanas hacia Estados Unidos.* https://americaretail-malls.com/paises/peru/nestle-impulsa-iconicas-marcas-peruanas-hacia-estados-unidos/
- Infobae (2026). *Multinacional Nestlé abandona el negocio heladero…* https://www.infobae.com/peru/2026/02/20/multinacional-nestle-abandona-el-negocio-heladero-en-todo-el-mundo-helados-donofrio-se-van-de-peru/
- El Comercio (2026). *Nestlé sobre venta de su negocio global de helados…* https://elcomercio.pe/economia/negocios/nestle-sobre-venta-de-su-negocio-global-de-helados-estamos-evaluando-detalles-y-proximos-pasos-en-peru-donofrio-noticia/
- Gestión (2026). *¿D'Onofrio dejará de ser de Nestlé? Froneri ya dio su primer paso en Perú.* https://gestion.pe/economia/empresas/donofrio-dejara-de-ser-de-nestle-froneri-ya-dio-su-primer-paso-en-peru-noticia/
- Peru Retail (2026). *¿D'Onofrio cambiará de dueño? Froneri registra su marca en Perú.* https://www.peru-retail.com/donofrio-cambiara-de-dueno-froneri-registra-su-marca-en-peru-y-crecen-senales-de-una-transicion/
- Mercado Negro (2026). *Nestlé negocia la venta global de su negocio de helados…* https://www.mercadonegro.pe/actualidad/nestle-negocia-la-venta-global-de-su-negocio-de-helados-y-abre-interrogantes-sobre-donofrio-en-peru/

## 1.5 Organigrama propuesto [S]

Se carga en RR. HH. (`hr.department` con `parent_id`) y se exporta como figura de la sección 3.

```
Gerencia General (Unidad Helados y Confitería)
├── Marketing y Ventas ── Canal Moderno · Canal Tradicional · Heladeros (rutas y liquidación)
├── Logística y Distribución ── Almacén Planta Lima (cámaras de frío) · CD Arequipa · Despacho
├── Producción y Operaciones ── Línea Helados · Línea Chocolates · Línea Panetón · Aseguramiento de Calidad
├── Compras
├── Administración y Finanzas (Facturación)
├── Recursos Humanos
└── Tecnologías de la Información
```

## 1.6 Problemas que resuelve el ERP

Estos problemas van en la tabla 1 de la plantilla: "Identificación de oportunidades".

| ID | Problema empresarial (AS-IS, supuesto S7) | Oportunidad | Tecnología propuesta |
|---|---|---|---|
| 1 | La liquidación diaria de miles de heladeros se hace en papel o Excel, con descuadres y mermas no trazadas | Automatización | Módulo `donofrio_heladeros` en Odoo (F2-M2; en la F1, pedido + devolución estándar) |
| 2 | El vencimiento de lotes no se controla y el despacho no sigue FEFO | Integración en tiempo real | Inventario Odoo con lotes y `product_expiry` |
| 3 | Las temperaturas de las cámaras se registran a mano; las alertas llegan tarde | Digitalización y alertas | Cadena de frío en `donofrio_calidad` (F2-M3) |
| 4 | Las inspecciones de calidad están en papel y no se vinculan al lote producido | Trazabilidad | `donofrio_calidad` + MRP (F2-M1; en la F1, lotes y trazabilidad estándar) |
| 5 | La planificación de campañas (verano y Navidad) se hace sin datos consolidados | Analítica | Dashboards estándar y vistas pivote (F1) + tablero OWL (F2-M4) |
| 6 | Ventas, almacén y producción tienen sistemas separados y digitan dos veces | Integración de sistemas | ERP Odoo 19 único sobre PostgreSQL |
| 7 | La gerencia no tiene reportes oportunos | Analítica (BI) | Tablero gerencial y dashboards de Odoo |
