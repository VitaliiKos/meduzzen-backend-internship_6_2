from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_error_handler(exc: Exception, context: dict) -> Response:
    """Handle custom error handling for REST framework views.

    This function serves as a custom error handler for REST framework views. It allows you to
    define specific error handling behavior for different types of exceptions.

    :param exc: The exception that was raised.
    :type exc: Exception
    :param context: The context information for the exception.
    :type context: dict
    :return: A custom Response object for handling the exception.
    :rtype: Response
    """
    handlers = {
        'ValidationError': _handler_generic_error,
        'Http404': _handler_generic_error,
        'PermissionDenied': _handler_generic_error,
    }

    response = exception_handler(exc, context)

    exc_class = exc.__class__.__name__

    if exc_class in handlers:
        return handlers[exc_class](exc, context, response)
    return response


def _handler_authentication_error(exc, context, response):
    response.data = {
        'error': 'Please login to proceed',
        'status_code': response.status_code

    }
    return response


def _handler_generic_error(exc, context, response):
    return response
