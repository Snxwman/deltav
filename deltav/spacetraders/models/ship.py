from __future__ import annotations

from datetime import datetime

from pydantic import Field

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.market import SurveySize, TradeSymbol, TransactionType
from deltav.spacetraders.enums.ship import (
    ShipComponent,
    ShipConditionEvent,
    ShipCrewRotationShape,
    ShipEngines,
    ShipFrames,
    ShipModules,
    ShipMountDeposits,
    ShipMounts,
    ShipNavFlightMode,
    ShipReactors,
    ShipRole,
    ShipType,
)
from deltav.spacetraders.enums.system import SystemType
from deltav.spacetraders.enums.waypoint import WaypointModifierSymbol, WaypointType
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models.agent import AgentShape
from deltav.spacetraders.models.market import TransactionShape
from deltav.spacetraders.models.waypoint import WaypointShape


class CargoItemReqShape(SpaceTradersAPIReqShape):
    """

    symbol: TradeSymbol
    units: int
    """

    symbol: TradeSymbol
    units: int


class CargoItemResShape(SpaceTradersAPIResShape):
    """

    symbol: TradeSymbol
    units: int
    """

    symbol: TradeSymbol
    units: int


class ExtractionShape(SpaceTradersAPIResShape):
    """

    ship_symbol: str
    extration_yield: CargoItemResShape = Field(alias='yield')
    """

    ship_symbol: str
    extration_yield: CargoItemResShape = Field(alias='yield')


class ShipShape(SpaceTradersAPIResShape):
    """

    symbol: str
    registration: ShipRegistrationShape
    nav: ShipNavShape
    crew: ShipCrewShape
    frame: ShipFrameShape
    reactor: ShipReactorShape
    engine: ShipEngineShape
    modules: list[ShipModuleShape]
    mounts: list[ShipMountShape]
    cargo: ShipCargoShape
    fuel: ShipFuelShape
    cooldown: ShipCooldownShape
    """

    symbol: str
    registration: ShipRegistrationShape
    nav: ShipNavShape
    crew: ShipCrewShape
    frame: ShipFrameShape
    reactor: ShipReactorShape
    engine: ShipEngineShape
    modules: list[ShipModuleShape] = []
    mounts: list[ShipMountShape] = []
    cargo: ShipCargoShape
    fuel: ShipFuelShape
    cooldown: ShipCooldownShape


class ShipsShape(SpaceTradersAPIResShape):
    """

    ships: list[ShipShape]
    """

    ships: list[ShipShape] = Field(alias='data')


class ShipCargoShape(SpaceTradersAPIResShape):
    """

    capacity: int
    units: int
    inventory: list[ShipCargoInventoryShape]
    """

    capacity: int
    units: int
    inventory: list[ShipCargoInventoryShape]


class ShipCargoInventoryShape(SpaceTradersAPIResShape):
    """

    symbol: TradeSymbol
    name: str
    description: str
    units: int
    """

    symbol: TradeSymbol
    name: str
    description: str
    units: int


class ShipCargoItemShape(SpaceTradersAPIResShape):
    """

    symbol: str
    units: int
    description: str
    """

    symbol: str
    units: int
    description: str


class ShipCargoTransferReqShape(SpaceTradersAPIReqShape):
    """

    trade_symbol: TradeSymbol
    units: int
    ship_symbol: str
    """

    trade_symbol: TradeSymbol
    units: int
    ship_symbol: str


class ShipCargoTransferResShape(SpaceTradersAPIResShape):
    """

    cargo: ShipCargoShape
    target_cargo: ShipCargoShape
    """

    cargo: ShipCargoShape
    target_cargo: ShipCargoShape


class ShipCooldownShape(SpaceTradersAPIResShape):
    """

    ship_symbol: str
    total_seconds: int
    remaining_seconds: int
    expiration: datetime
    """

    ship_symbol: str
    total_seconds: int = 0
    remaining_seconds: int = 0
    expiration: datetime = datetime.now()


