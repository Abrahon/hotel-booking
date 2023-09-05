from django.shortcuts import render,redirect
from.forms import RegistrationForm
from django.contrib.auth import login,logout,authenticate

# Create your views here.
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


def profile(request):
    return render(request, 'dashboard.html')

def user_login(request):
    if request.method =='POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = user_name, password = password)
        print(user)
        login(request, user)
        return redirect('profile')
    return render(request,'signin.html')

def user_logout(request):
    logout(request)
    return redirect('login')


def user_dashboard(request):
    return render(request, 'dashboard.html')
    