from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)

from api.v1.users.serializers import UserSerializer, RegisterSerializer, UsernameSerializer
from api.v1.users.permissions import RequestUserIsUserOrAdminElseAllowGetPost

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UsernameSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [RequestUserIsUserOrAdminElseAllowGetPost]
    # Disallow update methods for now, implement them later
    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ['put', 'patch']]
    
    @extend_schema(
        description='User data.',
        responses=UserSerializer,
    )
    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    @extend_schema(
        description='Register new user.',
        request=RegisterSerializer,
        responses=TokenObtainPairSerializer,
    )
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        registered_user = User.objects.get(serializer.data['username'])
        token = RefreshToken.for_user(registered_user)
        token_serializer = TokenObtainPairSerializer(token)
        return Response(token_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
