# Generated by Django 4.2.4 on 2023-09-10 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_and_time', models.DateTimeField()),
                ('venue', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='event_images/')),
                ('crowdfunding_event', models.BooleanField(default=False)),
                ('event_approved', models.BooleanField(default=False)),
                ('maximum_participants', models.PositiveIntegerField()),
                ('current_participants', models.PositiveIntegerField(default=0)),
                ('hosting_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Crowdfunding',
            fields=[
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='fle_events.event')),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('refundable_donation', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='FundContributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributor_display_name', models.CharField(max_length=100)),
                ('contribution_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contribution_date', models.DateTimeField(auto_now_add=True)),
                ('is_refundable', models.BooleanField(default=False)),
                ('UPI_ID', models.CharField(max_length=100)),
                ('refunded', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('crowdfund_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fle_events.crowdfunding')),
            ],
        ),
    ]
