from django.db import models
from fle_user.models import Account


class LandingPage(models.Model):
    video_url = models.URLField(max_length=255)
    announcement_text = models.TextField()

    def __str__(self):
        return "Landing Page"


class EventHighlight(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='event_highlights/')

    def __str__(self):
        return self.heading


class Volunteers(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return self.role
