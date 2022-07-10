from rest_framework import serializers
from air_admin.models import Flight

class GetFlightSerializer(serializers.ModelSerializer):    
    class Meta:
        model= Flight
        fields= ('departure_city', 'arrival_city', 'departure_time')
    