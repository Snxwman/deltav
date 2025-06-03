from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.waypoint import WaypointModifierSymbol, WaypointTraitSymbol, WaypointType
from deltav.spacetraders.models import SpaceTradersAPIResShape


class WaypointNavigateShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    """

    waypoint_symbol: str


class WaypointChartShape(SpaceTradersAPIResShape):
    """

    waypoint_symbol: str
    submitted_by: str
    submitted_on: datetime
    """

    waypoint_symbol: str
    submitted_by: str
    submitted_on: datetime


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
    chart: WaypointChartShape
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    orbitals: list[str]
    faction: FactionSymbol
    traits: list[WaypointTraitShape]
    chart: WaypointChartShape


class WaypointTraitShape(SpaceTradersAPIResShape):
    """

    symbol: WaypointTraitSymbol
    name: str
    description: str
    """

    symbol: WaypointTraitSymbol
    name: str
    description: str


class SystemWaypointModifierShape(SpaceTradersAPIResShape):
    """

    symbol: WaypointModifierSymbol
    name: str
    description: str
    """

    symbol: WaypointModifierSymbol
    name: str
    description: str


class SystemWaypointShape(SpaceTradersAPIResShape):
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    orbitals: list[str]
    orbits: str
    faction_symbol: FactionSymbol
    traits: list[WaypointTraitShape]
    modifiers: list[SystemWaypointModifierShape]
    chart: WaypointChartShape
    is_under_construction: bool
    """

    symbol: str
    type: WaypointType
    system_symbol: str
    x: int
    y: int
    orbitals: list[str]
    orbits: str
    faction_symbol: FactionSymbol
    traits: list[WaypointTraitShape]
    modifiers: list[SystemWaypointModifierShape]
    chart: WaypointChartShape
    is_under_construction: bool
