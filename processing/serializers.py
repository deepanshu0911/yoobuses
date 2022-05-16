from rest_framework import serializers
from processing.models import Location, SeatLayout, Bus, BusPhoto, Ticket

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('location_id', 'city', 'state')

class SeatLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatLayout
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'
  
class BusPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPhoto
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
