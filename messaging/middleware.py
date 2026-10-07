from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware:
    """
    Custom middleware that takes a JWT token from the query string and authenticates the user.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode("utf8"))
        token = query_string.get("token")

        if token:
            try:
                # This will verify the token's validity
                untyped_token = UntypedToken(token[0])
                # If valid, get the user
                user_id = untyped_token.payload.get('user_id')
                user = await get_user(user_id)
                scope['user'] = user
            except (InvalidToken, TokenError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)
