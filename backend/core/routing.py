from django.urls import re_path
from api.v1.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'chat/', ChatConsumer.as_asgi()),
]