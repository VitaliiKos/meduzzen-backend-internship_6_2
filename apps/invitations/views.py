from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.employee.models import EmployeeModel
from apps.companies.employee.serializers import EmployeeListSerializer, EmployeeSerializer
from apps.companies.models import CompanyModel
from apps.invitations.helper import (
    check_invite_status,
    get_employee_invitation,
    get_invite_by_status,
    get_user_invitation,
    get_user_invite_by_status,
    process_invitation_update,
)
from apps.invitations.serializers import InviteModelSerializer, RequestModelSerializer
from apps.users.models import UserModel as User
from core.enums.invite_enum import InviteEnum
from core.enums.request_enum import RequestEnum
from core.enums.user_enum import UserEnum
from core.permisions.is_company_owner import IsCompanyOwnerPermission

UserModel: User = get_user_model()


class CompanyInviteActionsView(ListCreateAPIView, RetrieveUpdateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = InviteModelSerializer
    permission_classes = (IsAuthenticated, IsCompanyOwnerPermission)

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        company = self.get_object()

        if company.has_member(user_id):
            return Response({'detail': 'Candidate have already relation to this company'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializers_data = {
            "user": user_id,
            "company": company.id,
            "status": InviteEnum.PENDING,
        }
        serializer = self.get_serializer(data=serializers_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        company = self.get_object()
        invitation_status = self.request.data.get('invitation_status', 'invite')
        company_invitation = get_employee_invitation(company, invitation_status)
        return self.paginate_and_serialize(company_invitation, EmployeeListSerializer)

    def update(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        company = self.get_object()
        invitation_status = self.request.data.get('invitation_status')
        employee = get_object_or_404(EmployeeModel, company=company.id, user=user_id)
        invite = get_invite_by_status(employee, invitation_status)
        check_invite_status(invite, InviteEnum.PENDING)
        process_invitation_update(employee, invite, invitation_status)

        invite.save()
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def paginate_and_serialize(self, data, serializer_class):
        page = self.paginate_queryset(data)
        serializer = serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class UserRequestActionsView(ListCreateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = RequestModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = self.request.user.id
        company = self.get_object()
        if company.has_member(user):
            return Response({'detail': 'Candidate have already relation to this company'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializers_data = {
            "user": user,
            "company": company.id,
            "status": RequestEnum.PENDING
        }
        serializer = self.get_serializer(data=serializers_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        invitation_status = self.request.data.get('invitation_status', 'request')
        user_invitation = get_user_invitation(user=request.user.id, invitation_status=invitation_status)
        page = self.paginate_queryset(user_invitation)
        serializer = EmployeeSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class UserInvitationDetailActionsView(RetrieveUpdateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        invitation_status = self.request.data.get('invitation_status', InviteEnum.APPROVE)
        filter_kwargs = {
            'user': user,
            'role': UserEnum.CANDIDATE
        }
        if invitation_status in [InviteEnum.APPROVE, InviteEnum.REJECTED]:
            filter_kwargs['invite_status__isnull'] = False
        else:
            filter_kwargs['request_status__isnull'] = False
        invitations = EmployeeModel.objects.filter(**filter_kwargs)
        return invitations

    def update(self, request, *args, **kwargs):
        invitation_status = self.request.data.get('invitation_status')
        employee = self.get_object()
        invite = get_user_invite_by_status(employee, invitation_status)
        check_invite_status(invite, RequestEnum.PENDING)
        process_invitation_update(employee, invite, invitation_status)
        invite.save()
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

