from enum import Enum


class UserEnum(Enum):
    OWNER = 'owner'
    MANAGER = 'manager'
    EMPLOYEE = 'employee'
    MEMBER = 'member'
    REQUEST_OPTION = 'get_option'
