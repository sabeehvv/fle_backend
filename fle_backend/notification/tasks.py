from celery import shared_task #type:ignore
from django.utils import timezone
from .models import FCMToken

@shared_task
def delete_old_tokens():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    old_tokens = FCMToken.objects.filter(created_at__lt=one_month_ago)
    old_tokens.delete()
