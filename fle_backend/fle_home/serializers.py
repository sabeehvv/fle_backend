from rest_framework import serializers
from .models import EventHighlight, LandingPage


class EventHighlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventHighlight
        fields = "__all__"

    def create(self, validated_data):
        pk = self.initial_data.get('position', None)
        instance = self.Meta.model(pk=pk, **validated_data)
        instance.save()
        return instance


class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = ['video_url', 'announcement_text']
