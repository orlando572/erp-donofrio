# 4.5 Gestión de riesgos

## Escalas y método

El registro del proyecto tiene 27 riesgos: 15 de desarrollo, 8 de despliegue y 4 de mantenimiento. Cada uno se califica con **impacto (I)** y **probabilidad (P)** de 1 a 3; el **nivel** es I × P y define la prioridad: *Alta* (6 a 9, acción inmediata), *Media* (3 a 5, seguimiento constante) o *Baja* (1 a 2, monitoreo). Las estrategias son evitar, mitigar, aceptar y transferir (esta no aplica: el proyecto es de costo cero y sin proveedores). El seguimiento se hace en cada Planning y Retrospectiva con un comentario en el issue «Registro de riesgos», con evidencia repetible (un script, un trabajo del CI o una consulta a la API de GitHub), y el Product Owner valida los cambios de nivel. Las tablas presentan los riesgos principales de cada etapa con su situación al 25/11/2026.

## 4.5.3 Riesgos de despliegue

El despliegue es el paso de una versión probada a un entorno donde se usa: la PC de la demostración con el perfil `proxy`, la versión publicada y la entrega del informe y del código (5.15).

**Tabla 4.11. Riesgos de despliegue**

| Id | Riesgo | Nivel | Estrategia y situación al cierre |
|---|---|---|---|
| **R7** | PC con poca RAM para Odoo, PostgreSQL, réplica y Nginx | 4 (Media) | Mitigar con perfiles de Compose. Con k6, Nginx, Odoo y PostgreSQL juntos, Odoo llegó a 513 MiB: **mitigando** |
| **R9** | Falla la subida única a la plataforma académica | 6 (Alta) | Mitigar generando PDF y zip con margen. El zip de ensayo pesó 17 MB y las versiones publicadas, de 23,5 a 26,1 MiB; el límite de la plataforma no se conoce: **vigente hasta la entrega** |
| **R14** | La demostración en vivo falla | 6 (Alta) | Mitigar con una base de demostración reproducible por código, respaldada (2 s) y restaurable (31 s), y un despliegue verificado con 7 grupos de comprobaciones. El certificado autofirmado muestra una advertencia: **mitigando** |
| **RS-01** | Migración fallida de un módulo (`-u`) sobre una base con datos | 4 (Media) | La Definition of Done exige `-u`; el CI instala en una base nueva y los datos `noupdate` exigen recrear la base: **mitigando** |
| **RS-02** | Secretos expuestos en un repositorio público | 6 (Alta) | Evitar con `.gitignore`, *secret scanning* y *push protection*; Odoo en producción rechaza una contraseña maestra de menos de 16 caracteres: **mitigado con límites** |
| **RS-03** | Puerto del gestor de BD o `/web/database` abiertos | 3 (Media) | Evitar con red interna, `list_db = False` y puertos solo en `127.0.0.1`; ZAP sin alertas altas: **mitigado** |

## 4.5.4 Riesgos de mantenimiento

El mantenimiento es lo que ocurre después de desplegar: conservar datos y código, recuperar el servicio y detectar regresiones.

**Tabla 4.12. Riesgos de mantenimiento**

| Id | Riesgo | Nivel | Estrategia y situación al cierre |
|---|---|---|---|
| **R8** | Pérdida de trabajo (disco, rama borrada, BD corrupta) | 3 (Media) | Mitigar con *push* diario, ramas protegidas, base reproducible, respaldos y réplica con retraso de 2.3 ms. Todo está en el mismo equipo: **mitigado con límites** |
| **RS-04** | Respaldos no probados | 6 (Alta) | `restore.sh` probado: RTO de 31 s frente a 2 h, un respaldo alterado se rechaza por SHA-256 y el trabajo `backup` del CI corrió 36 veces con éxito. El *cron* diario está documentado: **mitigado** |
| **RS-05** | Disco lleno | 4 (Media) | Retención de 7 días y limpieza de imágenes. El disco de la PC de Orlando está al 91 % y Docker ocupa 15.6 GB: **en vigilancia** |
| **RS-06** | Lotes vencidos por un *cron* caído | 2 (Baja) | La exclusión de un lote vencido se evalúa al reservar (FEFO) y está probada; solo la alerta a 30 días depende del *cron*: **mitigado** |

El límite común del mantenimiento es que todo está en una sola PC; la copia fuera del equipo, el *cron* instalado y el cifrado se recomiendan en la sección 8.
