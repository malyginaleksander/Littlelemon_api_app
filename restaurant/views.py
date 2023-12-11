from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Menu, Booking, MenuItem
from .serializers import bookSerializer, menuSerializers
from rest_framework import generics
from .serializers import MenuItemSerializer, BookingSerializer 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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