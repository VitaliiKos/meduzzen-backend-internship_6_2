from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import InviteModel, RequestModel
from core.enums.invite_enum import InviteEnum
from core.enums.request_enum import RequestEnum
from core.enums.user_enum import UserEnum


def check_invite_status(invite, expected_status) -> Response:
    if invite.status != expected_status:
        return Response({'detail': 'Unable to update'}, status=status.HTTP_400_BAD_REQUEST)


def get_employee_invitation(company, invitation_status):
    if invitation_status == 'invite':
        return EmployeeModel.objects.filter(company=company, role=UserEnum.CANDIDATE, invite_status__isnull=False)
    else:
        return EmployeeModel.objects.filter(company=company, role=UserEnum.CANDIDATE, request_status__isnull=False)


def get_invite_by_status(employee, invitation_status):
    if invitation_status in [RequestEnum.ACCEPT, RequestEnum.DECLINE]:
        return get_object_or_404(RequestModel, id=employee.request_status_id)
    else:
        return get_object_or_404(InviteModel, id=employee.invite_status_id)


def get_user_invite_by_status(employee, invitation_status):
    if invitation_status in [InviteEnum.APPROVE, InviteEnum.REJECTED]:
        return get_object_or_404(InviteModel, id=employee.invite_status_id)
    else:
        return get_object_or_404(RequestModel, id=employee.request_status_id)


def process_invitation_update(employee, invite, invitation_status):
    match invitation_status:
        case RequestEnum.ACCEPT:
            employee.role = UserEnum.MEMBER
            invite.status = RequestEnum.ACCEPT
        case RequestEnum.DECLINE:
            employee.role = None
            invite.status = RequestEnum.DECLINE
        case InviteEnum.APPROVE:
            employee.role = UserEnum.MEMBER
            invite.status = InviteEnum.APPROVE
        case InviteEnum.REJECTED:
            employee.role = None
            invite.status = InviteEnum.REJECTED
        case InviteEnum.CANCEL:
            employee.role = None
            invite.status = InviteEnum.CANCEL
        case _:
            return Response({'detail': 'Unable to update'}, status=status.HTTP_400_BAD_REQUEST)


def get_user_invitation(user: int, invitation_status: str):
    if invitation_status == 'request':
        return EmployeeModel.objects.filter(user=user, role=UserEnum.CANDIDATE, request_status__isnull=False)
    else:
        return EmployeeModel.objects.filter(user=user, role=UserEnum.CANDIDATE, invite_status__isnull=False)
