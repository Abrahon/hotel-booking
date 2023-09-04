from django.shortcuts import render
# from .models import Hotel 

def home(request):
    # hostels = Hotel.objects.filter(is_available=True)
    
    # context = {'hostels': hostels}
    return render(request,'index.html')