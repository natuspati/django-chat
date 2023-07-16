from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

User = get_user_model()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid example',
            summary='Valid example',
            description='Example of a user with username and email',
            value={
                'username': 'zlatan',
                'email': 'zlatan@ibrahimovic.io',
            },
            response_only=True,
        ),
    ]
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid input example',
            summary='Valid input example',
            description='Example of a user with valid email, strong password that matches',
            value={
                'username': 'zlatan',
                'email': 'zlatan@ibrahimovic.io',
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
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
