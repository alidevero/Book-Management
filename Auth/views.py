from django.shortcuts import render
from .models import *
from rest_framework.views import APIView , Response
from .serializers import *
from .utils import send_otp_via_mail , generate_jwt_token
import random
from django.core.cache import cache
from Auth.authentication import *
from django.contrib.auth.hashers import make_password
from rest_framework import status, permissions
# Create your views here.

class SignupUser(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSignupSerializer(data=data)
            if serializer.is_valid():
                otp = random.randint(1000,9999)
                email = serializer.validated_data.get("email")
                username = serializer.validated_data.get("username")
                password = serializer.validated_data.get("password")
                is_verified = serializer.validated_data.get("is_verified")
                payload = {
                    "email" :email,
                    "username" : username,
                    "password" : password,
                    "otp" : otp,
                    "is_verified": is_verified
                }
                send_otp_via_mail(email , otp)
                cache_key = f"email_otp{email}"
                cache.set(cache_key,payload,timeout=600)#save otp in cache for 10 mints
                return Response({"message" : "Check your email you have recived OTP","data":serializer.data})
            return Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong", "error": str(e)},
                status=500
            )
            
        
        except Exception as e:
            print(e)


class UserLogin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self , request):
        try:
            data = request.data
            serializer = UserLoginSerializer(data= data)
            if serializer.is_valid():
                email = serializer.validated_data.get("email")
                token = generate_jwt_token(email)
                return Response({
                    "success":True,
                    "message":"LogedIn successfully",
                    "token":token
                })
            return Response({
                "message":"Something went wrong",
                "error" : serializer.errors
            })
        
        except Exception as e:
            return Response({
                "message":"Error in Login",
                "error":str(e)
            })


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyOtpSerializer(data=data)
            if serializer.is_valid():
                otp_submited_by_user = serializer.validated_data.get("otp")
                email = serializer.validated_data.get("email")
                cache_key = f"email_otp{email}"
                payload = cache.get(cache_key)
                if not payload:
                    return Response({
                        "message" :"Not found"
                    })
                
                otp_sent_by_us = payload["otp"]

                if otp_sent_by_us != otp_submited_by_user:
                    return Response({
                        "message" : "wrong otp"
                    })
                payload["is_verified"] =True 
                 
                try:
                    user = User.objects.create(
                        email = payload['email'],
                        username = payload['username'],
                        password = make_password(payload['password']),
                        is_verified = payload["is_verified"]
                    )
                except Exception as e:
                    return Response({"message":"Error while creating user"})
                user.save()
                cache.delete(cache_key)
                return Response({
                        "success" : True,
                        "message" : "Account verified successfully",
                        "data" : payload
                    },status=200)
                    
                     
            return Response({
                "success" : False,
                "message" : "Something went wrong",
                "error" : serializer.errors
            },status=400)
                
                

        except Exception as e:
            return Response({
                "message":"server error 500",
                "error" : str(e)
            })
