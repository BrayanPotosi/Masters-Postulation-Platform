from django.urls import path
from .views import report_users

app_name = 'reports'

urlpatterns = [
    path('users/', report_users, name='users')
]