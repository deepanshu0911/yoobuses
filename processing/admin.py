from django.contrib import admin
from processing.models import Location, SeatLayout, Bus, BusPhoto, Ticket

admin.site.register(Location)
admin.site.register(SeatLayout)
admin.site.register(Bus)
admin.site.register(BusPhoto)
admin.site.register(Ticket)
