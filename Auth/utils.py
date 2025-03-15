from django.core.mail import send_mail
from django.conf import settings
import jwt
import datetime
from dotenv import load_dotenv
import os
load_dotenv()



def send_otp_via_mail(email,otp):
    subject = "OTP for verification"
    message = f"Your verification OTP is {otp}"
    from_email = settings.EMAIL_HOST
    try:
        send_mail(subject,message,from_email,[email])
    
    except Exception as e:
        raise e
    
def generate_jwt_token(email):
    try:
        
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=24.0)
        payload = {
            "email" : email,
            "exp": expiration,
            "iat":datetime.datetime.utcnow()
        }
        
        secret_key = os.environ.get('JWT_SECRET_KEY')
        print(f"Secret Key: {secret_key}")  # Debugging


        token = jwt.encode(payload , secret_key , algorithm='HS256')
        

        return token
    except Exception as e:
        print(f"Error while generating JWT toke: {e}")
        return None
    