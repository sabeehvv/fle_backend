from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from fle_user.permission import IsUser
from .models import Participant


class AuthenticationMixin:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUser]


class PromoteParticipantsMixin:

    def promote_waiting_participants(self, event):
        waiting_participants = Participant.objects.filter(
            event=event, rsvp_status='Waiting').order_by("registration_date")
        while event.current_participants < int(event.maximum_participants) and waiting_participants:
            waiting_participant = waiting_participants.first()
            waiting_participant.rsvp_status = 'Going'
            waiting_participant.save()
            event.current_participants += 1
            waiting_participants = waiting_participants.exclude(
                pk=waiting_participant.pk)
            event.save()
