from django.urls import path
# Views
from .views import profile_form, education_profile

app_name = 'profiles'

urlpatterns = [
    path('page/<int:page>', profile_form, name='page_form'),
    path('education/', education_profile.as_view(), name='education_profile'),
]
