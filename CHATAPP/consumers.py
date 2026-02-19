from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import chatroom, chat_message, profile
import json


class chat_consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user = self.scope['user']
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()
        
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        user_obj = data.get('sender')
        profile_image = data.get('profile_image')
        
        
        # Broadcast to all users in the group
        await self.channel_layer.group_send(self.room_id, {
            'type': 'chat.message',
            'message': message,
            'sender' : user_obj,
            'profile_image': profile_image,
        })
        
        
    async def chat_message(self, event):
        # This handler is called for all connections in the group
            message = event['message']
            sender = event['sender']
            profile_image = event['profile_image']
            # Save message to database
            await self.create_message(
                message=message
            )
            
            # Send to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': message,
                'sender' : sender,
                'profile_image': profile_image
            }))
    
    @database_sync_to_async
    def create_message(self,  message):
        try:
            get_group_obj = chatroom.objects.get(id=self.room_id)
            profile_obj = profile.objects.get(user=self.user)
            if not chat_message.objects.get(chatroom=get_group_obj, user=profile_obj, message=message).exists():
                message_save = chat_message.objects.create(
                    chatroom=get_group_obj,
                    user=profile_obj,
                    message=message,
                )
                message_save.save()
                return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
        
        
        
        
        