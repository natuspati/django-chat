from django.contrib.auth import get_user_model

from rest_framework import permissions

User = get_user_model()


class MessageRecipientReceiverOnly(permissions.BasePermission):
    """
    Messages between two users are accessible only to them.
    """
    
    def has_permission(self, request, view):
        conversation_name = request.GET.get('conversation')
        return request.user.username in conversation_name
