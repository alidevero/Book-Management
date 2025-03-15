from django.urls import path
from .views import *


urlpatterns = [
    path("signup/" , SignupUser.as_view(), name="signup"),
    path("verify-otp/" , VerifyOTP.as_view(), name="verify-otp"),
    path("login/",UserLogin.as_view(),name="login")
]