class ShipCrewShape(SpaceTradersAPIResShape):
    """

    current: int
    required: int
    capacity: int
    rotation: ShipCrewRotationShape
    morale: int
    wages: int
    """

    current: int
    required: int
    capacity: int
    rotation: ShipCrewRotationShape
    morale: int
    wages: int


class ShipEngineShape(SpaceTradersAPIResShape):
    """

    symbol: ShipEngines
    name: str
    condition: int
    integrity: int
    description: str
    speed: int
    requirements: ShipRequirementsShape
    quality: int
    """

    symbol: ShipEngines
    name: str
    condition: int
    integrity: int
    description: str
    speed: int
    requirements: ShipRequirementsShape
    quality: int


class ShipEventShape(SpaceTradersAPIResShape):
    """

    symbol: ShipConditionEvent
    component: ShipComponent
    name: str
    description: str
    """

    symbol: ShipConditionEvent
    component: ShipComponent
    name: str
    description: str


# FIX: Circular. Something not right
class ShipExtractionShape(SpaceTradersAPIResShape):
    """

    extraction: ShipExtractionShape
    cooldown: ShipCooldownShape
    cargo: ShipCargoShape
    modifiers: list[WaypointModifierSymbol]
    events: list[ShipEventShape]
    """

    extraction: ExtractionShape
    cooldown: ShipCooldownShape
    cargo: ShipCargoShape
    modifiers: list[WaypointModifierSymbol]
    events: list[ShipEventShape]


class ShipFlightModeShape(SpaceTradersAPIReqShape):
    """

    flight_mode: ShipNavFlightMode
    """

    flight_mode: ShipNavFlightMode


class ShipFrameShape(SpaceTradersAPIResShape):
    """

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
    """

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


class ShipFuelShape(SpaceTradersAPIResShape):
    """

    current: int
    capacity: int
    consumed: ShipFuelConsumedShape
    """

    current: int
    capacity: int
    consumed: ShipFuelConsumedShape


class ShipFuelConsumedShape(SpaceTradersAPIResShape):
    """

    amount: int
    timestamp: datetime
    """

    amount: int
    timestamp: datetime


class ShipJumpResShape(SpaceTradersAPIResShape):
    """

    nav: ShipNavShape
    cooldown: ShipCooldownShape
    transaction: TransactionShape
    agent: AgentShape
    """

    nav: ShipNavShape
    cooldown: ShipCooldownShape
    transaction: TransactionShape
    agent: AgentShape


class ShipModifyModuleShape(SpaceTradersAPIResShape):
    """

    agent: AgentShape
    modules: list[ShipModuleShape]
    cargo: ShipCargoShape
    transaction: ShipModifyTransactionShape
    """

    agent: AgentShape
    modules: list[ShipModuleShape]
    cargo: ShipCargoShape
    transaction: ShipModifyTransactionShape


class ShipModifyMountShape(SpaceTradersAPIResShape):
    """

    agent: AgentShape
    mounts: list[ShipModuleShape]
    cargo: ShipCargoShape
    transaction: ShipModifyTransactionShape
    """

    agent: AgentShape
    mounts: list[ShipModuleShape]
    cargo: ShipCargoShape
    transaction: ShipModifyTransactionShape


class ShipModifyTransactionShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: TradeSymbol
    total_price: int
    timestamp: datetime
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: TradeSymbol
    total_price: int
    timestamp: datetime


class ShipModuleShape(SpaceTradersAPIResShape):
    """

    symbol: ShipModules
    name: str
    description: str
    capacity: int
    range: int
    requirements: ShipRequirementsShape
    """

    symbol: ShipModules
    name: str
    description: str
    capacity: int = 0
    range: int = 0
    requirements: ShipRequirementsShape


class ShipModulesShape(SpaceTradersAPIResShape):
    """

    modules: list[ShipModuleShape] = Field(alias='data')
    """

    modules: list[ShipModuleShape] = Field(alias='data')


class ShipModuleSymbolShape(SpaceTradersAPIReqShape):
    """

    symbol: ShipModules
    """

    symbol: ShipModules


