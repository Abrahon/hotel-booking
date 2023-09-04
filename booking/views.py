from django.shortcuts import render

# Create your views here.

def bookings(request):
    return render(request,'booking_store.html')