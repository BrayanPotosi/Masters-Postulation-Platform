from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions

# Serializers
from .serializers import ( 
                            CambridgeLevelSerializer,
                            ExperienceSerializer, 
                            FisrtPageProfileSerializer, 
                            SecondPageProfileSerializer, 
                            EducationSerializer,
                            LanguagesSerializer,
                            CitiesSerializer,
                            CountriesSerializer,
                            GottenGradeSerializer,
                            LastGradeSerializer,
                            CivilStatusSerializer,
                            CambridgeLevel,
                        )
# Models
from .models import Cities, CivilStatus, Countries, Education, GottenGrade, LastGrade, Profile, ProfessionalExperience, Languages


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile_form(request, page):
    
    countries_serializer = CountriesSerializer(Countries.objects.all(), many=True)
   
    if page == '1':
        
        civil_status_serializer = CivilStatusSerializer(CivilStatus.objects.all(), many=True)
        options = {
            "countries": countries_serializer.data,
            "civil_status": civil_status_serializer.data,
        }
        profile = Profile.objects.filter(user=request.user.id)
        serializer = FisrtPageProfileSerializer(profile, many=True)

        return Response({
                            "profile": serializer.data,
                            "options": options,
                        })
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
 
        gotten_grade_serializer = GottenGradeSerializer(GottenGrade.objects.all(), many=True)

        last_grade_serializer = LastGradeSerializer(LastGrade.objects.all(), many=True)

        cities_serializer = CitiesSerializer(Cities.objects.all(), many=True)

        canbridge_level_serializer = CambridgeLevelSerializer(CambridgeLevel.objects.all(), many=True)

        options = {
            "cities": cities_serializer.data,
            "countries": countries_serializer.data,
            "last_grade": last_grade_serializer.data,
            "gotten_grade": gotten_grade_serializer.data,
            "cambridge_level": canbridge_level_serializer.data,
        }

        return Response({
                            "profile": serializer.data, 
                            "education": education_serializer.data,
                            "experience": experience_serializer.data,
                            "language": language_serializer.data,
                            "options": options,
                        })
    else:
        return Response({"response": "page not found"}, status=404)