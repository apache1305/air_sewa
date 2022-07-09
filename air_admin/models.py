from django.db import models

# Create your models here.
class Flight(models.Model):
    number= models.CharField(unique= True, max_length= 64)
    departure_city= models.CharField(max_length= 128)
    departure_time= models.DateTimeField()
    arrival_city= models.CharField(max_length= 128)
    arrival_time= models.DateTimeField()