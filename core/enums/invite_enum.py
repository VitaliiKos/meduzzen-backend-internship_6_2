from enum import StrEnum, auto


class InviteEnum(StrEnum):
    ACCEPTED = auto()
    DECLINED = auto()
    PENDING = auto()
    REVOKED = auto()
