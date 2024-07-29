from django.urls import path
from .consumers import ChatConsumer
# from .old_consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer.as_asgi())
]