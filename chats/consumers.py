import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from datetime import datetime
from server.settings import MONGO_DB

logger = logging.getLogger(__name__)


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            user = self.scope.get("user")
            if not user or not user.is_authenticated:
                logger.warning("Unauthenticated connection attempt")
                await self.close(code=4001)
                return

            # Use a dynamic room if needed (hardcoded to 'chat' here)
            self.room_name = "chat"
            self.room_group_name = f"chat_{self.room_name}"

            # Join WebSocket group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()
            logger.info(f"User {user.id} connected to {self.room_group_name}")

        except Exception as e:
            logger.error(f"Error in connect: {e}", exc_info=True)
            await self.close(code=4002)

    async def disconnect(self, close_code):
        try:
            if hasattr(self, "room_group_name"):
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name,
                )
            logger.info(f"Disconnected with code {close_code}")
        except Exception as e:
            logger.error(f"Error in disconnect: {e}", exc_info=True)

    async def receive(self, text_data):
        try:
            user = self.scope.get("user")
            if not user or not user.is_authenticated:
                logger.warning("Unauthenticated user tried to send a message")
                await self.close(code=4003)
                return

            if not text_data:
                logger.info("Received empty message")
                return

            data = json.loads(text_data)
            message = data.get("message")
            if not message:
                logger.info("No 'message' field in received data")
                return

            timestamp = datetime.utcnow()

            # Broadcast message to WebSocket group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender_id": user.id,
                    "timestamp": timestamp.isoformat(),
                },
            )

            # Save to MongoDB (direct write)
            result = MONGO_DB["messages"].insert_one(
                {
                    "room": self.room_name,
                    "message": message,
                    "sender_id": user.id,
                    "timestamp": timestamp,
                }
            )
            logger.info(f"Message saved to MongoDB with _id={result.inserted_id}")

        except json.JSONDecodeError:
            logger.error("Received invalid JSON message")
        except Exception as e:
            logger.error(f"Error in receive: {e}", exc_info=True)

    async def chat_message(self, event):
        try:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": event["message"],
                        "sender_id": event.get("sender_id"),
                        "timestamp": event.get("timestamp"),
                    }
                )
            )
        except Exception as e:
            logger.error(f"Error in chat_message: {e}", exc_info=True)
