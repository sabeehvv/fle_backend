from django.db import models
from fle_user.models import Account
import uuid


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=200)
    description = models.TextField()
    date_and_time = models.DateTimeField()
    venue = models.CharField(max_length=200)
    hosting_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')
    crowdfunding_event = models.BooleanField(default=False)
    event_approved = models.BooleanField(default=False)
    maximum_participants = models.PositiveIntegerField()
    current_participants = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.event_name
    


class Crowdfunding(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refundable_donation = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    end_date = models.DateTimeField()
    
    def __str__(self):
        return f"Crowdfunding for {self.event.event_name}"
    


class FundContributor(models.Model):
    crowdfund_id = models.ForeignKey(Crowdfunding, on_delete=models.CASCADE)
    contributor_display_name = models.CharField(max_length=100)
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_date = models.DateTimeField(auto_now_add=True)
    is_refundable = models.BooleanField(default=False)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE,null=True,blank=True)
    UPI_ID = models.CharField(max_length=100)
    refunded = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Contribution by {self.contributor_display_name} to {self.crowdfund_id.event.event_name}"
    


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    bringing_members = models.PositiveIntegerField(default=0)
    registration_date = models.DateTimeField(auto_now_add=True)
    RSVP_CHOICES = [
        ('Going', 'Going'),
        ('Not Going', 'Not Going'),
        ('Waiting', 'Waiting'),
    ]
    rsvp_status = models.CharField(max_length=20, choices=RSVP_CHOICES, default='Not Going')