# Django Utilities
from django.shortcuts import get_object_or_404

# Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView

# Models and Serializers
from fle_user.models import Account
from fle_user.serializers import UserSerializer, UserViewSerializer
from fle_events.models import Event
from fle_events.serializers import EventsViewSerializer
from fle_home.models import LandingPage, EventHighlight
from fle_home.serializers import EventHighlightSerializer, LandingPageSerializer


# Custom mixins and sendmails
from fle_user.sendmails import send_event_approve_mail
from .mixin import AuthenticationMixin


class LandingPageView(AuthenticationMixin, RetrieveAPIView):
    serializer_class = LandingPageSerializer

    def get_object(self):
        return LandingPage.objects.first()


class LandingPageUpdateView(AuthenticationMixin, UpdateAPIView):
    queryset = LandingPage.objects.all()
    serializer_class = LandingPageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return LandingPage.objects.first()


class EventHighlightCreateView(AuthenticationMixin, CreateAPIView):
    queryset = EventHighlight.objects.all()
    serializer_class = EventHighlightSerializer


class EventHighlightDeleteView(AuthenticationMixin, DestroyAPIView):
    queryset = EventHighlight.objects.all()
    serializer_class = EventHighlightSerializer


class AdminEventHighlight(AuthenticationMixin, APIView):

    def get(self, request):
        event_highlights = EventHighlight.objects.all().order_by('pk')
        serializer = EventHighlightSerializer(event_highlights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminViewUserManage(AuthenticationMixin, APIView):

    def get(self, request):
        users = Account.objects.filter(is_superuser=False).order_by('id')
        UserList = UserSerializer(users, many=True)
        return Response(UserList.data)

    def patch(self, request, pk):
        user = get_object_or_404(Account, pk=pk)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        serializer = UserViewSerializer(user)
        return Response({
            'status': 400,
            'data': serializer.data})


class AdminViewEventManage(AuthenticationMixin, APIView):

    def get(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'You are not an admin.'}, status=status.HTTP_403_FORBIDDEN)

        events = Event.objects.all().order_by('-date_and_time')
        EventList = EventsViewSerializer(events, many=True)
        return Response(EventList.data)

    def patch(self, request, id):
        event = get_object_or_404(Event, id=id)
        if event.event_approved:
            event.event_approved = False
        else:
            event.event_approved = True
            user = Account.objects.get(email=event.hosting_by)
            send_event_approve_mail(user, event)

        event.save()
        return Response({
            'status': 400,
        })
