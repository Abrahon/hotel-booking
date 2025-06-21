from django.shortcuts import render
from hostel.models import Hotel, Review

def home(request):
    hostels = Hotel.objects.all().filter(is_available=True).order_by('created_date')[:8]

    # Get the reviews
    context = {
        'hostels': hostels,
       
    }
    return render(request, 'index.html', context)