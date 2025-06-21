from django.shortcuts import render, redirect, get_object_or_404
from hostel.models import Hotel
from .models import Booking, BookingItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
 
# Create your views here.
from django.http import HttpResponse

 
def _booking_id(request):
    booking = request.session.session_key
    if not booking:
        booking = request.session.create()
    return booking
 
@login_required(login_url='login')
def add_booking(request, hostel_id):
    current_user = request.user
    hostel = Hotel.objects.get(id=hostel_id)  # get the hostel
    # If the user is authenticated
    if current_user.is_authenticated:
        is_booking_item_exists = BookingItem.objects.filter(
            hostel=hostel, user=current_user).exists()
        if is_booking_item_exists:
            booking_items = BookingItem.objects.filter(
                hostel=hostel, user=current_user)
            print(booking_items)
            item = BookingItem.objects.get(hostel=hostel, user=current_user)
            item.quantity += 1
            item.save()
 
        else:
            try:
                # get the booking using the booking_id present in the session
                booking = Booking.objects.get(booking_id=_booking_id(request))
            except Booking.DoesNotExist:
                booking = Booking.objects.create(
                    booking_id=_booking_id(request)
                )
            booking.save()
            booking_item = BookingItem.objects.create(
                hostel=hostel,
                quantity=1,
                booking=booking,
                user=current_user
            )
            booking_item.save()
        return redirect('booking')
    else:
        hostel = Hotel.objects.get(id=hostel_id)
        try:
            # get the booking using the booking_id present in the session
            booking = Booking.objects.get(booking_id=_booking_id(request))
        except Booking.DoesNotExist:
            booking = Booking.objects.create(
                booking_id=_booking_id(request)
            )
            booking.save()
 
        try:
            booking_item = BookingItem.objects.get(hostel=hostel, booking=booking)
            booking_item.quantity += 1
            booking_item.save()
        except BookingItem.DoesNotExist:
            booking_item = BookingItem.objects.create(
                hostel=hostel,
                quantity=1,
                booking=booking,
            )
            booking.save()
    return redirect('booking')
 
 
def remove_booking(request, hostel_id, booking_item_id):
 
    hostel = get_object_or_404(Hotel, id=hostel_id)
    try:
        if request.user.is_authenticated:
            booking_item = BookingItem.objects.get(
                hostel=hostel, user=request.user, id=booking_item_id)
        else:
            booking = Booking.objects.get(booking_id=_booking_id(request))
            booking_item = BookingItem.objects.get(
                hostel=hostel, booking=booking, id=booking_item_id)
        if booking_item.quantity > 1:
            booking_item.quantity -= 1
            booking_item.save()
        else:
            booking_item.delete()
    except:
        pass
    return redirect('booking')
 
 
def remove_booking_item(request, hostel_id, booking_item_id):
    hostel = get_object_or_404(Hotel,pk=hostel_id)
    if request.user.is_authenticated:
        booking_item = BookingItem.objects.get(
            hostel=hostel, user=request.user, id=booking_item_id)
    else:
        booking = Booking.objects.get(booking_id=_booking_id(request))
        booking_item = BookingItem.objects.get(
            hostel=hostel, booking=booking, id=booking_item_id)
    booking_item.delete()
    return redirect('booking')
 
@login_required(login_url='login')
def booking(request, total=0, quantity=0, booking_items=None):
    try:
       
        if request.user.is_authenticated:
            booking_items = BookingItem.objects.filter(
                user=request.user, is_active=True)
        else:
            booking = Booking.objects.get(booking_id=_booking_id(request))
            booking_items = BookingItem.objects.filter(booking=booking, is_active=True)
        for booking_item in booking_items:
            total += (booking_item.hostel.price * booking_item.quantity)
            quantity += booking_item.quantity
        
    except ObjectDoesNotExist:
        pass  # just ignore
 
    context = {
        'total': total,
        'quantity': quantity,
        'booking_items': booking_items,
        
    }
    return render(request, 'booking_store.html', context)
 
 
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, booking_items=None):
    print(request.POST)
    try:
       
        if request.user.is_authenticated:
            booking_items = BookingItem.objects.filter(
                user=request.user, is_active=True)
        else:
            booking = Booking.objects.get(booking_id=_booking_id(request))
            booking_items = BookingItem.objects.filter(booking=booking, is_active=True)
        for booking_item in booking_items:
            total += (booking_item.hostel.price * booking_item.quantity)
            quantity += booking_item.quantity
       
    except ObjectDoesNotExist:
        pass  # just ignore
 
    context = {
        'total': total,
        'quantity': quantity,
        'booking_items': booking_items,
        
    }
    return render(request, 'dashboard.html', context)



@login_required
def payment_page(request, booking_item_id):
    booking_item = get_object_or_404(BookingItem, id=booking_item_id, user=request.user)

    if request.method == 'POST':
        booking_item.is_paid = True
        booking_item.save()

        # Optionally mark the whole booking as paid if all items are paid
        booking = booking_item.booking
        all_paid = booking.bookingitem_set.filter(is_paid=False).count() == 0
        if all_paid:
            booking.is_paid = True
            booking.save()

        return redirect('booking')  # Or 'my_bookings' if you have that

    return render(request, 'payment.html', {'booking': booking_item})

