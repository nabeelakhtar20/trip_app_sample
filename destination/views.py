import requests
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from auth.models import User
from trip_app_sample.utils import fetch_nodes

APIKEY = settings.GOOGLE_MAP_PLACE_API_KEY


class GetCityNodes(APIView):

    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('t', 'City'),
            'name': request.GET.get('q', ''),
            'country': request.GET.get('c', ''),
            'jurisdiction': request.GET.get('j', ''),
            'sourceID': request.GET.get('s', ''),
            'limit': 10,
            'page': int(request.GET.get('p', 1)),
        }
        nodes = fetch_nodes(fetch_info)
        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)


class FavouriteCitiesDataView(APIView):

    def get(self, request):
        # Get Favourite Cities Data for explorer page
        # This API works for multiple attributes
        # It receives city_name, user_id, interest and pageToken as parameter

        response_code = 200
        message = 'Success'
        city_name = request.GET.get('city_name', None)
        user_id = request.GET.get('user_id', None)
        pagetoken = request.GET.get('pagetoken', None)
        interest_name = request.GET.get('interest', None)
        data = {}
        # If city_name and user_id is provided then get all the places of interests provided by user in given city
        if city_name and user_id and not interest_name and not pagetoken:
            user = User.nodes.get_or_none(uid=user_id)
            data[city_name] = {}
            for interest in user.favourites['interests']:
                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={interest}+in+{city}&key={APIKEY}".format(
                    interest=interest, city=city_name, APIKEY=APIKEY)
                response = requests.get(url)
                res = json.loads(response.text)
                data[city_name][interest] = res
            response_code = 200
        # If city_name and interest is provided then get all the places of provided interest in that city
        elif city_name and interest_name and not pagetoken:
            data[city_name] = {}
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={interest}+in+{city}&key={APIKEY}".format(
                interest=interest_name, city=city_name, APIKEY=APIKEY)
            response = requests.get(url)
            res = json.loads(response.text)
            data[city_name][interest_name] = res
            response_code = 200
        # If pageToken is provided then it means that more data is fetching doesn't matter for which attributes because
        # Google take care of it automatically
        elif pagetoken:
            data[city_name] = {}
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={pagetoken}&key={APIKEY}".format(
                pagetoken=pagetoken, APIKEY=APIKEY)
            response = requests.get(url)
            res = json.loads(response.text)
            data[city_name][interest_name] = res
            response_code = 200
        else:
            # If only user_id is provided then fetch all cities and interests from DB of that user and send result according to that
            if user_id:
                user = User.nodes.get_or_none(uid=user_id)
                if len(user.favourites['destinations']) > 0:
                    for city in user.favourites['destinations']:
                        data[city] = {}
                        for interest in user.favourites['interests']:
                            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={interest}+in+{city}&key={APIKEY}".format(
                                interest=interest, city=city, APIKEY=APIKEY)
                            response = requests.get(url)
                            res = json.loads(response.text)
                            data[city][interest] = res
                response_code = 200
            else:
                response_code = 404
                message = 'User ID not found'

        return Response({
            'response': {
                'status': response_code,
                'message': message,
                'data': data
            }
        }, status=response_code)
