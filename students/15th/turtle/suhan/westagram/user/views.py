import json 
import bcrypt
import jwt
import re

from django.views import View
from django.http import JsonResponse

from .models import User
from westagram.settings import SECRET_KEY

# 회원가입
class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$') #이메일 정규식 사용.

            if not p.match(data['email']): 
                return JsonResponse({'MESSAGE':'EMAIL_ERROR!'}, status=400)

            if len(data['password']) < 8:
                 return JsonResponse({'MESSAGE':'PASSWORD_IS_SHORT!'}, status=400)

            if User.objects.filter(email=data['email']):                           
                return JsonResponse({'MESSAGE':'EMAIL_ALEADY_IN_USE'}, status=400)
            
            hash_password =  bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            hash_password = hash_password.decode('utf-8')
        
            User.objects.create(
                email = data['email'],
                password = hash_password,
            )
            return JsonResponse({'MESSAGE':'SUCCESS!'}, status=200)
        
        except KeyError:
            return JsonResponse({"message": "KEYERROR!"}, status=400)
 
 # 로그인 
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
                       
        try:

            user = User.objects.get(email=data['email'])

            if User.objects.filter(email=data['email']): # 이메일 존재
                    
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')): # 비밀번호 확인
                    secret       = SECRET_KEY
                    token        = jwt.encode({'id' : user.id}, secret, algorithm = 'HS256')
                    access_token = token.decode('utf-8')   
                    return JsonResponse({"access-token" : access_token}, status=200)
                
                else: #비밀번호가 틀린 경우
                    
                    return JsonResponse({'MESSAGE':'INVALID_USER!'}, status=401)

            if not User.objects.filter(email=data['email']):    # 이메일이 존재 하지 않는다.

                return JsonResponse({"message": "INVALID_USER"}, status=401)
           
        except KeyError:
            return JsonResponse({'MESSAGE':'INVALID_USER!'}, status=401)




