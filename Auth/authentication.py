# In Auth/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from Auth.models import User
import jwt
import os
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        secret_key = os.environ.get('JWT_SECRET_KEY')
        
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            email = payload.get('email')
            user = User.objects.filter(email=email).first()
            
            if not user:
                raise AuthenticationFailed('User not found')
                
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')