from django.db import transaction
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import InviteModel, RequestModel
from core.enums.constants_enum import ConstantsEnum
from core.enums.invite_enum import InviteEnum
from core.enums.request_enum import RequestEnum
from core.enums.user_enum import UserEnum


def get_company_invitations_or_requests_list(company, invitation_status):
    if invitation_status == ConstantsEnum.INVITE:
        return EmployeeModel.objects.filter(company=company, role=UserEnum.CANDIDATE, invite_status__isnull=False)
    else:
        return EmployeeModel.objects.filter(company=company, role=UserEnum.CANDIDATE, request_status__isnull=False)


def get_company_invitation_or_request(employee, invitation_status):
    if invitation_status in [RequestEnum.APPROVE, RequestEnum.REJECTED]:
        return get_object_or_404(RequestModel, id=employee.request_status_id)
    elif invitation_status == InviteEnum.REVOKE:
        return get_object_or_404(InviteModel, id=employee.invite_status_id)


def get_user_invitation_or_request(employee, invitation_status):
    if invitation_status in [InviteEnum.ACCEPT, InviteEnum.DECLINE]:
        return get_object_or_404(InviteModel, id=employee.invite_status_id)
    else:
        return get_object_or_404(RequestModel, id=employee.request_status_id)


def get_user_invitations_or_requests_list(user: int, invitation_status: str):
    if invitation_status == ConstantsEnum.REQUEST:
        return EmployeeModel.objects.filter(user=user, role=UserEnum.CANDIDATE, request_status__isnull=False)
    else:
        return EmployeeModel.objects.filter(user=user, role=UserEnum.CANDIDATE, invite_status__isnull=False)


@transaction.atomic
def update_employee(employee, invitation_status, invite):
    if not invite or invite.status != InviteEnum.PENDING:
        return Response({'detail': 'Invalid invitation_status'}, status=status.HTTP_400_BAD_REQUEST)

    if invite.status in [RequestEnum.APPROVE, InviteEnum.ACCEPT]:
        employee.role = UserEnum.MEMBER
    else:
        employee.role = None

    invite.status = invitation_status
    employee.save()
    invite.save()
    return employee
