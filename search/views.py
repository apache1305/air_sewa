from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import GetFlightSerializer
from air_admin.models import Flight

# Create your views here.
def flight_plan(request):
    # Request validations
    if request.method != 'GET':
        return JsonResponse({"msg": "{} method not allowed!!!".format(request.method)}, 
            status= status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = GetFlightSerializer(data= request.GET)
    if not serializer.is_valid():
        print("flight_plan failed for {} with error {}".format(request.GET, serializer.errors))
        return JsonResponse(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    # Find best possible routes
    possible_routes= []
    route= list(Flight.objects.all().values())
    if route:
        possible_routes.append(route)
    
    if not possible_routes:
        print("flight_plan unresolved for for {}".format(request.GET))    
    return JsonResponse(possible_routes, safe= False)