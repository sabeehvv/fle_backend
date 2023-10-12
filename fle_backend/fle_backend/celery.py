from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab #type:ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fle_backend.settings')

app = Celery('fle_backend')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()



app.conf.beat_schedule = {
    'delete-old-tokens': {
        'task': 'notification.tasks.delete_old_tokens', 
        'schedule': crontab(hour=0, minute=0), 
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")