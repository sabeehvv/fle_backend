from rest_framework import serializers
from .models import Event, Crowdfunding, Participant, FundContributor


class CrowdfundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crowdfunding
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    hosting_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        crowdfunding_event = validated_data.get('crowdfunding_event')
        if crowdfunding_event:
            crowdfunding_data = {
                'event': event.id,
                'target_amount': self.initial_data.get('target_amount', None),
                'end_date': validated_data.get('date_and_time'),
            }
            crowdfunding_serializer = CrowdfundingSerializer(
                data=crowdfunding_data)
            if crowdfunding_serializer.is_valid():
                crowdfunding_serializer.save()
            else:
                errors = crowdfunding_serializer.errors
                print(errors, "error")
        return event


class EventsViewSerializer(serializers.ModelSerializer):
    hosting_by = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_hosting_by(self, instance):
        user = instance.hosting_by
        return {
            'user_id': user.id,
            'first_name': user.first_name,
        }

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


class FundContributorViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = FundContributor
        fields = ['id', 'contributor_display_name',
                  'contribution_amount', 'contribution_date']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        crowdfund = instance.crowdfund_id
        event = crowdfund.event

        data['event_name'] = event.event_name
        data['date_and_time'] = event.date_and_time
        data['venue'] = event.venue

        return data
