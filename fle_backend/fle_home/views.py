# Models and Serializers
from .models import EventHighlight, LandingPage, Volunteers
from .serializers import LandingPageSerializer, EventHighlightSerializer, VolunteerViewSerializer

# Django Rest Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Django Utilities
from django.shortcuts import get_object_or_404


class landingpageView(APIView):

    def get(self, request):
        landing_page = get_object_or_404(LandingPage, pk=1)
        serializer = LandingPageSerializer(landing_page)
        return Response(serializer.data)


class EventHighlightView(APIView):

    def get(self, request):
        event_highlights = EventHighlight.objects.all().order_by('pk')
        serializer = EventHighlightSerializer(event_highlights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VolunteersView(APIView):

    def get(self, request):
        Volunteerlist = Volunteers.objects.all().order_by('pk')
        Vserializer = VolunteerViewSerializer(Volunteerlist, many=True)
        return Response(Vserializer.data, status=status.HTTP_200_OK)
