# Django
from django.urls import path
# Views
from .views import profile_form, EducationProfile, LanguageProfile, ExperienceProfile, job_status, profile_cities

app_name = 'profiles'

urlpatterns = [
    path('information/', profile_form, name='profile_form'),
    path('job_status/', job_status, name='job_status'),
    path('education/', EducationProfile.as_view(), name='EducationProfile'),
    path('language/', LanguageProfile.as_view(), name='language_profile'),
    path('experience/', ExperienceProfile.as_view(), name='experience_profile'),
    path('cities/', profile_cities, name='profile_cities'),
]
