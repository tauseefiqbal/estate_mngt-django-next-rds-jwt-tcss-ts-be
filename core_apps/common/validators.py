"""
Common validators and sanitization utilities
"""
import re
from typing import Any
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
import bleach


# Allowed HTML tags for sanitization (keep it minimal for security)
ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "u",
    "a",
    "ul",
    "ol",
    "li",
    "code",
    "pre",
    "blockquote",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "code": ["class"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def sanitize_html_content(content: str) -> str:
    """
    Sanitize HTML content to prevent XSS attacks.
    Removes potentially dangerous tags and attributes while preserving safe formatting.

    Args:
        content: Raw HTML content string

    Returns:
        Sanitized HTML content
    """
    if not content:
        return ""

    # Use bleach to clean HTML
    cleaned_content = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )

    # Additional sanitization: remove javascript: protocol
    cleaned_content = re.sub(
        r'javascript:', '', cleaned_content, flags=re.IGNORECASE
    )

    return cleaned_content


def sanitize_text_content(content: str) -> str:
    """
    Strip all HTML tags from content for plain text fields.

    Args:
        content: Raw content string

    Returns:
        Plain text content without HTML tags
    """
    if not content:
        return ""

    return strip_tags(content).strip()


def validate_no_html(value: str) -> None:
    """
    Validator to ensure no HTML tags are present in the value.

    Args:
        value: String to validate

    Raises:
        ValidationError: If HTML tags are detected
    """
    if value and "<" in value and ">" in value:
        # Check if it looks like HTML
        if re.search(r"<[^>]+>", value):
            raise ValidationError(
                "HTML tags are not allowed in this field. Please use plain text only."
            )


def validate_sql_injection(value: str) -> None:
    """
    Basic SQL injection pattern detection validator.
    Note: This is a defense-in-depth measure. Django ORM already prevents SQL injection.

    Args:
        value: String to validate

    Raises:
        ValidationError: If suspicious SQL patterns are detected
    """
    if not value:
        return

    # Common SQL injection patterns
    sql_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        r"(--|\;|\|\||&&)",
        r"(\bOR\b.*\=)",
        r"(\bAND\b.*\=)",
        r"(\'.*\bOR\b.*\')",
    ]

    for pattern in sql_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(
                "Invalid input detected. Please avoid using special SQL characters."
            )


def validate_safe_filename(filename: str) -> None:
    """
    Validate that filename doesn't contain path traversal attempts.

    Args:
        filename: Filename to validate

    Raises:
        ValidationError: If suspicious patterns are found
    """
    if not filename:
        return

    # Check for path traversal attempts
    dangerous_patterns = ["..", "/", "\\", "\x00"]

    for pattern in dangerous_patterns:
        if pattern in filename:
            raise ValidationError(
                f"Invalid filename. Characters like '{pattern}' are not allowed."
            )


def validate_url_safe_slug(value: str) -> None:
    """
    Validate that a slug is URL-safe.

    Args:
        value: Slug to validate

    Raises:
        ValidationError: If slug contains invalid characters
    """
    if not value:
        return

    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", value):
        raise ValidationError(
            "Slug must contain only lowercase letters, numbers, and hyphens, "
            "and cannot start or end with a hyphen."
        )


def clean_user_input(data: dict[str, Any], text_fields: list[str] = None) -> dict[str, Any]:
    """
    Clean user input data by sanitizing specified text fields.

    Args:
        data: Dictionary of input data
        text_fields: List of field names to sanitize (default: all string fields)

    Returns:
        Cleaned data dictionary
    """
    if not data:
        return data

    cleaned_data = data.copy()

    if text_fields is None:
        # Sanitize all string fields
        text_fields = [key for key, value in data.items() if isinstance(value, str)]

    for field in text_fields:
        if field in cleaned_data and isinstance(cleaned_data[field], str):
            cleaned_data[field] = sanitize_text_content(cleaned_data[field])

    return cleaned_data


def validate_content_length(value: str, min_length: int = None, max_length: int = None) -> None:
    """
    Validate content length with optional min/max constraints.

    Args:
        value: Content to validate
        min_length: Minimum required length
        max_length: Maximum allowed length

    Raises:
        ValidationError: If length constraints are violated
    """
    if not value:
        if min_length and min_length > 0:
            raise ValidationError(f"Content must be at least {min_length} characters long.")
        return

    content_length = len(value.strip())

    if min_length and content_length < min_length:
        raise ValidationError(
            f"Content is too short. Minimum length is {min_length} characters."
        )

    if max_length and content_length > max_length:
        raise ValidationError(
            f"Content is too long. Maximum length is {max_length} characters."
        )
