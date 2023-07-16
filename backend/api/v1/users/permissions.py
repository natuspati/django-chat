from django.contrib.auth import get_user_model

from rest_framework import permissions

User = get_user_model()


class RequestUserIsUserOrAdminElseAllowRetrieveOnly(permissions.BasePermission):
    """
    Allow retrieve for anyone.
    For other actions, either Admin or User themselves must request.
    """
    
    def has_object_permission(self, request, view, obj: User):
        return view.action == 'retrieve' or request.user.is_superuser or request.user.id == obj.id
