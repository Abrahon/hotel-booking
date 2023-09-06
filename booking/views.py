from django.shortcuts import render,redirect
from hostel.models import Hotel
from booking.models import Booking,BookingItem

# Create your views here.



def bookings(request):
    return render(request,'booking_store.html')

def add_to_booking(request, hostel_id):
    hostel = Hotel.objects.get(id = hostel_id)
    print('add to booking',hostel)
    session_id = request.session.session_key
    booking_id = Booking.objects.filter(booking_id = session_id).exists()
    if booking_id:
        booking_item = BookingItem.objects.filter(hostel = hostel).exists()
        
        if booking_item:
            item = BookingItem.objects.get(hostel=hostel)
            item.quantity +=1
            item.save()
           
         
        else:
            bookingId = Booking.objects.get(booking_id = session_id)
            item = BookingItem.objects.create(
                
                hostel = hostel,
                quantity = 1,
                booking = booking
            )
            item.save()
            
        
    else:
        booking = Booking.objects.create(
        booking_id = session_id
    )
   
    booking.save()
    return redirect('booking')