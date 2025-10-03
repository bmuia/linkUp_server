# chats/routing.py

from django.urls import re_path
from . import consumers 

websocket_urlpatterns = [
    # CHANGE: Add /? to make the trailing slash optional
    re_path(r"^ws/chat/?$", consumers.GroupConsumer.as_asgi()), 
]