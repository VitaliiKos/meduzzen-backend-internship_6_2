from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.users.models import UserModel as User
from apps.users.serializers import UserCreateSerializer

from .models import CompanyModel, EmployeeModel

UserModel: User = get_user_model()


class EmployeeSerializer(ModelSerializer):
    """Serializer for EmployeeModel objects."""

    class Meta:
        model = EmployeeModel
        fields = '__all__'


class CompaniesForCurrentUserSerializer(ModelSerializer):
    """Serializer for displaying companies for the currently authenticated user.

    This serializer includes information about the company, its members, and its status.
    """

    member = EmployeeSerializer(many=True, read_only=True)
    members = UserCreateSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyModel
        fields = ('id', 'name', 'description', 'status', 'member', "members")
        read_only_fields = ('members',)


class CompanySerializer(ModelSerializer):
    """Serializer for creating and updating company objects."""

    member = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyModel
        fields = ('id', 'name', 'description', 'status', 'member')

    @transaction.atomic
    def create(self, validated_data: dict):
        """Create a new company with its members."""
        members = validated_data.pop('members')
        company = CompanyModel.objects.create(**validated_data)
        EmployeeModel.objects.create(
            user=members,
            company=company,
            invitation_status='accepted',
            request_status='accepted',
            role='Owner'
        )
        return company
