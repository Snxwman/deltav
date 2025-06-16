from __future__ import annotations

from enum import Enum


class RateLimitType(Enum):
    """

    ACCOUNT
    DDOS_PROTECTION
    IP_ADDRESS
    """

    ACCOUNT = 'Account'  # TODO: Verify
    DDOS_PROTECTION = 'DDos Protection'  # TODO: Verify
    IP_ADDRESS = 'IP Address'
