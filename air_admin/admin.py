from django.contrib import admin
from .models import Flight

# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    list_display= ('id', 'number', 'departure_city', 'departure_time', 'arrival_city', 'arrival_time',)
    search_fields= ('number', 'departure_city', 'arrival_city',)

admin.site.register(Flight, FlightAdmin)
