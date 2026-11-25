# 10.1 Fichas de requerimientos funcionales

Los 18 requerimientos funcionales están implementados: 14 con la Fase 1 y los de la Fase 2 con los módulos M1 (RF011 y RF012), M2 (RF004), M3 (RF008) y M4 (parte propia de RF013). Todos tienen prioridad Must. La ficha de cada uno (historia de usuario, pruebas y estado) está en la matriz de trazabilidad (10.7) y los casos de uso, en 4.2.4.

**Reglas de negocio y límites destacados.** RF004: el pedido usa solo lo vendido y la comisión del 10 % es un supuesto editable. RF008: las lecturas se registran a mano y no hay sensores. RF011 y RF012: los puntos de control son supuestos del caso y un lote sin inspección no se bloquea. RF013: el tablero tiene Lighthouse 76 en escritorio (límite conocido). RF016: se emiten comprobantes con IGV 18 % pero no se envían a SUNAT, porque `l10n_pe_edi` es Enterprise. Las 218 pruebas del repositorio corren en el CI de cada PR sin errores.
