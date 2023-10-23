from enum import StrEnum, auto


class UserEnum(StrEnum):
    OWNER = auto()
    CANDIDATE = auto()
    MEMBER = auto()
