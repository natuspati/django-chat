from django.contrib.auth import get_user_model

from rest_framework import permissions

User = get_user_model()


class RequestUserIsUserOrAdminElseAllowGetPost(permissions.BasePermission):
    """
    Allow get or post for anyone.
    For other actions, either Admin or User themselves must request.
    """
    
    def has_object_permission(self, request, view, obj: User):
        if view.action in ['list', 'retrieve', 'create', 'options']:
            # Allow anyone to create a new user or get information about users
            return True
        else:
            return request.user.is_superuser or request.user.id == obj.id
