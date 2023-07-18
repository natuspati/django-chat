from django.contrib.auth import get_user_model

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from api.v1.messages.serializers import MessageSerializer
from api.v1.models import Conversation
from api.v1.users.serializers import UsernameSerializer

User = get_user_model()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid output example',
            summary='Valid putput example',
            description='Example of Conversation list response',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'name': 'conversation__user1_user2',
                'other_user': {
                    'username': 'suarez',
                    'name': 'Luis'
                },
                'last_message': {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                    'conversation': '3fa85f64-5717-4562-b3fc-2c963f66afa',
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
            },
            response_only=True
        ),
    ]
)
class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ('id', 'name', 'other_user', 'last_message')
    
    def get_last_message(self, obj):
        messages = obj.messages.all().order_by('-timestamp')
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data
    
    def get_other_user(self, obj):
        usernames = obj.name.split('__')
        context = {}
        for username in usernames:
            if username != self.context['user'].username:
                # This is the other participant
                other_user = User.objects.get(username=username)
                return UsernameSerializer(other_user, context=context).data
