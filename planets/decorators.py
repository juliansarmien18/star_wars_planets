from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def api_response_handler(func):
    """
    Decorador para manejar responses de la API con formato estándar:
    {
        "error": bool,
        "data": str | dict | list
    }
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            result = func(self, request, *args, **kwargs)
            if isinstance(result, Response):
                return result
            if isinstance(result, dict):
                return Response(
                    {"error": False, "data": result}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": False, "data": str(result)}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": True, "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
