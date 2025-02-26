# Generated by Django 3.2.25 on 2025-01-05 11:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0003_alter_book_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='borrowed_books',
        ),
        migrations.RemoveField(
            model_name='member',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='member',
            name='fine_balance',
        ),
        migrations.RemoveField(
            model_name='member',
            name='membership_expiry',
        ),
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
        migrations.AddField(
            model_name='member',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='created_at',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='member',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='member',
            name='membership_type',
            field=models.CharField(choices=[('regular', 'Regular'), ('premium', 'Premium')], default='regular', max_length=50),
        ),
        migrations.AddField(
            model_name='member',
            name='name',
            field=models.CharField(default='Anonymous', max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
