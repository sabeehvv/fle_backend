from rest_framework import serializers
from .models import Event,Crowdfunding,Participant



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


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('bringing_members', 'registration_date', 'rsvp_status') 

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['rsvp_status'] == 'Waiting':
            waiting_position = self.calculate_waiting_position(instance)
            data['waiting_position'] = waiting_position
        return data

    def calculate_waiting_position(self, instance):
        event = instance.event
        registration_date = instance.registration_date
        waiting_participants = Participant.objects.filter(
            event=event,
            rsvp_status='Waiting',
            registration_date__lt=registration_date
        ).count()
        return waiting_participants + 1




