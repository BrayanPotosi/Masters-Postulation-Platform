import math
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import serializers, status, authentication, permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, GenericAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from profiles.models import Profile
from .serializers import CandidatesListSerializer
from profiles.serializers import UserSerializer
from utils.responses import Responses

from djoser.conf import settings
from djoser.views import UserViewSet
from djoser import utils
from djoser.serializers import TokenCreateSerializer



User = get_user_model()

"""Signup and login override Djoser methods
"""
class SignUp(UserViewSet):
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Login userd just created
        # _ = request.data.pop('re_password')
        serializer_token = TokenCreateSerializer(data=request.data)
        serializer_token.is_valid(raise_exception=True)
        token = utils.login_user(self.request, serializer_token.user)
        token_serializer_class = settings.SERIALIZERS.token
        data = {
            "signup": serializer.data,
            "login": token_serializer_class(token).data
        }
        return Responses.make_response(
            data=data, status=status.HTTP_200_OK
        )


class administrators_view(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.filter(is_staff=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        total_administrators = queryset.count()
        data = {
                "count": total_administrators,
                "data": serializer.data
                }
        return Responses.make_response(data=data)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def candidates_view(request):
    ITEMS_PER_PAGE = 2
    items_per_page = ITEMS_PER_PAGE
    page_num = request.query_params.get('page')    
    items_pp_query = request.query_params.get('ippage')
    sort_option = request.query_params.get('sort')
    order = 'total_score'
    if sort_option == 'desc':
        order = '-total_score'

        
    try:
        if items_pp_query is not None:
            items_per_page = items_pp_query

        profile_list = Profile.objects.order_by(order)
        total_candidates = profile_list.count()
        paginator = Paginator(profile_list,items_per_page)
        try:
            profile_list = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            profile_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            profile_list = paginator.page(paginator.num_pages)
        data_serializer = CandidatesListSerializer(profile_list, many=True)
        total_pages = math.ceil(total_candidates/int(items_per_page))
        data = {
                "pages":total_pages,   
                "count": total_candidates,
                "data": data_serializer.data
                }
        return Responses.make_response(data=data)
    except ValueError:
        return Responses.make_response(error=True, 
                                        message="Server error",
                                        status=status.HTTP_400_BAD_REQUEST)
