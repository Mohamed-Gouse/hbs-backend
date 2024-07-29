import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.route import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from chat.jwt_middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": JWTAuthMiddleware(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))
})