from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def create_flight(request):
    if request.method != 'POST':
        return JsonResponse({"msg": "{} method not allowed!!!".format(request.method)}, 
            status= status.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse({"msg": "Add Flight"})

@csrf_exempt
def update_flight(request, id):
    if request.method != 'PUT':
        return JsonResponse({"msg": "{} method not allowed!!!".format(request.method)}, 
            status= status.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse({"msg": "Update Flight"})

