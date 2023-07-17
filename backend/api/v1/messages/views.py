from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.v1.models import Message
from api.v1.messages.serializers import MessageSerializer
from api.v1.paginators import MessagePagination


class MessageViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    pagination_class = MessagePagination
    
    def get_queryset(self):
        conversation_name = self.request.GET.get("conversation")
        queryset = (
            Message.objects.filter(
                conversation__name__contains=self.request.user.username,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )
        return queryset
