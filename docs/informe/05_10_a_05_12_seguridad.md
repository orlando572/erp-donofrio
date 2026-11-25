# 5.10 a 5.12 Gestión de seguridad de la información: riesgos, controles, ataques y defensa

El proyecto se alinea con ISO 27001, ISO 31000, OWASP e ISO 22301 como buenas prácticas de referencia; no es una implementación certificada ni auditada (la declaración de aplicabilidad está en el anexo 10.6). Los riesgos se evalúan con las escalas del plan de riesgos (4.5.1): impacto (I) y probabilidad (P) de 1 a 3, nivel = I × P, con prioridad Alta (6 a 9), Media (3 a 5) o Baja (1 a 2). Los activos son los datos del negocio, las cuentas, la base con su *filestore*, el servicio web y el código. Las mediciones son del 23/11/2026; los módulos de la Fase 2 no cambiaron estos controles y sus permisos están en 5.5b a 5.5e.

## 5.10 Identificación de riesgos de seguridad

Se identificaron 16 riesgos del sistema desplegado: 11 de prioridad Alta (nivel 6), 4 Media y 1 Baja. La tabla de la sección siguiente los agrupa junto con el control que los trata.

## 5.11 Identificación de controles de seguridad

### Tabla 16. Riesgos, controles y riesgo residual

La eficacia (Ef.) es 3 si el control es automático y está verificado con una prueba repetible, 2 si se verificó una vez con alguna limitación y 1 si solo está documentado.

| Riesgo (nivel inicial) | Control implementado | Ef. | Residual | Evidencia y límite |
|---|---|---|---|---|
| RSI-01 Acceso indebido a datos de otra área o almacén (6) | Mínimo privilegio: 10 usuarios por rol sin administradores, grupo «Solo operaciones del CD Arequipa», 4 `ir.rule` y ACL | 3 | 3 Media | 9 pruebas con `AccessError`; las reglas por registro cubren solo el inventario |
| RSI-02 y 03 Fuerza bruta y contraseñas débiles (6) | Contraseña mínima de 12 caracteres con hash PBKDF2-SHA512; bloqueo tras 5 intentos por 60 s | 2 | 3 Media | Pruebas y verificación del despliegue; el contador es por IP y por *worker* |
| RSI-04 Toma de control del administrador o gerente (6) | Segundo factor obligatorio (TOTP o código por correo) en el despliegue protegido | 3 | 3 Media | 6 pruebas; el código por correo necesita un servidor de correo |
| RSI-05 Intercepción de tráfico o robo de sesión (6) | Nginx con TLS 1.2 y 1.3, redirección a HTTPS y HSTS | 3 | 3 Media | TLS 1.1 rechazado; certificado autofirmado |
| RSI-06 Inyección SQL o XSS (6) | Solo ORM, sin SQL crudo, y escape automático de QWeb | 3 | 3 Media | Entradas maliciosas devuelven 0 filas y salen escapadas |
| RSI-07 Gestor de BD o PostgreSQL expuestos (6) | `list_db = False`, 404 en `/web/database/`, puertos en `127.0.0.1` y `scram-sha-256` | 3 | 3 Media | Verificación del despliegue; Nginx publica 8080 y 8443 en todas las interfaces |
| RSI-08 y 12 Configuración insegura y secretos en el repositorio (6) | `admin_passwd` corta o de ejemplo rechazada, `workers = 2`, sin modo debug; `.env` fuera de Git; *secret scanning* y *push protection* | 3 | 3 Media | Verificación del despliegue e imagen; la contraseña de prueba es de desarrollo |
| RSI-09 Pérdida o corrupción de datos (6) | Respaldo con SHA-256 y retención de 7 días, restauración en base nueva y réplica | 2 | 4 Media | RTO de 31 s (objetivo 2 h); réplica asíncrona y respaldos sin cifrar |
| RSI-10 Indisponibilidad (4) | Reinicio automático y *healthchecks* | 1 | 4 Media | Un solo nodo y sin medición continua |
| RSI-11 Cambios sin rastro en precios y pedidos (6) | `auditlog` sobre listas de precios y pedidos de venta y compra | 3 | 3 Media | Prueba del cambio de precio con usuario, fecha y valores |
| RSI-13 y 14 Componentes vulnerables y código sin revisión (4) | Versiones fijadas; PR con aprobación del otro integrante y CI (`lint` y `test`) obligatorio | 2 | 2 Baja | Dependabot no está configurado |

Los riesgos de cabeceras laxas (RSI-15, CSP que admite `unsafe-inline` por OWL) y de datos personales (RSI-16, datos ficticios y sin política de privacidad) quedan en prioridad Baja. Los 11 riesgos de prioridad Alta pasan a nivel residual 3 o 4 (Media) y ninguno queda en Alta; los residuales de RSI-09 y RSI-10 dependen del despliegue en un solo equipo.

## 5.12 Identificación de ataques y defensa

### Tabla 17. Ataques, defensa y prueba

| Ataque (OWASP 2021) | Cómo se intentó | Defensa | Resultado y límite |
|---|---|---|---|
| XSS (A03) | `"><script>alert(1)</script>` en el parámetro `redirect` del login | Escape de QWeb y CSP | Sale escapado; ZAP lo clasificó informativo |
| Fuerza bruta (A07) | Intentos repetidos en `/web/login` | Bloqueo tras 5 intentos, contraseñas de 12 o más y 2FA | Mitigado: `Login attempt ignored` en el registro |
| Robo de sesión (A02, A07) | Leer la cookie por JavaScript, capturarla en la red o clickjacking | Cookie `HttpOnly; Secure; SameSite=Lax`, TLS, HSTS, `X-Frame-Options` y 2FA | Mitigado; la cookie dura 7 días y el certificado es autofirmado |

La inyección SQL (A03) se rechazó con entradas maliciosas por JSON-RPC (0 filas, tabla intacta), el gestor de BD responde 404 (A05) y la pérdida de datos es recuperable en 31 s. Otras categorías con evidencia: A05 (ZAP *baseline* con 0 alertas altas y 58 reglas pasivas sin hallazgo), A06 (imagen y `auditlog` fijados), A09 (`auditlog` e inicios de sesión registrados) y A08 (CI obligatorio y ramas protegidas). Los controles que el plan nombraba y no se implementaron son Uptime Kuma, Dependabot y la cinta de entorno de OCA.
