from enum import StrEnum, auto


class RequestEnum(StrEnum):
    APPROVED = auto()
    REJECTED = auto()
    PENDING = auto()
    CANCELED = auto()
