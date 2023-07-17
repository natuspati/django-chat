from rest_framework import serializers

from api.v1.models import Message
from api.v1.users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    # from_user = serializers.SerializerMethodField()
    # to_user = serializers.SerializerMethodField()
    # conversation = serializers.SerializerMethodField()
    from_user = serializers.CharField(read_only=True, source='from_user.username')
    to_user = serializers.CharField(read_only=True, source='to_user.username')
    conversation = serializers.CharField(read_only=True, source='conversation.id')
    
    
    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user",
            "to_user",
            "content",
            "timestamp",
            "read",
        )
    
    # def get_conversation(self, obj):
    #     return str(obj.conversation.id)
    #
    # def get_from_user(self, obj):
    #     return UserSerializer(obj.from_user).data
    #
    # def get_to_user(self, obj):
    #     return UserSerializer(obj.to_user).data
