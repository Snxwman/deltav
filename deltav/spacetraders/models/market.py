from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime

from deltav.spacetraders.enums.market import (
    ActivityLevel,
    MarketTradeGoodType,
    SupplyLevel,
    TradeSymbol,
    TransactionType,
)
from deltav.spacetraders.models import SpaceTradersAPIResShape


# FIX: Cargo Item Shape
class MarketShape(SpaceTradersAPIResShape):
    """

    symbol: str
    exports: list[MarketItemShape]
    imports: list[MarketItemShape]
    exchange: list[MarketItemShape]
    transactions: list[MarketTransactionShape]
    trade_goods: list[TradeGoodShape]
    """

    symbol: str
    exports: list[MarketItemShape]
    imports: list[MarketItemShape]
    exchange: list[MarketItemShape]
    transactions: list[MarketTransactionShape]
    trade_goods: list[TradeGoodShape]


class MarketItemShape(SpaceTradersAPIResShape):
    """

    symbol: TradeSymbol
    name: str
    description: str
    """

    symbol: TradeSymbol
    name: str
    description: str


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


class MarketTransactionShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: TradeSymbol
    type: TransactionType
    units: int
    price_per_unit: int
    total_price: int
    timestamp: datetime
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: TradeSymbol
    type: TransactionType
    units: int
    price_per_unit: int
    total_price: int
    timestamp: datetime


class MarketSupplyChainAdditionalPropertiesShape(SpaceTradersAPIResShape):
    ANY_ADDITIONAL_PROPERTY: list[str]


class MarketSupplyChainShape(SpaceTradersAPIResShape):
    export_to_import_map: Mapping[TradeSymbol, list[TradeSymbol]]  # TODO: Verify
