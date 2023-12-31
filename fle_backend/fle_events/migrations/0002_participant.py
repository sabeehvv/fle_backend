# Generated by Django 4.2.4 on 2023-09-17 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fle_events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bringing_members', models.PositiveIntegerField(default=0)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('rsvp_status', models.CharField(choices=[('Going', 'Going'), ('Not Going', 'Not Going'), ('Waiting', 'Waiting')], default='Not Going', max_length=20)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fle_events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
