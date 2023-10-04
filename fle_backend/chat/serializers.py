from rest_framework import serializers #type:ignore
from .models import EventChat



class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    class Meta:
        model = EventChat

        fields  = "__all__"

    def get_sender(self, instance):
        user = instance.sender
        return {
            'id': user.id,
            'name': user.first_name,
        }