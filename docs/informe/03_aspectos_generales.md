# 1. Aspectos generales

## 1.1 Definición del problema

D'Onofrio (helados, chocolates y panetón) opera con un negocio estacional, una red de distribución muy atomizada (miles de heladeros ambulantes) y productos perecibles que dependen de la cadena de frío. En el escenario del proyecto (corte 2026) la información de cada área vive en hojas de cálculo, papel y correos, lo que produce cuatro dificultades: (1) la liquidación diaria de los heladeros se hace en papel o Excel, con descuadres y mermas que nadie rastrea hasta un lote; (2) el producto vence sin que nadie lo vea a tiempo, porque no hay control de vencimiento por lote ni despacho FEFO (el que vence primero sale primero); (3) las temperaturas y las inspecciones se anotan a mano y no se ligan al lote; y (4) la gerencia decide tarde y sin datos consolidados, porque ventas, almacén y producción digitan dos veces.

Problema central. ¿Cómo puede D'Onofrio integrar ventas, logística, producción y gestión en un solo sistema, de modo que cada lote sea trazable desde la compra del insumo hasta el cliente y la gerencia vea datos confiables a tiempo, con una plataforma abierta (Odoo 19 Community) y sin licencias Enterprise?

Solución propuesta. Un ERP sobre Odoo 19.0 Community y PostgreSQL 16 en Docker (Odoo S. A., 2025; PostgreSQL Global Development Group, 2023), en dos fases: un núcleo con Odoo estándar configurado por código (módulo de configuración base) y cuatro módulos desarrollados para D'Onofrio (calidad, liquidación de heladeros, cadena de frío y tablero gerencial), publicados en las versiones v1.1.0 a v1.4.0.

## 1.2 Descripción del problema

### 1.2.1 Situación actual y datos de la empresa

D'Onofrio fue fundada en 1897 por Pedro (Pietro) D'Onofrio, un inmigrante italiano que empezó vendiendo helados en carretilla; en 1919 pintó los carritos de amarillo, color que se mantiene (Infomercado, 2023; Wikipedia, 2026). Abrió su fábrica de chocolates en 1924, incorporó la fórmula del panetón en 1950 y pasó a la planta de la Av. Venezuela en los años 50 (Gestión, 2025; Peru Retail, 2026); Nestlé la compró en 1997. Según El Popular (2022), hay más de 6 000 heladeros. En febrero de 2026 Nestlé anunció negociaciones para vender su negocio global de helados a Froneri (Infobae, 2026); el proyecto lo trata como riesgo del entorno y no lo modela, porque para Perú no hay nada confirmado.

El giro es la fabricación y comercialización de helados, chocolates y panetón, con venta por canal moderno (autoservicios), canal tradicional (bodegas y distribuidores), punto de venta propio y heladeros concesionarios. El escenario modelado es la unidad de helados y confitería de Nestlé Perú, con corte en 2026 y dos sedes: Planta Lima y el CD Arequipa, abastecido desde Lima. La estacionalidad marca el caso: los helados tienen su temporada alta en verano, de diciembre a marzo; el panetón, en la campaña de Navidad, de octubre a diciembre; y los chocolates se producen todo el año, con picos en fechas comerciales. Eso exige producción anticipada, listas de precios de campaña y FEFO por vencimiento.

### 1.2.2 Áreas y trabajadores

El ERP cubre las cinco áreas que piden los lineamientos: Marketing y Ventas, Logística y Distribución, Producción y Operaciones, Gerencia y Extras (Compras, Administración y Finanzas, Recursos Humanos y TI), con el organigrama cargado en el módulo de Recursos Humanos de Odoo. Son 21 empleados, diez de ellos con usuario en el ERP según su rol; los heladeros no son empleados sino concesionarios que compran a precio de heladero y liquidan cada día, por lo que se modelan como contactos.

### 1.2.3 Problemas y oportunidades

Los problemas describen la situación actual. La última columna muestra el estado final, con la Fase 2 completa.

**Tabla 3.1. Problemas, oportunidades y tecnología propuesta**

| ID | Problema | Oportunidad y tecnología | Estado final |
|---|---|---|---|
| 1 | Liquidación de heladeros en papel, con descuadres | Automatización: el módulo de Liquidación de heladeros | Resuelto (M2) |
| 2 | Vencimientos sin control y despacho sin FEFO | Integración: inventario con lotes y el control de vencimientos de Odoo | Resuelto |
| 3 | Temperaturas a mano y alertas tardías | Alertas: cadena de frío en el módulo de Calidad | Resuelto (M3) |
| 4 | Inspecciones en papel, sin ligar al lote | Trazabilidad: el módulo de Calidad | Resuelto (M1) |
| 5 | Campañas sin datos consolidados | Analítica: dashboards y tablero OWL | Resuelto (M4) |
| 6 | Sistemas separados y doble digitación | Un solo ERP sobre PostgreSQL | Resuelto |
| 7 | La gerencia sin reportes oportunos | BI con dashboards de Odoo | Resuelto |

### 1.2.4 Supuestos académicos

Los datos maestros son ficticios pero verosímiles (Ley 29733); el corte es 2026 bajo Nestlé Perú; los productos se inspiran en marcas públicas con recetas, precios y vida útil estimados; los heladeros son concesionarios; el helado se guarda a −18 °C o menos y los lácteos entre 2 y 6 °C; el CD Arequipa se abastece desde Lima; la situación actual se basa en Excel y registros manuales; hay un servidor de contenedores con réplica de base de datos; y el contexto es peruano: PEN, IGV 18 %, es_PE y America/Lima.

