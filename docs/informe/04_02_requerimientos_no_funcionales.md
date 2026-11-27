# 2.2.1.2 Requerimientos no funcionales

Cada RNF se asigna a una característica del modelo ISO/IEC 25010:2023 (ISO/IEC, 2023) y tiene una métrica y una prueba concreta; las pruebas automáticas corren en el CI y las de rendimiento, seguridad, respaldo y réplica se ejecutaron sobre el despliegue protegido (3.3.2). Las fichas están en el anexo 10.2.

**Tabla 4.3. Requerimientos no funcionales**

| Código | Requerimiento (característica ISO 25010) | Resultado | Estado |
|---|---|---|---|
| RNF001 | Interfaz adaptable a ventana angosta (flexibilidad) | Tablero y liquidación sin desplazamiento horizontal en 375 × 812 | Cumple |
| RNF002 | Tiempo de respuesta del 95 % de las peticiones (p95) < 2 s con 20 usuarios (eficiencia) | k6: 11.6 ms en listas y 9.1 ms en formularios | Cumple |
| RNF003 | Interfaz en español y tareas en ≤ 3 pasos (interacción) | español de Perú; la revisión por roles corrigió los textos en inglés | Cumple |
| RNF004 | Trazabilidad del 100 % de los lotes (adecuación funcional) | Pruebas de integración de compra a factura | Cumple |
| RNF005 | No se despacha un lote vencido ni rechazado (seguridad) | FEFO y bloqueo por calidad probados | Cumple |
| RNF006 | Respaldo diario, réplica y RTO ≤ 2 h (fiabilidad) | RTO de 31 s; réplica con retraso de 2.3 ms | Cumple |
| RNF007 | Módulos versionados, lint y pruebas en CI (mantenibilidad) | 224 pruebas en verde | Cumple |
| RNF008 | Tablero en < 3 s y Lighthouse ≥ 80 en el login (eficiencia) | Tablero en 2.11 s; login 100 | Cumple |
| RNF009 | Permisos por rol (RBAC), HTTPS, segundo factor de autenticación (2FA) y gestor de bases de datos deshabilitado (seguridad) | Diez roles, TLS, 2FA; ZAP sin alertas altas | Cumple |
| RNF010 | Auditoría de datos sensibles (seguridad) | El registro de auditoría en precios y pedidos; el resto usa el historial | Cumple |
| RNF011 | Disponibilidad ≥ 99 % (fiabilidad) | Reinicio automático y chequeo de salud; contenedores en estado saludable | Configurado |
| RNF012 | Entorno completo con un comando (flexibilidad) | Reproducido en dos PC y en el CI | Cumple |
| RNF013 | Ley 29733 con datos ficticios (seguridad) | Todos los datos de personas y RUC son ficticios | Cumple |

Los 13 RNF tienen su métrica, su prueba y su evidencia.
