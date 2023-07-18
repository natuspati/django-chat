from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from api.v1.models import Message
from api.v1.users.serializers import UsernameSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid output example',
            summary='Valid putput example',
            description='Example of message list response',
            value=
            {'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
             'conversation': '9gh67f67-59837-4562-b3fc-2c963f66afa6',
             'from_user': {
                 'username': 'zlatan',
                 'name': 'Zlatan'
             },
             'to_user': {
                 'username': 'suarez',
                 'name': 'Luis'
             },
             'content': 'string',
             'timestamp': '2023-07-18T06:33:58.536Z',
             'read': True
             }
        ),
    ]
)
class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = (
            'id',
            'conversation',
            'from_user',
            'to_user',
            'content',
            'timestamp',
            'read',
        )
    
    def get_conversation(self, obj):
        return str(obj.conversation.id)
    
    def get_from_user(self, obj):
        return UsernameSerializer(obj.from_user).data
    
    def get_to_user(self, obj):
        return UsernameSerializer(obj.to_user).data
