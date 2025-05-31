from __future__ import annotations
from hmac import trans_36

from deltav.spacetraders.enums.ship import ShipType
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.market import CargoItemShape, ShipTransactionShape, TradeGoodShape, TransactionShape
from deltav.spacetraders.models.ship import ShipShape


class ShipyardShape(SpaceTradersAPIResShape):
    symbol: str
    shipTypes: list[ShipType]
    transactions: list[ShipTransactionShape]
    ships: list[ShipShape]
    modificationsFee: int

class MarketShape(SpaceTradersAPIResShape):
    symbol: str
    exports: list[CargoItemShape]
    imports: list[CargoItemShape]
    exchange: list[CargoItemShape]
    transactions: list[TransactionShape]
    tradeGoods: list[TradeGoodShape]

class JumpgateShape(SpaceTradersAPIResShape):
    symbol: str
    connections: list[str]
