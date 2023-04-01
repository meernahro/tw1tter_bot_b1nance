import os
import json
from database_manager import models
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class TwitterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.internal_group =  "internal"
        self.room_group_name = os.getenv("ROOM_GROUP_NAME")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add(self.internal_group, self.channel_name)

        await self.accept()
            

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.internal_group, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        # Send message to room group
        await self.channel_layer.group_send(
            text_data_json['group'], {"type": text_data_json['type'], "message": text_data_json['message']}
        )

    # Receive message from room group
    async def chat_message(self, event):
        
        message = json.dumps(event)
        
        try:
        # Send message to WebSocket
            await self.send(text_data=message)
            print("Sent Message to Socket")
        except Exception as e:
            print("Failed sending to socket ", e)

    async def command(self, event):
        
        message = event['message']
            
        if message['function'] == "delete_tweet_by_id":
            await sync_to_async(models.delete_tweet_by_id)(int(message['id']))

    async def sentiment(self,event):
        message = json.dumps(event)
        
        try:
        # Send message to WebSocket
            await self.send(text_data=message)
            print("Sent Message to Socket")
        except Exception as e:
            print("Failed sending to socket ", e)