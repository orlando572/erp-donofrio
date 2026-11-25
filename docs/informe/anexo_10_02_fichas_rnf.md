# 10.2 Anexo: fichas de requerimientos no funcionales

Cada requerimiento no funcional se asocia a su característica de ISO/IEC 25010:2023 (ISO/IEC, 2023), que son juicios del equipo, y se verifica con una prueba repetible. Los estados son Cumple, Cumple con límites y Parcial.

### Tabla 40. Fichas de requerimientos no funcionales

| ID | Requerimiento y meta | Característica ISO 25010 | Verificación | Resultado |
|---|---|---|---|---|
| RNF001 | Portabilidad: navegador de escritorio y vista adaptable; pedidos y PdV sin errores y pantallas de M2 y M4 sin desplazamiento horizontal en 375 × 812 | Flexibilidad (adaptabilidad) | Revisión en escritorio y en ventana angosta, con capturas | **Parcial**: la revisión usó Chrome |
| RNF002 | Rendimiento: p95 < 2 s con 20 usuarios concurrentes, fallos < 1 % | Eficiencia de desempeño | k6 (5.14) | **Cumple**: p95 de 12 ms |
| RNF003 | Usabilidad: interfaz en español y tareas clave en 3 pasos o menos | Capacidad de interacción | Revisión por roles y evaluación heurística (6.12) | **Cumple con límites**: lo evaluó el equipo, sin tiempos por tarea |
| RNF004 | Trazabilidad del 100 % de los lotes: del insumo a la entrega | Adecuación funcional | Pruebas de integración de flujos | **Cumple** |
| RNF005 | Integridad: no se despacha un lote vencido, en fecha de retiro ni rechazado por calidad | Seguridad (integridad) | Pruebas de FEFO y de inspección | **Cumple con límites**: el punto de venta no verifica el vencimiento |
| RNF006 | Continuidad: respaldo diario, réplica en caliente y RTO ≤ 2 h | Fiabilidad (recuperabilidad) | Restauración cronometrada y réplica (5.9) | **Cumple**: RTO de 31 s |
| RNF007 | Mantenibilidad: módulos versionados, lint y pruebas en el CI | Mantenibilidad | CI con `ruff`, `check_legacy.sh` y 218 pruebas | **Cumple** |
| RNF008 | Rendimiento del tablero y del acceso: LCP del tablero < 3 s y Lighthouse ≥ 80 en el login | Eficiencia de desempeño | Lighthouse (5.14) | **Parcial**: login 100 y tablero en 2.11 s; tablero 76 y backend 59 son límite conocido |
| RNF009 | Seguridad: RBAC por 10 roles, HTTPS, gestor de BD cerrado, 2FA y ZAP sin alertas altas | Seguridad (confidencialidad y autenticidad) | Pruebas de acceso, verificación del despliegue y ZAP | **Cumple con límites**: análisis pasivo y sin sesión |
| RNF010 | Auditoría: un cambio en precios o pedidos deja registro | Seguridad (responsabilidad) | `auditlog` y pruebas | **Cumple** para precios, pedidos y compras; los módulos de la Fase 2 usan el historial del documento |
| RNF011 | Disponibilidad ≥ 99 % en horario laboral, con reinicio automático y *healthcheck* | Fiabilidad (disponibilidad) | *Healthchecks* de Docker | **Parcial**: sin medición continua |
| RNF012 | Reproducibilidad: el entorno se levanta con un comando y deja Odoo y PostgreSQL `healthy` | Flexibilidad (instalabilidad) | Despliegue en una PC limpia y CI | **Cumple** |
| RNF013 | Ley 29733: ningún dato real de personas ni RUC real en el repositorio | Seguridad (confidencialidad) | Revisión de datos y secret scanning | **Parcial**: datos ficticios, sin política de privacidad |

Las fichas completas incluyen además el método de verificación y los riesgos relacionados; el resumen por requisito está en 4.2.3 y en la matriz de trazabilidad (10.7).
