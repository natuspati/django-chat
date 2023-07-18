from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from drf_spectacular.utils import (
    extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample
)
from drf_spectacular.types import OpenApiTypes

from api.v1.models import Conversation

from api.v1.conversations.serializers import ConversationSerializer


@extend_schema_view(  # noqa
    list=extend_schema(
        description='List conversations of requesting user',
        parameters=[
            OpenApiParameter(
                'conversation',
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        'Conversation string query',
                        summary='Valid Conversation string query',
                        value='conversation__user1__user2'
                    )
                ]),
        ]
    ),
    retrieve=extend_schema(
        description='Retrieve a conversation of requesting user and another user',
        parameters=[
            OpenApiParameter(
                'name',
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                examples=[
                    OpenApiExample(
                        'Conversation name',
                        summary='Valid conversation name path variable',
                        value='conversation__user1__user2'
                    )
                ]),
        ]
    )
)
class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    lookup_field = "name"
    
    def get_queryset(self):
        queryset = Conversation.objects.filter(
            name__contains=self.request.user.username
        )
        return queryset
    
    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}
