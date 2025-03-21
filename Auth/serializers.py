from rest_framework import serializers
from .models import *


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email','password','is_verified')
        extra_kwargs = {'password': {'write_only': True}} 
    
    def validate_email(self,value):
        if not value:
           raise serializers.ValidationError("Email is required")
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_username(self,value):
        if not value:
           raise serializers.ValidationError("Username is required")
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required")
        if len(value) <8 :
            raise serializers.ValidationError("Password must be 8 characters Long")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain atleast one number")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one Character")
        return value
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data) #default create_user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self ,data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password both are required")
        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        return data


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email' ,'profile_photo']
        read_only_fields = ['email']

        