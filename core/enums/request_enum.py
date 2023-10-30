from enum import StrEnum, auto


class RequestStatusEnum(StrEnum):
    APPROVED = auto()
    REJECTED = auto()
    PENDING = auto()
    CANCELED = auto()
