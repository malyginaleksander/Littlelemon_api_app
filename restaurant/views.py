from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Menu, Booking
from .serializers import bookSerializer, menuSerializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework import generics
from .serializers import MenuItemSerializer, BookingSerializer 
# Create your views here.
# def menu(request):
#     menu_data = Menu.objects.all()
#     main_data = {'menu': menu_data}
#     return render(request, 'menu.html', {"menu": main_data})

def index(request):
    return render(request, 'index.html', {})


class bookingview(APIView):
    def get(self, request):
        items = Booking.objects.all()
        serializer = bookSerializer(items, many=True)
        return Response(serializer.data) # Return JSON


# class MenuItemView(generics.ListCreateAPIView):
class MenuItemView(APIView):
    def get(self, request):
        items = Menu.objects.all()  # Replace with your queryset
        serializer = menuSerializers(items, many=True)# Replace with your serializer class
        return Response(serializer.data) # Return JSON

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request):
        items = Menu.objects.all()  # Replace with your queryset
        serializer = menuSerializers(items, many=True)
        return Response(serializer.data) # Return JSON


class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer(queryset, many=True)

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer(queryset, many=True)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer