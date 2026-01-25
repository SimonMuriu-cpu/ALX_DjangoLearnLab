# LibraryProject/middleware.py
import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger('django.security.https')

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Custom middleware to add additional security headers.
    """
    
    def process_response(self, request, response):
        # Add custom security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add HSTS header if HTTPS is enforced
        if getattr(settings, 'SECURE_SSL_REDIRECT', False):
            hsts_seconds = getattr(settings, 'SECURE_HSTS_SECONDS', 31536000)
            hsts_include_subdomains = '; includeSubDomains' if getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False) else ''
            hsts_preload = '; preload' if getattr(settings, 'SECURE_HSTS_PRELOAD', False) else ''
            response['Strict-Transport-Security'] = f'max-age={hsts_seconds}{hsts_include_subdomains}{hsts_preload}'
        
        # Log security headers for debugging
        if settings.DEBUG:
            logger.debug(f'Security headers added for {request.path}')
        
        return response
    
    def process_request(self, request):
        # Log HTTPS requests
        if request.is_secure():
            logger.info(f'HTTPS request to {request.path}', 
                       extra={'ip': request.META.get('REMOTE_ADDR'), 
                              'user': request.user.username if request.user.is_authenticated else 'anonymous'})
        else:
            logger.warning(f'HTTP request to {request.path} (will be redirected to HTTPS)',
                          extra={'ip': request.META.get('REMOTE_ADDR'),
                                 'user': request.user.username if request.user.is_authenticated else 'anonymous'})
        return None


class HTTPSRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to enforce HTTPS redirects.
    This provides an additional layer of HTTPS enforcement.
    """
    
    def process_request(self, request):
        # Check if we should redirect to HTTPS
        secure_redirect = getattr(settings, 'SECURE_SSL_REDIRECT', False)
        
        if secure_redirect and not request.is_secure():
            # Don't redirect certain paths (like health checks)
            exempt_paths = ['/health/', '/robots.txt', '/favicon.ico']
            if not any(request.path.startswith(path) for path in exempt_paths):
                from django.http import HttpResponsePermanentRedirect
                # Build the HTTPS URL
                https_url = request.build_absolute_uri(request.get_full_path())
                https_url = https_url.replace('http://', 'https://', 1)
                
                logger.info(f'Redirecting HTTP to HTTPS: {request.path} -> {https_url}',
                           extra={'ip': request.META.get('REMOTE_ADDR'),
                                  'user': request.user.username if request.user.is_authenticated else 'anonymous'})
                
                return HttpResponsePermanentRedirect(https_url)
        
        return None