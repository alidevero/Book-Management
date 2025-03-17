from rest_framework import serializers
from .models import Friendship
from Auth.models import User  # Ensure you have a Custom User model

class FriendRequestSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name", read_only=True)
    receiver_name = serializers.CharField(source="receiver.name", read_only=True)

    class Meta:
        model = Friendship
        fields = ["id", "sender", "receiver", "status", "sender_name", "receiver_name", "created_at"]

class SendFriendRequestSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()

class RespondFriendRequestSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=["accept", "reject"])
