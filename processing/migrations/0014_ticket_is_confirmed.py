# Generated by Django 4.0.3 on 2022-04-29 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0013_rename_totalseats_bus_seatsleft'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]