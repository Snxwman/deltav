from __future__ import annotations
from typing import Any

from deltav.spacetraders.models import SpaceTradersAPIResShape


class ErrorShape(SpaceTradersAPIResShape):
    code: int
    message: str
    data: dict[Any, Any]  # pyright: ignore[reportExplicitAny]
    request_id: str

class HttpErrorShape(SpaceTradersAPIResShape):
    message: str
    error: str
    status_code: int