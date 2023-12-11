from . import views
from django.urls import path
from .views import bookingview
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    # path('', views.home, name="home"),
    # path('about/', views.about, name="about"),
    path('booking/', bookingview.as_view()),
    path('menu/',  views.MenuItemView.as_view()),
    path('menu_items/', views.MenuItemsView, name="menu_item"),
    path('menu_items/<int:pk>/', views.SingleMenuItemView, name="single_menu_item"),
    path('api-token-auth/', obtain_auth_token)

]