import jwt
from django.utils.timezone import now
from django.conf import settings
from Auth.models import User  # Import your custom User model
from dotenv import load_dotenv
import os
load_dotenv()


class LastLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            secret_key = os.environ.get('JWT_SECRET_KEY')
            

            try:
                print("trying")
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                print(f"got the pay load {payload}")
                email = payload.get('email')
                print(f"got the email {email}")
                user = User.objects.filter(email=email).first()
                
                
                if user:
                    request.user = user  # Manually set user
                    user.last_login = now()
                    user.save(update_fields=['last_login'])
                    print(f"Middleware executed: Last login updated for {user.email} and {user.last_login}")

            except jwt.ExpiredSignatureError:
                print("JWT expired")
            except jwt.DecodeError:
                print("Invalid JWT")
            except Exception as e:
                print(f"JWT Error: {e}")

        response = self.get_response(request)
        return response
