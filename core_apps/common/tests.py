"""
Tests for Common app (validators and exception handlers)
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from core_apps.common.validators import (
    sanitize_html_content,
    sanitize_text_content,
    validate_no_html,
    validate_sql_injection,
    validate_safe_filename,
    validate_content_length,
)
from core_apps.common.exceptions import (
    custom_exception_handler,
    ServiceUnavailableError,
    RateLimitExceededError,
    BusinessLogicError,
)


class ValidatorTest(TestCase):
    """Test suite for custom validators"""

    def test_sanitize_html_content_removes_scripts(self):
        """Test that sanitize_html_content removes script tags"""
        dirty_html = "Hello <script>alert('xss')</script> world"
        clean_html = sanitize_html_content(dirty_html)
        self.assertNotIn("<script>", clean_html)
        self.assertNotIn("alert", clean_html)

    def test_sanitize_html_content_allows_safe_tags(self):
        """Test that safe HTML tags are preserved"""
        html = "Hello <strong>world</strong> <em>test</em>"
        clean_html = sanitize_html_content(html)
        self.assertIn("<strong>", clean_html)
        self.assertIn("<em>", clean_html)

    def test_sanitize_text_content_strips_all_html(self):
        """Test that sanitize_text_content removes all HTML"""
        html = "Hello <strong>world</strong> <script>alert('xss')</script>"
        clean_text = sanitize_text_content(html)
        self.assertEqual(clean_text, "Hello world")

    def test_validate_no_html_passes_plain_text(self):
        """Test that validate_no_html allows plain text"""
        try:
            validate_no_html("This is plain text without HTML")
        except ValidationError:
            self.fail("validate_no_html raised ValidationError unexpectedly")

    def test_validate_no_html_fails_with_html(self):
        """Test that validate_no_html rejects HTML"""
        with self.assertRaises(ValidationError):
            validate_no_html("This has <strong>HTML</strong>")

    def test_validate_sql_injection_detects_patterns(self):
        """Test SQL injection pattern detection"""
        with self.assertRaises(ValidationError):
            validate_sql_injection("'; DROP TABLE users; --")

        with self.assertRaises(ValidationError):
            validate_sql_injection("1' OR '1'='1")

    def test_validate_sql_injection_allows_safe_input(self):
        """Test that safe input passes SQL injection validation"""
        try:
            validate_sql_injection("This is a normal string")
        except ValidationError:
            self.fail("validate_sql_injection raised ValidationError unexpectedly")

    def test_validate_safe_filename_rejects_path_traversal(self):
        """Test that path traversal attempts are blocked"""
        with self.assertRaises(ValidationError):
            validate_safe_filename("../../../etc/passwd")

        with self.assertRaises(ValidationError):
            validate_safe_filename("file\\with\\backslash")

    def test_validate_safe_filename_allows_safe_names(self):
        """Test that safe filenames pass validation"""
        try:
            validate_safe_filename("myfile.txt")
            validate_safe_filename("document_2024.pdf")
        except ValidationError:
            self.fail("validate_safe_filename raised ValidationError unexpectedly")

    def test_validate_content_length_min_constraint(self):
        """Test minimum content length validation"""
        with self.assertRaises(ValidationError):
            validate_content_length("Hi", min_length=5)

    def test_validate_content_length_max_constraint(self):
        """Test maximum content length validation"""
        with self.assertRaises(ValidationError):
            validate_content_length("This is a very long string", max_length=10)

    def test_validate_content_length_within_bounds(self):
        """Test that content within bounds passes validation"""
        try:
            validate_content_length("Valid content", min_length=5, max_length=50)
        except ValidationError:
            self.fail("validate_content_length raised ValidationError unexpectedly")


class ExceptionHandlerTest(TestCase):
    """Test suite for custom exception handler"""

    def setUp(self):
        """Set up test request factory"""
        self.factory = APIRequestFactory()

    def test_custom_exception_handler_authentication_error(self):
        """Test handling of authentication errors"""
        request = self.factory.get("/test/")
        exc = NotAuthenticated()
        context = {"request": request}

        response = custom_exception_handler(exc, context)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "Authentication required")

    def test_custom_exception_handler_permission_denied(self):
        """Test handling of permission denied errors"""
        request = self.factory.get("/test/")
        exc = PermissionDenied()
        context = {"request": request}

        response = custom_exception_handler(exc, context)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["status"], "error")

    def test_service_unavailable_error(self):
        """Test custom ServiceUnavailableError"""
        exc = ServiceUnavailableError()
        self.assertEqual(exc.status_code, 503)
        self.assertIn("unavailable", exc.default_detail.lower())

    def test_rate_limit_exceeded_error(self):
        """Test custom RateLimitExceededError"""
        exc = RateLimitExceededError()
        self.assertEqual(exc.status_code, 429)
        self.assertIn("rate limit", exc.default_detail.lower())

    def test_business_logic_error(self):
        """Test custom BusinessLogicError"""
        exc = BusinessLogicError()
        self.assertEqual(exc.status_code, 400)
        self.assertIn("business logic", exc.default_detail.lower())


class SanitizationIntegrationTest(TestCase):
    """Integration tests for sanitization in real scenarios"""

    def test_xss_prevention_in_content(self):
        """Test XSS prevention across different scenarios"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
        ]

        for payload in xss_payloads:
            clean = sanitize_html_content(payload)
            # Ensure no dangerous content remains
            self.assertNotIn("javascript:", clean.lower())
            self.assertNotIn("onerror", clean.lower())
            self.assertNotIn("onload", clean.lower())
            self.assertNotIn("<script", clean.lower())
