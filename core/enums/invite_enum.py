from enum import StrEnum, auto


class InviteEnum(StrEnum):
    APPROVE = auto()
    REJECTED = auto()
    PENDING = auto()
    CANCEL = auto()
