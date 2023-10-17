from enum import StrEnum, auto


class UserEnum(StrEnum):
    OWNER = auto()
    CANDIDATE = auto()
    EMPLOYEE = auto()
    MEMBER = auto()
    FORMER = auto()
