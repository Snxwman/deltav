from __future__ import annotations
from datetime import datetime
from typing import Any

from deltav.spacetraders.models import SpaceTradersAPIResShape


class EventShape(SpaceTradersAPIResShape):
    id: str
    type: str
    message: str
    data: Any
    created_at: datetime
