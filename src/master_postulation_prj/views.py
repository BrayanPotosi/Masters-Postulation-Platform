# Django
from django.contrib.auth import authenticate, get_user_model

# Rest Framework
from rest_framework import status, serializers

# Djoser
from djoser.views import UserViewSet, TokenCreateView
from djoser.serializers import TokenCreateSerializer
from djoser.conf import settings
from djoser import utils

# Utils
from utils.responses import Responses
from utils.constants import CONSTANTS

User = get_user_model()


class OverrideTokenCreateSerializer(TokenCreateSerializer):
    """Rewrite TokenCreateSerializer in order to manage error responses"""

    password = serializers.CharField(required=False, style={"input_type": "password"})

    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "inactive_account": settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[settings.LOGIN_FIELD] = serializers.CharField(required=False)

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")


class Login(TokenCreateView):
    """Login override HTTP response"""
    serializer_class = OverrideTokenCreateSerializer

    def _action(self, serializer):
        try:
            token = utils.login_user(self.request, serializer.user)
            token_serializer_class = settings.SERIALIZERS.token
            return Responses.make_response(
                data=token_serializer_class(token).data)
        except Exception as e:
            print(e)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_login'),
                                           status=status.HTTP_400_BAD_REQUEST)


class SignUp(UserViewSet):
    """Signup and login override Djoser methods"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Login userd just created
        serializer_token = TokenCreateSerializer(data=request.data)
        serializer_token.is_valid(raise_exception=True)
        token = utils.login_user(self.request, serializer_token.user)
        token_serializer_class = settings.SERIALIZERS.token
        data = {
            "signup": serializer.data,
            "login": token_serializer_class(token).data
        }
        return Responses.make_response(data=data)
