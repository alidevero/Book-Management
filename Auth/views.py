#system imports
import os
import random

#project imports
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView , Response

#local imports
from Auth.authentication import *
from Books.models import *
from Social.models import *
from Books.serializers import *
from Social.serializers import *
from .models import *
from .serializers import *
from .utils import send_otp_via_mail , generate_jwt_token


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
                email_sent = send_otp_via_mail(email, otp)
                
                cache_key = f"email_otp{email}"
                cache.set(cache_key, payload, timeout=600)  # save otp in cache for 10 mins
                return Response(
                    {"details": "Otp sent successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"details": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
                        "details": "OTP expired or not found"
                    }, status=status.HTTP_404_NOT_FOUND)
                
                otp_sent_by_us = payload["otp"]

                if otp_sent_by_us != otp_submited_by_user:
                    return Response({
                        "details": "Incorrect OTP"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                payload["is_verified"] = True 
                 
                try:
                    user = User.objects.create(
                        email=payload['email'],
                        username=payload['username'],
                        password=make_password(payload['password']),
                        is_verified=payload["is_verified"]
                    )
                except Exception as e:
                    return Response({ 
                        "details": str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                user.save()
                cache.delete(cache_key)
                return Response({
                    "success": True,
                    "details": "Account verified successfully",
                    "data": {
                        "email": payload["email"],
                        "username": payload["username"],
                        "is_verified": payload["is_verified"]
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "error": "OTP verification failed",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogin(APIView):
    
    def post(self , request):
        try:
            data = request.data
            serializer = UserLoginSerializer(data= data)
            if serializer.is_valid():
                email = serializer.validated_data.get("email")
                token = generate_jwt_token(email)
                return Response({
                    "success":True,
                    "details":"LogedIn successfully",
                    "token":token
                })
            return Response({
                "details" : serializer.errors
            })
        
        except Exception as e:
            return Response({
                "details":str(e)
            })


#need to add few other things
class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self , request):
        try:
            user = request.user
            user_book = BookModel.objects.filter(uploaded_by= user).all()
            user_like = LikeModel.objects.filter(user= user).all()
            book_serializer = UploadBookSerializer(user_book,many = True)
            like_serializer = LikeSerializer(user_like, many = True)
            serializer = UserProfileSerializer(user)
            return Response({"message":"This is you profile",
                             "data":serializer.data,
                             "books":book_serializer.data,
                             "likes":like_serializer.data
                             },status=status.HTTP_200_OK)          
        except Exception as e:
            return Response({
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self , request):
        try:
            if not request.user or request.user.is_anonymous:
                return Response({"message":"user is missing"})
            user = request.user
            print(f"this is the user {user}")
            
            user.delete()
            return Response({"details":"successully delete"})

        except Exception as e:
            return Response({"message":"Something went wrong while deleting","details":str(e)},status=500)
        
    

class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self , request):
        try:
            user = request.user
            serializer = UserUpdateSerializer(instance = user ,data= request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"details":"Successfully updated the user"})
            return Response({"details":serializer.errors})
        except Exception as e:
            return Response({"details":str(e)})
                
