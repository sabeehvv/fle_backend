from rest_framework import serializers
from .models import Event,Crowdfunding



class EventSerializer(serializers.ModelSerializer):

    date_and_time = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])


    hosting_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {'hosting_by': {'required': False}}

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['hosting_by'] = user
        return super().create(validated_data)


class CrowdfundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crowdfunding
        fields = '__all__'


class EventsViewSerializer(serializers.ModelSerializer):

    hosting_by = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_hosting_by(self, instance):
        user = instance.hosting_by
        return user.first_name


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.crowdfunding_event:
            try:
                crowdfunding = Crowdfunding.objects.get(event_id=instance)
                data['target_amount'] = crowdfunding.target_amount
                data['current_amount'] = crowdfunding.current_amount
            except Crowdfunding.DoesNotExist:
                pass
        return data
    

    class EventsUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = '__all__'






