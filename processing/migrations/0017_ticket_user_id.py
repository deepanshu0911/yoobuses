# Generated by Django 4.0.3 on 2022-05-01 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0016_rename_ticket_no_ticket_ticket_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='user_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
