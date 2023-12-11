from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
# from rest_framework import serializers

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    no_of_guests=models.IntegerField(validators=[MaxValueValidator(limit_value=999999)])
    booking_date=models.DateField()

    
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    inventory=models.IntegerField(validators=[MaxValueValidator(limit_value=99999)])
    def __str__(self):
        return f'{self.title} : {str(self.price)}'
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()

    def get_item(self):
        return f'{self.title} : {str(self.price)}'