from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions

# Serializers
from .serializers import (CivilStatusSerializer, 
                            ExperienceSerializer, 
                            FisrtPageProfileSerializer, 
                            SecondPageProfileSerializer, 
                            EducationSerializer,
                            LanguagesSerializer,
                        )
# Models
from .models import Education, Profile, ProfessionalExperience, Languages


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile_form(request, page):

    if page == '1':
        profile = Profile.objects.filter(user=request.user.id)
        print(profile)
        serializer = FisrtPageProfileSerializer(profile, many=True)

        return Response(serializer.data)
    if page == '2':
        profile = Profile.objects.filter(user=request.user.id)
        serializer = SecondPageProfileSerializer(profile, many=True)
        profile_id = profile[0].id

        education_list = Education.objects.filter(profile=profile_id)
        education_serializer = EducationSerializer(education_list, many=True)

        experience_list = ProfessionalExperience.objects.filter(profile=profile_id)
        experience_serializer = ExperienceSerializer(experience_list, many=True)

        language_list = Languages.objects.filter(profile=profile_id)
        language_serializer = LanguagesSerializer(language_list, many=True)

        return Response({
                            "profile": serializer.data, 
                            "education": education_serializer.data,
                            "experience": experience_serializer.data,
                            "language": language_serializer.data,
                        })
    else:
        return Response({"response": "page not found"},status=404)