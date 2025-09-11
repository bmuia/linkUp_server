import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from kafka import KafkaProducer
from django.conf import settings
from datetime import datetime

class GroupConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def connect(self):
        try:
            self.room_name = 'chat'
            self.room_group_name = f"chat_{self.room_name}"

        
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        except Exception as e:
            print(f"Error in connect: {e}")

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
            print(f"Disconnected with code {close_code}")
        except Exception as e:
            print(f"Error in disconnect: {e}")

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")

            sender_id = self.scope['user'].id

            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender_id": sender_id
                }
            )

           
            self.producer.send(
                topic='chat_messages',
                value={"room": self.room_name, "message": message,  "sender_id": sender_id}
            )
            self.producer.flush()  

            settings.mongo_db['messages'].insert_one({
                "room": self.room_name,
                "message": message,
                "sender_id": sender_id,
                "timestamp": datetime.utcnow()
            })

        except Exception as e:
            print(f"Error in receive: {e}")

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
