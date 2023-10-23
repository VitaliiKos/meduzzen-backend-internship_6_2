from enum import StrEnum, auto


class RequestEnum(StrEnum):
    ACCEPT = auto()
    DECLINE = auto()
    PENDING = auto()
    CANCEL = auto()
