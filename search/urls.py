from django.urls import path
from . import views

urlpatterns = [
    path('flight-plan/', views.flight_plan, name='flight_plan')
]
