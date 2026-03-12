"""
Custom test runner for Python 3.14 compatibility.

This prevents Django from capturing template contexts during tests,
which causes AttributeError in Python 3.14 due to changes in super().
"""
from django.test.runner import DiscoverRunner
from django.test import signals
from django import test
from unittest import mock


class Python314CompatibleTestRunner(DiscoverRunner):
    """
    Custom test runner that disables template context capturing.
    
    This prevents the AttributeError: 'super' object has no attribute 'dicts'
    that occurs in Python 3.14 when Django tries to copy template contexts.
    """
    
    def setup_test_environment(self, **kwargs):
        """Set up test environment without template instrumentation."""
        super().setup_test_environment(**kwargs)
        
        # Monkey-patch the store_rendered_templates function to do nothing
        # This prevents Django from trying to copy template contexts
        def noop_store_rendered_templates(**kwargs):
            """No-op function to replace store_rendered_templates."""
            pass
        
        # Replace the problematic signal handler
        signals.template_rendered.disconnect(dispatch_uid="template_rendered")
        test.signals.template_rendered.disconnect(dispatch_uid="template_rendered")
        
        # Patch the store_rendered_templates in the client module
        from django.test import client
        client.store_rendered_templates = noop_store_rendered_templates

