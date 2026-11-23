# Imagen de Odoo 19.0 Community con la etiqueta fechada fija (06 §6.5):
# el CI y las dos PC usan exactamente la misma. Para actualizarla, cambiar la fecha aquí.
FROM odoo:19.0-20261112

# La configuración se genera al arrancar a partir de las variables de entorno (.env),
# porque odoo.conf no expande variables y /etc/odoo es de solo lectura para el usuario odoo.
COPY --chmod=0644 odoo.conf.template /etc/odoo/odoo.conf.template
COPY --chmod=0755 entrypoint.sh /usr/local/bin/donofrio-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/donofrio-entrypoint.sh"]
CMD ["odoo"]
