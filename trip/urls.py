from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create_trip[/]?$', CreateTripView.as_view(), name='create_trip'),
    url(r'^detail[/]?$', TripDetailView.as_view(), name='trip_detail'),
    url(r'^update_trip[/]?$', UpdateTripView.as_view(), name='update_trip'),
]