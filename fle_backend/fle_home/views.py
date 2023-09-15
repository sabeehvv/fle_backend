from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import EventHighlight,LandingPage
from .serializers import LandingPageSerializer,EventHighlightSerializer
 
# Create your views here.

class landingpageView(APIView):
    def get(self, request):
        try:
            landing_page = LandingPage.objects.get(pk=1)
        except LandingPage.DoesNotExist:
            return Response({"error": "LandingPage not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LandingPageSerializer(landing_page)
        return Response(serializer.data)
    

class EventHighlightView(APIView):
    def get(self, request):
        event_highlights = EventHighlight.objects.all().order_by('pk')
        serializer = EventHighlightSerializer(event_highlights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)