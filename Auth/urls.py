from django.urls import path
from .views import *


urlpatterns = [
    path("signup/" , SignupUser.as_view(), name="signup"),
    path("verify-otp/" , VerifyOTP.as_view(), name="verify-otp"),
    path("login/",UserLogin.as_view(),name="login"),
    path("profile/",UserProfileView.as_view(),name="Profile"),
    path("delete/",UserDeleteView.as_view(),name="delete"),
    path("update/",UserUpdateView.as_view(),name="update"),
]
