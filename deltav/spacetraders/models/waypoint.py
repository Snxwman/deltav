from __future__ import annotations
from datetime import datetime

from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.waypoint import WaypointType, WaypointTraitSymbol


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