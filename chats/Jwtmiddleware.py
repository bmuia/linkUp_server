from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from jwt import InvalidTokenError

User = get_user_model()
jwt_auth = JWTAuthentication()

@database_sync_to_async
def get_user_from_token(token):
    try:
        validated_token = UntypedToken(token)
        user = jwt_auth.get_user(validated_token)
        return user
    except InvalidTokenError:
        return AnonymousUser()


class JWTAuthMiddlewareHeader:
    """
    JWT Auth Middleware that extracts token from 'Authorization' header
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["user"] = AnonymousUser()

        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b'authorization', b'').decode()

        if auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            scope["user"] = await get_user_from_token(token)

        return await self.app(scope, receive, send)
