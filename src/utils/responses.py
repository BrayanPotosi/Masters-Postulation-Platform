from rest_framework.response import Response
from rest_framework import status

class Responses():

    def make_response(data=None, status=status.HTTP_200_OK, message=None, error=False, authorization=False):
        response = {
            "error": error,
            "message": message,
            "data": data,
            "admin_auth": authorization
        }

        return Response(response, status=status)
