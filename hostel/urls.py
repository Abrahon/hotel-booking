from django.urls import path
from . import views

urlpatterns = [
    path('',views.hostel,name = 'hostel'),
    path(' ', views.search, name = 'find'),
    path('<slug:hostel_slug>/',views.hostel_details, name = 'details'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    # path('',views.search, name = 'index'),
]
