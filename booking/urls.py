from django . urls import path
from.import views

urlpatterns = [
    path('',views.bookings, name='booking'),
    path('<int:hostel_id>/',views.add_to_booking, name='add_booking')
]
