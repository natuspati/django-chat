from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

import logging

logger = logging.getLogger('dev')

User = get_user_model()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid example',
            summary='Valid example',
            description='Example of a user with username',
            value={
                'username': 'zlatan',
                'name': 'Zlatan'
            },
            response_only=True,
        ),
    ]
)
class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid example',
            summary='Valid example',
            description='Example of a user with username and email',
            value={
                'username': 'zlatan',
                'email': 'zlatan@ibrahimovic.io',
                'name': 'Zlatan'
            },
            response_only=True,
        ),
    ]
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'name']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid input example',
            summary='Valid input example',
            description='Example of a user with valid email, strong password that matches',
            value={
                'username': 'zlatan',
                'email': 'zlatan@ibrahimovic.io',
                'name': 'Zlatan',
                'password': 'secureP@55word',
                'password2': 'secureP@55word'
            },
            request_only=True,
        ),
    ]
)
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(required=False, default=None)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password', 'password2')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid input example',
            summary='Valid input example',
            description='Example of a user with valid email, strong password that matches',
            value={
                'username': 'zlatan',
                'password2': 'secureP@55word'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Success output example',
            summary='Success output example',
            description='Example of a successful login',
            value={
                'refresh': 'string',
                'access': 'string',
                'username': 'zlatan'
            },
            response_only=True,
        ),
    ]
)
class TokenObtainPairWithUsernameSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # Add username to token obtain view
        validated_data['username'] = self.user.username
        return validated_data
