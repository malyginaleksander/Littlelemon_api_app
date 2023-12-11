from . import views
from django.urls import path
from .views import bookingview
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('bookings/', bookingview.as_view(), name='bookings'),
    path('menu/', views.menu, name="menu"),
    # path('menu/',  views.MenuItemView.as_view()),
    path('menu_items/', views.MenuItemsView, name="menu_item"),
    path('menu_items/<int:pk>/', views.SingleMenuItemView, name="menu_item"),
    path('api-token-auth/', obtain_auth_token),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path('register/', views.register, name="register"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    # path('bookings/', views.bookings, name='bookings'), 

]