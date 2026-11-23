# HU-29: etapa de los módulos propios. Vacía por defecto (en desarrollo el compose monta ./addons); la release la llena con
#   docker buildx build --build-context addons=./addons ...   para publicar una imagen que corre sin montar nada.
FROM scratch AS addons

# Imagen de Odoo 19.0 Community con la etiqueta fechada fija (06 §6.5):
# el CI y las dos PC usan exactamente la misma. Para actualizarla, cambiar la fecha aquí.
FROM odoo:19.0-20261112

# HU-27 (03 §3.2): módulo OCA `auditlog` (AGPL-3) de OCA/server-tools, fijado por commit de la rama 19.0
# (19.0.2.0.2, 23/11/2026). Solo se descarga esa carpeta. Para actualizarlo, cambiar el commit aquí.
ARG OCA_SERVER_TOOLS_SHA=13e504f892ce8ba77fc16ed148ec3c248869a484
USER root
RUN mkdir -p /opt/oca \
 && curl -fsSL "https://github.com/OCA/server-tools/archive/${OCA_SERVER_TOOLS_SHA}.tar.gz" \
    | tar -xz -C /opt/oca --strip-components=1 "server-tools-${OCA_SERVER_TOOLS_SHA}/auditlog" \
 && test -f /opt/oca/auditlog/__manifest__.py

# La configuración se genera al arrancar a partir de las variables de entorno (.env),
# porque odoo.conf no expande variables y /etc/odoo es de solo lectura para el usuario odoo.
COPY --chmod=0644 odoo.conf.template /etc/odoo/odoo.conf.template
COPY --chmod=0755 entrypoint.sh /usr/local/bin/donofrio-entrypoint.sh

# Módulos propios dentro de la imagen (solo cuando la release pasa --build-context addons=./addons)
COPY --from=addons / /mnt/extra-addons/

USER odoo
ENTRYPOINT ["/usr/local/bin/donofrio-entrypoint.sh"]
CMD ["odoo"]
