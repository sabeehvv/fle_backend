from rest_framework import serializers
from .models import EventHighlight,LandingPage


class EventHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventHighlight
        fields = '__all__'

class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = '__all__'
