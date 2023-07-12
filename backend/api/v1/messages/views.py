from rest_framework import generics
from api.v1.messages.models import Message
from api.v1.messages.serializers import MessageSerializer


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    ordering = ('-timestamp',)
