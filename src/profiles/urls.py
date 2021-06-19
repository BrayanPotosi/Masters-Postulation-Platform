from django.urls import path
from .api import contact_api_view

urlpatterns = [
    path('job-status', contact_api_view, name='ProfileApi')
]