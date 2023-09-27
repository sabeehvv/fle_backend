from rest_framework import serializers
from .models import EventHighlight, LandingPage, Volunteers
from fle_user.models import Account


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


class VolunteerViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteers
        fields = ['id', 'role', 'details']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user

        representation['user_first_name'] = user.first_name
        representation['user_last_name'] = user.last_name
        if user.picture:
            representation['user_picture'] = user.picture.url
        else:
            representation['user_picture'] = None

        return representation
