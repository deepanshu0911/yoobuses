from django.urls import path
from processing import views

urlpatterns = [
    path('create-location', views.createLocation, name='create-location'),
    path('print-locations', views.printLocations, name='print-locations'),
    path('print-locations-by-search', views.printLocationBySearch, name='print-locations-by-search'),
    path('create-layout', views.createLayout, name='create-layout'),
    path('print-layouts', views.printLayouts),
    path('print-layout-by-id', views.printLayoutById),
    path('create-bus', views.createBus),
    path('create-bus-photo', views.createBusPhoto),
    path('print-bus-photos', views.printBusPhotos),
    path('check-bus-live', views.checkBusLive),
    path('print-buses', views.printBuses),
    path('print-bus-by-id', views.printBusById),
    path('print-buses-by-search', views.printBusesBySearch),
    
    # path('lock-seats', views.lockSeats),
    path('create-ticket', views.createTicket),
    path('print-tickets-for-user', views.printTicketsForUser),
    path('print-ticket-by-ticket-no', views.printTicketByTicketNo),
    path('print-ticket-for-cancellation', views.printTicketForCancellation),
]
