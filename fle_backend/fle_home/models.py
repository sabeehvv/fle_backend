from django.db import models

# Create your models here.
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