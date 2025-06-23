from __future__ import annotations

from deltav.spacetraders.enums.waypoint import (
    WaypointModifierSymbol,
    WaypointTraitSymbol,
    WaypointType,
)
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models.chart import ChartShape
from deltav.spacetraders.models.faction import FactionSymbolShape


class WaypointShape(SpaceTradersAPIResShape):
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


class WaypointModifierShape(SpaceTradersAPIResShape):
    """

    symbol: WaypointModifierSymbol
    name: str
    description: str
    """

    symbol: WaypointModifierSymbol
    name: str
    description: str


class WaypointOrbitalShape(SpaceTradersAPIResShape):
    """

    symbol: str
    """

    symbol: str


class WaypointSymbolReqShape(SpaceTradersAPIReqShape):
    """

    waypoint_symbol: str
    """

    waypoint_symbol: str


class WaypointSymbolResShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    """

    waypoint_symbol: str


class WaypointTraitShape(SpaceTradersAPIResShape):
    """

    symbol: WaypointTraitSymbol
    name: str
    description: str
    """

    symbol: WaypointTraitSymbol
    name: str
    description: str
