from django.shortcuts import render
from rest_framework.views import APIView  # type:ignore
from rest_framework.response import Response  # type:ignore
from rest_framework import status  # type:ignore
from fle_events.mixin import AuthenticationMixin
from django.db.models import Q
from .models import EventChat
from .serializers import MessageSerializer


# Create your views here.

class ChatMessageApiView(APIView, AuthenticationMixin):
    def get(self, request, event_id):
        try:
            messages = EventChat.objects.filter(receiver_id=event_id).order_by('timestamp')
            print('Number of Messages Retrieved:', messages.count())
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
