#!/bin/bash
# scripts/generate_ssl_cert.sh
# Generate self-signed SSL certificate for testing

echo "Generating SSL certificate..."

# Create SSL directory
mkdir -p deployment/ssl

# Generate private key
openssl genrsa -out deployment/ssl/library.key 2048

# Generate certificate signing request
openssl req -new -key deployment/ssl/library.key -out deployment/ssl/library.csr \
  -subj "/C=US/ST=State/L=City/O=Library/CN=localhost"

# Generate self-signed certificate
openssl x509 -req -days 365 -in deployment/ssl/library.csr \
  -signkey deployment/ssl/library.key -out deployment/ssl/library.crt

echo "SSL certificate generated in deployment/ssl/"
echo "Files: library.key (private key), library.crt (certificate)"