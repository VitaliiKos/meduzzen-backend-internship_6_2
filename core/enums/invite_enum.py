from enum import StrEnum, auto


class InviteStatusEnum(StrEnum):
    ACCEPTED = auto()
    DECLINED = auto()
    PENDING = auto()
    REVOKED = auto()
