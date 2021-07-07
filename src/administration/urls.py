# from django
from django.urls import path

# from Views
from .views import candidates_view, AdministratorsView, GetCandidateDetails, GetAdminDetails, UpdateScore

app_name = 'administration'

urlpatterns = [
    path('candidates/', candidates_view, name='candidates_list'),
    path('candidates/<int:user>', GetCandidateDetails.as_view(), name='candidate_detail'),
    path('candidates/score/<int:pk>', UpdateScore.as_view(), name='update_score'),
    path('administrators/<int:pk>', GetAdminDetails.as_view(), name='admin_detail'),
    path('administrators/', AdministratorsView.as_view(), name='administratorss_list'),
]
