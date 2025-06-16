from __future__ import annotations

from typing import TYPE_CHECKING

from deltav.spacetraders.models import SpaceTradersAPIResShape

if TYPE_CHECKING:
    from datetime import datetime


class ChartShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    submitted_by: str
    submitted_on: datetime
    """

    waypoint_symbol: str
    submitted_by: str
    submitted_on: datetime
