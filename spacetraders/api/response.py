from datetime import datetime
from typing import TypedDict

from spacetraders.api.enums import (
    ContractType,
    FactionSymbol,
    FactionTraitSymbol,
    ShipCrewRotation,
    ShipEngines,
    ShipFrames,
    ShipModules,
    ShipMountDeposits,
    ShipMounts,
    ShipReactors,
    ShipRole,
    TradeSymbol,
    WaypointType
)

class SpaceTradersAPIResponseShape(TypedDict):
    ...


class AccountShape(SpaceTradersAPIResponseShape):
    id: str
    email: str
    token: str  # TODO: Should be a JWT
    created_at: datetime


class AgentShape(SpaceTradersAPIResponseShape):
    account_id: str | None
    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int


class FactionShape(SpaceTradersAPIResponseShape):
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: list[FactionTraitSymbol]
    is_recruiting: bool


class ContractPaymentShape(SpaceTradersAPIResponseShape):
    on_accepted: int
    on_fulfilled: int


class ContractDeliverShape(SpaceTradersAPIResponseShape):
    trade_symbol: TradeSymbol
    destination_symbol: str
    units_required: int
    units_fulfilled: int


class ContractTermsShape(SpaceTradersAPIResponseShape):
    deadline: datetime
    payment: ContractPaymentShape
    deliver: ContractDeliverShape


class ContractShape(SpaceTradersAPIResponseShape):
    id: str
    faction_symbol: FactionSymbol
    type: ContractType
    terms: ContractTermsShape
    accepted: bool
    fulfilled: bool
    deadline_to_accept: datetime


class ShipRegistrationShape(SpaceTradersAPIResponseShape):
    name: str
    faction_symbol: FactionSymbol
    role: ShipRole


class ShipNavRouteLocationShape(SpaceTradersAPIResponseShape):
    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int


class ShipNavRouteShape(SpaceTradersAPIResponseShape):
    destination: ShipNavRouteLocationShape
    origin: ShipNavRouteLocationShape


class ShipNavShape(SpaceTradersAPIResponseShape):
    system_symbol: str
    waypoint_symbol: str
    route:
    departure_time: datetime
    arrival: datetime


class ShipCrewShape(SpaceTradersAPIResponseShape):
    current: int
    required: int
    capacity: int
    rotation: ShipCrewRotation
    morale: int
    wages: int

    
class ShipRequirementsShape(SpaceTradersAPIResponseShape):
    power: int
    crew: int
    slots: int


class ShipFrameShape(SpaceTradersAPIResponseShape):
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


class ShipReactorShape(SpaceTradersAPIResponseShape):
    symbol: ShipReactors
    name: str
    condition: int
    integrity: int
    description: str
    power_output: int
    requirements: ShipRequirementsShape
    quality: int


class ShipEngineShape(SpaceTradersAPIResponseShape):
    symbol: ShipEngines
    name: str
    condition: int
    integrity: int
    description: str
    speed: int
    requirements: ShipRequirementsShape
    quality: int


class ShipModulesShape(SpaceTradersAPIResponseShape):
    symbol: ShipModules
    name: str
    description: str
    capacity: int
    range: int
    requirements: ShipRequirementsShape


class ShipMountsShape(SpaceTradersAPIResponseShape):
    symbol: ShipMounts
    name: str
    description: str
    strength: int
    deposits: list[ShipMountDeposits]
    requirements: ShipRequirementsShape


class ShipCargoInventoryShape(SpaceTradersAPIResponseShape):
    symbol: TradeSymbol
    name: str
    description: str
    units: int


class ShipCargoShape(SpaceTradersAPIResponseShape):
    capacity: int
    units: int
    inventory: ShipCargoInventoryShape


class ShipFuelConsumedShape(SpaceTradersAPIResponseShape):
    amount: int
    timestamp: datetime


class ShipFuelShape(SpaceTradersAPIResponseShape):
    current: int
    capacity: int
    consumed: ShipFuelConsumedShape


class ShipCooldownShape(SpaceTradersAPIResponseShape):
    ship_symbol: str
    total_seconds: int
    remaining_seconds: int
    expiration: datetime


class ShipShape(SpaceTradersAPIResponseShape):
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

