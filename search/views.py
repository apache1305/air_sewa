from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import copy
from datetime import datetime
from pprint import pprint
from .serializers import GetFlightSerializer
from air_admin.models import Flight
from .models import SearchConfig

# Create your views here.
def flight_plan(request):
    # Request validations
    if request.method != 'GET':
        return JsonResponse({"data": [], "msg": "{} method not allowed!!!".format(request.method)}, 
            status= status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = GetFlightSerializer(data= request.GET)
    if not serializer.is_valid():
        print("flight_plan failed for {} with error -- {}".format(request.GET, serializer.errors))
        return JsonResponse({"data": [], "msg": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
    # Find best possible routes
    departure_city= serializer.data['departure_city']
    arrival_city = serializer.data['arrival_city']
    departure_time= serializer.data['departure_time']

    print("=========================================================================================")
    print("Fetching flight_plan from | {} | to | {} | for {} ({})".format(departure_city, arrival_city, read_time(departure_time), departure_time))
    print("=========================================================================================")

    possible_routes= get_all_possible_routes(departure_city, arrival_city, departure_time)
    
    # Recommend routes with minimum flight switches i.e minimum route length
    possible_routes= sorted(possible_routes, key= (lambda route: len(route)))  
    print("Total flight_plans from {} to {} = {}".format(departure_city, arrival_city, len(possible_routes))) 
    return JsonResponse({"data": possible_routes, "msg": ""})

def get_all_possible_routes(departure_city, arrival_city, departure_time):
    # Get maxium number of flight changes allowed from Database - Search Configuration table
    max_flight_changes_allowed= int(SearchConfig.objects.get_or_create(
        config_name= 'max_flight_changes_allowed', defaults= {'config_value': 3})[0].config_value)
    # Get minimum time(in ms) required to switch flight
    flight_switch_time= int(SearchConfig.objects.get_or_create(
        config_name= 'flight_switch_time', defaults= {'config_value': 3600000})[0].config_value)
    # Get maximum waiting time(in ms) between flights, including switch time
    max_time_between_flights= int(SearchConfig.objects.get_or_create(
        config_name= 'max_time_between_flights', defaults= {'config_value': 7200000})[0].config_value)
    possible_routes= []
    current_route = []
    visited_airports = {}
    #print("possible routes = {}".format(len(possible_routes)))
    # ToDo : Use BFS instead of DFS
    search_feasible_flights(possible_routes, departure_city, arrival_city, int(departure_time),
        flight_switch_time, max_time_between_flights, max_flight_changes_allowed, current_route, visited_airports)  
    return possible_routes

def search_feasible_flights(possible_routes, departure_city, destination, arrival_time, flight_switch_time, max_wait_time, 
    flights_remaining, current_route, visited_airports, first_flight= True):
    #print("flights_remaining = {}".format(flights_remaining))
    #print("current_route = {}".format(current_route))
    if flights_remaining < 1:
        return
    flights_departure_time_after = arrival_time
    if not first_flight:
        flights_departure_time_after = arrival_time + flight_switch_time
    available_flights= get_available_flights(departure_city, flights_departure_time_after, arrival_time + max_wait_time)
    for flight in available_flights:
        if flight['arrival_city'] == destination:
            current_route.append(flight)
            print("Found destination {} with route of length = {}".format(destination, len(current_route)))
            display_route(current_route)
            possible_routes.append(copy.deepcopy(current_route))
            current_route.pop()
            continue
        if flight['id'] in visited_airports:
            continue
        visited_airports[flight['id']] = flight['departure_city']
        current_route.append(flight)
        search_feasible_flights(possible_routes, flight['arrival_city'], destination, int(flight['arrival_time']),
            flight_switch_time, max_wait_time, flights_remaining - 1, current_route, visited_airports, False)
        current_route.pop()

def get_available_flights(departure_city, min_departure_time, max_departure_time):
    flights = Flight.objects.filter(
        departure_city= departure_city,
        departure_time__gte= min_departure_time,
        departure_time__lte= max_departure_time,
        ).values()
    print("Flights from {} between {} and {} = {}".format(
        departure_city, read_time(min_departure_time), read_time(max_departure_time), [flight['id'] for flight in flights]
    ))
    return flights

def display_route(current_route):
    print("ROUTE START :")
    pprint(["{} @ {} -> {} @ {}".format(
        airport['departure_city'], read_time(airport['departure_time']), airport['arrival_city'], read_time(airport['arrival_time'])) for airport in current_route])
    print(": ROUTE END")

def read_time(timestamp):
    return "{}".format(datetime.utcfromtimestamp(int(str(timestamp)[:10])).strftime('%Y-%m-%d %H:%M:%S'))