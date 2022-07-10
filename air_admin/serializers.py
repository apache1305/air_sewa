from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    departure_time = serializers.CharField(min_length= 13, max_length= 13)
    arrival_time = serializers.CharField(min_length= 13, max_length= 13)
    
    class Meta:
        model= Flight
        fields= '__all__'
    
    def validate(self, data):
        if data['arrival_time'] <= data['departure_time']:
            raise serializers.ValidationError("arrival_time cannot be less than or equal to departure_time")
        return data
