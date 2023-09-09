from django.shortcuts import render,redirect
from.forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from booking.models import Booking,BookingItem
from booking.views import _booking_id
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.views import password_reset

# Create your views here.

def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect('hostel')
            # print(form.cleaned_data.get('first_name'))
    return render(request,'register.html',{'form': form})


# @login_required(login_url = 'login')
def profile(request):
    return render(request, 'dashboard.html')

def user_login(request):
    if request.method =='POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = user_name, password = password)
        print(user)
        
        #login akhno hoy nai
        session_key = get_create_session(request)
        booking = Booking.objects.get(booking_id = session_key)
        is_booking_item_exists= BookingItem.objects.filter(booking = booking).exists()
        if user is not None:
            try:
                booking = Booking.objects.get(booking_id=_booking_id(request))
                is_booking_item_exists = BookingItem.objects.filter(booking=booking).exists()
                if is_booking_item_exists:
                    booking_item = BookingItem.objects.filter(booking=booking)
                    for item in booking_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    #  return redirect('profile')
    return render(request,'signin.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url = 'login')
def user_dashboard(request):
    orders = Book.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        userprofile = UserProfile.objects.create(user=request.user)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    # return render(request, 'accounts/dashboard.html', context)
    return render(request, 'dashboard.html',context)

    
@login_required(login_url='login')
def my_book(request):
    books = Book.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'books': books,
    }
    return render(request, 'my_bookings.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'edit_profile.html', context)




@login_required(login_url='login')
def book_detail(request, order_id):
    order_detail = BookHostel.objects.filter(order__order_number=order_id)
    book = Book.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'book_detail': order_detail,
        'book': book,
        'subtotal': subtotal,
    }
    return render(request, 'booking_detail.html', context)