from django . urls import path
from.import views

urlpatterns = [
    path('',views.booking, name='booking'),
    path('<int:hostel_id>/',views.add_booking, name='add_booking'),
    path('remove_booking/<int:hostel_id>/<int:booking_item_id>/', views.remove_booking, name='remove_booking'),
    path('remove_booking_item/<int:hostel_id>/<int:booking_item_id>/', views.remove_booking_item, name='remove_booking_item'),
    path('checkout/', views.checkout, name='checkout'),
    # path('payment/', views.checkout, name='payment'),
    # path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment/<int:booking_item_id>/', views.payment_page, name='payment_page'),

]
