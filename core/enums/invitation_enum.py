from enum import StrEnum, auto


class InvitationEnum(StrEnum):
    ACCEPTED = auto()
    REJECTED = auto()
    PENDING = auto()
