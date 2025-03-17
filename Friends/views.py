from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from Auth.middleware import *
from Auth.models import User
from Auth.authentication import JWTAuthentication
from .models import Friendship
from .serializers import FriendRequestSerializer, SendFriendRequestSerializer, RespondFriendRequestSerializer
from django.conf import settings
from .utils import send_webhook_notification
from channels.layers import get_channel_layer
import asyncio

class SendFriendRequestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(f"i have successfully got the user{request.user}")
        if not request.user or request.user.is_anonymous:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        sender = request.user
        receiver_id = request.data.get("receiver_id")

        if not receiver_id:
            return Response({"error": "Receiver ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            return Response({"error": "You cannot send a request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if Friendship.objects.filter(sender=sender, receiver=receiver, status="pending").exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.create(sender=sender, receiver=receiver, status="pending")

        return Response({"message": "Friend request sent successfully"}, status=status.HTTP_201_CREATED)


class RespondFriendRequestView(APIView):
    """Accept or Reject Friend Request"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RespondFriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            request_id = serializer.validated_data["request_id"]
            action = serializer.validated_data["action"]

            friend_request = Friendship.objects.filter(id=request_id, receiver=user, status="pending").first()
            if not friend_request:
                return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

            if action == "accept":
                friend_request.accept()

                # Notify sender via WebSocket
                channel_layer = get_channel_layer()
                asyncio.create_task(channel_layer.group_send(
                    f"friends_{friend_request.sender.id}",
                    {
                        "type": "friend_request_accepted",
                        "friend_id": friend_request.receiver.id,
                        "friend_name": friend_request.receiver.username,
                    }
                ))

                # Send Webhook Notification
                webhook_url = settings.WEBHOOK_URL
                send_webhook_notification(webhook_url, {
                    "event": "friend_request_accepted",
                    "receiver_id": friend_request.receiver.id,
                    "sender_id": friend_request.sender.id,
                })

                return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)

            elif action == "reject":
                friend_request.reject()
                return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
