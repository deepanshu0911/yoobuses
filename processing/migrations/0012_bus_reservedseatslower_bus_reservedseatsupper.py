# Generated by Django 4.0.3 on 2022-04-28 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0011_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='reservedSeatsLower',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='reservedSeatsUpper',
            field=models.TextField(blank=True, null=True),
        ),
    ]
