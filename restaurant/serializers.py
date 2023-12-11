from rest_framework import serializers
from .models import Menu, Booking, User, Menu

class menuSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Menu
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Menu
        fields = '__all__'


class bookSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Booking
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class BookingSerializer (serializers.ModelSerializer):
    class Meta: 
        model = Booking
        fields = '__all__'
