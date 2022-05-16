from django.db import models
import uuid
import os

def bus_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/images', filename)

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, null=True, blank=True)
    objects = models.Manager()
 
    def __str__(self):
       return self.city + ', ' + self.state 

class SeatLayout(models.Model):
    layout_id = models.AutoField(primary_key=True)
    layout_title = models.CharField(max_length=100, null=True, blank=True)
    rows = models.IntegerField(null=True, blank=True)
    columns = models.IntegerField(null=True, blank=True)
    layout = models.TextField(null=True, blank=True)
    seat_type = models.CharField(max_length=50, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.layout_title + str(self.layout_id)

class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    bus_name = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=100, null=True, blank=True)

    seats1 = models.TextField(null=True, blank=True)
    seats2 = models.TextField(null=True, blank=True)
    seatsLeft= models.IntegerField(null=True, blank=True)
    
    location_from = models.CharField(max_length=100, null=True, blank=True)
    location_to = models.CharField(max_length=100, null=True, blank=True)
    
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 

    departure_stop = models.CharField(max_length=100, null=True, blank=True)
    arrival_stop = models.CharField(max_length=100, null=True, blank=True)

    first_timing = models.DateTimeField(null=True, blank=True)
    last_timing = models.DateTimeField(null=True, blank=True)

    lower_deck = models.CharField(max_length=20, null=True, blank=True)
    upper_deck = models.CharField(max_length=20, null=True, blank=True)

    boarding_points = models.TextField(null=True, blank=True)
    dropping_points = models.TextField(null=True, blank=True)

    seller_name = models.CharField(max_length=100, null=True, blank=True)
    seller_mobile = models.CharField(max_length=50, null=True, blank=True)

    bank_name = models.CharField(max_length=100, null=True, blank=True)
    holder_name = models.CharField(max_length=100, null=True, blank=True)
    ac_no = models.CharField(max_length=100, null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, null=True, blank=True)

    staff = models.TextField(null=True, blank=True)
    cancellation_available = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    
    reservedSeatsLower = models.TextField(null=True, blank=True)
    reservedSeatsUpper = models.TextField(null=True, blank=True)
    ticketsSold = models.IntegerField(default=0)
    paid_status = models.CharField(max_length=100,default='Not Paid')
    
    photo1 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo2 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo3 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo4 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo5 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo6 = models.FileField(upload_to=bus_image, null=True, blank=True)
    
    objects = models.Manager()

    def __str__(self):
      return str(self.bus_id) + ' ' + self.bus_name + ' ' + self.bus_type  
    
    def delete(self, *args, **kwargs):
            # first, delete the file
        self.photo1.delete(save=False)
        self.photo2.delete(save=False)
        self.photo3.delete(save=False)
        self.photo4.delete(save=False)
        self.photo5.delete(save=False)
        self.photo6.delete(save=False)

        super(Bus, self).delete(*args, **kwargs)

class BusPhoto(models.Model):
    bus_id = models.IntegerField(null=True, blank=True)
    photo1 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo2 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo3 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo4 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo5 = models.FileField(upload_to=bus_image, null=True, blank=True)
    photo6 = models.FileField(upload_to=bus_image, null=True, blank=True)

    
    def delete(self, *args, **kwargs):
        # first, delete the file
        self.photo1.delete(save=False)
        self.photo2.delete(save=False)
        self.photo3.delete(save=False)
        self.photo4.delete(save=False)
        self.photo5.delete(save=False)
        self.photo6.delete(save=False)

        super(BusPhoto, self).delete(*args, **kwargs)

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_url = models.CharField(max_length=150, null=True, blank=True)
    
    user_id = models.CharField(max_length=100, null=True, blank=True)

    bus_id = models.CharField(max_length=200, null=True, blank=True)

    name = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)

    lower_deck = models.TextField(null=True, blank=True)
    upper_deck = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 
    created_date = models.DateTimeField(auto_now_add=True)
    boarding_point = models.CharField(max_length=150, null=True, blank=True)
    dropping_point = models.CharField(max_length=150, null=True, blank=True)
    
    is_confirmed = models.BooleanField(default=False)
    cancellation_available = models.BooleanField(default=False)
    exhausted = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return str(self.ticket_id)

