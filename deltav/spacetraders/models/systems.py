from __future__ import annotations

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.market import TradeSymbol
from deltav.spacetraders.enums.ship import ShipType
from deltav.spacetraders.enums.system import SystemType
from deltav.spacetraders.enums.waypoint import WaypointModifierSymbol, WaypointType
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.market import CargoItemShape, ShipTransactionShape, TradeGoodShape, TransactionShape
from deltav.spacetraders.models.ship import ShipCargoShape, ShipShape
from deltav.spacetraders.models.waypoint import WaypointChartShape, WaypointTraitShape


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


class SystemShape(SpaceTradersAPIResShape):
    constellation: str
    symbol: str
    sectorSymbol: str
    type: SystemType
    x: int
    y: int
    waypoints: list[SystemWaypointShape]
    factions: list[FactionSymbol]
    name: str


class SystemWaypointModifierShape(SpaceTradersAPIResShape):
    symbol: WaypointModifierSymbol
    name: str
    description: str


class SystemWaypointShape(SpaceTradersAPIResShape):
    symbol: str
    type: WaypointType
    systemSymbol: str
    x: int
    y: int
    orbitals: list[str]
    orbits: str
    factionSymbol: FactionSymbol 
    traits: list[WaypointTraitShape]
    modifiers: list[SystemWaypointModifierShape]
    chart: WaypointChartShape
    isUnderConstruction: bool


class ConstructionMaterialShape(SpaceTradersAPIResShape):
    tradeSymbol: TradeSymbol
    required: int
    fulfilled: int


class ConstructionSiteShape(SpaceTradersAPIResShape):
    symbol: str
    materials: list[ConstructionMaterialShape]
    isComplete: bool


class SupplyConstructionSiteShape(SpaceTradersAPIResShape):
    shipSymbol: str
    tradeSymbol: TradeSymbol
    units: int
    

class SupplyConstructionSiteResponseShape(SpaceTradersAPIResShape):
    construction: ConstructionSiteShape
    cargo: ShipCargoShape
