import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from kafka import KafkaProducer
from django.conf import settings
from datetime import datetime
from server.settings import MONGO_DB

logger = logging.getLogger(__name__)

class GroupConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = None
        self.room_name = "chat"
        self.room_group_name = f"chat_{self.room_name}"

    def connect(self):
        try:
            user = self.scope.get("user")
            if not user or not user.is_authenticated:
                logger.warning("Unauthenticated connection attempt")
                self.close(code=4001)
                return

            # Initialize Kafka producer once
            if not self.producer:
                self.producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                )

            # Join WebSocket group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name,
            )
            self.accept()
            logger.info(f"User {user.id} connected to {self.room_group_name}")

        except Exception as e:
            logger.error(f"Error in connect: {e}", exc_info=True)
            self.close(code=4002)

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name,
            )
            if self.producer:
                self.producer.close()
                self.producer = None
            logger.info(f"Disconnected with code {close_code}")
        except Exception as e:
            logger.error(f"Error in disconnect: {e}", exc_info=True)

    def receive(self, text_data):
        try:
            user = self.scope.get("user")
            if not user or not user.is_authenticated:
                logger.warning("Unauthenticated user tried to send a message")
                self.close(code=4003)
                return

            if not text_data:
                logger.warning("Received empty message")
                return

            data = json.loads(text_data)
            message = data.get("message")
            if not message:
                logger.warning("No 'message' field in received data")
                return

            # Broadcast message to WebSocket group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender_id": user.id,
                },
            )

            # Publish to Kafka
            if self.producer:
                self.producer.send(
                    topic="chat_messages",
                    value={
                        "room": self.room_name,
                        "message": message,
                        "sender_id": user.id,
                    },
                )
                self.producer.flush()

            # Save to MongoDB (directly from settings)
            result = MONGO_DB["messages"].insert_one(
                {
                    "room": self.room_name,
                    "message": message,
                    "sender_id": user.id,
                    "timestamp": datetime.utcnow(),
                }
            )
            logger.info(f"Message saved to MongoDB with _id={result.inserted_id}")

        except json.JSONDecodeError:
            logger.warning("Received invalid JSON message")
        except Exception as e:
            logger.error(f"Error in receive: {e}", exc_info=True)

    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"]}))
