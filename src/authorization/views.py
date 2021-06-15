"""Views to manage Authentication"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

@api_view(['GET','POST'])
def candidate_login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return Response({"user":user}, status=status.HTTP_200_OK)
    else:
        return Response({"error":"Method no allowed"}, status=status.HTTP_200_OK)

