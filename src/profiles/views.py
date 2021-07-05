# Rest Framework
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import serializers, status, authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Copy
from copy import error

# Custom classes
from utils.responses import Responses
from utils.constants import CONSTANTS

# Serializers
from .serializers import (
    AddressSerializer, CambridgeLevelSerializer, ExperienceSerializer,
    FisrtPageProfileSerializer, SecondPageProfileSerializer,
    EducationSerializer, LanguagesSerializer,
    CitiesSerializer, CountriesSerializer,
    GottenGradeSerializer, LastGradeSerializer,
    CivilStatusSerializer, CambridgeLevel,
    ProfileSerializer, UserSerializer,
    JobStatusSerializer, CitiesFkSerializer,
    GenderSerializer
)
# Models
from .models import (
    Address, Cities, CivilStatus,
    Countries, Education,
    GottenGrade, LastGrade,
    Profile, ProfessionalExperience,
    Languages, JobStatus, Gender,
)


class ModelObject:
    """Get a specific object from a model"""

    @staticmethod
    def get_object(request, pk, model):
        try:
            profile = Profile.objects.get(user=request.user.id)
            education_obj = model.objects.get(pk=pk)
            print(profile)
            print(education_obj)
            if education_obj.profile == profile:
                return education_obj
            raise Http404
        except:
            raise Http404


