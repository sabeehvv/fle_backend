from django.db import models
from django.utils import timezone
from django_celery_beat.models import SolarSchedule #type:ignore

class FCMToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token
    


class CustomSolarSchedule(SolarSchedule):
    class Meta:
        app_label = 'django_celery_beat'