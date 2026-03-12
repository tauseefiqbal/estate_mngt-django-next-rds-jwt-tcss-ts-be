"""
Global exception handler for Django REST Framework
"""
import logging
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework that provides
    consistent error responses across the API.
    """
    # Call DRF's default exception handler first
    response = drf_exception_handler(exc, context)

    # Log the exception
    logger.error(
        f"API Exception: {exc.__class__.__name__} - {str(exc)}",
        exc_info=True,
        extra={"context": context},
    )

    # Handle Django's core exceptions that DRF doesn't handle by default
    if response is None:
        if isinstance(exc, DjangoValidationError):
            response = Response(
                {
                    "status": "error",
                    "message": "Validation error occurred",
                    "errors": exc.message_dict
                    if hasattr(exc, "message_dict")
                    else {"detail": exc.messages if hasattr(exc, "messages") else str(exc)},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif isinstance(exc, DjangoPermissionDenied):
            response = Response(
                {
                    "status": "error",
                    "message": "Permission denied",
                    "errors": {"detail": str(exc)},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        elif isinstance(exc, Http404):
            response = Response(
                {
                    "status": "error",
                    "message": "Resource not found",
                    "errors": {"detail": str(exc) or "The requested resource was not found"},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Handle unexpected exceptions
        else:
            logger.critical(
                f"Unhandled exception: {exc.__class__.__name__}",
                exc_info=True,
                extra={"context": context},
            )
            response = Response(
                {
                    "status": "error",
                    "message": "An unexpected error occurred",
                    "errors": {"detail": "Internal server error. Please try again later."},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # Customize the response format if DRF handled it
    if response is not None:
        # Standardize error response format
        custom_response_data = {
            "status": "error",
            "message": get_error_message(exc),
            "errors": response.data if isinstance(response.data, dict) else {"detail": response.data},
        }

        # Add custom fields based on exception type
        if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            custom_response_data["message"] = "Authentication required"
        elif isinstance(exc, PermissionDenied):
            custom_response_data["message"] = "You do not have permission to perform this action"
        elif isinstance(exc, ValidationError):
            custom_response_data["message"] = "Invalid input data"

        response.data = custom_response_data

    return response


def get_error_message(exc):
    """
    Extract a user-friendly error message from the exception.
    """
    if hasattr(exc, "default_detail"):
        return str(exc.default_detail)
    elif hasattr(exc, "detail"):
        if isinstance(exc.detail, dict):
            # Get the first error message
            for key, value in exc.detail.items():
                if isinstance(value, list) and len(value) > 0:
                    return str(value[0])
                return str(value)
        return str(exc.detail)
    return str(exc)


class ServiceUnavailableError(APIException):
    """
    Custom exception for service unavailability.
    """

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service temporarily unavailable, please try again later."
    default_code = "service_unavailable"


class RateLimitExceededError(APIException):
    """
    Custom exception for rate limit exceeded.
    """

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = "Rate limit exceeded. Please try again later."
    default_code = "rate_limit_exceeded"


class BusinessLogicError(APIException):
    """
    Custom exception for business logic violations.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Business logic error occurred."
    default_code = "business_logic_error"
