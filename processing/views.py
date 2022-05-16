from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db.models import Q
from processing.models import Location, SeatLayout, Bus, BusPhoto, Ticket
from processing.serializers import LocationSerializer, SeatLayoutSerializer, BusSerializer, BusPhotoSerializer, TicketSerializer
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
import json

@csrf_exempt
def createLocation(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        city = data['city']
        state = data['state']
        if not city.isupper():
            city = city.capitalize()
        if not state.isupper():
            state = state.capitalize()    
        if not Location.objects.filter(city=city, state=state).exists():
            Location.objects.create(city=city, state=state)
            return JsonResponse({'status': 'success'}, safe=False)
        else:
            return JsonResponse({'status': 'exists'}, safe=False)   

@csrf_exempt
def printLocations(request):
        if request.method == "POST":
          data = JSONParser().parse(request)
          locations = Location.objects.all().order_by('-location_id')
          p = Paginator(locations,10)
        try:
          locations = p.page(data['page'])
          locationsData = LocationSerializer(locations, many=True)
          return JsonResponse({'status': 'success', 'result': locationsData.data, 'page': data['page']}, safe=False)
        except:
          return JsonResponse({'status': 'not-found'})

@csrf_exempt
def printLocationBySearch(request):
     if request.method == 'POST':
       data = JSONParser().parse(request)
       locations = Location.objects.filter(Q(city__icontains=data['term'])|
       Q(state__icontains=data['term'])).order_by('-location_id')[:10]
       try:
          locationsData = LocationSerializer(locations, many=True)
          return JsonResponse({'status': 'success', 'result': locationsData.data}, safe=False)
       except:
          return JsonResponse({'status': 'not-found'})

@csrf_exempt
def createLayout(request):
  if request.method == 'POST':
    data = JSONParser().parse(request)
    layoutData = json.dumps(data['layout'])
    SeatLayout.objects.create(layout_title=data['title'],
       rows=data['rows'], columns=data['columns'], layout=layoutData,
       seat_type=data['type'])
    return JsonResponse({'status': 'success'}, safe=False)   

def printLayouts(request):
  if request.method == 'GET':
    layouts = SeatLayout.objects.all()
    layoutsData = SeatLayoutSerializer(layouts, many=True)
    return JsonResponse({'status': 'success', 'result': layoutsData.data}, safe=False)

@csrf_exempt
def printLayoutById(request):
      if request.method == 'POST':
        data = JSONParser().parse(request)
        layout = SeatLayout.objects.filter(layout_id=data['layoutId'])
        layoutData = SeatLayoutSerializer(layout, many=True)
        return JsonResponse({'status': 'success', 'result': layoutData.data}, safe=False)


@csrf_exempt
def createBus(request):
  if request.method == 'POST':
    data = JSONParser().parse(request)
    if data['step']=='step1':
      bus =  Bus(bus_name=data['busName'], bus_type=data['busType'],
         location_from=data['locationFrom'], location_to=data['locationTo'],
         ticket_price=data['ticketPrice'], discount_price=data['discountPrice'],
         departure_stop=data['departureStop'], arrival_stop=data['arrivalStop'],
         first_timing=data['firstTiming'], last_timing=data['lastTiming'], 
         lower_deck=data['lowerDeck'], upper_deck=data['upperDeck'])
      lowerDeck = SeatLayout.objects.get(layout_id=data['lowerDeck'])
      lowerDeckSeats = json.loads(lowerDeck.layout)
      seats1 = []
      seats2 = []
      for key, value in lowerDeckSeats.items():
          if value!='empty':
                seats1.append(value)
      seats1.sort()   
             
      bus.seats1 = json.dumps(seats1)          
      if data['upperDeck'] !='none':
            upperDeck = SeatLayout.objects.get(layout_id=data['upperDeck'])
            upperDeckSeats = json.loads(upperDeck.layout)
            for key, value in upperDeckSeats.items():
              if value!='empty':
                    seats2.append(value)
            seats2.sort()
            bus.seats2 = json.dumps(seats2)
      bus.seatsLeft = len(seats1) + len(seats2) 
      bus.save()   
      return JsonResponse({'status': 'success', 'bus_id': bus.bus_id}, safe=False)
    if data['step']=='step2':
      bus = Bus.objects.get(bus_id=data['busId'])
      bus.dropping_points = json.dumps(data['droppingPoints'])
      bus.boarding_points = json.dumps(data['boardingPoints'])
      bus.save()
      return JsonResponse({'status': 'success', 'bus_id': bus.bus_id}, safe=False)
    if data['step']=='step3':
      bus = Bus.objects.get(bus_id=data['busId'])
      bus.seller_name = data['sellerName']
      bus.seller_mobile = data['sellerMobile']
      bus.bank_name = data['bankName']
      bus.holder_name = data['holderName']
      bus.ac_no = data['acNo']
      bus.ifsc_code = data['ifscCode']
      bus.staff = json.dumps(data['staff'])
      bus.save()
      return JsonResponse({'status': 'success', 'bus_id': bus.bus_id}, safe=False)
    if data['step']=='final':
      bus = Bus.objects.get(bus_id=data['busId'])
      if data['cancellation']=='yes':
          bus.cancellation_available = True
      bus.is_live = True
      bus.save()
      return JsonResponse({'status': 'success', 'bus_id': bus.bus_id}, safe=False)

# @csrf_exempt
# def createBusPhoto(request):
#     if request.method == 'POST':
#        bus_id = request.POST.get('busId')
#        photo1 = request.FILES.get('photo1')
#        photo2 = request.FILES.get('photo2')
#        photo3 = request.FILES.get('photo3')
#        photo4 = request.FILES.get('photo4')
#        photo5 = request.FILES.get('photo5')
#        photo6 = request.FILES.get('photo6')
#        if BusPhoto.objects.filter(bus_id=bus_id).exists():
#              BusPhoto.objects.filter(bus_id=bus_id).update(photo1=photo1, photo2=photo2,
#                  photo3=photo3, photo4=photo4, photo5=photo5, photo6=photo6)
#        else:          
#           BusPhoto.objects.create(bus_id=bus_id, photo1=photo1, photo2=photo2,
#                  photo3=photo3, photo4=photo4, photo5=photo5, photo6=photo6)
#        return JsonResponse({'status': 'success'})          

@csrf_exempt
def createBusPhoto(request):
    if request.method == 'POST':
       bus_id = request.POST.get('busId')
       photo1 = request.FILES.get('photo1')
       photo2 = request.FILES.get('photo2')
       photo3 = request.FILES.get('photo3')
       photo4 = request.FILES.get('photo4')
       photo5 = request.FILES.get('photo5')
       photo6 = request.FILES.get('photo6')
       if Bus.objects.filter(bus_id=bus_id).exists():
             Bus.objects.filter(bus_id=bus_id).update(photo1=photo1, photo2=photo2,
                 photo3=photo3, photo4=photo4, photo5=photo5, photo6=photo6)
             bus = Bus.objects.get(bus_id=bus_id)
             bus.photo1 = photo1
             bus.photo2 = photo2    
             bus.photo3 = photo3
             bus.photo4 = photo4 
             bus.photo5 = photo5 
             bus.photo6 = photo6  
             bus.save()
       else:          
          Bus.objects.create(bus_id=bus_id, photo1=photo1, photo2=photo2,
                 photo3=photo3, photo4=photo4, photo5=photo5, photo6=photo6)
       return JsonResponse({'status': 'success'})     

@csrf_exempt
def printBusPhotos(request):
    if request.method == 'POST':
      data = JSONParser().parse(request)
      if BusPhoto.objects.filter(bus_id=data['busId']).exists:
        busPhotos = BusPhoto.objects.filter(bus_id=data['busId'])
        busPhotosData = BusPhotoSerializer(busPhotos, many=True)
        return JsonResponse({'status': 'success', 'result': busPhotosData.data}, safe=False)  

@csrf_exempt
def checkBusLive(request):
  if request.method == 'POST':
    data = JSONParser().parse(request)
    if Bus.objects.filter(bus_id=data['busId'],is_live=True):
      return JsonResponse({'status': 'live'})
    else:
      return HttpResponse('Not live')  

@csrf_exempt
def printBuses(request):
  if request.method == 'POST':
    data = JSONParser().parse(request)
    buses = Bus.objects.all().order_by('-bus_id')
    p = Paginator(buses,10)
    try:
      buses = p.page(data['page'])
      busesData = BusSerializer(buses, many=True)
      return JsonResponse({'status': 'success', 'result': busesData.data, 'page': data['page']}, safe=False)
    except:
      return JsonResponse({'status': 'not-found'})

@csrf_exempt
def printBusesBySearch(request):
  if request.method == 'POST':
    data = JSONParser().parse(request)
    buses = Bus.objects.filter(location_from__icontains=data['source'],
            location_to__icontains=data['destination'], first_timing__date=data['date']).order_by('-bus_id')
    # p = Paginator(buses,10)
    # try:
    #   buses = p.page(data['page'])
    busesData = BusSerializer(buses, many=True)
    return JsonResponse({'status': 'success', 'result': busesData.data}, safe=False)
    # except:
      # return JsonResponse({'status': 'not-found'})

@csrf_exempt
def printBusById(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        bus = Bus.objects.filter(bus_id=data['busId'])
        busData = BusSerializer(bus, many=True)
        return JsonResponse({'status': 'success', 'result': busData.data}, safe=False)


# @csrf_exempt
# def lockSeats(request):
#     if request.method == 'POST':
#       data = JSONParser().parse(request)
#       bus = Bus.objects.get(bus_id=data['busId'])
#       lowerDeck = data['lowerDeck']
#       upperDeck = data['upperDeck']

#       bus.seats1 = json.loads(bus.seats1)
#       if bus.seats2:
#         bus.seats2 = json.loads(bus.seats2)
      
#       if bus.reservedSeatsLower is None:
#             bus.reservedSeatsLower = []
#       else:
#          bus.reservedSeatsLower = json.loads(bus.reservedSeatsLower)      
#       if bus.reservedSeatsUpper is None:
#             bus.reservedSeatsUpper = []      
#       else:
#         bus.reservedSeatsUpper = json.loads(bus.reservedSeatsUpper)  

#       for l in lowerDeck:
#         if l in bus.seats1:
#           bus.seats1.remove(l)
#           bus.reservedSeatsLower.append(l)
#         else:
#           return JsonResponse({'status': 'booked'})
#       for u in upperDeck:
#         if u in bus.seats2:
#           bus.seats2.remove(u)
#           bus.reservedSeatsUpper.append(u)
#         else:
#           return JsonResponse({'status': 'booked'})
#       bus.seats1 = json.dumps(bus.seats1)
#       if bus.seats2:
#         bus.seats2 = json.dumps(bus.seats2)
#       bus.reservedSeatsLower = json.dumps(bus.reservedSeatsLower)
#       bus.reservedSeatsUpper = json.dumps(bus.reservedSeatsUpper)  
#       bus.save()
#       return JsonResponse({'status': 'success'})    
        


@csrf_exempt
def createTicket(request):
    if request.method == 'POST':
      data = JSONParser().parse(request)
      ticket = Ticket.objects.create(bus_id=data['busId'], user_id=data['userId'], name=data['name'],mobile=data['mobile'], email=data['email'],
                       gender=data['gender'], lower_deck=json.dumps(data['lowerDeck']), upper_deck=json.dumps(data['upperDeck']),
                       total=data['total'], boarding_point=data['boardingPoint'], dropping_point=data['droppingPoint'],
                       )

      bus = Bus.objects.get(bus_id=data['busId'])
      lowerDeck = data['lowerDeck']
      upperDeck = data['upperDeck']      
      
      if bus.reservedSeatsLower is None:
            bus.reservedSeatsLower = []
      else:
         bus.reservedSeatsLower = json.loads(bus.reservedSeatsLower)      
      if bus.reservedSeatsUpper is None:
            bus.reservedSeatsUpper = []      
      else:
        bus.reservedSeatsUpper = json.loads(bus.reservedSeatsUpper)      
      
      bus.seats1 = json.loads(bus.seats1)
      if bus.seats2:
       bus.seats2 = json.loads(bus.seats2)
      
      for l in lowerDeck:
         bus.reservedSeatsLower.append(l)
         bus.seats1.remove(l)
      for u in upperDeck:
         bus.reservedSeatsUpper.append(u)   
         bus.seats2.remove(u)
      
      bus.reservedSeatsLower = json.dumps(bus.reservedSeatsLower)
      bus.reservedSeatsUpper = json.dumps(bus.reservedSeatsUpper)
      bus.seats1 = json.dumps(bus.seats1)
      if bus.seats2:
        bus.seats2 = json.dumps(bus.seats2)
      
      bus.seatsLeft = bus.seatsLeft - (len(lowerDeck) + len(upperDeck)) 
      bus.ticketsSold = bus.ticketsSold + len(lowerDeck) + len(upperDeck)
      ticket.ticket_url = str(ticket.ticket_id) + str(ticket.name[0].lower()) + str(ticket.name[1].lower()) + str(ticket.mobile)
      ticket.save()
      bus.save()
      return JsonResponse({'status': 'success'}, safe=False)

@csrf_exempt
def printTicketsForUser(request):
  if request.method == 'POST':
    data = JSONParser().parse(request)
    tickets = Ticket.objects.filter(user_id=data['userId']).order_by('-ticket_id')[:20]
    ticketsData = TicketSerializer(tickets, many=True)
    return JsonResponse({'status': 'success', 'result': ticketsData.data}, safe=False)

@csrf_exempt
def printTicketByTicketNo(request):
   if request.method == 'POST':
      data = JSONParser().parse(request)
      ticket = Ticket.objects.filter(ticket_url=data['ticketUrl']) 
      ticketData = TicketSerializer(ticket, many=True)
      return JsonResponse({'status': 'success', 'result': ticketData.data}, safe=False)

@csrf_exempt
def printTicketForCancellation(request):
  if request.method == 'POST':
    data = JSONParser().parse(request)
    ticket = Ticket.objects.filter(ticket_id=data['ticketNo'], email=data['email'], 
             cancellation_available=True, exhausted=False)
    ticketData = TicketSerializer(ticket, many=True)
    return JsonResponse({'status': 'success', 'result': ticketData.data}, safe=False)
         