#!/usr/bin/env bash
# HU-27: genera el certificado TLS AUTOFIRMADO de la demo en docker/nginx/certs/ (ignorado por git).
# Es idempotente: si ya existe, no lo toca (usa --renovar para crear otro). En una VM real se reemplaza
# por Let's Encrypt (06 §6.5). El navegador mostrará la advertencia normal de un certificado autofirmado.
# Uso: scripts/generar_certificado.sh [--renovar]
set -euo pipefail
cd "$(dirname "$0")/.."
dir=docker/nginx/certs
mkdir -p "$dir"
if [ -s "$dir/donofrio.crt" ] && [ -s "$dir/donofrio.key" ] && [ "${1:-}" != "--renovar" ]; then
  echo "El certificado ya existe en $dir/ (usa --renovar para crear otro)."
  exit 0
fi
openssl req -x509 -newkey rsa:2048 -nodes -sha256 -days 365 \
  -keyout "$dir/donofrio.key" -out "$dir/donofrio.crt" \
  -subj "/C=PE/O=Donofrio ERP (proyecto academico)/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1" 2>/dev/null
chmod 600 "$dir/donofrio.key"; chmod 644 "$dir/donofrio.crt"
echo "Certificado autofirmado creado en $dir/ (365 días, CN=localhost)."
