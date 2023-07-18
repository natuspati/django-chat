from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.v1.models import Message
from api.v1.messages.serializers import MessageSerializer
from api.v1.paginators import MessagePagination
from api.v1.messages.permissions import MessageRecipientReceiverOnly

extend_schema_view(
    list=extend_schema(
        description='text',
        parameters=[
            OpenApiParameter("conversation", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ]
    )
)


class MessageViewSet(ListModelMixin, GenericViewSet):  # noqa
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    pagination_class = MessagePagination
    permission_classes = [MessageRecipientReceiverOnly]
    
    def get_queryset(self):
        conversation_name = self.request.GET.get('conversation')
        queryset = (
            Message.objects.filter(
                conversation__name__contains=self.request.user.username,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )
        return queryset
