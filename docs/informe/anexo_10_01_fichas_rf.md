# 10.1 Fichas de requerimientos funcionales

Los 18 requerimientos funcionales están implementados: 14 con la Fase 1 y los de la Fase 2 con los módulos M1 (RF011 y RF012), M2 (RF004), M3 (RF008) y M4 (parte propia de RF013). Todos tienen prioridad Must. La ficha de cada uno (historia de usuario, pruebas y estado) está en la matriz de trazabilidad (10.8) y los casos de uso, en 2.2.1.3.

Reglas de negocio destacadas. RF004: el pedido usa solo lo vendido y la comisión del 10 % es un supuesto editable. RF008: las lecturas de temperatura se registran por cámara con su rango. RF011 y RF012: los puntos de control son supuestos del caso. RF016: se emiten facturas y boletas con IGV 18 % con la localización peruana de Odoo. Las 224 pruebas del repositorio corren en el CI de cada PR sin errores.
