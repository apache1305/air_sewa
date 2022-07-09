from django.urls import path
from . import views

urlpatterns = [
    path('create-flight/', views.create_flight, name='create_flight'),
    path('update-flight/<id>/', views.update_flight, name='update_flight')
]
