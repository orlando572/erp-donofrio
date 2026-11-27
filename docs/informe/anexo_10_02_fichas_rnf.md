# 10.2 Anexo: fichas de requerimientos no funcionales

Cada requerimiento no funcional se asocia a una característica de ISO/IEC 25010:2023 (ISO/IEC, 2023), según el juicio del equipo, y se verifica con una prueba repetible (3.3.1 y 3.3.2).

### Tabla 40. Fichas de requerimientos no funcionales

| ID | Requerimiento y meta | Resultado |
|---|---|---|
| RNF001 | Portabilidad: navegador de escritorio y vista adaptable; pedidos y PdV sin errores y pantallas de M2 y M4 sin desplazamiento horizontal en 375 × 812 | Cumple: verificado en escritorio y en 375 × 812 |
| RNF002 | Rendimiento: p95 < 2 s con 20 usuarios concurrentes, fallos < 1 % | Cumple: p95 de 12 ms |
| RNF003 | Usabilidad: interfaz en español y tareas clave en 3 pasos o menos | Cumple: revisión por roles y evaluación heurística |
| RNF004 | Trazabilidad del 100 % de los lotes: del insumo a la entrega | Cumple |
| RNF005 | Integridad: no se despacha un lote vencido, en fecha de retiro ni rechazado por calidad | Cumple: FEFO y bloqueo por calidad probados |
| RNF006 | Continuidad: respaldo diario, réplica en caliente y RTO ≤ 2 h | Cumple: RTO de 31 s |
| RNF007 | Mantenibilidad: módulos versionados, lint y pruebas en el CI | Cumple |
| RNF008 | Rendimiento del tablero y del acceso: LCP del tablero < 3 s y Lighthouse ≥ 80 en el login | Cumple: tablero en 2.11 s y login 100 |
| RNF009 | Seguridad: RBAC por 10 roles, HTTPS, gestor de BD cerrado, 2FA y ZAP sin alertas altas | Cumple: 10 roles, TLS, 2FA y 0 alertas altas |
| RNF010 | Auditoría: un cambio en precios o pedidos deja registro | Cumple para precios, pedidos y compras; los módulos desarrollados para D'Onofrio registran el historial del documento |
| RNF011 | Disponibilidad ≥ 99 % en horario laboral, con reinicio automático y chequeo de salud | Configurado: reinicio automático y chequeo de salud; contenedores en estado saludable |
| RNF012 | Reproducibilidad: el entorno se levanta con un comando y deja Odoo y PostgreSQL saludable | Cumple |
| RNF013 | Ley 29733: ningún dato real de personas ni RUC real en el repositorio | Cumple: todos los datos son ficticios |

Las fichas completas incluyen además el método de verificación y los riesgos relacionados; el resumen por requisito está en 2.2.1.2 y en la matriz de trazabilidad (10.8).
