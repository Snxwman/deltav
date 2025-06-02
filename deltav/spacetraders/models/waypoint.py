from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.waypoint import WaypointModifierSymbol, WaypointTraitSymbol, WaypointType
from deltav.spacetraders.models import SpaceTradersAPIResShape


class WaypointNavigateShape(SpaceTradersAPIResShape):
    waypointSymbol: str


class WaypointChartShape(SpaceTradersAPIResShape):
    waypointSymbol: str
    submittedBy: str
    submittedOn: datetime


class WaypointShape(SpaceTradersAPIResShape):
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
    symbol: WaypointTraitSymbol
    name: str
    description: str


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
