from rest_framework.response import Response
from rest_framework import status
import uuid
from fle_user.models import Account
from rest_framework.views import APIView
from fle_user.permission import IsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Event, Crowdfunding,FundContributor,Participant
from .serializers import EventSerializer,CrowdfundingSerializer,EventsViewSerializer,ParticipantSerializer
from datetime import datetime
import razorpay
from django.conf import settings
from decimal import Decimal




class create_event(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        event_data = request.data
        print(event_data,'dataaaaaaaaa')

        event_serializer = EventSerializer(data=event_data,context = {"request" : request})
        
        if event_serializer.is_valid():
            event = event_serializer.save()

            crowdfunding_event = event_data.get('crowdfunding_event', False)
            print(event_data,'event dataaaaaaaaaaa')
            print(crowdfunding_event)
            if crowdfunding_event:
                crowdfunding_data = {
                    'event': event.id,
                    'target_amount': event_data.get('target_amount'),
                    'end_date': event.date_and_time,
                }
                crowdfunding_serializer = CrowdfundingSerializer(data=crowdfunding_data)
                print('crowd fund saved')
                if crowdfunding_serializer.is_valid():
                    print('valid ')
                    crowdfunding_serializer.save()
            return Response({'message': 'Event created successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(event_serializer.errors)
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewEventManage(APIView):
    def get(self, request):
        print('hello  event')
        events = Event.objects.filter(event_approved=True).order_by('date_and_time')
        EventList = EventsViewSerializer(events, many=True)
        print(events[0])
        return Response(EventList.data)
    

class UserViewEvenDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUser]

    def get(self,request,event_id):
        user = request.user
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        Eventseialize = EventsViewSerializer(event)

        try:
            participant = Participant.objects.get(event=event, user=user)
        except Participant.DoesNotExist:
            participant = None

        if participant:
            participant_serializer = ParticipantSerializer(participant)
        else:
            participant_serializer = None
        if participant_serializer:
            participant = participant_serializer.data

        return Response({"event":Eventseialize.data ,"participant":participant})
    
    

class ContributonView(APIView):
    def post(self, request):
        data = request.data
        amount = int(float(data['amount']))

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        data = {"amount": amount, "currency": "INR"}
        payment = client.order.create(data=data)

        return Response({'order_id': payment['id'], 'amount': payment['amount'], 'currency': payment['currency']})


class VerifySignatureView(APIView):
    def post(self, request):
        data = request.data
        print(data,'payments datas')

        amount = data['amount']
        event_id = data['event_id']
        user_id = data['user_id']
        dis_name = data['dis_name']

        params_dict = {
            'razorpay_payment_id': data['razorpay_paymentId'],
            'razorpay_order_id': data['razorpay_orderId'],
            'razorpay_signature': data['razorpay_signature']
        }

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        status = client.utility.verify_payment_signature(params_dict)

        if status:
            event = Event.objects.get(id = event_id)
            fund = Crowdfunding.objects.get(event=event)
            fund.current_amount += Decimal(amount)
            fund.save()
            user = None
            try:
                user = Account.objects.get(id = user_id)
            except Account.DoesNotExist:
                        pass
            fund_contributor = FundContributor(
                    crowdfund_id=fund,
                    contributor_display_name=dis_name,
                    contribution_amount=Decimal(amount),
                    user_id=user,
                    UPI_ID=data.get('UPI_ID', ''),)
            fund_contributor.save()
            print(fund_contributor,'contributor')
            
            return Response({'status': 'Payment Successful'})
        return Response({'status': 'Payment Failed'})
    


class EventJoinView(APIView):
    def post(self, request):
        event_id = request.data.get('event_id')
        bringing_members = request.data.get('bringing_members')
        
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if event.current_participants >= event.maximum_participants:
            participant, _ = Participant.objects.get_or_create(
            event=event,
            user=request.user,
            )
            participant.rsvp_status = 'Waiting'
            participant.save()
            return Response({'message': 'You are in Waiting List /n Event is full.'})
        
        participant, _ = Participant.objects.get_or_create(
            event=event,
            user=request.user,
        )
        participant.bringing_members = bringing_members
        participant.rsvp_status = 'Going'
        participant.save()
        event.current_participants += bringing_members + 1
        event.save()
        print(event.current_participants,'currenct members')

        return Response({'message': 'Join to Event successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, event_id):
        user = request.user
        try:
            event = Event.objects.get(pk=event_id)
            participant = Participant.objects.get(event=event,user=user)
        except Event.DoesNotExist:
            return Response({'error': 'Event or participant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        members = participant.bringing_members + 1
        rsvp_status = participant.rsvp_status
        participant.delete()

        if rsvp_status == "Going":
            event.current_participants -= members
            event.save()

        waiting_participants = Participant.objects.filter(event=event, rsvp_status='Waiting').order_by("registration_date")
        while event.current_participants < event.maximum_participants and waiting_participants:
            waiting_participant = waiting_participants.first()
            waiting_participant.rsvp_status = 'Going'
            waiting_participant.save()
            event.current_participants += 1
            waiting_participants = waiting_participants.exclude(pk=waiting_participant.pk)
            event.save()

        return Response({'message': 'Registration canceled'}, status=status.HTTP_204_NO_CONTENT)