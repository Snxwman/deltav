from datetime import datetime

from deltav.spacetraders.enums.ratelimit import RateLimitType


class Ratelimit():
    # TODO: Evaluate if x_headers should get its own type
    def __init__(self) -> None:
        self.type: RateLimitType = RateLimitType.IP_ADDRESS
        self.reset: datetime = datetime.now()
        self.burst: int = 30
        self.per_second: int = 2
        self.remaining: int = 2


    def update(self, x_headers: dict[str, str]) -> None:
        self.type = RateLimitType(x_headers['X-Ratelimit-Type'])
        self.reset = datetime.fromisoformat(x_headers['X-Ratelimit-Reset'])
        self.burst = int(x_headers['X-Ratelimit-Limit-Burst'])
        self.per_second = int(x_headers['X-Ratelimit-Limit-Per-Second'])
        self.remaining = int(x_headers['X-Ratelimit-Remaining'])
