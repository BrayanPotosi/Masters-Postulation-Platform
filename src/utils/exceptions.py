from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import exception_handler
from utils.responses import Responses
from utils.constants import CONSTANTS

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError': _handle_generic_error_
    }
    
    exception_class = exc.__class__.__name__
    response = exception_handler(exc, context)

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response

def _handle_generic_error_(exc, context, response):
    return Responses.make_response(error=True, message=CONSTANTS.get('error_login') ,status=status.HTTP_400_BAD_REQUEST)
