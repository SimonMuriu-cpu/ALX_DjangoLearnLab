# LibraryProject/context_processors.py
from django.conf import settings

def security_context(request):
    """
    Context processor to add security-related information to templates.
    """
    return {
        'is_https': request.is_secure(),
        'security_mode': getattr(settings, 'SECURITY_MODE', 'development'),
        'https_enforced': getattr(settings, 'HTTPS_ENFORCED', False),
        'hsts_enabled': getattr(settings, 'SECURE_HSTS_SECONDS', 0) > 0,
        'csp_enabled': 'csp.middleware.CSPMiddleware' in getattr(settings, 'MIDDLEWARE', []),
    }