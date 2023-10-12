from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.users.models import UserModel as User
from apps.users.serializers import UserForDjoserSerializers
from core.enums.invitation_enum import InvitationEnum
from core.enums.user_enum import UserEnum

from .helper import get_user_role_in_company
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
    members = UserForDjoserSerializers(many=True, read_only=True)

    class Meta:
        model = CompanyModel
        fields = ('id', 'name', 'description', 'status', 'member', "members")
        read_only_fields = ('members',)

    def update(self, instance, validated_data):
        user_id = validated_data.get('user_id', None)
        user_role = get_user_role_in_company(user_id=user_id, company_id=instance.id)
        if user_role != UserEnum.OWNER:
            raise ValidationError(detail='You do not have permission to update this company.')

        if self.partial:
            instance.status = not instance.status

        if self.update:
            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)

        instance.save()

        return instance

    @staticmethod
    def delete(instance, user_id):
        user_role = get_user_role_in_company(user_id=user_id, company_id=instance.id)
        if user_role != UserEnum.OWNER:
            raise ValidationError(detail='You do not have permission to delete this company.')

        instance.delete()


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
            invitation_status=InvitationEnum.ACCEPTED,
            request_status=InvitationEnum.ACCEPTED,
            role=UserEnum.OWNER
        )
        return company
