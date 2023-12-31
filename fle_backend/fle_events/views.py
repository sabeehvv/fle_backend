from decimal import Decimal

# Django and DRF imports
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView #type:ignore
from rest_framework.response import Response #type:ignore
from rest_framework import status #type:ignore
from rest_framework.generics import UpdateAPIView, CreateAPIView #type:ignore

# Models and Serializers
from fle_user.models import Account
from .models import Event, Crowdfunding, FundContributor, Participant
from .serializers import EventSerializer, EventsViewSerializer, ParticipantSerializer, FundContributorViewSerializer

# Third-party libraries
import razorpay #type:ignore

# Custom mixins and sendmails
from fle_user.sendmails import send_contribution_email
from .mixin import AuthenticationMixin, PromoteParticipantsMixin


class EventCreateAPIView(AuthenticationMixin, CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(hosting_by=self.request.user)


class EventUpdateAPIView(PromoteParticipantsMixin, AuthenticationMixin, UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_update(self, serializer):
        event = self.get_object()
        self.promote_waiting_participants(event)
        serializer.save()


class EventListView(APIView):

    def get(self, request):
        print('hello  event')
        events = Event.objects.filter(
            event_approved=True).order_by('date_and_time')
        EventList = EventsViewSerializer(events, many=True)
        print(events[0])
        return Response(EventList.data)


class EventDetailView(AuthenticationMixin, APIView):

    def get(self, request, event_id):
        user = request.user
        user = request.user
        event = get_object_or_404(Event, id=event_id)
        event_serializer = EventsViewSerializer(event)

        participant = Participant.objects.filter(
            event=event, user=user).first()
        participant_serializer = ParticipantSerializer(
            participant) if participant else None

        response_data = {
            "event": event_serializer.data,
            "participant": participant_serializer.data if participant_serializer else None
        }
        return Response(response_data)


class EventJoinView(AuthenticationMixin, APIView):

    def post(self, request):
        event_id = request.data.get('event_id')
        bringing_members = request.data.get('bringing_members')

        event = get_object_or_404(Event, pk=event_id)
        if event.current_participants >= event.maximum_participants:
            rsvp_status = 'Waiting'
        else:
            rsvp_status = 'Going'
            event.current_participants += bringing_members + 1
            event.save()

        Participant.objects.create(
            event=event,
            user=request.user,
            rsvp_status=rsvp_status,
            bringing_members=bringing_members
        )
        message = 'Added into Waiting List, Event is full.' if rsvp_status == 'Waiting' else 'Join to Event successfully'
        return Response({'message': message}, status=status.HTTP_201_CREATED)


class DeleteJoinView(PromoteParticipantsMixin, AuthenticationMixin, APIView):

    def delete(self, request, event_id):
        user = request.user
        event = get_object_or_404(Event, pk=event_id)
        participant = Participant.objects.filter(event=event, user=user).first()
        print(participant,'participants')

        members = participant.bringing_members + 1
        rsvp_status = participant.rsvp_status
        participant.delete()

        if rsvp_status == "Going":
            event.current_participants -= members
            event.save()

        self.promote_waiting_participants(event)

        return Response({'message': 'Registration canceled'}, status=status.HTTP_200_OK)


class ContributorsView(APIView):
    def get(self, reqest):
        Contributors = FundContributor.objects.all().order_by("-contribution_date")
        serializer = FundContributorViewSerializer(Contributors, many=True)
        return Response(serializer.data)


# crowdfund Payment with razorpay
class ContributonView(APIView):
    def post(self, request):
        data = request.data
        amount = int(float(data['amount']))

        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        data = {"amount": amount, "currency": "INR"}
        payment = client.order.create(data=data)

        return Response({'order_id': payment['id'], 'amount': payment['amount'], 'currency': payment['currency']})


class VerifySignatureView(APIView):
    def post(self, request):
        data = request.data
        print(data, 'payments datas')

        amount = data['amount']
        event_id = data['event_id']
        user_id = data['user_id']
        dis_name = data['dis_name']

        params_dict = {
            'razorpay_payment_id': data['razorpay_paymentId'],
            'razorpay_order_id': data['razorpay_orderId'],
            'razorpay_signature': data['razorpay_signature']
        }

        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        status = client.utility.verify_payment_signature(params_dict)

        if status:
            event = Event.objects.get(id=event_id)
            fund = Crowdfunding.objects.get(event=event)
            fund.current_amount += Decimal(amount)
            fund.save()
            user = None
            try:
                user = Account.objects.get(id=user_id)
            except Account.DoesNotExist:
                pass
            fund_contributor = FundContributor(
                crowdfund_id=fund,
                contributor_display_name=dis_name,
                contribution_amount=Decimal(amount),
                user_id=user,
                UPI_ID=data.get('UPI_ID', ''),)
            fund_contributor.save()
            if user:
                send_contribution_email(user, event)
            print(fund_contributor, 'contributor')
            return Response({'status': 'Payment Successful'})
        return Response({'status': 'Payment Failed'})
