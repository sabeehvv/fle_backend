from django.shortcuts import render
from rest_framework.views import APIView #type:ignore
from rest_framework import status #type:ignore
from rest_framework.response import Response #type:ignore
from .models import FCMToken

# Create your views here.

class FCMTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not FCMToken.objects.filter(token=token).exists():
            FCMToken.objects.create(token=token)
        return Response(status=status.HTTP_200_OK)