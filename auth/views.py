from rest_framework.views import APIView
from rest_framework.response import Response

from auth.models import User
from destination.models import City


class CreateUserView(APIView):

    def post(self, request):
        # Create User API
        # Recieves, username, email and password, city and country_code in parameters
        response = 200
        message = ''
        data = request.data
        if not data["username"] or data["username"] is None:
            response = 400
            message = "Username is missing"
        elif not data["email"] or data["email"] is None:
            response = 400
            message = "Email is missing"
        elif not data["password"] or data["password"] is None:
            response = 400
            message = "Password is missing"
        if response == 400:
            return Response({
                'response': {
                    'status': response,
                    'data': message,
                }
            }, status=response)
        city = City.nodes.first(name=data['city'], country_code=data['country_code'])
        user = User(username=data['username'],
                    email=data['email'],
                    password=data['password']).save()  # Create
        user.city.connect(city)
        return Response({
            'response': {
                'status': response,
                'data': {
                    'id': user.id,
                    'user_data': user.serialize,
                }
            }
        }, status=response)


class LoginUserView(APIView):

    def post(self, request):
        # Login User API
        # Receives, username and password and returns user_id in case of successful login
        response = 200
        message = ''
        try:
            user_id = None
            data = request.data
            if not data["username"] or data["username"] is None:
                response = 400
                message = "Username is missing"
            elif not data["password"] or data["password"] is None:
                response = 400
                message = "Password is missing"
            if response == 400:
                return Response({
                    'response': {
                        'status': response,
                        'data': message,
                    }
                }, status=response)

            user = User.nodes.get_or_none(username=data['username'])
            if user:
                password = data['password']  # Convert utf-8 for hashing
                # if hashlib.sha256(password).hexdigest() == user.password:
                if str(password) == user.password:
                    response = 200
                    message = 'Login Successfull'
                    user_id = user.id
                else:
                    response = 404
                    message = 'Password incorrect'
                    user_id = None
            else:
                response = 404
                message = 'User not found'
                user_id = None

            return Response({
                'response': {
                    'status': response,
                    'data': {
                        'message': message,
                        'user_id': user_id
                    }
                }
            }, status=404)
        except Exception as e:
            return Response({
                'response': {
                    'status': 500,
                    'data': {
                        'message': 'Error occured. Try again later',
                    }
                }
            }, status=500)


class UserDetailView(APIView):

    def get(self, request):
        # User Detail API
        # Recieves user_id and returns user details

        user_id = request.GET.get('user_id')
        if user_id:
            user = User.nodes.get_or_none(uid=user_id)
            return Response({
                'response': {
                    'status': 200,
                    'data': {
                        'user': user.serialize
                    }
                }
            }, status=200)
        return Response({
            'response': {
                'status': 404,
                'data': {
                    'user': None,
                    'message': 'User not found'
                }
            }
        }, status=404)


class AddUserFavouritesView(APIView):

    def post(self, request):
        # Add favourites in User profile API
        # Receives, destinations, experience and interests and add it into user profile

        try:
            response = 200
            message = ''
            data = request.data
            if not data["user_id"] or data["user_id"] is None:
                response = 400
                message = "user_id is missing"
            user = User.nodes.get_or_none(uid=data["user_id"])
            if user:
                if user.favourites:
                    favourites = user.favourites
                else:
                    favourites = {'destinations': [], 'experience': [], 'interests': []}
                if data["destinations"]:
                    favourites['destinations'].extend(data['destinations'])
                    favourites['destinations'] = list(dict.fromkeys(favourites['destinations']))
                if data["experience"]:
                    favourites['experience'].extend(data['experience'])
                    favourites['experience'] = list(dict.fromkeys(favourites['experience']))
                if data["interests"]:
                    favourites['interests'].extend(data['interests'])
                    favourites['interests'] = list(dict.fromkeys(favourites['interests']))
                user.favourites = favourites
                user.save()
                message = 'Favourites updated successfully'
            else:
                response = 404
                message = 'User not found'
            return Response({
                'response': {
                    'status': response,
                    'data': message,
                }
            }, status=response)
        except Exception as e:
            return Response({
                'response': {
                    'status': 500,
                    'data': 'Something went wrong. Try again later',
                }
            }, status=500)
