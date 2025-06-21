from django.shortcuts import render,redirect
from.models import Hotel,Review
# from django.contrib.comments.models import Comment
from.forms import ReviewForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import the login_required decorator



def hostel(request):
    hostels = Hotel.objects.filter(is_available=True)
    # for item in hostels:
    #     print(hostels, item.hostel_name,item.price,item.is_available)
    
    context = {'hostels': hostels}
    return render(request, 'hostel.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Hotel, Review

def hostel_details(request, hostel_slug):  # better renamed to hostel_id
    single_room = get_object_or_404(Hotel, id=hostel_slug)

    reviews = Review.objects.filter(hostel_id=single_room.id, status=True)
    related_rooms = Hotel.objects.filter(
        location=single_room.location,
        is_available=True
    ).exclude(id=single_room.id)[:3]

    context = {
        'single_room': single_room,
        'reviews': reviews,
        'related_rooms': related_rooms,
    }
    return render(request, 'hostel_details.html', context)

    #  review funtionality


@login_required  # Ensure that the user is logged in before accessing this view
def submit_review(request, hostel_id):
    url = request.META.get('HTTP_REFERER')
 
    if request.method == 'POST':
        try:
            # Assuming your Review model has a ForeignKey to User called 'user'
            reviews = Review.objects.get(hostel__id=hostel_id, user=request.user)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.hostel_id = hostel_id
                data.user = request.user  # Assign the logged-in user to the review
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted')
 
        return redirect(url)
 
    return HttpResponse("Invalid request method")


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Review  # or adjust import

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Review

def delete_review(request, id):
    review = get_object_or_404(Review, pk=id)

    if request.user == review.user:
        hostel_id = review.hostel.id  # Correct relation to Hotel
        review.delete()
        messages.success(request, 'You have successfully deleted the review.')
        return redirect('hostel_details', hostel_slug=hostel_id)
  
    else:
        messages.error(request, 'You are not authorized to delete this review.')
        return redirect('hostel_details', hostel_slug=hostel_id)



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


