import math
import io
import pandas as pd 

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import serializers, status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, UpdateAPIView


from profiles.models import Profile
from .serializers import CandidatesListSerializer, CandidateDetailSerializer, AdminDetailSerializer, ScoreSerializer
from profiles.serializers import UserSerializer
from utils.responses import Responses
from .models import Score

from djoser.conf import settings
from djoser.views import UserViewSet
from djoser import utils
from djoser.serializers import TokenCreateSerializer
from utils.constants import CONSTANTS



User = get_user_model()

"""Update the score of a candidate's profile"""
class UpdateScore(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Score.objects.all()

    serializer_class = ScoreSerializer

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            profile_obj = Profile.objects.get(pk=request.data.get('profile_id'))
            if instance.id == profile_obj.score.id:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    response = serializer.save()
                    response = ScoreSerializer(response)
                    return Responses.make_response(data=response.data)
                    # return self.update(request, *args, **kwargs)
            raise Exception
        except:
            return Responses.make_response(error=True, message="Server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""Get the Profile detail of an Candidate user"""
class GetCandidateDetails(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = CandidateDetailSerializer
    lookup_field = 'user'
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CandidateDetailSerializer(obj)
        return Responses.make_response(data=serializer.data)
        

"""Get the User detail of an Admin user"""
class GetAdminDetails(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = AdminDetailSerializer
    queryset = User.objects.filter(is_staff=True)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = AdminDetailSerializer(obj)
        return Responses.make_response(data=serializer.data)


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


class AdministratorsView(ListAPIView):
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

        #-----------------------
        data = {
            'username':[],
            'email':[],
            'Name':[],
            'Location':[],
            'score':[],
        }
        for candidate in profile_list:
            data['username'].append(candidate.user.username)
            data['email'].append(candidate.user.email)
            data['Name'].append(candidate.user.first_name)
            data['Location'].append(candidate.Address)
            data['score'].append(candidate.score)

        # profile_list_df = pd.DataFrame(profile_list.values())
        profile_list_df = pd.DataFrame.from_dict(data)

        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        profile_list_df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        xlsx_data = output.getvalue()


        print(profile_list_df)
        profile_list_df.to_excel("output.xlsx")
        #-----------------------


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
                                        message=CONSTANTS.get('error_server'),
                                        status=status.HTTP_400_BAD_REQUEST)
