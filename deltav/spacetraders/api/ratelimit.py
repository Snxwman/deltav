from __future__ import annotations

from datetime import UTC, datetime
from typing import TypedDict

from deltav.spacetraders.enums.ratelimit import RateLimitType


class RatelimitHeaders(TypedDict):
    x_ratelimit_limit_burst: int
    x_ratelimit_limit_per_second: int
    x_ratelimit_remaining: int
    x_ratelimit_reset: str
    x_ratelimit_type: str


class Ratelimit:
    IP_ADDRESS_LIMIT_PER_SECOND: int = 2
    IP_ADDRESS_BURST_LIMIT: int = 30
    IP_ADDRESS_BURST_DURATION: int = 60

    ACCOUNT_LIMIT_PER_SECOND: int = 2
    ACCOUNT_BURST_LIMIT: int = 30
    ACCOUNT_BURST_DURATION: int = 60

    X_HEADERS: list[str] = [
        'X-Ratelimit-Limit-Burst',
        'X-Ratelimit-Limit-Per-Second',
        'X-Ratelimit-Remaining',
        'X-Ratelimit-Reset',
        'X-Ratelimit-Type',
    ]

    def __init__(self) -> None:
        self.limit_burst: int = 30
        self.limit_per_second: int = 2
        self.remaining: int = 2
        self.reset: datetime = datetime.now(tz=UTC)
        self.type: RateLimitType = RateLimitType.IP_ADDRESS

    def update(self, x_headers: RatelimitHeaders) -> None:
        self.limit_burst = x_headers['x_ratelimit_limit_burst']
        self.limit_per_second = x_headers['x_ratelimit_limit_per_second']
        self.remaining = x_headers['x_ratelimit_remaining']
        self.reset = datetime.fromisoformat(x_headers['x_ratelimit_reset'])

        if x_headers['x_ratelimit_type'] != self.type.value:
            self.type = RateLimitType(x_headers['x_ratelimit_type'])
