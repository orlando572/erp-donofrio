# 3.4 Despliegue

## 3.4.1 Enfoque y herramientas utilizadas

El sistema se despliega con Docker Compose en un solo equipo. Hay tres entornos: desarrollo (la PC de cada integrante, en `http://localhost:8069`), integración continua (los servidores de GitHub Actions, que prueban cada cambio) y la demostración protegida (`https://localhost:8443`, con Nginx, conexión cifrada y Odoo en modo producción con 2 procesos de trabajo).

| Aspecto | Decisión |
|---|---|
| Estrategia | Se reemplazan los contenedores en el mismo equipo: Docker vuelve a crear solo lo que cambió y espera a que quede saludable; hay unos segundos de corte, aceptables para una demostración |
| Vuelta atrás | Por versión: volver a la versión anterior del código o de la imagen publicada y, si los datos cambiaron, restaurar el respaldo en una base nueva |
| Respaldo previo | Antes de actualizar se ejecuta el script de respaldo, como indica el manual de instalación |
| Configuraciones | Básica (base de datos y Odoo) para desarrollo; con réplica de lectura; y protegida con Nginx, que se levanta con su propio script |

Procedimiento. Copiar el archivo de parámetros de ejemplo y completar las contraseñas, levantar los contenedores y crear la base, cargar los datos de demostración, levantar el despliegue protegido (con un certificado propio) y ejecutar el script de verificación del despliegue; la réplica y el respaldo son opcionales. Resultados. La verificación del despliegue comprueba siete grupos de controles y todos pasaron; la base, la réplica y Odoo quedan en estado saludable. La imagen publicada (3.25 GB) arranca sola, carga 109 módulos y su prueba confirma Odoo 19.0, los módulos de D'Onofrio y la auditoría.

Herramientas. Git y GitHub (cambios con revisión cruzada y ramas protegidas), Docker 29.1.3 y Compose 2.40.3 (la misma configuración en las dos PC y en las pruebas automáticas), GitHub Actions (pruebas y publicación), GHCR (registro de imágenes de GitHub) y Nginx 1.30.7 (HTTPS, cabeceras de seguridad y compresión). No se usa Kubernetes porque, con un solo equipo, no hay varias copias de Odoo que coordinar.

### Pipeline CI/CD

El pipeline de integración y entrega continuas (CI/CD) automatiza el camino de cada cambio: pruebas, revisión, fusión y publicación.

![Pipeline CI/CD](../diagramas/arquitectura/pipeline_cicd.png)

*Figura 5.15-a. Pipeline CI/CD: de la rama de trabajo a la versión y al despliegue en el nodo. Línea continua: automático en GitHub Actions; línea punteada: paso manual.*

| Flujo | Cuándo corre | Qué hace |
|---|---|---|
| Integración continua | En cada cambio propuesto, al fusionar en develop y main, cada lunes a las 06:00 de Lima y a pedido | Revisa el estilo y el código obsoleto (11 s), instala los módulos en una base nueva y corre todas las pruebas (199 s), y prueba la réplica (24 s), el respaldo (65 s) y el despliegue protegido (105 s). Las dos primeras son obligatorias para fusionar |
| Rendimiento | A pedido | Carga los datos, levanta el despliegue protegido, mide la carga con k6 y la seguridad con ZAP, y guarda los reportes |
| Publicación | Al crear una versión (v1.x.y) | Construye y prueba la imagen, arma el zip del código y publica ambos en GitHub |

Las ramas develop y main exigen una aprobación, observaciones resueltas y las pruebas en verde, y no permiten reescribir el historial. Cada cambio de trabajo entra a develop como un solo commit y las versiones salen de main.

### Resultados: releases y URLs

Se publicaron cinco versiones: v1.0.0 (24/11/2026, núcleo) y, el 25/11/2026, v1.1.0 (M1, Calidad), v1.2.0 (M2, Liquidación de heladeros), v1.3.0 (M3, cadena de frío) y v1.4.0 (M4, Tablero gerencial y marca). Cada una trae el zip del código (de 23,5 a 26,1 MiB) y su imagen instalable. El ERP protegido corre en `https://localhost:8443` y el de desarrollo en `http://localhost:8069`; la base principal y la réplica solo aceptan conexiones desde el propio equipo.

## 3.4.2 Mejores prácticas

| Práctica | Cómo se aplica |
|---|---|
| Infraestructura como código | La misma configuración de Docker en las dos PC y en las pruebas automáticas; Nginx, la imagen y los scripts están en el repositorio |
| Versiones fijas | Odoo y la auditoría en versiones fijas, y una imagen y un zip por cada versión publicada, que no se modifican |
| Verificar después de desplegar | Los scripts de verificación revisan el despliegue, la réplica, el respaldo y la imagen, y avisan con error si algo falla |
| Respaldo antes de cambiar | Respaldo antes de actualizar y vuelta atrás a la versión anterior o restauración en una base nueva (31 s) |
| Secretos fuera del repositorio | Las contraseñas están en un archivo que no se sube a GitHub; en modo protegido Odoo exige una contraseña maestra de 16 o más caracteres; GitHub revisa que no se suban claves por error |
| Superficie mínima | Odoo y la base de datos solo aceptan conexiones desde el propio equipo; el gestor de bases de datos está deshabilitado y Odoo corre en modo producción |