class EducationProfile(APIView):
    """Endpoint to perform CRUD operations on the Education model"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            profile = Profile.objects.get(user=request.user.id)
            education_serializer = EducationSerializer(Education.objects.filter(profile=profile.id), many=True)
        except:
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Responses.make_response(data=education_serializer.data)

    @staticmethod
    def post(request):
        education_serializer = EducationSerializer(data=request.data)
        if education_serializer.is_valid():
            response = education_serializer.create(request)
            if response:
                education_response = EducationSerializer(response)
                return Responses.make_response(data=education_response.data, status=status.HTTP_201_CREATED)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Responses.make_response(error=True, message=education_serializer.errors,
                                       status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        education_item = ModelObject.get_object(request, request.data.get('education_id'), Education)
        education_serializer = EducationSerializer(education_item, data=request.data)
        if education_serializer.is_valid():
            education_response = education_serializer.update(education_item, request.data)
            if education_response:
                response = EducationSerializer(education_response)
                return Responses.make_response(data=response.data)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Responses.make_response(error=True, message=education_serializer.errors,
                                       status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        education_item = ModelObject.get_object(request, request.data.get('education_id'), Education)
        education_item.delete()
        return Responses.make_response(data={"delete": "done"}, status=status.HTTP_204_NO_CONTENT)


class LanguageProfile(APIView):
    """Endpoint to perform CRUD operations on the Language model"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            profile = Profile.objects.filter(user=request.user.id)
            language_serializer = LanguagesSerializer(Languages.objects.filter(profile=profile[0].id), many=True)
        except:
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)

        return Responses.make_response(data=language_serializer.data)

    @staticmethod
    def post(request):
        language_serializer = LanguagesSerializer(data=request.data)
        if language_serializer.is_valid():
            response = language_serializer.create(request)
            if response:
                language_response = LanguagesSerializer(response)
                return Responses.make_response(data=language_response.data, status=status.HTTP_201_CREATED)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)
        return Responses.make_response(error=True, message=language_serializer.errors,
                                       status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        language_item = ModelObject.get_object(request, request.data.get('language_id'), Languages)
        language_serializer = LanguagesSerializer(language_item, data=request.data)
        if language_serializer.is_valid():
            language_response = language_serializer.update(language_item, request.data)
            if language_response:
                response = LanguagesSerializer(language_response)
                return Responses.make_response(data=response.data)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)
        return Responses.make_response(error=True, message=language_serializer.errors,
                                       status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        try:
            language_item = ModelObject.get_object(request, request.data.get('language_id'), Languages)
            language_item.delete()
            return Responses.make_response(data={"delete": "done"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Responses.make_response(error=True, message="Not Found", status=status.HTTP_404_NOT_FOUND)


class ExperienceProfile(APIView):
    """Endpoint to perform CRUD operations on the Experience model"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            profile = Profile.objects.filter(user=request.user.id)
            experience_serializer = ExperienceSerializer(ProfessionalExperience.objects.filter(profile=profile[0].id),
                                                         many=True)
        except:
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)

        return Responses.make_response(data=experience_serializer.data)

    @staticmethod
    def post(request):
        experience_serializer = ExperienceSerializer(data=request.data)
        if experience_serializer.is_valid():
            response = experience_serializer.create(request)
            if response:
                experience_response = ExperienceSerializer(response)
                return Responses.make_response(data=experience_response.data, status=status.HTTP_201_CREATED)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)
        return Responses.make_response(error=True, message=experience_serializer.errors,
                                       status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        experience_item = ModelObject.get_object(request, request.data.get('experience_id'), ProfessionalExperience)
        experience_serializer = ExperienceSerializer(experience_item, data=request.data)
        if experience_serializer.is_valid():
            experience_response = experience_serializer.update(experience_item, request.data)
            if experience_response:
                response = ExperienceSerializer(experience_response)
                return Responses.make_response(data=response.data)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)
        return Responses.make_response(error=True, message=experience_serializer.errors,
                                       status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        try:
            experience_item = ModelObject.get_object(request, request.data.get('experience_id'), ProfessionalExperience)
            experience_item.delete()
            return Responses.make_response(data={"delete": "done"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Responses.make_response(error=True, message="Not Found", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def job_status(request):
    if request.method == "GET":
        try:
            profile = Profile.objects.get(user=request.user.id)
            job_status = profile.job_status
            if job_status is None:
                job_status = JobStatus.objects.create()
                profile.job_status = job_status
                profile.save()
            job_status_serializer = JobStatusSerializer(job_status)
            experience_list = ExperienceSerializer(ProfessionalExperience.objects.filter(profile=profile.id), many=True)
            data = {
                "job_status": job_status_serializer.data,
                "professional_experience": experience_list.data
            }
            return Responses.make_response(data=data)
        except:
            return Responses.make_response(data={}, error=True,
                                           message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == "PUT":
        profile = Profile.objects.get(user=request.user.id)
        user = request.user
        data = request.data

        job_status_serializer = JobStatusSerializer(profile.job_status, data=data)
        if job_status_serializer.is_valid():
            response = job_status_serializer.save()
            response = JobStatusSerializer(response)
            return Responses.make_response(data=response.data)
        else:
            return Responses.make_response(error=True, message=job_status_serializer.errors,
                                           status=status.HTTP_400_BAD_REQUEST)
    else:
        return Responses.make_response(error=True, message="method not allowed",
                                       status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile_form(request):
    if request.method == 'GET':

        countries_serializer = CountriesSerializer(Countries.objects.all(), many=True)
        civil_status_serializer = CivilStatusSerializer(CivilStatus.objects.all(), many=True)
        gender_serializer = GenderSerializer(Gender.objects.all(), many=True)
        options = {
            "countries": countries_serializer.data,
            "civil_status": civil_status_serializer.data,
            "gender": gender_serializer.data,
        }
        profile = Profile.objects.filter(user=request.user.id)
        serializer = FisrtPageProfileSerializer(profile, many=True)
        data = {
            "profile": serializer.data,
            "options": options,
        }
        return Responses.make_response(data=data)

    elif request.method == 'PUT':

        profile = Profile.objects.get(user=request.user.id)
        user = request.user
        data = request.data

        user_data = {
            "email": user.email,
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "username": data.get("username")
        }
        try:
            profile_data = {
                "user": user,
                "birthday": data.get("birthday"),
                "civil_status": CivilStatus.objects.get(pk=data.get("c_status")),
                "home_phone": data.get("home_phone"),
                "mobile_phone": data.get("mobile_phone"),
                "gender": Gender.objects.get(pk=data.get("gender")),
            }
            address_data = {
                "country": Countries.objects.get(pk=data.get("country")),
                "city": Cities.objects.get(pk=data.get("city")),
                "address_line1": data.get("address_line1")
            }
        except ObjectDoesNotExist:
            return Responses.make_response(data={}, error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)

        address_item = profile.Address
        if address_item is None:
            address_item = Address.objects.create()
            profile_data['Address'] = address_item
        address_serializer = AddressSerializer(address_item, data=address_data)
        if address_serializer.is_valid():
            address_serializer.update(address_item, address_data)
        else:
            return Responses.make_response(error=True, message=address_serializer.errors,
                                           status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Responses.make_response(error=True, message=user_serializer.errors,
                                           status=status.HTTP_400_BAD_REQUEST)

        profile_serializer = ProfileSerializer(profile, data=profile_data)
        if profile_serializer.is_valid():
            profile_response = profile_serializer.update(profile, profile_data)
            if profile_response:
                response = FisrtPageProfileSerializer(profile_response)
                return Responses.make_response(data=response.data)
            return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                           status=status.HTTP_400_BAD_REQUEST)
        return Responses.make_response(error=True, message=profile_serializer.errors,
                                       status=status.HTTP_400_BAD_REQUEST)
    else:
        return Responses.make_response(error=True, message="method not allowed",
                                       status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile_cities(request):
    country = request.query_params.get('country')
    try:
        cities = Cities.objects.filter(country_id=country)
        cities_serializer = CitiesFkSerializer(cities, many=True)
        return Responses.make_response(cities_serializer.data)
    except:
        return Responses.make_response(error=True, message=CONSTANTS.get('error_server'),
                                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)
