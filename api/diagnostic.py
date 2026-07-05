"""
Simple diagnostic endpoint for Vercel debugging
Tests basic functionality without database
"""
import os
import sys
from pathlib import Path

def app(environ, start_response):
    """Simple WSGI app to test Vercel configuration"""
    
    # Collect diagnostic information
    diagnostics = []
    
    # Check Python version
    diagnostics.append(f"Python Version: {sys.version}")
    
    # Check environment variables
    required_vars = [
        'DJANGO_SETTINGS_MODULE',
        'DJANGO_SECRET_KEY',
        'POSTGRES_HOST',
        'POSTGRES_DB',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
    ]
    
    diagnostics.append("\n--- Environment Variables Check ---")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var or 'SECRET' in var or 'KEY' in var:
                masked = value[:3] + '*' * (len(value) - 6) + value[-3:] if len(value) > 6 else '***'
                diagnostics.append(f"✓ {var}: {masked}")
            else:
                diagnostics.append(f"✓ {var}: {value}")
        else:
            diagnostics.append(f"✗ {var}: MISSING")
    
    # Check Python path
    diagnostics.append(f"\n--- Python Path ---")
    diagnostics.append(f"sys.path: {sys.path}")
    
    # Check if Django can be imported
    diagnostics.append(f"\n--- Django Import Test ---")
    try:
        import django
        diagnostics.append(f"✓ Django version: {django.VERSION}")
    except Exception as e:
        diagnostics.append(f"✗ Django import failed: {str(e)}")
    
    # Try to setup Django
    diagnostics.append(f"\n--- Django Setup Test ---")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
        import django
        django.setup()
        diagnostics.append(f"✓ Django setup successful")
        
        # Try database connection
        diagnostics.append(f"\n--- Database Connection Test ---")
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            diagnostics.append(f"✓ Database connection successful")
        except Exception as e:
            diagnostics.append(f"✗ Database connection failed: {str(e)}")
            
    except Exception as e:
        diagnostics.append(f"✗ Django setup failed: {str(e)}")
        import traceback
        diagnostics.append(f"\nFull traceback:\n{traceback.format_exc()}")
    
    # Build response
    response = "\n".join(diagnostics)
    
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain; charset=utf-8'),
        ('Content-Length', str(len(response.encode('utf-8'))))
    ]
    
    start_response(status, response_headers)
    return [response.encode('utf-8')]
