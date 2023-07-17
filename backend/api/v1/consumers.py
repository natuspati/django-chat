import json
from uuid import UUID

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from api.v1.models import Message, Conversation
from api.v1.messages.serializers import MessageSerializer

import logging

logger = logging.getLogger('dev')

User = get_user_model()


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None
    
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return
        
        await self.accept()
        self.conversation_name = (
            f"{self.scope['url_route']['kwargs']['conversation_name']}"
        )
        self.conversation, created = await Conversation.objects.aget_or_create(
            name=self.conversation_name
        )
        
        await self.channel_layer.group_add(
            self.conversation_name,
            self.channel_name,
        )
        
        await self.send_json(
            {
                "type": "online_user_list",
                "users": await self.get_conversation_usernames(),
            }
        )
        
        await self.channel_layer.group_send(
            self.conversation_name,
            {
                "type": "user_join",
                "user": self.user.username,
            },
        )
        
        await self.add_user_to_conversation()
        
        message_count = await self.conversation.messages.all().acount()
        last_messages_data = await self.get_messages()
        
        await self.send_json(
            {
                "type": "last_50_messages",
                "messages": last_messages_data,
                "has_more": message_count > 50,
            }
        )
    
    async def disconnect(self, code):
        if self.user.is_authenticated:
            # send the leave event to the room
            await self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "user_leave",
                    "user": self.user.username,
                },
            )
            await self.remove_user_from_conversation()
        return await super().disconnect(code)
    
    async def receive_json(self, content, **kwargs):
        message_type = content["type"]
        
        if message_type == "read_messages":
            messages_to_me = self.conversation.messages.filter(to_user=self.user)
            messages_to_me.aupdate(read=True)
            
            # Update the unread message count
            unread_count = await Message.objects.filter(to_user=self.user, read=False).acount()
            await self.channel_layer.group_send(
                self.user.username + "__notifications",
                {
                    "type": "unread_count",
                    "unread_count": unread_count,
                },
            )
        
        if message_type == "typing":
            await self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "typing",
                    "user": self.user.username,
                    "typing": content["typing"],
                },
            )
        
        if message_type == "chat_message":
            receiver_user = await self.get_receiver()
            message_data = await self.create_message(content, receiver_user)
            
            await self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "name": self.user.username,
                    "message": message_data,
                },
            )
            
            notification_group_name = receiver_user.username + "__notifications"
            await self.channel_layer.group_send(
                notification_group_name,
                {
                    "type": "new_message_notification",
                    "name": self.user.username,
                    "message": message_data,
                },
            )
        
        return await super().receive_json(content, **kwargs)
    
    async def chat_message_echo(self, event):
        await self.send_json(event)
    
    async def user_join(self, event):
        await self.send_json(event)
    
    async def user_leave(self, event):
        await self.send_json(event)
    
    async def typing(self, event):
        await self.send_json(event)
    
    async def new_message_notification(self, event):
        await self.send_json(event)
    
    async def unread_count(self, event):
        await self.send_json(event)
    
    async def get_receiver(self):
        usernames = self.conversation_name.split("__")
        for username in usernames:
            if username != self.user.username:
                # This is the receiver
                return await User.objects.aget(username=username)
    
    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)
    
    @database_sync_to_async
    def get_messages(self):
        messages = self.conversation.messages.all().order_by("-timestamp")[0:50]
        return MessageSerializer(messages, many=True).data
    
    @database_sync_to_async
    def create_message(self, content, receiver_user):
        message = Message.objects.create(
            from_user=self.user,
            to_user=receiver_user,
            content=content["message"],
            conversation=self.conversation,
        )
        
        return MessageSerializer(message).data
    
    @database_sync_to_async
    def get_conversation_usernames(self):
        return [user.username for user in self.conversation.online.all()]
    
    @database_sync_to_async
    def add_user_to_conversation(self):
        return self.conversation.online.add(self.user)
    
    @database_sync_to_async
    def remove_user_from_conversation(self):
        return self.conversation.online.remove(self.user)

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.notification_group_name = None
    
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return
        
        await self.accept()
        
        # private notification group
        self.notification_group_name = self.user.username + "__notifications"
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name,
        )
        
        # Send count of unread messages
        unread_count = await Message.objects.filter(to_user=self.user, read=False).acount()
        await self.send_json(
            {
                "type": "unread_count",
                "unread_count": unread_count,
            }
        )
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name,
        )
        return await super().disconnect(code)
    
    async def new_message_notification(self, event):
        await self.send_json(event)
    
    async def unread_count(self, event):
        await self.send_json(event)
