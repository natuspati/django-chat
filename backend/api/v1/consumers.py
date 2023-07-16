import json

from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from api.v1.messages.models import Message

import logging

logger = logging.getLogger('file')


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
    
    async def connect(self):
        logger.info('Connected to ChatConsumer')
        self.room_name = 'home'
        await self.accept()
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )
        await self.send_json(
            {
                "type": "welcome_message",
                "message": "You've successfully connected!"
            }
        )
    
    async def disconnect(self, close_code):
        logger.info('Disconnected from ChatConsumer')
        return await super().disconnect(close_code)
    
    async def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message_echo",
                    "name": content["name"],
                    "message": content["message"],
                },
            )
        return await super().receive_json(content, **kwargs)
    
    async def chat_message_echo(self, event):
        await self.send_json(event)
    
    # @database_sync_to_async
    # def create_message(self, message, username):
    #     message_obj = Message.objects.create(
    #         content=message,
    #         username=username
    #     )
    #     return message_obj
    #
    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     message = data['message']
    #     username = data['username']
    #
    #     # Create a new message object and save it to the database
    #     message_obj = await self.create_message(message, username)
    #
    #     # Send the message to the group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message_obj.content,
    #             'username': message_obj.username,
    #             'timestamp': str(message_obj.timestamp)
    #         }
    #     )
    #
    # async def chat_message(self, event):
    #     message = event['message']
    #     username = event['username']
    #     timestamp = event['timestamp']
    #
    #     # Send the message to the websocket
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'username': username,
    #         'timestamp': timestamp
    #     }))
