from django.urls import path
from .views import SendFriendRequestView, RespondFriendRequestView

urlpatterns = [
    path("send-request/", SendFriendRequestView.as_view(), name="send-friend-request"),
    path("respond-request/", RespondFriendRequestView.as_view(), name="respond-friend-request"),
]
