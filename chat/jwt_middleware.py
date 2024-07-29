from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
import jwt
from django.conf import settings

@database_sync_to_async
def get_user(token):
    from django.contrib.auth.models import AnonymousUser
    try:
        from auth_app.models import Accounts
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload['user_id']
        user = Accounts.objects.get(id=user_id)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Accounts.DoesNotExist):
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        headers = dict(scope['headers'])
        token = headers.get(b'sec-websocket-protocol', None)
        if token:
            token = token.decode('utf-8')
            scope['user'] = await get_user(token)
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
