from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
# Django
from django.core.exceptions import ObjectDoesNotExist
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
        fields = ('level','id',)

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ('country_name','id',)

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ('city_name','id',)

class LastGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastGrade
        fields = ('name','id',)

class GottenGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=GottenGrade
        fields = ('name','id',)

class CivilStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivilStatus
        fields = ('c_status','id',)

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

    def create(self, request):
        data = request.data
        try:
            profile = Profile.objects.get(user=request.user.id)
            return ProfessionalExperience.objects.create(profile=profile, **data)
        except ObjectDoesNotExist:
            return None


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Education
        exclude = ['profile','created', 'updated']
        depth = 1
    
    def create(self,request):
        data = request.data
        try:
            profile = Profile.objects.get(user=request.user.id)
            gotten_grade = GottenGrade.objects.get(pk=data.get('gotten_grade_id')) or None
            last_grade = LastGrade.objects.get(pk=data.get('last_grade_id')) or None
            return Education.objects.create(profile=profile, last_grade=last_grade, gotten_grade=gotten_grade, **data)
        except ObjectDoesNotExist:
            return None
    
    def update(self, instance, data):
        try:
            instance.gotten_grade = GottenGrade.objects.get(pk=data.get('gotten_grade_id')) or None
            instance.last_grade = LastGrade.objects.get(pk=data.get('last_grade_id')) or None
            instance.institution_name = data.get('institution_name')
            instance.year_end = data.get('year_end')
            instance.save()
            return instance
        except ObjectDoesNotExist:
            return None


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        exclude = ['profile', 'created', 'updated']
        depth = 1

    def create(self, request):
        data = request.data
        try:
            profile = Profile.objects.get(user=request.user.id)
            level = CambridgeLevel.objects.get(pk=data.get('level_id')) or None
            return Education.objects.create(profile=profile, level=level, **data)
        except ObjectDoesNotExist:
            return None


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

    def create(self, request):
        print(f"-------------------------------------------\n")
        print(request)
        print(type(request))
        print(f"-------------------------------------------\n")
        data = request.data
        print(data)
        try:
            civil_status = CivilStatus.objects.get(pk=data.get('civil_status_id')) or None
            address = Address.objects.get(pk=data.get('Address_id')) or None
            return Profile.objects.create(user=request.user.id, civil_status=civil_status, address=address, **data)
        except ObjectDoesNotExist:
            return None


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
