from django.urls import path
# Views
from .views import profile_form, education_profile, LanguageProfile, ExperienceProfile,job_status, profile_cities

app_name = 'profiles'

urlpatterns = [
    path('information/', profile_form, name='progile_form'),
    path('job_status/', job_status, name='job_status'),
    path('education/', education_profile.as_view(), name='education_profile'),
    path('language/', LanguageProfile.as_view(), name='language_profile'),
    path('experience/', ExperienceProfile.as_view(), name='experience_profile'),
    path('cities/', profile_cities, name='profile_cities'),
]
