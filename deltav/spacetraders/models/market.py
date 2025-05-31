from __future__ import annotations
from datetime import datetime

from deltav.spacetraders.models import SpaceTradersAPIResShape

class CargoItemShape(SpaceTradersAPIResShape):
    symbol: str
    units: int

class TransactionShape(SpaceTradersAPIResShape):
    waypointSymbol: str
    shipSymbol: str
    tradeSymbol: str
    type: str
    units: int
    pricePerUnit: int
    totalPrice: int
    timestamp: datetime



