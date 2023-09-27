from rest_framework import serializers
from fle_events.models import Event, Crowdfunding, FundContributor
from fle_home.models import Volunteers
from fle_user.models import Account


class EventsDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["id", "event_name", "date_and_time", "current_participants",]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.crowdfunding_event:
            try:
                crowdfunding = Crowdfunding.objects.get(event_id=instance)
                data['Event_Contributors'] = FundContributor.objects.filter(
                    crowdfund_id=crowdfunding).count()
                data['current_amount'] = crowdfunding.current_amount
            except Crowdfunding.DoesNotExist:
                pass
        return data


class UserDataSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    new_users_count = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_events = serializers.IntegerField()
    Total_Contributions = serializers.IntegerField()


class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteers
        fields = ['id', 'role', 'details']

    def create(self, validated_data):
        pk = self.initial_data.get('position', None)
        user_id = self.initial_data.get('user_id', None)
        user = Account.objects.get(id=user_id)
        instance = self.Meta.model(pk=pk, user=user, **validated_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user

        representation['user_id'] = user.id
        representation['user_first_name'] = user.first_name

        return representation


class UserVolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name']
