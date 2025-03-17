import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class FriendRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect user to WebSocket"""
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_group_name = f"friends_{self.user.id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Remove user from WebSocket group"""
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def friend_request_notification(self, event):
        """Send real-time friend request notification"""
        await self.send(text_data=json.dumps({
            "event": "friend_request_received",
            "sender_id": event["sender_id"],
            "sender_name": event["sender_name"],
        }))

    async def friend_request_accepted(self, event):
        """Send real-time acceptance notification"""
        await self.send(text_data=json.dumps({
            "event": "friend_request_accepted",
            "friend_id": event["friend_id"],
            "friend_name": event["friend_name"],
        }))
