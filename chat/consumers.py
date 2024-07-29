import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{self.room_name}'
        print(f"User: {self.user} - room name: {self.room_name} - room group name: {self.room_group_name}")
        subprotocols = self.scope.get('subprotocols', [])
        token = subprotocols[0] if subprotocols else None
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept(subprotocol=token)

        # Load and send past messages between the user and the other user
        past_messages = await self.get_past_messages()
        await self.send(text_data=json.dumps({
            'type': 'past_messages',
            'messages': past_messages
        }))

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_username = text_data_json['receiver']

        # Save the message to the database
        receiver = await self.get_user(receiver_username)
        await self.save_message(self.user, receiver, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'receiver': receiver.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        if receiver == self.user.username or sender == self.user.username:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender,
                'receiver': receiver
            }))

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        from chat.models import Message
        Message.objects.create(sender=sender, receiver=receiver, messages=message)

    @database_sync_to_async
    def get_past_messages(self):
        from chat.models import Message
        messages = Message.objects.filter(
            (Q(sender=self.user) & Q(receiver=self.room_name)) | 
            (Q(receiver=self.user) & Q(sender=self.room_name))
        ).order_by('time')
        return [{'sender': msg.sender.username, 'message': msg.messages, 'receiver': msg.receiver.username} for msg in messages]

    @database_sync_to_async
    def get_user(self, username):
        from auth_app.models import Accounts
        return Accounts.objects.get(username=username)
