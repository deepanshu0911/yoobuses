# Generated by Django 4.0.3 on 2022-05-05 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0018_ticket_cancellation_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='exhausted',
            field=models.BooleanField(default=False),
        ),
    ]
