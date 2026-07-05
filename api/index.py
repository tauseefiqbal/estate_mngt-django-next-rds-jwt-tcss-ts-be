"""
Vercel serverless handler for Django
This wraps the WSGI application for Vercel's serverless environment
"""
import os
import sys
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Add the project directory to Python path
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module (Vercel will provide this via environment variable)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Ensure environment variables are available
# Vercel sets these directly, no need for .env files

try:
    # Initialize Django
    import django
    django.setup()
    
    # Get WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # Vercel serverless handler
    app = application
    
except Exception as e:
    # Create a simple error response for debugging
    def app(environ, start_response):
        import traceback
        status = '500 Internal Server Error'
        error_msg = f"Django startup failed: {str(e)}\n\n{traceback.format_exc()}"
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [error_msg.encode('utf-8')]

