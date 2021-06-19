from django.urls import path
# Views
from .views import profile_form

app_name = 'profiles'

urlpatterns = [
    path('page/<page>', profile_form, name='page_form'),
]
