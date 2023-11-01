from rest_framework.exceptions import APIException

from core.enums.invite_enum import InviteStatusEnum
from core.enums.request_enum import RequestStatusEnum
from core.enums.user_enum import UserEnum


def select_role(status):
    if status in [RequestStatusEnum.APPROVED.value, InviteStatusEnum.ACCEPTED.value]:
        role = UserEnum.MEMBER.value
    elif status in [RequestStatusEnum.REJECTED.value, InviteStatusEnum.DECLINED.value]:
        role = None
    else:
        raise APIException("Bad Request. Invalid request_status.")
    return role
