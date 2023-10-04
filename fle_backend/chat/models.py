from django.db import models
from fle_user.models import Account
from fle_events.models import Event

# Create your models here.

class EventChat(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)