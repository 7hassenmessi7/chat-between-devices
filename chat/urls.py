from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('books/', views.book_list, name='book_list'),
    path('upload_book/', views.upload_book, name='upload_book'),
    path('books/<int:pk>/', views.delete_book, name='delete_book'),


    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),



    path('',views.main,name='main'),
    path('user/',views.userPage,name="user-page"),
    path('index/', views.index,name='index'),
    path('products/', views.products,name='products'),
    
   
    
    path('customer/<str:pk_test>/',views.customer,name='customer'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    

    path( 'index/<str:room_name>/', views.room, name='room'),
    
    path('home/', views.home, name='home'),
    

]