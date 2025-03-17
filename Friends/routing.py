from django.urls import re_path
from .consumers import FriendRequestConsumer

websocket_urlpatterns = [
    re_path(r"ws/friends/$", FriendRequestConsumer.as_asgi()),
]
