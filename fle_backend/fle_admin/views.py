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
from fle_home.models import LandingPage,EventHighlight
from fle_home.serializers import EventHighlightSerializer,LandingPageSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

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



class LandingPageUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

    def patch(self, request):
        print("hello start")
        try:
            landing_page = LandingPage.objects.get(pk=1)
            print("hello done pk")
        except LandingPage.DoesNotExist:
            return Response({"error": "LandingPage not found"}, status=status.HTTP_404_NOT_FOUND)

        if "video_url" in request.data:
            print("hello video url")
            video_url = request.data["video_url"]
            if not self.is_valid_url(video_url):
                return Response({"error": "Invalid video URL"}, status=status.HTTP_400_BAD_REQUEST)
            landing_page.video_url = video_url

        if "announcement" in request.data:
            landing_page.announcement_text = request.data["announcement"]

        landing_page.save()
        return Response({"message": "Updated successfully"})

    def is_valid_url(self, url):
        validator = URLValidator()
        try:
            validator(url)
            return True
        except ValidationError:
            return False
        

    def get(self, request):
        try:
            landing_page = LandingPage.objects.get(pk=1)
        except LandingPage.DoesNotExist:
            return Response({"error": "LandingPage not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LandingPageSerializer(landing_page)
        return Response(serializer.data)
        

class AdminEventHighlight(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        pk = request.data.get("position")
        heading = request.data.get("heading", "")
        description = request.data.get("description", "")
        image = request.data.get("image", None)

        if pk is not None and EventHighlight.objects.filter(pk=pk).exists():
            return Response({"error": f"EventHighlight with PK {pk} already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        event_highlight = EventHighlight(
            pk = pk,
            heading=heading,
            description=description,
            image=image
        )
        event_highlight.save()
        print(pk,"pk number where")
        return Response({"message": "EventHighlight created successfully"}, status=status.HTTP_201_CREATED)
    

    def delete(self, request, pk):
        try:
            event_highlight = EventHighlight.objects.get(pk=pk)
            event_highlight.delete()
            return Response({"message": "EventHighlight deleted successfully."}, status=status.HTTP_200_OK)
        except EventHighlight.DoesNotExist:
            return Response({"error": f"EventHighlight with PK {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        
    
    def get(self, request):
        event_highlights = EventHighlight.objects.all().order_by('pk')
        serializer = EventHighlightSerializer(event_highlights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)