from __future__ import annotations

from datetime import datetime

from matplotlib.pyplot import cool
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.market import SurveySize, TradeSymbol
from deltav.spacetraders.enums.ship import (
    ShipCrewRotation, 
    ShipEngines,
    ShipFrames,
    ShipModules,
    ShipMounts,
    ShipMountDeposits,
    ShipReactors,
    ShipRole
)
from deltav.spacetraders.enums.system import SystemType
from deltav.spacetraders.enums.waypoint import WaypointModifierSymbol, WaypointType
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.agent import AgentShape
from deltav.spacetraders.models.event import EventShape
from deltav.spacetraders.models.market import ShipTransactionShape
from deltav.spacetraders.models.waypoint import WaypointChartShape
from deltav.spacetraders.system import SystemWaypointShape


class ShipRegistrationShape(SpaceTradersAPIResShape):
    name: str
    faction_symbol: FactionSymbol
    role: ShipRole


class ShipNavRouteLocationShape(SpaceTradersAPIResShape):
    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int


class ShipNavRouteShape(SpaceTradersAPIResShape):
    destination: ShipNavRouteLocationShape
    origin: ShipNavRouteLocationShape
    departureTime: datetime
    arrival: datetime


class ShipNavShape(SpaceTradersAPIResShape):
    systemSymbol: str
    waypointSymbol: str
    route: ShipNavRouteShape
    status: str
    flightMode: str


class ShipCrewShape(SpaceTradersAPIResShape):
    current: int
    required: int
    capacity: int
    rotation: ShipCrewRotation
    morale: int
    wages: int

    
class ShipRequirementsShape(SpaceTradersAPIResShape):
    power: int
    crew: int
    slots: int


class ShipFrameShape(SpaceTradersAPIResShape):
    symbol: ShipFrames
    name: str
    condition: int
    integrity: int
    description: str
    module_slots: int
    mounting_points: int
    fuel_capacity: int
    requirements: ShipRequirementsShape
    quality: int


class ShipReactorShape(SpaceTradersAPIResShape):
    symbol: ShipReactors
    name: str
    condition: int
    integrity: int
    description: str
    power_output: int
    requirements: ShipRequirementsShape
    quality: int


class ShipEngineShape(SpaceTradersAPIResShape):
    symbol: ShipEngines
    name: str
    condition: int
    integrity: int
    description: str
    speed: int
    requirements: ShipRequirementsShape
    quality: int


class ShipModulesShape(SpaceTradersAPIResShape):
    symbol: ShipModules
    name: str
    description: str
    capacity: int
    range: int
    requirements: ShipRequirementsShape


class ShipMountsShape(SpaceTradersAPIResShape):
    symbol: ShipMounts
    name: str
    description: str
    strength: int
    deposits: list[ShipMountDeposits]
    requirements: ShipRequirementsShape


class ShipCargoInventoryShape(SpaceTradersAPIResShape):
    symbol: TradeSymbol
    name: str
    description: str
    units: int


class ShipCargoShape(SpaceTradersAPIResShape):
    capacity: int
    units: int
    inventory: ShipCargoInventoryShape


class ShipFuelConsumedShape(SpaceTradersAPIResShape):
    amount: int
    timestamp: datetime


class ShipFuelShape(SpaceTradersAPIResShape):
    current: int
    capacity: int
    consumed: ShipFuelConsumedShape


class ShipCooldownShape(SpaceTradersAPIResShape):
    ship_symbol: str
    total_seconds: int
    remaining_seconds: int
    expiration: datetime


class ShipShape(SpaceTradersAPIResShape):
    symbol: str
    registration: ShipRegistrationShape
    nav: ShipNavShape
    crew: ShipCrewShape
    frame: ShipFrameShape
    reactor: ShipReactorShape
    engine: ShipEngineShape
    modules: ShipModulesShape
    mounts: ShipMountsShape
    cargo: ShipCargoShape
    fuel: ShipFuelShape
    cooldown: ShipCooldownShape


class ShipTradeResourceShape(SpaceTradersAPIResShape):
    symbol: TradeSymbol
    units: int


class ShipExtractionShape(SpaceTradersAPIResShape):
    symbol: str
    result: ShipTradeResourceShape


class ShipExtractShape(SpaceTradersAPIResShape):
    extraction: ShipExtractionShape
    cooldown: ShipCooldownShape
    cargo: ShipCargoShape


class ShipExtractSurveyShape(SpaceTradersAPIResShape):
    signature: str
    symbol: str
    deposits: list[str]
    expiration: datetime
    size: SurveySize

class ShipExtractSurveyResponseShape(SpaceTradersAPIResShape):
    extraction: ShipExtractionShape
    cooldown: ShipCooldownShape
    cargo: ShipCargoShape
    modifiers: list[WaypointModifierSymbol]
    events: list[EventShape]


class ShipPurchaseShape(SpaceTradersAPIResShape):
    shipType: str
    waypointSymbol: str


class SuccessfulShipPurchaseShape(SpaceTradersAPIResShape):
    ship: ShipShape
    agent: AgentShape
    transaction: ShipTransactionShape


class ShipRefuelShape(SpaceTradersAPIResShape):
    units: int
    fromCargo: bool | None


class ShipRefuelResponseShape(SpaceTradersAPIResShape):
    agent: AgentShape
    fuel: ShipFuelShape
    cargo: ShipCargoShape
    transaction: ShipTransactionShape


class ShipCreateChartShape(SpaceTradersAPIResShape):
    chart: WaypointChartShape
    waypoint: SystemWaypointShape
    transaction: ShipTransactionShape
    agent: AgentShape


class ShipJumpShape(SpaceTradersAPIResShape):
    nav: ShipNavShape
    cooldown: ShipCooldownShape
    transaction: ShipTransactionShape
    agent: AgentShape


class ShipScanShipsShape(SpaceTradersAPIResShape):
    cooldown: ShipCooldownShape
    ships: list[ShipShape]

class ShipSystemShape(SpaceTradersAPIResShape):
    symbol: str
    sectorSymbol: str
    type: SystemType
    x: int
    y: int
    distance: int

class ShipScanSystemsShape(SpaceTradersAPIResShape):
    cooldown: ShipCooldownShape
    systems: list[ShipSystemShape]


class ShipRefineShape(SpaceTradersAPIResShape):
    produce: TradeSymbol


class ShipRefineResponseShape(SpaceTradersAPIResShape):
    cargo: ShipCargoShape
    cooldown: ShipCooldownShape
    produced: ShipTradeResourceShape
    consumed: ShipTradeResourceShape




