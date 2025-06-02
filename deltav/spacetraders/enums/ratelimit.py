from enum import Enum


class RateLimitType(Enum):
    IP_ADDRESS = 'IP Address'
    ACCOUNT = 'Account'  # TODO: Verify
    DDOS_PROTECTION = 'DDos Protection'  # TODO: Verify
