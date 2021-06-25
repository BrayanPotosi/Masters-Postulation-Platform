from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from profiles.models import Profile
from .serializers import CandidatesListSerializer

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def candidates_view(request):
    ITEMS_PER_PAGE = 2
    items_per_page = ITEMS_PER_PAGE
    page_num = request.query_params.get('page')
    
    items_pp_query = request.query_params.get('ippage')
    if items_pp_query is not None:
        items_per_page = items_pp_query
    

    profile_list = Profile.objects.all()
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

    return Response(data_serializer.data)
