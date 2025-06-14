from __future__ import annotations

from datetime import datetime

from pydantic import Field

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.ship import ShipType
from deltav.spacetraders.enums.system import SystemType
from deltav.spacetraders.enums.waypoint import WaypointType
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.chart import ChartShape
from deltav.spacetraders.models.faction import FactionSymbolShape
from deltav.spacetraders.models.ship import ShipShape
from deltav.spacetraders.models.waypoint import (
    WaypointModifierShape,
    WaypointOrbitalShape,
    WaypointTraitShape,
)


class ShipyardShape(SpaceTradersAPIResShape):
    """
    symbol: str
    ship_types: list[ShipType]
    transactions: list[ShipyardTransactionShape]
    ships: list[ShipShape]
    modifications_fee: int

    """

    symbol: str
    ship_types: list[ShipType]
    transactions: list[ShipyardTransactionShape]
    ships: list[ShipShape]
    modifications_fee: int


class ShipyardTransactionShape(SpaceTradersAPIResShape):
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


class JumpgateShape(SpaceTradersAPIResShape):
    """

    symbol: str
    connections: list[str]
    """

    symbol: str
    connections: list[str]


class SystemShape(SpaceTradersAPIResShape):
    """

    constellation: str
    symbol: str
    sector_symbol: str
    type: SystemType
    x: int
    y: int
    waypoints: list[SystemWaypointShape]
    factions: list[FactionSymbol]
    name: str
    """

    constellation: str
    symbol: str
    sector_symbol: str
    type: SystemType
    x: int
    y: int
    waypoints: list[SystemWaypointShape]
    factions: list[FactionSymbol]
    name: str


class SystemsShape(SpaceTradersAPIResShape):
    """

    systems: list[SystemShape] = Field(alias='data')
    """

    systems: list[SystemShape] = Field(alias='data')


class SystemSymbolShape(SpaceTradersAPIResShape):
    """

    symbol: str
    """

    symbol: str


class SystemWaypointShape(SpaceTradersAPIResShape):
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    orbitals: list[WaypointOrbitalShape]
    orbits: str
    faction: FactionSymbolShape
    traits: list[WaypointTraitShape]
    modifiers: list[SystemWaypointModifierShape]
    chart: ChartShape
    is_under_construction: bool
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    orbitals: list[WaypointOrbitalShape]
    orbits: str
    faction: FactionSymbolShape
    traits: list[WaypointTraitShape]
    modifiers: list[WaypointModifierShape]
    chart: ChartShape
    is_under_construction: bool


class SystemWaypointsShape(SpaceTradersAPIResShape):
    """

    waypoints: list[SystemWaypointShape] = Field(alias='data')
    """

    waypoints: list[SystemWaypointShape] = Field(alias='data')
