from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.serializers import ModelSerializer
from djoser.serializers import UserCreateSerializer
from apps.users.models import ProfileModel

UserModel = get_user_model()


class UserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserModel
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class ProfileSerializer(ModelSerializer):
    """Serializer for creating user profile."""
    class Meta:
        model = ProfileModel
        fields = ('id', 'city', 'phone', 'age')


class UserAccountSerializer(ModelSerializer):
    """Serializer for creating user."""
    profile = ProfileSerializer()

    class Meta:
        model = UserModel

        fields = (
            'id', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at',
            'updated_at', 'profile'
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    @transaction.atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        return user
