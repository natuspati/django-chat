from urllib.parse import parse_qs
from channels.db import database_sync_to_async

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.authentication import JWTAuthentication


@database_sync_to_async
def get_user(scope):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    # postpone model import to avoid ImproperlyConfigured error before Django
    # setup is complete.
    from django.contrib.auth.models import AnonymousUser
    
    if "token" not in scope:
        raise ValueError(
            "Cannot find token in scope. You should wrap your consumer in "
            "TokenAuthMiddleware."
        )
    token = scope["token"]
    raw_encoded_token = token.encode('utf-8')
    
    JWT_authenticator = JWTAuthentication()
    
    validated_token = JWT_authenticator.get_validated_token(raw_encoded_token)
    
    existing_user = JWT_authenticator.get_user(validated_token)
    
    if existing_user:
        if existing_user.is_active:
            return existing_user
        else:
            raise AuthenticationFailed(_("User inactive or deleted."))
    else:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware that takes a token from the query string and authenticates via
    Django SimpleJWT.
    """
    
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        query_params = parse_qs(scope["query_string"].decode())
        token = query_params["token"][0]
        scope["token"] = token
        scope["user"] = await get_user(scope)
        return await self.app(scope, receive, send)
