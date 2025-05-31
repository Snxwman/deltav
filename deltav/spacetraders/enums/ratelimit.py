from enum import Enum, auto


class RateLimitType(Enum):
    IP_ADDRESS = auto()
    ACCOUNT = auto()
    DDOS_PROTECTION = auto()

