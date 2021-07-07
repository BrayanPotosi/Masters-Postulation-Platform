from rest_framework import status
from rest_framework.views import exception_handler
from utils.responses import Responses
from utils.constants import CONSTANTS

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError': _handle_generic_error_,
        'PermissionDenied': _handle_unathorized_error_,
        'AuthenticationFailed': _handle_auth_fail_error_,
    }
    
    exception_class = exc.__class__.__name__
    response = exception_handler(exc, context)
    print('class',exception_class)

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response

def _handle_generic_error_(exc, context, response):
    return Responses.make_response(error=True, message=CONSTANTS.get('error_login') ,
                                    status=status.HTTP_400_BAD_REQUEST)

def _handle_unathorized_error_(exc, context, response):
    return Responses.make_response(error=True, message=CONSTANTS.get('error_unauthorized'), 
                                    status=status.HTTP_403_FORBIDDEN)

def _handle_auth_fail_error_(exc, context, response):
    return Responses.make_response(error=True, message=CONSTANTS.get('error_auth_token'), 
                                    status=status.HTTP_401_UNAUTHORIZED)