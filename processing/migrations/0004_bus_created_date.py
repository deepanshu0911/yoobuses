# Generated by Django 4.0.3 on 2022-04-20 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0003_bus_busphoto_alter_seatlayout_layout_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
