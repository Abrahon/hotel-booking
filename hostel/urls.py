
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hostel, name='hostel'),  # /hostel/
    # path('details/<int:id>/', views.hostel_details, name='details')

    path('search/', views.search, name='find'),  # /hostel/search/
    path('<int:hostel_slug>/', views.hostel_details, name='hostel_details'),  # /hostel/11/
    path('submit_review/<int:hostel_id>/', views.submit_review, name='submit_review'),
    
    path('delete_review/<int:id>/', views.delete_review, name='delete_review'),

]

