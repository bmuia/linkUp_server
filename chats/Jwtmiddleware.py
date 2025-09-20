from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

jwt_auth = JWTAuthentication()

@database_sync_to_async
def get_user_from_token(token):
    try:
        validated_token = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated_token)
    except (InvalidToken, TokenError):
        return AnonymousUser()


class JWTAuthMiddlewareHeader:
    """
    Custom middleware for Django Channels that authenticates via JWT
    passed in the 'Authorization' header.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["user"] = AnonymousUser()

        # headers come as a list of (key, value) byte pairs
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode()

        if auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            scope["user"] = await get_user_from_token(token)

        return await self.app(scope, receive, send)
