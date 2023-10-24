from enum import StrEnum, auto


class RequestEnum(StrEnum):
    APPROVE = auto()
    REJECTED = auto()
    PENDING = auto()
    CANCEL = auto()
