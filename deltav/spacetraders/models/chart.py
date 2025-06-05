from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.models import SpaceTradersAPIResShape


class ChartShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    submitted_by: str
    submitted_on: datetime
    """

    waypoint_symbol: str
    submitted_by: str
    submitted_on: datetime


class ChartTransactionShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    ship_symbol: str
    total_price: int
    timestamp: datetime
    """

    waypoint_symbol: str
    ship_symbol: str
    total_price: int
    timestamp: datetime
