# Security Implementation Documentation

## Overview
This Django application implements comprehensive security measures to protect against common web vulnerabilities.

## Security Features Implemented

### 1. Secure Settings Configuration
- **DEBUG Mode**: Controlled by environment variable `DJANGO_DEBUG`
- **HTTPS Enforcement**: 
  - `SECURE_SSL_REDIRECT = True` in production
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
- **Security Headers**:
  - `SECURE_BROWSER_XSS_FILTER = True`
  - `X_FRAME_OPTIONS = 'DENY'` (prevents clickjacking)
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`
- **HSTS**: Enabled with 1-year duration

### 2. CSRF Protection
- All forms include `{% csrf_token %}`
- CSRF middleware enabled in settings
- CSRF cookies are secure and HttpOnly
- Additional `@csrf_protect` decorator on sensitive views

### 3. SQL Injection Prevention
- **Django ORM**: Used exclusively for database queries
- **Parameterized Queries**: All queries use Django's ORM which automatically parameterizes inputs
- **Input Validation**: Custom sanitization functions for search inputs
- **Safe Filtering**: Using Q objects and validated parameters

### 4. XSS Prevention
- **Template Auto-escaping**: Enabled by default in Django templates
- **Manual Escaping**: `|escape` filter used where needed
- **Content Security Policy (CSP)**: 
  - Implemented using `django-csp`
  - Restricts script sources to self and trusted CDNs
  - Uses nonce for inline scripts
- **HTML Sanitization**: `strip_tags()` for user-generated content

### 5. Content Security Policy (CSP)
```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "https://*")
CSP_FRAME_ANCESTORS = ("'none'",)  # No framing allowed