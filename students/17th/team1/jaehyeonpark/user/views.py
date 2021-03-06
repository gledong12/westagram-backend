import json, bcrypt, jwt, re

from django.http      import JsonResponse
from django.views     import View
from django.db.utils  import DataError, IntegrityError
from django.db.models import Q

from user.models      import User
from my_settings      import SECRET_KEY
from westagram.utils  import login_decorator

PASSWORD_MINIMUM_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            phone_number = data['phone_number']
            account      = data['account']
            password     = data['password']

            if "" in (email, password):
                return JsonResponse({'message':'NO_VALUE_ERROR'}, status=400)
            
            email_regex = re.compile("^.+@+.+\.+.+$")
            
            if not email_regex.match(email):
                return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'EMAIL_EXISTS'}, status=400)

            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message':'PHONE_NUMBER_EXISTS'}, status=400)

            if User.objects.filter(account=account).exists():
                return JsonResponse({'message':'ACCOUNT_EXISTS'}, status=400)
            
            if len(password) < PASSWORD_MINIMUM_LENGTH:
                return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)
     
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            encrypted_password = hashed_password.decode('utf-8')
            
            User.objects.create(email=email, password=encrypted_password, phone_number=phone_number, account=account)

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({'message':'INTEGRITY_ERROR'}, status=400)        

class SignInView(View):
    @login_decorator
    def post(self, request, user):
        access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm='HS256')
        return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)
