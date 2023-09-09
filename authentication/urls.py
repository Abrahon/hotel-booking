from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.register,name ='register'),
    path('profile',views.profile,name ='profile'),
    path('login',views.user_login,name= 'login'),
    # path('forgot',views.forgot_password,name= 'forgot'),
    path('logout', views.user_logout, name = 'logout'),
    path('',views.user_dashboard, name ="dashboard"),
    
    
    path('my_book/', views.my_book, name='my_book'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # path('change_password/', views.change_password, name='book_password'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail')
]
