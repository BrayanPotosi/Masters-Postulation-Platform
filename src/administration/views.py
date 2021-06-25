import math
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import serializers, status, authentication, permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from profiles.models import Profile
from .serializers import CandidatesListSerializer
from profiles.serializers import UserSerializer
from utils.responses import Responses

User = get_user_model()

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
    try:
        if items_pp_query is not None:
            items_per_page = items_pp_query

        profile_list = Profile.objects.all()
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
                                        message="Server error: Value error, ippage is not a number",
                                        status=status.HTTP_400_BAD_REQUEST)
