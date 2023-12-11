import json
from multiprocessing import AuthenticationError
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Menu, Booking, MenuItem
from .forms import BookingForm
from .serializers import bookSerializer, menuSerializers, BookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from rest_framework.permissions import IsAuthenticated, AllowAny

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index.html', {})

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

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

# class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
#     def get(self, request):
#         items = Menu.objects.all()  # Replace with your queryset
#         serializer = menuSerializers(items, many=True)
#         return Response(serializer.data) # Return JSON


# class MenuItemsView(generics.ListCreateAPIView)
#    permission_classes = [IsAuthenticated]
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer(queryset, many=True)

# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = Menu.objects.all()
#     serializer_class = MenuItemSerializer(queryset, many=True)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
# def securedview(request):
#     return Response({'message': "needs authentication"})
def SingleMenuItemView(request,pk):
    try:
        menu_item = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response({'message': 'Item not found'}, status=404)

    if request.method == 'GET':
        serializer = menuSerializers(menu_item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = menuSerializers(menu_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Menu item updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        menu_item.delete()
        return Response({'message': 'Menu Item Deleted Successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def MenuItemsView(request):
    if request.method == 'GET':
        menu_items = Menu.objects.all()
        serializer = menuSerializers(menu_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'error':'You do not have the authorization to perform this action.'},status=status.HTTP_403_FORBIDDEN)
        
        serializer=menuSerializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Menu items added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data=json.load(request)
        exist = Booking.objects.filter(booking_date=data['booking_date']).exists()
        if exist==False:
            booking = Booking(
                name=data['name'],
                no_of_guests=data['no_of_guests'],
                booking_date=data['booking_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(booking_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json') 

@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated]) 
def single_booking(request,pk):
    try:
        booking_item = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response({'message': 'Item not found'}, status=404)

    if request.method == 'GET':
        serializer = BookingSerializer(booking_item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookingSerializer(booking_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        booking_item.delete()
        return Response({'message': 'Booking Deleted Successfully.'}, status=status.HTTP_200_OK)
    
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationError(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

@api_view(['GET','POST'])
@permission_classes([AllowAny]) 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})