## 1.3 Visión

Ser la unidad de helados y confitería que llega fresca y a tiempo a cada rincón del país, con cada lote trazable de la compra del insumo hasta el cliente y decisiones tomadas con datos del día.


## 1.4 Misión

Elaborar y distribuir helados, chocolates y panetón de calidad, cuidando la cadena de frío y el vencimiento de cada lote, apoyados en un sistema integrado que conecta ventas, almacenes, producción y gerencia, y que acompaña tanto al canal moderno como al heladero de cada triciclo.

## 1.5 Entorno

### 1.5.1 Análisis PESTEL

En lo político, pesan la política comercial del país y la transición de Nestlé a Froneri, que se declara como riesgo y no se modela. En lo económico, la estacionalidad marcada, un mercado de panetón concentrado en la campaña navideña y los precios de lácteos y cacao justifican listas de precios por temporada. En lo social, la marca de arraigo histórico y el heladero como figura popular piden un trato diferenciado a ese canal. En lo tecnológico, los comprobantes electrónicos son obligatorios (Superintendencia Nacional de Aduanas y de Administración Tributaria [SUNAT], s. f.) y Odoo Community emite facturas y boletas con IGV mediante la localización peruana. En lo ecológico, el consumo de energía de las cámaras y los residuos de empaque se reflejan en el registro de temperaturas y mermas. En lo legal, rigen la Ley 29733 de datos personales (Congreso de la República del Perú, 2011), el D. S. 007-98-SA de vigilancia sanitaria y HACCP (Codex Alimentarius Commission, 2020; Ministerio de Salud, 1998) y el IGV de 18 %.

### 1.5.2 Cinco fuerzas de Porter

La rivalidad es alta (marcas de Alicorp/Lamborgini y Gloria, panaderías y heladerías artesanales; Gestión, 2025). Los nuevos entrantes son una amenaza media: el *delivery* entra con poca inversión, pero la red de distribución y las cámaras de frío son una barrera. El poder de los clientes es medio-alto (los autoservicios negocian) y el de los proveedores, medio (pocos proveedores de lácteos, cacao y harina); los sustitutos son una amenaza media. Si los helados pasan a Froneri, el diseño separa líneas de producto y canales para que el ERP siga útil con chocolates y panetón.

## 1.6 Estrategia empresarial

### 1.6.1 Análisis FODA

Las fortalezas son la marca histórica desde 1897, la red extensa de heladeros, la planta propia y un portafolio complementario entre verano y Navidad. Las debilidades son los procesos en Excel y papel, la falta de control de vencimiento por lote, la liquidación manual y los sistemas separados por área. Las oportunidades son un ERP abierto sin licencias Enterprise, los datos para planificar campañas, las exportaciones de chocolates y la trazabilidad como diferencial. Las amenazas son la venta de helados a Froneri, los precios de insumos, los competidores con mayor distribución y la normativa sanitaria y de etiquetado.

### 1.6.2 Estrategias cruzadas

- FO: usar los datos de ventas por canal y temporada para anticipar la producción de verano y de Navidad con la red de heladeros existente.
- DO: reemplazar Excel y papel por un solo ERP y digitalizar la liquidación de heladeros para detectar descuadres y mermas.
- FA: diversificar entre helados, chocolates y panetón para amortiguar la pérdida eventual de la línea de helados.
- DA: controlar vencimientos y temperaturas para evitar pérdidas ante precios altos de insumos.

### 1.6.3 Cascada de metas de COBIT 2019

COBIT 2019 (ISACA, 2018) sirve de referencia, sin evaluar madurez: integrar procesos (EG08, AG08, BAI03) con Odoo configurado por código y probado de punta a punta; disponibilidad en temporada alta (EG06, APO09, DSS01, DSS04) con despliegue protegido, réplica y respaldos; protección de la información (EG02, EG03, AG07, APO12, APO13, DSS05) con TLS, verificación en dos pasos y auditoría; cambio sin romper la operación (AG06, BAI06, DSS02, DSS03) con cambios revisados por el otro integrante (*pull requests*, PR) e integración continua; y decidir con datos (EG07, AG10, MEA01) con tableros e indicadores clave (KPI).

## 1.7 Planificación empresarial

Los objetivos estratégicos se organizan en un cuadro de mando integral sencillo y se ligan a indicadores que el ERP calcula (2.7.2); las metas son supuestos académicos.

**Tabla 3.2. Objetivos estratégicos e indicadores**

| Perspectiva | Objetivo | Indicador (KPI) | Meta |
|---|---|---|---|
| Financiera | Crecer la venta por canal y temporada | Ventas del mes por canal y línea | +10 % anual |
| Financiera | Reducir pérdidas por vencimiento | Stock vencido o por vencer a 30 días | < 2 % del inventario |
| Cliente | Cumplir los pedidos a tiempo | Pedidos entregados a tiempo | ≥ 95 % |
| Cliente | Atender bien al canal heladero | Descuadre de liquidación | < 2 % del despachado |
| Procesos internos | Trazar todos los lotes | Lotes con trazabilidad completa | 100 % |
| Aprendizaje | Personal y roles al día | Usuarios con empleado asignado | 100 % |
