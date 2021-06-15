"""Authentication URLs."""

#Django
from django.urls import include, path
from .views import candidate_login_view

app_name = 'authorization'

urlpatterns = [
    path(route='api/v1/auth/candidate/login', view=candidate_login_view, name='candidate_login')
]