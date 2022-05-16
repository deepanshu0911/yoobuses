# Generated by Django 4.0.3 on 2022-04-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0010_bus_ticketssold'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('bus_id', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=150, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('lower_deck', models.TextField(blank=True, null=True)),
                ('upper_deck', models.TextField(blank=True, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('boarding_point', models.CharField(blank=True, max_length=150, null=True)),
                ('dropping_point', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
    ]
