from rest_framework import serializers
from fle_events.models import Event, Crowdfunding,FundContributor



class EventsDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["id","event_name","date_and_time","current_participants",]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.crowdfunding_event:
            try:
                crowdfunding = Crowdfunding.objects.get(event_id=instance)
                data['Event_Contributors'] = FundContributor.objects.filter(crowdfund_id=crowdfunding).count()
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