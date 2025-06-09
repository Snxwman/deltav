from __future__ import annotations

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.waypoint import (
    WaypointModifierSymbol,
    WaypointTraitSymbol,
    WaypointType,
)
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models.chart import ChartShape


class WaypointShape(SpaceTradersAPIResShape):
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    orbitals: list[str]
    faction: FactionSymbol
    traits: list[WaypointTraitShape]
    chart: ChartShape
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    orbitals: list[str]
    faction: FactionSymbol
    traits: list[WaypointTraitShape]
    chart: ChartShape


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
