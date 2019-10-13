from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^city[/]?$', GetCityNodes.as_view(), name='get_all_cities'),
    url(r'^explore_city[/]?$', FavouriteCitiesDataView.as_view(), name='explore_city'),
]