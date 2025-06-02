from __future__ import annotations

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.market import TradeSymbol
from deltav.spacetraders.enums.ship import ShipType
from deltav.spacetraders.enums.system import SystemType
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.market import CargoItemShape, ShipTransactionShape, TradeGoodShape, TransactionShape
from deltav.spacetraders.models.ship import ShipCargoShape, ShipShape
from deltav.spacetraders.models.waypoint import SystemWaypointShape


class ShipyardShape(SpaceTradersAPIResShape):
    symbol: str
    ship_types: list[ShipType]
    transactions: list[ShipTransactionShape]
    ships: list[ShipShape]
    modifications_fee: int


class MarketShape(SpaceTradersAPIResShape):
    symbol: str
    exports: list[CargoItemShape]
    imports: list[CargoItemShape]
    exchange: list[CargoItemShape]
    transactions: list[TransactionShape]
    trade_goods: list[TradeGoodShape]


class JumpgateShape(SpaceTradersAPIResShape):
    symbol: str
    connections: list[str]


class SystemShape(SpaceTradersAPIResShape):
    constellation: str
    symbol: str
    sector_symbol: str
    type: SystemType
    x: int
    y: int
    waypoints: list[SystemWaypointShape]
    factions: list[FactionSymbol]
    name: str


class ConstructionMaterialShape(SpaceTradersAPIResShape):
    trade_symbol: TradeSymbol
    required: int
    fulfilled: int


class ConstructionSiteShape(SpaceTradersAPIResShape):
    symbol: str
    materials: list[ConstructionMaterialShape]
    is_complete: bool


class SupplyConstructionSiteShape(SpaceTradersAPIResShape):
    ship_symbol: str
    trade_symbol: TradeSymbol
    units: int


class SupplyConstructionSiteResponseShape(SpaceTradersAPIResShape):
    construction: ConstructionSiteShape
    cargo: ShipCargoShape
