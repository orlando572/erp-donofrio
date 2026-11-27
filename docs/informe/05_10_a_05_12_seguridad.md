# 5.10 a 5.12 Gestión de seguridad de la información: riesgos, controles, ataques y defensa

El proyecto se alinea con ISO 27001 (ISO/IEC, 2022), ISO 31000 (ISO, 2018), OWASP (OWASP Foundation, 2021) e ISO 22301 (ISO, 2019) (la declaración de aplicabilidad está en el anexo 10.7). Los riesgos se evalúan con las escalas del plan de riesgos (2.5.1): impacto (I) y probabilidad (P) de 1 a 3, nivel = I × P, con prioridad Alta (6 a 9), Media (3 a 5) o Baja (1 a 2). Los activos son los datos del negocio, las cuentas, la base con su archivos adjuntos, el servicio web y el código. Las mediciones son del 23/11/2026; los módulos de la Fase 2 no cambiaron estos controles y sus permisos están en 3.1.4.2 a 3.1.4.5.

## 3.2.1 Identificación de riesgos de seguridad

Se identificaron 16 riesgos del sistema desplegado: 11 de prioridad Alta (nivel 6), 4 Media y 1 Baja. La tabla de la sección siguiente los agrupa junto con el control que los trata.

## 3.2.2 Identificación de controles de seguridad

### Tabla 16. Riesgos, controles y riesgo residual

La eficacia (Ef.) es 3 si el control es automático y está verificado con una prueba repetible, 2 si se verificó una vez y 1 si solo está documentado.

| Riesgo (nivel inicial) | Control implementado | Ef. | Residual | Evidencia |
|---|---|---|---|---|
| RSI-01 Acceso indebido a datos de otra área o almacén (6) | Mínimo privilegio: 10 usuarios por rol sin administradores, grupo «Solo operaciones del CD Arequipa», 4 reglas de acceso por almacén y permisos por modelo | 3 | 3 Media | 9 pruebas que comprueban el acceso denegado |
| RSI-02 y 03 Fuerza bruta y contraseñas débiles (6) | Contraseña mínima de 12 caracteres con hash PBKDF2-SHA512; bloqueo tras 5 intentos por 60 s | 2 | 3 Media | Pruebas y verificación del despliegue |
| RSI-04 Toma de control del administrador o gerente (6) | Segundo factor obligatorio (TOTP o código por correo) en el despliegue protegido | 3 | 3 Media | 6 pruebas |
| RSI-05 Intercepción de tráfico o robo de sesión (6) | Nginx con TLS 1.2 y 1.3, redirección a HTTPS y HSTS | 3 | 3 Media | TLS 1.1 rechazado |
| RSI-06 Inyección SQL o XSS (6) | Solo ORM, sin SQL crudo, y escape automático de QWeb | 3 | 3 Media | Entradas maliciosas devuelven 0 filas y salen escapadas |
| RSI-07 Gestor de BD o PostgreSQL expuestos (6) | Gestor de bases de datos de Odoo deshabilitado, puertos solo dentro del propio equipo y contraseñas cifradas en PostgreSQL | 3 | 3 Media | Verificación del despliegue |
| RSI-08 y 12 Configuración insegura y secretos en el repositorio (6) | Odoo rechaza una contraseña maestra corta o de ejemplo y corre en modo producción; las contraseñas no se suben al repositorio y GitHub revisa que no se filtren claves | 3 | 3 Media | Verificación del despliegue e imagen |
| RSI-09 Pérdida o corrupción de datos (6) | Respaldo con SHA-256 y retención de 7 días, restauración en base nueva y réplica | 2 | 4 Media | RTO de 31 s (objetivo 2 h) |
| RSI-10 Indisponibilidad (4) | Reinicio automático y chequeos de salud | 1 | 4 Media | Los tres contenedores en estado saludable |
| RSI-11 Cambios sin rastro en precios y pedidos (6) | El registro de auditoría sobre listas de precios y pedidos de venta y compra | 3 | 3 Media | Prueba del cambio de precio con usuario, fecha y valores |
| RSI-13 y 14 Componentes vulnerables y código sin revisión (4) | Versiones fijadas; PR con aprobación del otro integrante y CI (estilo (lint) y pruebas) obligatorio | 2 | 2 Baja | Versiones fijas en la imagen y CI obligatorio en cada PR |

Los riesgos de cabeceras laxas (RSI-15, política de contenido del navegador) y de datos personales (RSI-16, datos ficticios) quedan en prioridad Baja. Los 11 riesgos de prioridad Alta pasan a nivel residual 3 o 4 (Media) y ninguno queda en Alta.

## 3.2.3 Identificación de ataques y defensa

### Tabla 17. Ataques, defensa y prueba

| Ataque (OWASP 2021) | Cómo se intentó | Defensa | Resultado |
|---|---|---|---|
| XSS (A03) | Inyectar un programa (`<script>`) en un parámetro del inicio de sesión | Odoo convierte el texto en inofensivo antes de mostrarlo y la política de contenido bloquea scripts ajenos | Sale escapado; ZAP lo clasificó informativo |
| Fuerza bruta (A07) | Intentos repetidos de inicio de sesión | Bloqueo tras 5 intentos, contraseñas de 12 o más caracteres y segundo factor | Mitigado: los intentos bloqueados quedan en el registro |
| Robo de sesión (A02, A07) | Leer la cookie por JavaScript, capturarla en la red o clickjacking | Cookie de sesión protegida (no legible por JavaScript y solo por HTTPS), conexión cifrada, bloqueo de inserción en otras páginas y segundo factor | Mitigado |

La inyección SQL (A03) se rechazó con entradas maliciosas por JSON-RPC (0 filas, tabla intacta), el gestor de BD responde 404 (A05) y la pérdida de datos es recuperable en 31 s. Otras categorías con evidencia: A05 (ZAP *baseline* con 0 alertas altas y 58 reglas pasivas sin hallazgo), A06 (imagen y el registro de auditoría fijados), A09 (el registro de auditoría e inicios de sesión registrados) y A08 (CI obligatorio y ramas protegidas).
