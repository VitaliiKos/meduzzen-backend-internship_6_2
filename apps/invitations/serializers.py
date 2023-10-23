from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import InviteModel, RequestModel
from core.enums.user_enum import UserEnum


class InviteModelSerializer(ModelSerializer):
    class Meta:
        model = InviteModel
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data: dict):
        user = validated_data.pop('user')
        company = validated_data.pop('company')
        invite_status = validated_data.pop('status')
        data = {'user': user, 'company': company, 'status': invite_status}
        company_invite = InviteModel.objects.create(**data)

        employee, created = EmployeeModel.objects.get_or_create(
            user=user,
            company=company,
            defaults={
                'role': UserEnum.CANDIDATE,
                'invite_status': company_invite}
        )

        if not created:
            employee.role = UserEnum.CANDIDATE
            employee.invite_status = company_invite
            employee.save()

        return company_invite


class RequestModelSerializer(ModelSerializer):
    class Meta:
        model = RequestModel
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data: dict):
        user = validated_data.pop('user')
        company = validated_data.pop('company')
        request_status = validated_data.pop('status')
        data = {'user': user, 'company': company, 'status': request_status}
        user_request = RequestModel.objects.create(**data)

        employee, created = EmployeeModel.objects.get_or_create(
            user=user,
            company=company,
            defaults={
                'role': UserEnum.CANDIDATE,
                'request_status': user_request
            }
        )
        if not created:
            employee.role = UserEnum.CANDIDATE
            employee.request_status = user_request
            employee.save()

        return user_request
