from . import views
from django.urls import path
from .views import bookingview

urlpatterns=[
    # path('', views.home, name="home"),
    # path('about/', views.about, name="about"),
    path('booking/', bookingview.as_view()),
    path('menu/',  views.MenuItemView.as_view()),
    path('menu_item/<int:pk>/', views.SingleMenuItemView.as_view),
    # path('', views.index, name='index')

]