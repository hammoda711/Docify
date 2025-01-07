from rest_framework.response import Response

def api_response(code, message, data=None, status_code=200):
    """
    Generate a standardized API response with an HTTP status code.
    :param code: 0 for success, 1 for errors
    :param message: Informative message about the response
    :param data: Any additional data (optional)
    :param status_code: HTTP status code (default is 200)
    :return: Standardized response with status code
    """
    return Response({"code": code, "message": message, "data": data}, status=status_code)
