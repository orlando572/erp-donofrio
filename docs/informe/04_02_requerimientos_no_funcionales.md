# 4.2.3 Requerimientos no funcionales

Cada RNF se asigna a una característica del modelo ISO/IEC 25010:2023 (ISO/IEC, 2023) y tiene una métrica y una prueba concreta; las pruebas automáticas corren en el CI y las de rendimiento, seguridad, respaldo y réplica se ejecutaron sobre el despliegue protegido (5.14). *Cumple* significa medido o probado; *Cumple con límites*, que cumple la meta con una limitación declarada; y *Parcial*, que una parte cumple y otra no. Las fichas están en el anexo 10.2.

**Tabla 4.3. Requerimientos no funcionales**

| Código | Requerimiento (característica ISO 25010) | Resultado | Estado |
|---|---|---|---|
| RNF001 | Interfaz adaptable a ventana angosta (flexibilidad) | Tablero y liquidación sin desplazamiento horizontal en 375 × 812; solo Chrome | Parcial |
| RNF002 | p95 < 2 s con 20 usuarios (eficiencia) | k6: 11.6 ms en listas y 9.1 ms en formularios | Cumple |
| RNF003 | Interfaz en español y tareas en ≤ 3 pasos (interacción) | `es_PE`; la revisión por roles, hecha por el equipo, corrigió textos en inglés | Cumple con límites |
| RNF004 | Trazabilidad del 100 % de los lotes (adecuación funcional) | Pruebas de integración de compra a factura | Cumple |
| RNF005 | No se despacha un lote vencido ni rechazado (seguridad) | FEFO y bloqueo por calidad probados; el PdV no verifica vencimiento | Cumple con límites |
| RNF006 | Respaldo diario, réplica y RTO ≤ 2 h (fiabilidad) | RTO de 31 s; réplica con retraso de 2.3 ms | Cumple |
| RNF007 | Módulos versionados, lint y pruebas en CI (mantenibilidad) | 218 pruebas en verde | Cumple |
| RNF008 | Tablero en < 3 s y Lighthouse ≥ 80 (eficiencia) | Login 100, dashboard 80; tablero propio 2.11 s pero 76 y backend 59 | Parcial |
| RNF009 | RBAC, HTTPS, 2FA y gestor de BD deshabilitado (seguridad) | Diez roles, TLS, 2FA; ZAP sin alertas altas (pasivo, certificado autofirmado) | Cumple con límites |
| RNF010 | Auditoría de datos sensibles (seguridad) | `auditlog` en precios y pedidos; el resto usa el historial | Cumple |
| RNF011 | Disponibilidad ≥ 99 % (fiabilidad) | Reinicio automático y *healthcheck*; no se midió en el tiempo | Parcial |
| RNF012 | Entorno completo con un comando (flexibilidad) | Reproducido en dos PC y en el CI | Cumple |
| RNF013 | Ley 29733 con datos ficticios (seguridad) | Todos los datos son ficticios; no hay política de privacidad | Parcial |

En resumen, seis RNF cumplen, tres cumplen con límites y cuatro son parciales. Las metas son juicios del equipo sobre una instancia local con datos de demostración; no se midieron la disponibilidad en el tiempo ni otros navegadores distintos de Chrome.
