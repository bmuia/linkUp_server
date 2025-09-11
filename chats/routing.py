from django.urls import path
from . import consumers 

websocket_urlpatterns = [
    path("ws/chat/", consumers.GroupConsumer.as_asgi()),
]
