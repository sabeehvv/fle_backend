import json
from channels.generic.websocket import AsyncWebsocketConsumer # type:ignore
import datetime
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async  # type:ignore
from .models import EventChat
from fle_user.models import Account

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = f'event_{self.event_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("connect success")

    async def disconnect(self, close_code):
        print("desconnect")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        message = json.loads(text_data)
        print(message,'message reaceave dddddddddd')
        sender = await self.get_user(message['sender'])
        receiver = message['receiver']
        content = message['content']
        user = {
            "id":sender.id,
            "name":sender.first_name,
        }
        
        await self.save_chat_message(sender, receiver, content)
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat.message',
            'message': {
                            'sender': user,
                            'receiver': receiver,
                            'content':content,
                            'timestamp':datetime.datetime.now().isoformat()

                    }
        }
    )

    @sync_to_async
    def save_chat_message(self, sender, event_id, content):
        event_chat = EventChat.objects.create(sender=sender, receiver_id=event_id, content=content)


    @database_sync_to_async
    def get_user(self, user_id):
        return Account.objects.get(id=user_id)

    # async def receive(self, text_data):
    #     print("receve")
    #     message = json.loads(text_data)
    #     sender = self.scope['user'].id
    #     receiver_id = message['receiver']
    #     content = message['content']

    #     event_chat = EventChat.objects.create(sender_id=sender, receiver_id=receiver_id, content=content)

    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat.message',
    #             'message': {
    #                 'id': event_chat.id,
    #                 'sender': sender,
    #                 'content': content,
    #                 'timestamp': event_chat.timestamp.isoformat(),
    #             }
    #         }
    #     )

    async def chat_message(self, event):
        print("chat message")
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'message': message
        }))
