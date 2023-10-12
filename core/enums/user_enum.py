from enum import StrEnum, auto


class UserEnum(StrEnum):
    OWNER = auto()
    MANAGER = auto()
    EMPLOYEE = auto()
    MEMBER = auto()
