from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from common_utils import querydict_to_dict
from air_admin.models import Flight
from .serializers import FlightSerializer
from django.http import QueryDict
from django.db import IntegrityError

# Create your views here.
@csrf_exempt
def create_flight(request):
    # Validate payload
    if request.method != 'POST':
        return JsonResponse({"msg": "{} method not allowed!!!".format(request.method)}, 
            status= status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = FlightSerializer(data= request.POST)
    if not serializer.is_valid():
        print("create_flight failed for {} with -- {}".format(request.POST, serializer.errors))
        return JsonResponse(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    # Create new flight
    try:
        serializer.save()
    except IntegrityError as ie:
        if "UNIQUE" in str(ie):
            print("create_flight failed for {} with IntegrityError -- {}".format(request.POST, ie))
            return JsonResponse({"message": "Flight already exist"}, status= status.HTTP_406_NOT_ACCEPTABLE)
        print("create_flight failed for {} with IntegrityError -- {}".format(request.POST, ie))
        return JsonResponse({"message": "Somethign went wrong while creating flight"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as ex:
        print("create_flight failed for {} with -- {}".format(request.POST, ex))
        return JsonResponse({"message": "Somethign went wrong while creating flight"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JsonResponse(serializer.data, status= status.HTTP_201_CREATED)

@csrf_exempt
def update_flight(request, id):
    # Validate payload
    if request.method != 'PUT':
        return JsonResponse({"msg": "{} method not allowed!!!".format(request.method)}, 
            status= status.HTTP_405_METHOD_NOT_ALLOWED)
    request_data = querydict_to_dict(QueryDict(request.body))
    serializer = FlightSerializer(data= request_data)
    if not serializer.is_valid():
        print("update_flight failed for {} with -- {}".format(request_data, serializer.errors))
        return JsonResponse(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    # Find flight by id and update
    try:
        updates= Flight.objects.filter(id= id).update(**request_data)
    except IntegrityError as ie:
        if "UNIQUE" in str(ie):
            print("update_flight failed for {} with IntegrityError -- {}".format(request.POST, ie))
            return JsonResponse({"message": "Details match with another Flight, update failed"}, status= status.HTTP_406_NOT_ACCEPTABLE)
        print("update_flight failed for {} with IntegrityError -- {}".format(request.POST, ie))
        return JsonResponse({"message": "Somethign went wrong while creating flight"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as ex:
        print("update_flight failed for {} with -- {}".format(request.POST, ex))
        return JsonResponse({"message": "Somethign went wrong while updating flight"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if not updates:
        print("update_flight failed flight with id {} not found".format(id))
        return JsonResponse({"msg": "Flight with id {} not found".format(id)}, status= status.HTTP_404_NOT_FOUND)
    request_data['id'] = id
    
    return JsonResponse(request_data)

