from django.db import models

# Create your models here.
class Flight(models.Model):
    number= models.CharField(max_length= 64)
    departure_city= models.CharField(max_length= 128, db_index= True)
    departure_time= models.CharField(max_length= 13, db_index= True)    # JS timestamp of order milliseconds; 13 digits
    arrival_city= models.CharField(max_length= 128, db_index= True)
    arrival_time= models.CharField(max_length= 13)  # JS timestamp of order milliseconds; 13 digits

    class Meta:
        constraints= [
            models.UniqueConstraint(fields= ('number', 'departure_city', 'departure_time'), name= "UNIQUE_FLIGHT")
        ]
        indexes= [
            models.Index(fields= ('departure_city', 'departure_time'))
        ]

    def __str__(self):
        return "{:<16} {:<16} {:<13} {:<16} {:<13}".format(self.number, self.departure_city, self.departure_time, self.arrival_city, self.arrival_time)