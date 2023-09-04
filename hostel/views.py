from django.shortcuts import render,redirect
from.models import Hotel,Review
from.forms import ReviewForm
from django.db.models import Q



def hostel(request):
    hostels = Hotel.objects.filter(is_available=True)
    # for item in hostels:
    #     print(hostels, item.hostel_name,item.price,item.is_available)
    
    context = {'hostels': hostels}
    return render(request, 'hostel.html', context)

def hostel_details(request,hostel_slug):
    single_room = Hotel.objects.get(slug = hostel_slug)# get single product k anar jonno// filter list product dibe
    
    # if request.user.is_authenticated:
    #     try:
    #         booking_hostel = BookingHostel.objects.filter(user=request.user, hostel_id=single_room.id).exists()
    #     except BookingHostel.DoesNotExist:
    #         booking_hostel = None
    # else:
    #     booking_hostel = None

    # Get the reviews
    reviews = Review.objects.filter(hostel_id=single_room.id, status=True)

    context = {
        'single_room': single_room,
        # 'booking_hostel': booking_hostel,
        'reviews': reviews,
        
    }
    return render(request, 'hostel_details.html', context)


 
    #  review funtionality

def submit_review(request, hostel_id):
    url = request.Meta.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(user__id = request.user.id, hostel__id = hostel_id)
            form = ReviewForm(request. POST,instance=reviews)
            form.save()
            message.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.hostel_id = hostel_id
                data.user_id = request.user.id
                data.save()
                message.success(request, 'Thank you! Your review has been submitted')
                return redirect(url)
        
            


       
# search funtionality
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    
    if keyword:
        hostels = Hotel.objects.order_by('-created_date').filter(Q(location__icontains = keyword) | Q(hostel_name__icontains = keyword ))
        print(hostels)
        
        hostel_count = hostels.count()
        context = {
            'hostels' :hostels,
            'h_count' : hostel_count,
        }
              
    return render(request, 'hostel.html',context)
