from enum import StrEnum, auto


class InviteEnum(StrEnum):
    ACCEPT = auto()
    DECLINE = auto()
    PENDING = auto()
    REVOKE = auto()
