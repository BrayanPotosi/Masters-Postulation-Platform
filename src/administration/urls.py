from django.urls import path
# Views
from .views import candidates_view, administrators_view

app_name = 'administration'

urlpatterns = [
    path('candidates/', candidates_view, name='candidates_list'),
    path('administrators/', administrators_view.as_view(), name='administratorss_list'),
]