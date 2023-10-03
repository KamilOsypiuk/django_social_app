import json
import aioredis

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Chat, Message
from .serializers import MessageSerializer
from .exceptions import ConsumerException
from users.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        current_user = self.scope['user'].id if self.scope['user'].is_authenticated else None
        chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.redis = await aioredis.from_url("redis://localhost:6379/", decode_responses=True)
        try:
            self.chat = await self.retrieve_chat(chat_id=chat_id)
            if self.chat:
                if current_user in self.chat.participants:
                    messages = await self.retrieve_messages(chat_id=chat_id)
                    serialized_messages = MessageSerializer(messages, many=True).data

                    payload = {
                        'type': 'chat_message',
                        'messages': serialized_messages
                    }
                    self.room_group_name = f"chat_{chat_id}"
                    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                    await self.channel_layer.group_send(self.room_group_name, payload)
                else:
                    raise ConsumerException('You are not part of this chat')
            else:
                self.chat = Chat.objects.create()
                self.chat.participants.add(current_user)
                self.room_group_name = f"chat_{self.chat.pk}"
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        except ConsumerException as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
            await self.close()

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        await self.disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get('type')
        user_id = data.get('user_id')
        message = data.get('message')
        sender = self.scope['user'].id

        try:
            with transaction.atomic():
                if message_type == 'chat_message':
                    self.redis.hset(f'chat_{self.chat.pk}', "chat", self.chat.pk, "sender", sender, "message", message)

                    messages = self.retrieve_messages(chat_id=self.chat.pk)
                    serialized_messages = MessageSerializer(messages, many=True).data

                    payload = {
                        'type': 'chat_message',
                        'sender': sender,
                        'message': message,
                        'messages': serialized_messages
                    }
                    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                    await self.channel_layer.group_send(self.room_group_name, payload)

                if message_type == 'add_user':
                    await self.add_user_to_chat(user_id=user_id)
                if message_type == 'delete_user':
                    await self.delete_user_from_chat(user_id=user_id)
        except NotFound as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
            await self.close()

    async def authenticate_user(self):
        # Extract JWT token from the connection headers
        token = self.scope.get('headers', {}).get(b'authorization', b'').decode('utf-8')
        if token.startswith('Bearer '):
            token = token.split(' ')[1]

        # Perform JWT authentication
        authentication = JWTAuthentication()
        validated_token = authentication.get_validated_token(token)
        user = authentication.get_user(validated_token)

        # Check if the user exists
        try:
            return await self.get_user(pk=user.pk)
        except User.DoesNotExist:
            return AnonymousUser()

    async def add_user_to_chat(self, user_id: int) -> dict:
        user = self.get_user(user_id=user_id)
        chat = self.retrieve_chat(chat_id=self.chat.pk)
        if chat and user:
            if self.scope['user'].id not in chat.participants.all():
                raise ConsumerException("You have no permission to add users to this chat")
            chat.participants.add(user)
            return {'message': 'User added successfully to chat'}
        else:
            raise NotFound("User or chat not found")

    async def delete_user_from_chat(self, user_id: int) -> dict:
        user = self.get_user(user_id=user_id)
        chat = self.retrieve_chat(chat_id=self.chat.pk)
        if chat and user:
            if self.scope['user'].id not in chat.participants.all():
                raise ConsumerException("You have no permission to delete users from this chat")
            chat.participants.remove(user)
            return {'message': 'User deleted successfully from chat'}
        else:
            raise NotFound("User or chat not found")

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        messages = event['messages']

        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'sender': sender,
                    'messages': messages,
                }
            )
        )

    @database_sync_to_async
    def retrieve_chat(self, chat_id: int) -> Chat:
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def retrieve_messages(self, chat_id: int) -> Message:
        return Message.objects.filter(chat_id=chat_id).order_by('timestamp')

    @database_sync_to_async
    def save_message(self, sender: int, chat_id: int, message: str):
        Message.objects.create(sender=sender, chat=chat_id, message=message)

    @database_sync_to_async
    def get_user(self, user_id: int) -> User:
        return User.objects.get(id=user_id)
