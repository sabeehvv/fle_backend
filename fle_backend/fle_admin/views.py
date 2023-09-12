from django.shortcuts import render
from fle_user.sendmails import send_event_approve_mail
from rest_framework.views import APIView
from fle_user.models import Account
from fle_events.models import Event
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from fle_user.serializers import UserSerializer,UserViewSerializer
from fle_events.serializers import EventsViewSerializer
from fle_user.permission import IsSuperuser
from rest_framework_simplejwt.authentication import JWTAuthentication  # type: ignore
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException, NotFound
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.timezone import now

# Create your views here.

class AdminViewUserManage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

    def get_object(self, pk):
        try:
            return Account.objects.get(id=pk)
        except Account.DoesNotExist:
            raise NotFound('User not found')


    def get(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'You are not an admin.'}, status=status.HTTP_403_FORBIDDEN)

        users = Account.objects.filter(is_superuser=False).order_by('id')
        UserList = UserSerializer(users, many=True)
        return Response(UserList.data)
    


    def patch(self, request, pk):
        user = self.get_object(pk)

        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        serializer = UserViewSerializer(user)
        return Response({
            'status': 400,
            'data': serializer.data

        })
    

class AdminViewEventManage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

    def get_object(self, id):
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise NotFound('User not found')

    def get(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'You are not an admin.'}, status=status.HTTP_403_FORBIDDEN)

        events = Event.objects.all().order_by('-date_and_time')
        EventList = EventsViewSerializer(events, many=True)
        return Response(EventList.data)
    

    def patch(self, request, id):
        event = self.get_object(id)

        if event.event_approved:
            print(event.event_approved,'hello ')
            event.event_approved = False
        else:
            event.event_approved = True
            user = Account.objects.get(email = event.hosting_by)
            message = f' Hi {user.first_name}, Your event "{event.event_name}" has been approved by the admin and is now published.'
            event_url = f'http://localhost:5173/events/eventdetail/{event.id}'
            send_event_approve_mail(user.email,message,event.event_name,event_url)

        event.save()
        return Response({
            'status': 400,
        })


