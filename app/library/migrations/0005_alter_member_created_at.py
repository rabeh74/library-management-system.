# Generated by Django 3.2.25 on 2025-01-06 09:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20250105_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]