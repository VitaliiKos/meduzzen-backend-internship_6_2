from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer
from core.enums.invitation_enum import InvitationEnum
from core.enums.user_enum import UserEnum

from ..invitations.models import EmployeeModel
from ..invitations.serializers import EmployeeSerializer
from .models import CompanyModel

UserModel: User = get_user_model()


class CompaniesForCurrentUserSerializer(ModelSerializer):
    """Serializer for displaying companies for the currently authenticated user.
    """

    member = EmployeeSerializer(many=True, read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyModel
        fields = ('id', 'name', 'description', 'visible', 'member', "members")
        read_only_fields = ('members',)

    def update(self, instance, validated_data):
        if self.partial:
            instance.visible = not instance.visible

        return super().update(instance, validated_data)


class CompanySerializer(ModelSerializer):
    """Serializer for creating and updating company objects."""

    member = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyModel
        fields = ('id', 'name', 'description', 'visible', 'member')

    @transaction.atomic
    def create(self, validated_data: dict):
        """Create a new company with its members."""
        members = validated_data.pop('members')
        company = CompanyModel.objects.create(**validated_data)

        EmployeeModel.objects.create(
            user=members,
            company=company,
            invitation_status=InvitationEnum.ACCEPTED,
            request_status=InvitationEnum.ACCEPTED,
            role=UserEnum.OWNER
        )
        return company
