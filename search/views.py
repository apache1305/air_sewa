from django.http import JsonResponse
from rest_framework import status

# Create your views here.
def flight_plan(request):
    if request.method != 'GET':
        return JsonResponse({"msg": "{} method not allowed!!!".format(request.method)}, 
            status= status.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse({"msg": "Flight Plan"})