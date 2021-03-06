import json
import bcrypt
import jwt
import my_settings

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import Account

MINIMUM_PASSWORD_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try : 
            # 이메일에 '@' , '.' 여부 확인 
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            # Password length Check
            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status=400)
        
            # Email 중복 확인 
            if Account.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXISTS'}, status=409)

            if Account.objects.filter(phone=data['phone']).exists():
                return JsonResponse({'message':'PHONE_NUMBER_ALREADY_EXISTS'}, status=409)

            if Account.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({'message':'NICKNAME_ALREADY_EXISTS'}, status=409)

            hash_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            Account.objects.create(
                    email     = data['email'],
                    name      = data['name'],
                    nickname  = data['nickname'],
                    password  = hash_pw,
                    phone     = data['phone']
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try :
            email    = data.get('email')
            phone    = data.get('phone')
            password = data.get('password')

            if Account.objects.filter(Q(email=email) | Q(phone=phone)).exists():
                account = Account.objects.get(Q(email=email) | Q(phone=phone))

                if bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
                    token = jwt.encode({'email' : email}, my_settings.SECRET['secret'], algorithm = 'HS256')
                    print(token)
                    return JsonResponse({'message' : 'SUCCESS'}, status=200)

                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError: 
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

