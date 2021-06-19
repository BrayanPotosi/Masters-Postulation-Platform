from django.db import models
from django.db.models import fields
from rest_framework import serializers
# Models
from .models import (CivilStatus, Countries, 
                        Education, Profile, 
                        User, Address, 
                        JobStatus, Cities, 
                        ProfessionalExperience, Languages,
                        LastGrade, GottenGrade,
                        CambridgeLevel,
                    )

class CambridgeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CambridgeLevel
        fields = ('level',)

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ('country_name',)

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ('city_name',)

class LastGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastGrade
        fields = ('name',)

class GottenGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=GottenGrade
        fields = ('name',)

class CivilStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivilStatus
        fields = ('c_status',)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'id',
        )

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalExperience
        exclude = ['profile', 'created', 'updated']

class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Education
        exclude = ['profile', 'created', 'updated']
        depth = 1

class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        exclude = ['profile', 'created', 'updated']
        depth = 1


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Address
        fields = (
            'address_line1',
            'address_line2',
            'postal_code',
            'city',
            'country',
        )
        depth = 1

class JobStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobStatus

        fields = (
            'has_job',
            'company_name',
            'salary',
            'change_opt',
        )

class FisrtPageProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    civil_status = CivilStatusSerializer()
    Address = AddressSerializer()
    
    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'birthday',
            'civil_status',
            'Address',
        )

class SecondPageProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    Address = AddressSerializer()
    job_status = JobStatusSerializer()

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'Address',
            'home_phone',
            'work_phone',
            'mobile_phone',
            'job_status',
        )

