#!/bin/bash
# scripts/configure_environment.sh
# Configure environment variables for HTTPS deployment

echo "Configuring environment for HTTPS..."

# Set Django settings for production
export DJANGO_SECRET_KEY="your-secure-secret-key-here"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,yourdomain.com"

# HTTPS settings
export DJANGO_SECURE_SSL_REDIRECT="True"
export DJANGO_SECURE_HSTS_SECONDS="31536000"
export DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS="True"
export DJANGO_SECURE_HSTS_PRELOAD="True"

# Secure cookies
export DJANGO_SESSION_COOKIE_SECURE="True"
export DJANGO_CSRF_COOKIE_SECURE="True"

echo "Environment configured for HTTPS deployment"
echo "To apply these settings, run: source scripts/configure_environment.sh"