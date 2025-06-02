from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.enums.market import ActivityLevel, MarketTradeGoodType, SupplyLevel
from deltav.spacetraders.enums.ship import ShipType
from deltav.spacetraders.models import SpaceTradersAPIResShape


class CargoItemShape(SpaceTradersAPIResShape):
    """

    symbol: str
    units: int
    description: str | None
    """

    symbol: str
    units: int
    description: str | None


class TransactionShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: str
    type: str
    units: int
    price_per_unit: int
    total_price: int
    timestamp: datetime
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: str
    type: str
    units: int
    price_per_unit: int
    total_price: int
    timestamp: datetime


class ShipTransactionShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    ship_type: ShipType
    price: int
    agent_symbol: str
    timestamp: datetime
    """

    waypoint_symbol: str
    ship_type: ShipType
    price: int
    agent_symbol: str
    timestamp: datetime


class TradeGoodShape(SpaceTradersAPIResShape):
    """

    symbol: str
    type: MarketTradeGoodType
    trade_volume: int
    supply: SupplyLevel
    activity: ActivityLevel
    purchase_price: int
    sell_price: int
    """

    symbol: str
    type: MarketTradeGoodType
    trade_volume: int
    supply: SupplyLevel
    activity: ActivityLevel
    purchase_price: int
    sell_price: int
