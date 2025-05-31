from __future__ import annotations
from datetime import datetime

from deltav.spacetraders.enums.market import ActivityLevel, MarketTradeGoodType, SupplyLevel
from deltav.spacetraders.enums.ship import ShipType
from deltav.spacetraders.models import SpaceTradersAPIResShape

class CargoItemShape(SpaceTradersAPIResShape):
    symbol: str
    units: int
    description: str | None


class TransactionShape(SpaceTradersAPIResShape):
    waypointSymbol: str
    shipSymbol: str
    tradeSymbol: str
    type: str
    units: int
    pricePerUnit: int
    totalPrice: int
    timestamp: datetime


class ShipTransactionShape(SpaceTradersAPIResShape):
    waypointSymbol: str
    shipType: ShipType
    price: int
    agentSymbol: str
    timestamp: datetime


class TradeGoodShape(SpaceTradersAPIResShape):
    symbol: str
    type: MarketTradeGoodType
    tradeVolume: int
    supply: SupplyLevel
    activity: ActivityLevel
    purchasePrice: int
    sellPrice: int

