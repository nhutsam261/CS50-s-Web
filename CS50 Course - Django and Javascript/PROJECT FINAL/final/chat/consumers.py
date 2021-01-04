import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from accounts.models import User
from .views import get_last_10_messages, get_user_contact, get_current_chat

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = get_last_10_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)


    def new_message(self, data):
        author_user = get_user_contact(data['from'])
        message = Message.objects.create(author=author_user, content=data['message'])

        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()

        content = {
            'command': 'new_message',
            'message': message.serialize()
        }
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(message.serialize())
        return result


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    # Send message to WebSocket
    def send_message(self, message):
        self.send(text_data=json.dumps(message))


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    