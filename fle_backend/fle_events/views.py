from rest_framework.response import Response
from rest_framework import status
import uuid
from fle_user.models import Account
from rest_framework.views import APIView
from fle_user.permission import IsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Event, Crowdfunding,FundContributor
from .serializers import EventSerializer,CrowdfundingSerializer,EventsViewSerializer
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
        event = Event.objects.get(id = event_id)
        Eventseialize = EventsViewSerializer(event)
        return Response(Eventseialize.data)
    
    

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