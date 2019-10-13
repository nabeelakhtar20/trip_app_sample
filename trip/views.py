from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from auth.models import User
from trip.models import Trip


class CreateTripView(APIView):

    def post(self, request):
        # Create Trip API
        # Recieves destination, start_date, end_date, adults, infants, estimate_budget_start, estimate_budget_end,
        # user_id and events(json array) as parameter
        try:
            response = 200
            message = ''
            data = request.data
            if not data["destination"] or data["destination"] is None:
                response = 400
                message = "Destination is missing"
            elif not data["start_date"] or data["start_date"] is None:
                response = 400
                message = "Trip start date is missing"
            elif not data["end_date"] or data["end_date"] is None:
                response = 400
                message = "Trip end date is missing"
            elif not data["adults"] or data["adults"] is None:
                response = 400
                message = "Adults number is missing"
            elif not data["infants"] or data["infants"] is None:
                response = 400
                message = "Infants number is missing"
            elif not data["estimate_budget_start"] or data["estimate_budget_start"] is None:
                response = 400
                message = "Estimated budget start limit is missing"
            elif not data["estimate_budget_end"] or data["estimate_budget_end"] is None:
                response = 400
                message = "Estimated budget end limit is missing"
            elif not data["user_id"] or data["user_id"] is None:
                response = 400
                message = "User ID is missing"

            if response == 400:
                return Response({
                    'response': {
                        'status': response,
                        'data': message,
                    }
                }, status=response)

            user = User.nodes.get_or_none(uid=data["user_id"])

            trip = Trip(destination=data["destination"],
                        start_date=datetime.strptime(data["start_date"], '%Y-%m-%d').date(),
                        end_date=datetime.strptime(data["end_date"], '%Y-%m-%d').date(),
                        adults=data["adults"],
                        infants=data["infants"],
                        estimated_budget_start=data["estimate_budget_start"],
                        estimated_budget_end=data["estimate_budget_end"],
                        events=data["events"]).save()  # Create
            trip.user.connect(user)
            return Response({
                'response': {
                    'status': response,
                    'data': {
                        'id': trip.id,
                        'trip_data': trip.serialize,
                    }
                }
            }, status=response)
        except Exception as e:
            return Response({
                'response': {
                    'status': 500,
                    'data': {
                        'message': "Something went wrong. Try again later",
                    }
                }
            }, status=500)


class TripDetailView(APIView):

    def get(self, request):
        # Trip Details API
        # Receives trip_id and send trip details
        trip_id = request.GET.get('trip_id')
        if trip_id:
            trip = Trip.nodes.get_or_none(uid=trip_id)
            return Response({
                'response': {
                    'status': 200,
                    'data': {
                        'trip': trip.serialize
                    }
                }
            }, status=200)
        return Response({
            'response': {
                'status': 404,
                'data': {
                    'user': None,
                    'message': 'trip_id not found'
                }
            }
        }, status=404)


class UpdateTripView(APIView):

    def post(self, request):
        # Create Trip API
        # Recieves destination, start_date, end_date, adults, infants, estimate_budget_start, estimate_budget_end,
        # trip_id and events as parameter and update it into existing trip data
        try:
            response = 200
            message = ''
            data = request.data
            if not data["destination"] or data["destination"] is None:
                response = 400
                message = "Destination is missing"
            elif not data["start_date"] or data["start_date"] is None:
                response = 400
                message = "Trip start date is missing"
            elif not data["end_date"] or data["end_date"] is None:
                response = 400
                message = "Trip end date is missing"
            elif not data["adults"] or data["adults"] is None:
                response = 400
                message = "Adults number is missing"
            elif not data["infants"] or data["infants"] is None:
                response = 400
                message = "Infants number is missing"
            elif not data["estimate_budget_start"] or data["estimate_budget_start"] is None:
                response = 400
                message = "Estimated budget start limit is missing"
            elif not data["estimate_budget_end"] or data["estimate_budget_end"] is None:
                response = 400
                message = "Estimated budget end limit is missing"
            elif not data["trip_id"] or data["trip_id"] is None:
                response = 400
                message = "Trip ID is missing"

            if response == 400:
                return Response({
                    'response': {
                        'status': response,
                        'data': message,
                    }
                }, status=response)

            trip = Trip.nodes.get_or_none(uid=data["trip_id"])

            trip.destination = data["destination"]
            trip.start_date = datetime.strptime(data["start_date"], '%Y-%m-%d').date()
            trip.end_date = datetime.strptime(data["end_date"], '%Y-%m-%d').date()
            trip.adults = data["adults"]
            trip.infants = data["infants"]
            trip.estimated_budget_start = data["estimate_budget_start"]
            trip.estimated_budget_end = data["estimate_budget_end"]
            trip.events = data["events"]
            trip.save()

            return Response({
                'response': {
                    'status': response,
                    'data': {
                        'id': trip.id,
                        'trip_data': trip.serialize,
                    }
                }
            }, status=response)
        except Exception as e:
            return Response({
                'response': {
                    'status': 500,
                    'data': {
                        'message': "Something went wrong. Try again later",
                    }
                }
            }, status=500)
