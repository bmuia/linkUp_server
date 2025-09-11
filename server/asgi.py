"""
ASGI config for ping_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chats.routing import websocket_urlpatterns

# Import your custom JWT middleware
from chats.Jwtmiddleware import JWTAuthMiddlewareHeader

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# Standard Django ASGI application for HTTP
django_asgi_app = get_asgi_application()

# ProtocolTypeRouter allows HTTP and WebSocket support
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddlewareHeader(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
