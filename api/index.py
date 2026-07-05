"""
Vercel serverless handler for Django
Django initialization is deferred until first request
"""
import os
import sys
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Lazy initialization - don't initialize Django until first request
_application = None

def get_application():
    """Initialize Django on first request, not at import time"""
    global _application
    if _application is None:
        import django
        django.setup()
        from django.core.wsgi import get_wsgi_application
        _application = get_wsgi_application()
    return _application

# Vercel handler - wraps lazy initialization
def app(environ, start_response):
    """WSGI application wrapper that initializes Django on first call"""
    application = get_application()
    return application(environ, start_response)

