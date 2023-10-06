from django.http import JsonResponse


def error_404(request, exception):
    """Handle 404 error and return a JSON response with a custom error message.

    This function handles 404 errors and returns a JSON response with a custom error message.

    :param request: The HTTP request.
    :type request: HttpRequest
    :param exception: The exception that triggered the 404 error.
    :type exception: Exception
    :return: JSON response with a custom error message and status code 404.
    :rtype: JsonResponse
    """
    message = 'The endpoint is not found'
    response = JsonResponse(data={'message': message, 'status_code': 404})
    response.status_code = 404
    return response


def error_500(request):
    """Handle 500 error and return a JSON response with a custom error message.

    This function handles 500 errors and returns a JSON response with a custom error message.

    :param request: The HTTP request.
    :type request: HttpRequest
    :return: JSON response with a custom error message and status code 500.
    :rtype: JsonResponse
    """
    message = 'An error occurred, its on us'
    response = JsonResponse(data={'message': message, 'status_code': 500})
    response.status_code = 500
    return response