class ShipMountShape(SpaceTradersAPIResShape):
    """

    symbol: ShipMounts
    name: str
    description: str
    strength: int
    deposits: list[ShipMountDeposits]
    requirements: ShipRequirementsShape
    """

    symbol: ShipMounts
    name: str
    description: str
    strength: int = 0
    deposits: list[ShipMountDeposits] = []
    requirements: ShipRequirementsShape


class ShipMountsShape(SpaceTradersAPIResShape):
    """

    modules: list[ShipMountShape] = Field(alias='data')
    """

    modules: list[ShipMountShape] = Field(alias='data')


class ShipMountSymbolShape(SpaceTradersAPIReqShape):
    """

    symbol: ShipMounts
    """

    symbol: ShipMounts


class ShipNavigationShape(SpaceTradersAPIResShape):
    """

    nav: ShipNavShape
    fuel: ShipFuelShape
    event: ShipEventShape
    """

    nav: ShipNavShape
    fuel: ShipFuelShape
    event: ShipEventShape


class ShipNavShape(SpaceTradersAPIResShape):
    """

    system_symbol: str
    waypoint_symbol: str
    route: ShipNavRouteShape
    status: str
    flight_mode: str
    """

    system_symbol: str
    waypoint_symbol: str
    route: ShipNavRouteShape
    status: str
    flight_mode: str


class ShipNavRouteShape(SpaceTradersAPIResShape):
    """

    destination: ShipNavRouteLocationShape
    origin: ShipNavRouteLocationShape
    departure_time: datetime
    arrival: datetime
    """

    destination: ShipNavRouteLocationShape
    origin: ShipNavRouteLocationShape
    departure_time: datetime
    arrival: datetime


class ShipNavRouteLocationShape(SpaceTradersAPIResShape):
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int


class ShipNavUpdateShape(SpaceTradersAPIResShape):
    """

    nav: ShipNavShape
    fuel: ShipFuelShape
    events: list[ShipEventShape]
    """

    nav: ShipNavShape
    fuel: ShipFuelShape
    events: list[ShipEventShape]


class ShipPurchaseReqShape(SpaceTradersAPIReqShape):
    """

    ship_type: str
    waypoint_symbol: str
    """

    ship_type: ShipType
    waypoint_symbol: str


class ShipPurchaseTransactionShape(SpaceTradersAPIReqShape):
    waypoint_symbol: str
    ship_type: ShipType
    price: int
    agent_symbol: str
    timestamp: datetime


class ShipPurchaseResShape(SpaceTradersAPIResShape):
    """

    ship: ShipShape
    agent: AgentShape
    transaction: ShipPurchaseTransactionShape
    """

    ship: ShipShape
    agent: AgentShape
    transaction: ShipPurchaseTransactionShape


class ShipReactorShape(SpaceTradersAPIResShape):
    """

    symbol: ShipReactors
    name: str
    condition: int
    integrity: int
    description: str
    power_output: int
    requirements: ShipRequirementsShape
    quality: int
    """

    symbol: ShipReactors
    name: str
    condition: int
    integrity: int
    description: str
    power_output: int
    requirements: ShipRequirementsShape
    quality: int


class ShipRefineReqShape(SpaceTradersAPIReqShape):
    """

    produce: TradeSymbol
    """

    produce: TradeSymbol


class ShipRefineResShape(SpaceTradersAPIResShape):
    """

    cargo: ShipCargoShape
    cooldown: ShipCooldownShape
    produced: CargoItemResShape
    consumed: CargoItemResShape
    """

    cargo: ShipCargoShape
    cooldown: ShipCooldownShape
    produced: CargoItemResShape
    consumed: CargoItemResShape


class ShipRefuelReqShape(SpaceTradersAPIReqShape):
    """

    units: int
    from_cargo: bool
    """

    units: int
    from_cargo: bool


class ShipRefuelTransactionShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: TradeSymbol
    type: TransactionType
    total_price: int
    units: int
    timestamp: datetime
    """

    waypoint_symbol: str
    ship_symbol: str
    trade_symbol: TradeSymbol
    type: TransactionType
    total_price: int
    units: int
    timestamp: datetime


class ShipRefuelResShape(SpaceTradersAPIResShape):
    """

    agent: AgentShape
    fuel: ShipFuelShape
    cargo: ShipCargoShape
    transaction: ShipShape
    """

    agent: AgentShape
    fuel: ShipFuelShape
    cargo: ShipCargoShape
    transaction: ShipRefuelTransactionShape


class ShipRegistrationShape(SpaceTradersAPIResShape):
    """

    name: str
    faction_symbol: FactionSymbol
    role: ShipRole
    """

    name: str
    faction_symbol: FactionSymbol
    role: ShipRole


class ShipRequirementsShape(SpaceTradersAPIResShape):
    """

    power: int
    crew: int
    slots: int
    """

    power: int = 0
    crew: int = 0
    slots: int = 0


class ShipRepairShape(SpaceTradersAPIResShape):
    """

    agent: AgentShape
    ship: ShipShape
    transaction: ShipScrapTransactionShape
    """

    agent: AgentShape
    ship: ShipShape
    transaction: ShipScrapTransactionShape


class ShipRepairTransactionShape(SpaceTradersAPIResShape):
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


class ShipScrapShape(SpaceTradersAPIResShape):
    """

    agent: AgentShape
    transaction: ScrapShipTransactionShape
    """

    agent: AgentShape
    transaction: ShipScrapTransactionShape


class ShipScrapTransactionShape(SpaceTradersAPIResShape):
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


class ShipSystemShape(SpaceTradersAPIResShape):
    """

    symbol: str
    sector_symbol: str
    type: SystemType
    x: int
    y: int
    distance: int
    """

    symbol: str
    sector_symbol: str
    type: SystemType
    x: int
    y: int
    distance: int


class SurveyCreateShape(SpaceTradersAPIResShape):
    """

    cooldown: ShipCooldownShape
    surveys: list[SurveyResShape]
    """

    cooldown: ShipCooldownShape
    surveys: list[SurveyResShape]


class SurveyDepositShape(SpaceTradersAPIResShape):
    """

    symbol: TradeSymbol
    """

    symbol: TradeSymbol


class SurveyReqShape(SpaceTradersAPIReqShape):
    """

    signature: str
    symbol: str
    deposits: list[SurveyDepositShape]
    expiration: datetime
    size: SurveySize
    """

    signature: str
    symbol: str
    deposits: list[SurveyDepositShape]
    expiration: datetime
    size: SurveySize


class SurveyResShape(SpaceTradersAPIResShape):
    """

    signature: str
    symbol: str
    deposits: list[SurveyDepositShape]
    expiration: datetime
    size: SurveySize
    """

    signature: str
    symbol: str
    deposits: list[SurveyDepositShape]
    expiration: datetime
    size: SurveySize


class ScanShipsShape(SpaceTradersAPIResShape):
    """

    cooldown: ShipCooldownShape
    ships: list[ShipShape]
    """

    cooldown: ShipCooldownShape
    ships: list[ShipShape]


class ScanSystemsShape(SpaceTradersAPIResShape):
    """

    cooldown: ShipCooldownShape
    systems: list[ShipSystemShape]
    """

    cooldown: ShipCooldownShape
    systems: list[ShipSystemShape]


class ScanWaypointsShape(SpaceTradersAPIResShape):
    """

    cooldown: ShipCooldownShape
    waypoints: list[WaypointShape]
    """

    cooldown: ShipCooldownShape
    waypoints: list[WaypointShape]


class SiphonShape(SpaceTradersAPIResShape):
    """

    ship_symbol: str
    siphon_yield: CargoItemResShape = Field(alias='yield')
    """

    ship_symbol: str
    siphon_yield: CargoItemResShape = Field(alias='yield')


class SiphonResShape(SpaceTradersAPIResShape):
    """

    siphon: SiphonShape
    cooldown: ShipCooldownShape
    cargo: ShipCargoShape
    events: list[ShipEventShape]
    """

    siphon: SiphonShape
    cooldown: ShipCooldownShape
    cargo: ShipCargoShape
    events: list[ShipEventShape]
