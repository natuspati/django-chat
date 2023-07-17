from django.urls import path
from api.v1.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    path('chats/<str:conversation_name>/', ChatConsumer.as_asgi()),
    path('notifications/', NotificationConsumer.as_asgi()),
]
