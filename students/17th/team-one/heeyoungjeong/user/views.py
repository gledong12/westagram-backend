import bcrypt
import my_settings
import json
import jwt
from json.decoder import JSONDecodeError
import re

from django.db.models import Q
from django.http      import JsonResponse, HttpResponse
from django.views     import View

from utils import login_decorator
from user.models import User
from user.models import Relationship


SECRET_KEY = my_settings.SECRET_KEY['secret']

EMAIL_REGULAR_EXPRESSION = re.compile('^[^-_.][a-zA-Z0-9-_.]*[a-zA-Z0-9]*[@][a-zA-Z0-9]+[.][a-zA-Z]{2,3}$')
PASSWORD_REGULAR_EXPRESSION = re.compile('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,16}$')

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            check_lst = ['email', 'password', 'name', 'user_name', 'phone_number']
            for key in check_lst:

                if key not in data.keys():
                    return JsonResponse({'message':'KEY_ERROR'}, status=400)

            for value in data.values():
                if not value:
                    return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if not EMAIL_REGULAR_EXPRESSION.search(data['email']):
                return JsonResponse({'message': 'INVAILD_EMAIL'}, status=400)

            if not PASSWORD_REGULAR_EXPRESSION.search(data['password']):
                return JsonResponse({'message': 'The password is not valid'}, status=400)

            user = User.objects.filter(email=data['email'])
            if not user:
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                decoded_hashed_password = hashed_password.decode('utf-8')
                try:
                    User.objects.create(
                        name       = data['name'],
                        user_name  = data['user_name'],
                        email        = data['email'],
                        password     = decoded_hashed_password,
                        phone_number = data['phone_number']
                    )
                    return JsonResponse({'message':'SUCCESS'}, status=200)
                except KeyError:
                    return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            return JsonResponse({'message':'USER_ALREADY_EXIST'}, status=409)

        except JSONDecodeError:
            return JsonResponse({'message':'The request is not valid'}, status=400)


class SignInView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            user_name    = data.get('user_name', None)
            email        = data.get('email', None)
            password     = data.get('password', None)
            phone_number = data.get('phone_number', None)

            if not (user_name or email or phone_number) and not password:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if User.objects.filter(Q(user_name=user_name) | Q(email=email) | Q(phone_number=phone_number)).exists():
                user = User.objects.get(Q(user_name=user_name) | Q(email=email) | Q(phone_number=phone_number))
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

                    encoded_jwt = jwt.encode({'user_id':user.id}, SECRET_KEY , algorithm='HS256')

                    return JsonResponse({'message': 'SUCCESS', 'ACCESS_TOKEN': encoded_jwt}, status=200)

                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)


class RelationShipView(View):
    @login_decorator
    def post(self, request, to_user_id):
        try:
            user = request.user

            from_user = User.objects.get(id=user.id)
            to_user = User.objects.get(id=to_user_id)

            if not Relationship.objects.filter(from_user=from_user, to_user=to_user).exists():
                relationship = Relationship(from_user=from_user, to_user=to_user)
                relationship.save()
                return JsonResponse({'message':'SUCCESS'}, status=200)

            return JsonResponse({'message':'INVALID_REQUEST'}, status=401)

        except User.DoNotExists:
            return JsonResponse({'message':'INVALID_USER'}, status=400)


class RelationShipUnfollowView(View):
    @login_decorator
    def post(self, request, to_user_id):
        try:
            user = request.user

            from_user = User.objects.get(id=user.id)
            to_user = User.objects.get(id=to_user_id)

            if not Relationship.objects.filter(from_user=from_user, to_user=to_user).exists():
                return JsonResponse({'message': 'INVALID_REQUEST'}, status=400)

            relationship = Relationship.objects.filter(from_user=from_user, to_user=to_user).delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except User.DoNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)

