from django.db import models
from django.utils import timezone

class FCMToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token