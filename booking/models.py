from django.db import models
from hostel.models import Hotel
from django.contrib.auth.models import User
# Create your models here.

class Booking(models.Model):
    booking_id = models.CharField(max_length=300, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.booking_id
    

class BookingItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hostel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null = True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.hostel.price * self.quantity
    
    def __str__(self):
        return str(self.hostel)

    
